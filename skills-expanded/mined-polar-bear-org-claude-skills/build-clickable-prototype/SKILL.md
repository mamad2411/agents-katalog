---
name: build-clickable-prototype
description: Builds a clickable prototype in Claude Design screen by screen from your spec, with two or three structurally different layouts, every screen in its empty, error and loading state, sample content, a visible prototype label and a build record. Use for "run build-clickable-prototype", "build a clickable prototype", "prototype this spec in Claude Design", "turn my spec into screens", "give me layout options", "show the empty and error states", "something a user can click through", part of the Claude for Product Builders Pack by 90n.
---

# Clickable Prototype

## When To Use
You have a week, a spec and no engineer, and you need something a user can click through. Use this once the requirements are numbered. It answers: which screens exist, which requirement each one serves, and what was decided on the way?

## When Not To Use
Not for setting the pass line (use Prototype Test Card), not for what the prototype cannot prove (use Prototype vs Production Note), and not for the design system import (use Design System Brief). If the belief can only be tested with real behaviour behind the screens, use First Working Version.

## Inputs
- The spec with numbered requirements, and the screen list or flow if you have one
- The sample content to show on screen, and whether the design system is imported or the look stays rough on purpose
If you have none of this, I start from one sentence on the task a user must complete and mark the output as a first draft.

## Approach
The method follows Anthropic's own guidance on Claude Design for prototypes (Anthropic Academy tutorial, https://academy.claude.com/tutorials/using-claude-design-for-prototypes-and-ux; help page, https://support.claude.com/en/articles/14604416-get-started-with-claude-design). Claude Design makes interactive prototypes from a conversation. The judgment is in what you ask for before anyone sees it. The most common gap is a prototype where only the happy path is drawn: the first tester has no data yet, lands on a blank screen, and the session is over.

## Workflow
1. I ask up to three questions. Which spec and which requirement ids are in this build? What is the full journey, from entry to done? What sample content may appear on screen?
2. I walk Claude Design through the whole journey first, then build one screen at a time, so each is made in context. Every screen carries the requirement id it serves; a screen with no id is cut or sent back to the spec.
3. I ask for two or three approaches and set them side by side. They must differ in structure (steps versus one page, list versus board), not in colour. You pick, and I write the reason in the chat.
4. Before anyone sees it, I ask how each screen handles its empty, error and loading state, and one case with a very different data volume. Missing states are built or listed.
5. I name screens and components clearly as we go and record each layout decision with its reason in the chat, because names and reasoning carry into the hand-off. Before any large change, I ask Claude to save the current work and confirm where it is saved. Claude Design has no version history, so this is the only way back.
6. I add a visible "prototype" label in the wording you choose, check every screen for sample content only, then write the build record. Whether the label shows on every screen a reader can reach is checked once, in Access and Sharing Check. Designs start private; sharing has three levels (view, comment, edit) and stays off until Pre-Share Sign-Off carries a named person's yes.

## Output Format
```markdown
# Clickable Prototype Build Record
Spec: [name, date] · Built in: Claude Design · Sharing: [private / view / comment / edit] · Label wording: [text]
## Screens
| Screen (name) | Requirement id | Empty | Error | Loading |
|---|---|---|---|---|
| [name] | [R-n] | [built / listed] | [built / listed] | [built / listed] |
Data volume case tried: [case, and what the screen did]
## Layout options
| Option | Structure | Kept or dropped | Reason |
|---|---|---|---|
| [A] | [steps / one page / other] | [kept / dropped] | [reason] |
## Decisions written in the chat
| Decision | Reason | Screen |
|---|---|---|
| [decision] | [reason] | [screen] |
## Saved copies
| Before which change | Where it is saved | Date |
|---|---|---|
| [change] | [location] | [date] |
## Sample content
Source: [sample data plan / written for this build] · Real names, emails or account details on any screen: [none / removed on date]
## Decision
[Builder role] decides by [date] which layout goes forward; the person named on the Pre-Share Sign-Off decides whether any link goes out.
```

## Done When
- Every screen cites a requirement id, and every in-scope requirement has a screen
- Two or three layouts exist and differ in structure; every screen shows its empty, error and loading state, or the gap is listed
- A saved copy exists from before the last large change, and you know where it is

## Quality Bar
- The record describes the build only: no pass line, no test brief and no list of what it does not prove.
- No real names, emails or account details on any screen, including in screenshots pasted for reference.
- It is called a prototype everywhere, in the label, the file name and the chat.
- Sample content only, a prototype label added during the build, and no link goes out before the Pre-Share Sign-Off says yes.

## Next
Run build-heuristic-review (Prototype Heuristic Review) to find the obvious problems before a user does.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
