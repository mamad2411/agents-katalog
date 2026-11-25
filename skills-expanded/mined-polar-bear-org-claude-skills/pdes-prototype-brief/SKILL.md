---
name: pdes-prototype-brief
description: Write a prototype brief with the one question the prototype must answer, the lowest fidelity that answers it, the real and faked parts and a pass line set before anyone sees it. Use for "run pdes-prototype-brief", "prototype brief", "just prototype it", "what is this prototype for", "what should the prototype test", "low fidelity or high fidelity", "test card for a prototype", "what does this prototype prove", part of the Claude for Product Designers Pack by 90n.
---

# Prototype Brief

## When To Use
Someone said "just prototype it" and nobody has said what the prototype is for. You are about to spend two days on something clickable, and you cannot yet name the question it answers, who will look at it or what result would change the design.

## When Not To Use
Not for writing tasks and a moderator script for sessions with people: use Usability Test Plan once this brief exists. If the question can be answered by reading data you already have, skip the prototype and read the data.

## Inputs
- The request as it was said, the design question behind it if you know it, and the flow or screens in question
- Who will see the prototype, by role and date, and what already exists (sketches, a design system, a working product)
If you have none of this, I start from the request in one sentence and mark the output as a first draft.

## Approach
The brief is a Test Card (Strategyzer, 5 Mar 2015, strategyzer.com/library/validate-your-ideas-with-the-test-card) with the fidelity choice from Nielsen Norman Group (UX Prototypes, Low Fidelity vs. High Fidelity, 18 Dec 2016, nngroup.com/articles/ux-prototype-hi-lo-fidelity). One prototype answers one question, at the lowest fidelity that can answer it. NN/g's trade-off decides the rest: rough work is quicker to change and invites more honest reactions, while high fidelity gives realistic behaviour and invites comments on polish. The failure this prevents is the polished prototype shown on Friday, where the room argues about a button colour and the pass line gets written afterwards to fit what happened.

## Workflow
1. I ask up to three questions. What must be true for this design to work, that you do not yet know? Who will see the prototype, and what do you need from them? What would make you change the design?
2. I reduce the answers to one question. If two questions survive, that is two prototypes or one question parked, and you choose which.
3. I write the Test Card as four labelled lines: the hypothesis (what must be true), the test (how you will check it), the measure (what you will observe), the success criteria (what success looks like and the threshold). You set the threshold. The pass line is dated before anyone sees the prototype.
4. I set fidelity on three dimensions, each on its own: interactivity, visuals, content and navigation. For each I propose the lowest level that still answers the question and say why. A question about wording needs real content and almost no visuals; a question about a transition needs the opposite.
5. I list what is real and what is faked, part by part, with how it is faked and who gets told. Faked data is invented, never copied from real accounts. Then the "does not prove" list (performance, accessibility, edge cases, technical feasibility) and the afterlife: thrown away, kept as a reference, or handed to engineering as a reference only.

## Output Format
```markdown
# Prototype Brief
## The one question
[One question the prototype must answer] For [feature or flow], seen by [roles] on [date]. Parked for later: [question, or none]
## Test Card
| Part | For this prototype |
|---|---|
| Hypothesis (what must be true) | [placeholder] |
| Test (how you will check it) | [placeholder] |
| Measure (what you will observe) | [placeholder] |
| Success criteria (pass line, set on [date]) | [threshold you set] |
## Fidelity
| Dimension | Lowest level that answers the question | Why |
|---|---|---|
| Interactivity | [static, click-through, or responds to input] | [placeholder] |
| Visuals | [sketch, wireframe, or styled] | [placeholder] |
| Content and navigation | [placeholder text, realistic invented content, one path or several] | [placeholder] |
## Real and faked
| Part | Real or faked | How it is faked | Who is told |
|---|---|---|---|
| [placeholder] | [placeholder] | [placeholder] | [placeholder] |
## Does not prove, and afterwards
- Does not prove: [placeholder]
- Afterwards: [thrown away, kept as a reference, or handed to engineering as a reference only]
## Decision
[Product manager or design lead, by role] decides whether this prototype is built at this fidelity with this pass line, by [date].
```

## Done When
- There is exactly one question, and a result on either side of the pass line would change what you do
- The pass line carries a date earlier than the first showing, and the threshold is yours
- Each fidelity dimension has its own level and a reason, every faked part is listed, and the "does not prove" list is not empty

## Quality Bar
- No invented thresholds or results; a missing number stays a [placeholder] until you set it
- Fidelity is argued from the question, never from how much time is left or how good it should look
- Real users answer the question; a Claude pass over the prototype is a second opinion on a file
- A prototype answers one question; it is never presented as the product or as proof that the design works.

## Next
Run pdes-claude-design-prototype (Claude Design Prototype Plan) to plan the build of the prototype.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
