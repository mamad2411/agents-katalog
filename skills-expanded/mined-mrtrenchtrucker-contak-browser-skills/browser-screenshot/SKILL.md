---
name: browser-screenshot
description: Capture a screenshot of a URL using a headless Chromium service (Browserless)
---

# Browser Screenshot

When invoked, capture a screenshot of the given URL via a Browserless Chromium service running locally or in your environment.

## Inputs
- `url` -- target page (required)
- `viewport` -- `{width, height}`, default `{1920, 1080}`
- `output_path` -- local file path for the resulting PNG, default `/tmp/screenshot.png`
- `full_page` -- boolean, default `false`

## Steps
1. POST to `http://<host>:<port>/screenshot` with the URL and viewport in the request body.
2. Save the returned PNG bytes to `output_path`.
3. Reference the saved path in your reply to the user.

## Output
- File path to the PNG screenshot.

## Example invocation
```bash
curl -s -X POST http://localhost:30001/screenshot \
  -H 'Content-Type: application/json' \
  -d '{
        "url": "https://example.com",
        "options": {"type": "png", "fullPage": false},
        "viewport": {"width": 1920, "height": 1080}
      }' \
  -o /tmp/screenshot.png
```

## Notes
- Browserless `/screenshot` endpoint requires no authentication by default.
- For the full setup guide (cross-host usage, troubleshooting, generating an SOP), see `sops/SOP_Headless_Browser_Screenshot.md`.
