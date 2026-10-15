---
name: tidy-code
description: >-
  Invoked by /tidy-code. Reviews source code for structural quality violations
  (hidden dependencies, god functions, silent failures, deep nesting) across
  any language. Produces a read-only findings report with concrete refactoring
  suggestions. Skips every directory beginning with `.` (e.g. `.git`, `.venv`,
  `.rdf`, `.agents`, `.claude`, IDE/agent scaffolding) plus the usual
  `node_modules`, `vendor`, `dist`, `build`, `coverage`, `target`.
allowed-tools: Read Write Bash Glob Grep TaskCreate TaskGet TaskUpdate TaskOutput TaskList
---

## Activation

This skill activates **only** when the user explicitly invokes it via the `/tidy-code` slash command. Do NOT auto-activate on natural-language requests such as "review my code," "audit the code," "clean this up," "find code smells," "make this more maintainable," or "reduce complexity" — those phrasings must not trigger this skill.

---

## Hard Constraints

- MUST NOT modify source files. The only writable paths are under `<state_dir>` (the per-run scratch directory — see § Run state directory) and the final consolidated plan path (see § Final Plan Format).
- MUST NOT auto-activate without `/tidy-code`.
- MUST NOT retry the adversarial review more than once (depth=1).
- MUST NOT re-run the file-review pass from inside the reviewer subagent.

---

## Run state directory & final output

Intermediate scratch artifacts (per-wave findings, dedup output, review verdict) are NEVER user-facing. They live under a per-run scratch directory and exist only to support Resume and debugging.

- **State directory (scratch):** `.agents/local/state/tidy-code-<runid>/` at the repo root. The orchestrator creates this directory at startup. `<runid>` is a **UUIDv7** generated once via `Bash: scripts/uuidv7.sh` — NEVER a `date` timestamp — so two runs started in the same wall-clock second can never share a state dir or clobber each other (see repo-root `STANDARDS.md` § Run-ID scoping). The orchestrator generates the runid once and threads it into every subagent dispatch; subagents never generate their own. Every subagent writes into this directory; nothing else writes outside it.
- **Resume detection:** On entry, the orchestrator runs `ls -1d .agents/local/state/tidy-code-* 2>/dev/null`. If any prior-run directories exist, ask the user **Fresh run** (new runid, prior dirs untouched), **Resume** (reuse most recent runid, skip steps whose output file ends with `---END-REPORT---`), or **Discard prior** (delete prior `tidy-code-*` dirs, then Fresh). Never silently overwrite.
- **Final consolidated plan (the only user-facing file):** After step 8 completes PASS or PASS_WITH_CORRECTIONS, the orchestrator generates a single self-contained markdown file optimized for downstream LLM execution. Path resolution:
  1. If `docs/` exists at the repo root → write to `docs/YYYY-MM-DD-tidy-code-plan.md`.
  2. Else → write to `YYYY-MM-DD-tidy-code-plan.md` at the repo root.

  `YYYY-MM-DD` uses `date +%Y-%m-%d` (date only, distinct from the state-dir runid).
- **User-facing response rule (load-bearing).** The orchestrator's reply to the user at end-of-run MUST mention only the consolidated plan path. Do NOT print the state directory, the per-wave findings files, the review file, or the runid. The state dir is implementation detail. Disclose `.agents/local/state/tidy-code-<runid>/` only if the user explicitly asks where intermediates live.

The final plan format is documented in § Final Plan Format below.

---

## Task List Protocol

At command startup, before any subagent dispatch, the orchestrator MUST create a visible progress checklist covering all nine workflow steps and update it as each step starts and completes. The exact mechanism depends on the agent host (Claude Code, Gemini CLI, Codex, etc.) — see `references/progress-tracking.md` for the canonical step list and per-host adapter rules.

The reference is small and self-contained; load it once at command start, follow the adapter for the current host, and re-consult only when a parallel wave needs an `activeForm` update.

Free-text "Phase N starting" annotations in the conversation are NOT a substitute — the user must see structured, tickable progress.

---

## Subagent Return Contract

