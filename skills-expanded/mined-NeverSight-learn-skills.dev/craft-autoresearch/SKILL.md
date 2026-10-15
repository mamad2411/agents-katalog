---
name: craft-autoresearch
description: Eval-driven autonomous optimization loop for a prompt or skill. Define eval criteria and a run harness, then iterate — run the artifact on test inputs, score outputs, mutate the prompt or skill, keep improvements, discard regressions, and stop on a written condition. Use this whenever the user wants to automatically improve a prompt or skill, mentions autoresearch, eval-driven optimization, benchmarking a skill, running evals, self-improving a prompt, or any iterative test-and-refine request — including 스킬 개선, 스킬 최적화, 스킬 벤치마크, 스킬 평가 — even if they don't say "autoresearch."
---

# craft-autoresearch

## Purpose

Run an eval-driven autonomous optimization loop on a prompt or skill.

Many prompts and skills feel "mostly fine" until the last 20-30% of failures show up. Re-reading rarely finds those gaps. You find them by running the artifact many times, scoring outputs against a rubric, mutating one thing at a time, and keeping only the changes that measurably move the score.

Unlike `craft-tune` (single human-driven edit) or `craft-critique` (diagnostic read), autoresearch *measures*. Gains come from the loop, not from one clever rewrite.

## Use this when

- a prompt or skill works "sometimes" and needs to work reliably
- measurable quality criteria exist or can be drafted (format rules, pass/fail checks, comparative quality)
- human-driven tuning has hit a plateau
- a skill is about to be shipped and should be benchmarked first

Do not use this when:

- quality is entirely subjective with no rubric even sketchable — prefer `craft-critique` + `craft-tune`
- the run harness cannot be automated at reasonable cost
- the artifact is too new and has no rough baseline yet

This skill is for optimizing prompt and skill artifacts against output-quality evals, not for generic code-metric loops (test coverage, bundle size, lint errors).

## Inputs

- **Target artifact** — path to the prompt or skill file to optimize
- **Test inputs** — 3-5 realistic prompts or scenarios
- **Eval criteria** — 3-6 binary checks plus 0-2 comparative quality checks
- **Run harness** — the exact repeatable command or procedure that runs the artifact on a test input
- **Budget** — max experiments per session (default: 10)
- **Stop condition** — target score, or "plateau for N kept experiments"

If the user provides an `evals.json`, use it directly instead of drafting evals inline.

## Steps

1. **Capture the experiment contract.** Lock in target, inputs, evals, harness, budget, and stop condition *before* running anything. A fuzzy contract produces fuzzy gains — ambiguity at this step compounds with every experiment.
2. **Design the eval suite.** Prefer deterministic checks (regex, section presence, parse success) over LLM-as-judge. Aim for at least half the suite at Tier 1-2 — see `references/eval-guide.md` for the full determinism hierarchy and quality checks. First-time suites skew toward Structure/Length only and saturate on baseline; see the Guardrails rule on near-100% baselines and `references/eval-guide.md` § "If your baseline scores near 100%" before locking the suite.
3. **Establish a baseline.** Snapshot the target artifact, run it on every test input through the harness, score every output, record the total in `results.tsv`. No mutation happens before baseline or the gains are unmeasurable. A near-saturated baseline (≥ 95% binary pass rate) is a signal, not a success — stop and strengthen the suite before mutating. See Guardrails below.
4. **Run the mutation loop.** For each experiment: analyze failing evals → form one hypothesis → make one bounded change at one mutation level → checkpoint the touched files → run harness → score → KEEP or DISCARD by the rules below → log. The change may span multiple files only when those files together implement the same hypothesis. See `references/mutation-guide.md` for mutation levels and when each fits.
5. **Respect rollback safety.** Before each mutation, commit (git-assisted mode) or snapshot (file-checkpoint mode) only the files you are about to touch. DISCARD rolls back only those files — never `git reset --hard`, which would destroy unrelated work in the repo.
6. **Try deletion every 5th experiment.** Remove recently added rules or examples. If the score holds, keep the deletion. Artifacts that only grow are a smell — bloat hides the real drivers.
7. **Stop on condition, not on vibes.** Stop when the budget is hit, when the stop condition is met (e.g. 95%+ binary pass rate sustained for 3 consecutive kept experiments), when the user interrupts, or when the harness is no longer trustworthy. Running out of ideas is not a stop condition — change mutation level first.
8. **Report back.** Baseline → final score, total experiments, keep rate, top helpful changes, remaining failure patterns, artifact size change, direction shifts.

## When the target is a skill (vs a prompt)

