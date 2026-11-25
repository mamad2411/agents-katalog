---
name: reach-target-account-list
description: Builds a target account list from a two-line brief, with the criteria that show an organisation has the problem, each one checked yes, no or unknown with a linked source, the number you can really work and the drops with reasons. Use for "run reach-target-account-list", "target account list", "build my prospect list", "which companies should I reach out to", "account list", "who should I target", "check these companies against my brief", "prospecting list", part of the Claude Guide for Outreach Pack by 90n.
---

# Target Account List

## When To Use
Your list is forty logos and no reason to write to any of them. This answers which organisations are worth your attention in the next runs, on what evidence, and which ones you can stop thinking about.

## When Not To Use
If you cannot yet say what you help with and in what situation, run Ideal Client Profile first; a vague brief gives a list nobody can act on. If one organisation is already chosen and you need to know it properly, go straight to Company Fact List.

## Inputs
- Your brief in two lines: what you help with, and the situation that makes someone need it. Your Ideal Client Profile and Buying Situations Map if you have them.
- The organisations you have in mind, or the public places to look (event pages, association member lists, news you follow).
- How many accounts you can really work in the coming weeks.
If you have none of this, I start from a two-sentence description of what you do and five organisations you name, and mark the list as a first draft.

## Approach
Account fit against a written brief, a generic practice: write down first who the work is useful to and why, then check each organisation against that, criterion by criterion, with yes, no or unknown. There is no score and no total, because a number hides thin evidence behind a ranking. With Claude in Chrome or web search I read the public pages you point me to: read only, never clicking, typing or filling a form, never on LinkedIn, and never from a bought or scraped list. The failure it prevents is the long list of logos that looks like a pipeline and is a wish list.

## Workflow
1. Ask, all at once: your brief in two lines, how many accounts you can really work, and how far back still counts as recent for you.
2. Write the brief back as a problem, the role that lives with it, and three to five criteria that show an organisation has the problem (and one or two that show it does not). You correct it before I look at a single organisation.
3. For each organisation, check each criterion: yes, no or unknown, with the public evidence linked and dated. "Unknown" is a real answer and is better than a guess written as a fact.
4. Show the grid as it is. No score, no total, no ranking. You mark each organisation keep, maybe or drop; I never move one for you.
5. For each kept organisation, note one possible reason to write, taken from a sourced, dated fact, or write "none yet". An account with no reason waits; it does not get a message.
6. Cut to the number you said you can work. Every drop is written down with its reason, so the same names do not come back next quarter.
7. Leave people out. This list holds organisations only: no names, emails or phone numbers are gathered here.

## Output Format
```markdown
# Target Account List
Brief: [what you help with, and the situation that makes someone need it] | Accounts I can work: [number you set] | Recent means: [window you set]
## Criteria
1. [sign that an organisation has the problem]
2. [sign]
3. [sign that it does not]
## Accounts
| Organisation | Criterion 1 | Criterion 2 | Criterion 3 | Evidence (link, date) | Your call | Possible reason to write |
|---|---|---|---|---|---|---|
| [organisation] | [yes / no / unknown] | [yes / no / unknown] | [yes / no / unknown] | [link, date] | [keep / maybe] | [fact, link, date, or "none yet"] |
## Dropped
| Organisation | Reason |
|---|---|
| [organisation] | [criterion failed or red flag, with link] |
## Unknowns
- [what could not be found, and where you might ask]
## Decision
[Your name] decides which accounts go into the Warm Path Check first, and by [date] whether each "maybe" is kept or dropped.
```

## Done When
- You approved the brief and the criteria before any organisation was checked.
- Every yes or no has a link and a date; everything else says unknown.
- The list is no longer than the number you said you can work, and every drop has a reason.
- No score, total or ranking appears anywhere.

## Quality Bar
- Criteria describe a situation you can see evidence of, never a size, sector or revenue band.
- No contact details and no lists of people are gathered at this stage.
- A maybe stays a maybe until you move it.
- Public pages only, read where you point; nothing scraped, bought or logged into.
- Organisations are checked against your brief and nobody is scored; you choose who makes the list.

## Next
Run reach-warm-path-check (Warm Path Check) to see who you already know at each account before anything cold.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
