---
name: build-first-working-version
description: Plans the first working version of a prototype as a First Working Version Build Plan with the one flow that must really work end to end, the parts that stay faked and labelled, small build steps each with a check you can see on screen, a save point after every working step and a stop rule. Use for "run build-first-working-version", "Claude built forty files and I cannot tell what works", "make one flow really work", "split the build into small steps", "what should stay faked", "when do I stop building", "turn my design into a working prototype", part of the Claude for Product Builders Pack by 90n.
---

# First Working Version

## When To Use
You asked for the whole app at once, got forty files, and cannot tell what works. Or you are about to. Run this before the first build prompt in Claude Code. It answers: which one flow has to work for real, what stays faked, and how will you know after each step that it still works?

## When Not To Use
If the prototype folder and its rules do not exist yet, run Claude Code Setup first. If a step has already failed and you are staring at a message, that is Error Fix Log; this skill is the plan of steps, not the response to a broken one.

## Inputs
- The belief on your test card
- The spec with its requirement ids, or the hand-off from your design
- Your time box, and whether an engineer has set up version control in the folder
If you have none of this, I start from a one-line description of the flow and mark the output as a first draft.

## Approach
The method is a thin end-to-end slice, an engineering convention: build one path from the first screen to done, thinly, before widening anything. It is paired with the hand-off from Claude Design to Claude Code (support.claude.com/en/articles/14604416-get-started-with-claude-design) and with checkpoints in Claude Code (code.claude.com/docs/en/checkpointing). Small steps matter more for you than for an engineer, because a check on screen is the only test you can read. The failure it prevents: a wide, impressive build where every screen renders and no task can be completed.

## Workflow
1. Ask up to three questions: which belief are you testing, what are you starting from (the design hand-off or the spec), and what time box have you set?
2. Pick the one flow the belief needs, from first screen to done. The usual mistake is picking the easy flow. If the belief is about whether people finish a task, the flow is that task, including its awkward middle.
3. List everything else as faked, and say how: a fixed sample response, a static screen, a button that goes nowhere. Each faked part carries a label on screen, so nobody watching takes it for working.
4. Choose the start. Claude Design can hand a design to Claude Code, locally or on the web; otherwise start from the spec. Either way the requirement ids come with you.
5. Split the build into small steps, one step per prompt so each has its own checkpoint. Each step has one check you can see on screen, tied to a requirement id: what you click and what you should then see. A step with no visible check is too big or too hidden; split it.
6. Save after every step that works: a commit if an engineer has set up version control, otherwise a dated copy of the folder. Checkpoints are for quick recovery inside a session; the docs call them "Not a replacement for version control".
7. Apply the stop rule. When the time box you set runs out, the build stops and what works is written down, step by step. An unfinished flow is recorded as unfinished.

## Output Format
```markdown
# First Working Version Build Plan
Prototype: [name] | Belief tested: [from the test card] | Starts from: [design hand-off / spec] | Time box: [set by builder], ends [date]
## The one flow
From [first screen] to [done]. Why this flow: [what the belief needs it to show].
## Faked and labelled
| Part | How it is faked | Label shown on screen |
|---|---|---|
| [part] | [fixed sample response / static screen] | [wording of the label] |
## Steps
| Step | What Claude builds | Check I can see on screen | Requirement | Works? | Save point |
|---|---|---|---|---|---|
| [1] | [one thing] | [what I click, what I then see] | [R1] | [yes / no / not run] | [commit or dated folder copy] |
## Stop rule
The build stops on [date]. Working: [steps]. Not working: [steps]. Not started: [steps].
## Decision
[Builder, by role] decides by [date] whether the flow goes on to the checks that end in Pre-Share Sign-Off or gets one more time box; [engineering lead, by role] decides what, if anything, is kept.
```

## Done When
- One flow is named from first screen to done, and it is the flow the belief needs
- Every step has one on-screen check and a requirement id
- Every faked part is listed with its label, and a save point exists for each step marked as working
- The stop date was written before the first step

## Quality Bar
- "Works" means you saw the check pass on screen, not that Claude said so.
- One step per prompt. Two steps in one prompt is how you lose track of which one broke.
- Sample data only, and no hosting, sign-in or payment step in this plan; those are engineering work.
- Widening comes after the thin flow is complete, never during it.
- It works on one flow with sample data: that makes it a working prototype, never production, and engineers decide what is kept.

## Next
Run build-error-fix-log (Error Fix Log) for the first step that breaks.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
