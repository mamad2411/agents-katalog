---
name: sb-config-and-flags
description: >-
  Configuration reference for the second-brain plugin repo: every configuration axis — the
  SB_* environment variables (~249, re-verify via §10 — this count drifts every release),
  ~/.second-brain/config.json keys, plugin.json userConfig,
  persona-rules.json, and the env > config.json > hard-default precedence model. Load it when the
  task involves: disabling/enabling a guard, banner, nudge, or pipeline (kill switches); finding a
  flag's default, definition site, or test coverage; changing where the brain/knowledge dirs live;
  adding a NEW flag (the 8-step checklist); auditing deprecated or advisory-only flags; or any
  question shaped like "what does SB_X do", "how do I turn off Y", "where is Z configured".
  Do NOT load it to learn what the subsystems themselves DO (use sb-architecture-contract), to
  debug a live failure (sb-debugging-playbook), to set up the build environment
  (sb-build-and-env), or for install/upgrade operation (sb-run-and-operate).
---

# Configuration and flags — second-brain plugin

Everything configurable in this repo, how precedence resolves, and how to add a flag without
tripping the gates. Facts verified against the working tree at plugin version 0.33.31
(uncommitted release batch) on 2026-07-05; the flag census and the auto_codemap citation were
re-verified 2026-09-05 at 0.49.0 and had drifted (§3, flag-catalog.md). Counts are volatile —
re-verify with §10.

Term sheet (defined once, used throughout):

| Term | Meaning |
|---|---|
| BRAIN_DIR | Runtime state root, default `~/.second-brain` (transcripts, raw inbox, config.json, audit log) |
| KNOWLEDGE_DIR | Wiki root, default `~/knowledge` (the durable knowledge base) |
| kill switch (KS) | Env var, default `on`, where ONLY the literal string `off` disables a behavior |
| guard | A PreToolUse hook script that can deny/ask on a tool call |
| banner | A SessionStart block of additionalContext text (informational) |
| dream | Staged wiki consolidation job (snapshot → propose → human/auto accept) |
| drainer | The out-of-band timer job that extracts queued session transcripts |
| FORGET | Dream phase that reversibly archives low-value wiki pages |
| advisory flag | Read only by LLM prompt text in agent/skill markdown — no code enforces it |

What subsystems do: sb-architecture-contract. Why the guards exist: sb-failure-archaeology.

## 1. The precedence model (read this first)

Documented at `scripts/lib.sh:1704-1713`, implemented by `sb_config_get` / `sb_config_bool`
(lib.sh:1714-1732):

> An explicit `SB_*` env var ALWAYS wins; `~/.second-brain/config.json` is the persistent default
> when the env is unset; a hard-coded default is the final fallback.
> Pattern: `"${SB_FOO:-$(sb_config_get .foo HARD)}"`.

Critical nuances:

1. **Only ONE env var is actually layered over config.json today**: `SB_DREAM_KEEP_COUNT` over
   `.retention.dream_keep_count` (`scripts/dream-snapshot.sh:77`). Every other config.json key is
   config-only, and the other ~180 `SB_*` vars are env-only. The three-layer pattern is the
   INTENDED idiom, not the current reality. (`SB_FOO` at lib.sh:1709 is a doc example, not a flag.)
2. **CRLF strip is load-bearing**: every jq read in the config reader pipes through `tr -d '\r'`
   — Windows (Git-Bash) jq emits CRLF in `-r` output, so without the strip `auto_improve: true`
   reads back as `"true\r"` and the whole config system silently mis-reads on Windows
   (comment lib.sh:1710-1713).
3. **`sb_config_bool` reads raw (no jq `//`)** so an explicit `false` is honoured as OFF instead
   of being treated as absent: `true`→on, `false`→off, null/absent/malformed→the default.
4. Directory roots stand OUTSIDE config.json entirely (§2).

House idioms every flag consumer follows (copy these when adding a flag):

```bash
# Kill switch (shell): default on, only literal "off" disables
[ "${SB_PLAN_FIRST_NUDGE:-on}" = "off" ] && exit 0            # plan-first-nudge.sh:16
# Numeric knob: validate-or-default, never trust the env blindly
N="${SB_PLAN_FIRST_MIN_LINES:-3}"; case "$N" in ''|*[!0-9]*) N=3 ;; esac   # :42
```

