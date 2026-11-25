---
name: strat-product-strategy-doc
description: Writes the Product Strategy document a leader signs, two pages at most, starting with a line-by-line check of the current strategy, then a diagnosis with evidence and confidence, a guiding policy with the options it rules out, three to five coherent actions, the top "we will not" lines and the bets. Use for "run strat-product-strategy-doc", "write our product strategy", "we have no strategy to say no against", "everything is high priority", "check our strategy for fluff", "is this a strategy or a list of goals", "turn our goals into a strategy", "strategy document for leadership to sign", part of the Claude Guide for Product Strategy Pack by 90n.
---

# Product Strategy Document

## When To Use
Nothing is written down to say no against. Every request looks equally reasonable, the "strategy" is a list of goals and features, and the roadmap follows whoever asked last. Use this to write the argument a leader reads and signs. It answers: what is the hard problem in front of us, what approach do we take to it, and what does that approach rule out?

## When Not To Use
If no direction has been chosen yet, run Strategic Options first: this document argues for a choice, it does not make one. If the strategy is signed and teams still cannot use it, One-Page Strategy is the cut for them. If it has to win a room, use Product Strategy Deck.

## Inputs
- The current strategy or priority list, word for word as leadership states it
- The evidence: customer interviews, usage data, win and loss notes, market sources, constraints on team, budget and technology
- The option set, the not-doing list and the bet table, if they exist, and who signs the strategy and by when
If you have none of this, I start from the current priority list, treat the diagnosis as a hypothesis and mark the output as a first draft.

## Approach
The strategy kernel and the marks of bad strategy come from Richard Rumelt's 2011 article "The perils of bad strategy": a diagnosis of the critical challenge, a guiding policy for dealing with it, and coherent actions that carry it out. Most product strategies skip the diagnosis and jump to goals, so I read what you have today before drafting anything. The failure this prevents is the page with twelve priorities and no named obstacle, which rules nothing out and changes nobody's Monday. In Claude Docs the draft is one shared document. It works the same in a plain chat.

## Workflow
1. Ask at most three questions: who signs and by when, the one or two obstacles as you see them, and what evidence sits behind that view. Then, before any drafting, check the current strategy. Quote each line and tag it: fluff (sounds strategic, says little), a goal presented as strategy, no named challenge, a list of everything, or holds. Say what is missing, not only what is wrong. If there is no current strategy, I say so and move on.
2. Write the diagnosis: one or two critical challenges in plain words, each claim tied to a source you gave, with a confidence mark. Thin evidence is stated as thin, never smoothed.
3. Write the guiding policy in two or three sentences. Test it by naming at least two reasonable options it rules out, taken from your option set. If it rules nothing out, it is not a policy yet, and I say which sentence fails.
4. Write three to five coherent actions. For each: how it serves the policy and which other action it depends on. Flag any action that does not follow from the policy or pulls against another.
5. Quote the top three to five "we will not" lines from your not-doing list, each with its reason, then "how we will know": the bets with the signals that show the policy is working. Targets belong to the quarter's OKRs, not here.
6. Cut to two pages. Put one line at the top ("[challenge], so we will [policy]"), the owner by name and role, and the sign-by date.

## Output Format
```markdown
# Product Strategy
**In one line:** [challenge], so we will [policy]. | **Owner:** [name, role] | **Sign by:** [date]
## Check of the current strategy
- "[quoted line]": [fluff / goal as strategy / no named challenge / list of everything / holds]; missing: [what a strategy would say here]
## Diagnosis
| Critical challenge | Evidence | Source | Confidence |
|---|---|---|---|
| [challenge] | [fact, base, period] | [interviews, data, document] | [high / medium / low] |
## Guiding policy
[Two or three sentences.] Rules out: [option], [option].
## Coherent actions
| Action | How it serves the policy | Depends on | Owning team (role) |
|---|---|---|---|
| [action] | [link to the policy] | [other action] | [role] |
## We will not
- We will not [request, segment or bet], because [reason from the policy]
## How we will know
- [bet]: [signal, an early behaviour and not a target], read in [report, how often] (Source: [source] / assumption)
## Decision
[Role of the leader who owns the strategy] signs the diagnosis, the policy and the "we will not" lines by [date], and names who shares it with [audience].
```

## Done When
- Every line of the current strategy is quoted and tagged, or its absence is stated
- The diagnosis names a challenge, not a goal, with a source per claim
- The policy rules out at least two named options
- Every action traces to the policy and to at least one other action

## Quality Bar
- A revenue or growth target never passes as strategy on its own
- Two pages at most from diagnosis to decision; the check is a working note in front of it
- The check quotes lines as text and never names or judges who wrote them
- Claude drafts from your diagnosis and evidence; leadership owns and signs the choices, and every market claim carries a source or "unverified".

## Next
Run strat-one-page-strategy (One-Page Strategy) to cut the signed strategy to the page teams use to say no.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
