---
name: pmjob-recruiter-screen
description: Checks an inbound recruiter message for red flags before you share anything, then builds a one page Recruiter Screen Prep Sheet with your answers on why you are looking, timing and pay expectations (the employer's stated range first, no pay history) and your questions on the rounds, the timeline and the AI rules. Use for "run pmjob-recruiter-screen", "recruiter call tomorrow", "prepare for a recruiter screen", "what salary do I say I expect", "is this recruiter message real", "why are you looking answer", "questions to ask a recruiter", "first call with a recruiter", part of the Claude Guide for Product Interviews Pack by 90n.
---

# Recruiter Screen Prep

## When To Use
A recruiter wants thirty minutes tomorrow and will ask what salary you expect. Use this to check the message is what it says it is, then to walk into the call with short true answers and your own list of questions. It answers one thing: what do I say, and what do I ask, in the first call?

## When Not To Use
Once a written offer exists, the pay conversation belongs to Offer Negotiation Prep; this covers the first mention only. To say the answers aloud before the call, run Mock Interview. If you have already sent money or bank details to someone, stop and contact your bank and the platform first.

## Inputs
- The recruiter's message pasted in full, with the name, firm and role as stated, and what you found yourself on the firm's own site (does the firm exist, is the role listed)
- Any pay range the employer has stated, with where and when you saw it
- Your Tell Me About Yourself Answer and Target Role Brief, if you have them
If you have none of this, I start from the pasted message alone and mark the output as a first draft.

## Approach
Two public conventions meet here. Careers services advise checking a recruiter and a role independently before sharing details, so the check comes first and its best result is "no red flags found yet", never "safe". On pay, Directive (EU) 2023/970, Article 5 says applicants are entitled to information on starting pay or its range and that employers shall not ask about pay history; it applies through national law, which differs, so check with a qualified adviser. The failure this prevents is the experienced candidate who treats the screen as a formality, names last year's pay in minute four and never asks what the rounds are.

## Workflow
1. Ask at most three questions: what you found on the firm's own site; whether the message asks for money, bank details, ID or personal data, pushes a deadline or moves you to another app; and whether the employer has stated a pay range anywhere.
2. Run the inbound check on the message, not on the person: firm on its own site, role listed there or explained, requests for money or personal data, pressure, a move to another app. Mark each found, not found or unknown. With any flag: no personal details, report through the platform, and the sheet stops at the log line.
3. Build the call page. Public employer guides describe this call as about thirty minutes on your experience, your interest and what you want next, so it holds four things: your twenty second introduction, timing and notice, location and working pattern, and "why are you looking".
4. Keep "why are you looking" to two true, neutral sentences, forward-looking, with no blame of an employer or a person. If you already wrote them, they are carried over unchanged. If the true reason is hard to say, we find its short true form; no cover story is supplied.
5. Set the pay lines in fixed order: first you ask for the range for the role; then you answer only from the employer's stated range or from data you bring, with its source and date; you offer no pay history. For a push for a number with no range given, prepare one of three lines and choose it yourself: a question back, your own sourced range, or "I would like to understand the scope first". Claude gives no figure.
6. List your questions: the rounds and who is in each, what each assesses, the timeline, what AI use is allowed at each stage, the level and the reporting line. Then write the log line with name, firm, role, date, flags and what was agreed.

## Output Format
```markdown
# Recruiter Screen Prep Sheet
## Inbound check
| Check | Found / not found / unknown | What you saw |
|---|---|---|
| Firm on its own site, and the role listed there or explained | [ ] | [ ] |
| Asks for money, bank details, ID or personal data | [ ] | [ ] |
| Pressure, a deadline or a move to another app | [ ] | [ ] |
| Result | [Red flags found / No red flags found yet] | [ ] |
## Your answers
| Topic | What you will say, in your words | Source and date |
|---|---|---|
| Introduction, twenty seconds | [points] | [evidence rows] |
| Why you are looking | [sentence one] [sentence two] | n/a |
| Timing, notice, location and working pattern | [ ] | n/a |
| Pay, step one (ask for the range first) | [your question] | n/a |
| Pay, if they state a range | [your reply] | [their range, where stated, date] |
| Pay, if pressed with no range | [the one line you chose] | [your source, or none] |
## Questions for the recruiter
1. [The rounds and who is in each, what each assesses, the timeline, the AI rule per stage, the level and reporting line]
## Log line
[Name] · [firm] · [role] · [date] · [flags] · [what was agreed]
## Decision
You decide whether to take the call and which pay line you will use, by [date].
```

## Done When
- The inbound check is complete and never says "safe"
- "Why are you looking" is two sentences you would be happy to hear repeated, and every figure has a source and a date or the cell is a question
- The questions cover the rounds, the timeline and the AI rule at each stage

## Quality Bar
- The check judges the message, never the recruiter as a person, and notes hold name, firm and role only
- No pay history anywhere on the sheet, and no benchmark or "typical" range
- Legal points on pay and personal data are flagged, not answered: check with a qualified adviser
- No pay figure comes from Claude, no detail is shared before the checks, and you hold the call yourself.

## Next
Run pmjob-interview-loop-map (Interview Loop Map) to map the rounds the recruiter described.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
