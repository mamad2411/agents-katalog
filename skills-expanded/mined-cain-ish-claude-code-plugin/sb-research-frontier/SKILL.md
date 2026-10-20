---
name: sb-research-frontier
description: >-
  The second-brain plugin's open research problems where this repo can pass state of the art —
  what SOTA memory systems (mem0, Letta/MemGPT, Zep/Graphiti, ChatGPT memory, RAG-over-code) get
  wrong, which in-repo asset gives this project an edge, the first three file-level steps, and a
  falsifiable "you have a result when …" milestone for each. Load when picking the next frontier
  workstream (P2 learned guardrails, P3a code-map, P3b reranker, P8 eval, P6 autonomous
  consolidation, guard-liveness injection, cross-project practice transfer), when asked "what
  should this project do next / what would be novel / where can it beat SOTA", or when writing a
  new plan doc for any of these. Do NOT load for executing the autonomous-consolidation campaign
  (use sb-autonomous-consolidation-campaign), for the evidence-bar/idea-lifecycle discipline (use
  sb-research-methodology), for novel-vs-known claim wording against the ecosystem (use
  sb-external-positioning), or for how the shipped memory machinery works today (use
  sb-memory-systems-reference).
---

# sb-research-frontier — open problems where this project can pass SOTA

This skill is the frontier map: six problems where the second-brain plugin has a real,
asset-backed shot at going past published/shipped state of the art, each with an honest status.
It tells you WHY SOTA fails, WHAT this repo already has, WHERE to start (file-level), and WHEN
you may claim a result. It does not teach methodology (sb-research-methodology), campaign
execution (sb-autonomous-consolidation-campaign), or claim wording (sb-external-positioning).

**Repo:** `C:/Workplace/Projects/claude-code-plugin` (a Claude Code plugin). All commands run
from the repo root in git-bash/Linux/macOS bash unless flagged.

**Version stamp:** everything below verified against the working tree **as of 0.33.31
(2026-07-05; 0.33.31 was uncommitted at authoring — HEAD was `6fba312` = 0.33.30)**. Statuses
are volatile; re-verify with the one-liners in Provenance before acting.

## Terms used below (defined once)

| Term | Meaning | Deep definition lives in |
|---|---|---|
| BRAIN_DIR | runtime state dir, default `~/.second-brain` | sb-architecture-contract |
| KNOWLEDGE_DIR | knowledge dir, default `~/knowledge`; the wiki is `KNOWLEDGE_DIR/wiki` | sb-architecture-contract |
| dream | staged background consolidation of the wiki (snapshot → 7 phases → accept/discard) | sb-memory-systems-reference |
| drainer | out-of-band timer job `scripts/extract-drain.sh` that processes archived transcripts outside any session | sb-run-and-operate |
| FORGET | the dream phase that proposes reversible page archiving (never hard-deletes) | sb-memory-systems-reference |
| guard | a PreToolUse hook script that can deny/ask/rewrite a tool call before it runs | sb-architecture-contract |
| hot tier | USER.md + PROJECT.md context injected at SessionStart under a byte budget | sb-architecture-contract |
| surface budget | `.claude-plugin/surface-budget.json` ratchet — live counts of skills/agents/scripts/tests may not grow without a same-commit bump | sb-change-control |

**Status legend:** `PLAN-QUEUED` = plan doc exists, zero code. `PARTIAL` = some shipped
substrate, milestone not met. `NOT-STARTED` = no plan doc, no code.

## Frontier map

| # | Problem | Status (as of 0.33.31) | Plan doc |
|---|---|---|---|
| 1 | P2: learning → active guardrail | PLAN-QUEUED (zero code) | `archive/docs:docs/superpowers/plans/2026-06-30-p2-learning-to-guardrail.md` |
| 2 | P3a: orientation code-map | SHIPPED 0.33.33–0.33.35 (Phases 1–3; Phases 4–5 open — verified 2026-07-13 at 0.33.37) | `archive/docs:docs/superpowers/plans/2026-06-30-p3a-orientation-code-map.md` |
| 3 | P8: memory eval / silent-failure detection | PARTIAL | spec §6 P8 (no standalone plan doc) |
| 4 | Safe fully-autonomous consolidation | PLAN-QUEUED + shipped substrate | `archive/docs:docs/superpowers/plans/2026-06-30-p6-quarantine-dual-llm.md` |
| 5 | Guard liveness as a continuous property | PARTIAL | none (spec §6 P8 names it) |
| 6 | Cross-project practice transfer | NOT-STARTED | none |