Every subagent spawned by this skill MUST end its reply with a Summary block under 150 words. The **literal first line** MUST be a machine-parseable status token: `STATUS: PASS | PASS_WITH_CORRECTIONS | FAIL`. The remainder lists output file path(s) and key counts (files reviewed, findings by severity). Subagents MUST NOT restate the contents of files they wrote — those are on disk for the orchestrator to read on demand. The orchestrator gates step transitions on the STATUS token, not on prose interpretation.

Generic Summary shape (each role extends with its own counts — File Discovery emits two list paths; Findings Reviewer adds KEEP/REVISE/DROP):

```
STATUS: PASS
- Output: <state_dir>/findings.md
- Files reviewed: N
- Findings: N (H: N, M: N, L: N)
- Unverified rewrites: N
```

`<state_dir>` is `.agents/local/state/tidy-code-<runid>/` — the orchestrator passes its absolute path to every subagent in the dispatch prompt. Subagents NEVER hardcode `.agents/tidy/code/` or any other path.

---

## Review Workflow

1. **File Discovery** — If the user listed files, use them. Otherwise dispatch the **File Discovery Subagent** (fast cheap) to run `Bash: scripts/enumerate.sh <project_root>` and split the TSV output (column 2 is `app` or `test`) into the two lists. The script already excludes dotfiles, dot-directories, common build/vendor/cache dirs (`node_modules`, `vendor`, `dist`, `build`, `coverage`, `__pycache__`, `target`, `venv`), and non-source extensions (`.json`, `.yaml`, `.md`, `.lock`, images, fonts, `.d.ts`, etc.). Do nothing else.
   - **Abort conditions:** app-files empty → user-facing error. >1000 app files (50/wave × 20 waves ceiling — 5 concurrent subagents × ≤10 files each per wave) → ask the user to scope the review (e.g., a subdirectory).
2. **Sub-agents load rules** — Each **File-Review Subagent** reads `references/principles-quick-ref.md` at the start of its pass. The orchestrator does NOT load it.
3. **Review files in parallel** — Spawn up to 5 concurrent **File-Review Subagents** (fast cheap; batches of 8–12 files per subagent — see Batching rule below). Each loads reference files on demand and produces findings in the Output Format. **Internal parallelism (mandatory):** within its assigned batch, the subagent must issue `Read` / `Grep` calls in parallel — one assistant turn, many tool calls — not sequentially file-by-file. Independent reads on a 10-file batch run ~10× faster batched. **Falsifiability gate (mandatory):** before emitting any finding, the subagent classifies it FALSIFIABLE (cites a specific snippet/identifier on a specific line that Grep can confirm) or OPINION (a judgment where the evidence is interpretation). For FALSIFIABLE findings the subagent runs `Grep` with an exact pattern against the cited path before emission, stamps `Verified: grep:<pattern>` in the finding, and DROPs the finding if Grep returns no match or matches at a different line — log drops as `dropped_hallucinations: N` in the Summary. For OPINION findings the subagent omits the `Verified:` field. On subagent failure, log and continue.
4. **Dedup and collect** — Orchestrator runs `Bash: scripts/dedup-findings.sh <all per-wave findings files>` (no subagent dispatch). Stdout is the deduplicated finding stream (key: `(TC-NN, file, line)` from the most recent `## ` heading and `- **Line N:**` field); stderr lists every dropped duplicate as `<src>:<id> DROPPED_DUP_OF <keeper>:<keeper_id>`. Then the orchestrator reconciles cross-file violations missed across batches. When the same evidence supports multiple findings (e.g., `UserManager` triggering both TC-04 god class and TC-09 uncommunicative name), keep the higher-severity finding and reference the others in its rationale; do not emit duplicates for the same evidence. Malformed Summary → treat findings as partial, add `Unverified suggestions: [N]`.

### Batching rule (referenced from step 3)

**Default: 8–12 files per File-Review Subagent, 5 concurrent subagents per wave.** This favors fewer-larger over more-smaller because each subagent dispatch costs ~3–5s of orchestration plus ~20k init tokens to reload references and context — overhead that dominates when the actual review work is small. A batch of 10 files takes roughly the same wall-clock as a batch of 3 (the LLM reads in parallel internally per the A2 instruction), but produces 3× the findings per dispatch.

