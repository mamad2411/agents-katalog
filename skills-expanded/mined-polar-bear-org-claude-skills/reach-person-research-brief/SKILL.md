---
name: reach-person-research-brief
description: Writes a person research brief from public, work-related sources, with sourced and dated facts about the person's role, talks, interviews and articles, what is out of scope, what you share from your own knowledge, the unknowns and the questions research could not answer. Use for "run reach-person-research-brief", "person research brief", "research this person", "prospect research", "what do I know about this person", "research before I message someone", "background on a contact", "facts about their work", part of the Claude Guide for Outreach Pack by 90n.
---

# Person Research Brief

## When To Use
You have chosen someone to write to and you want to say something specific, and you refuse to guess or pad. This answers one question: what do I actually know about this person's work, and where does each fact come from?

## When Not To Use
If you have not confirmed that the pages are about the right person, run Identity Check first. If you only need a recent, dated reason to write, Trigger Event Scan is the shorter job.

## Inputs
- The person's name, role and organisation, with your Identity Check verdict.
- Public pages to read: their organisation's site, an article or interview, a talk, a conference programme. Never LinkedIn, and nothing behind a login.
- What you know first hand: a shared event, a mutual contact, a topic of theirs you also work on.
If you have none of this, I start from the name and organisation and mark the brief as a first draft with most rows "unknown".

## Approach
One source per fact, public and work-related only: a generic research discipline. It is the difference between "I read your talk on [topic]" and "I can see you care about growth". With Claude in Chrome or web search I read the public pages you point to, read only: no clicking, typing or forms, and never LinkedIn. Unknowns stay unknown. The failure it prevents is the confident line built on a guess, which the other person spots in one read and remembers.

## Workflow
1. Ask at most three questions: what the brief is for (a first message or a first call), how far back to look, and what you already know first hand.
2. Set the scope before reading. In: role, talks, interviews, articles, public statements about their work. Out from the start: family, health, home, politics, religion, personal social media, anything behind a login.
3. Write each fact as one line with its link and the date on the page. A claim with no source is dropped, not softened into "seems to". If two sources disagree, show both.
4. Label old material as old. An article from years ago is background, with its year, never presented as what they think now.
5. List what is unknown as unknown. Never infer personality, motives, seniority, mood or how busy someone is.
6. Write "what you share" from your own knowledge only. I prompt, you confirm each line, and each is marked "your history".
7. Turn the gaps into open questions about their work that you could honestly ask. Then stop: no angle, no opening line, no message.

## Output Format
```markdown
# Person Research Brief
Person: [name] | Role: [role, as of date] | Identity: [confirmed on date] | For: [first message / first call]
## Public facts about their work
| # | Fact (one claim) | Source link | Date on source |
|---|---|---|---|
| P1 | [fact] | [link] | [date] |
## Out of scope, not collected
- [categories only, for example personal social media]
## What you share
- [your words: event, mutual contact or topic] (your history)
## Unknown
- [what you would want to know and could not find]
## Questions research could not answer
1. [open question about their work]
## Decision
[Your name] decides by [date] whether this is enough to write from, after the Research Coverage Check.
```

## Done When
- Every fact has a working link and a date; nothing is unsourced.
- The Unknown section exists, even if it is longer than the facts.
- No line touches private life, personality or motives.
- "What you share" is in your words and confirmed by you.

## Quality Bar
- Three sourced facts beat a page of guesses; the table is never padded.
- Inference dressed as fact ("clearly ambitious", "probably frustrated") is deleted.
- The brief is about the person's work, kept private, and never pasted into a shared file.
- It contains no outreach wording of any kind.
- Public sources only, a source for every fact, unknowns stated; you decide whether to write.

## Next
Run reach-research-coverage-check (Research Coverage Check) to label honestly how much the research supports.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
