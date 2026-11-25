---
name: build-routine-skill
description: Turns the steps you repeat for every new idea into your own custom Claude skill, producing a skill draft with the phrases you really type, a quality bar that carries the pre-share checks, a test on three past cases and a change log. Use for "run build-routine-skill", "turn my prototyping routine into a skill", "make a custom skill from my own steps", "I start every idea from a blank chat", "test my skill on past work", "why does my routine skip the checks", "write my own skill for the next idea", part of the Claude for Product Builders Pack by 90n.
---

# Build Routine Skill

## When To Use
The second idea arrives and you start again from a blank chat. You remember roughly what you did last time, you retype half of it, and the step that gets dropped is the dull one: checking what is safe to share. This answers: which of my steps are fixed, and does a skill made from them do as well as the work I already approved?

## When Not To Use
If what you keep retyping is facts about your product, that is Product Context File, which is always loaded; a skill is a routine that loads when asked for. If you have taken only one idea through, wait: one run is not a routine yet.

## Inputs
- The steps you followed last time, as you really did them, in your own words
- Three past cases you pick: what you pasted in, and the output you approved at the time
- The phrases you type when you want this done
If you have none of this, I start from a plain description of your routine and one past output, and mark the output as a first draft with the test rows blank.

## Approach
Custom skills, as the Anthropic help page "What are skills" describes them (support.claude.com/en/articles/12512176-what-are-skills): folders of instructions, scripts and resources that Claude loads when relevant, which anyone can write in Markdown, with code execution turned on. The test is a small before-and-after on past work, a common practitioner habit. The failure it prevents: a long prompt saved in a new file, never tested, that drops the pre-share checks the first week you are in a hurry.

## Workflow
1. Ask three questions: which phrases you really type when you start a new idea; which three past cases count as good, and what you approved for each; and what the output must never leave out.
2. Split your routine into parts: a name, a description holding your real phrases, what to paste, numbered steps, a bar, a fixed output shape. Anything that changes per idea is something to paste, not a step.
3. Write the bar so the routine cannot skip the checks before sharing: keys, personal data, who can open the link, a named person's yes, and a visible prototype label. These are fixed lines, not reminders.
4. Prepare the three past cases with customer personal data removed first. Run the draft on each and set the result beside the output you approved at the time. Compare on three things: what is missing, what is wrong, and tone. You judge each row; I do not grade my own output.
5. Change one thing per round and log it with the reason. Three changes at once hide which one helped. Untested rows stay blank.
6. Write the install note: upload under Customize > Skills with code execution on; on Team and Enterprise plans an owner may need to allow it. The skill can then be called in a chat or in Claude Code.

## Output Format
```markdown
# Build Routine Skill Draft
## Skill draft
| Part | Content |
|---|---|
| Name and description | [short name; what it produces; the phrases you really type] |
| What to paste | [what changes per idea] |
| Steps | [1. ... 2. ... 3. ...] |
| Bar | [your rules, then the fixed lines below] |
| Output shape | [the headings every output has] |
| Install | [where it was uploaded, code execution on, who allowed it if an owner had to] |
Fixed lines in the bar: keys checked [how]; personal data checked [how]; access checked [how]; yes from [role] before any link goes out; "prototype" label on every screen and every share.
## Before and after on three past cases
| Case | What was pasted (date, personal data removed) | Output you approved | Missing | Wrong | Tone | Your verdict |
|---|---|---|---|---|---|---|
| [1] | [source] | [link] | [what the draft left out] | [what it got wrong] | [match / off] | [better / same / worse] |
## Change log
| Round | One change | Why | Result |
|---|---|---|---|
| [1] | [change] | [reason] | [effect, or blank if not run] |
## Decision
The [builder, by role] accepts the skill for the next idea, or names the one change for the next round, by [date].
```

## Done When
- The description holds phrases you really type, and the output shape is fixed
- The bar carries the three pre-share checks, the named yes and the prototype label
- Three past cases were run and set beside outputs you approved, with personal data removed
- Each round changed one thing and the log says why

## Quality Bar
- "Better" is judged against past outputs you approved, never against Claude's opinion of its own work. No invented test results; a row that was not run stays blank.
- Past cases carry no customer personal data and no key.
- Steps describe how the work is done, never how a person should be rated.
- The skill covers the road up to a prototype; it does not replace real users or the engineer's review.
- The routine carries the pre-share checks and the prototype label; the builder judges the test, not Claude.

## Next
Run build-problem-frame (Problem Frame) to start the next idea from its question, with your routine in hand.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
