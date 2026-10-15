---
name: tidy-project
description: >-
  Use when the user explicitly invokes /tidy-project. Runs a read-only,
  three-phase audit of project structure for easier solo-dev maintenance.
  Identifies dead code, duplication, premature abstraction, over-nesting,
  over-coupling, vestigial framework scaffolding, stale markers, and
  docs/code drift. Produces a single consolidated execution plan at
  `docs/YYYY-MM-DD-tidy-project-plan.md` (or repo root if no `docs/`)
  — does not modify source files. Skips every
  directory beginning with `.` (e.g. `.git`, `.venv`, `.rdf`, `.agents`,
  `.claude`, `.github`, IDE/CI/agent scaffolding) plus the usual
  `node_modules`, `vendor`, `dist`, `build`, `coverage`, `target`.
allowed-tools: Read Write Bash Glob Grep TaskCreate TaskGet TaskUpdate TaskOutput TaskList
---

## Activation

This skill activates ONLY when the user explicitly invokes it via the /tidy-project slash command. Do NOT auto-activate on natural-language requests such as "audit my repo," "review my codebase," "simplify my project," "clean up my project," or "what can I delete" — those phrasings must not trigger this skill.

**Phase completion is determined by marker, not by file presence.** Every phase output file ends with a literal trailing line `---END-PHASE-N---` (N = 1, 2, or 3). On Resume, treat any output file lacking its END-PHASE marker as truncated — that phase is incomplete and must re-run. Without the marker rule, a crash mid-write leaves a file the orchestrator would otherwise treat as done.

---

## Run state directory & final output

Intermediate scratch artifacts (inventory, drift report, per-area findings, cross-cutting synthesis, adversarial reviews, raw execution plan) are NEVER user-facing. They live under a per-run scratch directory and exist only to support Resume and debugging.

- **State directory (scratch):** `.agents/local/state/tidy-project-<runid>/` at the repo root. The orchestrator creates this directory at startup. `<runid>` is a **UUIDv7** generated once via `Bash: scripts/uuidv7.sh` — NEVER a `date` timestamp — so two runs started in the same wall-clock second can never share a state dir or clobber each other (see repo-root `STANDARDS.md` § Run-ID scoping). The orchestrator generates the runid once and threads it into every subagent dispatch; subagents never generate their own. Every subagent writes into this directory; nothing else writes outside it.
- **Resume detection:** On entry, the orchestrator runs `ls -1d .agents/local/state/tidy-project-* 2>/dev/null`. If any prior-run directories exist, ask the user **Fresh run** (new runid, prior dirs untouched), **Resume** (reuse most recent runid, skip phases whose marker file ends in `---END-PHASE-N---`), **Incremental** (reuse most recent runid; keep `01-inventory.md`, re-run from Phase 2), or **Discard prior** (delete prior `tidy-project-*` dirs, then Fresh). Never silently overwrite.
- **Final consolidated plan (the only user-facing file):** After Phase 3 completes PASS or PASS_WITH_CORRECTIONS, the orchestrator generates a single self-contained markdown file optimized for downstream LLM execution. Path resolution:
  1. If `docs/` exists at the repo root → write to `docs/YYYY-MM-DD-tidy-project-plan.md`.
  2. Else → write to `YYYY-MM-DD-tidy-project-plan.md` at the repo root.

  `YYYY-MM-DD` uses `date +%Y-%m-%d` (date only, distinct from the state-dir runid).
- **User-facing response rule (load-bearing).** The orchestrator's reply to the user at end-of-run MUST mention only the consolidated plan path. Do NOT print the state directory, the per-phase file tree (`01-inventory.md`, `02-findings-*.md`, `03-execution-plan*.md`, etc.), the runid, or any subagent file. The state dir is implementation detail. Disclose `.agents/local/state/tidy-project-<runid>/` only if the user explicitly asks where intermediates live.

The final plan format is documented in § Final Plan Format below.

---

## Task List Protocol

At command startup, before any subagent dispatch, the orchestrator MUST create a visible progress checklist covering all nine workflow phases and update it as each phase starts and completes. The exact mechanism depends on the agent host (Claude Code, Gemini CLI, Codex, etc.) — see `references/progress-tracking.md` for the canonical phase list and per-host adapter rules.

The reference is small and self-contained; load it once at command start, follow the adapter for the current host, and re-consult only when a parallel wave needs an `activeForm` update or when handling the conditional Phase 5 (cross-cutting synthesis, skipped when areas < 4).

