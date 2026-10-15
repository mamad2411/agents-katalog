---
name: happy-app-audit
description: Audit a local macOS app's telemetry / reporting behavior using static analysis only. Reverse-engineers an .app bundle to identify embedded SDKs (AppLog/TEA, Parfait, TTNet, mars, MMKV, Sentry, Firebase, Bugly, Umeng, etc.), mapped upload endpoints, local on-disk queues, and privacy-relevant fields — without packet capture, network requests, debugger attach, or DRM bypass. Use when user asks to investigate, audit, or reverse-engineer a macOS app for telemetry, reporting, data upload, privacy, or SDK fingerprinting. Targets /Applications, ~/Applications, /Library/Input Methods, /Library/PrivilegedHelperTools, and similar local install paths.
metadata:
  author: iamzhihuix
  version: "0.1.0"
---

# Happy App Audit

Static-only macOS app telemetry auditor. Produces a markdown report describing what an installed `.app` bundle reports, to whom, how often (inferred), and what it leaves on disk.

## When to invoke

Invoke when the user says any of: "审计 / 调查 / 看看 / 拆 / 逆向 / 上报 / 埋点 / 隐私 / 抓 SDK" combined with a `.app` path or app name. Also invoke when given paths under `/Applications`, `~/Applications`, `/Library/Input Methods`, or `/Library/PrivilegedHelperTools`.

Do **NOT** invoke for: source-code repos, web sites, mobile (iOS/Android) packages — this skill is macOS-bundle specific.

## Hard rules (non-negotiable)

- **Read only.** No `curl/wget/nc/dig` against discovered endpoints. No `lldb attach`, `dtrace`, `fs_usage`, `tcpdump`, `mitmproxy`, `frida`. No Keychain reads. No DRM bypass. No memory dump.
- **Allowed commands only.** See `references/safe_commands.md`. If a step seems to need something outside the whitelist, stop and tell the user instead of improvising.
- **Privacy by default.** In every output file, scrub `device_id`, `uid`, `session_id`, `email`, IDFV, IDFA, JWT, and any 16+ hex blob to `<redacted:N>` (keep length, drop content).
- **Scope cap.** Refuse a single invocation that targets more than 5 apps. Refuse paths under `/System/`, `/usr/libexec/`, `/private/var/db/com.apple.*`. Those are OS components, not third-party telemetry targets.

## Runtime

`{baseDir}` = directory of this SKILL.md.

All scripts are bun + TypeScript. Resolve runtime as: prefer `bun` in PATH, otherwise `npx -y bun`. If neither exists, abort with a one-line install hint.

```bash
# Smoke check
bun --version  ||  npx --version  ||  echo "Need bun (recommended) or npx"
```

## Workflow — 6 phases, in order

Each phase has: **Goal → Inputs → Commands → Output → Stop conditions**. Do not skip ahead. Do not interleave.

### Phase 0 — Scope confirm

**Goal.** Lock the target list to ≤5 valid `.app` paths.

**Inputs.** Whatever the user said — could be a path, a name, or "the input methods I have installed."

**Commands.**
- If user gave a path → verify it exists and ends with `.app`
- If user gave a name → search a fixed list:
  ```bash
  /Applications         (depth 2)
  ~/Applications        (depth 2)
  /Library/Input Methods (depth 1)
  /Library/PrivilegedHelperTools  (depth 1)
  ```
- Reject anything under `/System/`, `/usr/libexec/`, `/private/var/db/com.apple.*`

**Output.** A list `target_apps[]` with absolute paths.

**Stop.** If the list is empty, ask the user once. If >5, ask which to keep.

### Phase 1 — Metadata snapshot

**Goal.** Per app, capture the immutable surface: bundle id, version, signing, entitlements, network policy, embedded frameworks.

**Inputs.** `target_apps[]` from Phase 0.

**Commands.** Run `scripts/snapshot_app.ts`:
```bash
bun {baseDir}/scripts/snapshot_app.ts <app-path> --out <workdir>/meta.json
```

The script collects:
- `plutil -p <app>/Contents/Info.plist`
- `codesign -dv --entitlements - <app>` (stderr)
- `find <app>/Contents/Frameworks -maxdepth 3 -name '*.dylib' -o -name '*.framework'`
- `otool -L <main-binary>`
- `file <main-binary>` for arch
- Sizes via `du -sh`

**Output.** `<workdir>/meta.json` with: `bundle_id`, `version`, `sandboxed`, `arbitrary_loads`, `ats_exceptions[]`, `entitlements_summary[]`, `frameworks[]` (each: name, path, size_bytes, archs).

**Stop.** If `bundle_id` cannot be read → abort, app is malformed.

### Phase 2 — Strings preprocessing

**Goal.** Turn raw `strings` of every embedded binary into bucketed markdown that fits in context.

**Inputs.** `meta.json::frameworks[]`.

**Commands.**
```bash
bun {baseDir}/scripts/classify_strings.ts <workdir>/meta.json --out <workdir>/strings/
```

