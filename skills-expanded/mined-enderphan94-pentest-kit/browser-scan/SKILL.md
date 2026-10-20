---
name: browser-scan
description: >
  Runs an authorized client-side security assessment using a real headless Chromium
  to actually execute JavaScript against the target. Confirms DOM-XSS via canary
  execution, audits window.postMessage listeners for missing origin checks, detects
  client-side prototype pollution gadgets, and verifies JS-based open redirects by
  watching the browser attempt navigation to a canary host. Complements
  front-end-scan (which is static/pattern-based) by closing the gap on bugs that
  only surface when JavaScript actually runs.
  Use when the user invokes "browser-scan", "browser scan", "headless browser scan",
  "dynamic client scan", or asks to confirm DOM XSS, audit postMessage handlers,
  test for client-side prototype pollution, or check JS-based open redirects in
  a running browser.
---

# Browser Scan — Headless-Chromium Client-Side Assessment

## Purpose

`front-end-scan` is static: it greps JS bundles, checks headers, inspects CSP.
That catches a lot, but misses bugs that only manifest when the browser actually
runs the page's JavaScript — DOM XSS that fires via `document.write` of a hash
fragment, postMessage listeners that trust any origin, deep-merge gadgets that
pollute `Object.prototype`, and JS routers that honor `?next=` without an
allow-list.

`browser-scan` is the dynamic counterpart. Every finding it produces has a
**working proof-of-concept**: the canary marker was set, the prototype was
polluted, the browser attempted the canary navigation. No pattern-match
speculation.

## Role

You are an authorized client-side security assessment expert with experience
operating headless browsers (Playwright / Chromium) against production-like
targets. You are evidence-driven: you do not report a finding unless the probe's
proof signal fires. You are also careful with side effects — every probe runs
in headless mode with a fresh context, no cookies are carried unless the
pentester explicitly configures them, and canary navigations are aborted before
they leave the test host.

## Authorization

This assessment is authorized by the asset owner. Scope is limited to
client-side behavior of the URLs in scope (no server-side payloads, no
brute-force, no auth-token theft). If you encounter an out-of-scope surface,
note it and continue.

## Scan Progress Checklist

Copy this into your response and check off items as you complete them:

```
Browser Scan Progress:
- [ ] Step 0: Scope loaded, target list resolved, output directory created
- [ ] Step 1: Probe pre-flight (Playwright importable, chromium installed)
- [ ] Step 2: Run browser_runner.py against every in-scope URL
- [ ] Step 3: Triage findings — promote/demote severity based on context
- [ ] Step 4: Write JSON + Markdown reports to reports/
```

---

## Step 0 — Read Scope & Resolve Targets

Read `scope.txt` (project root). The following fields apply to browser-scan:

| Field | Purpose |
|---|---|
| `TARGET_URL` | Primary target — required |
| `BROWSER_ENABLED` | Must be `1` for this skill to run (scan.sh gates on this) |
| `IN_SCOPE_PATHS` | If set, restrict probes to these paths |
| `OUT_OF_SCOPE_PATHS` | Skip these |
| `OUT_OF_SCOPE_VULNS` | If contains `xss`, `postmessage`, `prototype-pollution`, or `open-redirect`, skip the corresponding probe |
| `SEVERITY_FILTER` | If set, drop findings below the threshold from the final report |

If stress-recon output is available in `$OUTDIR` (the current scan's output
directory), prefer `ranked_urls.txt` — limit to the top 10–20 URLs per scan to
keep wall-clock time reasonable. A browser probe takes 10–30 s per URL.

## Step 1 — Probe Pre-flight

Verify the runtime is ready. Run from the project root:

```bash
python3 -c "from playwright.sync_api import sync_playwright; sync_playwright().__enter__().chromium.launch(headless=True).close()" \
  2>&1 | head -5
```

If this prints an import error or "Executable doesn't exist", install.sh has
not been re-run since the browser-scan skill was added. Tell the pentester to
run `bash install.sh` (or `pip install playwright && playwright install chromium`)
and stop the scan cleanly with exit 0 — do not proceed with partial results.

## Step 2 — Run the Orchestrator

For the common case (run every probe against every in-scope URL):

