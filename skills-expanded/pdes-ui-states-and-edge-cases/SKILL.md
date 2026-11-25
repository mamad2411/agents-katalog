---
name: pdes-ui-states-and-edge-cases
description: Build a table of screens against nine states plus an edge-case sweep per screen, marking every cell designed, missing or not needed with the reason, and order the gaps by what would block the build first. Use for "run pdes-ui-states-and-edge-cases", "UI states", "edge cases", "empty state check", "what states am I missing", "error and loading states", "states table", "what happens when the list is empty", part of the Claude for Product Designers Pack by 90n.
---

# UI States and Edge Cases

## When To Use
Engineering asks "what happens when the list is empty?" on day three of the build, and the honest answer is that nobody drew it. The file shows each screen once, full of tidy sample content. This skill answers one question: for every screen, which states and edge cases exist, which are missing, and which do you not need?

## When Not To Use
Not for the full handoff. Rules, tokens, motion, focus order and the ready check belong in the Design Handoff Spec, which links to this table. Not for the paths between screens either: if the branches are still unclear, write the User Flow first.

## Inputs
- The list of screens in the flow, by name, and the frames that exist today for each (a typed list is enough)
- What each screen loads, lists or submits
- The smallest viewport you ship and the languages you ship in
- Optional: the Figma connector reads the frame list, which comes back as structure and text descriptions
If you have none of this, I start from the screen names you can type out and mark the output as a first draft with every cell reading "not shown to me".

## Approach
Missing states and edge cases come up as the top gap in a practitioner's public study of how engineers use design files (2026): error, empty and unusual breakpoint states were absent, and engineers filled them in alone. The nine states are common practice with no single originator. The viewport question follows W3C WAI's tip to design for different viewport sizes (w3.org/WAI/tips/designing). The judgement is in "not needed": a states table grows without limit unless you may close a cell with a reason, and a reason is what tells engineering it was a choice.

## Workflow
1. I ask up to three questions: which screens are in scope, which frames exist for each, and the smallest viewport and the languages you ship.
2. I build the table: screens down the side, nine states across (default, loading, empty, error, partial, success, disabled, no permission, offline).
3. Each cell gets one of three answers and nothing else: designed, missing, or not needed with the reason. If you tell me "all states exist" without listing them, the cell reads "not shown to me".
4. Two rules I apply without asking. A screen with a list has an empty state or a written reason. A screen that loads data has loading and error.
5. The edge-case sweep, the same five questions for every screen with content: the longest realistic content, translated text length, the smallest viewport you ship, a slow or failed request, first use and heavy use.
6. I order the missing cells by what would block the build first: states on the main path before rare ones, errors before polish.
7. You decide each gap: design it, mark it not needed with a reason, or take it to engineering as a question.

## Output Format
```markdown
# UI States and Edge Cases
Flow: [flow] · Checked from: [frame list, typed inventory] · Date: [date]
## States table
| Screen | Default | Loading | Empty | Error | Partial | Success | Disabled | No permission | Offline |
|---|---|---|---|---|---|---|---|---|---|
| [screen] | [designed] | [missing] | [not needed, reason] | [missing] | [designed] | [designed] | [not shown to me] | [missing] | [not needed, reason] |
## Edge-case sweep
| Screen | Longest content | Translated length | Smallest viewport | Slow or failed request | First use and heavy use |
|---|---|---|---|---|---|
| [screen] | [designed, missing, not needed] | [answer] | [answer] | [answer] | [answer] |
## Gaps, in build order
| Order | Screen | State or edge case | Why it blocks | Your call |
|---|---|---|---|---|
| [1] | [screen] | [state] | [what engineering cannot build without it] | [design, not needed, ask engineering] |
## Decision
[You] decide which gaps to design and which to close as not needed by [date]. [The engineering lead] confirms the "not needed" reasons that depend on how the system behaves by [date].
```

## Done When
- Every cell holds one of the three answers, or "not shown to me", and every "not needed" has its reason
- Every screen with a list has an empty state or a reason
- Every screen with content went through all five sweep questions
- The gap list is in build order, with your call on each row

## Quality Bar
- Three answers only. No "partly designed" and no "weak": this table checks whether a state exists, never whether the design is good.
- Gaps are stated as what the screens lack, never as what someone forgot.
- I do not design the missing states here. The table says what is absent, and you decide what it looks like.
- Translated length and the smallest viewport are prompts to check with real text and a real device. I measure nothing.
- "Designed" means a frame exists, not that it works; only what you list is checked.

## Next
Run pdes-prototype-brief (Prototype Brief) to decide what a prototype must answer.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
