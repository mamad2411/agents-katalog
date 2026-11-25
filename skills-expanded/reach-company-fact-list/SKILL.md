---
name: reach-company-fact-list
description: Collects up to twelve numbered facts about one organisation from public pages, one claim per line with its date and link, sorted into what the organisation is doing now and recent signals, with the claims dropped for having no source and the unknowns. Use for "run reach-company-fact-list", "company fact list", "research this company", "company research with sources", "facts about this company", "what is this company doing", "account research", "research before I write", part of the Claude Guide for Outreach Pack by 90n.
---

# Company Fact List

## When To Use
You have twenty minutes before you write to someone at this organisation, and you refuse to write from a guess. This answers one question: what can I say about this organisation that is true, dated and checkable?

## When Not To Use
If you are still choosing between organisations, one line of evidence per criterion is enough: use Target Account List. If you already have a fact list and want half a page to prepare from, go to Company Research Brief.

## Inputs
- The organisation's name and website.
- The public pages you want read: their news page, a report, the leadership page, job adverts, an interview. With Claude in Chrome or web search I read those pages only.
- How far back still counts as recent for you.
If you have none of this, I start from the organisation's own website and mark the list as a first draft.

## Approach
Facts first, brief second: a generic research discipline. Collecting and writing are kept apart, because a summary written in one step fills its gaps with fluent sentences nobody can check. Here each fact is one short claim with a date and a link, and a claim that cannot be tied to a page is dropped, not softened into "it seems". Where I use Claude in Chrome it is read only: no clicking, no typing, no forms, and never LinkedIn. The failure it prevents is the confident line in your first message that the reader knows is wrong.

## Workflow
1. Ask at most three questions: which pages to read, how far back counts as recent, and what you already know first hand that I should not go looking for.
2. Read the pages and write candidate claims, one claim per line, with the date or year inside the claim.
3. Tie each claim to the page it came from. A claim I cannot tie to a page goes to the dropped list, even when it sounds right. I say how many were dropped.
4. Sort what survives into two kinds: what the organisation is doing now (what it says it does, stated goals, launches, structure) and recent signals inside your window (a new leader, hiring for a role, an announcement).
5. Number them F1, F2 and so on, most recent first, and stop at twelve. If more exist, keep the ones that touch your work and say what was left out.
6. List the unknowns as unknown: what you would want to know and no page said.
7. Stop there. No summary, no hypotheses, no angle and no message: those come later and may cite only these numbers.

## Output Format
```markdown
# Company Fact List
Organisation: [name] | Pages read: [number] | Recent means: [window you set] | Collected: [date]
## What they are doing now
| # | Fact (one claim, with its date) | Source link |
|---|---|---|
| F1 | [claim, date] | [link] |
## Recent signals
| # | Fact (one claim, with its date) | Source link |
|---|---|---|
| F2 | [claim, date] | [link] |
## Dropped for having no source
- [claim], dropped: [no page says it / page says something else]
## Unknowns
- [what no page said]
## Decision
[Your name] decides which facts go through the Source Check and whether this account is worth a brief, by [date].
```

## Done When
- Every fact is one claim with a date and a working link.
- There are no more than twelve facts, numbered.
- The dropped list and the unknowns list both exist, even if short.
- The output contains no summary, hypothesis or message.

## Quality Bar
- One claim per line: "and" in a fact usually means two facts.
- A date is the date on the page, not the day I read it.
- Numbers about the organisation appear only when the linked page states them.
- Three solid facts are a fine result; the list is never padded to reach twelve.
- A fact with no source is dropped, never softened; you decide what to do with what is left.

## Next
Run reach-source-check (Source Check) to test the sources behind the facts you plan to use.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