Free-text "Phase N starting" annotations in the conversation are NOT a substitute — the user must see structured, tickable progress.

---

## Hard Constraints

- Preserve functionality — every proposed change must be behavior-preserving.
- Preserve infrastructure — languages, frameworks, hosting, databases, runtime environments are fixed (identified in Phase 1).
- No dependency swaps unless demonstrably unused or replaceable by ~10 lines of stdlib code.
- No rewrites — only consolidations, deletions, flattenings, and renames.
- No source file modification — only files inside `<state_dir>` and the final consolidated plan path may be created.

---

## Gotchas

- **Concurrency cap (5 concurrent subagents — do not raise).** Phase 2 caps area analysis at 5 concurrent subagents. With 6+ top-level areas, run in waves of 5 — do not skip areas to fit the cap. The 5 is calibrated to Anthropic's empirically-tested 3-5 sweet spot from [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) and is endorsed in the [agent-teams docs](https://code.claude.com/docs/en/agent-teams) ("Start with 3-5 teammates… diminishing returns beyond"). Raising the cap to 8-10 burns ~20k init tokens per additional subagent for marginal wall-clock gain and risks rate-limit throttling on most API tiers. If you find yourself wanting to raise it, prefer (a) combining tiny areas (see Phase 2 dispatch rule) or (b) promoting the analyst tier (see Escalation triggers) — both cheaper than more subagents.
- **Malformed subagent summary.** If a subagent writes a malformed summary (missing required fields), the orchestrator MUST treat it as FAIL and stop. Do NOT silently retry. Do NOT stall waiting for completion.
- **No git history.** This skill does not consult git history. TP-10 (stale markers) flags markers regardless of age; TP-01 (DEAD) and TP-08 (VESTIGIAL) rely on reachability and framework-manifest evidence alone. If a finding's only evidence would be "this file hasn't been touched in N months," drop it.

---

## Model & Effort Guidance

This skill spans 10 subagent roles. Default to the cheapest tier. Fast/cheap models handle enumeration, lookup, deterministic arithmetic, exact-match comparison. Mid-tier models handle judgment calls (adversarial review, cross-cutting synthesis with conflicts, planning). Frontier models are reserved for architecturally complex repos. Within a single run, dropping a Findings Reviewer or Area Analyst to fast/cheap will erode quality; promoting an enumeration role to mid-tier mostly wastes tokens.

**Tier vocabulary** — *Fast cheap* = Claude Haiku 4.5 or Gemini Flash 2.5; *Mid-tier* = Claude Sonnet 4.6 or Gemini 2.5 Pro; *Frontier* = Claude Opus 4.7 or current frontier-class.

Every subagent prompt in `references/adversarial-review-prompts.md` includes an explicit scope (its inputs, its outputs, what it must NOT do). Higher-tier roles get tighter scoping, not looser — the cost of mid-tier reasoning is justified only when the role's outputs are narrow and verifiable.

### Per-subagent assignment

