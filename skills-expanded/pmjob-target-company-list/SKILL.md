---
name: pmjob-target-company-list
description: Builds a Target Company List of ten to twenty companies against your brief, each with a sourced reason it fits, the open role or "none posted", who you already know there or one step away, and a dropped list with reasons. Use for "run pmjob-target-company-list", "which companies should I target", "my list is five famous names", "build my company list", "where do I know someone", "companies that fit my criteria", "find less well-known companies hiring product people", part of the Claude Guide for Product Interviews Pack by 90n.
---

# Target Company List

## When To Use
Your list is five famous names, and you have never checked who you know at any of them. After years of work you have former colleagues, managers and partners spread across more companies than you can recall in one sitting. This skill answers: which companies fit what I wrote in my brief, and where do I already know someone?

## When Not To Use
If you have no criteria or deal-breakers written down, run Target Role Brief first, because a list with no brief is a list of logos. To go deep on one company use Company Research Brief, and once a process is live it belongs in Job Search Tracker.

## Inputs
- Your Target Role Brief, or the roles, level, own criteria and deal-breakers in a few lines
- Companies already on your mind, including the ones you are unsure about
- People you have worked with and where they are now, as far as you know (names and how you know them, no contact details)
If you have none of this, I start from one target role and two criteria and mark the output as a first draft.

## Approach
This is a banded company list with a source on every row, a common careers-service convention, with one column added: who you already know. The bands exist because the well-known names get everybody's applications, while a less well-known company may fit your criteria better and hold someone who has seen your work. Research on reconnecting with former contacts (Dormant Ties: The Value of Reconnecting, Organization Science, 2011) and on weaker ties and job moves on one professional network (A Causal Test of the Strength of Weak Ties, Science, 2022) is context for that column, never a promise. The failure this prevents: three months on the same five names, while a former manager two companies away never hears you are looking.

## Workflow
1. Ask at most three questions: which criteria and deal-breakers from your brief matter most, which companies you already have in mind, and who you have worked with that has moved somewhere interesting.
2. Apply the deal-breakers first. A company that fails one goes straight to the dropped table with the reason, however well known it is.
3. Suggest companies in three bands by how well known they are to people in your field: well known, known in its field, less well-known. Ten to twenty in total, with at least a few in the last band. A band describes visibility and nothing else about the company.
4. Fill each row: why it fits, tied to one named criterion, the source and its date, and the open role or "none posted". No source, no row. With web search on in the chat, Claude reads the company's own careers and product pages.
5. Fill "Who I know" from your memory only: former colleagues, managers, partners, clients, or one step away through someone you name, with the closeness in your own words. Claude does not look people up. Empty is fine and is written "nobody yet".
6. You cut and add rows by hand. Fit is company against brief, in words. If you use the desktop app with Google Drive connected, the final list can go into a Google Sheet created from the chat.

## Output Format
```markdown
# Target Company List
## Brief in one line
[roles, level, top criteria, deal-breakers]
## Companies
| Company | Band | Why it fits my brief (criterion) | Source and date | Open role or "none posted" | Who I know | Closeness, in my words |
|---|---|---|---|---|---|---|
| [company] | [well known / known in its field / less well-known] | [one line, naming the criterion] | [page, date] | [role title or "none posted"] | [name or "nobody yet"] | [e.g. worked beside them for years, not spoken since] |
## Dropped
| Company | Reason |
|---|---|
| [company] | [the deal-breaker or criterion it fails] |
## To check
- [company]: [what the source did not show]
## Decision
You decide the final ten to twenty and the first people to get back in touch with by [date].
```

## Done When
- Ten to twenty companies across all three bands, with a few in the less well-known band
- Every row names a criterion from the brief and carries a source with a date
- Every dropped company has a reason
- The people column holds only names you gave, or "nobody yet"

## Quality Bar
- One line per company; depth belongs in Company Research Brief
- No row carries a number, an order of preference set by Claude or a verdict on a company or a person
- An open role comes from the company's own page with its date, never from memory
- Names and closeness only: no contact details, and no view on who is "useful". If you keep notes on other people and have a data protection question, check with a qualified adviser
- Claude suggests companies with sources; the people column is yours, and nobody is looked up or contacted for you.

## Next
Run pmjob-reason-to-write (Reason to Write) to get back in touch with the people on the list.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
