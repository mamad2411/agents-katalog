---
name: research-results-auditor
description: Use when auditing completed results for confounds, claim-drift, protocol integrity, or attribution before locking claims into the paper. Not for deciding what to do after a surprising result (use result-diagnosis). Not for significance tests or effect sizes (use statistical-analysis-planner). Not for engineering failures (use experiment-debugger).
argument-hint: "[project-dir] [--claim <claim-id>] [--mode full|confound|protocol|drift|inference]"
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Research Results Auditor

Produce a structured validity verdict for completed experiment results before they become paper claims. This skill asks: *is the evidence scientifically defensible as stated?*

Use this skill when:

- experiments are complete and results are about to be written into the paper as claims
- a result looks convincing but the connection between the measurement and the stated conclusion feels stretched
- a reviewer is likely to ask "what else could explain this?"
- an ablation result is used to attribute a performance gain to a specific component
- class imbalance, calibration, or threshold choice may be driving the metric
- the gap between what was measured and what is claimed in the paper needs to be checked before submission

Do not use this skill when experiments are still running or results are not yet final — use `result-diagnosis` for in-progress diagnosis and next-action decisions. Do not use this skill for test selection or variance reporting — use `statistical-analysis-planner`.

Pair this skill with:

- `result-diagnosis` upstream: resolve engineering and scientific issues before auditing validity
- `statistical-analysis-planner` upstream: ensure variance is characterized before the audit
- `paper-evidence-board` downstream: update evidence slots with the validity verdict
- `paper-writing-contract-planner` downstream: narrow or forbid claims that fail the audit
- `experiment-design-planner` when the audit identifies a controlled experiment needed to rule out a confound

## Skill Directory Layout

```text
<installed-skill-dir>/
├── SKILL.md
└── references/
    └── audit-criteria.md
```

## Progressive Loading

- Always read `references/audit-criteria.md`.
- Read `memory/claim-board.md` and `memory/evidence-board.md` before auditing.
- Read `paper/.agent/paper-evidence-board.md` when claims have paper-facing evidence slots.

## Core Principles

- Separate data observations from author interpretation before auditing.
- A claim is only as strong as its weakest alternative explanation.
- Ablation results prove component contribution only when all other factors are controlled.
- A benchmark metric is not the same as the real-world property being claimed.
- Confidence should decrease as the distance between measurement and claim increases.
- A failed audit should result in a narrowed claim, not silence.

## Step 1 — Reconstruct the Claim

For each result to audit, write in one sentence:

```
Claim: [method/component X] causes [effect Y] on [task/benchmark Z], as shown by [metric M].
```

Then identify:
- the artifact(s) that support it: experiment reports, tables, figures, logs
- what the metric M actually measures vs what Y asserts
- any gap between M and Y (e.g. M = accuracy on a benchmark, Y = "robustness to distribution shift")

If the claim cannot be written in one sentence without hedges, that is an early signal of drift.

## Step 2 — Protocol Integrity Check

Read `references/audit-criteria.md`.

For each claim, verify:

- **Metric–task alignment**: does the metric directly measure the claimed property, or is it a proxy?
- **Comparable conditions**: same data split, same compute budget, same preprocessing for all compared methods?
- **Ablation isolation**: when attributing a gain to component X, is exactly one variable changed?
- **Evaluation coverage**: is the test set representative of the claim's stated scope?
- **Reproducibility**: is the result averaged over enough seeds to be stable? (use `statistical-analysis-planner` if not)

Flag each violation as:
- `blocker`: the claim cannot be made as stated without fixing this
- `risk`: the claim is defensible but a reviewer will likely raise it
- `note`: disclose in limitations or experiment settings

## Step 3 — Confound Audit

For each claim, list at least two alternative explanations and classify:

```
Alternative: [alternative explanation]
Likelihood: high / medium / low
Ruling-out evidence: [experiment, analysis, or prior work that rules it out]
Status: ruled-out / possible / unaddressed
```

Common confounds in ML:

- **Scale confound**: larger model / more parameters / more compute explains the gain
- **Data confound**: the method was tuned on data that overlaps with test distribution
- **Hyperparameter confound**: baseline was not fairly tuned; proposed method was
- **Metric confound**: metric rewards a property (e.g. output length, confidence calibration) that correlates with but is not the claimed property
- **Selection confound**: result is reported only for seeds or checkpoints where it worked

Any unaddressed confound with `high` or `medium` likelihood is an audit blocker.

## Step 4 — Claim-Drift Check

Compare the measured quantity to the stated conclusion. Flag drift if:

- the paper uses language that implies a broader scope than the benchmark covers (e.g. "general reasoning" from a single benchmark)
- a controlled lab result is described as if it transfers to deployment conditions
- a relative improvement % is used to support an absolute capability claim
- performance on a specific demographic or domain is generalized to all users
- a correlation is described as causation without a controlled intervention

For each drift finding, record:
- the measured quantity
- the stated conclusion
- the drift type: scope / generalization / causation / magnitude
- the maximum defensible claim given only the evidence

## Step 5 — Inferential Quality Check

Check that comparative claims meet minimum statistical support:

- Is there a reported uncertainty interval (std, CI, or range) for comparative claims?
- If multiple comparisons are made, has multiple-comparison correction been applied?
- Does class imbalance in the test set affect the metric? (accuracy on imbalanced data overstates performance on the minority class)
- Is calibration relevant? (for claims about probability outputs or confidence-weighted metrics)
- Does threshold choice affect the reported metric? (precision/recall/F1 are threshold-sensitive)

Any comparative claim without reported uncertainty is classified as a `risk`.

## Step 6 — Write the Validity Verdict

For each audited claim, produce:

```markdown
Claim: [one-sentence claim]
Protocol verdict: pass | conditional | fail
Confound verdict: clean | possible-[confound-name] | unaddressed-[confound-name]
Drift verdict: none | scoped-[drift-type]
Inferential verdict: supported | conditional | unsupported
Overall verdict: valid | narrowed | blocked | insufficient-evidence

Recommended wording:
  Allowed: [maximum defensible phrasing]
  Forbidden: [specific language that overclaims]

Required actions:
  - [action to resolve each blocker or risk]
```

Save the audit report to `paper/.agent/results-audit-<date>.md`.

## Step 7 — Memory Writeback

- Update `memory/claim-board.md`: narrow or strengthen claims based on verdicts
- Update `memory/risk-board.md`: add confound and drift risks with severity
- Update `memory/action-board.md`: add required actions for each blocker
- Update `paper/.agent/paper-evidence-board.md`: annotate evidence slots with validity verdict

## Final Sanity Check

Before finishing:

- every main claim has a one-sentence reconstruction
- alternative explanations are listed and classified for each claim
- every blocker has an action
- the audit report is saved with date
- allowed and forbidden claim wordings are explicit for each result
