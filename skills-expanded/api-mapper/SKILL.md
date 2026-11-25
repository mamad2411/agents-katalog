---
name: api-mapper
description: >
  Reverse-engineer undocumented APIs using Chrome CDP and curl. Controls a real Chrome browser via
  Python scripts to intercept traffic, reverse-engineer JS bundles, and produce markdown docs per
  domain area in docs/apis/. Output is designed as input for a client or SDK-building agent -- complete enough
  that no browser is ever needed again. Complex flows (multi-step sequences, computed values, JS-driven behaviour) are fully
  extracted and documented with a runnable Python flow script in scripts/flows/. Use this skill
  whenever the user wants to map, reverse-engineer, document, or explore the API of a website -- even
  phrased as "figure out how X works", "what endpoints does Y use", "sniff the API", "intercept
  requests", "document the backend", or "build an SDK for". Always use for any task involving CDP
  browser automation for API research.
---

# API Mapper Skill

Map the full API surface of a target site and document it so completely that any client
implementation can replicate every behaviour without ever opening a browser.

Keep going until the entire reachable API surface is documented or a wall is hit. Use whatever
combination of browser interception, curl probing, and JS reverse-engineering the situation calls
for.

---

## Requirements

- Python 3 + pip
- Google Chrome (path must be known or discoverable)
- curl (or curl.exe on Windows)

---

## Goal

Produce a complete, reproducible map of the site's API:

- Every discovered endpoint documented with method, URL, auth requirements, request shape, and
  response shape
- Every non-trivial flow (multi-step sequences, computed values, anything beyond a plain HTTP
  call) fully reverse-engineered: the logic extracted, annotated, and implemented as a standalone
  Python script that runs without a browser
- Docs written so that someone who has never seen the site can implement a working client in
  any language from scratch using only the docs

---

## Tools

**Chrome CDP via Python** -- launch Chrome and intercept network traffic to observe what the site
actually does. Read `references/cdp-capture.md` before writing any CDP scripts.

Find the Chrome executable before writing any scripts -- read the relevant platform reference:

| OS | Reference |
|----|-----------|
| Windows | `references/chrome-windows.md` |
| macOS | `references/chrome-macos.md` |
| Linux | `references/chrome-linux.md` |

Use the CDP protocol directly via raw WebSocket. Install any needed Python packages in the repo root.

**curl** -- probe endpoints directly once discovered. Run `curl` or `curl.exe` commands as
needed; document useful results in `docs/apis/`.

**JS bundle analysis** -- when a flow requires client-side computation, download the relevant
bundles and read them. Extract and annotate the logic. See `references/js-flow-analysis.md` for
the reverse-engineering procedure.

---

## Walls -- stop and ask the user

Pause and ask the user when:

- An area requires credentials that haven't been provided. If a username and password are
  available, attempt the login flow first. If not, ask.
- A rate limit blocks an entire area.
- A CAPTCHA or bot-detection wall can't be bypassed.

Before pausing, always write current findings to `docs/apis/`. Explain clearly what is needed
to continue.

---

## Output Structure

```
repo/
├── scripts/
│   ├── flows/       <- end-to-end flow scripts, one per documented flow
│   └── *.py         <- reusable helpers (auth wrappers, path extractors, etc.)
├── artifacts/
│   └── {timestamp}/ <- one folder per session
│       ├── requests.ndjson     <- all intercepted XHR/Fetch requests, one JSON per line
│       └── bundles/            <- downloaded JS bundles
└── docs/
    └── apis/
        ├── README.md           <- index of all areas and sessions
        └── {area}.md           <- one file per domain area
```

**Session folders** use an ISO 8601 timestamp with colons and dots replaced by dashes, trimmed to
seconds: `artifacts/2025-01-15T14-30-00/`.

**Placement:** session output (captured requests and bundles) goes in
`artifacts/{timestamp}/`. Reusable scripts go in `scripts/`. Docs go in `docs/apis/`.

**Write findings to docs continuously** -- don't batch everything to the end. Update `docs/apis/`
whenever a new area is understood well enough to document.

---

## docs/apis/{area}.md

One file per domain area (auth, users, search, products, etc.). Read `references/api-doc-requirements.md`
before writing any doc file.

Each file must be complete enough to implement the area from scratch without opening a browser.

---

## scripts/flows/{flow}.py

One Python script per documented flow. Read `references/flow-script-template.md` before writing
any flow script. The script must run with no browser open.
