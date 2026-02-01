#!/usr/bin/env python3
"""Prod smoke test for QWEN API.

Runs lightweight checks against a deployed instance:
- GET /health
- POST /enhance-prompt
- POST /generate-dual-prompts
- (optional) POST /analyze-feasibility if --image is provided

Exits non-zero on failure.

Usage:
  python scripts/prod_smoke_test.py --url https://your-host

Auth:
  export API_TOKEN=... (optional)

Optional image test:
  python scripts/prod_smoke_test.py --url https://your-host --image ./test.jpg
"""

from __future__ import annotations

import argparse
import base64
import os
import time
from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str
    elapsed_s: float


def _normalize_base_url(url: str) -> str:
    url = url.strip()
    if not url:
        raise ValueError("--url is required")
    return url.rstrip("/")


def _headers(api_token: str | None) -> dict[str, str]:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if api_token:
        headers["Authorization"] = f"Bearer {api_token}"
    return headers


def _request_json(
    session: requests.Session,
    method: str,
    url: str,
    headers: dict[str, str],
    timeout_s: float,
    verify_tls: bool,
    json_body: Any | None = None,
) -> tuple[int, Any]:
    resp = session.request(
        method=method,
        url=url,
        headers=headers,
        json=json_body,
        timeout=timeout_s,
        verify=verify_tls,
    )
    try:
        data = resp.json()
    except Exception:
        data = {"_raw": resp.text}
    return resp.status_code, data


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def check_health(
    session: requests.Session,
    base_url: str,
    headers: dict[str, str],
    timeout_s: float,
    verify_tls: bool,
) -> CheckResult:
    t0 = time.time()
    status_code, data = _request_json(
        session,
        "GET",
        f"{base_url}/health",
        headers={k: v for k, v in headers.items() if k.lower() != "content-type"},
        timeout_s=timeout_s,
        verify_tls=verify_tls,
    )
    elapsed = time.time() - t0

    try:
        _assert(status_code == 200, f"/health HTTP {status_code}: {data}")
        _assert(isinstance(data, dict), f"/health expected JSON object, got: {type(data)}")
        _assert("status" in data, f"/health missing 'status': {data}")
        _assert("model_loaded" in data, f"/health missing 'model_loaded': {data}")
        # We treat /health reaching as a pass, but report model_loaded.
        model_loaded = bool(data.get("model_loaded"))
        return CheckResult(
            name="health",
            ok=True,
            detail=f"status={data.get('status')} model_loaded={model_loaded} device={data.get('device')}",
            elapsed_s=elapsed,
        )
    except Exception as e:
        return CheckResult(name="health", ok=False, detail=str(e), elapsed_s=elapsed)


def check_enhance_prompt(
    session: requests.Session,
    base_url: str,
    headers: dict[str, str],
    timeout_s: float,
    verify_tls: bool,
) -> CheckResult:
    t0 = time.time()
    payload = {
        "prompt": "woman smiling, portrait photo",
        "skip_enhancement": False,
        "lora_triggers": [],
    }
    status_code, data = _request_json(
        session,
        "POST",
        f"{base_url}/enhance-prompt",
        headers=headers,
        json_body=payload,
        timeout_s=timeout_s,
        verify_tls=verify_tls,
    )
    elapsed = time.time() - t0

    try:
        _assert(status_code == 200, f"/enhance-prompt HTTP {status_code}: {data}")
        _assert(isinstance(data, dict), f"/enhance-prompt expected JSON object, got: {type(data)}")
        _assert(data.get("success") is True, f"/enhance-prompt success=false: {data}")
        enhanced = (((data.get("data") or {}).get("enhanced")) if isinstance(data.get("data"), dict) else None)
        _assert(isinstance(enhanced, str) and enhanced.strip(), f"/enhance-prompt missing enhanced text: {data}")
        _assert(
            "woman" in enhanced.lower() or "portrait" in enhanced.lower(),
            f"/enhance-prompt output seems unexpected: {enhanced!r}",
        )
        return CheckResult(
            name="enhance-prompt",
            ok=True,
            detail=f"len={len(enhanced)} sample={enhanced[:120].replace('\n', ' ')}",
            elapsed_s=elapsed,
        )
    except Exception as e:
        return CheckResult(name="enhance-prompt", ok=False, detail=str(e), elapsed_s=elapsed)


