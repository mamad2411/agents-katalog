---
name: senang-carousel-generator
description: "Generate Indonesian carousel PNG ZIPs via SenangCarousels API using Gemini BYOK."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [carousel, senangcarousels, content-creation, gemini, social-media]
created_by: agent
---

# Senang Carousel Generator

Use this skill when Basim asks to generate a carousel/Carousell/carousel image, especially phrases like:
- "generate carousel tips trick"
- "buat carousel tentang ..."
- "generate gambarnya lewat SenangCarousels API"
- "pakai API `http://43.156.20.232:8000/static/AGENTS.md`"

This workflow generates an Indonesian carousel through the SenangCarousels API, exports a ZIP of PNG slides, verifies the ZIP, and returns it as a media attachment.

## API

- Agent guide: `http://43.156.20.232:8000/static/AGENTS.md`
- Base URL: `http://43.156.20.232:8000`
- Generate endpoint: `POST /api/carousel/generate`
- Export endpoint: `POST /api/carousel/export`
- Default illustration: `http://43.156.20.232:8000/static/illustration.jpg`

## Required credential

Use Gemini BYOK from `~/.hermes/.env`:

- `GEMINI_API_KEY`
- fallback alias: `GOOGLE_API_KEY`

Do **not** print the key in terminal output or final response.

## Standard style

Follow SenangCarousels document constraints unless Basim asks otherwise:

- Indonesian language.
- Minimalist black/white style.
- `theme_colors`: `[#ffffff, #000000, #000000]` as a JSON string, but with normal double quotes in actual payload.
- `title_font`: `Playfair Display`
- `body_font`: `Plus Jakarta Sans`
- `handle_name`: `@cerita.basim.id`
- Each slide:
  - `image_url`: `http://43.156.20.232:8000/static/illustration.jpg`
  - `image_layout`: `right`
  - lowercase text
  - title is two lines separated by `\n`
  - body is line 3
  - 1–4 words per line
  - exactly one bold word per line using `**kata**`

## Workflow

### 1. If topic is vague/current

If Basim says "sesuatu yang viral hari ini", use `web_search` first. Prefer broad, useful creator/business trends over sensitive crime/accident virality. Examples:

- AI creator / AI content trend
- social media creator mindset
- TikTok/Instagram trend reports
- practical content/marketing tips

Use `date` via terminal to ground the day.

Basim-specific correction from carousel testing: do **not** use dummy evergreen slide copy when he asks for trend-based carousel examples. The slide content must be derived from current web-search signals, and if he asks for the "paling terbaru" source, prioritize articles from today by timestamp/date over merely relevant older items. For scheduled/cron carousel runs, aim slide content at the newest safe trend/news/data source available on the exact day and time the cron job runs; disclose the source/date-time in the run report, and only fall back to evergreen after stating no safe fresh source was strong enough. In the final preview message, briefly name the source/date and explain the angle. Send the preview/contact sheet here first; do not schedule to Repliz until he explicitly approves.

### 2. Generate carousel JSON

Run a Python script like this. It avoids printing secrets:

```python
import json, pathlib, urllib.request, urllib.error
API = "http://43.156.20.232:8000"

def load_key():
    env = pathlib.Path.home() / ".hermes" / ".env"
    for line in env.read_text(encoding="utf-8").splitlines():
        if line.startswith("GEMINI_API_KEY=") or line.startswith("GOOGLE_API_KEY="):
            value = line.split("=", 1)[1].strip()
            if value:
                return value
    raise RuntimeError("No GEMINI_API_KEY/GOOGLE_API_KEY in ~/.hermes/.env")

key = load_key()
payload = {
    "topic": "tips dan trik mengikuti tren ai creator yang viral hari ini tanpa kehilangan suara manusia",
    "tone": "casual",
    "num_slides": 6,
    "user_gemini_key": key,
    "user_openai_key": None,
}
req = urllib.request.Request(
    API + "/api/carousel/generate",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)
with urllib.request.urlopen(req, timeout=240) as r:
    body = r.read()
pathlib.Path("/tmp/senang_carousels").mkdir(parents=True, exist_ok=True)
pathlib.Path("/tmp/senang_carousels/api-generate.json").write_bytes(body)
```

Expected success:

- HTTP `200`
- JSON has `title`, `slides`
- slide count matches requested number.

### 3. Normalize JSON before export

After generation, enforce the standard style:

```python
import json, pathlib
API = "http://43.156.20.232:8000"
inp = pathlib.Path("/tmp/senang_carousels/api-generate.json")
carousel = json.loads(inp.read_text(encoding="utf-8"))
carousel["theme_colors"] = '["#ffffff", "#000000", "#000000"]'
carousel["title_font"] = "Playfair Display"
carousel["body_font"] = "Plus Jakarta Sans"
carousel["handle_name"] = "@cerita.basim.id"
for i, s in enumerate(carousel.get("slides", [])):
    s["position"] = i
    s["image_url"] = API + "/static/illustration.jpg"
    s["image_layout"] = "right"
    s.setdefault("subtitle", None)
    s.setdefault("visual_cue", None)
    if isinstance(s.get("title"), str):
        s["title"] = s["title"].lower()
    if isinstance(s.get("body"), str):
        s["body"] = s["body"].lower()
pathlib.Path("/tmp/senang_carousels/api-carousel-final-normalized.json").write_text(
    json.dumps(carousel, ensure_ascii=False, indent=2), encoding="utf-8"
)
```

