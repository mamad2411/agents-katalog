---
name: pmjob-tell-me-about-yourself
description: Drafts your Tell Me About Yourself Answer as speaking notes, a ninety second version in present, past, future order built from three evidence rows, a twenty second version and two true sentences for why you are looking. Use for "run pmjob-tell-me-about-yourself", "tell me about yourself answer", "walk me through your background", "introduce myself in an interview", "why are you looking answer", "my intro is a spoken resume", "twenty second introduction for a panel", part of the Claude Guide for Product Interviews Pack by 90n.
---

# Tell Me About Yourself

## When To Use
The first question of every interview is the one you answer worst. You start at your first job, walk through every role in order, and the interviewer learns nothing about what you want now. Run this to answer: what do I say in ninety seconds that is true, chosen for this role, and easy to say?

## When Not To Use
For full stories with follow-ups, run Interview Story Bank; this is the opening answer and nothing else. For everything else a first recruiter call needs, such as timing and pay expectations, run Recruiter Screen Prep.

## Inputs
- Your Career Evidence Inventory, or the three pieces of work you would pick
- Your Target Role Brief, for what you want next in your own words
- Who is asking (recruiter, hiring manager, panel) and the true reason you are looking, said roughly
If you have none of this, I start from your current role, one thing you are known for and the role in front of you, and mark the output as a first draft.

## Approach
The present, past, future introduction is a common careers-service convention: what you do now, how you got here, what you want next. The judgment is the limit of three evidence rows, chosen for the role in front of you. The failure this prevents is the spoken resume: four minutes, every role in order, and the interviewer waiting for the point.

## Workflow
1. Ask up to three questions: which role this is for and who is asking, the one thing you are best known for today, and the true reason you are looking, in whatever rough words come first.
2. Present: what you do now and the one thing you are best known for, backed by one row.
3. Past: two moves or pieces of work that explain how you got here, one row each, chosen for the target role. Three rows in total, no more. Anything else waits for a later question.
4. Future: what you want next and why this role, in the words of your Target Role Brief. No praise of the employer that their own website could have supplied.
5. Write two lengths as speaking notes, with the row ID beside each claim: about ninety seconds spoken, and about twenty seconds for a recruiter or a panel introduction.
6. "Why are you looking": two true sentences, forward-looking, with no blame of an employer or a person and nothing you would not want repeated. If the true reason is hard to say, we look for its true and short version. I never supply a cover story.
7. Say it aloud once. Voice mode lets you speak the answer, hear it back and time it. This is practice only: in the interview you say it yourself, without Claude.

## Output Format
```markdown
# Tell Me About Yourself Answer
For: [role] · Asked by: [recruiter / hiring manager / panel] · Updated: [date] · Timed aloud at: [your timing]
## Ninety second version (speaking notes)
| Part | What you say, in your words | Row |
|---|---|---|
| Present | [what you do now, and the one thing you are known for] | [E_] |
| Past | [first move or piece of work, and why it mattered] | [E_] |
| Past | [second move or piece of work, and why it mattered] | [E_] |
| Future | [what you want next, and why this role] | [Target Role Brief] |
## Twenty second version
[one line of present, one line of past, one line of future]
## Why are you looking
1. [true sentence about what you want next]
2. [true sentence about why now]
## Left out on purpose
- [role or piece of work] · [where it can come up instead]
## Decision
You decide the final wording of both versions and the two sentences, and say them aloud once more, by [date].
```

## Done When
- Three evidence rows are used, each with its ID beside the claim
- The ninety second version runs present, past, future and holds to time when you say it
- The twenty second version stands on its own
- The two sentences are true, neutral and safe to repeat
- You have said it aloud at least once

## Quality Bar
- Speaking notes, not a script: short lines you can say in your own way.
- No employer, manager or team is criticised, by name or by role.
- "Why are you looking" stays at two plain sentences, with no drama and no long explanation.
- No adjective about you without the row that shows it.
- Three true rows in your own words; no cover story for why you are looking, and you say it yourself in the room.

## Next
Run pmjob-resume-bullets (Product Resume Bullets) to put the same evidence on the page.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
