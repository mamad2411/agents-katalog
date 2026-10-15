---
name: result-diagnosis
description: Use when results are valid but surprising, negative, unstable, or ambiguous — to decide debug/rerun/ablate/revise/park. Not for engineering failures like NaN/OOM (use experiment-debugger). Not for confound or claim-drift audit before locking results into the paper (use research-results-auditor).
argument-hint: "[project-dir] [--result <summary>] [--mode quick|full|debug|decision]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Result Diagnosis

Diagnose what an experiment result means for the project. This skill is for decision-making after results exist, especially when they are negative, surprising, unstable, or hard to interpret.

Use this skill when:

- a method does not improve over baseline
- results vary strongly across seeds
- a metric improves but another metric worsens
- a baseline unexpectedly wins
- a plot or table looks suspicious
- a result may be caused by an implementation bug, metric bug, data issue, or unfair comparison
- early experiments suggest revising the algorithm or paper claim
- the user asks "what does this result mean?" or "what should we do next?"

Do not use this skill to write a polished report. Pair it with `experiment-report-writer` after the diagnosis is clear.

Pair this skill with:

- `research-project-memory` when the diagnosis should update claims, evidence, risks, actions, or worktree status
- `experiment-report-writer` when results need a shareable report
- `algorithm-design-planner` when the diagnosis points to method revision
- `experiment-design-planner` when the diagnosis requires a new controlled experiment
- `run-experiment` when the next step is a rerun, sanity check, or ablation
- `conference-writing-adapter` when the right action is to narrow or reframe paper claims

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    ├── diagnosis-taxonomy.md
    ├── evidence-audit.md
    ├── next-decision-rules.md
    ├── report-template.md
    └── triage-protocol.md
```

## Progressive Loading

- Always read `references/diagnosis-taxonomy.md`, `references/triage-protocol.md`, and `references/next-decision-rules.md`.
- Read `references/evidence-audit.md` when inspecting logs, configs, metrics, plots, runs, or code state.
- Use `references/report-template.md` for full diagnosis reports.
- If a result depends on current SOTA, benchmark conventions, or recent baseline performance, verify current sources with web search or user-provided papers.

## Core Principles

- Diagnose before optimizing.
- Separate observed result from interpretation.
- Prefer simple sanity checks before expensive reruns.
- Treat negative results as information: they may kill a claim, not the whole project.
- Do not blame the algorithm before checking implementation, data, metric, baseline, and selection rules.
- Do not blame implementation forever when repeated controlled evidence falsifies the claim.
- Every diagnosis should end with a decision: debug, rerun, ablate, revise method, narrow claim, write, park, or kill.
- Record uncertainty explicitly.

## Step 1 - Define the Result and Expected Behavior

Extract:

- experiment question and linked claim
- method and baseline
- dataset/split
- metrics and expected direction
- observed result
- number of seeds/repeats
- configs, commit, logs, tables, and figures
- what result was expected and why
- whether this result affects paper claims or only internal debugging

Rewrite vague input into:

```text
Expected [method] to improve [metric/diagnostic] over [baseline] on [setting], but observed [result] under [controls].
```

If expected behavior was never defined, route back to `experiment-design-planner`.

## Step 2 - Classify the Symptom

Read `references/diagnosis-taxonomy.md`.

Classify the primary symptom:

- no improvement
- regression
- instability or high variance
- metric conflict
- suspiciously large gain
- baseline unexpectedly strong
- diagnostic/performance mismatch
- training failure or divergence
- reproducibility failure
- plot/table inconsistency
- result contradicts paper story

Then classify likely diagnosis categories:

- implementation bug
- metric/evaluation bug
- data/split/preprocessing issue
- unfair baseline or tuning issue
- seed variance or insufficient repeats
- optimization/hyperparameter issue
- method mechanism failure
- scale/regime mismatch
- claim/evidence mismatch
- expected negative result

## Step 3 - Gather Evidence

Read `references/evidence-audit.md`.

Prefer primary artifacts:

- config diffs
- run commands
- git commit
- logs and stderr
- metric files
- checkpoints
- seeds
- dataset versions and split hashes
- plots and tables
- previous baseline runs
- implementation changes

Mark missing evidence rather than guessing.

## Step 4 - Run Triage

Read `references/triage-protocol.md`.

Use this order:

1. Reproducibility and provenance: correct commit, config, data, seed, output path.
2. Metric and evaluation: metric direction, aggregation, split, leakage, postprocessing.
3. Baseline fairness: same budget, tuning, checkpoint rule, data, sampler, and code path.
4. Implementation sanity: feature flag, tensor shapes, gradient flow, loss scale, train/eval mode.
5. Statistical stability: seeds, variance, confidence intervals, outliers.
6. Mechanism diagnostic: whether the intended mechanism changed.
7. Claim alignment: whether the result supports, weakens, or falsifies the paper claim.

Stop early only when a blocking bug or invalid comparison is found.

## Step 5 - Build Competing Explanations

For each plausible explanation, state:

- evidence for it
- evidence against it
- cheapest test that would distinguish it
- decision if true

At minimum consider:

- bug
- bad metric
- weak experiment design
- baseline too strong or under-tuned
- hyperparameter issue
- mechanism false
- claim too broad

## Step 6 - Choose Next Decision

Read `references/next-decision-rules.md`.

Choose one primary decision:

- `debug`: result is not trustworthy until a bug or provenance issue is resolved
- `rerun`: result is plausible but underpowered or missing controls
- `ablate`: result needs mechanism isolation
- `revise-method`: mechanism likely needs design change
- `narrow-claim`: evidence supports a smaller or different claim
- `write`: evidence is trustworthy enough to report
- `park`: result is inconclusive and not worth immediate compute
- `kill`: claim or direction is falsified under fair controls

Do not pick `write` if basic provenance or fairness is unresolved.

## Step 7 - Write the Diagnosis

Use `references/report-template.md` for full reports.

If saving to a project and no path is given, use:

```text
docs/diagnosis/result_diagnosis_YYYY-MM-DD_<short-name>.md
```

Required output:

```markdown
# Result Diagnosis: [Short Name]

