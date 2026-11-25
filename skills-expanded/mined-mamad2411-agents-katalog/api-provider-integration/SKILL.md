---
name: api-provider-integration
version: 1.0.0
description: >-
  Systematic methodology for integrating third-party APIs when docs are unreliable
  or incomplete. Covers endpoint discovery, model naming, auth patterns, retry
  strategies, and prompt sanitization. Includes provider-specific quirks as references.
category: devops
metadata:
  hermes:
    triggers:
      - api integration
      - third-party api
      - provider setup
      - api client
      - kie.ai
      - fal.ai
      - api endpoint discovery
    tags: [api, integration, providers, video-generation, image-generation]
    related_skills: [local-business-revenue, ai-model-router-gateway]
---

# API Provider Integration

Systematic methodology for integrating third-party APIs when the docs don't match
the real API. Learned from integrating kie.ai (Seedance 2.0 + GPT Image 2),
and directly applicable to any provider (fal.ai, Poyo, Higgsfield, etc.).

## Firefox MCP Diag: When `--remote-debugging-port` Serves httpd.js

On this machine, Firefox 153+ started with `--remote-debugging-port` may serve **httpd.js** (Firefox's built-in HTTP server) instead of the WebDriver BiDi or CDP debugging protocol. The `firefox_connect` MCP tool returns `connected: false`.

**Detection:** `curl http://127.0.0.1:{port}/` returns an httpd.js welcome page (not a CDP/BiDi endpoint).

**Workarounds:** geckodriver, `computer_use` + Chrome, or direct API calls.
Full verified geckodriver WebDriver HTTP recipe (session create, navigate,
inspect, cleanup, profile caveats): [references/geckodriver-webdriver-fallback.md](references/geckodriver-webdriver-fallback.md).

## The Discovery Methodology

When docs and reality diverge, don't guess — test. This 5-step flow takes ~30 min
and saves hours of client code debugging:

### Step 1: Scrape the docs HTML for real endpoint paths

Docs pages are often rendered client-side. Grab the raw HTML and grep for paths:

```bash
curl -sL "https://docs.kie.ai/market/gpt/gpt-image-2-text-to-image" \
  -H "User-Agent: Mozilla/5.0" | grep -oP '/api/v1/[a-zA-Z/]+'
```

This reveals the **actual** endpoint paths the API uses, often different from
the docs page URL structure.

### Step 2: Test with curl before writing any client code

Test the smallest possible request to confirm endpoint + auth + body shape:

```bash
# Test model name and endpoint
curl -s -X POST "https://api.kie.ai/api/v1/jobs/createTask" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"<model_name>","input":{"prompt":"test"}}'
```

Check: does it accept the model name? Does it 422 (wrong shape) or 500 (model wrong)?

### Step 3: Discover the model name format

Docs URLs, sidebar labels, and API model fields often use **different naming**:

| Docs URL path | Sidebar label | API `"model"` field |
|---------------|---------------|---------------------|
| `market/gpt/gpt-image-2-text-to-image` | "GPT Image 2 - Text to Image" | `gpt-image-2-text-to-image` |
| `market/bytedance/seedance-2` | "Bytedance Seedance 2.0" | `bytedance/seedance-2` |

**Always test the model name with curl.** Never assume the docs path = API field.

### Step 4: Discover GET vs POST for query endpoints

Docs often show POST-like examples for everything. Test both:

```bash
# Test POST
curl -s -X POST "https://api.kie.ai/api/v1/jobs/recordInfo" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"taskId":"xxx"}'

# Test GET with query param
curl -s "https://api.kie.ai/api/v1/jobs/recordInfo?taskId=xxx" \
  -H "Authorization: Bearer $API_KEY"
```

**Kie gotcha:** recordInfo is GET (docs implied POST).

### Step 5: Run a real generation and trace the full flow

Before writing the client, run one cheap generation end-to-end:
1. createTask → get task ID
2. Poll until state=success/fail
3. Parse resultJson for URLs
4. Verify the URL downloads

This catches state-value gotchas (e.g., `"fail"` not `"failed"`), result
extraction shapes, and temp-URL expiration before you build polling logic.

## Common API Pitfalls (Provider-Agnostic)

| Pitfall | What to check | Example |
|---------|---------------|---------|
| Resolution casing | Test with curl; some APIs reject `2k` but accept `2K` | GPT Image 2: `2K` only |
| Model name ≠ docs path | Test the exact string from docs vs the API | `gpt-image-2-text-to-image` not `gpt/gpt-image-2...` |
| GET vs POST for queries | Always try both if docs are ambiguous | Kie recordInfo is GET |
| State values | Check for `"fail"` vs `"failed"` vs numeric codes | Kie uses `"fail"` |
| Temp URL expiration | Download immediately after generation, or use signed URL endpoint | tempfile.aiquickdraw.com expires ~10 min |
| Non-ASCII in prompts | Some APIs reject arrows, em-dashes, smart quotes | Sanitize: `→` `—` `"` `'` |
| Transient Internal Errors | Retry 3× with backoff; ~30% failure rate is normal on some APIs | Kie GPT Image 2 |
| **Client swallows HTTP errors** | If the client returns `[]`/None on any exception, outages look like "no data" / "not found". Test the endpoint directly with curl/httpx to see the real status | Serper key out of credits → rank-check silently reported `source: "none"`, empty SERP (the 400 `Not enough credits` was hidden) |
| **Credential presence ≠ validity** | Readiness/health checks that test `bool(key)` pass with dead keys. Use a live probe call (one real request) instead | Readiness said `credential_serper: pass` while every rank check failed on HTTP 400 |

## Diagnosing Silent API Failures

When an integration stops returning data but doesn't raise errors, the client is
likely swallowing exceptions. Bypass it and probe the endpoint directly with the
configured key:

```python
import httpx
from landlord.config import get_api_key  # or os.getenv / your config loader
key = get_api_key('serper_api_key')
r = httpx.post('https://google.serper.dev/search',
               json={'q': 'test', 'gl': 'us', 'hl': 'en', 'num': 1},
               headers={'X-API-KEY': key, 'Content-Type': 'application/json'},
               timeout=20)
print(r.status_code, r.text[:300])
```

Interpretation:
- **400 with a message like "Not enough credits"** → prepaid quota exhausted. Top up, don't debug code.
- Any other non-200 → invalid/rotated key or network egress issue.
- **Regression signature:** when a monitoring snapshot timeline flips from live data (`serper`, `not_found`) to empty (`source: "none"`), that's the API dying — NOT the monitored object dropping out. Don't report "site lost its ranking / data went missing" until you've confirmed the API itself still returns 200.

## Client Design Pattern

```python
# The pattern that works across providers:

class ProviderClient:
    def _create_task(self, model, payload): ...     # POST createTask
    def _query_task(self, task_id): ...              # GET/poll
    def _wait_for_result(self, task_id, timeout): ... # poll loop with state check
    def _get_download_url(self, file_url): ...       # temp → signed URL
    def generate(self, ad_spec): ...                 # retry loop (3×) around create+wait
```

Key decisions:
- **Retry loop** around the whole create→wait flow (not just the HTTP call)
- **Exponential backoff** (5s, 10s, 15s) between retries
- **State check** handles both `"fail"` and `"failed"` variants
- **Result extraction** tries multiple paths (`resultJson.resultUrls[0]`, `output.videoUrl`, etc.)
- **Download URL conversion** as the final step before returning to caller

## Prompt Sanitization Template

```python
def sanitize_prompt(prompt: str) -> str:
    """Strip non-ASCII that some API providers reject."""
    return (prompt
        .replace("\u2192", "->").replace("\u2190", "<-")   # arrows
        .replace("\u2014", "-")                              # em-dash
        .replace("\u2019", "'").replace("\u2018", "'")       # smart single quotes
        .replace("\u201c", '"').replace("\u201d", '"')       # smart double quotes
    )
```

Test before applying: run one request with the sanitized prompt, one without.
If the sanitized version succeeds and the raw version fails, the sanitizer is needed.

## Provider-Specific References

- [Kie.ai API quirks](references/kie-api-discovery.md) — full endpoint/model/state details from live testing
- [Local OpenAI-compatible inference endpoints](references/local-openai-compatible-endpoints.md) — faster-whisper (STT) + Qwen3TTS quirks: Bearer-key auth on local endpoints, model-id dash gotchas (`qwen3-tts` not `qwen3tts`), first-request model downloads, TTS->STT round-trip verification
- fal.ai, Poyo, Higgsfield: test independently with the same 5-step methodology
