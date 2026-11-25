---
name: firm-pre-call-brief
description: Builds a one-page pre-call brief from the company's own public pages, with sourced facts, the likely trigger marked as inference, two or three hypotheses each with its test question and kill answer, what an AI summary would say and miss, and a do-not-assume list. Use for "run firm-pre-call-brief", "prepare me for this first call", "research this company before we talk", "I have twenty minutes before the meeting", "give me a point of view on them", "what should I test on the call", "what would an AI summary of them miss", part of the Claude for Consultants · Team in Claude Pack by 90n.
---

# Pre-Call Research Brief

## When To Use
The first conversation is today and you have a gap between two client sessions to prepare. The client can get a tidy summary of their own company from any model; what they cannot get is a consultant who arrives with a view that might be wrong and knows how to test it. Run this to decide what you believe about their situation and what answer would change your mind.

## When Not To Use
If they sent a document, read it with AI-Written Brief Review first. If the hypotheses exist and you need the full question page, go to Discovery Call Questions.

## Inputs
- The company name and the pages to read (their site, newsroom, public announcements, whatever prompted the contact)
- What you already know, and the public job title of the person you will meet
- Your one-line hunch about what is going on, if you have one
If you have none of this beyond a name, I start from their home page and mark the brief as a first draft. With Claude in Chrome (paid plans) I read the public pages myself; otherwise paste them.

## Approach
Hypothesis-led preparation is an old consulting habit, described generically: form a view before the meeting, then go in to test it instead of to confirm it. The failure it prevents is opening with ten minutes of questions the client already answered on their website, which tells a senior buyer you did not look. Research stays on the company and on the public role of the person you meet, never their private life or personality.

## Workflow
1. Ask, in one go: what prompted this contact? Which pages should I read or leave alone? What is your hunch, in one line?
2. Read only the company's own public pages and the announcements you named. Each fact goes down with its link beside it. A fact I cannot link is left out, including things I think I remember.
3. Name the likely trigger, the reason this is happening now: a change, a launch, a stated goal, a new public appointment. Label it inference and name the fact it rests on.
4. Write two or three hypotheses, each a sentence the client could disagree with. Next to each: the question that tests it on the call and the answer that would kill it. Three is the ceiling; a longer list is browsing, not a view.
5. Write what an AI summary of this company would say from the same pages, then what it would miss: constraints, what was tried and dropped, who really decides, what nobody publishes. That second list is the reason for the call.
6. List what not to assume: that the public goal is funded, that the person you meet holds the budget, that the announced plan is still the plan. Then cut to one page; a line that would not change what you ask goes.

## Output Format
```markdown
# Pre-Call Point of View
Company: [name] · Call: [date] · Meeting: [public role] · Pages read on [date]
## Public facts
| Fact | Source (link) |
|---|---|
| [fact] | [link] |
## Likely trigger (inference)
[Why this is happening now, in a line or two] · Built on: [fact above]
## Hypotheses to test
| Hypothesis (untested) | Question that tests it | Answer that would kill it |
|---|---|---|
| [one sentence] | [question] | [answer] |
## What an AI summary would say, and miss
- Would say: [the generic picture]
- Would miss: [what only the conversation can show]
- Do not assume: [what looks true from outside]
## Decision
[You] choose the hypothesis to open with before [call time]. All of them stay untested until the client answers.
```

## Done When
- Every fact links to the company's own page or a public announcement
- The trigger reads "inference" and each hypothesis reads "untested", with a test question and a kill answer
- Nothing concerns a person beyond a public role, and it fits one page

## Quality Bar
- Two or three hypotheses, never a list of ten
- The "would miss" list is specific to this company, not a stock list of unknowns
- No figure appears that is not printed on a source page
- Requests to research a person's social profiles, private life or character are declined
- Every fact is sourced and every hypothesis marked untested; I invent nothing about the company, and the view you take into the room is yours.

## Next
Run firm-discovery-call-agenda (Discovery Call Agenda) to agree the purpose and possible outcomes of the call in advance.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