### 4. Export ZIP and verify

```python
import json, pathlib, urllib.request, zipfile
API = "http://43.156.20.232:8000"
carousel = json.loads(pathlib.Path("/tmp/senang_carousels/api-carousel-final-normalized.json").read_text(encoding="utf-8"))
req = urllib.request.Request(
    API + "/api/carousel/export",
    data=json.dumps(carousel).encode("utf-8"),
    headers={"Content-Type": "application/json", "Accept": "application/zip"},
    method="POST",
)
with urllib.request.urlopen(req, timeout=240) as r:
    body = r.read()
zip_path = pathlib.Path("/tmp/senang_carousels/api-carousel-final.zip")
zip_path.write_bytes(body)
with zipfile.ZipFile(zip_path) as z:
    names = z.namelist()
    bad = z.testzip()
print("zip_path", zip_path)
print("zip_files", names)
print("zip_bad_file", bad)
```

Expected success:

- HTTP `200`
- `Content-Type: application/zip`
- ZIP contains slide PNGs such as `slide-1.png`, `slide-2.png`, etc.
- `zip_bad_file None`

### 5. Return result or continue to Repliz

Final response should be concise Indonesian and include:

```text
MEDIA:/tmp/senang_carousels/api-carousel-final.zip
```

Mention only key verification facts, e.g. slide count and that ZIP was valid.

If Basim replies to a generated carousel with “post/kirim ke Repliz”, treat that as approval for this artifact and use the `threads-content-and-scheduling` Repliz album workflow: extract slide PNGs from the ZIP, upload each slide to public image URLs, verify the URLs, then schedule `type: "album"` through Repliz with ordered `medias`. Report the Repliz `scheduleId` and local WIB schedule time.

For Basim trend-sourced carousel previews, see `references/basim-trend-carousel-preview-workflow.md`: source slide content from current web search, prefer today's newest safe/business-relevant article, disclose the source/date in the preview, and do not schedule until explicit approval.

## Troubleshooting

### `/generate` says API key unavailable

Check `~/.hermes/.env` contains `GEMINI_API_KEY`. Do not print the secret.

### `/generate` model errors or Gemini quota

Past observed errors:

- `models/gemini-1.5-flash is not found`
- temporary Gemini quota/high-demand errors
- Gemini free-tier quota exhausted, e.g. HTTP 500 from SenangCarousels wrapping Gemini `429`:
  - `Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests`
  - `limit: 20, model: gemini-3.5-flash`
  - `GenerateRequestsPerDayPerProjectPerModel-FreeTier`

If this happens, retry once only if the response includes a short retry delay. If daily quota is exhausted, do **not** keep retrying `/api/carousel/generate`.

Workaround: bypass `/generate` and create the CarouselCreate JSON yourself, then call `/api/carousel/export`. The export endpoint works without Gemini as long as the JSON conforms to the schema. Use the same standard style rules: 6 slides, lowercase, `theme_colors`, fonts, `@cerita.basim.id`, default illustration URL, `image_layout: right`, title line 1+2 separated by `\n`, body as line 3, exactly one bold word per line. Verify ZIP as usual. See `references/manual-json-export-fallback.md` for the known-good JSON shape, export verification, and MP4 slideshow pattern.

### Debugging a failing scheduled carousel job

If a scheduled carousel-to-Repliz job is failing or the user asks to pause while investigating:

1. Pause the cron job first and verify it is disabled/paused.
2. Probe `/static/AGENTS.md` and `/static/illustration.jpg` to confirm the API host is reachable.
3. Run a minimal `/api/carousel/generate` request with a safe test topic and redacted secret handling; write response to `/tmp/...` but do not print keys.
4. If generate succeeds, normalize and test `/api/carousel/export`; verify ZIP with `zipfile.testzip()`.
5. Only state root cause after the probe actually ran. If terminal approval or policy blocks the probe, say the investigation is blocked rather than guessing.

### `/export` Playwright error

Past server issue:

```text
BrowserType.launch: Executable doesn't exist ...
current: mcr.microsoft.com/playwright/python:v1.44.0-jammy
required: mcr.microsoft.com/playwright/python:v1.60.0-jammy
```

If this returns, the SenangCarousels server/container needs Playwright image update. Do not claim export succeeded. Optionally create a local fallback ZIP only if Basim accepts or if task requires a usable artifact despite API failure; label it as fallback, not API output.

Basim production-cron pitfall: do **not** silently replace the normal SenangCarousels visual output with a local/off-template fallback and auto-schedule it. If the fallback would materially change the usual carousel look, send a preview/audit first and wait for explicit approval before Repliz scheduling. For `@ceritaberkelas`-style requests, keep the normal visual template by default and adapt only content mechanics unless Basim explicitly requests that visual experiment.

### Security

The API is plain HTTP on a raw IP. Treat this as user-approved for this workflow because Basim explicitly provided the endpoint and Gemini key for SenangCarousels. Still avoid sending unrelated secrets, and never echo the key.
