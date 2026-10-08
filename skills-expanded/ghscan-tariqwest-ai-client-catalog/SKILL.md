---
name: add-to-catalog
description: Add AI desktop IDEs, workspace apps, or terminal coding CLIs to the AI CLI client catalog.
---

# Add to Catalog

Add AI desktop IDEs, workspace apps (e.g. OpenHands, Claude), or terminal coding CLIs to the deduplicated [catalog master table](../../../catalog-master-table.md).

> **Target:** `catalog-master-table.md` is the canonical spreadsheet (90 deduplicated IDs after 2026-08 peer pass, §3.1-shaped plus `Vendor`/`Category`/`Version`/`License` + `homepage_url`/`github_url`). This skill parses a single URL/path and upserts one row via the helpers below. The long-form `ai-cli-client-catalog.md` may be updated secondarily for prose, but the master table is the source of truth.

## Overview

This skill accepts a **single source** of AI client tooling and integrates the extracted entries into the catalog document. Supported inputs:

1. **GitHub repository URL** — scans READMEs, package files, and CLI manifests
2. **Downloads / releases page URL** — parses release assets and distribution info
3. **Directory or listing URL** — scrapes structured lists of agents or CLIs
4. **Local directory path** — recursively inspects project files for CLI/IDE metadata

It auto-detects the agent type (desktop IDE, workspace app, terminal CLI), version, distribution method, and source links, then appends or updates catalog entries with minimal redundancy.

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input` | string | no* | Single GitHub repo URL, downloads page URL, directory/listing URL, or local path. *Required if `inputs` not set. If the string contains multiple URLs/entries (newline-separated, comma-separated, or space-separated), it is auto-split into a batch — see **Merged batch behavior** below. |
| `inputs` | string[] | no* | Batch list — each element is a tool name, URL, or listing-page URL to scrape. *Required if `input` not set. When present (or when `input` contains >1 entry), the skill automatically runs the batch pipeline. Also accepts `@/path/to/file` (one entry per line). |
| `type` | string | no | Override agent category: `desktop-ide`, `workspace-app`, or `terminal-cli` (applies to all entries in batch mode) |
| `update` | boolean | no | If true, update existing catalog entries for matched IDs (default: `false`) |
| `dryRun` | boolean | no | If true, only report what would be added/skipped without writing `catalog-master-table.md` |
| `override` | boolean | no | If true, allow web UI/SaaS or cloud-agent candidates that the agent would otherwise exclude by the gating criteria (default: `false`) |

\* `input` or `inputs` must be provided (exactly one). The skill auto-detects batch: if `inputs` is given, or `input` contains multiple entries, or a single listing-page URL that scrapes to many candidates, execution routes to `helpers/batch.js`.

**Examples (single):**
```json
{"input": "https://github.com/openai/codex", "type": "terminal-cli"}
{"input": "https://github.com/abrokenshark/ClueNote/releases", "update": true}
{"input": "/Users/tariqwest/Developer/my-ai-tool"}
```
**Examples (batch — now via same skill):**
```json
{"inputs": ["https://github.com/openai/codex", "https://github.com/anomalyco/opencode", "Windsurf"]}
{"input": "https://github.com/openai/codex\nhttps://github.com/anomalyco/opencode\nWindsurf"}
{"inputs": ["https://github.com/ai-for-developers/awesome-ai-coding-tools"], "dryRun": true}
{"inputs": ["@/tmp/urls.txt"]}
```

> **Merged batch behavior:** `add-to-catalog` and `batch-add-to-catalog` are now a single skill. Any call with `inputs` array, or with `input` that contains commas/newlines/spaces yielding >1 token or a scrapable listing page (`awesome`, `dev.to`, etc.), is automatically expanded via `helpers/batch.js` (dedup + vet + enrich). See that helper for scrape logic. Single URL/name continues down the single-item `url-parser.js → md-table.js` path.

## Helpers

| Helper | Path | Purpose |
|--------|------|---------|
| **URL parser** | [`helpers/url-parser.js`](./helpers/url-parser.js) | Parse a single `input` URL/path into 16-col master-table fields (`id`, `display_name`, `vendor`, `category`, `version`, `license`, `homepage_url`, `github_url`, …). Handles `github.com/<owner>/<repo>` (capitalized `OpenAI`/`Sourcegraph` etc.), `/releases`, and known download hosts (`jules.google.com→jules`, `zed.dev→zed`, `bolt.new→bolt-new`, `tabnine.com→tabnine-cli`, `mistral.ai→codestral`, etc.) → stable `id` + `vendor` + `type`. Closed download pages set `github_url: "—"`. Enriches by fetching README/package when network available. CLI: `node helpers/url-parser.js "https://github.com/QwenLM/qwen-code"` |
| **MD table helper** | [`helpers/md-table.js`](./helpers/md-table.js) | Reliable pipe-table row manipulation (md-spreadsheet style). No regex row edits — treats `catalog-master-table.md` as a spreadsheet: `Spreadsheet.fromMarkdown(md)` → `upsert(row, {key:'id'})` → `toMarkdown()`. Handles escaped `\|`, inline-code pipes, alignment rows, and preserves surrounding doc. Must `upsert` with **full 16-col row** (partial upsert clears other columns). CLI: `node helpers/md-table.js --file ../../../catalog-master-table.md --upsert '{"id":"`my-tool`","display_name":"My Tool",...}'` |
| **Batch helper** | [`../batch-add-to-catalog/helpers/batch.js`](../batch-add-to-catalog/helpers/batch.js) | Batch orchestration (now invoked automatically by this skill): expand `inputs`/`input`-with-many into flat candidates, dedup against `catalog-master-table.md` + within batch, vet peer type, then upsert. Uses `curl` + `bun.webview` fallback for JS-rendered listicles (see `../batch-add-to-catalog/helpers/scrape-webview.js`). CLI: `node ../batch-add-to-catalog/helpers/batch.js --inputs '["https://github.com/openai/codex","Windsurf"]' [--dry-run]` — you do **not** need to invoke the separate skill; this skill calls it when it detects a batch. |

## Instructions

0. **Auto-route single vs batch (merged behavior):** Before step 1, normalize the call:
   ```js
   // pseudo: helpers/route.js
   let normalizedInputs;
   if (inputs) normalizedInputs = inputs; // array → batch
   else if (input) {
     // if `input` is a single listing-page URL that will scrape to many, treat as batch of 1 (scrape will expand)
     // otherwise split on newlines/commas; trim empties; if >1 token → batch
     const parts = input.split(/[\n,]+/).map(s=>s.trim()).filter(Boolean);
     // also split on whitespace if multiple https:// present
     const urls = input.match(/https?:\/\/\S+/g);
     if (parts.length > 1 || (urls && urls.length > 1)) normalizedInputs = parts.length>1 ? parts : urls;
   }
   if (normalizedInputs) {
     // batch path — delegate to batch helper (same dedup/vet/enrich as before)
     // node .agents/skills/batch-add-to-catalog/helpers/batch.js --inputs '<JSON>' [--type X] [--update] [--dry-run]
     // then skip single-item steps below and go to Verification/Report.
   } else {
     // single-item path — continue to step 1
   }
   ```
   Explicit `inputs` array always → batch. Plain `input` with commas/newlines or multiple URLs → batch (split). A lone `input` (one URL/name, even if it is a listing page that later scrapes to many) also routes through batch so scrape logic runs — caller need not know.

1. **Parse the `input` URL/path** with the URL parser (single-item path):
   ```bash
   node .agents/skills/add-to-catalog/helpers/url-parser.js "$input" [--type terminal-cli|desktop-ide|workspace-app]
   # → { parsed, row }  (16-col shaped: id, vendor, category, version, license, homepage_url="—" for closed, etc.)
   ```
   Source-type detection:
   - **URL with github.com/<owner>/<repo>** → fetch repo metadata + README + package files (enrich `version`/`distribution`/`description`); `vendor` is capitalized via `ownerMap` (`openai→OpenAI`)
   - **URL ending in /releases** → parse release assets for binaries, packages, SHAs
   - **HTTPS URL to a listing/download page** (e.g. `jules.google.com`, `zed.dev`, `bolt.new`, `tabnine.com`, `mimo.xiaomi.com`) → via `knownIds` map to stable `id` (`jules`, `zed`, `bolt-new`, `tabnine-cli`, `codestral`, `jetbrains-ai`) + correct `vendor`/`type` (`Workspace app` for `bolt.new`/`lovable`/`v0`/`replit`, `Desktop IDE` for `zed.dev`, `Desktop IDE plugin` for `tabnine`/`jetbrains`/`codestral`); closed pages set `github_url="—"` (not `""`)
   - **Local path (starts with `/` or `.`)** → inspect recursively
   If the network is unavailable, the parser still derives `id`/`homepage_url`/`github_url` from URL tokens and flags `needsFetch: true` for a later enrich pass. Enrich `Vendor`/`Category`/`Version`/`License` manually before upsert.
2. Extract/reconcile these fields per agent/tool (when available):
   - `id` — de-duplicated handle (slugified from name; backticked in the table, e.g. `` `qwen-code` ``)
   - `display_name` — display name
   - `vendor` — inferred from host/owner (e.g. `Qwen/Alibaba`, `Xiaomi/MiMo`, `ByteDance`)
   - `type` — desktop IDE, workspace app, or terminal CLI (auto-detected unless overridden)
   - `category` — `code` / `agent` / `host` / `library+server` (from §3.5)
   - `version` — latest release or package version
   - `description` — short purpose statement
   - `distribution` / `install` — `npx`, `uvx`, or platform binaries (Darwin/ARM64, Linux/x86_64, Windows)
   - `homepage_url` / `github_url` — canonical source links (separate columns; `—` when closed/no GH)
   - `license` — `MIT`/`Apache-2.0`/`Closed`/etc.
3. **Vet peer type** — ensure the candidate is actually the same class as the catalog. Catalog scope is **IDEs, desktop clients, terminal CLIs, agents/harnesses** for AI coding. Reject otherwise:
   - `type` must be one of: `Terminal CLI` (incl. `(+ ACP)`), `Desktop IDE`, `Desktop IDE plugin`, `Workspace app`, `ACP Adapter`, `Library+Server`, `Desktop app`. Any other (e.g. pure library, model weights, hosting infra, non-coding chatbot, CI runner) → skip with reason `not-a-peer-type`.
   - `category` should be `code`/`agent`/`host`/`library+server`; unknown → skip `not-a-peer-category`.
   - Description/README must signal AI coding (keywords: `code`, `agent`, `IDE`, `CLI`, `harness`, `ACP`, `assistant`, `autocomplete`, `completion`, `LLM`, `AI` + `code`). If README/package manifest lacks these and no install binary, skip `not-a-peer-scope`. When in doubt, fetch homepage/README and look for `code`/`agent`/`CLI` in title/description; err on rejection and flag `needs-manual-review`.
   - **Web UI / SaaS / cloud-agent gating.** The catalog tracks installable, locally-runnable AI coding clients (terminal CLIs, desktop IDEs, local workspace apps, ACP adapters) rather than browser-only SaaS tools or cloud-hosted coding agents. If a candidate's primary interface is a web UI with no local installable binary, or it is a cloud-only agent that runs in a hosted sandbox/IDE rather than on the user's machine, exclude with reason `excluded-web-ui-saas` or `excluded-cloud-agent`. This gating can be overridden by the user by passing `override: true`, by confirming when asked (e.g. "add it anyway"), or by overriding `type` to a local peer and confirming. When `override` is not set and the gating is ambiguous, ask the user before adding.
4. **Deduplicate against catalog** — before any write:
   ```bash
   node .agents/skills/add-to-catalog/helpers/md-table.js --file catalog-master-table.md --list | python3 -c "import json,sys; ids={r['id'].strip('\`').lower() for r in json.load(sys.stdin)}; print('qwen-code' in ids)"
   ```
   Or programmatic: `sheet.find(parsed.id)` using `helpers/md-table.js`. If a normalized `id` already exists:
   - if `update=false` (default) → skip with reason `already-in-catalog (use update:true)`;
   - if `update=true` → merge: load existing row, overlay enriched fields, then `upsert`. Never create a second row with same `id`.
5. Match against the catalog's layer model:
   - **Terminal CLI** — goes in the CLI-Tools section
   - **Workspace app** — maps to ACP session or promptpipe backend
   - **Desktop IDE** — noted as IDE plugin / extension host
6. **Upsert the master table** `catalog-master-table.md` **via the MD table helper** (do not hand-edit rows — and never do a *partial* upsert, it clears other columns):
   ```bash
   # Single row (must supply full 16-col row — merge parsed + enriched):
   node .agents/skills/add-to-catalog/helpers/md-table.js \
     --file catalog-master-table.md \
     --upsert '{"id":"`qwen-code`","display_name":"Qwen Code — Qwen/Alibaba","vendor":"Qwen/Alibaba","category":"code","type":"Terminal CLI","binary":"`qwen`","acp_launch":"…","headless_print":"…","trust_bypass":"…","distribution_install":"…","version":"0.21.9","license":"Apache-2.0","baseurl_config":"…","popularity":"26.9k★","homepage_url":"https://github.com/QwenLM/qwen-code","github_url":"https://github.com/QwenLM/qwen-code"}'
   # Or from a JSON file (full row):
   node .agents/skills/add-to-catalog/helpers/md-table.js --file catalog-master-table.md --upsert-file ./new-row.json
   # List current rows (for dedup check):
   node .agents/skills/add-to-catalog/helpers/md-table.js --file catalog-master-table.md --list
   ```
   Programmatic (merge existing row to avoid clearing):
   ```js
   const { Spreadsheet } = require('./.agents/skills/add-to-catalog/helpers/md-table.js');
   const md = fs.readFileSync('catalog-master-table.md','utf8');
   const sheet = Spreadsheet.fromMarkdown(md);
   const existing = sheet.find(parsed.id.replace(/`/g,'')); // undefined if new
   const full = { ...(existing ? (({__raw,__line,...r})=>r)(existing) : {}), ...toTableRow(parsed, enriched) };
   sheet.upsert(full).writeFile('catalog-master-table.md');
   ```
   **Generate `uid` for new rows.** If the row is new, generate an 8-character stable `uid` (uppercase A-Z + 0-9) formatted as `XXXX-XXXX` for readability, e.g. `PAVY-M44Y` (`crypto.randomBytes(8).toString('hex').slice(0,8).toUpperCase()` is not safe — use an alphabet and modulo, then insert a dash between the first 4 and last 4 characters). Include it in the upsert object; do not leave the `uid` column empty.
6a. **Sync CLI surface mapping** — If the upserted master row is a `Terminal CLI` (`type` includes `terminal_cli`) or has a CLI `binary`, also add or update the corresponding row in `cli-surface-mapping-table.md`:
   ```bash
   node .agents/lib/sync-cli-surface.js --id qwen-code
   # or for multiple terminal CLI additions/updates:
   node .agents/lib/sync-cli-surface.js --ids qwen-code,codex,opencode
   # dry-run:
   node .agents/lib/sync-cli-surface.js --id qwen-code --dry-run
   ```
   This helper reads the master row and upserts a `cli-surface-mapping-table.md` row with the same `id`, `uid`, `command` (from `binary`), `created`, `updated`, and `project_status`; unknown CLI surface columns are left as `—` or filled from known patterns. Run it after every terminal CLI addition or update, including renames (`update: true`).
   Also append/update the corresponding prose entry in `ai-cli-client-catalog.md` (§14 for external/Chinese-lab sources). If `update=true` and the ID exists, the helper replaces the existing table row in place (deduped by `ID`).
7. Run `git --no-pager diff --check` on `catalog-master-table.md`, `ai-cli-client-catalog.md`, and `cli-surface-mapping-table.md` (if modified) and strip any trailing-whitespace or tab issues from the new rows. The helper's CLI does this automatically and exits non-zero on violations. Then verify `Vendor`/`Category`/`Version`/`License` are not `"—"` for open repos, and that `homepage_url`/`github_url` are present (`github_url: "—"` for closed SaaS).
8. Report: number of entries added/updated, any entries skipped (with reason: `already-in-catalog`, `not-a-peer-type`, `not-a-peer-category`, `not-a-peer-scope`, `needs-manual-review`, `excluded-web-ui-saas`, `excluded-cloud-agent`), and the catalog sections modified. Include the `homepage_url`/`github_url` mapping and the 16-col verification (`Vendor | Category | Version | License`) for review.

## Validation

If you add a release-asset table, verify each URL resolves (HEAD request). If any asset returns 404 or times out, flag the entry for manual review.

## Verification (after implementation)

```bash
# URL parser smoke test
node .agents/skills/add-to-catalog/helpers/url-parser.js "https://github.com/QwenLM/qwen-code"
node .agents/skills/add-to-catalog/helpers/url-parser.js "https://github.com/XiaomiMiMo/MiMo-Code"
node .agents/skills/add-to-catalog/helpers/url-parser.js "https://www.warp.dev/agent-cli"

# MD table helper smoke test (read-only)
node .agents/skills/add-to-catalog/helpers/md-table.js --file catalog-master-table.md --list | head -n 20

# Round-trip probe (writes then reverts — must preserve doc and diff --check clean)
cp catalog-master-table.md /tmp/_probe.md
node .agents/skills/add-to-catalog/helpers/md-table.js --file /tmp/_probe.md --upsert '{"id":"`_probe`","display_name":"Probe","type":"Terminal CLI","homepage_url":"https://example.com","github_url":"https://github.com/example/probe"}'
node .agents/skills/add-to-catalog/helpers/md-table.js --file /tmp/_probe.md --remove _probe
diff -u catalog-master-table.md /tmp/_probe.md && echo "round-trip OK"
git --no-pager diff --check -- catalog-master-table.md ai-cli-client-catalog.md
```
