# Scripts

## Production smoke test

Run a minimal set of calls against a deployed API instance.

```bash
python scripts/prod_smoke_test.py --url https://YOUR_HOST
```

If the API uses auth, set a bearer token:

```bash
export API_TOKEN=YOUR_TOKEN
python scripts/prod_smoke_test.py --url https://YOUR_HOST
```

Optional image feasibility check:

```bash
python scripts/prod_smoke_test.py --url https://YOUR_HOST --image ./some_image.jpg
```

Options:
- `--timeout` per-request timeout (seconds)
- `--insecure` disable TLS verification (not recommended)
