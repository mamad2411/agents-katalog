---
name: codev
description: Salesforce development workflows for sf-core backed by the sfp dev pool. Three modes — (1) implement, autonomous end-to-end build/fix on a fresh sandbox with deploy and report; (2) sandbox-fetch, grab a fresh sandbox for ad-hoc work like exploring, debugging, manual testing; (3) sandbox-open, reopen a sandbox already assigned to you. Use when the user asks to build/fix in this repo, asks for a sandbox/org, or asks to reopen one they already have.
---

# codev

Salesforce development workflows for this repo, backed by the sfp dev pool. Three modes — pick by the user's intent:

| User intent | Mode | Reference |
|---|---|---|
| "Build/fix X", "implement Y", end-to-end task | **implement** | [references/implement.md](references/implement.md) |
| "Grab me a sandbox", "give me an org for X", ad-hoc work | **sandbox-fetch** | [references/sandbox-fetch.md](references/sandbox-fetch.md) |
| "Open my sandbox", "reopen the one for X" | **sandbox-open** | [references/sandbox-open.md](references/sandbox-open.md) |

Read the matching reference file before acting. Each reference is self-contained; you do not need to read the others.

## Shared operating context (all modes)

- **CLI:** only `sfp` (sfp-pro V3, server-based) is available. `sf` and `sfdx` are NOT installed — don't try them as fallbacks. When `sfp` errors, run `sfp <cmd> --help` rather than guessing flags.
- **Repo identifier:** derive from `origin` — don't hardcode.
  ```bash
  REPO=$(git remote get-url origin | sed -E 's|\.git$||; s|^.*[:/]([^/]+/[^/]+)$|\1|')
  # e.g. flxbl-io/sf-core-staging
  ```
- **sfp config:** read from `.sfp-pro/config.json` at the repo root. Sfp auto-loads `server-url` and `server-email` — don't pass `--sfp-server-url` or `-e/--email` flags. Read `pool-tag` (and `server-email` for sandbox-open) via `jq`. If a required value is missing, surface the issue and stop — don't guess.
  ```bash
  POOL_TAG=$(jq -r '."pool-tag" // empty' .sfp-pro/config.json)
  [ -z "$POOL_TAG" ] && { echo "pool-tag missing from .sfp-pro/config.json" >&2; exit 1; }
  ```
  If `.sfp-pro/config.json` isn't present in the current directory (e.g. you're in a fresh worktree), surface that rather than silently failing — the user likely wants to run this from the main repo checkout, or symlink the config in (the **implement** mode does this automatically).
- **stdout/stderr with `--json`:** `sfp ... --json` writes JSON to stdout and logs to stderr. Do **not** redirect stderr — it corrupts the JSON.
  ```bash
  # WRONG
  sfp pool fetch ... --json 2>&1 | jq .
  # CORRECT
  sfp pool fetch ... --json | jq .
  # CORRECT — capture JSON, stderr still visible
  result=$(sfp pool fetch ... --json)
  echo "$result" | jq -r '.username'
  ```
- **Session secrets — never print to your output:** frontdoor URLs (the `https://<org>/secur/frontdoor.jsp?sid=...` form) and `sfdxAuthUrl` values contain live session credentials good for hours. Your output is captured in conversation transcripts, logs, and screenshots — printing a session URL "just once in the report" still leaks it. Open the browser via `sfp org open --targetusername <alias>` **without** `--json` — sfp opens the browser locally as a side effect and the URL never surfaces. If the user wants to open the org in a different browser later, tell them to rerun the same `sfp org open` command themselves; do not capture or paste the URL on their behalf. Never write these values to files either. Pass `sfdxAuthUrl` to `sfp org login` via stdin (`--url-stdin -`), never as an argument.
