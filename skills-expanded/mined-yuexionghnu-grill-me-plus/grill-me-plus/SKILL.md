---
name: grill-me-plus
description: Pressure-test a plan, design, decision, or idea with a branch-aware interview that balances full-map coverage and adaptive follow-ups. Best suited to sustained collaboration between a user and an Agent on large or evolving proposals, where scope, decisions, and unresolved risks must remain coherent across many turns. Use when the user invokes the host-specific command for grill-me-plus, such as $grill-me-plus in Codex, /grill-me-plus in slash-command hosts, or @skill:grill-me-plus in WorkBuddy; asks to be grilled or rigorously questioned; wants a proposal stress-tested; needs configurable follow-up limits; or wants both breadth and depth without getting trapped in one conversational branch.
---

# Grill Me Plus

Interrogate the proposal without implementing it. Balance planned coverage with
answer-driven follow-ups, stop digging as soon as the issue is clear, and keep
the user oriented throughout the session.

## Establish the question map

1. Inspect available files and tools for facts instead of asking the user.
2. Extract the proposal, goal, constraints, stakeholders, and current decisions.
3. Build an internal map of 5-9 main questions spanning the material dimensions,
   such as problem definition, users, scope, assumptions, alternatives, failure
   modes, operations, security, cost, measurement, and reversibility. Adapt the
   dimensions to the topic; do not use a generic checklist blindly.
4. Order main questions by dependency and risk. Assign stable IDs `Q1`, `Q2`,
   and so on. Preserve these IDs for the whole session.
5. Start with a compact coverage map and the visible follow-up policy. Do not
   ask the user to approve the map unless the scope itself is a decision.

## Configure the follow-up ceiling

Maintain a session setting named `follow_up_cap`. It is the maximum number of
follow-ups allowed for one main-question branch across the whole session.

- Honor a cap supplied in the invocation, such as `max follow-ups 4`.
- Allow `0` to disable follow-ups.
- Allow per-branch overrides, such as `Q3 max follow-ups 5`.
- Allow the user to raise or lower either cap at any time.
- If no cap is supplied, select an initial cap from `1-5` based on proposal
  complexity and risk; recommend `3` for an ordinary session.
- State the active policy before the first question:

  `Follow-up policy: session cap 3 per main branch · adaptive stop enabled`

The cap is a ceiling, never a quota. A branch may use any number from `0` to its
configured cap. Never ask another follow-up merely because budget remains.

## Label every question

Ask exactly one question per turn and wait for the answer.

Use one of these labels, translated to the user's language while preserving IDs:

- `[Main Q2/7 · Scope]` for a planned main-chain question.
- `[Follow-up Q2.F1 · from Q2 · 1/4]` for the first follow-up under a cap of four.
- `[Added main Q8 · Operations]` when a new independent dimension is discovered.

Number follow-ups sequentially under their owning main question: `Q2.F1`,
`Q2.F2`, and so on. A follow-up must always identify the main question that owns
the branch and show the used/configured budget.

After the label:

1. State why the question matters in one short sentence.
2. Ask one concrete decision question.
3. Give `Recommended answer:` with a clear recommendation and its main tradeoff.

Do not hide a new dimension inside a follow-up. Promote it to an added main
question so breadth remains visible.

## Apply the clarity gate

Maintain two logical queues:

- **Main queue:** unanswered planned questions in dependency order.
- **Follow-up queue:** unresolved answer-driven branches, each with source,
  count, cap, risk, and whether it blocks later decisions.

After each answer:

1. Record the decision, assumption, disagreement, or missing evidence.
2. Decide whether a material ambiguity remains. A material ambiguity exists
   only when at least one of these is true:
   - two plausible interpretations lead to different recommendations;
   - the answer does not make the requested decision or name a testable rule;
   - an unstated assumption blocks a downstream main question;
   - a high-impact risk is neither mitigated nor explicitly accepted.
3. If no material ambiguity remains, mark the branch clear and return to the
   main queue immediately, even if most of the follow-up budget is unused.
4. If ambiguity remains, ask an immediate follow-up only when resolving it now
   is more valuable than advancing breadth. Otherwise queue it and continue with
   the next main question.
5. Before every follow-up, check the active branch cap. If the cap is reached,
   state the provisional assumption or unresolved risk, park the branch, and
   return to the next main question.
6. After all main questions have been asked once, revisit queued follow-ups in
   descending risk order only while their branch has remaining budget.

Stop asking follow-ups as soon as the decision is clear enough for downstream
reasoning. Also stop when the user accepts the risk, the remaining ambiguity is
immaterial, another main question has higher information value, or the cap is
reached.

When leaving a branch, show the reason:

- `Branch Q2: clear after 1/4 follow-ups; returning to main.`
- `Branch Q2: cap 4/4 reached; risk parked; returning to main.`

Honor commands such as `max follow-ups 4`, `Q3 max 6`, `go deeper on Q3`,
`skip this branch`, or `return to the main line`. Do not silently let one
interesting answer replace the original coverage map.

Every three completed main questions, or every five total questions, include one
short status line before the next question:

`Coverage: 3/7 main · Q2 clear at 1/4 · 1 branch parked`

The status line is not another question.

## Handle interruptions and drift

- If the user asks a side question, answer it briefly, record whether it changes
  the map, and resume using the next explicit question ID.
- If the user gives an unrelated answer, clarify once or park it; do not build an
  unlimited branch around it.
- If a fact is discoverable, investigate it and report the evidence instead of
  consuming an interview turn.
- If the user's answer overturns the premise, revise the map visibly. Keep old
  IDs and mark removed questions as superseded rather than renumbering silently.

## Finish the grill

Do not declare shared understanding merely because one branch is detailed.
Finish only after:

1. Every non-superseded main question has been asked.
2. Critical follow-ups are resolved or explicitly accepted as risks.
3. The user confirms the session can close.

Then summarize:

- coverage by main question;
- follow-ups used versus configured cap for each branch;
- decisions and recommended defaults;
- unresolved risks and parked branches;
- assumptions and evidence still needed;
- the next artifact the user may choose to create.

Do not implement, edit the proposal, or hand off automatically. Wait for explicit
authorization after the grilling session.