The loop shape is the same, but the *edit unit* differs. A prompt is a single file; a skill is a folder with `SKILL.md`, `references/`, sometimes `scripts/` and `templates/`. That changes five things:

1. **Target selection.** For a prompt, the target is a single file path. For a skill, decide up front what the target covers — usually `SKILL.md` alone, but a mutation may legitimately touch `references/<file>.md` too. Write it into the experiment contract: *"mutable files: SKILL.md, references/eval-guide.md. All other files are frozen."*
2. **Mutation locus.** Mutation levels stay the same (wording / example / structure / principle), but for skills a sixth question appears before applying them: *which file?* Prefer editing `SKILL.md` for skill-spine changes and `references/` for deep-detail changes. Adding a new reference file counts as a Level-3 (structural) mutation — it shifts the skill's shape, not just its wording.
3. **Size metric.** For prompts, `wc -l <file>` is enough. For skills, track two numbers: `skill_lines` (SKILL.md only — the always-loaded budget) and `folder_lines` (everything including references). The primary discipline is keeping `SKILL.md` under its ~500-line target; `folder_lines` is secondary and can grow more before bloat becomes a concern.
4. **Mutation safety.** A prompt mutation touches one file, so checkpoint and rollback are trivial. A skill mutation may touch several — record the exact file list in the experiment's checkpoint, and on DISCARD restore *only those files*. Never rollback the whole folder; unrelated files may hold accepted prior-experiment state.
5. **Fidelity evals (multi-skill pipelines).** If the target is a skill that feeds another skill's input (e.g. `craft-scaffold` → `craft-tune`), add fidelity evals that check stage-to-stage consistency. Not applicable for single-file prompts.

Everything else — experiment contract, baseline discipline, KEEP/DISCARD rules, deletion experiments, stop conditions — works identically for prompts and skills.

## KEEP vs DISCARD

Record artifact size for every experiment. For prompts, `wc -l <file>` is enough. For skills, record both `skill_lines` (`SKILL.md` only) and `folder_lines` (the whole skill folder). Apply these defaults unless the user defined stricter rules:

| Score change | Artifact size change | Default decision |
|---|---|---|
| Improved meaningfully | Any reasonable change | KEEP |
| Improved marginally | Large growth | DISCARD unless the gain fixes an important failure |
| Flat | Shorter or simpler | KEEP |
| Flat | Longer or more complex | DISCARD |
| Worse | Any | DISCARD |

Additional guardrails:

- If a previously passing eval now fails, lean toward DISCARD even if the total score rose — a regression hidden by aggregate gain is still a regression.
- On ties, prefer the shorter artifact.
- If the mutation changes user-facing behavior, diff representative outputs before keeping it.

## Output format

### Experiment contract

A compact record of target, inputs, evals, harness, budget, stop condition. In addition, state these quality commitments explicitly, not just as labels:

- **mutable files** — explicit list of the files the session may modify. All other files are frozen. Mandatory for skill targets; every skill has more than one file even when references are not planned to change.
- **evals 4th diagnostic** — for every Logic or Comparative eval, name a concrete output the target-skill-as-written would plausibly produce that fails the check (the 4th diagnostic question from `references/eval-guide.md`). A Logic eval without a named plausible-failing-output is a loose eval and usually saturates.
- **harness design** — the named design category plus its trade-off against alternatives. A bare command string is not a harness design.
- **first-mutation hypothesis preview** — the predicted mutation locus in the target (a specific `## Output format` subsection, a specific `## Steps` entry, or a specific reference-file section) plus a justification that either invokes the Build-step enforcement prior from `references/mutation-guide.md` by name, or explicitly argues why a non-build-step locus is warranted from the failing outputs.

### Baseline
Score (numerator/denominator), failing evals, 1-2 representative outputs.

### Experiment log
One row per experiment: number, hypothesis, change, score, KEEP/DISCARD, rationale.

### Final artifact
Path to the accepted version and a one-line size note.

### Direction shifts
Meaningful strategy pivots during the run, one line each. Record in `research-log.json` if persisting.

### Next steps
What to run next if the user wants more, or which evals to sharpen.

## Artifact layout

Run artifacts live in `~/.craftkit/`, not in the target repo. This keeps `git status` clean, makes runs worktree-agnostic, and avoids accumulating audit dirs in the project being tuned. Findings that justify a spec change belong in the commit message body, not in committed run artifacts.

```text
~/.craftkit/autoresearch/<skill-name>/<YYYY-MM-DD-slug>/
├── run-harness.md      # exact harness and contract for this session
├── evals.json          # eval suite used
├── results.tsv         # one row per experiment
├── changelog.md        # mutation rationale + human insights
├── research-log.json   # direction shifts only, not every edit
├── <target>.baseline   # backup of the starting artifact at session start
└── runs/
    ├── inputs/
    ├── baseline/
    ├── exp-1/
    └── ...
```