The governing spec for 1–5 is
`archive/docs:docs/superpowers/specs/2026-06-26-second-brain-constitution-and-diet-design.md` (workstreams
§6, open questions §10, success criteria §8). All frontier work is bound by `CONSTITUTION.md`
(autonomy, untrusted-content isolation, cross-platform, reversibility, surface budget,
single-source resolution) — read it before writing any plan.

---

## 1. P2 — Learned practice compiled into a tool-time guardrail

**Why SOTA fails here.** Shipped memory systems (mem0, Letta/MemGPT, ChatGPT memory) store
learned preferences as retrievable prose: the model must retrieve the memory, keep it in
context, and choose to obey it. A remembered "never force-push main" is one context eviction
away from being ignored, and nothing enforces it at the moment the tool call fires. Memory
that only informs is not memory that protects. (Project direction, context accepted by the
maintainer 2026-07-04; ecosystem comparison wording → sb-external-positioning.)

**This repo's asset.** A working enforcement point plus a working signal pipeline — the two
halves SOTA lacks, already running autonomously:

- `scripts/persona-tool-guard.sh` — PreToolUse guard over `Bash|PowerShell|Write|Edit|MultiEdit|Read|WebFetch|WebSearch|Task|Agent`,
  rules from `scripts/persona-rules.default.json`, every verdict audit-logged via
  `sb_log_audit`, kill switch `SB_PERSONA_GATE=off`. Re-armed on Windows path forms in 0.33.31
  (`sb_normalize_path` funnel — archive/docs:CHANGELOG.md, 0.33.31 entry).
- `scripts/merge-persona-signals.sh` — Stop-hook signal accumulation into
  `BRAIN_DIR/persona-signals.jsonl` with word-overlap dedup; `count>=2` high-confidence signals
  already auto-graduate (today: to `BRAIN_DIR/persona-learned.md` via `sb_pin_to_learned`;
  USER.md is human pins only).
- A proven bi-temporal soft-retire pattern to copy: `scripts/merge-edges.sh`
  (`valid_from`/`valid_to`, conflict log, never hard-delete).
- A complete, constitution-checked plan: `archive/docs:docs/superpowers/plans/2026-06-30-p2-learning-to-guardrail.md`.

**First three steps (from the queued plan — follow it, do not re-design):**

1. **Task 1 — citation contract + slug plumbing.** Extend `scripts/extract-prompt.txt`
   `persona_signals[]` with the optional structured `rule` hint (`{tool, match_command|match_path, reason}`);
   pass the project slug from `scripts/stop-extract.sh` / `scripts/pre-compact.sh` into
   `scripts/merge-persona-signals.sh` so a transcript citation path
   (`~/.second-brain/transcripts/<session_id>_<slug>_<date>.txt`) is reconstructable.
2. **Task 2 — loader merge.** In `scripts/persona-tool-guard.sh`, merge runtime store
   `~/.second-brain/persona-rules.learned.json` on top of the pristine defaults (one `jq -s`;
   learned rules appended AFTER defaults, filtered to `valid_to == null`; fail-soft to base);
   surface the citation in `permissionDecisionReason`; kill switch `SB_PERSONA_LEARNED=off`.
   New test `tests/test-persona-learned-rule.sh` — must cover the no-learned-file branch.
3. **Task 3 — synthesis.** In `merge-persona-signals.sh`, graduate a validated `rule`-hinted
   `count>=2` high-confidence signal into a citation-carrying learned rule (regex compile-check
   via `grep -qE`; upsert-by-name idempotent; cap ~200 rules). Prose-only signals keep flowing
   to USER.md unchanged — that is the rule-worthy vs prose-worthy discriminator.

Fenced wrong paths (the plan rejects these explicitly): editing `persona-rules.default.json`;
learned `deny`/`rewrite` actions (learned rules are hard-capped to `action:"ask"`);
regex-subsumption contradiction detection (exact-string identity only); `awk`; hard deletes;
any manual accept gate.