For each binary, the script runs `strings -a -n 6` and sorts each line into one of:
- `urls` — anything matching `https?://`
- `domains` — bare hostnames
- `paths` — `/Library/...`, `~/Library/...`, container-relative paths
- `sql` — `CREATE TABLE`, `INSERT INTO`, `SELECT ... FROM`
- `events` — looks like an event name (`/^[a-z][a-z0-9_]{8,80}$/` with at least one underscore)
- `keys` — base64 / hex blobs ≥ 24 chars (kept count + first 12 chars only, never full)
- `noise` — discarded

**Output.** `<workdir>/strings/<binary-name>.{urls,domains,paths,sql,events}.md` (the `keys` bucket holds only counts + redacted previews).

**Stop.** If a binary is >200 MB → skip it and emit a warning line, do not OOM.

### Phase 3 — SDK fingerprint matching

**Goal.** Identify which third-party SDKs are present and how confident.

**Inputs.** `<workdir>/strings/`, plus `references/sdk_fingerprints.md`.

**Commands.**
```bash
bun {baseDir}/scripts/match_fingerprints.ts <workdir>/strings/ \
  --fingerprints {baseDir}/references/sdk_fingerprints.md \
  --out <workdir>/matched.md
```

The script applies each fingerprint's `tell-tale strings` regex set to the bucketed strings. A fingerprint counts as **confirmed** when its `min_hits` threshold is met (defined per fingerprint).

**Output.** `<workdir>/matched.md` with one row per SDK: name, vendor, hits, evidence file lines, status (confirmed / partial / absent).

**Stop.** If zero fingerprints confirmed AND the app embeds no third-party `.framework` → write a one-line "no telemetry detected" report and skip Phase 4-5.

### Phase 4 — Endpoint mapping

**Goal.** Build the table that answers "where does it talk to, with what protocol, for what purpose, how often?"

**Inputs.** `<workdir>/strings/*.urls.md` + `<workdir>/strings/*.domains.md` + `<workdir>/matched.md` + `references/known_endpoints.md`.

**Commands.** This phase is mostly Claude reading the files. The only mechanical step:
```bash
bun {baseDir}/scripts/match_fingerprints.ts <workdir>/strings/ \
  --fingerprints {baseDir}/references/known_endpoints.md \
  --out <workdir>/endpoints.md
```

Then **Claude** writes `<workdir>/endpoint_table.md`:
| Endpoint | SDK | Protocol | Inferred purpose | Frequency source |
|----------|-----|----------|------------------|------------------|

`Frequency source` MUST cite either: a literal interval found in `<workdir>/strings/`, or a config file found in Phase 5, or "unknown — not stated in static evidence." **Never guess.**

**Stop.** If `endpoints.md` is empty but Phase 3 confirmed an SDK → flag in the report (likely runtime-resolved hosts).

### Phase 5 — Local data dive

**Goal.** Inventory the on-disk surface that the app writes to.

**Inputs.** `meta.json::bundle_id`, plus `references/data_locations.md`.

**Commands.**
```bash
bun {baseDir}/scripts/inventory_data.ts <bundle_id> --out <workdir>/local_data.md
```

The script `find`s:
- `~/Library/Application Support/<bundle>/`
- `~/Library/Containers/<bundle>/Data/`
- `~/Library/Group Containers/group.<bundle-prefix>.*/`
- `~/Library/Caches/<bundle>/`
- `~/Library/Preferences/<bundle>.plist`
- `~/Library/Logs/<bundle>/`

For each `.sqlite*` file: `sqlite3 <file> '.schema'` and `.tables` only — **never SELECT**. For each `.mmkv` / `.json` config: list path + size, do not open.

**Output.** `<workdir>/local_data.md` with: tree of relevant paths, sizes, and SQLite schemas.

**Stop.** If user is not the file owner → skip with a note (do not prompt sudo).

### Phase 6 — Report rendering (+ optional 4:5 card)

**Goal.** Assemble the user-facing report. Optionally render a 4:5 infographic card for sharing.

**Inputs.** All prior phase outputs.

**Commands.**
```bash
bun {baseDir}/scripts/render_report.ts <workdir> \
  --template {baseDir}/templates/report.md.tmpl \
  --out ~/Documents/app-telemetry-audit/<YYYY-MM-DD>_<bundle-id>/report.md
```

When `--card` is passed to `scripts/run.ts`, the orchestrator additionally:

1. Calls `lib/card.ts::renderCardPrompt()`, which extracts top-6 SDKs (by size, with privacy-hot ones flagged red), top-6 endpoints (preferring `endpoints.md` confirmed matches with Chinese purpose labels and synthesized proto for `quic`/`-ws.` hosts), and top-5 local-data buckets (collapsed by parent dir + note, with `DoubaoIme`/`doubaoime` casing variants merged).
2. Writes the filled prompt to `<workdir>/card_prompt.md`.
3. Auto-discovers `baoyu-imagine` at `~/.claude/skills/baoyu-imagine/scripts/main.ts` (or via `BAOYU_IMAGINE_SCRIPT` env), invokes it with `--ar 4:5 --quality 2k` defaults, and writes `<workdir>/card.png`.

