---
name: pmjob-ai-use-plan
description: Build a one page plan per employer showing what they allow candidates to do with AI at each stage and where that is written, the points to put to the recruiter where nothing is written, and the sentence you will say when asked. Use for "run pmjob-ai-use-plan", "can I use AI on the take-home", "what AI use does this employer allow", "candidate AI policy", "should I say I used Claude", "ask the recruiter about AI tools", "AI rules for my interview process", "what do I say if they ask about AI", part of the Claude Guide for Product Interviews Pack by 90n.
---

# Candidate AI Use Plan

## When To Use
You do not know whether using AI on the take-home is expected or forbidden, and you have not asked. Each employer sets its own rule, often a different one for each stage, and some have written nothing down. This skill answers one question per employer: what may I use AI for at each stage, how do I know, and what will I say when they ask?

## When Not To Use
Not for "how do you use AI in your work": that is about your job, not your candidacy, and AI Fluency Answer builds it. If one assignment is already on your desk, Take-Home Assignment Plan applies the rule to that brief.

## Inputs
- The employer's own words on candidate AI use, pasted with the date you read them: careers page, recruiter email, assignment brief.
- The stages ahead of you, or your Interview Loop Map, and what you have already used AI for in this process.
If you have none of this, I start from the four stages with every rule marked "not stated" and mark the output as a first draft.

## Approach
The method is candidate AI rules by stage, with Anthropic's public Guidance on Candidates' AI Usage as the model of what one clear employer policy looks like. It is that employer's rule for its own hiring and says nothing about anyone else's, so this employer's own words always come first. The judgment: silence is never permission. The failure it prevents is the take-home polished with AI over a weekend, followed by a brief whose last paragraph asked for unaided work.

## Workflow
1. I ask up to three questions: which employer and which stages are still ahead; what they have written or said about candidates using AI, and where; what you have used AI for so far in this process.
2. I lay out four stages as rows: application (resume and written answers), take-home assessment, interview preparation, live interviews. "What this employer says" is filled only from text you paste, quoted briefly, with where it is written and the date. Nothing written means the cell reads "not stated".
3. Beside it I show the reference model, labelled as one employer's rule for its own hiring: write your own first draft and refine it after; take-homes without AI unless the employer says otherwise; use AI in preparation to research the company, practise answers and prepare questions; live interviews are your own thinking with no AI help unless told otherwise; be open about your use. It shows what to ask for. It never fills an empty cell.
4. You set your plan per stage: what you will use Claude for, and a "will not" list that always holds three lines: no generated experience, no AI during a live round, no AI on a take-home that forbids it. A stage marked "not stated" stays on hold until the recruiter answers.
5. I give you the recruiter question as points you write and send yourself: which stages allow AI tools, whether the take-home expects or forbids them, whether they want AI use declared and how. Any accommodation you need goes to the recruiter early, in your own words.
6. You write one disclosure sentence per stage where AI was used: what you used it for and what you did yourself. Plain enough to say aloud when asked. I check it against the plan and flag anything it leaves out.
7. I date the page and write one AI rule line per stage, the rule and where it is written, or "not asked yet". That line is what goes in the AI rule column of the Interview Loop Map and the Job Search Tracker. When the recruiter replies, run this again and the status changes from first draft to confirmed.

## Output Format
```markdown
# Candidate AI Use Plan
Employer: [as you state it] | Role: [title] | Date: [date] | Status: [first draft, or confirmed by the recruiter on date]
## Rules by stage
| Stage | What this employer says | Where it is written, with date | My plan | Open question |
|---|---|---|---|---|
| Application (resume, written answers) | [short quote or "not stated"] | [page, email or brief, date] | [what I use Claude for] | [question or "none"] |
| Take-home assessment | [short quote or "not stated"] | [source, date] | [plan or "on hold"] | [question or "none"] |
| Interview preparation | [short quote or "not stated"] | [source, date] | [plan] | [question or "none"] |
| Live interviews | [short quote or "not stated"] | [source, date] | No AI during the round | [question or "none"] |
## AI rule (copy into the AI rule column of the loop map and the tracker)
- [stage]: [rule and where written, or "not asked yet"]
## I will not
- Present generated experience, a role, a result or a number as mine.
- Use AI during a live round.
- Use AI on a take-home that forbids it, or while its rule is still "not stated".
## Points for the recruiter
- [each open question as a point, in your words]
## What I will say when asked
- [stage]: [your sentence on what you used AI for and what you did yourself]
## Decision
You decide which open questions go to the recruiter and send them yourself by [date], before [next stage] begins.
```

## Done When
- All four stages have a row, and every rule cell holds a quote with its source and date or the words "not stated".
- Every "not stated" cell has a matching point for the recruiter, and the "will not" list holds its three fixed lines.
- Each stage has an AI rule line, and there is one disclosure sentence for each stage where AI was used, in your words.

## Quality Bar
- The employer's rule is quoted, never paraphrased into something more generous. The reference model is labelled as another employer's rule every time it appears.
- One page per employer: a rule from one process is never carried into another. Recruiter messages are points you write and send.
- I refuse plainly to help hide AI use, reword text so the use is harder to notice, or work around a stated rule.
- Accommodations and any legal point on AI in hiring: check with a qualified adviser.
- Follow each employer's stated rule, ask where there is none, stay out of the live interview, and say what you used AI for when asked.

## Next
Run pmjob-ai-fluency-answer (AI Fluency Answer) to answer how you use AI in your work.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
