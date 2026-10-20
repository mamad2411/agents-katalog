---
name: sb-failure-archaeology
description: The settled-battle chronicle of the second-brain plugin — ~45 incidents grouped into 9 cross-cutting failure classes, the tried-then-backed-out undo table (23 rows), dead/stalled work, and the condensed 9-era history. Load this when a bug matches a known signature and the historical root cause + evidence sha is needed; when someone proposes something that may have been tried and reverted (ranking boosts, symlinks, spend caps, root .mcp.json, vendored skills); when asking "has this broken before", "why is X shaped this way", "did we already try Y"; when writing a post-mortem, regression test, or migration note for a recurring class; or when auditing whether an OPEN finding is still open. Do NOT load for live triage of a currently-failing system (use sb-debugging-playbook), for design invariants and why-this-architecture (sb-architecture-contract), or for release/gating process (sb-change-control).
---

# sb-failure-archaeology — the incident chronicle

This skill is the project's institutional memory of failure: what broke, why, what fixed it,
and what was tried and abandoned. Its job is to stop you from re-fighting settled battles and
re-shipping known bug classes. The full incident table lives in
[references/chronicle.md](references/chronicle.md) — SKILL.md is the index, the class map, the
undo table, and the search recipes.

**Snapshot date:** as of 0.33.31 (2026-07-05), when HEAD was `6fba312` (release 0.33.30) and the
0.33.31 batch was still UNCOMMITTED in the working tree. Any status marked FIXED-WT@0.33.31 means
"fixed in the working tree, not yet in a released commit" — **0.33.31 has since landed as
`e9dfbd1`**, so a FIXED-WT@0.33.31 status now reads as plain FIXED. (The snapshot originally
proved this against CHANGELOG.md, removed from main in 0.34.0; it lives on `archive/docs`.)

## Terms used in the chronicle (defined once)

| Term | Meaning |
|---|---|
| BRAIN_DIR | Runtime state dir, default `~/.second-brain` (markers, logs, dreams, transcripts, access counts) |
| KNOWLEDGE_DIR / wiki | Canonical knowledge wiki at `~/knowledge/wiki`. Anything writing to legacy `~/.second-brain/wiki` is a bug even if it "works" |
| hot tier | Files injected at SessionStart (USER.md rules, PROJECT.md blockers/decisions, banners) |
| dream | Background consolidation job: snapshot wiki + transcripts → staged changes → accept/discard (`dream_create`/`dream_accept`) |
| drainer | Out-of-band extraction pipeline (`extract-drain.sh` + `agents/raw-drainer.md`) mining archived transcripts and the raw inbox on a timer |
| raw inbox | Captured docs/items pending drain into wiki pages (`raw-capture-cli`, `raw-scan-cli`) |
| maintainer | `agents/knowledge-maintainer.md` — the consolidation agent dispatched to organize the wiki |
| FORGET | Eviction/archiving scoring pass that retires low-value wiki pages (structural-importance-only since 0.33.25) |
| REFLECT | Dream phase (0.33.28) synthesizing cross-cutting practice pages from clusters |
| MOC | Map-of-content hub pages generated under wiki `projects/` and `themes/` |
| guards | PreToolUse hooks: `symlink-guard.sh`, `persona-tool-guard.sh`, `wiki-write-guard.sh` |
| MinHash | Near-duplicate detection engine (0.33.26) gating dedup/FORGET |
| bwrap | bubblewrap sandbox jailing headless consolidation runs on Linux |
| drm_* / ec=124 | Dream job dirs under `~/.second-brain/dreams`; exit code of a `timeout`-killed process |

Status legend used everywhere: **FIXED@ver** (released) · **FIXED-WT@0.33.31** (working tree
only) · **MITIGATED** (partial, residual documented) · **OPEN**.

## Ground rules for reading this history

