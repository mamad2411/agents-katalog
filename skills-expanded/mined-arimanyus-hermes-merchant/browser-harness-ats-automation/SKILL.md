---
name: browser-harness-ats-automation
description: Automate job applications on ATS platforms (Ashby, Greenhouse, Workday) using browser-use/browser-harness with CDP. Covers iframe session management, file upload, hidden checkbox handling, and known reCAPTCHA/S3 blockers.
---

# browser-harness-ats-automation

Automate job applications on ATS platforms (Ashby, Greenhouse, Workday) using [browser-use/browser-harness](https://github.com/browser-use/browser-harness) with CDP.

## Critical architecture: ATS forms live in iframes

Modern ATS platforms (Ashby, Greenhouse) render application forms inside **cross-origin iframes**. This is the root cause of most automation failures. You MUST attach to the iframe session before any DOM operations.

### Standard setup

```bash
# Start Xvfb + Chrome with remote debugging
Xvfb :99 -screen 0 1280x800x24 &
export DISPLAY=:99
/usr/bin/chromium-browser --headless --no-sandbox --disable-gpu \
  --remote-debugging-port=9222 \
  --remote-debugging-address=127.0.0.1 &
sleep 3

# Install browser-harness
git clone https://github.com/browser-use/browser-harness.git
cd browser-harness && uv sync && uv tool install -e .

# Start daemon
cd browser-harness && nohup uv run bu-daemon &
sleep 2
```

### CDP socket pattern

The socket is at `/tmp/bu-default.sock`. Use this helper inside `uv run browser-harness <<'PY'`:

```python
import socket, json

def cdp(method, session_id=None, **params):
    sk = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sk.connect("/tmp/bu-default.sock")
    r = {"method": method, "params": {"session_id": session_id, **params} if session_id else params}
    sk.sendall((json.dumps(r) + "\n").encode())
    data = b""
    while not data.endswith(b"\n"):
        chunk = sk.recv(1 << 20)
        if not chunk: break
        data += chunk
    sk.close()
    return json.loads(data).get("result", {})

FRAME_ID = "DFF978A387F9E4D8D8A8AF1EF7385A08"
sid = cdp("Target.attachToTarget", targetId=FRAME_ID, flatten=True).get("sessionId")
```

### Finding the right iframe target

```python
targets = cdp("Target.getTargets")
for t in targets.get("result", {}).get("targetInfos", []):
    if t["type"] in ("page", "iframe"):
        print(f"  {t['type']}: {t.get('url','')[:80]} id={t['targetId']}")
```

### File upload in iframes

CSS selectors (`querySelector`) often fail inside iframes. Walk the DOM tree instead:

```python
def find_file_inputs_in_frame(session_id):
    doc = cdp("DOM.getDocument", session_id=session_id, depth=-1)
    queue = [doc["root"]]
    found = []
    while queue:
        node = queue.pop(0)
        al = node.get("attributes", [])
        attrs = {}
        for i in range(0, len(al) - 1, 2):
            attrs[al[i]] = al[i + 1]
        if node.get("nodeName") == "INPUT" and attrs.get("type") == "file":
            found.append({"nodeId": node["nodeId"], "name": attrs.get("name", "")})
        queue.extend(node.get("children", []))
    return found

# Load resume path from profile.yaml
import yaml, os
from pathlib import Path
cfg = yaml.safe_load(Path("profile.yaml").read_text())
resume_path = os.path.expanduser(cfg["resume"]["path"])

for inp in find_file_inputs_in_frame(sid):
    if 'resume' in inp['name'].lower() or inp['name'] == '_systemfield_resume':
        cdp("DOM.setFileInputFiles", session_id=sid,
            files=[resume_path], nodeId=inp["nodeId"])
```

### Hidden work-authorization checkboxes (Ashby)

Ashby uses hidden checkboxes at `y=0` in the DOM, controlled by visible Yes/No button overlays. Use CDP mouse clicks in the frame session:

```python
# Work auth "No" — coordinates will differ per viewport; take a screenshot to confirm.
cdp("Input.dispatchMouseEvent", session_id=sid, type="mousePressed",
    x=348, y=1282, button="left", clickCount=1)
cdp("Input.dispatchMouseEvent", session_id=sid, type="mouseReleased",
    x=348, y=1282, button="left", clickCount=1)

# Visa "No"
cdp("Input.dispatchMouseEvent", session_id=sid, type="mousePressed",
    x=348, y=1415, button="left", clickCount=1)
cdp("Input.dispatchMouseEvent", session_id=sid, type="mouseReleased",
    x=348, y=1415, button="left", clickCount=1)
```

Answer selection is driven by `cfg["work_authorization"]` from `profile.yaml`.

### Submit and intercept server response

```python
cdp("Runtime.evaluate", session_id=sid, expression="""
(function() {
  window._gqlResponse = null;
  const origFetch = window.fetch;
  window.fetch = function(req) {
    const url = typeof req === 'string' ? req : req.url;
    if (url && url.includes('non-user-graphql')) {
      return origFetch.apply(this, arguments).then(async r => {
        const clone = r.clone();
        const text = await clone.text();
        window._gqlResponse = {status: r.status, body: text};
        return r;
      });
    }
    return origFetch.apply(this, arguments);
  };
})()
""", returnByValue=True, awaitPromise=True)

cdp("Runtime.evaluate", session_id=sid,
    expression="(function(){const b=Array.from(document.querySelectorAll('button')).find(b=>b.innerText&&b.innerText.includes('Submit'));if(b){b.click();return 'clicked'}})()",
    returnByValue=True, awaitPromise=True)
import time; time.sleep(5)

resp = cdp("Runtime.evaluate", session_id=sid,
    expression="JSON.stringify(window._gqlResponse || 'no response')",
    returnByValue=True, awaitPromise=True)
print(resp.get("result", {}).get("value"))
```

## ATS split strategy — the core automation pattern

Not all ATS platforms are equal. This is the most important thing learned from trial:

| ATS Type | Browser automation | Email automation | Best path |
|----------|--------------------|------------------|-----------|
| **Ashby** | BLOCKED (reCAPTCHA v3 + S3 upload rejection) | Works via `careers@` | Email only — browser always fails |
| **Greenhouse** | RISKY — React custom `select__input` dropdowns can't be filled via CDP; text fields work via the React-value-setter | Works via `careers@` | **Email first** — only use browser when no `careers@` available |
| **Workday / Workable** | Checkbox reCAPTCHA, untested | Works via `careers@` | Email |
| **Naukri** | Blocked (login wall) | — | Manual only |
| **Indeed** | Blocked (login wall) | — | Manual only |
| **LinkedIn Easy Apply** | Blocked (complex JS) | — | Manual only |

### Decision tree for each job

```
Is it Greenhouse?
  → YES: Try browser (checkbox reCAPTCHA is solvable)
  → NO: Is it Ashby?
      → YES: Send email to careers@ OR mark failed with manual_apply_url
      → NO: Is it a known company with careers@ email?
          → YES: Send email
          → NO: Mark failed with manual_apply_url
```

Email addresses live in `profile.yaml` under `careers_emails`. Extend as you discover more.

### Queue data structure for failed jobs (Slack reporting)

Every job that can't be applied to must carry these fields so the Slack reporter can render a clickable follow-up link:

```json
{
  "status": "failed",
  "failure_reason": "ashby_recaptcha_v3_blocked",
  "manual_apply_url": "https://jobs.ashbyhq.com/cohere/75c0032c-..."
}
```

Without `manual_apply_url`, Slack reports are useless for manual follow-up.

## Known blockers

### Ashby: Invisible reCAPTCHA v3
- Ashby runs invisible reCAPTCHA v3 on every submission.
- Scores the browser session — headless Chrome scores ~0.0 → auto-rejected.
- Error: `RECAPTCHA_SCORE_BELOW_THRESHOLD`.
- **Not solvable in pure automation.** Use the email path or collect for manual apply.

### Ashby: S3 pre-signed URL fetch fails
- After upload, Ashby fetches the file from S3 via a pre-signed URL — fails from headless.
- Error: `Failed to fetch (ashbyhq-infra-prd-main-app-uploaded-files-us-east-1.s3.us-east-1.amazonaws.com)`.
- File IS correctly set in the DOM. The rejection is server-side on headless clients.

### Greenhouse: Checkbox reCAPTCHA — solvable
- Greenhouse uses checkbox reCAPTCHA v2, clickable programmatically via CDP.
- Form lives in an iframe — use the same `Target.attachToTarget` pattern as Ashby.
- Verified: Together AI applications submitted successfully via browser.
- Strategy: visit job page → click "Apply" → fill form in iframe → click reCAPTCHA checkbox → submit.
- Email path also works and is faster — prefer email for bulk.

### Greenhouse application steps

```python
goto("https://job-boards.greenhouse.io/COMPANY/jobs/JOBID")

click("//button[contains(text(),'Apply')]")

# Attach to the form iframe
targets = cdp("Target.getTargets")
frame_id = next((t["targetId"] for t in targets["result"]["targetInfos"]
                 if "apply" in t.get("url", "").lower()), None)
sid = cdp("Target.attachToTarget", targetId=frame_id, flatten=True).get("sessionId")

# Fill fields + click checkbox reCAPTCHA in the frame session
cdp("DOM.setFileInputFiles", session_id=sid, files=[resume_path], nodeId=nodeId)
# ... type text fields ...
cdp("Input.dispatchMouseEvent", session_id=sid, type="mousePressed",
    x=CAPTCHA_X, y=CAPTCHA_Y, button="left", clickCount=1)
cdp("Input.dispatchMouseEvent", session_id=sid, type="mouseReleased",
    x=CAPTCHA_X, y=CAPTCHA_Y, button="left", clickCount=1)
```

## Orchestrator cron pattern

For a fully automated job-hunt pipeline, use three crons:

1. **`job-scraper`** (`*/15 * * * *`) — searches jobs, scores against `profile.yaml`, appends to the queue.
2. **`job-orchestrator`** (`*/30 * * * *`) — reads queue, applies Tier 1 / Tier 2, updates statuses, appends to `applied.json`.
3. **`job-slack-reporter`** (`0 */6 * * *`) — reads `applied.json`, posts a digest to Slack.

The Slack reporter MUST include failed jobs with `manual_apply_url` so you can batch-apply manually.

### CDP bridge down — fallback strategy

When the browser CDP bridge is unavailable (connection refused, or `Failed to connect via CDP to wss://*.cdp1.browser-use.com`):

1. **Greenhouse**: email `careers@COMPANY.com` — works reliably.
2. **All others**: mark failed with a full `manual_apply_url`.

CDP WebSocket URL pattern for browser-use: `wss://HASH.cdp1.browser-use.com/devtools/browser/ID`. The older `ws://127.0.0.1:9222/devtools/browser/UUID` pattern is stale. The daemon socket is `/tmp/bu-default.sock`.

### Failure-reason conventions (for Slack reporting)

Every failed job MUST carry these fields:

```json
{
  "status": "failed",
  "failure_reason": "manual_apply_required | search_page | ashby_recaptcha_v3_blocked | recaptcha_blocked | email_bounced",
  "manual_apply_url": "<original job URL>"
}
```

- **`search_page`** — Indeed job URL is a search/listing page, not a direct job; requires manual search on Indeed.
- **`manual_apply_required`** — known-blocked platform (Naukri, LinkedIn Easy Apply, etc.) or URL is a search page.
- **`ashby_recaptcha_v3_blocked`** — Ashby invisible reCAPTCHA; not solvable programmatically.

## Reliable automation path

- **Email applications** (Tier 2): send directly to `careers@company.com` via SMTP 587 TLS. Bypasses all ATS form complexity. `smtplib` with a Gmail app password is verified working.
- **Manual link collection**: for Ashby/Greenhouse jobs blocked by reCAPTCHA, collect the job URL in a `manual_apply` list and report to Slack for human review.

## Verified working

- `goto()`, `click()`, `type_text()`, `screenshot()`, `wait_for_load()` helpers
- `DOM.setFileInputFiles` via iframe session
- CDP `Input.dispatchMouseEvent` for hidden checkbox buttons
- Gmail SMTP port 587 TLS
- Slack reporter via `deliver: "slack"` in cron
