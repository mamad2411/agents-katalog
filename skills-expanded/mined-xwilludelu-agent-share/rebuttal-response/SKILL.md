---
name: rebuttal-response
description: "Plan and draft evidence-based academic rebuttals after reviews arrive. Use for conference, journal, workshop, or grant reviews to triage concerns, rank decision blockers, choose evidence, write AC-facing summaries, draft per-reviewer responses, correct factual misunderstandings, repair tone, and track camera-ready promises. Do not use for pre-submission manuscript critique; use review-revision."
---

# Rebuttal Response

## Overview

Use this skill to turn reviews into an evidence-based rebuttal package. A good rebuttal is not an apology letter and not a debate. It helps the AC and reviewers decide that the core concerns have been clarified, weakened, or resolved.

Use this skill instead of `review-revision` when actual reviews, AC comments, or rebuttal rules are available and the task is to respond. Do not use it for pre-submission manuscript critique, general paper revision, or section rewriting without reviewer comments; use `review-revision` for those tasks.

For detailed tactics, templates, and tone rules, read `references/rebuttal_playbook.md` whenever the task asks for a full rebuttal plan, drafted response, AC summary, new-experiment prioritization, or response polishing.

## Operating Modes

Choose the smallest mode that satisfies the request.

1. **Review triage**: classify every comment by severity, reviewer, factual basis, required evidence, and decision impact.
2. **Rebuttal strategy**: identify which concerns can change the outcome, which reviewers are persuadable, and what the AC needs to see.
3. **Evidence plan**: prioritize new experiments, tables, analyses, revised paragraphs, or factual clarifications under the rebuttal time and page budget.
4. **Draft response**: write AC-facing summaries and reviewer-specific replies with evidence, action, and impact.
5. **Tone repair**: remove defensiveness, false apologies, vague promises, and hostile phrasing.
6. **Final checklist**: verify coverage, traceability, evidence, claim scope, tone, and camera-ready promises.

## Core Principle

Treat the rebuttal as a decision document.

Every paragraph should help answer at least one of these:

- Can this concern still justify rejection?
- Did the authors provide evidence, not only explanation?
- Can the AC cite this response in the meta-review?
- Does the response reduce acceptance risk without overclaiming?

Cut sentences that only express frustration, gratitude, belief, or hope without adding evidence.

## Workflow

### 1. Intake Reviews and Constraints

Read the reviews before drafting. Capture:

- venue and rebuttal rules if provided
- deadline, word/page limit, and whether discussion is public or per-reviewer
- reviewer scores, confidence, and recommendation changes if visible
- paper title, abstract, main claim, and key experiments if provided
- all reviewer concerns, including positive comments

If the manuscript or reviews are incomplete, proceed with explicit assumptions and mark unknowns.

Do not invent new results. Use placeholders such as `[new result here]` when the user has not provided numbers.

### 2. Build the Review Map

Produce a compact triage table:

| ID | Reviewer | Concern | Type | Severity | Factual basis | Evidence needed | Strategy |
| --- | --- | --- | --- | --- | --- | --- | --- |

Use these concern types:

- **Decision blocker**: novelty, missing key baseline, unfair setup, unsupported main claim, major theory gap, invalid evaluation.
- **Misunderstanding**: reviewer missed an existing result, confused notation, misread scope, or attributed a claim the paper does not make.
- **Fixable clarity issue**: writing, notation, table caption, related work positioning, missing explanation.
- **Scope mismatch**: request is useful but tests a different task, assumption, or contribution.
- **Low-value comment**: vague, cosmetic, or unlikely to affect the decision.

### 3. Prioritize by Decision Impact

Do not reply with equal force to every comment.

Use this order:

1. Concerns shared by multiple reviewers.
2. The lowest-score reviewer's main blocker.
3. Concerns from supportive reviewers that might make them withdraw support.
4. AC-relevant concerns even if mentioned once.
5. Small clarity or formatting fixes.

When the paper is borderline, the goal is not to make everyone love it. The goal is to give the AC enough reason to believe the main contribution is sound and the remaining risks are fixable.

### 4. Choose the Response Structure

Prefer a hybrid structure:

1. **AC-facing executive summary**: one short paragraph naming the main concerns and the evidence/actions that address them.
2. **Issue-centered response blocks**: novelty, baselines, experimental setup, mechanism, clarity, scope, etc.
3. **Reviewer traceability**: label each block with the reviewer concerns it addresses, such as `Addresses R1-Q2 and R3-Q1`.
4. **Short closing**: state that the clarifications and new evidence address the concerns. Do not plead for acceptance.

If the venue requires per-reviewer threads, write within each thread but keep the issue-centered logic inside the reply.

### 5. Write Each Response Block

Use this structure:

1. **Concern**: restate the reviewer concern neutrally.
2. **Acknowledge**: accept the importance of the concern, not a false technical fault.
3. **Clarify or evidence**: give facts, new results, prior text locations, or reasoning.
4. **Action**: say exactly what will change in the manuscript.
5. **Impact**: explain why the concern is resolved or reduced.

Do not mechanically write "We agree" when the reviewer conclusion is wrong. Agree with the need for clarity, comparison, or evidence instead.

### 6. Handle Common Concern Types

Use `references/rebuttal_playbook.md` for detailed templates.

Default tactics:

- **Novelty**: rebuild the comparison dimensions: problem, assumption, mechanism, setting, evidence, and boundary.
- **Missing baseline**: add the baseline if feasible; otherwise explain why it tests a different setting and provide alternative evidence for the underlying concern.
- **Experimental fairness**: show matched protocol, compute, data split, hyperparameters, and evaluation metric.
- **Method motivation**: connect design choice -> failure mode -> prediction -> ablation.
- **Clarity**: provide the exact revision, not a vague promise.
- **Factual error**: correct the fact without insulting the reviewer; make the paper easier to read.
- **Scope overreach**: respect the suggestion, restate the paper's claim boundary, and address the underlying concern.
- **Reviewer disagreement**: use positive reviews as evidence of positioning ambiguity, not as a weapon against another reviewer.

### 7. Tone Rules

Be polite to reviewers and firm on facts.

Avoid:

- "The reviewer is wrong."
- "As clearly stated..."
- "The reviewer misunderstood..."
- "This is obvious."
- excessive "We apologize"
- vague "We will improve the paper"
- unsupported "This will be fixed in the final version"

Prefer:

- "We respectfully clarify that..."
- "Our current presentation may not have made this point sufficiently visible."
- "To avoid ambiguity, we will revise..."
- "The key distinction is..."
- "Following the suggestion, we added..."

### 8. Final Checklist

Before finalizing, check:

- Every high-severity concern has a response.
- Every response maps to a reviewer comment.
- The AC can identify the main remaining risk in under one minute.
- New experiments include exact numbers or are marked as placeholders.
- Factual corrections cite table, figure, section, or appendix locations.
- The response does not concede false technical faults.
- All promised camera-ready changes are specific and feasible.
- Tone is calm, evidence-based, and non-hostile.

## Output Style

Be concise, strategic, and evidence-first. Use tables for triage and prioritization. Use polished paragraphs for final rebuttal drafts. Preserve the user's technical claims and never fabricate results, experiments, or reviewer quotes.
