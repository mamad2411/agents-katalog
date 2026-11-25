---
name: pmjob-informational-questions
description: Writes Informational Interview Questions for a conversation with someone inside before you apply or interview, covering how the team decides, what the role is really for and what changed lately, with website-answerable questions removed, five to ask first and a closing question on who else to talk to. Use for "run pmjob-informational-questions", "what do I ask an insider", "questions for a coffee chat", "a former colleague agreed to twenty minutes", "questions before I apply", "what to ask someone who works there", "informational interview questions", part of the Claude Guide for Product Interviews Pack by 90n.
---

# Informational Interview Questions

## When To Use
An insider agreed to twenty minutes, and you are about to ask what the careers page already says. You want the things only this person can tell you: how the team really decides, what the role is for, what changed in the last year. This skill answers: which questions are worth their time, and which five come first?

## When Not To Use
Inside a selection interview the questions do a different job, so use Questions to Ask there. If nobody has said yes yet, Reason to Write comes first; if you want to ask this person for a referral, that is Referral Ask, after this conversation and not during it.

## Inputs
- Who you are meeting: their role, and which of three kinds of contact they are (a peer in your function, a senior leader or hiring manager, a recruiter or someone in the hiring process)
- The company's site, the job ad if one exists, and anything public about their work, so answered questions can be cut
- What you most want to learn, in a line, and how long the slot is
If you have none of this, I start from their role title alone and mark the output as a first draft.

## Approach
The principle comes from the University of Cambridge Careers Service page Networking: who you ask shapes what you ask, and anything public information already answers is cut. Here the three kinds of contact are set for an experienced product person, who is often talking to a peer. The judgment is the website test. Asking a head of product what the company's mission is spends a slot you will not get twice, and tells them you did not read the page.

## Workflow
1. Ask at most three questions: their role and which kind of contact they are, what you most want to learn, and how long you have.
2. Set the questions by contact. Peer: how decisions really get made, how product, design and engineering work together, what the role is really for, what changed lately, what they wish they had known. Senior leader or hiring manager: where the product is going, what the team is short of, how they judge good work at this level. Recruiter: how hiring runs, timing, what the team looks for.
3. Draft across five themes: the work, how the team decides, what changed in the last year, what a strong person in this role does differently, who else to talk to. Open questions only, each short enough to say in one breath.
4. Run the website test. Drop anything the company site, the ad or their public profile answers, and name the source that answered it.
5. Remove anything that asks for a job, an interview or a referral, and anything that would need confidential information to answer. This conversation is for learning.
6. Mark five to ask first for a twenty minute slot, then add the close: who else should I talk to, and may I mention your name?

## Output Format
```markdown
# Informational Interview Questions
**For:** [name], [role] · **Kind of contact:** [peer / senior leader or hiring manager / recruiter] · **Slot:** [minutes]
## Questions by theme
| Theme | Question | Ask first? |
|---|---|---|
| The work | [question] | [yes / no] |
| How the team decides | [question] | [yes / no] |
| What changed in the last year | [question] | [yes / no] |
| What a strong person here does differently | [question] | [yes / no] |
## Dropped by the website test
- [question] (answered by [source])
## Closing question
Who else should I talk to, and may I mention your name?
## Decision
You decide the five you will ask, and in what order, by [date of the conversation].
```

## Done When
- The kind of contact is set from their role, and every question fits it
- No question survives that a public page already answers, and each dropped one names its source
- Exactly five are marked to ask first, and the closing question is there
- Nothing asks for a job, an interview, a referral or confidential information

## Quality Bar
- Questions are about the work and the team, never their pay, private life or views of named colleagues
- Kind of contact describes their role, never a judgement of the person
- Each question rests on something specific: a sourced fact, or work you shared with them
- You take your own notes in the conversation; nothing is recorded without their agreement. If you are unsure about recording, check with a qualified adviser
- Claude suggests questions; you ask them yourself in the real conversation and nothing is asked that would put the other person in a hard position.

## Next
Run pmjob-referral-ask (Referral Ask) to check whether a referral ask is ready.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