def check_generate_dual_prompts(
    session: requests.Session,
    base_url: str,
    headers: dict[str, str],
    timeout_s: float,
    verify_tls: bool,
) -> CheckResult:
    t0 = time.time()
    payload = {
        "action": "woman dancing",
        "skip_generation": False,
        "lora_triggers": [],
    }
    status_code, data = _request_json(
        session,
        "POST",
        f"{base_url}/generate-dual-prompts",
        headers=headers,
        json_body=payload,
        timeout_s=timeout_s,
        verify_tls=verify_tls,
    )
    elapsed = time.time() - t0

    try:
        _assert(status_code == 200, f"/generate-dual-prompts HTTP {status_code}: {data}")
        _assert(isinstance(data, dict), f"/generate-dual-prompts expected JSON object, got: {type(data)}")
        _assert(data.get("success") is True, f"/generate-dual-prompts success=false: {data}")
        inner = data.get("data")
        _assert(isinstance(inner, dict), f"/generate-dual-prompts missing data: {data}")
        p1 = inner.get("prompt_1")
        p2 = inner.get("prompt_2")
        _assert(isinstance(p1, str) and p1.strip(), f"prompt_1 missing: {data}")
        _assert(isinstance(p2, str) and p2.strip(), f"prompt_2 missing: {data}")
        return CheckResult(
            name="generate-dual-prompts",
            ok=True,
            detail=f"p1={p1[:70]!r} p2={p2[:70]!r}",
            elapsed_s=elapsed,
        )
    except Exception as e:
        return CheckResult(name="generate-dual-prompts", ok=False, detail=str(e), elapsed_s=elapsed)


def check_analyze_feasibility(
    session: requests.Session,
    base_url: str,
    headers: dict[str, str],
    timeout_s: float,
    verify_tls: bool,
    image_path: str,
) -> CheckResult:
    t0 = time.time()
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "image_base64": image_b64,
        "action": "person standing",
        "skip_analysis": False,
    }

    status_code, data = _request_json(
        session,
        "POST",
        f"{base_url}/analyze-feasibility",
        headers=headers,
        json_body=payload,
        timeout_s=timeout_s,
        verify_tls=verify_tls,
    )
    elapsed = time.time() - t0

    try:
        _assert(status_code == 200, f"/analyze-feasibility HTTP {status_code}: {data}")
        _assert(isinstance(data, dict), f"/analyze-feasibility expected JSON object, got: {type(data)}")
        _assert(data.get("success") is True, f"/analyze-feasibility success=false: {data}")
        inner = data.get("data")
        _assert(isinstance(inner, dict), f"/analyze-feasibility missing data: {data}")
        score = inner.get("feasibility_score")
        _assert(isinstance(score, (int, float)), f"feasibility_score missing/invalid: {data}")
        return CheckResult(
            name="analyze-feasibility",
            ok=True,
            detail=f"score={score} risk={inner.get('hallucination_risk')}",
            elapsed_s=elapsed,
        )
    except Exception as e:
        return CheckResult(name="analyze-feasibility", ok=False, detail=str(e), elapsed_s=elapsed)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="Base URL, e.g. https://example.com")
    parser.add_argument(
        "--timeout",
        type=float,
        default=float(os.environ.get("SMOKE_TIMEOUT", "120")),
        help="Per-request timeout seconds (default: 120 or SMOKE_TIMEOUT)",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable TLS cert verification (not recommended)",
    )
    parser.add_argument(
        "--token",
        default=None,
        help="Bearer token (default: API_TOKEN env var). Use '-' to read from stdin.",
    )
    parser.add_argument(
        "--token-stdin",
        action="store_true",
        help="Read bearer token from stdin (recommended for avoiding shell history)",
    )
    parser.add_argument(
        "--image",
        default=None,
        help="Optional image path to run /analyze-feasibility",
    )

    args = parser.parse_args()

    base_url = _normalize_base_url(args.url)
    verify_tls = not args.insecure

    token = args.token if args.token is not None else os.environ.get("API_TOKEN")
    if args.token_stdin or token == "-":
        try:
            # Works with piping or interactive paste.
            token = (os.read(0, 1_000_000).decode("utf-8")).strip()
        except Exception:
            token = ""
    token = token.strip() if isinstance(token, str) else None
    hdrs = _headers(token)

    results: list[CheckResult] = []

    with requests.Session() as session:
        results.append(check_health(session, base_url, hdrs, args.timeout, verify_tls))
        results.append(check_enhance_prompt(session, base_url, hdrs, args.timeout, verify_tls))
        results.append(check_generate_dual_prompts(session, base_url, hdrs, args.timeout, verify_tls))
        if args.image:
            results.append(check_analyze_feasibility(session, base_url, hdrs, args.timeout, verify_tls, args.image))

    # Print summary
    failed = [r for r in results if not r.ok]
    for r in results:
        status = "OK" if r.ok else "FAIL"
        print(f"[{status}] {r.name} ({r.elapsed_s:.2f}s): {r.detail}")

    if failed:
        print("\nSmoke test FAILED")
        return 1

    print("\nSmoke test PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