TS side reads `process.env.SB_*` directly with `?? 'default'` / parseInt+finite-check, or via the
helpers `clampEnvInt('SB_SCOPE_HOPS', 2, 0, 4)` and `envFloat('SB_REDUNDANCY_THRESHOLD', 0.7, 0.01, 1)`
— note a grep for `process.env.SB_` MISSES the helper-mediated reads (§10).

## 2. Directory roots and the userConfig flow

`.claude-plugin/plugin.json` declares exactly ONE userConfig option: `knowledge_dir`
(type `directory`, default `~/knowledge`). Claude Code surfaces userConfig values to hooks and MCP
servers as `CLAUDE_PLUGIN_OPTION_<UPPERNAME>` env vars — so the wiki root arrives as
`CLAUDE_PLUGIN_OPTION_KNOWLEDGE_DIR`.

| Root | Resolution chain (first set wins) | Canonical site |
|---|---|---|
| Brain dir | `SB_BRAIN_DIR` → `BRAIN_DIR` → `os.homedir()/.second-brain` | `mcp/src/brain-paths.ts:27-33` (TS funnel) |
| Knowledge dir (TS, brain-paths funnel: search/fetch, archive_to_wiki, sb CLI, CLI shims) | `CLAUDE_PLUGIN_OPTION_KNOWLEDGE_DIR` → `KNOWLEDGE_DIR` → `homedir()/knowledge` | `brain-paths.ts:35-42` |
| Knowledge dir (MCP server + dream tools) | **REVERSED: `KNOWLEDGE_DIR` → `CLAUDE_PLUGIN_OPTION_KNOWLEDGE_DIR`** → `homedir()/knowledge` | `mcp/src/server.ts:29-43`; `mcp/src/tools/dream.ts:75-84` — divergence, see rules below |
| Knowledge dir (shell) | `CLAUDE_PLUGIN_OPTION_KNOWLEDGE_DIR` → `$HOME/knowledge`, then tilde-expand `${kdir/#\~/$HOME}` | `lib.sh:159,337,369,1630` |

> Note (0.35.x): cost-router was absorbed and removed — its capture script (and its `SB_KNOWLEDGE_DIR`-first resolution row) and all `COST_ROUTER_*` flags are gone. History: wiki `entities/cost-router` + the archive/docs branch. Any `cost-router` mention below/in references is historical.

Rules and caveats:

- **BRAIN-dir resolution funnels through `brain-paths.ts`** — `os.homedir()`, never
  `process.env.HOME` (the Windows CWD-relative stray-folder bug class; Node on native Windows
  does not inherit `HOME`). This one IS machine-locked: `mcp/src/brain-paths.test.ts:85-115`
  fails any non-test source file containing `process.env.HOME` or a `.second-brain` string
  literal — and ONLY those two patterns.
- **The KNOWLEDGE-dir funnel is NOT machine-locked, and today it is not single-source**:
  `mcp/src/server.ts:29-43` and `mcp/src/tools/dream.ts:75-84` each re-implement
  `resolveKnowledgeDir()` with `KNOWLEDGE_DIR` first — the OPPOSITE precedence to
  brain-paths.ts. With BOTH env vars set and different, the MCP server/dream tools use one wiki
  while search and archive_to_wiki use another (the split-wiki failure; OPEN audit medium —
  sb-debugging-playbook row 11). Workaround: set at most ONE of the two vars.
- Env-derived paths are CRLF-stripped via `cleanEnvPath` on the TS side.
- Brain dir is NOT a userConfig option; it is env-only.
- Gotcha: the repo-root `.mcp.json` cannot serve as a *project* MCP server
  (`${CLAUDE_PLUGIN_ROOT}` unexpanded outside plugin context) — validate-plugin.sh fails if a
  root `.mcp.json` exists. Story: sb-failure-archaeology.

## 3. `~/.second-brain/config.json`

Reader: `sb_config_get` / `sb_config_bool` (§1). Seeded self-documenting by
`scripts/ensure-dirs.sh:29-41` on first SessionStart — idempotent, never clobbers an existing
file. Writer: `scripts/set-autonomy.mjs` is "the ONLY writer of the autonomy consent tiers"
(its header) — invoked by `/second-brain:setup`'s consent step; per-key merge, refuses inside
nested spawns and on unparseable config (fail-closed).