**You have a result when:** a rule synthesized end-to-end from a real session — zero
hand-written rule JSON — fires `action:"ask"` on a matching PreToolUse call, its
`permissionDecisionReason` carries the transcript citation, and the verdict lands in
`BRAIN_DIR/audit-log.jsonl`; AND a hand-planted `action:"deny"` in the learned store is NOT
honored (the ask-cap is enforced, test-asserted); AND a contradicted rule auto-retires by
`valid_to` and stops firing while staying on disk. Falsifier: if the learned rule only appears
in injected context but the tool call proceeds un-asked, you have SOTA-equivalent passive
memory, not a result.

**Status: PLAN-QUEUED, zero code.** `grep -r 'persona-rules.learned' --include='*.sh' scripts/`
→ no hits; the string appears only in the plan doc. Caution: the plan was authored at 0.33.29 —
its version target (0.33.30) and test-budget arithmetic (`151 → 154`) are stale; recompute
against the live `.claude-plugin/surface-budget.json` (tests: 153 as of 0.33.31) in the same commit
(mechanics → sb-change-control).

---

## 2. P3a — Orientation: a standing, token-capped code-structure map

**Why SOTA fails here.** RAG-over-code retrieves snippets per query but gives the model no
standing mental model — every cold session re-derives the repo by grep. Aider's repo-map is the
closest prior art but is interactive-session-scoped and defaults to native tree-sitter
(node-gyp — exactly the heavy-native-dep class `CONSTITUTION.md` forbids); graph-code tools
that dump whole-repo structure blow the token budget. Nothing shipped gives a persistent,
auto-refreshed, budget-capped orientation layer tied to a memory system. (Aider comparison:
plan §Task 0 decision table; "Aider's repo-map is itself approximate" — plan doc.)

**This repo's asset.**

- The out-of-band drainer (`scripts/extract-drain.sh`, single-flight lock, timer via
  `scripts/install-extract-timer.sh`) — a proven home for regeneration with no in-session cost.
- JIT injection discipline with a measured baseline: the per-turn injection is ~662 B / ~165
  tokens with no wiki body (P1c, archive/docs:CHANGELOG.md 0.33.30 entry) — a 2k-token map has a defined
  budget posture to slot into.
- `mcp/src/tools/graph-store.ts` bi-temporal fold machinery, reusable by import for layer-5
  code↔wiki edges.
- A complete phased XL plan with the cross-platform generator decision already made:
  `archive/docs:docs/superpowers/plans/2026-06-30-p3a-orientation-code-map.md`.

**What shipped (Phases 0–3, 0.33.33–0.33.35 — the plan executed, kept here as the as-built
record):**

1. **Phases 1+2 (0.33.33).** The `mcp/src/tools/codemap/` module family: `git ls-files -z`
   source enumeration with blowup caps (`SB_CODEMAP_MAX_FILE_BYTES` 512 KiB,
   `SB_CODEMAP_MAX_FILES` 4000); Tier-0 pure-JS regex symbol/import extraction for ts/js/py
   (node-tree-sitter REJECTED; WASM deferred to Phase 5); **deterministic** PageRank (damping
   0.85, fixed 30 iterations or L1<1e-6, sorted accumulation order); store at
   `BRAIN_DIR/projects/<slug>/codemap/{graph.json,map.md}` capped at `SB_CODEMAP_TOKEN_BUDGET`
   (default 2000 tokens); `code-map-cli` bundle; and the two MCP tools `code_map` (ranked map +
   honest `stale` flag) and `code_neighbors` (BFS blast-radius; `direction:'in'` = what breaks).
2. **Phase 3 (0.33.34).** Real drift detection (`drift.ts` — one predicate shared by CLI and
   both tools: `git_rev` ≠ HEAD, nogit-mtime fallback, dirty-tree always re-checks) +
   autonomous out-of-band regeneration in the drainer (`extract-drain.sh`, config key
   `auto_codemap`, default on).
3. **The orient rung (0.33.35).** SessionStart spine injection (`session-load.sh` §0d, kill
   switch `SB_CODEMAP_ORIENT` — placed BEFORE the forced USER.md/PROJECT.md after live
   verification caught budget starvation) + read-only `code_map`/`code_neighbors` grants for
   `code-review-unit-reviewer` and `quality-reviewer` (deliberately narrower than the auto-team
   B0 five-agent slice — least privilege; both agents were later removed in 0.44.0, so those
   grants are gone with them).