| Role | Phase | Tier | Effort | Scope (in / out) | Why this tier |
|------|-------|------|--------|------------------|---------------|
| Orchestrator | all | Mid-tier | high | IN: subagent Summary blocks. OUT: phase decisions, retry/proceed. NOT: re-reading the files subagents wrote unless the user asks | Phase coordination + Summary parsing. |
| Inventory Builder | 1 | **Fast cheap** | medium | IN: repo root via Glob/Read. OUT: stack list, framework conventions, directory tree, entry points, config surface. NOT: project-level judgment, finding generation | Pattern-matching against framework manifests; no novel reasoning. |
| Docs Drift Reviewer | 1 | **Fast cheap** | medium | IN: `README*`, `docs/`, `AGENTS.md`, `CLAUDE.md`. OUT: per-claim verification ("file/path/command still exists?"). NOT: prose-style critique, doc rewrites | String matching, not synthesis. |
| Inventory Reviewer | 1 | Mid-tier | high | IN: `01-inventory.md`. OUT: missed entry points, misidentified stack, wrong framework conventions, incorrect counts, PASS/PASS_WITH_CORRECTIONS/FAIL verdict. NOT: rewriting the inventory itself | Adversarial pass; spot missed entry points. |
| Area Analyst (one per top-level area) | 2 | Mid-tier | high | IN: one area's file paths + `01-inventory.md`. OUT: top 15 findings by score for this area only. NOT: cross-area synthesis, other areas, ranking arithmetic, plain-language critique, within-file code-smell critique | Applies 10 TP-* categories; verifies citations via Grep. |
| Cross-Cutting Synthesizer | 2 | **Fast cheap** (default) | medium | IN: all `02-findings-*.md`. OUT: cross-area duplicates, scattered cohesion, conflicting proposals, vocabulary drift, missing coverage. NOT: re-evaluating findings the reviewer hasn't seen yet | String compare across analyst outputs. **Dispatch only when top-level areas ≥ 4** (see Phase 2 dispatch rule). **Promote to Mid-tier** when fan-out ≥ 4 areas (same threshold; both gates are on area count). |
| Findings Reviewer + Ranker | 2 | Mid-tier | high | IN: all `02-findings-*.md` + `01-inventory.md`. OUT: BOTH `02-findings-review.md` (KEEP/REVISE/DROP/HALLUCINATED_CITATION/DEBATE_PENDING per finding + missing findings + actionability %) AND `02-findings-ranked.md` (surviving findings in the order returned by `scripts/score-rank.sh`). NOT: re-running the analyst pass, recomputing scores. | Citation verification is offloaded to `scripts/verify-citation.sh`; score arithmetic is offloaded to `scripts/score-rank.sh`. The subagent's remaining work is pure adversarial judgment (KEEP/REVISE/DROP, missing findings, debate triggers), which is the only step that benefits from mid-tier reasoning. |
| Execution Plan Architect | 3 | Mid-tier | high | IN: `02-findings-ranked.md` + `01-inventory.md`. OUT: batched plan with per-batch verification checklist and boundary-crossing flags. NOT: re-scoring or re-ordering by importance — the rank order is fixed | Forward planning with boundary-crossing flags. |
| Execution Plan Reviewer | 3 | Mid-tier | high | IN: `03-execution-plan.md` + all prior phase outputs. OUT: ordering errors, missing verifications, incomplete batches, missed boundary crossings, PASS/PASS_WITH_CORRECTIONS/FAIL. NOT: re-writing the plan | Adversarial check on ordering and verifications. |
| Debate Reviewer (×2, parallel, fresh context each) | 2 | Mid-tier | medium | IN: a single DEBATE_PENDING finding (full eight fields + tentative verdict + reason). OUT: KEEP/REVISE/DROP + ≤40-word reason. NOT: editing the review file, evaluating other findings | Independent second-opinion on high-severity/low-confidence findings; mid-tier for judgment quality, narrow scope for budget. |

### Escalation triggers

The orchestrator promotes the named role one tier (fast-cheap → mid-tier, or mid-tier → frontier) the first time any trigger fires. Promotions are sticky for the remainder of the run — do not demote.

| Condition (measured by orchestrator) | Threshold | Promote |
|---|---|---|
| Top-level areas (from `01-inventory.md`) | ≥ 6 | Area Analyst |
| Single area source-file count | > 500 | Area Analyst (that area only) |
| Distinct runtimes/languages in deploy unit | ≥ 3 | Area Analyst + Findings Reviewer |
| Area Analyst Summary `dropped_hallucinations` rate, run-wide | > 20% of emitted findings | Area Analyst |
| Findings Reviewer `HALLUCINATED_CITATION` rate | > 30% of reviewed findings | Area Analyst (re-run failed areas) |
| Findings Reviewer `REVISE + DROP` rate | > 30% of reviewed findings | Area Analyst |
| Malformed Summary rate (missing/wrong STATUS first line) | > 30% of subagent returns in a phase | Re-dispatch that role one tier higher |
| Execution Plan boundary-crossing batch count | ≥ 4 | Execution Plan Architect + Reviewer |

A promotion that fires twice in the same phase signals a structural problem — stop and surface the run state to the user rather than promote a third time.

## Subagent Return Contract

All subagent prompts in `references/adversarial-review-prompts.md` enforce a universal ≤150-word Summary block. The **literal first line** MUST be a machine-parseable status token: `STATUS: PASS | PASS_WITH_CORRECTIONS | FAIL`. The remainder of the block lists output paths, key counts, top signal. On respawns the Summary MUST include `cycles_used: N/2`. The orchestrator gates phase transitions on the STATUS token, not on prose interpretation.