## Result Snapshot
## Expected vs Observed
## Symptom Classification
## Evidence Checked
## Competing Explanations
## Most Likely Diagnosis
## Decision
## Next Checks or Actions
## Claim Impact
## Project Memory Writeback
```

## Step 8 - Write Back to Project Memory

If the project uses `research-project-memory`, update:

- `memory/evidence-board.md`: observed result, limitations, and source paths
- `memory/provenance-board.md`: mark result provenance verified, stale, contradictory, or missing when diagnosis depends on source validity
- `memory/claim-board.md`: claims supported, weakened, revised, evidence-needed, provisional, parked, or cut
- `memory/risk-board.md`: bugs, metric risks, baseline risks, mechanism risks, or claim risks
- `memory/action-board.md`: debug, rerun, ablation, method revision, writing, park, or kill actions
- `memory/handoff-board.md`: create handoffs to method design, experiment design, paper evidence, or writing when diagnosis changes downstream work
- `memory/phase-dashboard.md`: update the active gate when diagnosis advances evidence production or regresses the project to debugging, method revision, or claim narrowing
- worktree `.agent/worktree-status.md` "Local Hot Results": update here first when in a code-worktree; mark confirmed/invalidated/superseded status locally before any graduation
- `<ProjectRoot>/memory/hot-results.md`: graduate here only when the result is confirmed and changes a project-level claim; do not write here while diagnosis is still in progress
- `memory/decision-log.md`: durable decisions such as killing a claim, changing method, or narrowing scope

Use `observed` for verified results and `inferred` for explanations. Mark stale claims explicitly.

## Final Sanity Check

Before finalizing:

- observed result and interpretation are separated
- provenance and config are checked or listed as missing
- metric direction and aggregation are clear
- baseline fairness is addressed
- implementation sanity checks are considered
- seed variance and repeats are considered
- mechanism diagnostic is checked when relevant
- result is mapped to a concrete decision
- paper claim impact is explicit
- project memory is updated when present
