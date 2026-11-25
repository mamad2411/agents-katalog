---
name: sb-diagnostics-and-tooling
description: >-
  How to MEASURE the second-brain plugin instead of eyeballing it. Load when you need to observe
  live state — read/interpret error-log.jsonl vs audit-log.jsonl, run the sb CLI (sb auth doctor,
  sb query, sb status), prove a PreToolUse guard is actually armed (guard liveness probes), check
  whether the drainer/extraction ran, inspect dream status.json/diff.md/forget-manifest, diagnose
  degraded search (bm25-only/text-only, embeddings coverage), run wiki health checks
  (knowledge_validate/reindex), or measure per-turn injection bytes/tokens. Trigger phrases:
  "is it running", "did extraction happen", "check the logs", "is the guard armed", "why is search
  degraded", "health check", "hook latency", "audit log", "measure". Do NOT use for interpreting a
  specific failure once measured — sb-debugging-playbook owns symptom→triage; flag/kill-switch
  semantics live in sb-config-and-flags; hook wiring and state-file rationale live in
  sb-architecture-contract.
---

# sb-diagnostics-and-tooling — measure, don't eyeball

The costliest failures in this project were **silent degradations, never crashes**:
guards inert for months on the dev platform, 169 consecutive extraction timeouts,
gigabytes of silently duplicated deps. "No errors" has repeatedly meant "not
running". This skill is the instrument panel: every observability surface, the exact
command to read it, and how to interpret what comes back. When a measurement looks
bad, hand off to **sb-debugging-playbook** for triage.

All commands are bash, run from the repo root (`C:/Workplace/Projects/claude-code-plugin`
on the dev box, or any plugin checkout/install). They work on Windows git-bash, Linux,
and macOS unless flagged. Version-stamped facts: **as of 0.33.31 (2026-07-05)**.

**Vocabulary** (defined once; deeper rationale in sb-architecture-contract):

| Term | Meaning |
|---|---|
| `BRAIN_DIR` | plugin state root, default `~/.second-brain` (env-overridable; MSYS-normalized on git-bash) |
| `KNOWLEDGE_DIR` | wiki root, default `~/knowledge` (env `CLAUDE_PLUGIN_OPTION_KNOWLEDGE_DIR` / `KNOWLEDGE_DIR`) |
| hot tier | always-injected `USER.md` + per-project `PROJECT.md` under `BRAIN_DIR` |
| guard | a PreToolUse hook script that reads a stdin JSON payload and may emit a deny/ask/allow verdict |
| drainer | `scripts/extract-drain.sh`, the out-of-band (timer-run) extractor for archived transcripts |
| dream | background wiki-consolidation job under `~/.second-brain/dreams/drm_*/` |
| FORGET | the dream phase proposing reversible page archival (manifest only until accept) |
| plugin root | `$CLAUDE_PLUGIN_ROOT` at hook runtime; the repo checkout works for manual runs |

## 1. The two log channels

Both live under `BRAIN_DIR`; they have **different schemas and different rotation**.
Writers: `sb_log_error` / `sb_log_audit` in `scripts/lib.sh` (~lines 192–306).

| | `error-log.jsonl` | `audit-log.jsonl` |
|---|---|---|
| Purpose | fail-loud error channel | trajectory/evidence channel (guard verdicts, latency, TRACE) |
| Schema | `{timestamp, script, message, exit_code}` | verdicts: `{ts, hook, verdict, rule, target, reason, session_id, extra}`; latency: `{ts, kind:"latency", hook, duration_ms, exit_code, budget_warn?}`; plus re-routed TRACE lines in the error schema |
| Verdict values | — | `allow \| ask \| deny \| flag` (+ `rewrite` counted by SAR) |
| Rotation | >512 KB → keep newest 1000 lines | >5000 lines or >5 MiB → drop OLDEST 50% (`SB_AUDIT_MAX_LINES/BYTES` are hard-coded constants, not env knobs) |
| Write failure | logged loud where possible | fail-soft (`2>/dev/null`) — a guard never blocks a tool call over an unwritable audit file |

**R6b gate-breadcrumb routing rule** (the one that trips people): a message starting
`gate=` logged with `exit_code == 0` is TRACE, not an error — `sb_log_error`
re-routes it to the **audit-log**. A `gate=` message with a NONZERO exit stays in the
error-log as a real failure. (Before this rule, gate breadcrumbs were 41% of
error-log lines.) So: the audit-log is **heterogeneous** — filter by field presence,
and never assume every error-log line is a failure (`exit_code: 0` entries like
`extractor-diag …` are diagnostics).

