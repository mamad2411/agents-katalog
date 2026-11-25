---
name: review-revision
description: "Review and revise academic manuscripts with a senior-reviewer workflow. Use for paper drafts, rejected papers, or concrete paper ideas to audit the claim, insight, novelty, method, theory, experiments, statistics, figures, writing, and submission risk; produce revision plans, section edits, or final checklists. Do not use for rebuttal or review-response letters after reviews arrive; use rebuttal-response."
---

# Review Revision

## Overview

Use this skill as a review-and-revision workflow for an existing manuscript, rejected paper, post-review manuscript revision, or idea with a concrete direction. Treat the paper as a research system: problem, insight, novelty, idea, method, experiments, writing, and final readiness. The goal is not to summarize what the paper says, but to judge what it actually proves, what reviewers will doubt, and what concrete edits or experiments can fix it.

Post-review manuscript revision is in scope; writing the response letter is not. For rebuttal-only work, AC-facing summaries, reviewer concern triage, or response tone repair, use `rebuttal-response`.

For the detailed review/revision framework, read `references/review_revision_skill.md` whenever the task asks for deep critique, revision planning, experiment design, detailed editing, or final checklist work.

## Operating Modes

Choose the smallest mode that satisfies the user request.

1. **Paper整理**: extract the paper map, core claim, contribution type, method logic, experiment logic, and closest related work.
2. **论文拆解**: rebuild the author’s intended reasoning chain from problem to evidence; identify where the chain breaks.
3. **深刻反思**: evaluate insight, novelty, claim scope, mechanism, theory assumptions, statistical rigor, alternative explanations, experiment sufficiency, and likely reviewer objections.
4. **修改规划**: produce a prioritized plan with issue, why it matters, exact fix, target section, and required evidence or edits.
5. **细致修改**: rewrite or patch the manuscript section by section while preserving the author’s real contribution and avoiding unsupported claims.
6. **最终 checklist**: produce a submission-readiness checklist covering problem, novelty, method, theory, experiments, statistics/reproducibility, figures/tables, writing, naming/positioning, ethics/compliance, and reviewer-risk items.

## Core Workflow

### 1. Intake the Artifact

Read the provided artifact before judging it. For a manuscript, inspect the abstract, introduction, related work, method, experiments, limitations, conclusion, figures, tables, and appendix when available.

If only a paper idea or partial draft exists, reconstruct the missing parts explicitly and mark them as assumptions.

Capture:

- target venue or level if provided: A会, B会, journal, workshop, thesis
- field and task
- paper stage: idea, early draft, full draft, rejected paper, post-review revision, camera-ready
- target output: summary, critique, revision plan, edited text, checklist

### 2. Build the Paper Map

Before critique, write a compact map:

- **Main claim**: the one sentence reviewers must believe.
- **Contribution type**: problem definition, mechanism explanation, method improvement, benchmark, dataset, system, theory, empirical study.
- **Core insight**: the specific failure mechanism or variable the paper exposes.
- **Novelty source**: clarified failure mode, controllable variable, new setting that reveals old methods’ weakness, or method mechanism.
- **Evidence chain**: which experiments support which claims.
- **Boundary**: where the claim applies and where it does not.
- **Closest prior work**: what it solves and what it does not answer.

If the main claim cannot be written cleanly, flag this as the first problem.

### 3. Diagnose the Lifecycle

Audit the paper in this order:

