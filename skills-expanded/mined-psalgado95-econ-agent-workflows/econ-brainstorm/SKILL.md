---
name: econ-brainstorm
description: "Clarify an economics research idea before planning the analysis."
---

# Economist Brainstorm Workflow

Where `econ-plan` asks "what are we building?", `econ-brainstorm` asks "what are we trying to learn?". This is the conversation before anyone deserves a plan, built for low-energy moments: the researcher may arrive with fragments and half-formed hunches; the skill carries all the structure. This file is the contract; read `references/scope_memo_template.md` only when writing or refreshing the scope memo.

## Direct invocation contract

Treat the arguments passed with this invocation, or the user's current request, as the topic. If it is empty, ask (blocking) what is on their mind — a fragment is enough to start.

Every session ends with a saved or refreshed scope memo at `docs/plans/YYYY-MM-DD-<slug>-scope.md` (or the repo's plan convention), with `readiness: scoping-only` in its frontmatter, plus a one-line receipt naming the exit ramp taken. The memo is the session state: brainstorms resume across sessions by reading it, so an inline-only summary is not a valid completion.

The research code and data are read-only: no code changes, data mutation, or estimation. Writing the scope memo and an explicitly accepted mock exhibit are the only exceptions. Read project material to resume the discussion or verify an availability claim.

## Questions

Ask one short question at a time using `request_user_input` when available, otherwise ordinary chat; never require a tool the host does not provide. Build on the fragments and answers already supplied rather than restarting the interview. Match the researcher's energy: casual, fragmentary answers are fine — organising them is the skill's job, not theirs. Every question carries the context that makes it answerable — why it matters for the direction, the plausible answers with their tradeoffs — and, where sensible, a suggested default. There is no question budget.

Ask what the researcher is already thinking before offering your own framings — their half-formed version carries context, and an early agent framing is easy to fixate on.

The hidden engine: move the researcher's unknown-knowns into stated form — the population they picture, the comparison they assume, the data they trust, the result they secretly expect — and run a blindspot pass for what they have not considered at all.

## Thinking partner, not stenographer

Support the idea first, but never do pure transcription. Challenge assumptions, propose alternatives, and bring at least one non-obvious angle per session: an inversion, an adjacent design, or "what would make this paper fail?". Record the non-obvious alternative in the memo's identification candidates even when the researcher declines it — a declined alternative is still scope knowledge.

## Verify before claiming

Any claim about data availability, register contents, frequency, coverage, or sample size gets checked locally (read-only) before the conversation builds on it, or is explicitly marked `assumed` in the memo's data requirements. Never let a design firm up on an unverified availability claim.

## Mock exhibits

When a candidate design firms up, offer — do not produce unasked — a mock exhibit as a conversation piece: a mock main-results table (a shell with hypothesised signs, clearly labelled hypothesised, never real numbers), or a design timeline or DAG drawn with a standalone SVG-figure skill (such as `econ-svg-fig`) when installed. Produce it on acceptance. Reacting to an exhibit beats abstract discussion, but a mock exhibit is never evidence and never leaves the brainstorm as a result.

## Workflow

### Stage 0 — Resume or open

If the user names a scope memo, or an obvious recent `-scope.md` matches the topic, read it and resume from its open unknowns rather than restarting. Otherwise open with one question about what is pulling at them.

*Close when:* the starting point is explicit — a fresh idea, or a named memo's open unknowns.

### Stage 1 — Draw out the question

One question at a time: the economic question; the population and unit; the outcome and variation that matter; the decision, policy, or literature the answer speaks to. Surface the unknown-knowns as you go.

*Close when:* the question and the candidate estimand or descriptive object can each be stated in one sentence, or the genuine blocker preventing that is named.

### Stage 2 — Stress the design

Work through identification candidates, data requirements (verify or mark `assumed`), and kill criteria ("what evidence would make you drop this?"). Run the blindspot pass and bring the session's non-obvious angle here if it has not already landed.

*Close when:* at least one identification candidate, the data requirements with `verified`/`assumed` status, and at least one kill criterion are on the table.

### Stage 3 — Exhibits (optional)

Offer a mock exhibit when the design is firm enough to react to; skip freely when the conversation is still upstream of a design.

*Close when:* the exhibit was produced and reacted to, or the offer was declined or skipped.

### Stage 4 — Save and route

Write or refresh the scope memo using `references/scope_memo_template.md`, then take exactly one exit ramp:

- **→ $econ-plan** when the direction is firm: hand over the saved memo as the planning surface;
- **→ parked** when it should not proceed: the memo is saved with its kill criteria and open unknowns, and nothing chains onward;
- **→ blocked evidence** when literature, access, or missing evidence prevents a sound direction: keep the memo as the local user-facing output, name the exact gap, and ask only for the decision or evidence needed to resume.

*Close when:* the memo is saved and the receipt names the exit ramp.

## Graduation

The memo graduates rather than getting orphaned: when the direction is firm, `econ-plan` upgrades the same document in place to a full plan — `readiness: scoping-only` is its trigger. A scope memo can also seed a new project's backbone or `DEFINITIONS.md`.

## Hard stops

- Do not change code, mutate data, or run estimation — availability reads only.
- Do not write the plan; when the direction is firm, route to `econ-plan` on the saved memo.
- Do not give verdicts on external methods, papers, or referee comments — that is outside this skill's scope.
- Do not chain into `econ-work` or run autonomously; the session ends at the exit ramp.
- Do not let the conversation build on an unverified availability claim.
- Do not end a session without the saved scope memo.
