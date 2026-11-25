---
name: pdes-critique-session-brief
description: Prepares a Critique Session Brief with two or three numbered objectives, the stage of the work, the one question for the room about a real user moment, what is out of scope today, a walkthrough cut to the timebox, a framing sentence to read aloud and prompts that turn reactions into questions. Use for "run pdes-critique-session-brief", "prep my crit", "I present at critique on Thursday", "what should I ask the room", "how do I get useful feedback on my design", "design critique brief", "frame my work for crit", "stop getting opinions at crit", part of the Claude for Product Designers Pack by 90n.
---

# Critique Session Brief

## When To Use
You present at crit on Thursday and "thoughts?" will get you opinions. Most critiques are lost in the first sentence, before anyone has seen a screen. It answers: what must this work achieve, what stage is it at, and what one thing do I need the room to tell me?

## When Not To Use
If the people in the room approve or reject the work, build a Design Review Deck: a review asks for a decision, crit asks peers to improve work in progress. If the session has already happened, go straight to Critique Notes to Actions.

## Inputs
- What the work is for: the user, the job it does, the brief or ticket it came from
- The stage it is at, what you already know is unfinished, and how long your slot is
- Optional: the frames you will show, as a list, or read through the Figma connector, which reads frames, variables and components
If you have none of this, I start from the brief alone and mark the output as a first draft.

## Approach
Objective-led critique as Nielsen Norman Group describes it (Design Critiques, Gibbons, 2016): a presenter, critiquers, a facilitator and an optional recorder, with feedback given as questions tied to the objectives of the work. The stage decides what feedback is useful: layout comments on work that is ready to build are late, copy comments on an exploration are early. Claude prepares the question and does not answer it. The failure it prevents is a whole slot spent on the colour of a button you had already said was a placeholder.

## Workflow
1. Ask three questions: what are the two or three objectives this work must meet, which stage is it at (explore, refine or ready to build) and how long is your slot, and what is the one thing you need to know this week?
2. Number the objectives so a comment can point at one. If none can be named, the brief opens with "objectives not yet agreed", and that is the first finding: agree two with whoever asked for the work before the session.
3. State the stage and what it rules in. Explore: direction and alternatives. Refine: does the flow work. Ready to build: gaps and states, not direction.
4. Sharpen the question until it is about a user moment. Example: "Does the order of these three steps make sense for someone who arrives from the reminder email?" is a question; "thoughts?" is an invitation to taste.
5. List what is out of scope today, then cut the walkthrough to the slot: how many screens fit, alternatives or not (yes at explore, rarely at ready to build), prototype or stills. Long explanations are how presenters defend.
6. Draft the framing sentence to read aloud: "This is [artifact] at [stage]. It has to [objective 1] and [objective 2]. Today I need to know [question]. I already know [out of scope] needs work."
7. Write the prompts for the facilitator: "which objective does that touch?", "what would the user do here?", "is that a question or a fix?". If you paste screens and ask what I think, I decline here and finish the brief.

## Output Format
```markdown
# Critique Session Brief
**Work:** [artifact] | **Session:** [date] | **Slot:** [minutes the team gives] | **Roles:** presenter, facilitator, [recorder if any]
## Objectives
1. [objective, or "objectives not yet agreed"]
## Stage
[Explore, refine or ready to build]: [the feedback that is useful at this stage]
## The one question
[About a specific user moment]
## Out of scope today
- [known unfinished part]
## Walkthrough
| Screen or frame | What I say in one line | Minutes |
|---|---|---|
| [frame] | [line] | [n] |
## Framing sentence
"This is [artifact] at [stage]. It has to [objective 1] and [objective 2]. Today I need to know [question]. I already know [out of scope] needs work."
## Prompts for the facilitator
- [prompt that turns a reaction into a question]
## Decision
[Designer] confirms the objectives with [product manager or whoever asked for the work] by [date before the session] and sends the brief to the facilitator.
```

## Done When
- Objectives are numbered, or the gap is stated at the top
- One question only, about a user moment; the walkthrough adds up to the slot and the framing sentence reads aloud in a breath or two

## Quality Bar
- Objectives come from the brief or from you, never made up to fill the list
- No judgment of the screens anywhere in the brief, and out of scope is written down so silence on it is not read as approval
- Roles in the room are named as roles, with no note on who is a strong or weak critic
- Claude prepares the question; the room gives the critique and you decide what to do with it

## Next
Run pdes-critique-notes-to-actions (Critique Notes to Actions) to sort what the room said after the session.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