1. **选题**: Is the problem important, essential, variable-driven, testable, and bounded?
2. **Insight**: Does the paper explain a concrete failure mechanism rather than repeat domain common sense?
3. **Novelty**: Does novelty survive after removing the method name and pipeline diagram? Is there one core contribution, or five co-equal modules diluting it?
4. **Idea**: Does the paper have a single claim-experiment spine?
5. **Method**: Does each module correspond to a failure mode, variable, and testable prediction, with enough implementation detail to reproduce?
6. **Theory** (if any propositions/bounds/guarantees): Are assumptions stated and realistic, does the theorem match what the method does, and is the claimed quantity measured directly rather than inferred from a score drop?
7. **Experiments**: Do experiments prove the problem, test the core setting, exclude alternative explanations, include oracle/boundary/subgroup tests, and explain cases?
8. **Statistics & reproducibility**: Are seeds, variance, significance, and matched compute reported? Is any result "too good" (contamination/leakage/shortcut)? Could an independent group rebuild it?
9. **Figures & tables**: Is there an honest page-1 figure that makes the problem undeniable? Is the claimed setting the highlighted comparison? Are captions self-contained?
10. **Writing**: Do abstract, introduction, related work, method, experiments, and conclusion guide the reviewer through the claim, with consistent notation and justified claim-strength wording?
11. **Naming, positioning & compliance**: Do the title and method name fit the contribution without overclaiming? Is concurrent work positioned? Are ethics/data-license/reproducibility-checklist and (for blind venues) anonymity requirements met?

Re-weight these by paper type (method, benchmark, dataset, theory, empirical, survey, system) — see `references/review_revision_skill.md` Section 13.

Read `references/review_revision_skill.md` for the detailed questions and section templates.

### 4. Think Like a Reviewer

Convert critique into reviewer objections. Prefer concrete objections over general comments.

Good objections:

- "The method may improve performance because the retriever changed, not because evidence composition improved."
- "The paper claims model-agnostic behavior but evaluates only one backbone."
- "The related work hides the closest self-checking method, making novelty look stronger than it is."
- "The main table tests ordinary QA, but the claimed contribution is evidence conflict handling."

Weak objections:

- "Need more experiments."
- "Writing should be improved."
- "Novelty is unclear."

For each objection, name the missing evidence or exact rewrite needed.

### 5. Plan Revisions by Priority

Use this priority system:

- **P0 论文主线问题**: main claim unclear, novelty collapsed or diluted across co-equal modules, claim unsupported, wrong experiment setting, missing closest prior work, broken theory assumption.
- **P1 证据链问题**: weak ablation, missing oracle test, no failure analysis, no boundary or subgroup test, uncontrolled variables, no variance/significance, unexplained "too good" result.
- **P2 写作表达问题**: abstract vague, intro starts with generic background, related work is a literature list, method reads like module documentation, conclusion repeats the abstract, figure/table problems, notation drift, overclaiming wording.

Revision plans must include:

- issue
- why it matters for acceptance
- exact section/table/figure affected
- concrete edit or experiment
- expected reviewer concern it resolves

### 6. Make Detailed Edits

When asked to modify text, preserve the paper’s real technical contribution. Do not inflate claims to sound stronger.

For each rewritten section:

- make the main claim explicit
- connect method choices to failure mechanisms
- align experiments with claims
- reduce generic background
- expose boundaries rather than hiding them
- avoid unsupported "general", "robust", "universal", or "model-agnostic" wording unless evidence supports it

For large documents, edit one section at a time and keep a change log.

### 7. Final Checklist

End review-revision work with a checklist unless the user asks only for a narrow task.

Use statuses:

- **Pass**: ready
- **Risk**: acceptable but reviewers may question it
- **Blocker**: must fix before submission
- **Unknown**: cannot judge from provided material

Checklist categories:

- problem and motivation
- insight and novelty
- claim scope
- related work honesty
- method-mechanism alignment
- theory soundness and assumption realism (if any)
- experiment evidence chain
- ablation and alternative explanations
- oracle, stress, and boundary tests
- statistical rigor and reproducibility
- figures and tables
- abstract, introduction, related work, conclusion
- title, naming, and positioning
- ethics, compliance, and responsible-research requirements
- reproducibility and limitations
- final reviewer-risk summary

## Output Style

Be direct, specific, and diagnostic. Write like a senior researcher doing a serious paper meeting.

Avoid generic praise. If the paper is weak, say where and why. If it is promising, name the exact lever that can make it stronger.

Prefer tables for audits and revision plans. Prefer rewritten paragraphs for writing tasks. Prefer claim-experiment matrices for experiment planning.