Every key consumed in live code (grep in §10; verified 2026-07-05):

| Key | Seeded | Consumer | Effect |
|---|---|---|---|
| `brain_os` | `true` (0.41.0) | brain-os-run.sh:33 (env `SB_BRAIN_OS=off` also kills it) | THE OFFLINE ENGINE SEAM. One entry point for every out-of-band pass that processes already-captured knowledge — prune, deterministic upkeep, embedding warm pass, the quarantined consolidation lane, code-map regen — invoked once from the drainer tick. `false` = no offline processing at all; capture, retrieval and the in-session `/second-brain:maintain` + `/second-brain:dream` paths are untouched (the engine is optional by construction). Each pass still honors its own gate below. |
| `auto_embed` | `true` (0.41.0) | brain-os-run.sh (embedding warm pass) | Precompute wiki embeddings offline via the shipped search path, so the first search of a session isn't paying to embed changed pages. Writes only `KNOWLEDGE_DIR/wiki/.embeddings-cache.json`; runs with a scratch `SB_BRAIN_DIR` so it cannot pollute live access-count telemetry. No-op when `SECOND_BRAIN_DISABLE_EMBEDDINGS=1` or vector deps are absent. |
| `auto_improve` | `true` | brain-os-run.sh (deterministic pass); session-load.sh:600 | Free + offline deterministic upkeep (validate + reindex wiki) on the drainer timer. `false` + raw backlog ≥ threshold → autoconsolidate nudge banner. |
| `auto_maintain` | `true` (on since 0.30.0) | brain-os-run.sh (consolidate pass); maintain-llm-drain.sh:26 | The consolidation lane: quarantined zero-tool Stage A summarizer → deterministic netless Stage B writer. READS YOUR CLAUDE OAUTH + SPENDS TOKENS (ensure-dirs.sh). **Cross-platform since 0.41.x — bubblewrap is now ADDITIVE Linux defense, no longer a gate, so this lane RUNS on Windows/macOS too** (previously a documented no-op there). Stage B preconditions (node + the writer bundle) are checked before staging. Quarantine marker: `~/.second-brain/.llm-maintain-quarantine`. What reaches the live wiki is governed by `auto_accept` + the held-untrusted gate. |
| `auto_accept` | `"safe"` | maintain-llm-drain.sh:257 → `sb_auto_accept_decision` (lib.sh:409) | `safe` = auto-accept only LOW-RISK dream changes: sets `SB_DREAM_ACCEPT_NO_DELETE=1` (dream-accept.sh:117 comment) and leaves FORGET-proposing dreams for manual review. `off` = always manual. `"all"` = accept everything (documented in the seed comment as "too aggressive", not the default). |
| `auto_codemap` | NOT seeded — hard default `on` at the consumer | brain-os-run.sh:83 (dispatched from extract-drain.sh's brain-os-run.sh call, not read there directly) | Out-of-band code-map regen (P3a Task C2) inside the drainer's single-flight lock: runs `mcp/dist/tools/code-map-cli.bundle.js` (source `mcp/src/tools/codemap/`) against `SB_CODEMAP_REPO` or the newest registry `root_path`; the CLI self-gates on git-rev drift. `false` = kill switch. |
| `retention.dream_keep_count` | `5` | dream-snapshot.sh:77 (env `SB_DREAM_KEEP_COUNT` wins) | Dream snapshots retained — the ONLY layered knob (§1.1). |
| `retention.bak_ttl_days` | `14` | sb-prune-archives.sh:46 (validate-or-default) | Backup TTL days. |
| `retention.embeddings_cache_gc` | `true` | sb-prune-archives.sh:21 | Embeddings-cache GC on/off. |
| `retention.wiki_archive_ttl_days` | `0` (= NEVER) | seeded + asserted by test-config-reader.sh:47; NO live code consumer found (grep 2026-07-05) | Reserved: TTL for the FORGET archive. 0 keeps the irreversible store off. |

**`auto_codemap` is LIVE** (P3a Task C2, shipped 0.33.33+). Definition site + default:
`sb_config_bool .auto_codemap on` at `scripts/brain-os-run.sh:83` — hard default `on`,
deliberately NOT seeded into config.json. The pass moved off `extract-drain.sh` at the 0.41.0
engine-seam refactor (§3.8 in sb-architecture-contract); `extract-drain.sh` only dispatches to
`brain-os-run.sh` (:288,:474), which drives the `mcp/src/tools/codemap/` implementation via the
committed CLI bundle. Kill switch exercised end-to-end (through that dispatch) by
`tests/test-extract-drain.sh:393-397`.

Reader tested by `tests/test-config-reader.sh`; the CRLF hazard by `tests/test-jq-crlf-windows.sh`.

## 4. persona-rules.json — the shipped guard policy

Selected at `scripts/persona-tool-guard.sh:39-45`: user file `~/.second-brain/persona-rules.json`
wins when present, else the shipped `scripts/persona-rules.default.json`. Shipped defaults —
**note the asymmetry, commonly misremembered**:

| Section | Shipped `enabled` | What it does |
|---|---|---|
| `tool_scope` | **`false` (OPT-IN)** | Asks when a tool outside a 14-tool allowlist is invoked. Session extension: `SB_TOOL_SCOPE_EXTRA` (colon-separated). |
| `resource_scope` | **`true` (LIVE by default)** | Asks before Edit/Write/MultiEdit/Read touch a path outside: `$CWD`, `$HOME/.second-brain`, `$HOME/knowledge`, `/tmp`, `/var/tmp`. Extension: `SB_RESOURCE_SCOPE_EXTRA`. |

So `SB_TOOL_SCOPE=off` is usually a no-op (the guard is already inert unless the user enabled
tool_scope), while `SB_RESOURCE_SCOPE=off` disarms a live guard. Both sit under the master
`SB_PERSONA_GATE`.

The `rules[]` array holds named PreToolUse rules (rewrite/ask), e.g. `strip-silent-fallback`
(rewrites `2>/dev/null` out of Bash commands — the fail-loud convention), `warn-force-push-main`,
`warn-rm-rf`, `warn-direct-write-hot-tier`, and self-protection rules that ask before edits to
plugin hook scripts or persona-rules itself. This file is the HARD-enforcement counterpart of
USER.md; drift between them is surfaced by the rules-gap banner (`SB_RULES_GAP_BANNER`).

## 5. The SB_* catalog — subsystem index

~187 distinct `SB_*` names exist across the tree (census 2026-07-05; 17 of those are
test-infrastructure-only). Full per-flag tables with defaults, definition sites, kind, and test
coverage: [references/flag-catalog.md](references/flag-catalog.md). Index:

| # | Subsystem (catalog §) | Contents |
|---|---|---|
| 1 | Directory & identity plumbing | `SB_BRAIN_DIR`, `SB_ACTIVE_SLUG`, `SB_NESTED_SPAWN`, kb-schema exports |
| 2 | Hook guards & nudges | every PreToolUse/PostToolUse/Stop guard's kill switch + tuning |
| 3 | SessionStart banners & auto-dispatch | all banner switches, maintainer auto-dispatch, dream autostage |
| 4 | Extractor / drainer pipeline | engine pin, local backend, timeouts, batch/lock/defer dials |
| 5 | Dream lifecycle | accept guards, SUMMARIZE/REFLECT, FORGET weights, redundancy engine |
| 6 | Search / retrieval / MCP server | scoping, boosts, MOC, capture dedup, egress budget |
| 7 | Persona subsystem | dismissal backoff, persona_think model/timeout |
| 8 | Eval / project-merge / misc | recall gates, staleness, liveness/test overrides |
| 9 | Internal variables | set by the plugin — NOT user axes (`SB_SESSION_ID`, `SB_AUDIT_FILE`, …) |
| 10 | Test-infrastructure vars | run-all knobs + stub doubles, tests/-only |

## 6. The most load-bearing flags

The subset you will actually reach for. Status: P = production default-on, O = opt-in/experimental,
A = advisory-only (§8), D = debug. Tests: does the name appear in any test (bash/vitest/none).

**Kill switches — guards, gates, banners** (all P, all `:-on`, only `off` disables):

| Flag | Disarms | Site | Tests |
|---|---|---|---|
| `SB_PERSONA_GATE` | MASTER: persona injection + tool guard + wiki-write guard | persona-context.sh:18; persona-tool-guard.sh:15; wiki-write-guard.sh:12 | bash |
| `SB_RESOURCE_SCOPE` | path-allowlist ask-guard (LIVE by default, §4) | persona-tool-guard.sh:102 | bash |
| `SB_TOOL_SCOPE` | tool-allowlist ask-guard (inert unless enabled, §4) | persona-tool-guard.sh:70 | bash |
| `SB_SYMLINK_GUARD` | symlink-resolved write denial into `~/.ssh` etc. | symlink-guard.sh:32 | bash |
| `SB_FLOW_GUARD` | credential-egress ask-guard on Bash/WebFetch/WebSearch | flow-guard.sh:29 | bash |
| `SB_INJECTION_SCAN` | PostToolUse prompt-injection scan (flags, never blocks) | tool-return-scanner.sh:20 | bash |
| `SB_CONFIG_CHANGE_AUDIT` | ConfigChange audit logging | config-change-guard.sh:26 | bash |
| `SB_VERIFY_GATE` | Stop-hook verification gate | stop-verify-gate.sh:13 | bash |
| `SB_QUALITY_GATE` | extraction quality filter (off = passthrough cat) — NOT the PostToolUse quality-gate.sh nudge (§7 name trap) | extraction-quality-gate.sh:18 | bash |
| `SB_PLAN_FIRST_NUDGE` | once-per-session multi-file plan nudge (0.33.30) | plan-first-nudge.sh:16 | bash |
| `SB_SIMPLICITY_GATE` | large-single-write advisory nudge | simplicity-gate.sh:7 | bash |
| `SB_SAR_SUMMARY` | Stop-hook safety-adherence banner | sar-summary.sh:22 | bash |
| `SB_SUBAGENT_CAPTURE` | SubagentStop result archiving | subagent-capture.sh:22 | bash |
| `SB_DREAM_AUTOSTAGE` | dream suggest/reclaim/quarantine banner logic | dream-autostage.sh:23 | bash |
| `SB_MAINTAINER_AUTO` | knowledge-maintainer auto-dispatch | session-load.sh:151 | bash |
| `SB_PRINCIPLES_INJECT` | persona principles in per-prompt context | persona-context.sh:249 | bash |

Banner switches (`SB_AUTH_LINE`, `SB_CAPTURE_HEALTH_BANNER`, `SB_DRAIN_HEALTH_BANNER`,
`SB_EMBED_PENDING_BANNER`, `SB_SCOPE_BANNER`, `SB_RULES_GAP_BANNER`, `SB_RAW_INBOX`,
`SB_AUTOCONSOLIDATE_NUDGE` — all `:-on`) and `SB_DISABLE_AUTO_TIMER` (`:-0`; `1` stops the
drainer-timer self-heal): catalog §3.

**Directories** (§2 above): `SB_BRAIN_DIR`, `CLAUDE_PLUGIN_OPTION_KNOWLEDGE_DIR` /
`KNOWLEDGE_DIR`, `SB_VECTOR_DEPS_DIR`.

**Pipeline dials — extractor/drainer/dream:**

| Flag | Default | Effect | Status | Tests |
|---|---|---|---|---|
| `SB_EXTRACTOR_ENGINE` | `auto` | Backend pin: auto / local / cli / bare | P | bash |
| `SB_EXTRACTOR_LOCAL_URL` | empty | OpenAI-compatible `/v1` endpoint; when set, tried FIRST (offline-capable, no OAuth lock) | O (inert until set) | bash |
| `SB_EXTRACT_TIMEOUT` | `25`/`30` s | In-hook extraction budget (stop-extract/pre-compact) — deliberately NOT shared with the drainer | P | none |
| `SB_DRAIN_EXTRACT_TIMEOUT` | `240` s | Drainer per-attempt budget. BUDGET PROOF at lib.sh:3455-3465: 5×3×240 = 3600s = half the lock steal-threshold. Do NOT raise without raising `SB_DRAIN_LOCK_STALE` | P | bash |
| `SB_DRAIN_BATCH` / `SB_DRAIN_MAX_FAILS` | `5` / `3` | Transcripts per cycle / fails before terminal `error` (or floor) | P | bash |
| `SB_DRAIN_LOCK_STALE` | `7200` s | Steal a drain lock older than this | P | bash |
| `SB_DRAIN_FLOOR` | `on` | After MAX_FAILS write the deterministic files-changed baseline instead of losing the session | P | none |
| `SB_DREAM_KEEP_COUNT` | `5` (via config) | Dream snapshots retained — the only layered knob | P | none |
| `SB_DREAM_ACCEPT_MIN_RATIO` | `50` % | Refuse accept when staging < N% of live pages ("a broken dream must not --delete the live wiki") | P (guard) | bash |
| `SB_DREAM_ACCEPT_NO_DELETE` | `0` | `1` refuses accepts whose apply would delete a live page; post-snapshot live pages are not counted, and a merge-only apply (no rsync / no `created_at`) skips the check (set by `auto_accept=safe`) | P (guard) | bash |
| `SB_DREAM_SUMMARIZE` / `SB_DREAM_REFLECT` | `on`/`on` | Theme-MOC / reflection ops; each independently gates graph-cluster.sh to `[]` | P | bash |
| `SB_WIKI_FORGET` | `on` | Dream FORGET phase | P, **A** | bash |
| `SB_PROJECT_SCOPE` | on | Project-scoped tiering of knowledge_search | P | bash+vitest |
| `SB_GRAPH_RANKING_BOOST` | **off** | DEMOTED opt-in (P7 2026-06-28: measured net-zero, displaced exact title matches — comment knowledge-search.ts:194-197) | O | vitest |
| `SB_CAPTURE_DEDUP` | `on` | Write-path MinHash NOOP/UPDATE on the raw inbox (0.33.29); never touches the wiki | P | vitest |
| `SB_REDUNDANCY` | `on` | MinHash near-dup engine feeding FORGET cross-checks (0.33.26/27) | P | bash |

`SB_NESTED_SPAWN` is internal but load-bearing: every plugin-spawned headless `claude` sets it to
`1`, and 13 scripts + the TS `guardDestructive` wrapper no-op under it (the 3 setters — lib.sh,
maintain-llm-drain.sh, extraction-quality-gate.sh — export it into spawns; they do NOT no-op).
Never set it manually except to simulate a nested spawn in a test.

## 7. Kill switches vs hook wiring

`hooks/hooks.json` holds no boolean toggles itself — its axes are event/matcher wiring and
per-hook `timeout`; the on/off axis lives in each script's own SB_* switch, where one exists.
The full event/matcher/script/timeout matrix is owned by sb-architecture-contract §2 (not
restated here). What THIS skill owns is script → switch:

- Every switch-bearing hook script appears in §6 above with its definition site (guards, gates,
  banners), or in catalog §2-§3.
- **Wired scripts with NO switch (unconditional):** `ensure-dirs.sh` and the three
  `discover-*.sh` (SessionStart scaffolding/discovery); `pre-compact.sh` and `stop-extract.sh`
  (extraction — tuned by the engine knobs, catalog §4, but no single kill switch); and
  `quality-gate.sh` (PostToolUse `Write|Edit`) — a 3-line unconditional `echo` of the
  self-review nudge with no `SB_*` read and no `_comment` in hooks.json. There is currently no
  flag that turns the post-write nudge off; only editing hooks.json does.
- **Name trap:** `SB_QUALITY_GATE` does NOT silence `quality-gate.sh`. It gates a different
  script, `extraction-quality-gate.sh` — the extraction pipeline's quality filter, invoked
  inside the Stop-hook extraction chain (`lib.sh:165`, `lib.sh:1679`, `stop-extract.sh:221`),
  not hook-wired itself. Setting `SB_QUALITY_GATE=off` to kill the post-write nudge does
  nothing to it and silently disables the extraction filter instead.
- `session-load.sh` (SessionStart) has no master switch — only the per-banner switches
  (catalog §3). (`cost-router-capture.sh` and its Stop wiring were removed with cost-router
  in 0.35.x.)

## 8. Status markers — experimental, advisory, deprecated, debug

- **Opt-in / experimental** (off until explicitly enabled): `SB_GRAPH_RANKING_BOOST` (demoted P7),
  `SB_QUALITY_GATE_LLM` (off), `SB_CONFLICT_MULTIPARENT` (off), `SB_RAW_PRUNE_AFTER_DRAIN` (unset),
  `SB_EXTRACTOR_LOCAL_URL` (inert until set), persona-rules `tool_scope.enabled` (false —
  `resource_scope.enabled` by contrast ships true, §4).
- **Advisory-only** — the flag is read by LLM prompt text in skills/agents markdown, NOT by code;
  enforcement = the model following the prompt: `SB_DREAM_AI_BLOCKS` (both files self-label it
  "advisory, not machine-enforced"), `SB_RECONCILE`/`SB_RECONCILE_TOPK`/`SB_RECONCILE_MAX`
  (knowledge-maintainer.md only), `SB_SCAN_SKIP` (setup SKILL.md only), `SB_RAW_PRUNE_AFTER_DRAIN`
  (case statement in raw-drainer.md), `SB_WIKI_FORGET` (gate in dream skill/agent markdown; the
  candidate scripts + wiring ARE code, and parity tests assert both files name the flag). Verified
  by grep 2026-07-05: none of these five appears in scripts/, mcp/src, bin/, or hooks/.
- **Deprecated** (zero live consumers, verified by grep): `SB_PERSONA_DAILY_BUDGET`
  (migrations/0.24.45.md:11 — "no longer gate anything"; `SB_PERSONA_COST_PER_CALL` survives as
  logging only), `SB_FORGET_RECENCY_DAYS` (migrations/0.24.47.md:19; v4 forget scoring dropped the
  recency AND access terms — access counts persist only as `acc=` telemetry, 0.33.30 P4b).
- **Debug escape hatches** (never set in prod): `SB_FORCE_CLI` ("debugging only", lib.sh:1293),
  `SB_DREAM_ACCEPT_SKIP_BACKUP`, `SB_MAINTAIN_FORCE`, `SB_MAINTAIN_LLM_FORCE`,
  `SB_MAINTAIN_LLM_DRYRUN`.

## 9. Add-a-flag checklist

Ground truth: everything ONE flag (`SB_PLAN_FIRST_NUDGE`, release 0.33.30, commit `6fba312`)
touched. Do all eight or a gate fails:

1. **The script/consumer.** Kill switch FIRST line of behavior
   (`[ "${SB_MY_FLAG:-on}" = "off" ] && exit 0`); numeric knobs validate-or-default (§1 idioms);
   `set -u`; fail-soft on bad stdin; ALWAYS `exit 0` in hooks; sanitize any session_id used in
   paths (`tr -dc 'A-Za-z0-9_-' | cut -c1-64`); `cygpath -u` on BRAIN_DIR for Windows; emitted
   banner text NAMES its own off switch ("Silence: SB_MY_FLAG=off."); no awk (portability);
   document known false-positive bounds in a header comment. All observable in
   `scripts/plan-first-nudge.sh`.
2. **hooks/hooks.json** (if hook-wired): new block with `_comment` naming semantics + the kill
   switch, and a `timeout`. Full new-hook recipe (per-event stdin/output contract, posture,
   validator rules): sb-architecture-contract references/extending-the-plugin.md.
3. **Test** — `tests/test-<name>.sh` covering the kill-switch branch AND the default branch
   (house rule: test fallback branches, not just happy path). Mechanics: sb-validation-and-qa.
4. **.claude-plugin/surface-budget.json** — bump `scripts`/`tests` counts in the SAME commit (6fba312:
   scripts 51→52, tests 150→151), else the validate-plugin.sh R8 gate fails.
5. **Release-commit body** — a bullet naming the flag, its default, and its kill switch
   (CHANGELOG.md was removed in 0.34.0; RELEASING.md "The checklist" owns the format).
6. **Version bump** — `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` together
   (`tests/test-release-version-bump.sh` tripwires shipped-path changes without a bump).
7. **Bundles (TS-side flags only)** — any flag consumed in mcp/src requires `cd mcp && npm run
   bundle` + committed `mcp/dist/**` in the same commit (`tests/test-bundle-current.sh`
   byte-compares).
8. **Gates green locally before push** (6fba312 commit body): tsc, vitest (offline), 
   bundle-current, run-all bash suite, validate-plugin, version-bump tripwire, portability static
   guards. Exact commands: sb-validation-and-qa. Never route around these — see sb-change-control.

Also update README.md if the flag is user-facing ("README matches what ships", RELEASING.md), and
add a `skills/upgrade/migrations/<version>.md` ONLY if the release needs a real user action.

## 10. Re-verification greps (run from repo root, git-bash/Linux/macOS)

```bash
# master census: every SB_* name + frequency (catches helper-mediated TS reads too)
grep -rhoE 'SB_[A-Z0-9_]+' scripts tests mcp/src hooks skills agents bin 2>/dev/null | sort | uniq -c | sort -rn
# shell defaults with file:line (the flag-catalog's shell ground truth)
grep -rnoE '\$\{SB_[A-Z0-9_]+:-[^}]*\}' scripts hooks bin 2>/dev/null | sort -u
# TS env reads — NOTE: misses clampEnvInt/envFloat-mediated flags; grep the bare name for those
grep -rnoE 'process\.env\.SB_[A-Z0-9_]+' mcp/src --include='*.ts' | grep -v '\.test\.ts' | sort -u
grep -rn "clampEnvInt('SB_\|envFloat('SB_" mcp/src --include='*.ts'
# config.json keys consumed in live code
grep -rn 'sb_config_get\|sb_config_bool' scripts bin 2>/dev/null | grep -v 'lib.sh:17'
# coverage set-diffs (src-only = untested; tests-only = test infrastructure)
grep -rhoE 'SB_[A-Z0-9_]+' tests | sort -u > /tmp/t; grep -rhoE 'SB_[A-Z0-9_]+' scripts mcp/src hooks skills agents bin | sort -u > /tmp/s
comm -23 /tmp/s /tmp/t   # in src, not in bash tests
comm -13 /tmp/s /tmp/t   # test-only vars
grep -rhoE 'SB_[A-Z0-9_]+' mcp/src --include='*.test.ts' | sort -u   # vitest-covered
# hook wiring + kill switches named in comments
jq -r '.. | ._comment? // empty' hooks/hooks.json | grep -oE 'SB_[A-Z0-9_]+' | sort -u
# userConfig + persona-rules shipped defaults (expect tool_scope=false, resource_scope=true)
jq .userConfig .claude-plugin/plugin.json
jq '{tool_scope: .tool_scope.enabled, resource_scope: .resource_scope.enabled}' scripts/persona-rules.default.json
# config.json seed + auto_codemap liveness (expect: consumer brain-os-run.sh:83 + kill-switch test test-extract-drain.sh:393-397)
sed -n '29,41p' scripts/ensure-dirs.sh; grep -rn 'auto_codemap' scripts tests skills agents mcp/src hooks bin
```

## Provenance and maintenance

Derived from the working tree of `C:/Workplace/Projects/claude-code-plugin` at plugin version
0.33.31 (uncommitted release batch on `main`, HEAD ancestry `6fba312`), authored 2026-07-05.
Primary evidence: `scripts/lib.sh` (config reader + precedence comment), `scripts/ensure-dirs.sh`
(seed), `scripts/persona-rules.default.json`, `.claude-plugin/plugin.json`,
`mcp/src/brain-paths.ts` (+ the divergent `mcp/src/server.ts:29-43` / `mcp/src/tools/dream.ts:75-84`
resolvers, §2), `hooks/hooks.json`, `scripts/quality-gate.sh` vs `scripts/extraction-quality-gate.sh`
(§7 name trap), per-flag definition sites listed in
[references/flag-catalog.md](references/flag-catalog.md), commit `6fba312` (add-a-flag worked
example), `skills/upgrade/migrations/0.24.45.md` + `0.24.47.md` (deprecations). Every default and
site was re-verified by reading the file or by the §10 bulk greps on 2026-07-05.

Volatile facts and their one-line re-checks (all in §10): the ~187-name census; the 92
bash-tested / 9 vitest-tested coverage split; the persona-rules shipped defaults; the config.json
seed keys; `auto_codemap` liveness; hook wiring/timeouts (`jq . hooks/hooks.json`); the surface
budget counts (`cat .claude-plugin/surface-budget.json`). If plugin.json's version no longer starts with
0.33, re-run all of §10 before trusting any table here.
