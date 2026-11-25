---
name: yesmem-cap-builder
description: Use when a user wants to persist a working REPL snippet, bash command, or multi-step workflow as a reusable cap (CAP.md tool) available in future sessions. Trigger on save_cap, cap_store, auto_active, capblob-pipe, "/build-tool", "make this reusable", or when a one-off shell pipeline is about to be retyped a third time.
---

# YesMem Cap Builder

A cap is a CAP.md file (YAML frontmatter + `## Purpose` + `## Scripts` + optional `## Database` + optional `## Actions`) that yesmem persists as a learnings row, deploys to `~/.claude/caps/<name>/CAP.md`, and re-injects into future sessions via the proxy. Caps are how an ad-hoc REPL command becomes a session-spanning, queryable tool.

This skill is the **discovery surface**. Side-files in this directory hold the depth — open them when you actually need them.

## Side-files (open on demand)

| File | Open when |
|------|-----------|
| `recipes.md` | You're about to build a cap and want a working template to copy |
| `api-reference.md` | You're calling `save_cap`/`get_caps`/`activate_cap`/`cap_store`/`cap_proposal_decide` and need the exact param shape |
| `gotchas.md` | A cap fails on activate, save_cap silently stores garbage, `sh()` returns truncated output, or anything else surprises you |

## External references

- **Cap-Spec (canonical format)**: `https://github.com/carsteneu/cap-spec` — treat as authoritative for CAP.md structure, frontmatter rules, and the v1.1 multi-script format. **Note**: spec.md is at v1.1-draft, but `cap-spec/examples/*/CAP.md` are still v1.0 — see `gotchas.md` "Cap-spec format drift" before copying.
- **Working caps to copy from**: `caps/bundled-caps/cap_collect/CAP.md` (current, v1.1) and `caps/bundled-caps/reddit/CAP.md` are the freshest in-repo references. `wiki_export` and `reddit_fetch` no longer ship as bundled caps, so their paths are dead.
- **yesmem CLI for caps**: `yesmem query --format objects` (read-only SQL across `yesmem.db`/`messages.db`/`caps.db`/`runtime.db`, projection-wrapped JSON), `yesmem json` (gojq-style filter pipeline, no `--slurpfile`), `yesmem cap-blob-put` (chunked blob ingest, bypasses the 30 KB `sh()` wall). Bash-runtime caps wire these together — see `recipes.md` "Cap that pipes `yesmem query` into `yesmem json`" and `api-reference.md` "yesmem CLI surface for caps".

## When to build a cap

- Working command/script the user will reach for again next week
- Multi-step REPL sequence likely to recur
- Output deserves to be queryable later (search, aggregate, meta-analyze)
- Trigger phrases: "save this", "build a cap", "make this reusable", "/build-tool"

## When NOT to build a cap

- One-off command for a specific URL or task today only
- Trivial bash under 20 chars
- Wrapping an existing MCP tool 1:1 with no new logic — call the MCP tool directly
- Data isn't worth persisting

When in doubt: ask the user if they'd reach for this next week. If not, don't build it.

## The CAP.md format (Cap-Spec v1.1)

