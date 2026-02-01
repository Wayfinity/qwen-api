#!/usr/bin/env python3
"""Test image-capable endpoints on a deployed QWEN API.

This script is meant for quick manual verification against prod/staging.
It supports endpoints that accept an image:
- POST /analyze-feasibility
- POST /image-to-video

Example:
  export API_TOKEN=...
  python scripts/test_image_endpoints.py \
    --url https://your-host \
    --image ./frame.png \
    --action "woman dancing"

To avoid putting the token in shell history:
  python scripts/test_image_endpoints.py --url https://your-host --token-stdin ...
  (paste token, then Ctrl-D)
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import time
from dataclasses import dataclass
from typing import Any

import requests


@dataclass
class CallResult:
    name: str
    url: str
    status_code: int
    elapsed_s: float
    json_data: Any


def _normalize_base_url(url: str) -> str:
    url = url.strip()
    if not url:
        raise ValueError("--url is required")
    return url.rstrip("/")


def _read_token(args_token: str | None, token_stdin: bool) -> str | None:
    token = args_token if args_token is not None else os.environ.get("API_TOKEN")
    if token_stdin or token == "-":
        try:
            token = (os.read(0, 1_000_000).decode("utf-8")).strip()
        except Exception:
            token = ""
    if token is None:
        return None
    token = token.strip()
    return token or None


def _headers(token: str | None) -> dict[str, str]:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _post_json(
    session: requests.Session,
    url: str,
    headers: dict[str, str],
    payload: dict[str, Any],
    timeout_s: float,
    verify_tls: bool,
) -> CallResult:
    t0 = time.time()
    resp = session.post(url, headers=headers, json=payload, timeout=timeout_s, verify=verify_tls)
    elapsed = time.time() - t0
    try:
        data = resp.json()
    except Exception:
        data = {"_raw": resp.text}
    return CallResult(name="POST", url=url, status_code=resp.status_code, elapsed_s=elapsed, json_data=data)


def main() -> int:
    parser = argparse.ArgumentParser(description="Test QWEN API image endpoints")
    parser.add_argument("--url", required=True, help="Base URL, e.g. https://example.com")
    parser.add_argument("--image", required=True, help="Path to an image file")
    parser.add_argument(
        "--action",
        dest="action_opt",
        default=None,
        help="Target action/prompt, e.g. 'woman dancing' (optional if provided positionally)",
    )
    parser.add_argument(
        "action",
        nargs="*",
        help="Positional alternative to --action (e.g. woman dancing)",
    )

    parser.add_argument(
        "--only",
        choices=["feasibility", "image-to-video", "both"],
        default="both",
        help="Which endpoints to call (default: both)",
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=float(os.environ.get("SMOKE_TIMEOUT", "180")),
        help="Per-request timeout seconds (default: 180 or SMOKE_TIMEOUT)",
    )
    parser.add_argument("--insecure", action="store_true", help="Disable TLS verification")

    parser.add_argument(
        "--token",
        default=None,
        help="Bearer token (default: API_TOKEN env var). Use '-' to read from stdin.",
    )
    parser.add_argument("--token-stdin", action="store_true", help="Read bearer token from stdin")

    # image-to-video options
    parser.add_argument("--skip-feasibility", action="store_true", help="Skip feasibility in /image-to-video")
    parser.add_argument("--skip-enhancement", action="store_true", help="Skip enhancement in /image-to-video")

    parser.add_argument(
        "--out",
        default=None,
        help="Optional output JSON path. Writes a combined object with all responses.",
    )

    args = parser.parse_args()

    action = (args.action_opt or " ".join(args.action)).strip()
    if not action:
        parser.error("missing action: pass --action \"...\" or provide the action as a positional argument")

    base_url = _normalize_base_url(args.url)
    verify_tls = not args.insecure
    token = _read_token(args.token, args.token_stdin)
    headers = _headers(token)

    image_b64 = _image_to_base64(args.image)

    combined: dict[str, Any] = {
        "base_url": base_url,
        "action": action,
        "image": os.path.basename(args.image),
        "results": {},
    }

    with requests.Session() as session:
        if args.only in ("feasibility", "both"):
            payload = {
                "image_base64": image_b64,
                "action": action,
                "skip_analysis": False,
            }
            r = _post_json(
                session,
                f"{base_url}/analyze-feasibility",
                headers,
                payload,
                timeout_s=args.timeout,
                verify_tls=verify_tls,
            )
            combined["results"]["analyze_feasibility"] = {
                "status_code": r.status_code,
                "elapsed_s": r.elapsed_s,
                "json": r.json_data,
            }
            print(f"/analyze-feasibility HTTP {r.status_code} ({r.elapsed_s:.2f}s)")
            print(json.dumps(r.json_data, indent=2)[:20000])
            print()

        if args.only in ("image-to-video", "both"):
            payload = {
                "image_base64": image_b64,
                "action": action,
                "skip_feasibility": bool(args.skip_feasibility),
                "skip_enhancement": bool(args.skip_enhancement),
                "lora_triggers": [],
            }
            r = _post_json(
                session,
                f"{base_url}/image-to-video",
                headers,
                payload,
                timeout_s=args.timeout,
                verify_tls=verify_tls,
            )
            combined["results"]["image_to_video"] = {
                "status_code": r.status_code,
                "elapsed_s": r.elapsed_s,
                "json": r.json_data,
            }
            print(f"/image-to-video HTTP {r.status_code} ({r.elapsed_s:.2f}s)")
            print(json.dumps(r.json_data, indent=2)[:20000])
            print()

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(combined, f, indent=2)
        print(f"Wrote: {args.out}")

    # Exit non-zero on non-2xx.
    for _, entry in combined["results"].items():
        code = int(entry.get("status_code", 0))
        if code < 200 or code >= 300:
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
