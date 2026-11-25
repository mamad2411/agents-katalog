---
name: swh-save-code-now
description: >-
  Composer skill that submits "Save code now" requests to Software Heritage
  via JXA-driven Chrome (reusing the Anubis PoW challenge clearance), reads
  origins from a manifest file, and records the returned visit/snapshot IDs.
  Delegates no generic primitives — the JXA pattern is macOS-specific.
category: Software-Heritage
---

# SWH Save Code Now Skill (v1)

This is a **composer** skill. It automates submission of "Save code now"
requests to the Software Heritage archive using macOS JXA (JavaScript for
Automation) to drive the user's existing Google Chrome instance. This
reuses the browser's Anubis proof-of-work clearance cookie and any active
SWH session — both of which block pure HTTP clients.

***

## 1. Scope & Intent

- **In scope**:
    - Open `https://archive.softwareheritage.org/save/` in the user's Chrome
    - Wait for Anubis PoW + page load (configurable timeout)
    - Inject a page-side worker that POSTs the Save-code-now API for each origin
    - Fall back to DOM form-fill if the API endpoint is unavailable
    - Collect visit/snapshot IDs from the JSON response
- **Out of scope**:
    - Browser automation on non-macOS (use Playwright + persistent profile elsewhere)
    - Ingest verification (delegated to `swh-ingest-verify`)
    - Content hash computation or link minting (delegated to `swh-content-link-mint`)

***

## 2. Environment & Dependencies

### 2.1 Runtime
- **macOS 14+** (JXA is macOS-native)
- **Google Chrome** with an existing profile (holds Anubis clearance + SWH session)
- **Python 3.12+** (for the origin-manifest loader helper)

### 2.2 Required Setup
- Grant Terminal/iTerm Accessibility permissions (System Settings → Privacy).
- The `swh-save.jxa` script must be compiled: `osacompile -l JavaScript`.

### 2.3 Required Skill Loading
- This skill's `SKILL.md`
- [`browser-network-interception`](../../browser-network-interception/SKILL.md) (JXA/Chrome automation pattern reference)

***

## 3. Protocol

### 3.1 Step 1 — Submit Save Requests

```bash
osascript -l JavaScript .agents/skills/software-heritage/save-code-now/scripts/swh-save.jxa \
  --file .agents/skills/software-heritage/save-code-now/origins.txt

osascript -l JavaScript .agents/skills/software-heritage/save-code-now/scripts/swh-save.jxa \
  https://github.com/baneeishaque/ai-suite
```

### 3.2 Step 2 — Record Visit/Snapshot IDs

The JXA script prints a JSON array to stdout. Capture it for the audit trail:

```bash
osascript -l JavaScript scripts/swh-save.jxa \
  --file .agents/skills/software-heritage/save-code-now/origins.txt \
  | tee ai-session-exports/swh-save-$(date +%Y%m%d-%H%M%S).json
```

### 3.3 Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `<origin-url>...` | One of positional or `--file` | — | Origin URLs to submit individually |
| `--file <path>` | No | — | File with one origin per line (`#`-comments supported) |
| `--help` / `-h` | No | — | Print usage |

### 3.4 Output Contract

- **stdout**: JSON array, one object per origin:
  ```json
  [{"origin": "...", "id": 123456, "save_request_status": "accepted",
    "save_task_status": "scheduled", "snapshot_swhid": "swh:1:snp:...",
    "request_url": "/api/1/origin/save/..."}]
  ```
- **Exit 0**: All origins accepted or already scheduled
- **Exit 1**: At least one origin failed or Anubis timeout

### 3.5 Scripts

| Script | Language | Purpose |
|--------|----------|---------|
| [`scripts/swh-save.jxa`](scripts/swh-save.jxa) | JXA | macOS driver: Chrome open/wait/inject/poll |
| [`scripts/swh-save-inject.js`](scripts/swh-save-inject.js) | JavaScript | Page worker: POST /api/1/origin/save/git/url/<origin>/ + DOM fallback |
| [`scripts/swh-save.jxa.md`](scripts/swh-save.jxa.md) | Markdown | Industrial Explainer for the pair |
| [`origins.txt`](origins.txt) | Text | Canonical origin manifest (one URL per line) |

***

## 4. Edge Cases

- **Anubis still solving after LOAD_WAIT_SECONDS (default 12s)**: JXA reports
  `timed-out waiting for Save results`; the operator should let Chrome finish the
  PoW, then re-run.
- **Origin URL blocked by SWH**: Returned as `save_request_status: rejected`
  with a `note` field — not a transport error.
- **Save throttled**: HTTP non-200 in the JSON array; exit 1 so the operator notices.

***

## 5. Composition Rationale

This skill is a **composer** because the JXA + Chrome + Anubis interaction is
entirely macOS-specific; there is no generic primitive to extract. The same
Save-code-now API call is generic (POST origin/save/git/url/<url>/) and IS
reused by `swh-ingest-verify`'s `--trigger-save` flag rather than
re-implemented here.

The origin manifest (`origins.txt`) is owned by THIS skill (not a shared base)
because it is domain-specific: it lists the exact origins belonging to this
repository's SWH crawl-submission procedure.

***

## 6. Composition by Higher-Level Skills

None needed — `swh-save-code-now` is invoked manually by an operator after a
push, or optionally triggered by `swh-ingest-verify` when a push's verification
fails (origin unknown).

***

## 7. Verification

```bash
osacompile -l JavaScript -o /tmp/check.scpt scripts/swh-save.jxa && echo "jxa-compile-ok"
```

## 8. Related Skills

- [`swh-ingest-verify`](../../software-heritage/ingest-verify/SKILL.md) — composer that verifies ingest per push; can call this skill's API endpoint via its `--trigger-save` flag.
- [`swh-content-link-mint`](../../software-heritage/content-link-mint/SKILL.md) — composer for minting browseable content links from verified blobs.
- [`browser-network-interception`](../../browser-network-interception/SKILL.md) — base skill for browser network interception via JXA/Playwright (pattern reference).