- **Releases ship directly on `main`** as version-locked batches (`release: X.Y.Z — …`
  commits). No hotfix branches; the undo mechanism is a forward commit, never `git revert`
  (verified: `git log --all --oneline --grep="^Revert" | wc -l` → 0). Undo commits carry the
  rationale in the body, often with "Supersedes"/"CORRECTS" markers and an inverted or new CI
  guard so the reverted shape cannot come back.
- **Windows (git-bash/MSYS) is the dev platform but has NO CI lane** — every Windows bug class
  in the chronicle shipped through green CI. The local suite is the release gate for Windows.
- **The two recurring meta-causes:** (1) "green ≠ working" — tests asserting PRESENCE (grep a
  source file) instead of EFFECT (run it); quantified in CHANGELOG 0.24.50 ("506 green tests
  missed 14 bugs… an audit found 53 tautological tests"). (2) Silent swallow — `2>/dev/null` /
  `|| exit 0` hiding multi-release breakage; the house rule is fail-loud via `sb_log_error`.
- **The version line is NOT monotonic:** 0.2.x→0.7.0, then 1.0.0→1.9.0, then 2.1.0→2.11.1,
  re-baselined 2.11.1→0.11.1 on 2026-05-24 (commit `88602f7`: "The 2.x numbering was
  aspirational"), then 0.11.1→0.33.x. archive/docs:CHANGELOG.md covers 0.14.0+ only; earlier history exists
  only in git.

## The 9 cross-cutting failure classes

Every incident in the chronicle belongs to at least one of these. When triaging a NEW bug,
check its signature against this table first — the fix pattern is usually already established.

| # | Class | Mechanism | Chronicle §§ | Established fix pattern |
|---|---|---|---|---|
| 1 | Path-form mismatch at the Node↔bash / Windows↔POSIX boundary | `C:\…` vs `C:/…` vs `/c/…` vs `\r`-tainted paths; comparisons and tools silently mis-parse | 1, 2, 4, 10, 18 | Normalize ONCE at the boundary funnel (`sb_normalize_path` in lib.sh, the lib.sh BRAIN_DIR block, `mcp/src/brain-paths.ts`, `cleanEnvPath`, `toBashPath`) — never per-consumer |
| 2 | Silent swallow hides multi-release breakage | `2>/dev/null`, `\|\| exit 0`, guessed error messages | 2.5, 6, 7, 12, 24 | Fail loud; report the REAL stderr; route through `sb_log_error` |
| 3 | Green-but-fake gates | Presence-vs-effect tests, stubbed binaries, suites silently SKIPPING on the buggy OS, no version-bump assertion, vitest-isn't-tsc | 13 | Behavioral tests vs independent oracles; mutation-proven RED; static class scanners (`test-script-portability.sh`, source-scans, `test-real-kb-isolation.sh`, `test-release-version-bump.sh`) |
| 4 | Self-reinforcing feedback loops in the knowledge machinery | Boosts computed from boosted scores; generated pages re-entering the generator's input; autofix↔regenerate churn | 8, 9, 12 | Freeze inputs (pre-boost snapshot); exclude `generated: true` output from generator input; converge all emitters on one canonical byte shape |
| 5 | Ambient/global state trusted over per-process signals | Global slug pin hijack; capture destination from ambient session, not the scanned resource | 15 | Per-process authority; known-project gates; `origin:` provenance; fail-loud on mismatch |
| 6 | Non-GNU userland silent divergence | mawk, BSD sed/grep, bash 3.2 parser, Windows jq, MSYS schtasks translation | 10A, 11, 13, 18, 19 | Portability scanner rules; `ENVIRON[]` not `awk -v`; no GNU regex escapes; macOS CI on real bash 3.2 (since 0.24.44) |
| 7 | Byte-budget starvation silently dropping priority context | Banners spend the hook budget before forced USER.md/PROJECT.md sections; end-truncation | 21 | `force` appends + RESERVE forced-section bytes from the banner budget |
| 8 | Cap/eviction logic keyed on the wrong ordering | UUID-lexical filename sort treated as age order | 23 | Rank by MTIME; adversarial-ordering test |
| 9 | Grants/wiring drift between prose and machine config | Agent protocol mandates tools its whitelist excludes; renamed `subagent_type` no-ops dispatch | 13, 20 | Machine locks on prose promises (`mcp/src/agent-grants.test.ts`, `test-subagent-dispatch-resolves.sh`) |

## The undo table — tried, backed out, do not re-fight

Zero literal `git revert` commits exist; each row was undone by a forward fix with rationale.
Before proposing anything resembling a row below, read its "why" — most rows also have a CI
guard that will actively reject the old shape.

| # | What was tried | Why backed out | Evidence | Current state |
|---|---|---|---|---|
| 1 | v0.x graph layer (`compile-graph.sh`) | "graph layer never used in practice" | deprecated 0.7.0 `5cc0027` | Reborn as typed bi-temporal graph 0.22.0 (`11bd5fe`); its ranking boost later demoted too (row 18) |
| 2 | Reflection pipeline + 6 skills (0.x era) | v1.0 redesign judged it noise | dropped `65bc3c4` | Gone; "reflection" today = the unrelated dream REFLECT op (0.33.28) |
| 3 | `knowledge_index`/`knowledge_feedback` MCP tools | v1.0 simplification | removed `99986b9` | Never returned |
| 4 | Embeddings removed from search | v1.0 rebuilt search on ripgrep, "no embeddings" | `8b89178` | Restored: hybrid BM25+ONNX with `degraded:'bm25-only'` honesty flag (0.24.39) |
| 5 | External episodic-memory plugin dependency | dropped 0.5.4 | `eaf254b` | Rebuilt natively in-plugin at 2.2.0 (`24f3f45`) |
| 6 | CHANGELOG.md deleted at re-baseline | "not maintained for now" | `88602f7` | Re-created 2026-06-11 (`782861a`); now the narrative of record |
| 7 | 2.x version numbering | "aspirational; not 1.0.0 maturity" | `88602f7` re-baseline 2.11.1→0.11.1 | 0.x ever since; RELEASING.md codifies the release-gate lesson |
| 8 | `.mcp.json` at repo root; later `${CLAUDE_PLUGIN_ROOT:-.}` form | Claude Code substitutes only the BARE token → cwd-relative path → server failed for every user; the 0.24.5 guard REQUIRED the broken form | root move `96b5d8a`; broken form `c324033`; revert+restructure `7c5e162` (0.24.35) | Manifest at `.claude-plugin/mcp.json` via plugin.json `mcpServers`; root `.mcp.json` now FAILS validate-plugin.sh |
| 9 | code-review FP auto-record ratchet + haiku scorer pin + dropping the 16-69 confidence band | wrong auto-suppression hides real bugs indefinitely; haiku gating Opus = capability inversion | `ff764d5` `580cb3b` `40b78cc` (0.18.0) | FP store grows only from explicit user dismissals; scorer inherits session model; band shown as "lower-confidence (unverified)" |
| 10 | Enforced daily Opus spend cap | tier→model assignments change across releases; no dollar limit keyed to a model name | `d856ccf` (0.24.45) | Spend reported, never enforced; `COST_ROUTER_OPUS_CAP_USD`/`SB_PERSONA_DAILY_BUDGET` inert |
| 11 | Vendored superpowers skills inside the plugin (2.4.0) | token/surface diet | vendored `18030a3`; de-vendored 0.24.42 `40f0acd` | Removed; `docs/superpowers/` keeps only plans/specs |
| 12 | "BLOCKING REQUIREMENT — you MUST" maintainer banner + auto-stage auto-dispatch | Anthropic-doctrine conflicts: plugins shouldn't coerce the model or auto-spawn side-effectful subagents | added `e1c907a`; softened 0.21.0 `4837873` | Suggestion banners only; auto-dispatch returned only as gated, consented automation (0.25.0→0.30.0) |
| 13 | ~9 model-invocable skills in the catalog | per-session metadata + selection ambiguity | trimmed 0.21.0/0.27.0/0.29.0/0.33.24 (`4837873` `2f1a1eb` `5ccdde3` `acfe1ad`) | Model catalog = 2 since 0.44.0 removed code-review-deep (query, using-second-brain); rest slash-command-only |
| 14 | Slug precedence `CLAUDE_PROJECT_DIR > pin > cwd` (0.24.29) | var inconsistently set across MCP spawns → stale pin still hijacked; tests were made green by reverting precedence ("green tests over real-env correctness") | `6c43b25` → corrected next day `c08dd6f` (0.24.30) | `CLAUDE_PROJECT_DIR > cwd-if-known-project > pin > cwd`, one shared resolver, verified live |
| 15 | Claim in `9a03a26` that bare-YAML `related:` lists were migrated | claim was false | `6b1535a` "…CORRECTS false claim in 9a03a26" | Fixed; loud self-correction commits are the house convention |
| 16 | FORGET score rewarding access-frequency (w=0.30) + recency (w=0.25) | usage-frequency = recsys rich-get-richer hub bias; goal-agnostic recency decay demonstrably hurts | `7638c94` (0.33.25) | Structural-importance-only score; `SB_FORGET_W_ACCESS`/`_W_RECENCY` inert; access survives as `acc=` telemetry |
| 17 | Access-frequency SEARCH boost (`1 + 0.1·min(count,10)`) | same hub-bias class as the graph boost | cut 0.33.30 `6fba312` | Removed from ranking; counts recorded as telemetry only. Open: no regression lock yet; server.ts tool description still advertises it |
| 18 | Uncapped graph ranking boost | hub pages inflated scores ~10,000×; exact-title pages floor-evicted | capped/frozen R2.1 `b210133` (0.24.39); demoted off-by-default P7 `71df749` (0.33.22) after a live measurement showed a wash | Off by default (`SB_GRAPH_RANKING_BOOST=1` opt-in); `knowledge_neighbors` is the graph-discovery tool |
| 19 | Historical 1.x/2.x migration rows in `skills/upgrade/SKILL.md` | dead weight; runner must not re-fire across the re-baseline | pruned `f63bd25`; table split `782861a` | Per-release `skills/upgrade/migrations/<version>.md` (18 files as of 0.33.31) |
| 20 | Dead migrations + "phantom knobs" (documented env vars nothing read) | cleanup | `83e8402` (0.31.0) | Removed |
| 21 | Duplicate persona-card emission (per-prompt AND SessionStart) | ~330 tokens re-sent every prompt, ~95% USER.md paraphrase | `98b3f20` (0.32.0) | Single card path; per-turn injection measured ~662 B (0.33.30 P1c) |
| 22 | Live `access-counts.json` contents | file contained ONLY test artifacts — eval runs had polluted live state | reset in R2 (0.24.39) | Engine resolves via `SB_BRAIN_DIR`/`BRAIN_DIR` so tests can't pollute live state |
| 23 | doubt-skill artificial question/layer count limits | limits were arbitrary | `afabda1` (0.6.4 era) | Skill itself retired in the v1.0 purge |

## Dead / stalled work (don't rediscover it)

- **Branch `fix/home-cwd-relative-brain-dir` — DEAD.** Its only commit `ef7a8e7` is
  patch-identical to main's `788f193` (released as 0.33.17): `git cherry main
  fix/home-cwd-relative-brain-dir` → `- ef7a8e7…` (minus = already on main; verified
  2026-07-05). Safe to delete; nothing unique on it.
- **Plans staged with NO code (as of 0.33.31):**
  `archive/docs:docs/superpowers/plans/2026-06-30-p2-learning-to-guardrail.md`,
  `…-p3a-orientation-code-map.md`, `…-p6-quarantine-dual-llm.md` — CHANGELOG 0.33.30: "Plans
  staged (no code)". The P6 quarantine/dual-LLM design is the fix-of-record for the open
  headless credential-exfil residual (chronicle §20) but is UNIMPLEMENTED.
- **Deep-dive waves defined in `archive/docs:docs/specs/2026-06-10-plugin-deep-dive-improvements-design.md`
  but never shipped:** R3 (security follow-ups — partially overtaken by P6a/P6b but never
  closed as R3), R5.2 (cost-router 2-week dogfood → keep-or-kill decision — never recorded in
  this repo, and mooted when cost-router was removed in 0.35.x), R9 (data-plane integrity & privacy — never started; partially overtaken by
  0.33.21 transcript sanitization). R7 shipped only its "a" slice (observability, `918f34a`);
  the served→used retrieval metric has no commits. Treat all as open/candidate, not failed.
- **Misc residue:** backup tags `sb-backup/pr1-…`/`sb-backup/pr2-…` point at commits already on
  main (harmless); `bash.exe.stackdump` at repo root is an untracked crash artifact, not
  history.

## The 9 eras, condensed

| Era | Versions (dates 2026) | What defined it |
|---|---|---|
| 1 Prototype | 0.2.1–0.7.0 (04-24→04-30) | "Self-evolving companion"; lib.sh + hybrid search born; first graph layer deprecated at 0.7.0 |
| 2 v1.0 redesign | 1.0.0–1.9.0 (05-01→05-07) | Ground-up rewrite: hot-tier model, MCP server born, search rebuilt on ripgrep (no embeddings), esbuild-bundled dist committed |
| 3 v2.x persona core | 2.1.0–2.11.1 (05-12→05-22) | Episodic memory, persona layers, vendored superpowers, first release-verification gate (v2.11.0) |
| 4 Re-baseline + memory science | 0.11.1–0.22.x (05-24→06-01) | 2.11.1→0.11.1 re-baseline + CHANGELOG deleted; forgetting/recall eval; shared vector-deps; 0.21.0 hardening (guards born); 0.22.0 bi-temporal graph returns |
| 5 KB restructuring + SP waves | 0.22.2–0.24.31 (06-01→06-08) | Graphiti/GraphRAG adoption, AI-block pages, raw inbox + deep-scan + drain (SP-0…SP-5), headless maintainer, slug-precedence saga |
| 6 Deep-dive repair R1–R8 | 0.24.37–0.24.50 (06-10→06-13) | Whole-plugin audit → 9 waves; R1 extraction loop, R2 hub-proof ranking, R4 dream lifecycle, R8 process gates; YAML corruption era repaired |
| 7 Autonomy consent + cross-OS | 0.25.0–0.32.0 (06-14→06-17) | Gated auto-accept consent ladder, CRLF classes, 0.31.0 un-starve automation, 0.32.0 nested-spawn guard + persona slim |
| 8 Scoping M3 + Windows-first | 0.33.0–0.33.16 (06-18→06-24) | Monorepo family model + provenance; 9 releases in one day (06-22) fixing Windows classes (junctions, dream_accept, schtasks) |
| 9 Constitution + Diet | 0.33.17–0.33.31 (06-26→present) | CONSTITUTION.md governance; P-workstreams (capture, security P6a/b, graph-boost demotion, P4 diet/MinHash/REFLECT); deep-audit batch B in-flight |

## Known documentation defects (real, verified)

1. ~~`## 0.33.19` orphaned heading~~ and ~~CHANGELOG tail ordering quirk~~ — **both MOOT**: CHANGELOG.md
   was removed from main in 0.34.0, so nothing in the tree parses it any more. The file (and both
   quirks) survive on `archive/docs` if you are reading pre-1.0 history there.
2. **`knowledge_search` tool description stale** — `mcp/src/server.ts:74` still advertises the
   access-frequency boost removed in 0.33.30 (verified 2026-07-05). OPEN (audit low).

## How to search the chronicle (and beyond it)

All commands run from the repo root in bash (git-bash on Windows works).

```bash
# Is this symptom in the chronicle? Search the sibling first:
grep -in "<keyword>" .claude/skills/sb-failure-archaeology/references/chronicle.md

# Find the release that fixed/introduced something:
git show archive/docs:CHANGELOG.md | grep -n "^## " | head -40   # version headings (0.14.0+ only)
git show archive/docs:CHANGELOG.md | grep -n -i "<keyword>"        # full narrative search
# (CHANGELOG.md was removed from main in 0.34.0 — release records now live in release-commit
#  bodies, so `git log --grep` above is the primary search for anything 0.34.0 or newer.)

# Find the commit history of a phrase/mechanism (works pre-0.14 too):
git log --all --oneline -i --grep="<keyword>"   # commit subjects/bodies
git log --all --oneline -S"<code-string>"       # when a string was added/removed
git log --oneline --follow -- <path>            # one file's history
git blame -L <start>,<end> <path>               # who last touched these lines and why

# War-story comments in live code (the codebase narrates its own incidents):
grep -rn "0\.33\.\|0\.24\.\|regression\|fail-open\|fail-OPEN\|POISON" scripts/*.sh | head -30

```

Interpretation rules: a chronicle **OPEN** status was true at the snapshot date — always
re-verify in code before acting on it; an incident's line-number evidence drifts — re-anchor by
the quoted comment text; anything sourced from "the 2026-07-02 deep audit" refers to the
11-agent audit whose HIGH-severity closure is documented under CHANGELOG `## 0.33.31`.

## Incident index (full detail in references/chronicle.md)

| § | Incident (one line) | Status |
|---|---|---|
| 1 | Windows HOME→CWD stray-`.second-brain/` resolver class (~16 call sites) | FIXED@0.33.17 |
| 2 | Dream-on-Windows chain: 5 stacked root causes (backslash → CRLF env → WSL shadow → HOME unset → tar `C:\` = remote host) | FIXED@0.33.12 |
| 3 | `ln -s` MSYS deep-copy: ~490MB duplicated per version, 3.1GB cache | FIXED@0.33.7 |
| 4 | All three PreToolUse guards silently fail-open on Windows (G-HOOK-2 re-arm) | FIXED-WT@0.33.31 |
| 5 | R1: 169 unattended extraction timeouts, recursive claude self-spawn, 18× re-archives | FIXED@0.24.38 |
| 6 | Automation drifted to manual (starvation + silent failure) + ee8a74c poison-pill regression | FIXED@0.31.0 |
| 7 | Dream lifecycle: 19-day nag, running-state deadlock, bwrap RestrictNamespaces 100% failure | FIXED@0.24.22/0.24.41; mediums OPEN |
| 8 | Search-ranking corruption family (~10,000× graph boost; access-count pollution; P4b cut) | FIXED@0.24.39/0.33.30; residuals OPEN |
| 9 | REFLECT feedback loop (generated pages re-entered clustering input) | FIXED-WT@0.33.31 |
| 10 | jq on Windows: CRLF faucet (121 call sites) + `jq`-without-`-c` shredding projects.jsonl | FIXED@0.30.1 / FIXED-WT@0.33.31 |
| 11 | CRLF frontmatter loss + autofix double-block corruption | FIXED@0.29.2 |
| 12 | YAML/graph corruption era: ~86% of pages invalid, no real YAML parser anywhere | FIXED@0.26.0 |
| 13 | run-all SKIP false-green + the whole green-but-fake-gate family | FIXED-WT@0.33.31; members OPEN |
| 14 | Silently-wrong-output wave (awk range collapse, `0\n0`, wc -l, printf '- ') | FIXED@0.29.4 |
| 15 | Attribution: 88 docs filed into the wrong project; slug hijack prequel | FIXED@0.33.0 |
| 16 | MCP server failed to start for every installed user (`${CLAUDE_PLUGIN_ROOT:-.}`) | FIXED@0.24.35 |
| 17 | Release/process: unversioned ship; missing 0.33.19 CHANGELOG heading | FIXED@0.30.2; heading MOOT — CHANGELOG.md removed 0.34.0 |
| 18 | awk/mawk/BSD portability class (6 shipped silent no-ops) | FIXED (per version) |
| 19 | macOS bash-3.2 class (case-in-comsub parse error; readlink -f) | FIXED@0.24.33 |
| 20 | Security: staging symlink escape; secret leak; nested-spawn reachability; invisible Unicode; dream-accept data loss; agent grants | Mixed — see chronicle |
| 21 | SessionStart budget starvation silently dropping USER.md/PROJECT.md | FIXED@0.29.0; timeout OPEN |
| 22 | Raw-inbox drain truncation/duplication trilogy + drainer wiki misroute | FIXED@0.33.5; misroute MITIGATED |
| 23 | Transcript eviction in UUID-lexical order destroyed undrained captures | FIXED-WT@0.33.31 |
| 24 | "Wired ≠ works": the drainer that was never installed; shim-less scheduler | FIXED@0.33.19 |
| 25 | Persona noise: double injection, phantom dismiss, author-identity leak | FIXED@0.32.0 |
| 26 | Deep-audit 2026-07-02 disposition ledger (9 HIGH closed; open medium/low backlog) | 9 HIGH FIXED-WT@0.33.31 |
| 27 | Chronology quick-reference table (incident → version → sha) | — |

## Provenance and maintenance

**Derived from** (repo evidence only): `CHANGELOG.md` (1522+ lines, read against
`git show <sha>:CHANGELOG.md` for removed entries), `git log --all` (780 commits at HEAD
`6fba312`), `docs/plans/*.md`, `docs/specs/*.md` (notably
`2026-06-10-plugin-deep-dive-findings-appendix.md` and
`2026-06-18-project-scoping-model-design.md`), war-story comments in `scripts/lib.sh`,
`scripts/dream-accept.sh`, `scripts/extract-drain.sh`, `scripts/symlink-guard.sh`,
`tests/run-all.sh`, `mcp/src/tools/knowledge-search.ts`, `mcp/src/tools/graph-cluster-cli.ts`,
and the 2026-07-02 11-agent deep audit whose closure is documented in CHANGELOG `## 0.33.31`.
Authored 2026-07-05 against the uncommitted 0.33.31 working tree.

**Re-verification one-liners** (run before trusting a volatile fact):

```bash
git log -1 --oneline                                        # HEAD (was 6fba312 / 0.33.30)
grep -o '"version": *"[^"]*"' .claude-plugin/plugin.json    # was 0.33.31 (working tree)
git log --oneline | wc -l                                   # commit count (was 780)
git cherry main fix/home-cwd-relative-brain-dir             # "-" = branch still dead/merged
git show archive/docs:CHANGELOG.md | grep -c "^## 0.33.3"        # pre-1.0 narrative (removed from main 0.34.0)
grep -n "access-frequency" mcp/src/server.ts | head -2      # stale tool description still present?
ls skills/upgrade/migrations/ | wc -l                       # migration files (was 18)
git log --all --oneline --grep="^Revert" | wc -l            # still 0 true reverts?
```

Every FIXED-WT@0.33.31 status must be flipped to FIXED@0.33.31 once
`git log --oneline --grep "0.33.31"` shows the release commit. New incidents belong in
`references/chronicle.md` with the same symptom → root cause → evidence → fix → status shape,
and in the class table above if they fit (or as a new class if they genuinely don't — that is
rare and worth flagging).