The `<YYYY-MM-DD-slug>` naming (e.g. `2026-04-12-output-format-tightening`) prevents collisions when the same skill is tuned in multiple sessions and gives each session a human-readable anchor. Treat the folder shape above as the convention, and copy findings back into the repo only when they justify a spec change, usually as an inline quote or a commit-message note rather than committed run artifacts.

## Guardrails

- One hypothesis per experiment. The accepted change may touch more than one file only when those files implement the same mutation and are checkpointed as a unit.
- Always run the harness and record the score; never KEEP on "this feels better."
- Deterministic evals first; LLM-as-judge only with a rubric explicit enough that two reviewers would agree.
- Rollback touches only the files in the mutation — never broad reverts.
- Autonomy is batch-based. Set a budget and stop condition up front, not "loop forever."
- **If the baseline binary pass rate is ≥ 95%, do NOT start the mutation loop.** A saturated baseline means the suite only measures output shape, not quality — mutating against it produces noise. Strengthen the evals first: read 3-5 real outputs, name the quality dimensions the suite missed, add 2-3 new Tier 1-2 assertions, rebaseline. See `references/eval-guide.md` § "If your baseline scores near 100%."
- If eval scores rise but real outputs feel worse, treat it as a false-positive signal: review 10 real outputs and rebuild the evals before continuing.

## Failure modes

- Starting without a baseline — "improvement" becomes meaningless.
- An eval suite that's entirely LLM-as-judge — scores drift and you optimize noise.
- Mutating several unrelated things in one experiment — outcomes can't be attributed to specific changes.
- Using `git reset --hard` for rollback — destroys the user's unrelated work.
- Running until "looks good" without a written stop condition — produces prompts that overfit the eval set.
- Declaring victory when score rises but real outputs feel worse — the evals are the problem, not the artifact.
- Treating autoresearch as a one-off — the 1-week re-run against fresh inputs is where overfitting gets caught.

## Example

### Input

Optimize `skills/craft-critique/SKILL.md` so reviews are structurally consistent across Claude Code and Codex.

Test inputs: three real review prompts from last week.

Eval criteria:

- Binary: output has exactly five sections (What's working, Issues, Recommended changes, Failure modes, Minimal rewrite plan).
- Binary: Issues section contains at most 5 prioritized items.
- Binary: every item in Recommended changes is phrased as an imperative command.
- Comparative: is the review more actionable than baseline? (blind A/B judge)

Budget: 8 experiments. Stop condition: 95% binary pass rate sustained for 3 consecutive kept experiments.

### Output

**Experiment contract**
- target: `skills/craft-critique/SKILL.md`
- inputs: 3 prompts
- evals: 3 binary + 1 comparative
- harness: `node scripts/run-skill.mjs craft-critique <input.txt>`
- budget: 8; stop: 95% × 3 consecutive

**Baseline**
Score: 7/12 (58%). Failing: section count varies (3-6); issue count unbounded.

**Experiment log**

| # | Hypothesis | Change | Score | Decision |
|---|---|---|---|---|
| 1 | Tighten section spec | Added "exactly these 5 sections" line | 9/12 | KEEP |
| 2 | Cap issue list | Added "max 5, ordered by severity" | 11/12 | KEEP |
| 3 | Enforce imperative recs | Added example + "commands, not questions" rule | 12/12 | KEEP |
| 4 | Deletion check | Removed the added example | 10/12 | DISCARD (example carries weight) |
| 5 | Restore + sharpen example | Restored example with two cases | 12/12 | KEEP |
| 6 | Stability check | Re-ran to confirm | 12/12 | KEEP — 3 consecutive hit, STOP |

**Direction shifts**
- Flipped from "softer wording" to "explicit constraints" after baseline showed agents needed more structure, not less.

**Next steps**
- Add an eval for "cites file:line in at least one issue" to ground recommendations.
- Re-run in 1 week on fresh inputs to catch eval overfitting.

## References

- `references/eval-guide.md` — Binary, comparative, and fidelity evals; the determinism hierarchy; assertion categories; subjective-to-binary decomposition; eval quality check; a prompt template for drafting evals with an agent; `evals.json` schema; false-positive recovery.
- `references/mutation-guide.md` — Mutation levels (wording, example, structure, principle), when each fits, and the deletion discipline.
- `references/worked-example.md` — A full illustrative cycle against `craft-critique` showing baseline, five experiments (including a DISCARD and a deletion), stop condition, and the simplicity judgment behind each KEEP/DISCARD.
