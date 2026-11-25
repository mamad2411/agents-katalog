---
name: baseline-selection-audit
description: Audit whether an ML or AI paper's experimental baselines are necessary, fair, current, and reviewer-proof. Use this skill whenever the user is planning experiments, comparing methods, choosing baselines, worried about missing SOTA or unfair comparisons, preparing a reviewer-proof experiment section, or converting a literature review into must-have, should-have, optional, and not-comparable baselines.
argument-hint: "[project-dir-or-paper-claim] [--mode plan|audit|rebuttal|camera-ready] [--venue <venue>]"
allowed-tools: Read, Write, Edit, Bash, Glob, WebSearch, WebFetch
---

# Baseline Selection Audit

Turn a claim, method, draft experiment plan, or literature map into a reviewer-proof baseline set and fairness ledger.

Use this skill when:

- experiments are being planned and the right baselines are unclear
- a literature review found competitors but they have not been converted into comparisons
- a paper may be missing SOTA, direct competitors, classics, ablation baselines, or control baselines
- a reviewer might complain about unfair tuning, scale, data, compute, protocol, or metric differences
- a rebuttal or revision needs to decide which additional baseline experiment is worth running
- the user needs to justify why a baseline is excluded as not comparable

Do not use this skill for citation metadata checks. Use `citation-audit` for BibTeX and LaTeX correctness. Use `citation-coverage-audit` when the primary question is missing references rather than missing comparisons.

Pair this skill with:

- `literature-review-sprint` before this skill when the competing paper map is incomplete
- `algorithm-design-planner` when the closest baseline changes the method design
- `experiment-design-planner` after this skill to turn selected baselines into a concrete experiment matrix
- `run-experiment` only after baseline scope, fairness rules, and stop conditions are clear
- `result-diagnosis` when baseline results are surprising, unstable, or stronger than the proposed method
- `paper-evidence-board` when baseline risks must be linked to paper claims, figures, and sections
- `research-project-memory` when baseline decisions, risks, and actions should persist across sessions

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    ├── baseline-taxonomy.md
    ├── fairness-ledger.md
    ├── memory-writeback.md
    ├── report-template.md
    └── reviewer-risk.md
```

## Progressive Loading

- Always read `references/baseline-taxonomy.md`, `references/fairness-ledger.md`, and `references/reviewer-risk.md`.
- Read `references/report-template.md` before writing the final audit.
- Read `references/memory-writeback.md` when the project has `memory/`, component `.agent/` folders, or the user asks for persistent project memory.
- If the baseline set depends on current SOTA, recent concurrent work, or venue expectations, verify with current sources through web search, OpenReview, proceedings, arXiv, PMLR, ACL Anthology, CVF, DBLP, Semantic Scholar, or user-provided papers.
- If current verification is unavailable, mark baseline status as provisional and identify the missing search needed before final experiment planning.

## Core Principles

- Baselines exist to defend a claim, not to decorate a table.
- Separate closest conceptual competitor, strongest empirical baseline, standard benchmark baseline, ablation baseline, and control baseline.
- A baseline can be missing for citation purposes, comparison purposes, or both. Name which one.
- Fairness must cover data, model size, compute, tuning, metric, protocol, code availability, and reporting.
- Do not ask the user to run every possible baseline. Rank by reviewer impact and decision value.
- Excluding a baseline requires a defensible reason and often a citation or limitation statement.
- A strong baseline beating the method is project information, not merely an experiment failure.
- The output must hand off directly to `experiment-design-planner`.

## Step 1 - Recover Claim and Comparison Surface

Collect:

- paper claim or experiment claim
- proposed method and closest baseline, if known
- target task, dataset, benchmark, metric, and protocol
- target venue or community expectations
- existing results, draft tables, or planned experiments
- literature-review outputs, if available
- code availability and compute budget
- project memory IDs such as `CLM-###`, `EVD-###`, `RSK-###`, or `ACT-###`

Rewrite the claim into:

```text
We need to show that [method] improves [property] over [comparison set] under [task/protocol], without the result being explained by [confound].
```

If this cannot be written, route to `research-idea-validator`, `algorithm-design-planner`, or `paper-evidence-board`.

## Step 2 - Build Candidate Baseline Pool

Use:

- literature review outputs
- cited related work
- benchmark leaderboards or official baselines
- recent accepted papers at the target venue
- code repositories or model releases
- reviewer comments, if this is rebuttal mode

Classify each candidate using `references/baseline-taxonomy.md`.

The pool should include:

- direct competitor
- strongest current method
- standard benchmark baseline
- classic baseline
- previous version or nearest ablation of the user's method
- no-method or trivial control baseline
- oracle, upper bound, or diagnostic baseline when appropriate
- resource-matched baseline
- domain-specific baseline expected by the venue

## Step 3 - Assign Baseline Requirement Level

For each candidate, assign exactly one:

- `must-have`: paper is hard to defend without it
- `should-have`: materially improves reviewer confidence, but omission may be defensible
- `optional`: useful context, low acceptance impact
- `not-comparable`: related but unfair or invalid as a direct comparison
- `citation-only`: should be discussed/cited but does not need an experiment

Every `must-have` baseline needs an owner, experiment form, fairness constraints, and fallback if impossible.

Every `not-comparable` baseline needs a reason:

- different task or data
- incompatible metric
- unavailable code and reproduction too expensive
- different resource regime
- uses extra supervision or data
- no public details sufficient for faithful reproduction
- evaluates a different claim

## Step 4 - Audit Fairness

Read `references/fairness-ledger.md`.

For each `must-have` and `should-have` baseline, check:

- same data split and preprocessing
- same training data and extra-data policy
- comparable model size or explicit scale control
- comparable compute or explicit compute-normalized metric
- comparable tuning budget
- comparable evaluation metric and decoding/sampling protocol
- correct official code or faithful reimplementation
- enough seeds, confidence intervals, or variance reporting
- same reporting unit: tokens, examples, images, FLOPs, wall-clock, NFE, parameters, or memory

If fairness cannot be achieved, decide whether to:

- change claim
- add a matched subset comparison
- run a smaller diagnostic comparison
- mark baseline as citation-only with clear limitation
- defer to rebuttal risk

## Step 5 - Forecast Reviewer Attacks

Read `references/reviewer-risk.md`.

For each missing, weak, or unfair baseline, write the likely reviewer objection:

```text
Reviewer could say: [attack].
Severity: fatal / major / medium / minor
Mitigation: run / cite / justify / narrow claim / move to appendix / accept risk
```

Prioritize by acceptance impact:

- fatal novelty or comparison threat
- required benchmark/SOTA omission
- unfair tuning or compute
- weak ablation baseline
- unclear protocol
- missing control

## Step 6 - Produce Experiment Handoff

For `experiment-design-planner`, output:

- selected baselines and requirement levels
- exact comparison table rows
- fairness ledger fields to log
- metrics and protocol constraints
- ablation/control baselines
- stop conditions
- expected reviewer question each baseline answers
- fallback plan if a baseline is impossible

If compute is limited, propose a staged plan:

1. minimal reviewer-proof set
2. high-impact optional additions
3. appendix or deferred baselines

## Step 7 - Write the Baseline Audit Report

Read `references/report-template.md`.

If saving to a project and no path is given, use:

```text
docs/experiments/baseline_selection_audit_YYYY-MM-DD_<short-name>.md
```

If working inside a code repo or code worktree created by `init-python-project` / `new-workspace`, prefer:

```text
docs/reports/baseline_selection_audit_YYYY-MM-DD_<short-name>.md
```

The report must include:

- claim under audit
- candidate baseline pool
- requirement-level table
- fairness ledger
- reviewer attack forecast
- selected experiment matrix handoff
- baselines excluded and why
- memory update section

## Step 8 - Write Back to Project Memory

Read `references/memory-writeback.md` when memory exists.

Update the smallest useful set of entries:

- `memory/risk-board.md`: missing, unfair, unavailable, or not-comparable baseline risks
- `memory/evidence-board.md`: planned baseline comparisons and ablations
- `memory/action-board.md`: implementation, run, citation, or justification actions
- `memory/claim-board.md`: claims narrowed by baseline feasibility
- `memory/decision-log.md`: durable decisions to include, exclude, or stage baselines
- worktree `.agent/worktree-status.md`: baseline implementation purpose and exit condition
- `paper/.agent/`: table/section implications when a draft exists

Use certainty labels:

- `verified` for baselines checked against primary sources or official code
- `user-stated` for constraints supplied by the user
- `inferred` for reviewer risks and fairness judgments
- `unverified` for candidates not yet checked

## Final Sanity Check

Before finalizing:

- every paper claim has at least one direct comparison or control
- closest conceptual competitor and strongest empirical baseline are not conflated
- `must-have` baselines are explicit
- excluded baselines have defensible reasons
- fairness constraints are concrete enough to run
- reviewer attacks are written in reviewer language
- the output can feed directly into `experiment-design-planner`
- project memory is updated when present