```bash
B=~/.second-brain
tail -20 "$B/error-log.jsonl" | jq .                                   # newest errors
jq -r '.script' "$B/error-log.jsonl" | sort | uniq -c | sort -rn        # who is failing
jq -r 'select(.verdict != null) | .verdict' "$B/audit-log.jsonl" | sort | uniq -c   # verdict mix
jq -c 'select(.verdict=="deny" or .verdict=="ask") | {ts,hook,rule,target}' "$B/audit-log.jsonl" | tail -20
jq -c 'select(.session_id=="<SID>")' "$B/audit-log.jsonl"               # one session's trajectory
```

**SAR (Safety Adherence Rate)**: `scripts/sar-summary.sh` (Stop hook, kill switch
`SB_SAR_SUMMARY=off`) computes `1 - (ask + deny) / total_verdicts` per session —
allow/rewrite = in-lane, flag = warning (doesn't lower SAR) — and prints a
`systemMessage` banner with the follow-up jq command. Whole-log SAR on demand = the
verdict-mix one-liner above.

**Reading the numbers** (good vs bad): the error-log's raw line count is history,
not state (rotation keeps the newest 1000 lines) — judge by RECENCY + REPETITION.
Bad = one `script` dominating the histogram with fresh timestamps (a live failure
loop; the 169-consecutive-`ec=124` incident looked exactly like this); fine = a
long tail of old, varied entries. A healthy verdict mix is dominated by
allow/rewrite; ask/deny are low-volume and worth reading individually (the SAR
banner already surfaces them). ZERO verdict rows ever, on a system with guards
wired, is the fail-open signature — prove liveness with §4 before trusting it.

## 2. The `sb` CLI

Standalone, no Claude session needed. Wrapper `bin/sb` (and `bin/sb.cmd` on Windows)
execs `node mcp/dist/cli/sb-entry.bundle.js`. Env: `BRAIN_DIR`, `KNOWLEDGE_DIR`.
Exit codes: 0 ok, 1 operation failed (e.g. pin rejected), 2 usage error.

```bash
bash "${CLAUDE_PLUGIN_ROOT:-.}/bin/sb" help
```

| Command | Measures / does | Output |
|---|---|---|
| `sb query <text>` | wiki search (BM25+vector hybrid), top 5 | `NN%  [[slug]]  — desc` + path; `(no results)` |
| `sb recall <text>` | episodic transcript search, limit 5 | `NN%  [date project]  snippet` + `archivePath:lineStart-lineEnd` |
| `sb pin user <text>` | append preference to USER.md | `+ <line>` or exit 1 + stderr reason |
| `sb pin project <slug> <blockers\|decisions> <text>` | append to PROJECT.md | `+ <line>  (slug/section)` |
| `sb status` | hot-tier + wiki sizes, drainer recency, transcript backlog | USER.md bytes, project count, per-project PROJECT.md bytes, wiki counts, `transcript backlog:  N of M archived (K dead-lettered); dead windows: W in A archives, L lines` (N = `pending` rows of `sb_drain_cursor_map`; the dead suffix only when some window is dead-lettered), `archive scrub:` (`done` / `N to scrub (K with failed attempts >= 3)`) |
| `sb auth status` | extractor auth mode (authoritative) | see table below |
| `sb auth doctor` | prints the two supported auth setups + verify step | text |

**`sb auth status` interpretation** (probe: spawns `claude auth status`, hard
SIGKILL timeout `SB_AUTH_PROBE_TIMEOUT_MS` default 3000 ms):

| `mode:` | Meaning | Extraction consequence |
|---|---|---|
| `api-key` | `ANTHROPIC_API_KEY` env set (short-circuits everything) | works everywhere: Stop hooks, cron, CI |
| `api-key (claude-managed)` | logged in via claude's own key helper | still the recursive `claude` CLI path — in-session extraction queues |
| `subscription` | OAuth login | in-session Stop/PreCompact extraction structurally impossible (recursive-claude OAuth lock); work queues to the out-of-band drainer (§5) |
| `none` / `none (logged out)` | no key, no usable `claude` | no extraction backend |
| `unknown` | `claude` present but probe unparseable | inspect `claude auth status` yourself |

**GAP (as of 0.33.31)**: `sb query`/`sb recall` print hits only — they do NOT
surface the `degraded` search flags (§7). Use the MCP tools when you need the flag.

**Interpreting CLI output**: `(no results)` from `sb query` on a topic you KNOW is
in the wiki does not mean the knowledge is gone — check the legacy-misroute probe
first (§8: a page in the old `~/.second-brain/wiki` exists on disk but is invisible
to search), then re-run through the MCP tool to see whether search is degraded
(§7.1). Exit codes are part of the contract: 2 means your invocation is malformed,
not that the brain is unhealthy.

## 3. Status report anatomy, verify.sh, hook latency

`/second-brain:status` (user-invocable; `skills/status/SKILL.md`) renders: active
slug → hot-tier bytes (cap ≈3200) → registered projects → wiki counts
(`knowledge_stats` or filesystem fallback) → `knowledge_validate` → embeddings
coverage (§7.3) → persona stats → dream states → native auto-memory state →
pending-update flag → `verify.sh` → hook latency.

**`scripts/verify.sh`** — runtime smoke check; exit 0 + `verify: ok`, or exit 1 with
one `verify: FAIL: <check> — <detail>` per failure. Checks: (1) USER.md exists,
non-empty, has `## Intent`; (2) active PROJECT.md exists; (3) hot tier ≤ 66 lines
total; (4) `mcp/dist/server.bundle.js` present; (4b) wiki dir exists; (4c) index.md
present when pages exist; (5b) stale dreams (pending/running with status.json mtime
older than `SB_DREAM_RUN_TIMEOUT`=21600 s) or completed-but-unreviewed dreams;
(5) error-log entries newer than `~/.second-brain/.last-verify`. **Not read-only**:
success stamps `.last-verify`.

**Hook latency (R7)** — `scripts/hook-timer.sh` wraps the heavy hooks and appends
`kind:"latency"` rows to the audit-log; `budget_warn:true` when duration ≥ 70% of
budget. Budgets (hooks/hooks.json, as of 0.33.31): session-load 15 s,
dream-autostage 20 s, persona-context 10 s, stop-extract 45 s, pre-compact 45 s.
Render p50/p95 per hook:

```bash
AUD="$HOME/.second-brain/audit-log.jsonl"
grep '"kind":"latency"' "$AUD" | tail -500 \
  | jq -r '[.hook, .duration_ms] | @tsv' | sort \
  | awk -F'\t' '{v[$1]=v[$1]" "$2; n[$1]++} END{for(h in n){split(substr(v[h],2),a," ");m=n[h];
      for(i=1;i<m;i++)for(j=i+1;j<=m;j++)if(a[i]+0>a[j]+0){t=a[i];a[i]=a[j];a[j]=t}
      p50=a[int((m+1)*0.50)];p95=a[int((m+1)*0.95)];if(p50=="")p50=a[m];if(p95=="")p95=a[m]
      printf "  %-22s p50=%sms p95=%sms (n=%d)\n",h,p50,p95,m}}'
grep -c '"budget_warn":true' "$AUD"    # runs past 70% of budget
```

Interpretation: a p95 approaching its hooks.json timeout is about to become an
`ec=124` failure class (the R1 24s-stack-vs-25s-timeout bug) — act BEFORE it flips.

## 4. Guard liveness probes — prove a guard is armed

This is violation injection done manually (the P8 idea): feed each PreToolUse guard
a synthetic hook payload on stdin and assert the JSON verdict. Wiring ground truth
is `hooks/hooks.json` (guards run with 5 s timeouts); full wiring table belongs to
sb-architecture-contract.

**Rules of the probe** — empty stdout = silent allow; JSON with
`.hookSpecificOutput.permissionDecision` = guard fired. Sandbox `BRAIN_DIR` (verdicts
append to the real audit-log otherwise; wiki-write-guard's tombstone branch can even
move files). Build payloads with `printf`, not `jq --arg` (Windows git-bash MSYS
path conversion breaks `$HOME`-prefix checks).

Shipped automation — run this first:

```bash
bash .claude/skills/sb-diagnostics-and-tooling/scripts/guard-liveness.sh
# per-guard ARMED / NOT LIVE / DISABLED; exit 0 only when all three are armed
```

Core manual one-liners (one per guard; the full matrix incl. Windows-form,
case-varied, `\\?\` and fail-closed probes is in
[references/guard-probes.md](references/guard-probes.md)):

```bash
P="${CLAUDE_PLUGIN_ROOT:-$PWD}"; PB=$(mktemp -d)
# 1. symlink-guard: credential write must deny
printf '{"session_id":"probe","hook_event_name":"PreToolUse","tool_name":"Write","tool_input":{"file_path":"%s"}}' "$HOME/.ssh/x" \
  | BRAIN_DIR="$PB" bash "$P/scripts/symlink-guard.sh" | jq -r '.hookSpecificOutput.permissionDecision // "SILENT-FAIL-OPEN"'
# 2. persona-tool-guard: force-push to main must ask
echo '{"tool_name":"Bash","tool_input":{"command":"git push --force origin main"}}' \
  | BRAIN_DIR="$PB" bash "$P/scripts/persona-tool-guard.sh" | jq -r '.hookSpecificOutput.permissionDecision // "SILENT-FAIL-OPEN"'
# 3. wiki-write-guard: frontmatter-less wiki write must deny
printf '{"tool_name":"Write","tool_input":{"file_path":"%s","content":"# no frontmatter"}}' "$PB/knowledge/wiki/state/probe.md" \
  | BRAIN_DIR="$PB" bash "$P/scripts/wiki-write-guard.sh" | jq -r '.hookSpecificOutput.permissionDecision // "SILENT-FAIL-OPEN"'
```

Expected: `deny`, `ask`, `deny`. Anything else on a Write-to-`~/.ssh` probe means
the guard is fail-open in YOUR environment — the exact class that was inert on
Windows until 0.33.31 (`sb_normalize_path` funnel). If a kill switch
(`SB_SYMLINK_GUARD=off`, `SB_PERSONA_GATE=off`) is exported, the guard is DISABLED
by choice, not broken. After probing, audit evidence:
`grep '"hook":"persona-tool-guard.sh"' "$PB/audit-log.jsonl"`.

## 5. Extraction health — did capture/drain actually run?

State files (all under `~/.second-brain`; full map owned by sb-architecture-contract):

| File | Meaning |
|---|---|
| `.last-archived-line-<slug>--<session_id>` | archive-first cursor: `<raw_line>`, a tab, then the transcript path; raw transcript lines already copied into the archive (0.56.0); swept after 30 d idle |
| `.last-extracted-line-<slug>--<session_id>` | per-session extraction marker (bare integer, raw transcript lines); swept after 30 d idle |
| `.extractor-health.json` | `{checked_at, backend, status, reason}`; `status ∈ ok\|fail\|queued` — `queued` is NORMAL on subscription auth (in-session OAuth deferral) |
| `.extraction-state.jsonl` | drainer done-set: `{basename, ts, outcome: ok\|baseline\|retry\|error, reason?, latency_s?, fails?, from, lines}`; `from`/`lines` = the archive-line window extracted; a cursor = max `lines` over `ok`/`baseline` rows; `error` = that window dead-lettered after `SB_DRAIN_MAX_FAILS` (3), lines stay un-extracted |
| `transcripts/*.txt` | archived session windows, credential formats redacted by `sb_scrub_secrets` (kinds and what is not matched: `references/archive-and-backlog.md`); caps 400 files / 25 MB soft, 1200 files / 75 MB hard, only `pending` archives protected from eviction; subagent `sub-*` sub-cap 200 |
| `transcripts/.<archive>.lock`, `.archive-scrub-v1`, `.archive-scrub-v1.todo` | per-archive write lock (`<pid>.<nonce>`, 5 s wait, stolen from a dead holder after 60 s or any holder after 600 s); one-time scrub marker and to-do list |
| `.drain-defer-count` / `.last-drain-escape` | drainer starvation-escape state |
| `.project-update-pending-<slug>` | queued reflection work flag |

Four probes, in order:

```bash
B=~/.second-brain; P="${CLAUDE_PLUGIN_ROOT:-$PWD}"
# 1. Health marker (drainer stamps it at the end of EVERY run):
jq . "$B/.extractor-health.json"          # healthy: status "ok", reason "drained N this run (M failed)"
# 2. Done-set recency:
tail -5 "$B/.extraction-state.jsonl" | jq -c '{basename,ts,outcome,reason}'
# 3. Backlog = archives holding unextracted lines (0 pending = drained). Cursor map, one TSV row per
#    archive, oldest first: basename cursor lines state next fails mtime flag (state done|pending|dead)
source "$P/scripts/lib.sh"; M=$(sb_drain_cursor_map "$B/.extraction-state.jsonl" "$B/transcripts")
printf '%s' "$M" | cut -f4 | sort | uniq -c        # archives per state
printf '%s' "$M" | awk -F'\t' '$4=="pending"' | head   # what is waiting
# 4. Scheduler registered (checks the shim $B/bin/sb-extract-drain.sh + per-OS registration):
source "$P/scripts/lib.sh"; sb_timer_health    # installed | absent
```

**Drain-health banner logic** (inline in `scripts/session-load.sh`, block
"0a-quater"; there is NO `drain-health*.sh` script): banner fires when
`sb_count_drain_timeouts 40` (count of `extractor-diag .*ec=124` in the last 40
error-log lines) ≥ `SB_DRAIN_TIMEOUT_BANNER_THRESHOLD` (3), OR
`sb_count_drain_dead_letters` (archives holding a dead-lettered window, whatever their state, even one mid-archive: a window that failed `SB_DRAIN_MAX_FAILS` times; map columns 8/9 give the window and line totals the banner shows) ≥ `SB_DRAIN_DEADLETTER_THRESHOLD` (5). Suppressed when the
extractor-FAILED banner already fired (`.extractor-health.json` status `fail`);
kill switch `SB_DRAIN_HEALTH_BANNER=off`. Replicate both counters:

```bash
source "$P/scripts/lib.sh"; echo "timeouts(40)=$(sb_count_drain_timeouts 40) dead-letters=$(sb_count_drain_dead_letters)"
```

Context for interpreting a non-draining backlog: the drainer refuses in-session
(`CLAUDECODE=1`), defers while an interactive `claude` runs (starvation escape after
6 defers / oldest-pending >24 h, only when SAFE), single-flights on
`.extract-drain.lock` (7200 s staleness steal), makes up to 5 extractor calls per tick, per-attempt timeout 240 s.
A live archive is extracted once `SB_DRAIN_DELTA_MIN_BYTES` (4096) of new lines exist or it has been quiet
`SB_DRAIN_QUIET_S` (3600 s), so a small growing archive legitimately reads `pending`. Archive lock, eviction rules, the one-time scrub migration
(an archive awaiting its scrub is neither extracted nor indexed for recall), dead-window totals and done-set compaction: `references/archive-and-backlog.md`.
A large backlog with `mode: subscription` + an always-open interactive session is
the known starvation shape, not a bug — see sb-debugging-playbook for the triage.

## 6. Dream observability

Per-dream dir `~/.second-brain/dreams/<drm_YYYYMMDDTHHMMSSZ>/`:

- **`status.json`** — `{id, status: pending|running|completed|failed|canceled,
  created_at, started_at, ended_at, archived_at, model, instructions,
  inputs{transcript_count, wiki_page_count, wiki_snapshot_bytes, project_slug?},
  outputs{pages_added, pages_modified, pages_removed}, error}` (`mcp/src/tools/dream.ts:86-107`).
  **The file's mtime is the liveness heartbeat** — the runner re-stamps it between
  phases; a pending/running dream whose mtime is older than `SB_DREAM_RUN_TIMEOUT`
  (21600 s = 6 h) is stale/reclaimable (`sb_dream_is_stale`).
- **`diff.md`** — staged-vs-live diff written by phase "diff"; the `dream_status`
  MCP tool returns only the FIRST 50 lines as `diff_preview` (and only when
  `status=="completed"`); read the file directly for the whole thing.
- **`forget-manifest.tsv`** — FORGET proposals, columns `slug<TAB>category`. Nothing
  is archived until accept; the candidate script exits **2** when the recall guard
  cannot run and the phase skips fail-safe.

```bash
for sf in ~/.second-brain/dreams/drm_*/status.json; do
  jq -r '[.id,.status,(.archived_at//"-"),(.outputs|"+\(.pages_added) ~\(.pages_modified) -\(.pages_removed)"),(.error//"-")]|@tsv' "$sf"
done
```

**`acc=` telemetry** — `scripts/wiki-forget-score.sh` emits one TSV row per page,
sorted score ASC (most forgettable first), age-DESC tie-break:
`score<TAB>slug<TAB>path<TAB>acc=N inb=N age=Nd cat=X body=Nb<TAB>protflag`.
`acc` (read count from `~/.second-brain/access-counts.json`) is **deliberately NOT
in the score** — v4 correction: usage frequency is the rich-get-richer hub bias; the
score is connectivity (inbound `[[links]]`, weight 0.25) + category weight (0.20)
only. `protflag` empty = eligible; else `PROTECT:category|age|linked` (age floor
30 d; ANY inbound link protects). Theory behind the scoring belongs to
sb-memory-systems-reference.

```bash
bash "$P/scripts/wiki-forget-score.sh" | head -10                     # top eviction candidates (read-only)
bash "$P/scripts/wiki-forget-score.sh" | awk -F'\t' '$5==""' | wc -l  # eligible count
```

## 7. Search diagnostics

### 7.1 Degraded flags (in MCP tool results, contract-locked by `mcp/src/tools/search-output-contract.test.ts`)

| Tool | Flag | Meaning |
|---|---|---|
| `knowledge_search` | `degraded: 'bm25-only'` | ONNX embeddings unavailable; ranking fell back to BM25+graph |
| `episodic_search` | `degraded: 'text-only'` | mode `both`, vector engine down, text fallback ran |
| `episodic_search` | `degraded: 'vector-unavailable'` | explicit `mode:'vector'` or multi-concept array query with no embeddings — no fallback exists |

Absence of the flag = the hybrid path actually ran. The `sb` CLI hides these flags
(§2 GAP); `knowledge-search-cli.bundle.js` prints `### [[slug]]` lines only.

### 7.2 Are embeddings alive?

Embeddings = dynamic import of `@huggingface/transformers`, model
`Xenova/all-MiniLM-L6-v2` (dim 384). Unavailable when
`SECOND_BRAIN_DISABLE_EMBEDDINGS=1` or the package/model load fails — load failure
is logged (once per brain dir per process) to error-log as `script:"embeddings"`,
`exit_code: 0`, message `transformers model load failed: …`.

```bash
ls ~/.second-brain/vector-deps/node_modules/@huggingface/transformers/package.json  # shared tree present?
ls "$P/mcp/node_modules/@huggingface/transformers" >/dev/null 2>&1 && echo linked || echo NOT-linked
jq -c 'select(.script=="embeddings")' ~/.second-brain/error-log.jsonl | tail -3      # load failures?
bash "$P/bin/install-vector-deps.sh" --relink-only   # heal WITHOUT network; exit 3 = needs a real (re)install
```

**Interpretation**: the `script:"embeddings"` failure COUNT is cumulative history,
not current state — what matters is whether the NEWEST such timestamp postdates
your last successful install/relink. Live dev-box example (2026-07-05): 137
accumulated entries with the newest dated 2026-06-26, alongside a present+linked
vector-deps tree and 100% episodic coverage — all 137 are healed history, not a
live problem. Fresh entries after a relink = a real, current load failure.

(Windows history: `ln -s` deep-copies on MSYS — the ~3.1 GB dup bug, fixed 0.33.7
via node junction; details in sb-failure-archaeology.)

### 7.3 Episodic index coverage

Exchanges in `~/.second-brain/episodic-index.json` lacking a vector are
text-searchable only (backfilled at the next session-end extraction once deps link). Since 0.56.0 a
vector is `e8` (int8 components, base64) + `es` (scale); an index the 0.56.0 build has not rewritten
yet still holds float `embedding` arrays, so the check reads both:

```bash
jq -r '(.exchanges|length) as $t
  | ([.exchanges[] | select(((.e8 // .embedding // "") | length) > 0)] | length) as $e
  | if $t == 0 then "no exchanges indexed yet"
    else "Embeddings coverage: \($e)/\($t) (\(($e*100/$t)|floor)%)" end' ~/.second-brain/episodic-index.json
```

Regenerable caches (safe to delete, expensive to rebuild):
`<knowledge>/wiki/.embeddings-cache.json`, `~/.second-brain/transcripts/.embeddings-cache.json`.

## 8. Wiki health

**`knowledge_validate`** (MCP tool; TS `mcp/src/tools/knowledge-validate.ts`).
Issue taxonomy: `orphan_file, broken_link, missing_frontmatter,
malformed_frontmatter, incomplete_frontmatter, related_drift, duplicate_slug,
stale_page, empty_page, root_orphan, ai_block_incomplete, ai_block_missing`; each
`severity: error|warning`. Errors: `empty_page`, `duplicate_slug`, `root_orphan`
(root-level pages are never indexed → invisible to search). Report-only by default;
`{autofix: true}` MUTATES (deletes empty pages, rewrites/patches frontmatter) — run
report-only first.

**`knowledge_reindex`** regenerates `<knowledge>/wiki/index.md` AND — **caution** —
hardcodes `knowledgeValidate(…, {autofix: true})` inside the pass
(`mcp/src/tools/knowledge-reindex.ts:103`). A "reindex" is therefore never
read-only: it can delete empty pages without naming them. This is an OPEN
medium-severity finding from the 2026-07-02 deep audit (proposed fix: gate behind
`SB_REINDEX_AUTOFIX`); until it lands, treat reindex as a mutating operation and
validate report-only first when you care about the diff.

Headless (no Claude session) invocations via the bash wrappers in `scripts/lib.sh`:

```bash
source "$P/scripts/lib.sh"
sb_validate_wiki "$HOME/knowledge"    # runs the validate bundle WITH autofix; echoes fix count
sb_reindex_wiki  "$HOME/knowledge"    # regenerate index.md (failures routed to error-log)
```

Adjacent probes:

```bash
source "$P/scripts/lib.sh"; sb_conflicts_open_count            # open graph conflicts (folds graph/conflicts.jsonl)
find ~/.second-brain/wiki -name '*.md' 2>/dev/null | wc -l     # legacy-misroute check: expect 0
```

The legacy check matters: pages written into old `~/.second-brain/wiki` instead of
`~/knowledge/wiki` are invisible to search (a real raw-drainer incident — history in
sb-failure-archaeology). Anything >0 → move the pages into `~/knowledge/wiki/<category>/`
and reindex. Machine-generated pages must be born with the 7-field frontmatter
(`sb_write_generated_page`) or they churn forever as repeated `updated:`-only diffs.

## 9. Measuring the per-turn injection (the ~165-token method)

The claim (spec success criteria, measured 2026-06-30, P1c; recorded in CHANGELOG
0.33.30): the per-turn `UserPromptSubmit` injection from `scripts/persona-context.sh`
is ~662 bytes ≈ ~165 tokens, with no wiki page body. **Method**: run the hook with a
synthetic prompt payload, byte-count the emitted `additionalContext`, convert at the
~4 bytes/token heuristic (662/4 ≈ 165). No measurement script shipped; the
byte→token conversion step is inferred from the numbers, not documented
(UNVERIFIED (method) — reproduce below and count for yourself). Reproduce:

```bash
BYTES=$(printf '{"session_id":"measure-%s","prompt":"how should I refactor the search module to add caching?"}' "$$" \
  | bash "$P/scripts/persona-context.sh" \
  | jq -r '.hookSpecificOutput.additionalContext // ""' | wc -c)
echo "injection: ${BYTES} bytes ≈ $((BYTES / 4)) tokens"
```

Use a FRESH session_id per measurement (hence `measure-$$`): the hook keeps
per-session dedup memos in `$BRAIN_DIR/.injected/` (7 d GC), so a reused id
underreports on the second run. Vary the prompt (coding vs non-coding) — injection
is keyword-driven with per-section hard caps. The value is **state-dependent**: the
~662-byte figure was the maintainer's persona/wiki state on 2026-06-30; a live run
on the dev box on 2026-07-05 measured 1264 bytes ≈ 316 tokens — same order of
magnitude, different state. Measure YOUR state; don't quote the spec number as
universal. Related always-on budget surfaces: Claude Code hard-caps hook output at
10 K chars; `session-load.sh` enforces `BYTE_BUDGET=8000` / `HARD_CAP=9500`,
reserving USER.md ≤6000 + PROJECT.md ≤3000; budget-skips appear as `gate=byte-budget`
TRACE lines in the audit-log (§1). Repo-surface budgets (skills/agents/scripts/tests
counts) are sb-change-control territory.

## 10. Shipped scripts (in this skill dir)

All are read-only/side-effect-free and were tested live on Windows git-bash at
authoring time. The `.sh` scripts are bash-3.2-safe and self-locate the plugin root
(env `CLAUDE_PLUGIN_ROOT` → `$1` → walk-up); `usage-audit.mjs` is node ≥ 18, no deps,
and reads its turn rule from this repo's `scripts/persona-context.sh` (`--hook` overrides).

| Script | What it does | Exit |
|---|---|---|
| [scripts/guard-liveness.sh](scripts/guard-liveness.sh) | injects synthetic payloads into all three PreToolUse guards (sandboxed HOME+BRAIN_DIR) and prints ARMED / NOT LIVE / DISABLED per guard, incl. a Windows-form probe when cygpath exists and an audit-wiring check | 0 = all armed; 1 = any not live; 2 = prereqs missing |
| [scripts/sb-health-snapshot.sh](scripts/sb-health-snapshot.sh) | one screen: auth mode, scheduler timer, extractor health + last-drain + backlog, drain counters, error/audit tails, wiki counts + legacy-misroute, embeddings state + episodic coverage, unreviewed dreams | 0 (informational); 2 = root/lib unusable |
| [scripts/usage-audit.mjs](scripts/usage-audit.mjs) | per-TURN audit of the per-prompt injection over `--since/--until/--project` (UTC days; `--json`): human vs machine turns by kind (the hook's own `machine-turn` block + exact-repeat triage, parsed at runtime), injections on each, slugs offered and offered→fetched (same turn + next 2), KB reads per human turn, boilerplate past-session snippets, `gate=machine-turn`/`headless-child` audit rows, `gate=inject-precision mode=off` rows as "precision rollback active: N rows", hook_cancelled by script, a `turnOrigin` cross-check; headless (`sdk-cli`) and subagents reported apart; possible undercounts print as `WARNING` lines first (`warnings` array in `--json`); `--self-test` | 0 ok (read any WARNING first); 1 self-test failed; 2 bad args or impossible date, missing input (transcripts root, hook, an explicit `--audit`, a `--project` matching nothing), transcript format drift (no user record parsed, no dated turn), or the hook rule no longer parses |

```bash
bash .claude/skills/sb-diagnostics-and-tooling/scripts/sb-health-snapshot.sh   # start here
bash .claude/skills/sb-diagnostics-and-tooling/scripts/guard-liveness.sh      # then prove the guards
node .claude/skills/sb-diagnostics-and-tooling/scripts/usage-audit.mjs --since 2026-10-05   # injections vs reads, per turn
```

**1-week post-release check (0.55.0).** Seven days after release run `usage-audit.mjs --since <release-day>` and, for the baseline, `--since <release−7d> --until <release−1d>` (pre-release, `--since 2026-09-28 --until 2026-10-05`: 94 human turns, 77% of injections on machine turns, 1/102 offers fetched, 0.11 KB reads per human turn).
Pass: machine-turn injections ≈ 0 with `gate=machine-turn` rows present, headless persona injections 0 with `gate=headless-child` rows present, boilerplate past-session snippets falling (after the episodic reindex).
`WARNING audit-no-gate-rows` means no such rows at all: the installed plugin predates 0.55.0, or the row shape changed; not a pass. `precision rollback active: N rows` > 0 means `SB_INJECT_PRECISION=off` (the 0.54.1 gate) served some injections in the window.
Read the `turnOrigin cross-check` line before trusting "human": origin `scheduled` there is a cron prompt the prefix rule passes as human (only an exact repeat is skipped). Slash commands are judged as the hook sees them, `/name args` rebuilt from the transcript's expanded tags (probed, CLI 2.1.289), so they count as human; `<local-command-…>` records are not turns.

Note `scripts/verify.sh` (§3) is NOT side-effect-free (stamps `.last-verify`);
the snapshot deliberately does not run it.

## 11. Where the neighbors are (one home per fact)

| Question | Skill |
|---|---|
| A measurement looks bad — now what? | sb-debugging-playbook |
| What does flag X default to / kill-switch semantics? | sb-config-and-flags |
| Why is the hook/state-file architecture like this? Full wiring + state map | sb-architecture-contract |
| Ranking/dedup/forgetting theory behind the numbers | sb-memory-systems-reference |
| Test mechanics, CI lanes, add-a-test | sb-validation-and-qa |
| Past incidents these probes exist because of | sb-failure-archaeology |
| Install/upgrade/auth setup, data geography | sb-run-and-operate |
| Release gates, surface budget governance | sb-change-control |

## Provenance and maintenance

Derived from the working tree of `claude-code-plugin` at plugin version **0.33.31
(uncommitted release batch), HEAD 6fba312, authored 2026-07-05**. Primary evidence:
`scripts/lib.sh` (log writers/rotators, drain counters, timer health),
`scripts/verify.sh`, `scripts/hook-timer.sh`, `scripts/sar-summary.sh`,
`mcp/src/cli/sb.ts`, `skills/status/SKILL.md`, `scripts/extract-drain.sh`,
`scripts/session-load.sh`, `mcp/src/tools/{dream,knowledge-search,episodic-search,embeddings,knowledge-validate,knowledge-reindex}.ts`,
`scripts/wiki-forget-score.sh`, `scripts/wiki-forget-candidates.sh`,
`tests/test-{symlink,persona-tool,wiki-write}-guard.sh` (probe payloads), and the
2026-07-02 deep-audit findings (reindex-autofix). Shipped scripts were executed
against the live dev system before shipping.

Re-verify volatile facts before trusting them after an upgrade:

```bash
jq -r .version .claude-plugin/plugin.json                                  # skill written against 0.33.31
grep -n 'SB_AUDIT_MAX_LINES\|SB_AUDIT_MAX_BYTES\|524288\|tail -n 1000' scripts/lib.sh   # rotation caps
grep -n 'gate=\*\|gate=)' scripts/lib.sh | head -5                          # R6b routing rule still present
grep -n 'hook-timer.sh [0-9]*' hooks/hooks.json                             # wrapped hooks + budgets
grep -n "cmd === '" mcp/src/cli/sb.ts                                       # sb subcommand set
grep -rn "degraded" mcp/src/tools/knowledge-search.ts mcp/src/tools/episodic-search.ts | grep -v test  # flag values
grep -n 'autofix' mcp/src/tools/knowledge-reindex.ts                        # reindex-autofix finding still open?
grep -n 'DRAIN_TIMEOUT_BANNER_THRESHOLD\|DRAIN_DEADLETTER_THRESHOLD' scripts/session-load.sh  # banner thresholds
grep -n 'SB_DREAM_RUN_TIMEOUT' scripts/lib.sh | head -3                     # dream staleness window
bash tests/test-symlink-guard.sh && bash tests/test-wiki-write-guard.sh     # probe shapes
bash tests/test-persona-tool-guard.sh   # probe shapes (Test 22 lib.sh-fallback case fixed
#   2026-07-05: rules now supplied via a user persona-rules.json in BRAIN_DIR — green at 0.33.31)
ls mcp/dist/tools/ mcp/dist/cli/                                            # bundle inventory (no standalone knowledge-search bundle)
bash .claude/skills/sb-diagnostics-and-tooling/scripts/guard-liveness.sh    # the probes themselves still pass
node .claude/skills/sb-diagnostics-and-tooling/scripts/usage-audit.mjs --self-test   # hook turn rule still parses
```