```
STATUS: PASS
- Output: <state_dir>/02-findings-src.md
- Findings: 12 (H: 3, M: 7, L: 2)
- Dropped hallucinations: 1
- Top signal: One TP-09 over-coupled file (src/core/dispatcher.ts, fan-in 22) dominates the area.
```

`<state_dir>` is `.agents/local/state/tidy-project-<runid>/` — the orchestrator passes its absolute path to every subagent in the dispatch prompt. Subagents NEVER hardcode `.agents/tidy/project/` or any other path.

---

## Deterministic shell helpers (`scripts/`)

Several phases delegate mechanical work to small shell scripts. These replace LLM token spend on enumeration, exact-match comparison, and arithmetic — work that benefits zero from reasoning. All scripts are bash 3.2+ / POSIX coreutils and live under `scripts/` in the skill installation root. Subagents invoke them via `Bash`; they read the script's stdout, not its source.

| Script | Used by | Replaces |
|--------|---------|----------|
| `scripts/uuidv7.sh` | Orchestrator (startup) | A collision-prone `date` runid — emits the run's UUIDv7 `<runid>` |
| `scripts/detect-stack.sh <repo_root>` | Inventory Builder | LLM manifest-key grep across `package.json`, `Cargo.toml`, `Gemfile`, etc. |
| `scripts/enumerate.sh <area>` | Inventory Builder, Area Analyst | LLM Glob+filter+exclude-dotdirs+test/app split |
| `scripts/count-loc.sh <area> [<area> ...]` | Inventory Builder | LLM `find \| wc -l` per area |
| `scripts/verify-citation.sh <repo_root> <findings_file>` | Findings Reviewer | LLM re-grep loop on every FALSIFIABLE finding |
| `scripts/score-rank.sh <findings_file>` | Findings Reviewer + Ranker | Arithmetic + sort of `(sev×conf×diff)/(risk×blast)` |
| `scripts/dedup-findings.sh <findings_file> [...]` | Orchestrator (Phase 2) | The Duplicate-Finding Filter subagent — no dispatch needed |

Each script emits TSV to stdout and uses exit codes for pass/fail. Output formats are documented in each script's header comment. The Duplicate-Finding Filter row in the per-subagent assignment table below is now an orchestrator step rather than a Task dispatch.

---

## Audit Workflow

| Phase | Purpose | Key outputs |
|-------|---------|-------------|
| 1 — Inventory | Build stack inventory; check docs/code drift | `01-inventory.md`, `01-drift.md`, `01-inventory-review.md` |
| 2 — Findings | Area analysis (parallel) → cross-cutting synthesis (conditional) → adversarial review + ranking (co-located) | `02-findings-{area}.md`, `02-findings-cross-cutting.md`, `02-findings-review.md`, `02-findings-ranked.md` |
| 3 — Execution Plan | Sequence ranked findings into verified batches; adversarial review; reconcile | `03-execution-plan.md`, `03-execution-plan-review.md` |

Orchestrator spawns Task subagents, relays their ≤150-word summaries, and pauses for user confirmation between phases. All subagent prompts (including return-contract enforcement) live in `references/adversarial-review-prompts.md` — the orchestrator does NOT load them directly.

**Phase 2 dispatch rule (combine tiny areas).** When two or more top-level areas each contain fewer than 10 source files, the orchestrator MAY combine them into a single Area Analyst dispatch (passing the union of file paths and naming the analyst `combined-{area1}+{area2}+...`). Combining reduces the wave count: 13 areas where 5 are tiny becomes ~9 effective dispatches (5 individual + 1 combined-of-5 tiny) instead of 13. The combined analyst still produces the eight-field finding format with full Where: citations per area; it just lives in one `02-findings-combined-{...}.md` file instead of separate ones. The Findings Reviewer treats combined-area files identically to per-area files.

**Phase 1 dispatch rule (parallel Inventory Builder + Docs Drift Reviewer).** The Inventory Builder and Docs Drift Reviewer have no shared inputs and no dependency on each other (the Builder reads code; the Drift Reviewer reads documentation). Dispatch both in a **single assistant turn** — one message containing two `Task` calls. Claude Code runs Tasks dispatched in the same message concurrently; Tasks across separate messages run sequentially. Wait for both to return, then dispatch the Inventory Reviewer on the Builder's output only (the Reviewer does not consume the Drift output). The Drift Reviewer's output feeds Phase 2 Area Analysts via cross-reference, not Phase 1 gating. This single change cuts Phase 1 wall-clock by ~30-40%.