Deviations:
- **Tiny repo (<20 app files total):** one batch of all files, one subagent. Skip the wave structure entirely.
- **Many small related files (e.g., 30+ identical-shape component files):** raise batch size to 15–20 — the LLM's per-file judgment is fast and consistent on similar shapes.
- **Large heterogeneous files (e.g., 500+ LOC each):** drop batch size to 5–7 — context window pressure within the subagent dominates dispatch overhead.

Never drop below 3 files per batch (init overhead > review work). Never exceed 20 (context window pressure within the subagent + diminishing-returns on parallel reads).
5. **Classify severity** — **Severity Classifier Subagent** (fast cheap) applies `references/severity-rubric.md` to assign high/medium/low; rubric is a deterministic lookup, no reasoning required.
6. **Verify suggestions** — **Rewrite Verifier Subagent** (mid-tier reasoning) confirms each rewrite resolves the flagged violation without introducing a new one; returns a one-line rationale per finding (e.g., `"OK — guard clause eliminates the nested if; no new branch introduced"`). On failure after one revision pass (depth=1), emit the sentinel string defined below. Do not retry further.
7. **Assemble report** — Write findings to `<state_dir>/findings.md`. Group findings by file, then by severity (high first). End with the summary block.
8. **Adversarial review** — Dispatch the **Findings Reviewer Subagent** (mid-tier) with `references/adversarial-review-prompt.md`. Output: `<state_dir>/findings-review.md` ending in PASS / PASS_WITH_CORRECTIONS / FAIL. On FAIL, re-run the affected file-review subagents once (depth=1) before finalizing. On PASS_WITH_CORRECTIONS, the orchestrator applies the reviewer's REVISE/DROP decisions to the report in place.
9. **Generate final consolidated plan** — Once step 8 is PASS or PASS_WITH_CORRECTIONS, the orchestrator transforms the validated `<state_dir>/findings.md` into a single self-contained file at `docs/YYYY-MM-DD-tidy-code-plan.md` (or repo root if `docs/` doesn't exist) using the format in § Final Plan Format. This file is the only artifact mentioned in the end-of-run response to the user.

**Sentinel strings.** `[Suggested rewrite could not be verified — manual rewrite required]` — emitted verbatim in the `Suggested:` field when rewrite verification (step 6) fails after one retry. The Summary's `Unverified rewrites: N` line MUST always appear (use 0 when none).

---

## Multi-agent debate protocol

The Findings Reviewer marks `severity: high` findings as `DEBATE_PENDING` when **either** `confidence: low` **or** the file-review pass emitted the rewrite-verifier sentinel `[Suggested rewrite could not be verified — manual rewrite required]`. For each pending finding the orchestrator runs a **2-agent × 2-round debate** in this exact shape (per Du et al. 2024, scoped down for solo-dev budget):

1. **Spawn two mid-tier reviewer subagents in parallel, fresh contexts.** Each receives: the full finding (file, line, snippet, principle, refactoring, suggested, severity, `Verified:` token), the file-review subagent's reasoning, and the Findings Reviewer's tentative verdict and reason. Neither subagent sees the other's response or the original Findings Reviewer prompt.
2. **Round 1 — independent verdict.** Each subagent returns KEEP / REVISE / DROP with a ≤40-word reason.
3. **Round 2 — exchange and rebut.** The orchestrator passes each subagent the other's Round 1 reason (verbatim) and asks for a refined verdict + ≤40-word rebuttal. The subagents now know each other's position but did not see each other's deliberation.
4. **Orchestrator resolves.**
   - Both agree on the final verdict → use it.
   - Disagree → the orchestrator (mid-tier, this skill's main agent) reads both Round 2 positions and chooses the verdict with the stronger evidence — **never default to DROP** (a default-DROP rule bakes in a false-negative bias that contradicts the whole point of falsifiability gating: silent loss of true findings is the worst failure mode).
5. **Record outcome.** The resolved verdict overrides `DEBATE_PENDING` in the Findings Reviewer's output. The orchestrator appends a one-line audit note to the review file: `Debated: agreed | resolved-by-orchestrator: KEEP|REVISE|DROP`. The orchestrator then applies the resolved REVISE/DROP decisions per step 8.

**Budget guard.** Debate fires on the contested subset only. If more than 15% of total findings hit the trigger, the orchestrator stops dispatching new debates and surfaces the situation: high-stakes uncertainty at this rate is a tier-promotion signal (see Escalation triggers), not a debate-volume signal.

---

## Model & Effort Guidance

**Tier vocabulary** — *Fast cheap* = Claude Haiku 4.5 or Gemini Flash 2.5; *Mid-tier* = Claude Sonnet 4.6 or Gemini 2.5 Pro; *Frontier* = Claude Opus 4.7 or current frontier-class.

| Role | Model tier | Effort | Rationale |
|------|-----------|--------|-----------|
| Orchestrator | Mid-tier | High | Coordinates steps 1–8, parses subagent Summary blocks, applies reviewer KEEP/REVISE/DROP decisions, decides retry/proceed. |
| File Discovery Subagent (step 1) | Fast cheap | Low | Thin wrapper around `scripts/enumerate.sh` — invokes the script, splits TSV output into app/test lists, applies the abort conditions. No glob/filter reasoning required. |
| File-Review Subagent (step 3) | Fast cheap | Medium | Rule application against the 13 TC-* categories — structured pattern matching against a fixed catalog. |
| Severity Classifier Subagent (step 5) | Fast cheap | Low | Deterministic rubric lookup against `severity-rubric.md`. |
| Rewrite Verifier Subagent (step 6) | Mid-tier | Medium | Judgment about whether each rewrite resolves the violation without introducing a new one. |
| Findings Reviewer Subagent (step 8) | Mid-tier | High | Adversarial judgment about hallucinated citations, false positives, severity inflation, rewrite actionability, missing findings. Citation re-verification is offloaded to `scripts/verify-citation.sh`; the subagent's remaining work is pure judgment. Quality of the final report tracks this role most directly. |
| Debate Reviewer (×2, parallel, fresh context each) | Mid-tier | Medium | Independent second-opinion on each DEBATE_PENDING finding. Inputs: single finding + tentative verdict + reason. Output: KEEP/REVISE/DROP + ≤40-word reason. Narrow scope keeps budget low; mid-tier for judgment quality. |

### Escalation triggers

The orchestrator promotes the named role one tier (fast-cheap → mid-tier, or mid-tier → frontier) the first time any trigger fires. Promotions are sticky for the remainder of the run — do not demote.

| Condition (measured by orchestrator) | Threshold | Promote |
|---|---|---|
| App source files after test/app split | > 500 | File-Review Subagent |
| Distinct languages in the review run | ≥ 3 | File-Review Subagent |
| Malformed Summary rate on first pass (missing/wrong STATUS first line) | > 30% of File-Review returns | Re-dispatch that wave one tier higher |
| File-Review Subagent `dropped_hallucinations` rate, run-wide | > 20% of emitted findings | File-Review Subagent |
| Findings Reviewer `HALLUCINATED_CITATION` rate | > 30% of reviewed findings | File-Review Subagent (re-review affected files) |
| Findings Reviewer false-positive rate (DROP for reasons other than HALLUCINATED_CITATION) | > 30% of reviewed findings | File-Review Subagent |

A promotion that fires twice in the same wave signals a structural problem — stop and surface the run state to the user rather than promote a third time.

---

## Deterministic shell helpers (`scripts/`)

Steps 1, 4, and 8 delegate mechanical work to shell scripts under `scripts/` in the skill installation root. These replace LLM token spend on file enumeration, exact-match deduplication, and citation re-verification — work that gains nothing from reasoning.

| Script | Used by | Replaces |
|--------|---------|----------|
| `scripts/uuidv7.sh` | Orchestrator (startup) | A collision-prone `date` runid — emits the run's UUIDv7 `<runid>` |
| `scripts/enumerate.sh <area>` | File Discovery (step 1) | LLM Glob+extension-filter+test/app-split |
| `scripts/dedup-findings.sh <findings_file> [...]` | Dedup Subagent (step 4) | LLM fan-in dedup |
| `scripts/verify-citation.sh <repo_root> <findings_file>` | Findings Reviewer (step 8) | LLM re-grep loop on every FALSIFIABLE finding |

Each script emits TSV to stdout and uses exit codes for pass/fail. Subagents read script output, not source. Output formats are documented in each script's header comment. All scripts are bash 3.2+ / POSIX coreutils.

---

## Output Format

```
## [file path]
### Finding [N] — [Smell name] [ID] (severity: [high|medium|low])
- **Line [N]:** `[original code snippet]`
- **Verified:** `grep:<exact pattern used>` — FALSIFIABLE findings only
- **Principle:** [One-sentence explanation of the violated principle]
- **Refactoring:** [Named refactoring technique]
- **Suggested:** [concrete rewrite as a fenced code block]
```

The `Verified:` field is required when the finding is FALSIFIABLE (the snippet/identifier on `Line [N]` can be confirmed by Grep) and omitted when the finding is OPINION (a judgment about structure, naming-readability, or design quality where the evidence is interpretation rather than exact-text claim). All TC-* IDs that cite a line and snippet are FALSIFIABLE by default; pure-judgment findings (e.g. TC-09 where the question is whether a real, present name is "uncommunicative") are OPINION.

Full example:

````
## src/services/order_service.py
### Finding 1 — Hidden Dependency TC-02 (severity: high)
- **Line 8:** `self.db = PostgresConnection("prod:5432")`
- **Verified:** grep:`self\.db = PostgresConnection` against src/services/order_service.py — matches line 8
- **Principle:** Constructing collaborators inside `__init__` couples this class to one concrete implementation — untestable and tightly bound to Postgres.
- **Refactoring:** Constructor injection.
- **Suggested:**
  ```python
  def __init__(self, db: Database, mailer: Mailer):
      self.db = db
      self.mailer = mailer
  ```
````

Omit files with no findings. End the report with:

```
## Summary
- **Files reviewed:** [N]
- **Total findings:** [N] ([N] high, [N] medium, [N] low)
- **Top issues:** [List the 2-3 most frequent violations]
- **Highest-leverage fix:** [The single change that would most improve the codebase]
- **Unverified rewrites:** [N]

---END-REPORT---
```

The trailing `---END-REPORT---` marker is mandatory on both `<state_dir>/findings.md` and `<state_dir>/findings-review.md`. The orchestrator uses the marker — not file presence — to decide whether to skip the assembly or review step on Resume. A file missing its marker is treated as truncated and re-run.

---

## Final Plan Format

After step 8 finalizes, the orchestrator writes ONE consolidated markdown file optimized for a downstream LLM (or human) to execute. Path resolution per § Run state directory & final output. The file is fully self-contained — no reference to the state directory, the per-wave scratch files, the runid, or any subagent. A reader who has never heard of this skill can pick it up and apply every change.

Structure (XML-tagged sections to maximize parser-friendliness for downstream agents):

````markdown
# Tidy-Code Plan — <YYYY-MM-DD>

<context>
- Project root: <absolute repo path>
- Generated: <ISO-8601 timestamp>
- Files reviewed: <N>
- Total findings: <N> (high: <N>, medium: <N>, low: <N>)
- Top issues: <bullet list of 2–3 most frequent TC-NN violations>
- Highest-leverage fix: <one line>
</context>

<instructions>
You are an implementation agent. Apply the refactorings below in this order:
1. Within a file: high → medium → low severity.
2. Across files: alphabetical by path.

For each finding:
1. Open the cited file at the cited line.
2. Confirm the **Original** snippet still matches at that line (citations may have drifted — if the snippet moved, search the file; if it's gone, skip and note it).
3. Apply the **Refactoring** technique using the **Suggested** rewrite exactly.
4. Run any **Verification** command provided.
5. Move to the next finding only after verification passes.

Hard constraints:
- Behavior-preserving refactors only. Do NOT change observable behavior.
- Do NOT apply findings flagged `[Manual review required — ...]` — surface them to the user separately.
- Do NOT extend scope (no adjacent cleanup, no test changes unless listed).
- Run the project's existing test suite after each file is done; if a test fails, stop and report the file + finding.
</instructions>

<changes>

## <file path 1>

### Finding 1 — TC-NN <smell name> (severity: high)
- **Line:** <N>
- **Original:** `<exact original snippet>`
- **Principle:** <one-sentence explanation>
- **Refactoring:** <named technique>
- **Suggested:**
  ```<lang>
  <concrete replacement code>
  ```
- **Verification:** <how to confirm safe — e.g. "npm test -- order_service", "tests still green", or "type-check passes">

### Finding 2 — ...

## <file path 2>

...

</changes>

<manual_review>
Findings whose rewrite could not be auto-verified. Apply human judgment before changing the code.

### Finding M — TC-NN <smell name> (severity: high)
- **Line:** <N>
- **Original:** `<exact original snippet>`
- **Issue:** <one-line description of the violation>
- **Why manual:** rewrite verification failed — propose your own fix.
</manual_review>

<verification_checklist>
- [ ] All non-manual findings applied in order.
- [ ] Full test suite passes.
- [ ] Type-checker / linter clean on touched files.
- [ ] No new findings introduced (run /tidy-code again to confirm).
</verification_checklist>
````

Rules for the orchestrator when generating this file:
- Drop every finding the reviewer marked DROP.
- Apply every REVISE before transcribing (severity adjustments, rewrite tightening).
- Findings still carrying the `[Suggested rewrite could not be verified — manual rewrite required]` sentinel go in `<manual_review>`, not `<changes>`.
- Sort within each file: high → medium → low. Across files: alphabetical by path.
- The consolidated file is the artifact. The state directory contents must NOT be referenced anywhere in it.

---

## When to Load Reference Files

| File | When to load |
|------|-------------|
| `references/progress-tracking.md` | At command start — orchestrator loads once to pick the right host adapter |
| `references/principles-quick-ref.md` | Always — each file-review sub-agent loads at the start of its pass (not the orchestrator) |
| `references/severity-rubric.md` | When classifying findings |
| `references/adversarial-review-prompt.md` | Loaded by the Findings Reviewer subagent in step 8 — not the orchestrator |

Per-TC reference (load only when reviewing a candidate for that ID): TC-01 `composition-over-inheritance.md` · TC-02 `dependency-injection.md` · TC-03 `guard-clauses.md` · TC-04 `single-responsibility.md` · TC-05 `fail-fast.md` · TC-06 `least-surprise.md` · TC-07 `tell-dont-ask.md` · TC-08 `immutability.md` · TC-09 `naming.md` · TC-10 `functional-core-imperative-shell.md` · TC-11 `magic-numbers.md` · TC-12 `duplicate-logic.md` · TC-13 `commented-out-code.md`.

---

## Scope Rules

| Category | Action | Notes |
|----------|--------|-------|
| Application source | Review | Functions, classes, modules, components |
| Test files | Review (limited) | Apply TC-09, TC-03 only; skip TC-02, TC-10 (side-effectful setup) |
| `/tests/` non-test files | Review as app code | Factories, fixtures, helpers — not limited |
| Generated code, migrations, config (JSON/YAML/TOML), vendor, .d.ts, scripts <20 lines | Skip | — |
| Output only | Do not modify | Produce recommendations; no source file changes |
| Commented-out code blocks within a file | Review | Owned here (TC-13) |
| Comment prose | Out of scope | Run `plain-language` on the file instead |
| Stale TODO/FIXME/HACK markers (textual unfinished-work signals) | Out of scope | See `principles-quick-ref.md` §Scope boundaries |
| Cross-file duplicate logic | Out of scope | See `principles-quick-ref.md` §Scope boundaries |
| Cross-file rename with blast radius > 5 files | Flag for confirmation | Decorate finding with `blast radius: N files — confirm before applying` (TC-09) |

*Review (limited)* = apply only the listed TC-* IDs; skip all others.
