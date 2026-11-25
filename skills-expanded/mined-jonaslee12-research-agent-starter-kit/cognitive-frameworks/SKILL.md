---
name: cognitive-frameworks
description: Use before major research proposals, manuscripts, reports, methodology sections, literature reviews, grants, or stakeholder-facing academic/professional writing to make claims, gaps, warrants, boundaries, and section rhetoric explicit before drafting.
---

# Cognitive Frameworks

Use this skill before substantial research writing or revision when the output needs an argument, not just polished wording.

## Trigger

Use for:

- proposal, manuscript, report, grant, protocol, thesis, dissertation, or chapter planning;
- literature review, methodology, introduction, rationale, discussion, recommendation, or implications sections;
- supervisor, PI, client, reviewer, examiner, funder, or stakeholder-facing drafts;
- research-gap, problem-statement, contribution, or design-rationale decisions;
- major revisions where the current text feels shallow, unfocused, or under-justified.

Do not use for short factual answers, file listing, simple formatting, or routine maintenance notes unless the user asks for deeper reasoning.

## Required Inputs

Before using this skill, check:

1. `AGENTS.md`
2. `PROJECT_AGENT_PREFERENCES.md`
3. `RESEARCH_PROJECT_BRIEF.md` if present, otherwise `RESEARCH_PROJECT_BRIEF_TEMPLATE.md`
4. relevant source files or source notes
5. `knowledge-base/SOURCE_READINESS_MATRIX.md` for citation-heavy work

If project facts or sources are missing, mark them `TO CONFIRM`.

## Core Output

Create a short cognitive protocol before drafting:

```text
Cognitive protocol:
- Section type:
- Main claim:
- Gap/problem type:
- Evidence base:
- Warrant:
- Boundary:
- Rhetorical plan:
- Risks:
- Next drafting move:
```

The protocol can be a temporary note, a checkpoint file, or a section inside a planning document.

Use `research-wiki/CLAIM_LEDGER_LITE_PROTOCOL.md` when formal claims, stakeholder-facing claims, source-readiness upgrades, or citation claim-support audits need stable `claim_id` boundaries. `cognitive-frameworks` prepares candidate claims, warrants, limitations, and concept contracts; `dissertation-citation-audit` owns the ledger check.

## Gap / Problem Type Taxonomy

Use one or more of these allowed categories. Do not write a vague gap statement without naming the type.

| Type | Use When | Signal |
|---|---|---|
| Conceptual gap | Existing concepts do not clearly explain the target issue | terms are broad, contested, or under-specified |
| Empirical/context gap | A population, site, setting, or case is under-examined | evidence exists elsewhere but not in this context |
| Methodological gap | Existing studies rely on limited methods or miss a useful form of evidence | surveys only, no interviews, weak design input, limited triangulation |
| Implementation/adoption boundary | Existing work discusses value but not practical conditions for use | barriers, acceptability, workload, trust, adoption, governance |
| Ethics/governance gap | Existing work under-specifies risk, accountability, privacy, autonomy, or consent | compliance or responsible-use assumptions are unclear |
| Policy/practice gap | Evidence does not translate cleanly into guidance for practitioners or organisations | unclear actions, roles, or implementation pathway |
| Evidence synthesis gap | The issue is fragmented across literature areas | relevant work exists but is not connected for this project |
| Technical/design gap | A tool, system, workflow, or interface requirement is under-specified | design boundaries, feature requirements, failure modes |

If none fits, write `Gap/problem type: TO CONFIRM` and explain what source review is needed.

## Claim-Evidence-Warrant Map

Every important claim should have:

- Claim: the sentence or judgement the document needs to defend.
- Evidence: source material, data, policy, user requirement, or project fact that supports the claim.
- Warrant: the reasoning that explains why the evidence supports the claim.
- Boundary: what the evidence does not prove.

Weak warrant examples:

- "This is supported by the literature."
- "This is important."
- "This shows the gap."

Stronger warrant pattern:

```text
Because [evidence] shows [specific condition], it is reasonable to claim [claim] within [boundary].
```

## Warrant Quality Test

Before drafting, test the warrant:

1. Does the evidence actually lead to the claim, or only relate to the topic?
2. What assumption connects the evidence to the claim?
3. What counterexample would weaken this claim?
4. Is the claim narrower than the evidence can support?
5. Does the sentence need a source, a caveat, or `TO CONFIRM`?

If the warrant fails, narrow the claim or return to source review.

## Section Rhetorical Moves

Choose a section type and follow the relevant moves in:

- `references/research_rhetorical_moves.md`
- `references/argumentation_reasoning_framework.md`

Minimum requirement:

- Introduction/rationale: establish issue, locate literature, define gap/problem type, state project response.
- Literature review: group sources by argument job, compare positions, identify usable evidence and boundaries.
- Methodology/methods: connect research question, data, method, ethics/compliance, and limitations.
- Findings/results: separate observed evidence from interpretation.
- Discussion/implications: show what the findings mean, where they apply, and what remains limited.
- Proposal/grant/report recommendation: show need, feasible action, evidence basis, risk, and decision point.

## Boundary

This skill improves reasoning discipline. It does not:

- verify citations;
- prove sources support claims;
- replace source-first checks;
- replace ethics, legal, journal, funder, client, or institutional review;
- guarantee assessment, publication, funding, or client acceptance.

After this skill, use `academic-self-review-loop` for formal drafts, then style and document-quality gates.