```markdown
---
name: my_cap
description: One-line, written as discovery bait for future Claude.
version: 1
tags: [web, fetch]
scope: user
auto_active: false
tested: true
---

## Purpose

What it does, when to use it, expected inputs/outputs, edge cases.

## Scripts

### my_cap
kind: tool
schema: {"type":"object","properties":{"url":{"type":"string"}},"required":["url"]}

```javascript
async ({url}) => { ... }
```

## Database

```sql
CREATE TABLE cap_my_cap__hits (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  url TEXT,
  fetched_at INTEGER,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```
```

**Hard rules** (parser rejects these — non-negotiable):

- `name`: `[a-z][a-z0-9_]{0,63}` — lowercase, underscores, no dashes. Must match the directory name.
- `## Scripts` is required, must contain at least one `### <name>` subsection. v1.0 single-`## Script` form is rejected.
- Each `### <name>` has exactly one code fence. Optional `kind: tool|handler`, `runtime: repl|bash`, `schema: <single-line JSON>`, `sandbox: none|standard|strict` between heading and fence (block ends at first blank line, prose, or fence).
- `kind: tool` + `runtime: bash` REQUIRES `schema:` — no derivation possible from bash. Use `schema: {"type":"object"}` for no-arg bash tools.
- `kind: handler` MUST NOT have a `schema:` field — handlers aren't called with structured args.
- `schema:` must be single-line JSON. Multi-line YAML schemas are not supported in v1.1.
- `scope: project` + `sandbox: none` → parser error. Project-scoped caps must use `standard` or `strict` (or omit).
- Cap-store table names use `cap_<capname>__<tablename>` prefix; daemon adds the prefix automatically when you call `cap_store({capability, table})`.

## save_cap real shape (Cap-Spec v1.1)

The current in-repo skill documents `handler_repl: '...', handler_bash: '...'` as separate fields. **That is the legacy shape.** The canonical v1.1 shape is `scripts:` as a stringified JSON array:

```javascript
await mcp__yesmem__save_cap({
  name: 'my_cap',
  description: 'One-line discovery bait',
  scripts: JSON.stringify([
    { name: 'my_cap', kind: 'tool', runtime: 'repl',
      body: handlerSource,
      schema: JSON.stringify({type:'object', properties:{...}}) }
  ]),
  tags: 'web,fetch',
  tested: true,
  test_date: '2026-05-01',
  auto_active: false
});
```

`scriptsFromSaveCapParams` (`internal/daemon/handler_caps_helpers.go`) still accepts the legacy `handler_repl`/`handler_bash` fields for backward compatibility, but per-script kind/runtime overrides, multi-script bundles, and per-script sandbox profiles only work via `scripts:`. Always write new caps in the `scripts:` shape. See `api-reference.md` for return values, supersede semantics, and the inline-body-size pitfall.

## The 6 steps

### 1. Define

| Field | Notes |
|---|---|
| `name` | snake_case, unique, findable |
| `description` | one sentence, written as discovery bait — not "fetches web data" but "Fetch top N HN stories and persist into cap_hn_top__stories, queryable by score/title/date" |
| inputs | name + type + required? |
| persists data? | yes → step 2b; no → skip to 3 |
| scope | start minimal. 3-5 fields you'll actually query on. Adding fields later is cheap; un-creeping a 20-column escape-hell cap is not. |

### 2a. Handler

Pick `runtime: repl` (rich, JS in REPL VM) or `runtime: bash` (portable, callable outside REPL, scheduler-friendly). Most caps are one or the other. Multi-script bundles can mix both — see `recipes.md` "Multi-script cap".

REPL handler skeleton:

```javascript
async ({limit = 10}) => {
  const raw = await sh(`curl -s --max-time 15 "${URL}"`, 20000);
  return { count: 1, items: JSON.parse(raw) };
}
```

REPL VM allowlist: `sh, cat, rg, rgf, gl, put, gh, shQuote, log, str, haiku, REPO`, `await Read({...})`, `await Write({...})`, `await Edit({...})`, `await Bash({...})`, `await mcp__yesmem__*({...})`. **No** `process.env`, **no** `require`, **no** `fetch`, **no** `file()` global. See `gotchas.md` "REPL VM allowlist hallucinations".

Hard rules:
- Bash single-line; chain with `&&` or `;`. No heredoc, no multi-line.
- Timeouts always: `sh(cmd, 20000)`, `curl --max-time 15`.
- Output > 30 KB → capblob-pipe. See `recipes.md` "Cap that needs capblob-pipe".

### 2b. Database (if persisting)

```javascript
await mcp__yesmem__cap_store({
  capability: 'my_cap',
  action: 'create_table',
  table: 'hits',
  columns: JSON.stringify([
    {name:'url', type:'TEXT'},
    {name:'fetched_at', type:'INTEGER'}
  ])
});
```

`id`, `created_at`, `updated_at` are auto-added — listing them yields `duplicate column name`.

Upsert semantics: `data` with `id` → UPDATE; without `id` → INSERT (new row, new auto-id, new timestamps). Time-series capture works by omitting `id`.

Quotas: 10 tables per cap, 10 000 rows per table, 64 KB per cell. WHERE clauses are sanitized — see `gotchas.md` "sanitize_where blocked keywords".

### 3. Test

Run the handler with real inputs in the REPL before saving:

```javascript
const r = await handler({limit: 3});
r;                                              // shape OK?
await mcp__yesmem__cap_store({capability:'my_cap', action:'query', table:'hits'});
await handler({limit: 3});                      // re-run: idempotent? no duplicates?
```

Verify output shape, persisted rows, dedup on re-run, error paths (network fail, empty result, malformed input). If output approaches 30 KB, switch to capblob-pipe NOW, not later.

### 4. Schema & metadata

Input schema (single-line JSON when inlined as script metadata; can be multi-line when passed via `save_cap` since it's just a string param):

```json
{"type":"object","properties":{"limit":{"type":"integer","description":"how many"}},"additionalProperties":false}
```

`additionalProperties: false` on every object level — required by Anthropic tool-use spec.

Tags: comma-separated for `save_cap` param (`tags: "web,hn,fetch"`), array for CAP.md frontmatter (`tags: [web, hn, fetch]`).

`auto_active: true` → injected into every session automatically. Use ONLY for universally useful caps (search, generic fetchers). Start `false`; promote later.

### 4.5. Pre-save self-checks

Three checks. Skipping these is the #1 cause of caps that pass install-tests but crash on `activate_cap`.

**(a) Parse-probe.** Right after save_cap, call `mcp__yesmem__activate_cap({name})` and verify the returned `code` field is non-empty. Empty `code` = parser found no usable tool subsection = `activate_cap` will silently fail downstream.

**(b) Handler-lint against REPL VM allowlist.** Sweep your handler text:

```bash
grep -nE 'sh\(|file\(|process\.|require\(|import |globalThis|fetch\(' <handler-text>
```

| Wrong | Right |
|---|---|
| `file({action:'write', path, content})` | `put(path, content)` or `await Write({file_path, content})` |
| `process.env.X` | `(await sh('echo $X')).trim()` |
| `require('fs')`, `import x from 'y'` | use `sh`, `cat`, `put` directly |
| `JSON.parse(sh(...))` | `JSON.parse(await sh(...))` — `sh` is async |
| `globalThis.fetch`, `axios` | `sh('curl -s URL')` |

**(c) Schema cross-check.** When the cap persists data:

- Every column referenced in handler INSERT/SELECT/WHERE must appear in `## Database` (or in the `cap_store` `columns` array).
- Auto-added (`id`, `created_at`, `updated_at`) MUST NOT appear in your columns list.
- `## Database` ```sql fence accepts only `CREATE TABLE/INDEX/VIEW/TRIGGER IF NOT EXISTS`. SQL comments inside the fence are rejected. For stateless caps, leave the fence body empty or omit `## Database` entirely.
- Table names use `cap_<capname>__<tablename>` prefix in raw SQL; the cap_store API takes only the short name.

### 5. save_cap

```javascript
const handler = async ({limit = 10}) => { /* ... */ };

await mcp__yesmem__save_cap({
  name: 'my_cap',
  description: 'Discovery-bait one-liner',
  scripts: JSON.stringify([{
    name: 'my_cap',
    kind: 'tool',
    runtime: 'repl',
    body: handler.toString(),
    schema: JSON.stringify({
      type:'object',
      properties:{ limit:{type:'integer', description:'count, default 10'} },
      additionalProperties:false
    })
  }]),
  tags: 'web,fetch',
  tested: true,
  test_date: '2026-05-01',
  auto_active: false
});
```

Re-saving with same name auto-supersedes the old row, bumps version. Returns `{id, name, superseded, version}`.

**Inline-body trap**: if the `scripts` JSON exceeds ~10 KB AS A LITERAL TOOL ARGUMENT, the daemon may store the literal string `"PLACEHOLDER"` instead of your body. Build the JSON in a REPL variable first, then pass via `await mcp__yesmem__save_cap({scripts})`. Never paste a 10 KB+ scripts string into a top-level tool_use call. See `gotchas.md` "save_cap PLACEHOLDER bug".

### 6. Verify

```javascript
await mcp__yesmem__get_caps({name: 'my_cap'});               // 1. row in DB
const r = await mcp__yesmem__activate_cap({name: 'my_cap'}); // 2. parse-probe
r.code;                                                       // non-empty?
eval(r.code);                                                 // 3. register in REPL
await my_cap({limit: 5});                                     // 4. callable
await mcp__yesmem__cap_store({capability:'my_cap', action:'query', table:'hits'});
```

After superseding a schema, existing threads must re-`activate_cap` — proxy caches per thread.

## Activation modes

| Mode | Trigger | Use for |
|---|---|---|
| `auto_active: true` | proxy injects every session | universal caps (search, general fetchers) |
| `activate_cap(name)` | per-thread MCP call | task-specific caps |
| Manual `registerTool(...)` | copy/paste returned code | ad-hoc test before save_cap |

`deactivate_cap(name)` reverses activation for the current thread.

## Bundled cap update lifecycle (CRITICAL)

Bundled caps live at `caps/bundled-caps/<name>/CAP.md`. They are also persisted as a learnings row in `caps.db`. The daemon reads from DB at runtime, and **writes DB content back to disk on restart** unless a manifest entry vouches for the disk body. What decides a delivery is `derived_from_hash` in `manifest.yaml` (shipped as `caps/bundled-caps/manifest.yaml`, kept per installation as `<caps_dir>/manifest.yaml`), not the frontmatter `version:`, which is display only. The digest is `textutil.BodyDigest`: line endings and trailing newlines normalized, case and indentation kept. So:

| Situation | Required step |
|---|---|
| Entry names the installed body, or the bundled body hashes like the installed one | the bundle is that body's successor. Edit `caps/bundled-caps/<name>/CAP.md`, then `make deploy` (builds the binary that carries the new source) and `yesmem migrate` (runs `InstallBundledCaps`). `make deploy` alone installs no cap: measured 2026-10-23, rocketchat stood at v15 before and after a deploy. No `version:` bump needed. |
| No entry, and a body sits on disk | nothing vouches for the bundle: the installed body is kept and one conflict line names both hashes. Merge the installed body into the repo file, then record the installed digest as `derived_from_hash`. |
| Entry names a different body | same conflict, same way out: reconcile the repo body with the installed one, then record the digest the line prints. Raising `version:` changes nothing. |
| Installed copy disagrees with the DB row | the export (`WriteCapToDisk`) writes the row back when the row's version is above the copy and the row is the later state, but never over a delivery its own source is behind. Diagnostic: compare the file's digest with `~/.claude/caps/manifest.yaml`; `sha256sum` alone is misleading because the provenance digest normalizes line endings. If the file is the body you want to keep, make it official via `save_cap`. |

This contradicts a previous note in the skill ("no manual save_cap needed for bundled cap update") — that was incomplete. See `gotchas.md` "DB write-back overrides disk edit".

## Sandbox

Sandbox is per-script in v1.1 (`sandbox: none|standard|strict` in script metadata). Resolution order: per-script > scheduled-job profile > daemon default. `scope: project` rejects `sandbox: none`. See cap-spec/spec.md and `internal/capfile/parse.go:120-145` for the guard.

## Auto-correct loop (handler caps run by scheduler)

When a `kind: handler` bash script fires under the scheduler with `auto_correct: true` (default) and fails, the daemon may stage a corrected version as a `cap_proposed` learning. Workflow:

```javascript
await mcp__yesmem__list_cap_proposals();                       // pending
await mcp__yesmem__cap_proposal_decide({id: 12345, decision: 'accept'});
// or { decision: 'reject' }
```

Active cap is untouched until `accept`. See `api-reference.md` for the exact shapes. **Multi-script caps are now safe**: a historical bug overwrote the entire `scripts` array with a single corrected bash body — that is fixed via `script:<name>`-keyword-plumbing in `persistProposalForReview` and `handleCapProposalDecide`. Older notes saying "set `auto_correct: false` on multi-script caps" are stale. See `gotchas.md` "autoCorrectBashCap on multi-script bundles — historical bug, now resolved".

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| `id` / `created_at` / `updated_at` in columns array | `duplicate column name` | Remove them — auto-added |
| Bash heredoc / multiline | hook reject or shell mangle | Single-line, `&&`/`;` |
| Forgot `create_table` at handler start | first call passes, later fails on fresh DB | Always `create_table` first — idempotent |
| `tested: true` without running | bugs surface on first real use | Actually run with real inputs first |
| `auto_active: true` for rare/experimental caps | every session pays the token cost | Start `false`, promote after validation |
| No timeout on `sh`/`curl` | hung handler blocks REPL | `sh(cmd, 20000)`, `curl --max-time 15` |
| User input concatenated into WHERE | sanitizer-bypass / blocked keyword | `?` placeholders + `args` array |
| Silent error swallow | user thinks it worked | Return `{error: ..., detail: ...}`, don't throw |
| Inline Python/Perl/awk in bash with nested quoting | `r'\''...\''` escape hell | Move logic into REPL JS, or extract a helper file |
| Schema change without `activate_cap` in open threads | old threads see old shape | Tell user to re-activate after supersede |

## Quick mode (3 steps, trivial caps only)

For caps with no storage and a single bash one-liner:

1. Working one-liner in REPL
2. `save_cap({name, description, scripts: JSON.stringify([{name, kind:'tool', runtime:'bash', body, schema:'{"type":"object"}'}]), tags, tested: true})`
3. `get_caps({name})` to confirm

Most real caps need the full 6 steps.

## Related

- `recipes.md` (this directory) — six concrete patterns with complete CAP.md
- `api-reference.md` (this directory) — exact MCP shapes and return values
- `gotchas.md` (this directory) — every known pitfall with symptom/cause/fix
- `internal/storage/cap_store.go` — storage layer + sanitize_where + quota constants
- `internal/daemon/handler_caps.go` + `handler_caps_helpers.go` — save/activate/deactivate
- `internal/daemon/handler_cap_proposal.go` — auto-correct accept/reject
- `internal/proxy/caps_inject.go` — `auto_active` injection mechanics
- `internal/capfile/parse.go` — CAP.md parser; the v1.1 contract is enforced here