Pass `--no-image` to write only the prompt and skip the image call. Pass any `--image-*` flag (`--image-provider`, `--image-model`, `--image-imageSize`, etc.) to override the defaults — e.g. `--image-provider google --image-model gemini-3-pro-image-preview --image-imageSize 4K` for native nano-banana-pro 4K output.

If `baoyu-imagine` is not installed, Phase 6 still writes `card_prompt.md` and prints an install hint, but skips the PNG. The skill remains fully functional without it.

**Output.** Final markdown report. Print its absolute path. If `--card`, also `card_prompt.md` and `card.png`.

## Output layout (per app)

```
~/Documents/app-telemetry-audit/<YYYY-MM-DD>_<bundle-id>/
├── meta.json
├── matched.md
├── endpoints.md
├── endpoint_table.md
├── local_data.md
├── strings/
│   └── <binary>.{urls,domains,paths,sql,events}.md
├── card_prompt.md          # only if --card requested
└── report.md               # the deliverable
```

Working files (`strings/`, intermediate `*.md`) are kept by default — they are the audit trail. Pass `--clean` to delete them after `report.md` is written.

## Quick start

```bash
# Single app, full audit (markdown report only)
bun {baseDir}/scripts/run.ts /Library/Input\ Methods/DoubaoIme.app

# Add a 4:5 share card (prompt + PNG via baoyu-imagine)
bun {baseDir}/scripts/run.ts /Library/Input\ Methods/DoubaoIme.app --card

# Card prompt only — skip image generation
bun {baseDir}/scripts/run.ts /Library/Input\ Methods/DoubaoIme.app --card --no-image

# Card with Google nano-banana-pro at 4K
bun {baseDir}/scripts/run.ts /Library/Input\ Methods/DoubaoIme.app --card \
  --image-provider google \
  --image-model gemini-3-pro-image-preview \
  --image-imageSize 4K

# Multiple apps in one go (capped at 5)
bun {baseDir}/scripts/run.ts /Library/Input\ Methods/DoubaoIme.app /Applications/Foo.app
```

`scripts/run.ts` is a thin orchestrator that calls Phases 1→6 in sequence. Use it for the common case. Use individual phase scripts only when iterating.

### `--card` flag surface

| Flag | Purpose | Default |
|------|---------|---------|
| `--card` | Render `card_prompt.md` AND `card.png` | off |
| `--no-image` | With `--card`: write prompt, skip PNG | off |
| `--image-provider` | baoyu-imagine provider (`google`, `openai`, `replicate`, `dashscope`, …) | provider auto-selected |
| `--image-model` | Model id within the provider | provider default |
| `--image-ar` | Aspect ratio | `4:5` |
| `--image-size` | Explicit `WxH` | from `--image-quality` / provider |
| `--image-quality` | `normal` or `2k` | `2k` |
| `--image-imageSize` | Google/OpenRouter `1K`/`2K`/`4K` | from `--image-quality` |
| `--out` | Override output root | `~/Documents/app-telemetry-audit/` |

Any `--image-*` flag implicitly enables `--card`.

## Relevant references

- `references/safe_commands.md` — command whitelist + rationale
- `references/sdk_fingerprints.md` — SDK detection rules (12+ SDKs MVP)
- `references/known_endpoints.md` — domain → product reverse lookup
- `references/data_locations.md` — typical on-disk layout per vendor
- `references/methodology_examples.md` — two worked examples (WeType, DoubaoIme)
- `templates/report.md.tmpl` — final report skeleton
- `templates/card_prompt.md.tmpl` — 4:5 visual card prompt skeleton

## Failure modes Claude should NOT do

- Do not paraphrase strings into "looks like X" without quoting the literal evidence line + file path
- Do not infer frequencies from SDK names — only from literal numbers in strings or config files
- Do not run any binary inside the target app
- Do not open `.sqlite` content — only schemas
- Do not write a report when Phase 3 found nothing — write the short "no telemetry detected" note instead
- Do not invent endpoints from training memory; if the URL is not in `<workdir>/strings/`, it does not go in the table

## Verification (when developing this skill)

Smoke test on `/Library/Input Methods/DoubaoIme.app` and confirm the report covers:
- Frameworks: `applogrs`, `Parfait`, `bytenn`, `onnxruntime`, `sscronet`, `TTNet`, `ime_net_sdk`, `sami`
- Endpoints: at least 3 of `ime.doubao.com/obric/ime/cloud/convert`, `log-klink.zijieapi.com`, `ime-gw.oceancloudapi.com`, `frontier-audio`
- Local data: `~/Library/Application Support/DoubaoIme/Parfait/ready/685343/0/`

Regression: run on the WeType IME bundle and confirm `wetype.weixin.qq.com` + `CACHE_LOG_TBL` schema appear.

Negative: run on a small app with no third-party telemetry — must produce the short "no telemetry detected" output without inventing SDKs.
