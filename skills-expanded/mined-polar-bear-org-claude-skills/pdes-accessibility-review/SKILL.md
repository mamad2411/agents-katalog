---
name: pdes-accessibility-review
description: Runs a design-stage Accessibility Review of one screen or flow against WCAG 2.2 at your team's level, marking each check pass, fail or cannot tell from a design, writing the fix for each fail as a design change, and listing what only code, assistive technology and disabled users can show. Use for "run pdes-accessibility-review", "accessibility review of my design", "check my screens against WCAG 2.2", "accessibility audit of this flow", "is my contrast ok", "check focus order and target size", "accessibility check before handoff", "the AI audit said everything passed", part of the Claude for Product Designers Pack by 90n.
---

# Accessibility Review

## When To Use
Accessibility gets looked at after the build, when every fix is expensive, or an "AI audit" said everything passed and you do not believe it. You want the problems a design file can show found now. It answers: which checks does this screen pass or fail at design stage, and what can nobody know until it is coded and used?

## When Not To Use
If the design is ready to put in front of disabled people, plan Accessible Test Sessions: a file review never stands in for them. For a quick contrast and keyboard look before sharing a prototype, Prototype Share Check is enough. A conformance statement or a formal audit needs a qualified accessibility auditor, not this skill.

## Inputs
- One screen or flow, with every state you want reviewed listed by name
- The real colour values for text, icons, borders and backgrounds, plus target sizes and spacing, pasted as values or token names with values
- The WCAG 2.2 level your team commits to, and the intended focus order if you have numbered it
- Optional: the Figma connector, which reads frames, variables and components
If you have none of this, I start from a written description of the screen and mark the output as a first draft, with most contrast rows reading "cannot tell from a design".

## Approach
WCAG 2.2 (W3C Recommendation, 5 October 2023) read through W3C WAI's Designing for Web Accessibility tips and Easy Checks, with manual and assistive technology testing as the GOV.UK Service Manual describes it. The judgment is in the third answer: "cannot tell from a design" is honest, and a table with no such rows was filled in by guessing. W3C WAI states that tools cannot check all accessibility aspects automatically, so a person must judge. The failure it prevents is a slide that says "accessibility: passed" over a product no screen reader user has opened.

## Workflow
1. Ask three questions: which screen or flow and which states, which WCAG 2.2 level does your team commit to, and can you paste the real colour values and target sizes?
2. Fix the scope in writing: the frames and states reviewed. Anything you did not show me reads "not reviewed", never "pass".
3. Seeing and reading: 1.4.3 Contrast (Minimum), 1.4.11 Non-text Contrast, 1.4.1 Use of Color, 1.4.4 Resize Text, 1.4.10 Reflow. Contrast is worked out only from pasted values, against the threshold on the criterion's W3C page, which I link for you to read. From a described screenshot the answer is "cannot tell".
4. Pointing and moving: 2.5.8 Target Size (Minimum), 2.4.7 Focus Visible, 2.4.11 Focus Not Obscured (Minimum), 2.4.3 Focus Order. You number the order you intend; I check it against reading order and meaning, and ask where a focus style is not drawn.
5. Understanding: 3.3.2 Labels or Instructions, 3.3.1 Error Identification, 1.3.1 Info and Relationships, 2.4.6 Headings and Labels. An error shown by colour alone fails twice, and I say so once per criterion.
6. Three answers only: pass, fail, cannot tell from a design. Each fail gets a fix written as a design change (which token, which label, which size or spacing), and you decide whether to make it.
7. Close with the fixed list of what only code, assistive technology and disabled users can show: screen reader output, real focus behaviour, zoom in a browser, timing, and how people cope. I never simulate how a disabled person would use the product. Legal duties vary, so check with a qualified adviser.

## Output Format
```markdown
# Accessibility Review
**Screen or flow:** [name] | **Stage:** design file, not built | **Level reviewed against:** [WCAG 2.2 level the team stated] | **Date:** [date]
## Scope
Reviewed: [frames and states]. Not reviewed: [frames and states].
## Checks
| Success criterion | Where | Answer | What I saw or was given | Fix (design change) |
|---|---|---|---|---|
| [number and name] | [element or frame] | [pass, fail or cannot tell from a design] | [values or description] | [change, or what is needed to tell] |
## What a design file cannot show
- Screen reader output: [what to test in code]
- Real focus behaviour, zoom in a browser, timing: [what to test in code]
- How disabled people get through the task: [sessions planned or not yet planned]
## Status line to use when sharing
"Design-stage review of [scope] on [date]. Not an audit. Not a conformance statement."
## Decision
[Designer] makes or declines each fix by [date]; [product manager or engineering lead] decides by [date] when the coded build is tested with assistive technology and with disabled people.
```

## Done When
- Every row names a success criterion by number and gives one of the three answers, and every fail has a fix written as a design change
- Every contrast answer comes from pasted values, or reads "cannot tell from a design"
- The closing list and the status line are in the output, word for word

## Quality Bar
- No threshold is quoted from memory: the criterion is linked and the W3C page is the reference
- A clean table is reported as "no fails found in what was shown", never as "accessible" or "compliant"
- Gaps describe the screens, never what someone forgot
- Nothing is said about how a disabled person "would" experience the design
- This is a design-stage review, never an audit or a conformance statement; for legal duties, check with a qualified adviser

## Next
Run pdes-design-sameness-check (Design Sameness Check) to see which visible choices were ever decided.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