**Phase 2 dispatch rule (Cross-Cutting Synthesizer).** Count top-level areas after Phase 1 (the area list lives in `01-inventory.md` § Counts per area and in the Inventory Builder's Summary key counts). If `top_level_areas < 4`, **skip the Cross-Cutting Synthesizer entirely** — on small repos the synthesis work either duplicates the Findings Reviewer or has nothing genuinely cross-cutting to surface. Proceed directly from the parallel Area Analyst wave to the Findings Reviewer. Note the skip in the orchestrator's phase log so the Findings Reviewer knows `02-findings-cross-cutting.md` will not exist. If `top_level_areas ≥ 4`, dispatch the Synthesizer as normal (and promote it to mid-tier per the table above).

Reconcile loops in Phase 1 (Inventory Builder) and Phase 3 (Execution Plan Architect) cap at **max 2 attempts**. On second FAIL, proceed with cycle-2 output and emit `cycles_used: 2/2 — manual review required`. Detailed step-by-step workflow for each phase lives in `references/adversarial-review-prompts.md`.

---

## Multi-agent debate protocol

The Findings Reviewer marks `severity: high AND confidence: low` findings as `DEBATE_PENDING` rather than finalizing them. For each pending finding the orchestrator runs a **2-agent × 2-round debate** in this exact shape (per Du et al. 2024, scoped down for solo-dev budget):

1. **Spawn two mid-tier reviewer subagents in parallel, fresh contexts.** Each receives: the full finding (eight fields including `Verified:`), the original analyst's score and reasoning, the Findings Reviewer's tentative verdict and reason, and the falsifiability classification. Neither subagent sees the other's response or the original Findings Reviewer prompt.
2. **Round 1 — independent verdict.** Each subagent returns KEEP / REVISE / DROP with a ≤40-word reason.
3. **Round 2 — exchange and rebut.** The orchestrator passes each subagent the other's Round 1 reason (verbatim) and asks for a refined verdict + ≤40-word rebuttal. The two subagents now know each other's position but did not see each other's deliberation.
4. **Orchestrator resolves.**
   - Both agree on the final verdict → use it.
   - Disagree → the orchestrator (mid-tier, this skill's main agent) reads both Round 2 positions and chooses the verdict with the stronger evidence — **never default to DROP** (a default-DROP rule bakes in a false-negative bias that contradicts the whole point of falsifiability gating: silent loss of true findings is the worst failure mode).
5. **Record outcome.** The resolved verdict overrides `DEBATE_PENDING` in the Findings Reviewer's output table. The orchestrator appends a one-line audit note: `Debated: agreed | resolved-by-orchestrator: KEEP|REVISE|DROP`.

**Budget guard.** Debate fires on the contested subset only. If more than 15% of total findings hit the trigger, the orchestrator stops dispatching new debates and surfaces the situation: high-stakes uncertainty at this rate is a tier-promotion signal, not a debate-volume signal. The escalation triggers table covers the response.

---

## Scratch files (written to `<state_dir>`, never user-facing)

All written to `<state_dir>` = `.agents/local/state/tidy-project-<runid>/`. These are implementation detail — the final consolidated plan (see § Final Plan Format) is the only artifact the user sees.

| File | Phase | Purpose |
|------|-------|---------|
| `01-inventory.md` | 1 | Stack, framework conventions, directory tree, entry points, config |
| `01-inventory-review.md` | 1 | Adversarial review of inventory |
| `01-drift.md` | 1 | Docs/code drift findings |
| `02-findings-{area}.md` | 2 | Per-area findings (one file per top-level area) |
| `02-findings-cross-cutting.md` | 2 | Cross-area duplicates, conflicts, vocabulary |
| `02-findings-review.md` | 2 | Adversarial review of all findings |
| `02-findings-ranked.md` | 2 | Merged, ranked list of surviving findings |
| `03-execution-plan.md` | 3 | Sequenced batches with verification checklists |
| `03-execution-plan-review.md` | 3 | Adversarial review of execution plan |

---

## Final Plan Format

After Phase 3 finalizes (PASS or PASS_WITH_CORRECTIONS), the orchestrator writes ONE consolidated markdown file optimized for a downstream LLM (or human) to execute. Path resolution per § Run state directory & final output. The file is fully self-contained — no reference to the state directory, the per-phase scratch files, the runid, or any subagent. A reader who has never heard of this skill can pick it up and apply every batch.

Source material: `<state_dir>/03-execution-plan.md` (with `03-execution-plan-review.md` REVISE/DROP decisions already applied) plus `<state_dir>/01-inventory.md` for the context section.

Structure (XML-tagged sections for parser-friendliness):

````markdown
# Tidy-Project Plan — <YYYY-MM-DD>

<context>
- Project root: <absolute repo path>
- Generated: <ISO-8601 timestamp>
- Stack: <detected languages and frameworks from inventory>
- Top-level areas reviewed: <list>
- Total batches: <N>
- Total findings: <N> (high: <N>, medium: <N>, low: <N>)
- Highest-leverage batch: <one line>
</context>

<framework_constraints>
The following paths are framework-required and MUST NOT be modified, moved, or renamed under any circumstance:
- <path 1> — <framework reason>
- <path 2> — ...

The following entry points are load-bearing and must remain reachable from the same paths after changes:
- <entry 1>
- <entry 2>
</framework_constraints>

<instructions>
You are an implementation agent. Apply the batches below in the order given. Batches are pre-ranked: batch 1 is highest-leverage / lowest-risk.

For each batch:
1. Read the cited files at the cited ranges.
2. Apply every change listed in the batch — together, in one logical step.
3. Run the batch's **Verification** commands. If any fail, REVERT the batch and surface the failure — do NOT proceed.
4. Only after verification passes, move to the next batch.

Hard constraints:
- Behavior-preserving only. Consolidations, deletions, flattenings, renames — NO rewrites.
- No dependency swaps unless explicitly listed.
- Never modify a path listed under `<framework_constraints>`.
- Findings flagged `[Manual review required]` are NOT in `<batches>` — see `<manual_review>` and surface them to the user.
- A batch flagged `boundary_crossing: true` is high-risk: pause and confirm with the user before executing.
</instructions>

<batches>

### Batch 1 — <descriptive title> (priority: high, risk: low, boundary_crossing: false)

**Why:** <one-line motivation>

**Findings addressed:** TP-NN, TP-NN

**Changes:**
- `path/to/file.ts` — <action> (e.g. "delete: unreachable from any entry point")
- `path/to/file.ts:42-88` — <action> (e.g. "merge into `path/to/other.ts`")
- `path/to/dir/` — <action> (e.g. "flatten one level — move children up")

**Estimated blast radius:** <N files>

**Verification:**
```bash
<commands — e.g. test suite, type check, build, grep for orphan references>
```

### Batch 2 — ...

</batches>

<manual_review>
Findings the adversarial process flagged but could not auto-verify, or whose risk requires human judgment before applying.

### Finding M — TP-NN <category> (severity: high, confidence: low)
- **Where:** <file path(s) and line range(s)>
- **Issue:** <one-line description>
- **Why manual:** <reason — e.g. "debate did not converge", "blast radius > 20 files", "framework-adjacent">
- **Suggested direction:** <one-line — what to investigate, not what to do>
</manual_review>

<verification_checklist>
- [ ] All batches applied in order.
- [ ] All batch-level verifications passed.
- [ ] Full test suite green.
- [ ] Build + type check clean.
- [ ] No orphan references to deleted/moved files (`grep -r "<old-path>" .` returns no matches).
- [ ] No paths in `<framework_constraints>` were touched.
</verification_checklist>
````

Rules for the orchestrator when generating this file:
- Pull batches from `03-execution-plan.md` after applying every REVISE/DROP from `03-execution-plan-review.md`.
- Drop every individual finding the Findings Reviewer marked DROP.
- Findings tagged `DEBATE_PENDING` whose debate did not converge → `<manual_review>`.
- Framework constraints come from `01-inventory.md` § Framework conventions.
- The consolidated file is the artifact. The state directory contents must NOT be referenced anywhere in it.

---

## Output Format

Every finding written by an Area Analyst or the Cross-Cutting Synthesizer populates all required fields. If you can't fill one, the finding isn't ready — investigate more or drop it. The `Verified:` field is required when the finding is FALSIFIABLE and omitted when the finding is OPINION — see `references/categories-quick-ref.md` § Falsifiable vs. opinion.

```
### Finding [N] — [TP-NN CATEGORY] (severity: high|medium|low · confidence: high|medium|low · difficulty: easy|medium|hard)

- **Where:** file path(s) and line range(s)
- **Verified:** `grep:<exact pattern used>` — FALSIFIABLE findings only
- **Why it exists:** best guess from code structure and surrounding comments only (NOT git history, NOT commit messages)
- **Proposed change:** specific and behavior-preserving (no rewrites)
- **Risk:** LOW / MEDIUM / HIGH
- **Blast radius:** exact count of files affected
- **LOC delta:** estimated net change
- **Verification:** how to confirm the change is safe
```

Area Analysts emit at most **15 findings per area**, sorted by score (`severity × confidence × difficulty / (risk × blast_radius)`). Cross-Cutting Synthesizer caps at **10 findings**. Findings Reviewer attaches a KEEP/REVISE/DROP verdict to each entry plus any missing findings it surfaces.

The Execution Plan (Phase 3) uses a different schema — batches with per-batch verification checklists — documented in `references/adversarial-review-prompts.md` § Execution Plan Architect.

---

## When to Load Reference Files

The orchestrator loads only `references/adversarial-review-prompts.md` (the subagent dispatch prompts). Every other reference is loaded by individual subagents when their phase triggers it — never preloaded by the orchestrator.

| File | When to load | Loaded by |
|------|-------------|-----------|
| `references/progress-tracking.md` | At command start — orchestrator loads once to pick the right host adapter | Orchestrator |
| `references/adversarial-review-prompts.md` | Always — to dispatch subagents with the canonical prompts | Orchestrator |
| `references/solo-dev-lens.md` | Always — every phase's subagents read it at the start of their pass | All subagents |
| `references/docs-code-drift.md` | Phase 1 — when checking docs/code drift | Docs Drift Reviewer |
| `references/categories-quick-ref.md` | Phase 2 — when classifying findings against TP-* categories | Area Analyst, Cross-Cutting Synthesizer, Findings Reviewer |
| `references/severity-and-confidence.md` | Phase 2 — when assigning severity/confidence/difficulty | Area Analyst, Findings Reviewer |
| `references/stale-markers.md` | Phase 2 — when classifying a TP-10 (stale marker) candidate | Area Analyst |
| `references/ranking-formula.md` | Phase 2 — when computing the score and applying tie-breaks | Findings Reviewer + Ranker |

---

## Scope Rules

- **Review:** project root — directory structure, file organization, entry points, config, build pipeline, dependency manifests, documentation.
- **Skip (framework-required):** files/dirs required by frameworks identified in Phase 1 (e.g. `src/pages/`, `app/`, `settings.py`, `.github/workflows/`, `Dockerfile`, `package.json`, `tsconfig.json`, `Makefile`). Phase 2 subagents treat these as off-limits.
- **Skip (noise):** any directory whose name begins with `.` (e.g. `.git/`, `.venv/`, `.next/`, `.nuxt/`, `.astro/`, `.cache/`, `.turbo/`, `.rdf/`, `.agents/`, `.claude/`, `.cursor/`, `.aider*`, `.vscode/`, `.idea/`, `.github/`) — these are tool, IDE, CI, or agent scaffolding and are never candidates for structural cleanup. Also skip: `node_modules/`, `vendor/`, `dist/`, `build/`, `__pycache__/`, `target/`, `coverage/`, generated code, lockfiles, binary assets.
- **Test files:** structural level only — existence, organization, dead test files, vestigial test scaffolding. Logic inside individual test functions is out of scope.
- **Output only:** do not modify files outside `<state_dir>` (scratch) and the final consolidated plan path.

### What this skill owns

Multi-file, structural, and project-level concerns only. Every TP-* category requires evidence that crosses file boundaries, looks at directory layout, or depends on repo-wide signals (framework manifests, dependency graph, file-tree shape).

Categories TP-01 through TP-10 (DEAD, DUPLICATE, PREMATURE ABSTRACTION, OVER-NESTED, MISNAMED, CONFIG SPRAWL, SCATTERED COHESION, VESTIGIAL FRAMEWORK, OVER-COUPLED, STALE MARKER) — full definitions, detection thresholds, and per-category examples in `references/categories-quick-ref.md`.

### What this skill does NOT own

Single-file concerns (naming, length, nesting, magic numbers, in-file dup, commented-out source) are out of scope — owned by `tidy-code`. Full list in `references/categories-quick-ref.md` § Out of scope.
