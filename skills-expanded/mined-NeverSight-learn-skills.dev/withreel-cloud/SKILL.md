---
name: withreel-cloud
description: Generate a product-walkthrough video of any PUBLIC website using the HOSTED WithReel service — no local install, no ffmpeg/Playwright, no API token. Give a URL + a description; it renders in the cloud (cursor motion, captions, highlights, branded intro/outro) and returns a shareable mp4 link. Use when the user wants a walkthrough / demo / feature-tour / onboarding video of a website.
---

# WithReel (hosted) — generate a walkthrough video over HTTP

The hosted service turns a public URL + a description into a cinematic
walkthrough mp4. You start a render, poll until it's done, and hand back the
video URL. Rendering takes a few minutes — it is asynchronous on purpose.

## Configuration

**None required.** The hosted service is open — no token, no setup. The commands
below default the base URL to the public deployment, so they work as-is.

Optional overrides:
- `WITHREEL_API` — point at a different deployment (defaults to `https://reelapp.withvibe.dev`).
- `WITHREEL_TOKEN` — only if a deployment has re-enabled `MCP_TOKEN`; when set,
  requests add `-H "Authorization: Bearer $WITHREEL_TOKEN"`.

## Step 1 — start the render

```bash
API="${WITHREEL_API:-https://reelapp.withvibe.dev}"
# the Authorization header is added only if WITHREEL_TOKEN happens to be set
curl -sS -X POST "$API/api/action/walkthrough" \
  -H "Content-Type: application/json" \
  ${WITHREEL_TOKEN:+-H "Authorization: Bearer $WITHREEL_TOKEN"} \
  -d '{
        "url": "https://example.com",
        "description": "Tour the landing page, then open Pricing and highlight the Pro plan",
        "audience": "first-time visitors"
      }'
# -> {"jobId":"clx...","status":"queued","message":"Rendering started — poll ..."}
```

Capture the `jobId`.

Guidance for a good video — put it in `description`:
- Be specific and ordered: name the pages/sections to visit and the one action
  to end on ("…then click Get Started"). The director follows the brief literally.
- Public pages only on the no-login path.
- To demonstrate a LOGGED-IN flow, pass **test-only** credentials as dedicated
  fields — never inline them in the description:
  `"loginUser": "test@acme.dev", "loginPass": "…"`. They are stored encrypted,
  used off-camera to sign in, and never appear in the video.

## Step 2 — poll until done

```bash
curl -sS "${WITHREEL_API:-https://reelapp.withvibe.dev}/api/action/walkthrough/$JOB_ID" \
  ${WITHREEL_TOKEN:+-H "Authorization: Bearer $WITHREEL_TOKEN"}
# working: {"jobId":"…","status":"working","stage":"Recording the walkthrough"}
# done:    {"jobId":"…","status":"done","videoUrl":"https://…/videos/<id>.mp4"}
# error:   {"jobId":"…","status":"error","error":"…"}
```

Poll every ~20s. Typical render is a few minutes; stop on `done` or `error`.
Report the `stage` to the user between polls so they see progress.

## Step 3 — deliver

On `done`, give the user the `videoUrl` (directly playable / shareable). On
`error`, relay the message and suggest a more specific description or a
different public URL.

## Notes

- The same capabilities are exposed as an MCP endpoint at `$WITHREEL_API/api/mcp`
  (tools `create_walkthrough` / `check_status`) and as an OpenAPI schema at
  `$WITHREEL_API/api/action/openapi.json` — see
  [CONNECTORS.md](https://github.com/withvibe/withreel-skill/blob/main/CONNECTORS.md)
  to wire it into Claude, Gemini, or a Custom GPT instead of calling it by hand.
- There is a global daily render cap; on HTTP 429 tell the user to retry later.
- Don't print `WITHREEL_TOKEN`.
