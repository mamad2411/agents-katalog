---
name: Ask_Why
description: Use this skill for vague, high-rework planning work that needs iterative human decisions, such as product design, research planning, technical strategy, PRDs, workflow design, agent design, or skill design. Run concise P2A decision rounds, challenge assumptions early, record decisions in PLAN.md, DECISIONS.md, and OPEN_QUESTIONS.md, then produce FINAL_PLAN.md when converged. Do not use for simple factual Q&A, routine coding fixes, direct execution, translation, writing polish, or one-shot requests.
---

# Ask Why

Use this skill to turn an ambiguous request into a traceable planning conversation. Keep the user in charge of direction-changing choices, make tradeoffs explicit, and preserve the reasoning in durable state files.

## Cache Strategy

- Keep `SKILL.md` as the stable dispatcher. Long structural templates live in `references/formats.md`.
- Read `references/formats.md` only after the Entry Gate passes or when artifact formats are needed.
- Use the same localized labels, heading order, and file names within each session.
- Put stable content before volatile content in artifacts: goal, boundaries, decisions, then open questions.
- Prefer short state summaries over pasting full prior plans, transcripts, or file contents into chat.
- Append decisions; do not rewrite confirmed history unless correcting an error.
- Avoid timestamps, environment dumps, long examples, and local file listings unless they change the plan.

## Entry Gate

Enter Ask Why mode only when all are true:

- The task is vague, open-ended, or complex.
- User preference will materially change the result.
- Multiple reasonable directions exist.
- Early wrong choices would cause substantial rework.
- The user appears willing to co-design through questions and decisions.

If any condition is false, briefly say why the workflow is not needed and handle the request directly.

## Primary Language Contract

- At the moment this skill is invoked, determine the primary language of the user's triggering prompt before producing Ask Why output.
- Use that initial primary language for every user-facing interaction and maintained artifact in the session, including round prefaces, decision questions, option labels, recommendations, summaries, `PLAN.md`, `DECISIONS.md`, `OPEN_QUESTIONS.md`, and `FINAL_PLAN.md`.
- If the triggering prompt mixes languages, choose the dominant natural language by meaningful user-written content and intent-bearing phrasing. If no dominant language can be determined, ask one brief language-selection question before continuing.
- Keep filenames, code identifiers, API names, product names, quoted user text, and other proper nouns in their original form when translation would reduce precision.
- Do not switch the session language just because the user writes a later message in another language. Switch only when the user explicitly asks to change the session language.
- When using templates from `references/formats.md`, translate or localize all headings, bracketed labels, field labels, option labels, helper text, and prose into the session's primary language while preserving the template structure and semantics.

## Operating Rules

- Follow the Primary Language Contract for all interaction, state files, draft plans, and final plans.
- Treat the user as the decision maker. Recommend, challenge, and explain tradeoffs, but do not silently decide key unknowns.
- Ask 3-5 focused questions per round; each question must change the plan, confirm a key assumption, or choose a real tradeoff.
- If files can be written, maintain state in `p2a-session/` unless the user specifies another path.
- If writing is unavailable, maintain the same state inline using the same headings.

## Required State

Maintain these files:

- `PLAN.md`: current version, goal, non-goals, mechanism, workflow, outputs, risks, next phase.
- `DECISIONS.md`: append-only confirmed choices with rationale and plan impact.
- `OPEN_QUESTIONS.md`: unresolved `P0`, `P1`, and `P2` questions.
- `FINAL_PLAN.md`: final deliverable once the direction has converged.

Use the localized structural templates from `references/formats.md` when creating or repairing these files.

## Runbook

1. Read `references/formats.md`.
2. Start with understanding, not a final plan.
3. Create or update the state files.
4. Build an ambiguity map and rank unknowns as `P0`, `P1`, or `P2`.
5. Run decision rounds with 3-5 focused questions.
6. Update state files after every user answer before asking the next round.
7. Challenge strongly in rounds 1-3; converge from round 4 onward.
8. Summarize every 2-3 rounds.
9. Produce a draft plan when all `P0` and most `P1` questions are resolved.
10. Produce `FINAL_PLAN.md` when remaining uncertainty is explicit and non-blocking.

## Ambiguity Map

Classify unknowns with these categories:

- Goal ambiguity
- User or audience ambiguity
- Use-case ambiguity
- Interaction granularity ambiguity
- Platform or environment ambiguity
- Output format ambiguity
- Success criteria ambiguity
- Risk tolerance ambiguity
- Boundary or non-goal ambiguity
- Follow-up execution ambiguity

Use these priorities:

- `P0`: blocks further design.
- `P1`: changes the core plan.
- `P2`: can be assumed temporarily and confirmed later.

## Rounds 1-3

- Include current plan, current ambiguities, and round goal.
- Name at least 2 credible weaknesses in the current framing.
- Offer at least 2 expansion or reframing directions.
- Recommend one option for every key question.
- Do not assume the user's initial framing is automatically correct.
- Do not make final decisions for the user.
- Use the localized structural round and question formats from `references/formats.md`.

## Rounds 4+

- Reduce scope expansion unless a blocking contradiction appears.
- Prioritize unresolved `P0` and `P1` questions.
- Keep asking 3-5 questions per round while questions remain useful.
- If the user introduces no major new direction for 2 consecutive rounds, prepare the draft plan.
- Ask only for decisions that materially change the plan once convergence starts.

## Draft And Final Plans

- Draft plan: produce when all `P0` and most `P1` questions are resolved.
- Final plan: produce when remaining uncertainty is explicit and non-blocking.
- Use the localized draft, final, and stage summary formats from `references/formats.md`.

The final plan must include:

- Task definition and boundaries
- Goals and non-goals
- Key decisions and why they hold
- Constraints and risks
- Execution path
- Non-blocking open questions
- Next actions, including who decides, who executes, and what happens first

## Definition Of Done

The Ask Why session is complete only when:

- The task boundary is clear.
- Direction-changing decisions are resolved and recorded.
- Remaining uncertainty is explicit and non-blocking.
- The final plan is concrete enough for discussion, task breakdown, implementation, or continued collaboration.
- `DECISIONS.md` and `OPEN_QUESTIONS.md` trace the main reasoning.
