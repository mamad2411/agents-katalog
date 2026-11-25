---
name: build-idea-one-pager
description: Writes an Idea One-Pager with the ask in the first lines (a time box to prototype and access to five real target users), the problem with its evidence source, who it is for and why now, the bet in one paragraph, one success measure, what you will not build and open questions with owners. Use for "run build-idea-one-pager", "write a one-pager for my idea", "I need a go-ahead to prototype", "ask for a week to build a prototype", "turn this chat thread into one page", "pitch this idea on a page", "what am I asking for", "one page idea brief", part of the Claude for Product Builders Pack by 90n.
---

# Idea One-Pager

## When To Use
You want a go-ahead to spend a week on a prototype and all you have is a chat thread. The person who can say yes will give it one read. This skill answers: what exactly are you asking for, from whom, and why is it worth their yes?

## When Not To Use
If nobody has agreed what question the idea answers, run Problem Frame first. If you already have the go-ahead and need to fix what the prototype must do, run Prototype Spec: this page carries no requirements.

## Inputs
- The agreed question and its decision owner (the Problem Frame, if you have one), or the idea in a few sentences.
- The evidence behind the problem and where each piece came from (session notes, support themes, usage data).
- Your ask: the time you want, who you need to reach, and any person whose help or yes you need.
If you have none of this, I start from the idea in one sentence and mark the output as a first draft, with every evidence gap listed as an open question.

## Approach
The one-page brief is a practitioner convention with no single originator. The order comes from the US Army's writing standard (Army Regulation 25-50, https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN42124-AR_25-50-007-WEB-13.pdf): writing is understood "in a single rapid reading", the main point goes at the beginning, and the voice is active. The page limit is the method: detail moves to open questions, never to a smaller font. The failure this prevents: a page that reads well, gets nods, and ends with nobody knowing whether you may start. In Claude Docs you can ask for the page as a doc in the conversation, comment on it, and share it with viewers or editors; any chat works too.

## Workflow
1. Ask at most three questions: which role answers the ask and by when; what time box do you want and what else do you need; which evidence can I use, and where did it come from?
2. Write the ask first, in active voice: the time box you stated, access to five real target users, and anything else needed (an engineer's half hour, a design system owner's yes). It is an ask for time to learn. It is never budget or headcount.
3. Write the problem in the user's terms, each claim with its evidence source. A claim with no source becomes an open question, not a softer sentence.
4. Name one primary group by need, then why now. "Why now" names a change in users, the market or the product. Urgency and "leadership wants it" are not changes.
5. Write the bet in one paragraph: what you would try and why you think it works. No feature list. Add one success measure with baseline and target as [placeholders] you fill in, and a "will not build" list of what a reasonable reader would assume is in.
6. List open questions, each with an owner role and a date. Repeat the ask in the Decision at the bottom, then cut to one page and run the rapid-reading test: would a reader who stops after the first three lines know what you need? If not, the ask is still buried.

## Output Format
```markdown
# Idea One-Pager
**The ask:** [time box] to build a prototype, access to five real target users, and [anything else needed], from [role] by [date]
## Problem, who it is for and why now
[The problem in the user's terms] | Evidence: [source]
**For:** [one group, named by need] | **Why now:** [the change]
## The bet
[One paragraph: what you would try and why you think it works]
## Success measure
| Measure | Baseline | Target | Read on |
|---|---|---|---|
| [one measure] | [you set] | [you set] | [date] |
## What we will not build
- [Thing a reader would assume is in]
## Open questions
| Question | Owner (role) | Answer by |
|---|---|---|
| [question] | [role] | [date] |
## Decision
[Role who answers the ask] says go, reshape or stop on [time box] and access to five real target users by [date].
```

## Done When
- It fits one page, and the ask (a time box, five real target users, a role and a date) is in the first lines and again in the Decision.
- Every problem claim has a source or sits in open questions.
- "Why now" names a change, there is exactly one success measure, and at least one item sits under "What we will not build".

## Quality Bar
- No invented numbers: baseline, target, time saved and market figures stay [placeholders] until you supply them.
- One bet per page, in plain words a reader outside the team understands: no codenames, no ticket numbers.
- No requirements and no screen list. Those are settled after the yes.
- The target group is named by need, never as a profile of a named customer or person.
- The page asks for time to learn, never for a launch; a named person answers the ask.

## Next
Run build-prototype-test-card (Prototype Test Card) to set the pass line before the build.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
