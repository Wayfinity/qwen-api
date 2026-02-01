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

To avoid putting the token in your shell history, read it from stdin:

```bash
python scripts/prod_smoke_test.py --url https://YOUR_HOST --token-stdin
```

Optional image feasibility check:

```bash
python scripts/prod_smoke_test.py --url https://YOUR_HOST --image ./some_image.jpg
```

Options:
- `--timeout` per-request timeout (seconds)
- `--insecure` disable TLS verification (not recommended)

## Image + prompt endpoint tester

Calls the endpoints that accept an image (`/analyze-feasibility` and `/image-to-video`) and prints full JSON.

```bash
export API_TOKEN=YOUR_TOKEN
python scripts/test_image_endpoints.py \
	--url https://YOUR_HOST \
	--image ./some_image.jpg \
	--action "woman dancing"
```

Avoid shell history:

```bash
python scripts/test_image_endpoints.py --url https://YOUR_HOST --image ./some_image.jpg --action "woman dancing" --token-stdin
```