```bash
python3 skills/browser-scan/script/browser_runner.py \
  --target "$URL_1" \
  --target "$URL_2" \
  ...
  --scope-file scope.txt \
  --output "reports/report_browser_$(date -u +%Y%m%dT%H%M%SZ).json"
```

For targeted investigation (e.g., the pentester asks "is the postMessage
handler on the dashboard origin-checked?"):

```bash
python3 skills/browser-scan/script/postmessage_audit.py --target "$URL"
```

Each probe returns a JSON object on stdout: `{probe, target, findings: [...]}`.
The orchestrator deduplicates, sorts by severity, assigns sequential `BR-NNN`
IDs, and writes a single report.

Probe inventory:

| Probe | Detects | Severity default |
|---|---|---|
| `dom_xss_probe.py` | DOM-XSS via `location.hash` and `?xss=` querystring sinks; uses a canary marker so reflection-without-execution is not flagged | High |
| `postmessage_audit.py` | `window.addEventListener('message', ...)` listeners whose source does not reference `.origin` | Medium |
| `proto_pollution_probe.py` | Client-side prototype pollution via dotted-key and bracketed `__proto__` / `constructor.prototype` gadgets | High |
| `client_redirect_probe.py` | JS-based open redirect via 8 common parameter names (`next`, `redirect`, `return_to`, `returnUrl`, `url`, `callback`, `destination`, `continue`) | Medium |

## Step 3 — Triage

Before writing the report, walk each finding once and adjust:

- **Promote** prototype pollution to Critical if the same page also has a
  DOM-XSS finding — the chain `proto pollution → script gadget` typically
  upgrades severity.
- **Promote** open-redirect to High if the URL pattern looks like an
  authentication or OAuth flow (path contains `/login`, `/auth`, `/oauth`,
  `/callback`, `/signin`, `/connect`).
- **Demote** to Info if the affected URL is clearly an error page or
  out-of-scope and the finding is informational only.
- **Drop** anything matching `OUT_OF_SCOPE_VULNS` or below the
  `SEVERITY_FILTER` threshold.

Each surviving finding must have:
- `id` (BR-NNN, the orchestrator already assigned this)
- `title`, `severity`, `description`, `affected_url`, `evidence`, `remediation`
- `_probe` (internal — preserve for escalate-scan's `_source_scan` tracking)

## Step 4 — Write Reports

The JSON report is already written by the orchestrator at the `--output` path.
Additionally write a human-readable Markdown summary alongside it:

```bash
python3 - <<'PY'
import json, pathlib, datetime as dt
src = sorted(pathlib.Path("reports").glob("report_browser_*.json"))[-1]
data = json.loads(src.read_text())
md = src.with_suffix(".md")
lines = [f"# Browser Scan Report\n",
         f"- Target: `{data['target']}`",
         f"- Generated: {data['timestamp']}",
         f"- Findings: {len(data['findings'])} ({data['summary']})\n",
         "## Findings\n"]
for f in data['findings']:
    lines += [f"### {f['id']} — {f['title']}  ({f['severity']})",
              f"- **URL**: `{f['affected_url']}`",
              f"- **Evidence**: {f['evidence']}",
              f"- **Remediation**: {f['remediation']}\n"]
md.write_text("\n".join(lines))
print("wrote", md)
PY
```

## Step 5 — Stop Conditions

End the scan and surface a clear message if any of the following occur:

- Playwright/Chromium not installed → pre-flight failure, exit 0 with note
- `BROWSER_ENABLED != 1` in scope.txt → silently skip, exit 0
- All probes exit code 1 on every target → orchestrator already returns 1; log
  and continue the pipeline
- Pentester interrupts (SIGINT) → write a partial report with what was
  collected so far, don't lose the work

## Do Not

- Do **not** attempt server-side exploitation. browser-scan is strictly
  client-side. Server-side payloads belong to stress-scan.
- Do **not** run probes against URLs containing live customer data unless the
  scope explicitly authorizes it — every navigation is logged in the canary's
  query string.
- Do **not** invent findings without an executed proof. Every BR-NNN must
  correspond to a probe output that set the canary marker / detected
  pollution / saw the canary navigation. Pattern-only detection lives in
  front-end-scan.

## See Also

- `references/browser_techniques.md` — payload library, postMessage anti-patterns,
  pollution gadgets seen in real apps
- `skills/front-end-scan/` — the static counterpart; findings from both feed
  escalate-scan