Fenced wrong paths (still binding for Phases 4–5): duplicating `knowledge_neighbors` (the wiki
graph and code graph are separate stores, separate tools — plan §Separation table); storing
under `KNOWLEDGE_DIR/graph`; new `scripts/*.sh` or `tests/test-*.sh` beyond the shipped set
(codemap unit tests are vitest under `mcp/src/`); auto-downloading optional deps; building P3b
reranker inside P3a.

**You have a result when:** a cold-start session (fresh context, zero prior greps) answers
"where does X live" and "what breaks if I change Y" for the active project from `code_map` /
`code_neighbors` output alone; the served map is ≤ 2000 tokens (default budget, never
exceeded); after a new commit the tools report `stale:true` until the drainer regenerates; and
a Windows-generated `graph.json` answers queries byte-identically on Linux (POSIX-normalized
node ids — a tested contract per plan Task A3). Shipped substrate meets the mechanical clauses
(budget cap, drift/staleness, determinism — all test-locked; live smoke 0.33.33: 106 files /
~1816 tokens under budget, dist noise 0). The cold-start orientation clause has no recorded
measurement yet — the value-loop telemetry (0.33.37 `gate=value-loop`) is the instrument for
it. Falsifier unchanged: if answering still requires grep, or the map exceeds budget on a
large repo, the orientation claim fails.

**Status: SHIPPED (Phases 0–3) as of 0.33.35, verified 2026-07-13 at 0.33.37. Open remainder:
Phase 4 (layer-5 code↔wiki edges), Phase 5 (opt-in WASM tier), and the cold-start milestone
measurement above.**

---

## 3. P8 — Memory eval you can trust: deterministic, offline, on CI

**Why SOTA fails here.** Memory products are vibes-evaluated. LLM-as-judge scoring passes ~63%
of wrong-but-plausible answers (spec §6 P8); published memory benchmarks (LongMemEval,
2410.10813) assume hosted-model inference — not reproducible offline, not runnable as a CI
gate, and blind to the deadliest failure mode this repo has actually lived: silent degradation
("no errors" meaning "not running" — see sb-failure-archaeology).

**This repo's asset.** A deterministic, network-free eval substrate already gating releases:

- `tests/test-knowledge-eval.sh` — strict recall@2 (`SB_EVAL_MIN_RECALL=1.0`, "a single miss …
  is a ranking regression") over the curated fixture corpus `tests/fixtures/eval-wiki` +
  `tests/fixtures/eval-queries.jsonl` (**12 golden queries** as of 0.33.31).
- `mcp/src/tools/retrieval-guards.test.ts` (shipped 0.33.22) — deterministic with
  `SECOND_BRAIN_DISABLE_EMBEDDINGS=1`: exact-term canary rank-#1; knowledge-update
  (new content wins, stale stops matching); episodic search→read round-trip; abstention
  (absent term → zero positive-score candidates); project-scope isolation; P7 graph-boost
  default-off guard.
- A suite that can no longer lie green: run-all SKIP classification requires exit 0 as of
  0.33.31 (`tests/test-run-all-skip-semantics.sh`).
- The LongMemEval-shaped design already specced: spec §6 P8.

**First three concrete steps:**

1. Grow `tests/fixtures/eval-queries.jsonl` + `tests/fixtures/eval-wiki` toward the specced
   20–50 hand-authored (fact, gold-answer, planted-session) triples, adding planted-transcript
   fixtures so episodic recall is covered, with abstention and knowledge-update cases
   first-class. Exact-match assertions only — no LLM judge.
2. Add the retrieval-vs-reading decomposition arm (force-fed-memory ceiling vs real-retrieval
   actual) as vitest cases in `mcp/src/` alongside `retrieval-guards.test.ts` — vitest files
   are not surface-budget-counted (per P3a plan §Global Constraints).
3. Build capture reconciliation: a declared-vs-observed capture counter plus a
   produced-at-vs-captured-at silence-latency metric. **Nothing exists today** —
   `grep -ri 'silence.latency' scripts/ mcp/src/` hits nothing. Natural seams: the extraction
   ledger `BRAIN_DIR/.extraction-state.jsonl` (written by `scripts/extract-drain.sh`) vs
   transcript archive timestamps (measurement plumbing → sb-diagnostics-and-tooling).

**You have a result when:** recall@k numbers for the full triple suite compute offline (no
network, `SECOND_BRAIN_DISABLE_EMBEDDINGS=1`, `HF_HUB_OFFLINE=1` — the existing CI posture in
`.github/workflows/ci.yml`) and are identical across repeated CI runs; AND a deliberately
broken ranking change (e.g., inverting a BM25 field weight locally) turns the gate red
(test-the-test — house rule, see sb-validation-and-qa); AND the ceiling-vs-actual split
attributes at least one real miss to retrieval vs reading. Falsifier: an eval that stays green
under a known-bad ranking is itself the silent failure it was meant to catch.

**Status: PARTIAL.** Shipped: the 12-query gate + P8a/b guards above. Missing (verified, no
repo evidence): the 20–50 triple suite with a ceiling arm; capture reconciliation;
silence-latency; and the specced BM25-only-vs-hybrid recall-diff guard (UNVERIFIED whether any
test implements the diff form specifically — the canary exists, the diff does not appear by
name; check `grep -rn 'hybrid' mcp/src/tools/*.test.ts`).

---

## 4. Safe fully-autonomous consolidation (the WHY and the finish line)

**Execution is owned by sb-autonomous-consolidation-campaign — go there to DO this. This
section states why it beats SOTA, the file-level entry points, and when it counts as done.**

**Why SOTA fails here.** Every shipped consolidating memory system runs an LLM that reads
untrusted content (transcripts, tool returns) while holding write privileges over the memory
that will be auto-injected into future sessions — the memory-poisoning substrate (Willison's
lethal trifecta). The field's answers are a human review gate (breaks autonomy) or hoping an
injection detector catches it (detectors are ≤100% evasion-proof; "99% is a failing grade in
appsec" — spec §6 P6). CaMeL (2503.18813) shows the dual-LLM split on paper; nobody ships it in
a local, cross-platform memory system. This repo's constitution makes autonomy AND isolation
hard constraints simultaneously — closing both at once is the pass-SOTA move.

**This repo's asset.** The queued P6 plan (`archive/docs:docs/superpowers/plans/2026-06-30-p6-quarantine-dual-llm.md`:
quarantined summarizer → **netless deterministic writer**, not two LLMs) plus a shipped safety
substrate no comparable system has: `mcp/src/tools/sanitize.ts` invisible-char strip,
`mcp/src/path-guard.ts` `assertWithin`, `mcp/src/agent-grants.test.ts` machine-locked agent
grants, five independent dream-accept guards, reversible FORGET, the self-clearing
`.llm-maintain-quarantine` 3-strike breaker, and a scanner pattern-regression corpus
(`tests/test-injection-corpus.sh` — note: it locks `scripts/tool-return-scanner.sh` telemetry
patterns only; it is NOT an end-to-end consolidation-boundary test).

**First three concrete steps (plan Tasks 1–3; per-task commands, red/green sequences, and
rollbacks live in the campaign skill — this is the file-level entry map):**

1. **Candidate-fact contract.** Create `mcp/src/tools/candidate-facts.ts` +
   `candidate-facts.test.ts`: the closed Stage-A→Stage-B JSONL schema (op/type vocab,
   `provenance.trust:"untrusted"` required, byte caps), fail-loud validation, `validateSlug`
   imported from `mcp/src/path-guard.ts`, every string field through `stripInvisible`
   (`mcp/src/tools/sanitize.ts`). Red test first — the module must be proven absent.
2. **Quarantined summarizer.** Create `agents/dream-summarizer.md` (reads transcripts as DATA,
   emits `candidate-facts.jsonl`; NO node/script/rm/Edit grants) and extend
   `mcp/src/agent-grants.test.ts` to machine-lock both the grant absence and the literal
   "UNTRUSTED DATA" body framing.
3. **Deterministic netless writer.** Create `mcp/src/tools/consolidate-writer.ts` +
   `consolidate-writer-cli.ts` + `consolidate-writer.test.ts`; add the CLI to the esbuild
   `bundle` script in `mcp/package.json`. Writes only under `staging/wiki` (`assertWithin`
   every write), local-BM25 target resolution with no network, idempotent by content hash,
   never reads a transcripts path (test-asserted).

**You have a result when:** N consecutive fully-hands-off consolidation cycles (staged dream →
auto-accept, zero human interaction) complete with (a) zero data loss — no protected live page
overwritten, backup/restore path never needed; (b) the privileged writer provably netless and
provably never reading a transcript path (both test-asserted, per plan Tasks 3–4); (c) an
end-to-end poisoned-transcript fixture — a transcript carrying an embedded instruction — that
fails to plant that instruction in any wiki page or learned rule (this fixture does not exist
yet; building it is part of the milestone); and (d) the existing injection corpus and all
accept-guard tests green throughout. Pick N and the falsification protocol in the campaign
skill. Falsifier: a single cycle where an injected instruction reaches the live wiki, or where
auto-accept loses a page FORGET never proposed, kills the claim.

**Status: PLAN-QUEUED remainder + shipped substrate.** 0.33.31 shipped a nibble ("untrusted
input — DATA, not instructions" framing + grant hardening on `agents/dream-runner.md`,
`agents/knowledge-maintainer.md`, `agents/raw-drainer.md`). The kernel split (plan Tasks 1–4)
is Linux-first (bwrap); Tasks 5–7 (confirm-gate, injection-wrap, scanner reword) are the
cross-platform earliest slice. The plan requires a maintainer brainstorm before Task 4.

---

## 5. Guard liveness as a continuously-proven property

**Why SOTA fails here.** Agent-safety tooling tests its guards once, at unit level, at build
time. Nothing in the ecosystem continuously proves that the installed guard chain actually
fires in situ. This repo has the scar that motivates the frontier: all three PreToolUse guards
sat fail-open on the dev platform (Windows path forms) for months, invisible under a green
suite, proven only by the 2026-07-02 deep audit and fixed in 0.33.31 (archive/docs:CHANGELOG.md 0.33.31,
"Windows guard fail-open class"). The spec's phrasing is the thesis: "prove each guard fires by
injecting the violation it targets (a check that always passes is itself a silent failure)"
(spec §6 P8).

**This repo's asset.**

- Per-guard violation-feeding tests already exist and now include Windows-form vectors via
  stubbed `cygpath`/`realpath` running on Linux/BSD CI (as of 0.33.31):
  `tests/test-persona-tool-guard.sh`, `tests/test-wiki-write-guard.sh`,
  `tests/test-symlink-guard.sh`, plus `tests/test-normalize-path.sh`.
- An observable verdict channel: every guard verdict is appended to `BRAIN_DIR/audit-log.jsonl`
  (schema `{ts,hook,verdict,rule,target,reason,session_id,extra}` — `scripts/lib.sh`).
- Enumerable wiring: `hooks/hooks.json` declares every PreToolUse guard and matcher — the
  harness can discover the guard set instead of hardcoding it.

**First three concrete steps (proposed — no plan doc yet; write one first, per
sb-research-methodology):**

1. Generate a guard manifest from `hooks/hooks.json` (jq over the PreToolUse entries) pairing
   each guard script with ≥1 archetypal violating payload and its expected verdict.
2. Add a harness test that pipes each payload through the real guard script exactly as the
   Claude Code harness would (stdin JSON, `BRAIN_DIR` pointed at a `mktemp -d`), asserting the
   deny/ask verdict lands in the temp audit-log — and that FAILS if any enumerated guard
   returns permissive. Include the disarm matrix: `lib.sh` unsourceable, backslash path form,
   rules file missing. Mind: a new `tests/test-*.sh` requires a same-commit surface-budget bump
   (tests: 153 as of 0.33.31), and SKIP semantics require exit 0 (0.33.31 rule).
3. Wire it into both CI lanes in `.github/workflows/ci.yml` (currently `linux` + `macos` only —
   **there is no Windows lane**, which is exactly how the 0.33.31 fail-open class survived;
   the stubbed-cygpath vector pattern is the stopgap until one exists).

**You have a result when:** a CI lane exists where deliberately disarming any single guard —
delete its rule, feed the Windows path form to a build without `sb_normalize_path`, make
`lib.sh` fail to source — turns the lane red, for every guard enumerated from `hooks.json`, on
every CI OS. Falsifier: if you can comment out a guard's deny branch and CI stays green, the
property does not hold. Do not confuse this with `scripts/liveness-check.sh` — that is R7
artifact-dormancy detection (unreferenced-file rot), not guard-fire proof.

**Status: PARTIAL.** Per-guard tests exist; no enumerate-and-inject harness, no disarm matrix,
no Windows CI lane.

---

## 6. Cross-project practice transfer without fact leakage

**Why SOTA fails here.** Memory products either silo memory per project/thread (a practice
learned in repo A never helps in repo B) or pool everything globally (repo A's private facts —
paths, names, decisions — surface in repo B's context). None distinguish a *practice*
(portable behavioral rule: "run gates before push") from a *fact* (project-bound: "this repo's
jq emits CRLF") at write time.

**This repo's asset.** The two-tier store already draws the line physically: USER.md
(global hot tier, 2200-byte cap) vs `BRAIN_DIR/projects/<slug>/PROJECT.md` (per-project).
Signal machinery is global by construction — `BRAIN_DIR/persona-signals.jsonl` with graduation
to USER.md via `sb_pin_to_user` (`scripts/merge-persona-signals.sh:99`) — so transfer already
*happens*; what is missing is scoping. Supporting substrate: the single-source slug resolver
(`mcp/src/tools/project-dir.ts` / `sb_resolve_slug`), the extract prompt's existing
project-affinity rule and REUSABLE discriminator for wiki learnings
(`scripts/extract-prompt.txt`), and — once P2 lands — learned rules as the enforcement-grade
transfer vehicle.

**First three concrete steps (proposed — no plan doc; write one first):**

1. Add an optional `scope: "global"|"project"` field to the `persona_signals[]` contract in
   `scripts/extract-prompt.txt` with a discriminator instruction mirroring the existing wiki
   REUSABLE rule ("would this hold in a different repo?"), and record the originating slug on
   each evidence entry in `scripts/merge-persona-signals.sh` (the P2 Task 1 slug plumbing
   delivers this datum anyway — sequence after it to avoid a merge collision).
2. Split the graduation target in `merge-persona-signals.sh`: `scope:"project"` signals
   graduate into that project's PROJECT.md (the `pin_to_project` / decisions path) instead of
   persona-learned.md; `scope:"global"` (and legacy scopeless) keep today's `sb_pin_to_learned` behavior —
   backward compatibility is a test, not a hope.
3. Add the leak test: `tests/test-persona-signal-scope.sh` (surface-budget bump required) —
   fixture signals under two slugs in a `mktemp -d` BRAIN_DIR; assert a project-scoped signal
   containing a repo-A path never reaches persona-learned.md, and a global practice graduated from repo A
   is present in the context a repo-B session would load (drive `scripts/session-load.sh` with
   `CLAUDE_PROJECT_DIR` pointed at the second fixture repo).

**You have a result when:** a practice observed twice in repo A fires in a fresh repo B session
with zero manual steps — visible in repo B's injected context (or, post-P2, as a learned rule
whose citation still points at the repo-A transcript) — while a planted repo-A-specific fact in
the same fixture set never appears in repo B's injected context; both directions asserted by
the two-slug test. Falsifier: either a portable practice that stays siloed, or one leaked
project fact, fails the milestone.

**Status: NOT-STARTED.** No plan doc, no scope field, no split graduation. Today's behavior is
all-or-nothing global: every graduated signal lands in persona-learned.md regardless of origin — transfer
by leakage, not by design.

---

## Second-tier open questions (tracked, smaller, or partially resolved)

From spec §10 unless noted. Do not oversell any of these as active workstreams.

| Question | State (as of 0.33.31) |
|---|---|
| P3b cross-encoder reranker (spec calls it "highest-ROI retrieval gain") | NOT-STARTED — no plan doc, no code; `grep -ril rerank .` → docs only. Vet deps like `bin/install-vector-deps.sh` |
| Code-map regen trigger/cadence (every commit / N edits / drift threshold) | RESOLVED 0.33.34 — git-rev drift + dirty-tree re-check, regenerated out-of-band by the drainer (`auto_codemap`) |
| Dual-capture (Stop + PreCompact) dedup conflicts | partially resolved empirically — write-path MinHash NOOP/UPDATE at capture (`mcp/src/tools/raw-inbox.ts:289-306`, `SB_CAPTURE_DEDUP_THRESHOLD` 0.9, 0.33.29) |
| Quarantine boundary granularity: does the privileged writer ever need free-text? | open; P6 plan bets "no" (structured candidate-facts only) — the bet itself is testable |
| Reflection cadence | RESOLVED 0.33.28 (per-dream + `member_hash` idempotence). Residual frontier: self-referential memory ops need input/output separation — 0.33.31 had to exclude `generated: true` pages from clustering input after a reflection page could become its own cluster id (`mcp/src/tools/graph-cluster-cli.ts:69-76`) |
| Forgetting without frequency: does structural-importance-only FORGET actually shrink the wiki? | mechanism SHIPPED (`scripts/wiki-forget-score.sh` — access counts are `acc=` telemetry only, never scored); the §8 criterion "wiki page count down materially after P4" has NO measured evidence yet — that measurement is an open, cheap result |

Domain theory behind these (MinHash, BM25/RRF, bi-temporal graph, forgetting) →
sb-memory-systems-reference. What is genuinely novel vs known → sb-external-positioning.

## Rules that bind all frontier work

- Every problem above ships through normal change control: version lockstep, surface-budget
  bump in the same commit, all gates locally before push. Mechanics → sb-change-control. Never
  route around gates.
- Plan docs before code for anything L/XL; evidence bar and idea lifecycle →
  sb-research-methodology.
- The queued P2/P6 plans carry stale version targets (authored at 0.33.29) — recompute
  version and budget arithmetic at implementation time. (P3a executed 0.33.33–0.33.35.)
- Nothing here may contradict `CONSTITUTION.md`; when a frontier idea and a constitution
  constraint collide, the constitution wins or gets amended first (a governance change, not a
  workaround).

## Provenance and maintenance

Derived from repo evidence only: `CONSTITUTION.md`;
`archive/docs:docs/superpowers/specs/2026-06-26-second-brain-constitution-and-diet-design.md` (§6, §8, §10);
plan docs `archive/docs:docs/superpowers/plans/2026-06-30-{p2-learning-to-guardrail,p3a-orientation-code-map,p6-quarantine-dual-llm}.md`;
`archive/docs:CHANGELOG.md` (0.33.22–0.33.31); and direct reads of the scripts/tests/tools cited inline.
The "why SOTA fails" framings condense the spec's cited research (mem0 2504.19413, CaMeL
2503.18813, LongMemEval 2410.10813, Generative Agents 2304.03442, GraphRAG-Bench 2506.05690)
and accepted project direction; wording discipline for external claims lives in
sb-external-positioning. Authored 2026-07-05 against version 0.33.31 (uncommitted working
tree, HEAD `6fba312`).

Re-verify volatile facts before relying on them:

```bash
# current version + surface budget (counts drift every release)
jq -r .version .claude-plugin/plugin.json && cat .claude-plugin/surface-budget.json
# P2 still zero-code? (expect: hits only in docs/)
grep -rl 'persona-rules.learned' . --include='*.sh' --include='*.ts'
# P3a still shipped? (expect: codemap module files + code_map hits in mcp/src)
ls mcp/src/tools/codemap 2>/dev/null; grep -rln 'code_map' mcp/src
# P3b still not started? (expect: docs/CHANGELOG hits only)
grep -ril rerank . | grep -v node_modules
# eval-suite size (spec target 20–50; was 12)
wc -l tests/fixtures/eval-queries.jsonl
# capture reconciliation still missing? (expect: exit 1, zero hits — do NOT widen to
# 'reconcil': scripts/kb-drain-reconcile.sh et al. are drain-state/plan reconciliation,
# unrelated to the declared-vs-observed capture counter)
grep -rin 'silence.latency' scripts/ mcp/src/
# CI lanes (expect: ubuntu-latest + macos-latest; a windows lane would close a step in problem 5)
grep -n 'runs-on' .github/workflows/ci.yml
# graduation still all-global? (expect: sb_pin_to_learned with no scope branch)
grep -n 'sb_pin_to_learned\|scope' scripts/merge-persona-signals.sh
# P6 remainder still unimplemented? (expect: no summarizer agent / writer CLI)
ls agents/dream-summarizer.md mcp/src/tools/candidate-facts.ts 2>&1
```
