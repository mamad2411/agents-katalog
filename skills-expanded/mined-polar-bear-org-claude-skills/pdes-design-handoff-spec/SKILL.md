---
name: pdes-design-handoff-spec
description: Writes a Design Handoff Spec that says which file, page and version is final, puts the behaviour rules beside each screen and runs a ready check before the walkthrough with engineering. Use for "run pdes-design-handoff-spec", "design handoff", "handoff spec", "spec for engineering", "is this ready for engineering", "which design is final", "handoff to developers", "what am I missing before dev", part of the Claude for Product Designers Pack by 90n.
---

# Design Handoff Spec

## When To Use
The file is polished and engineering still cannot tell which design is final or what happens on error. Run it when one feature is about to go to engineering, before the walkthrough. It answers: what exactly is being handed over, what are the rules, and what is still missing?

## When Not To Use
If nobody has worked out the loading, empty and error states yet, run UI States and Edge Cases first; this spec links to that table and never rebuilds it. If the feature needs a component the system lacks, note it here and propose it with Design System Change Record.

## Inputs
- The file structure: pages, frame names and what each page is for (pasted, or read through the optional Figma connector, which reads frames and variables and returns screenshots as text descriptions)
- The states table, the copy and the rules you know, wherever they live today (tickets, chat, your head), plus platforms, who receives the spec and the walkthrough date
If you have none of this, I start from a typed list of screens and mark the output as a first draft.

## Approach
The spec is built around the gaps engineers report in a practitioner's public study of how engineers use design files (2026): they could not tell which version was final, error and empty states were missing, and rules lived in tickets and wikis. It adds the handoff advice in Anthropic's Claude Design tutorial (academy.claude.com/tutorials/using-claude-design-for-prototypes-and-ux): clear component names, documented decisions, and empty, error and loading states. The ready check is a common team convention with no single originator. The failure it prevents: an engineer builds a week of work from a page that was an abandoned exploration, because three pages looked equally finished.

## Workflow
1. Ask three questions: which file, page and version is final and from what date; who receives the spec and when the walkthrough is; what you already know is incomplete, so it is listed as known.
2. Write the "what is final" block first. Each page gets one status word from a fixed list: exploring, in critique, ready, handed off, archived. Only one page is "ready" for a given screen, and version words in page names get flagged.
3. Go screen by screen: how the user gets in, how they get out, what back does. Write each behaviour and business rule beside the screen it applies to, with where it came from. Link the states table.
4. Name the details. Tokens by name, and a raw value is a flag. Motion as duration, easing and trigger, never an adjective. Focus order and control labels. Copy marked final or placeholder, with the owner of the final copy.
5. Write what is out of scope in one paragraph, then the open questions, each with an owner and a date.
6. Run the ready check: every spec item answered present, missing or unclear. "Unclear" means I could not tell from what you shared, so it becomes a question for you. There is no fourth answer such as "weak". Order the gaps by what would block the build first, then suggest a ready call ("ready after items 1 to 3"). You and the engineering lead make it, and the walkthrough happens either way.

## Output Format
```markdown
# Design Handoff Spec
**Feature:** [name] | **Platforms:** [list] | **Receives it:** [role] | **Walkthrough:** [date]
## What is final
| Screen | File and page | Status | Final from | Note |
|---|---|---|---|---|
| [screen] | [file / page] | [exploring / in critique / ready / handed off / archived] | [date or version] | [flag, if any] |
## Screens, rules and details
States: [link to the states table]
| Screen | In, out and back | Rules that apply here, with source | Tokens by name | Motion | Focus order and labels | Copy |
|---|---|---|---|---|---|---|
| [screen] | [entry points, exits, what back does] | [behaviour and business rules; ticket, decision or role] | [names; raw values flagged] | [duration, easing, trigger] | [order, label per control] | [final / placeholder, owner by role] |
## Out of scope and open questions
[One paragraph on what is out of scope.]
| Question | Owner | Answer due |
|---|---|---|
| [question] | [role] | [date] |
## Ready check
| Order | Spec item | Present, missing or unclear | What would close it |
|---|---|---|---|
| [1] | [item] | [answer] | [fix or question] |
## Decision
Suggested ready call: [ready now / ready after items 1 to n]. [Designer] and [engineering lead] decide whether the spec is ready, at or before the walkthrough on [date].
```

## Done When
- One page, and only one, is marked "ready" for every screen in scope
- Every rule sits beside a screen and names where it came from
- Every ready check row carries one of the three answers, the gaps are in blocking order, and every open question has an owner and a date

## Quality Bar
- Gaps name what the handoff lacks, never who forgot it, and no history is kept of who missed what; only what you shared is checked, so "all states exist" with no list reads "unclear"
- Focus order and labels are design intent, not an accessibility check; for legal duties, check with a qualified adviser
- Claude Docs can hold the spec as a document, and the Claude Design handoff bundle for Claude Code is optional and never replaces the walkthrough
- A complete spec is not a tested design; the ready check covers completeness, and engineering owns the build

## Next
Run pdes-design-system-change-record (Design System Change Record) for anything the feature needs that the system lacks.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
