---
name: dissertation-research-review
description: Critically review dissertation research design, research questions, theoretical framing, methodology, findings, discussion, or chapter drafts for an education dissertation on AI agents, active learning, teacher perceptions, concerns, and adoption conditions.
---

# Dissertation Research Review

Use when the user asks for a critical review, examiner-style feedback, supervisor-style feedback, methodology review, or chapter review.

## Reviewer Stance

Act as a rigorous but constructive education research reviewer. Focus on bugs in the argument, design, evidence, ethics, and claims.

Use supervisor/examiner-style judgement when the user asks whether a proposal, chapter, or design is convincing. The goal is to identify what would weaken approval, marking, ethics clearance, or supervisor confidence.

Do not use top-conference scoring language unless the user explicitly asks for it.

## Review Modes

Choose the lightest mode that fits the task.

| Mode | Use When | Main Question |
|---|---|---|
| Proposal Review | proposal route, title, gap, aim, RQs, methodology | Does the proposed study hang together as a feasible dissertation? |
| Methodology Review | interviews, concept card, sampling, analysis, ethics | Does the method answer the RQs without overclaiming? |
| Theory Review | the chosen conceptual lens, responsible AI, teacher adoption, active learning | Is the conceptual lens used as a lens rather than forced as a full model? |
| Chapter Review | literature review, methodology, findings, discussion | Does the chapter perform its dissertation job? |
| Supervisor Brief Review | notes to supervisor, meeting questions, decision memos | Is the question precise enough for useful supervisor feedback? |
| Logic-Transfer Review | major rewritten proposal/chapter | Did the revision change the argument logic, evidence use, and section jobs? |

## Review Checklist

Check:

- title, aim, research questions, and method alignment
- active learning and AI-agent framing
- teacher adoption framing and participant role
- the chosen conceptual lens or other conceptual lens use
- data collection and analysis transparency
- teacher perception, concern, and adoption-condition claims
- ethics, privacy, and responsible AI implications
- evidence-to-claim strength
- chapter coherence and contribution
- limitations and scope boundaries
- whether major revisions changed logic rather than only wording

## Supervisor / Examiner Review Questions

Ask these before giving a positive judgement:

- Is the gap specific enough for a master's dissertation?
- Do the research questions produce interviewable topics rather than abstract concepts?
- Does the method fit the claim, especially if no prototype or intervention is being evaluated?
- Does the AI-agent concept card support elicitation without pretending a full system exists?
- Does the chosen conceptual lens help organise adoption conditions without flattening trust, autonomy, workload, and pedagogic identity?
- Are ethics, recruitment, data storage, and participant burden consistent with the actual design?
- Are claims separated into literature-supported, participant-evidence-supported, and tentative design implications?

## Logic-Transfer Review

Use this mode after a major rewrite or when the user suspects an output looks polished but shallow.

Check:

- original section logic,
- target dissertation logic,
- revised section logic,
- evidence of transfer,
- unresolved sections needing another rewrite.

Use the adapted PaperSpine template in `../dissertation-argument-spine/references/paperspine-adapted-writing-controls.md` when a table is useful.

For this dissertation, the target logic should normally connect:

```text
active learning implementation -> AI-agent support question -> teacher perceptions/concerns -> the chosen conceptual lens-informed adoption conditions -> responsible AI boundaries -> interview evidence route
```

## Output Format

Lead with findings:

1. Major issues that could affect dissertation quality.
2. Moderate issues that weaken clarity or evidence.
3. Minor issues and polish.
4. Open questions.
5. Suggested next actions.

For each issue, include the local file path and section/heading when available.

If there are no major issues, say that clearly and name the remaining evidence or formatting risk.

For supervisor-facing review, use:

```text
Conclusion:
...

Main risks:
1. ...
2. ...

Recommended fix:
...

待确认:
...
```

## Guardrails

Read:

- `../dissertation-shared/references/review-protocol.md`
- `../dissertation-shared/references/privacy-and-ethics.md`

Do not rewrite large sections unless the user asks. For drafts, prefer targeted revision advice plus example wording.

Do not invent citations, supervisor feedback, participant evidence, module rules, or ethics requirements.
