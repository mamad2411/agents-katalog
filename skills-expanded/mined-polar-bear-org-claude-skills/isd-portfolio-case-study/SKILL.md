---
name: isd-portfolio-case-study
description: Drafts a portfolio case study for one course, with a confidentiality check first, the problem, your decisions and why, what the checks found and changed, and an honest split of what Claude drafted and what you did. Use for "run isd-portfolio-case-study", "write a case study for my portfolio", "my portfolio is just screenshots", "show my design decisions", "how do I show work under NDA", "write up this course project", "portfolio piece for an instructional design role", "how do I say I used AI on this", part of the Claude for Instructional Designers Pack by 90n.
---

# Portfolio Case Study

## When To Use
Your portfolio is screenshots, and the decisions behind them are what make you worth hiring. Use this after a course has shipped, when you want a reader outside the project to see how you think: what you were asked, what you found, what you chose, what you cut, and what your checks changed.

## When Not To Use
Not for the working record of a live project: that is Course Design Document, and this is the story told afterwards. Not for telling learners what was released (Course Release Note). It is not a CV or a cover letter, and if you may not show the work in any form, the simpler move is one paragraph on your method with no project in it.

## Inputs
- What you are allowed to show: the contract or employer rule, and any written permission from the owner of the work
- The brief, the decisions log from your design document, and the results of the checks and the pilot
- Any results you hold yourself, with where each number comes from, and your notes on what Claude drafted and what you did
If you have none of this, I start from your account of the request and three decisions you remember, and mark the output as a first draft.

## Approach
The shape is problem, decisions, evidence, result, a common practice convention for showing design work. A screenshot proves a screen exists; a decision with the option you turned down proves a designer was there. The failure this prevents is the polished case with a round improvement figure nobody measured and a client logo nobody cleared: one question from an interviewer, or one message from the former employer, and the whole portfolio is in doubt.

## Workflow
1. Ask at most three questions, all on confidentiality, before any drafting: who owns the work, what the contract or employer allows you to show, and what must be anonymised or recreated. No employer, client, colleague, expert or learner is named or recognisable without permission. Where you are unsure, ask the owner and check with a qualified adviser. Until this is answered I draft nothing.
2. Write the problem in two lines: the request in the requester's words, and what you found underneath it, taken from your brief. If the two are the same, say so; not every request hides a different problem.
3. Pick three to five decisions from your decisions log. For each: the options you had, what you chose, why. Include one thing you cut or refused, and who agreed. You choose the decisions; I only ask "what was the alternative?" until each has one.
4. Lay out the evidence: the checks you ran, one thing each found, and what you changed after the pilot. A check you did not run is left out or written as not run, never implied.
5. Write the honest split: what Claude drafted, what you did and decided. No line hides the tool, and none hides the designer. Then add results only where you have them, in your own numbers with the source. Otherwise write "not measured" and what you would measure next time. I never supply a figure, a quote or a testimonial.
6. Run the confidentiality pass on the finished text and on every image you plan to attach, line by line, and list what still needs permission or recreating. You make each call.

## Output Format
```markdown
# Portfolio Case Study
Title: [course described by task, no organisation named unless cleared] | Your role: [role] | Date: [period]
## Confidentiality check
| Item (text, screen, file, name) | Owner | Shown as (original, anonymised, recreated, left out) | Permission from, and date |
|---|---|---|---|
| [item] | [owner] | [treatment] | [role, date, or "to ask"] |
## The problem
Asked: [the request in the requester's words] | Found: [the gap underneath, by role and task]
## Decisions
| # | Decision | Options I had | What I chose | Why | What it cost or cut |
|---|---|---|---|---|---|
| [1] | [decision] | [options] | [choice] | [reason] | [cut, or refused, agreed by role] |
## What I checked, and what changed
| Check | Run by | One thing it found | What I changed |
|---|---|---|---|
| [check] | [role] | [finding] | [change] |
## Who did what, and the result
| Task | Claude drafted | I did and decided |
|---|---|---|
| [task] | [draft] | [decision, rewrite, test] |
- Result: [measure], [your number with its source, or "not measured" and what I would measure]
## Decision
[Designer, by name] decides what is published and where, by [date], once [owner of the work, role] has answered every "to ask" row.
```

## Done When
- The confidentiality table has no "to ask" row left for anything you intend to show
- Each decision names an option you did not take, every figure has a source, and every gap says "not measured"
- The split of who did what would survive a question in an interview

## Quality Bar
- Learners, colleagues, experts and clients appear by role only, unless they gave permission, and results describe the course, never how any learner performed
- Recreated screens are labelled as recreated, and one decision you cut or refused is in the case; a story with no "no" in it is a brochure
- Claude drafts the write-up; the decisions and the results in it are yours and real, and nothing confidential or invented is shown.

## Next
Run isd-course-brief (Course Brief) to start right when the next request arrives.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
