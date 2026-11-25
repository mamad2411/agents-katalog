---
name: pdes-claude-design-prototype
description: Plan a Claude Design prototype with the written brief to give it, the design system and look to specify, three or more directions to ask for and remix, and the copies to save at each milestone. Use for "run pdes-claude-design-prototype", "claude design prototype", "plan a prototype in claude design", "clickable prototype this afternoon", "my prototype looks generic", "what do I tell claude design", "prompt for a prototype", "three design directions", part of the Claude for Product Designers Pack by 90n.
---

# Claude Design Prototype Plan

## When To Use
You want a clickable prototype this afternoon and the first result looks like everyone else's. You typed one line, got a tidy screen with a default typeface and a row of cards, and now you are nudging it prompt by prompt with nothing to steer by. This plan answers what to give Claude Design before you ask, and what to do by hand after.

## When Not To Use
If nobody has said what the prototype must answer, run Prototype Brief first. If the directions are options a stakeholder has to choose between, use Design Options Trade-off Table; the directions here are visual explorations, never a decision record.

## Inputs
- The question the prototype answers and who will see it (the prototype brief, if you have one), with the flow or screens and the content each needs
- The look: typefaces, colours, references you admire and why
- Your design system and whether it is imported into Claude Design; the codebase, if real components matter
If you have none of this, I start from the flow in a few sentences, pasted into any chat, and mark the output as a first draft.

## Approach
The plan follows Anthropic's own guidance: the Claude Academy tutorial Using Claude Design for prototypes and UX (academy.claude.com/tutorials/using-claude-design-for-prototypes-and-ux), the help article Get started with Claude Design (support.claude.com/en/articles/14604416-get-started-with-claude-design) and Anthropic's published designer workflow of 24 Jul 2026. Claude Design builds a first version on a canvas beside the chat, and it is only as specific as what it was given. Plan before prompting, say what the look is, ask for directions that differ, then finish by hand. The failure this prevents: three hours of nudging one default layout, no saved copy, and a colleague's edit that wipes the version you liked.

## Workflow
1. I ask up to three questions. What must the prototype answer, and for whom? What design system and codebase exist, and are they imported? What should it look like, and which references say so?
2. I write the brief for Claude Design in four parts: goal, layout, content, audience. Content is realistic and invented, with no real customer names or accounts.
3. I list the context to link (the imported design system, and the codebase where real components matter) and state the look in plain terms: fonts, colours or a moodboard, so the result does not fall back on a default.
4. I draft the request for three or more directions that differ in structure (navigation, hierarchy, the order of the task), and name how each one differs. Three colourways of one layout count as one direction. Then a remix note: which parts you would carry across, left blank for you to fill after you have seen them.
5. I list what you finish by hand on the canvas: comments on a single element, direct text edits, drag, resize and align. Choosing the direction is on that list, and it is yours.
6. I set milestones and plan around the limits the help page states. There is no version history yet, so you export a copy (ZIP, PDF, PPTX or standalone HTML) at each milestone. Multi-person editing may not work reliably, so one editor at a time. Very large codebases lag, so link only the part you need. A design starts private and the owner sets view, comment or edit; the handoff bundle for Claude Code is optional, and engineering owns the build.

## Output Format
```markdown
# Claude Design Prototype Plan
## Brief, context and look to give Claude Design
| Part | What to write, link or state |
|---|---|
| Goal | [the one question this prototype answers, for which flow] |
| Layout | [placeholder] |
| Content | [realistic invented content; no real names or accounts] |
| Audience | [placeholder] |
| Design system | [imported system, or what is missing] |
| Codebase | [the part that holds the real components, or not needed] |
| Type, colour, references | [fonts, colours, moodboard and why] |
## Directions to ask for
| Direction | How it differs in structure | Parts to remix |
|---|---|---|
| [A] | [placeholder] | [filled in after you see it] |
| [B] | [placeholder] | [placeholder] |
| [C] | [placeholder] | [placeholder] |
## By hand, saved copies and limits
- By hand on the canvas: [element or text to fix by hand]
- Saved copies: at [milestone], export as [ZIP, PDF, PPTX or standalone HTML] to [place]
- Limits planned around: [no version history yet; one editor at a time; codebase size]
## Decision
[Designer, by role] chooses the direction to take forward by [date]; [engineering lead] decides whether any of it is used as a reference for the build.
```

## Done When
- The brief has all four parts and could be pasted into Claude Design as it stands
- The look is stated in fonts, colours or references, with nothing left as "modern and clean"
- At least three directions differ in structure, and every milestone has an export format and a place the copy is stored

## Quality Bar
- Only what Anthropic's pages describe is promised; no export to other design tools is assumed
- Invented content only; no real customer names, accounts or data go into the prototype
- Nothing produced here is described as tested with users or checked for accessibility
- What Claude Design produces is a prototype for ideas and buy-in; you choose the direction and engineering owns what ships.

## Next
Run pdes-prototype-share-check (Prototype Share Check) before anyone outside the team sees it.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
