---
name: pmjob-interviewer-research
description: Writes Interviewer Research Notes for each person on your loop with a facts table of public professional history with source and date, their likely angle by role, shared links that rest on facts from both sides, the unknowns and one question only they could answer. Use for "run pmjob-interviewer-research", "research my interviewers", "who is interviewing me", "I only have names and job titles", "what will the engineering interviewer ask", "do we have a former employer in common", "what should I ask this interviewer", part of the Claude Guide for Product Interviews Pack by 90n.
---

# Interviewer Research Notes

## When To Use
You have five names on a calendar invite and know a job title for each. Run this to answer: what is public about each person's professional path, what angle does their function usually bring to a round, what truly links you, and what could you ask that their profile does not already answer?

## When Not To Use
For the organisation and its product, use Company Research Brief. For a full set of questions per interviewer, use Questions to Ask; these notes give the facts and one question. If almost nothing about a person is public, do not dig: their role and the round they run are enough to prepare.

## Inputs
- The names and roles from the invite or the recruiter's email
- Public professional material you paste: a profile's work history, a talk, an article or a post on a work topic
- Your own role history and product areas, or your Career Evidence Inventory
If you have none of this, I start from each person's name, role and function and mark the output as a first draft.

## Approach
Sourced professional research that never pads a thin profile. Two rules carry it: no source, no fact; and a gap is written as "unknown", not filled with a plausible guess. The likely angle comes from the role, not from the person, because a function's concerns are public knowledge and a stranger's temperament is not. The failure this prevents: opening with a remark built on a guess, or asking a design lead something their own published talk answered.

## Workflow
1. Ask up to three questions: who is on the loop, with role and round; what have you pasted, and may I use web search in chat for public professional pages; what do you want to learn from each person.
2. Build a facts table per person: fact, source, date. If the material is thin, the notes say "little public information" and stop there.
3. Keep to professional information: role history, public work, talks, published writing on work topics. Left out: family, home, health, beliefs, personal accounts, photos. I never infer age, ethnicity, nationality, personality or "style", and I decline requests for a read on how to win someone over.
4. Write the likely angle from the function, labelled "by role, a guess": product tends to probe decisions and outcomes; design probes craft and users; engineering probes feasibility and how you work with engineers; data probes metrics and evidence.
5. List shared links only where a fact exists on both sides: the same former employer, the same product area, the same public event. A link resting on one side is dropped.
6. Write one question only this person could answer, built from a sourced fact such as a launch they spoke about. Then list the unknowns plainly, so your preparation does not assume them.

## Output Format
```markdown
# Interviewer Research Notes
Process: [role] · Prepared on: [date] · Status: [full / first draft]
## [Name], [role], [round]
| Fact (professional, public) | Source | Date |
|---|---|---|
| [role history item] | [page or document named] | [date or "undated"] |
| [public talk, article or work post] | [source] | [date] |
Likely angle (by role, a guess): [product / design / engineering / data], so expect [what that function tends to probe]
| Shared link | Their side (source) | Your side (evidence row or your fact) |
|---|---|---|
| [former employer / product area / public event] | [sourced fact] | [E5, or your fact] |
Unknown: [what you must not assume]
One question only they could answer: [question] (from: [sourced fact])
## [Next name], [role], [round]
[Same blocks, or "little public information"]
These notes are for this loop only. Delete them when the process ends. Nothing is saved to memory.
## Decision
You decide which question to bring to each person by [date of the first round], and you delete these notes when the process ends.
```

## Done When
- Every fact carries a named source and a date or "undated"
- Every likely angle is labelled "by role, a guess" and says nothing about the person's character
- Shared links rest on facts from both sides
- Each person has an unknowns line and a question their profile does not answer, and the closing line about deleting the notes is present

## Quality Bar
- A thin profile stays thin: "little public information" beats a padded page.
- No judgement of the interviewer: not how senior, how friendly or how hard to please.
- Nothing on private life or protected characteristics is searched for, inferred or recorded, whatever the request.
- Personal data questions about keeping notes on named people: check with a qualified adviser.
- Use a shared link once and lightly; reciting someone's history back to them reads as surveillance, not preparation.
- Public professional facts only, each with a source and a date; nothing is guessed about anyone and nothing is kept in memory.

## Next
Run pmjob-interview-loop-map (Interview Loop Map) to place each person on their round.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).