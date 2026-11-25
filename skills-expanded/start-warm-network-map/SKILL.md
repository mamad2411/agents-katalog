---
name: start-warm-network-map
description: Maps your warm network against a two-line brief from your own connections file, showing each visible match with its reason, fit set by you, closeness in four tiers in your own words, at most three names per organisation, a run of about 10 you pick with a reason for each and the names set aside. Use for "run start-warm-network-map", "who should I talk to this week", "map my network", "go through my LinkedIn connections", "who in my network could help", "pick 10 people to contact", "I have years of contacts and no plan", part of the Claude Guide for New Founders Pack by 90n.
---

# Warm Network Map

## When To Use
You have years of connections and cannot say who to talk to this week. Scrolling the list ends at the names you already think of. Run this once the brief is clear, to turn your own export into a short run of people you chose for a reason.

## When Not To Use
For the people who worked with you directly, Former Colleagues List is the better start and needs no export. If you have no connections file yet, run LinkedIn Data Export Guide first.

## Inputs
- Your brief in two lines: what you want help with now, and who you would like to meet (roles in situations)
- Your cleaned connections file, uploaded to a private chat or a private Project
- Optional: your messages file or your own count of exchanges, for a first guess at closeness
If you have none of this, I start from your brief and 20 names with titles that you paste, and mark the map as a first draft.

## Approach
Granovetter's "The Strength of Weak Ties" (1973) found that new information often arrives through acquaintances, not close friends, so the map keeps distant ties in view. The working rule is a practitioner one, stated as a principle: fit to the brief first, closeness as a bonus, and a cap per organisation. Fit is to a brief, never a judgement of a person; closeness says how well you know someone, never what they are worth or whether they might buy. The failure it prevents: a list that is really your friends, padded with ten people from your last employer.

## Workflow
1. Ask at most three questions: your brief (help with what, to meet whom), how many conversations you can really hold in the next fortnight, and whether any organisation is out of scope, for instance under your terms check.
2. Write the brief at the top before any name is read. One goal per run; a second goal gets a second map.
3. Read each row against the brief from title and organisation only. Write the visible match with its reason ("title matches: owns [problem]") or "no visible match". Anything not visible in those fields is "needs research", not a guess.
4. You set fit for every row: fits, maybe, not for this brief. A visible match is a suggestion; vague titles hide people who fit. A row you mark "not for this brief" is not carried forward, however well you know them.
5. Set closeness in four tiers, in your words: close ("I could call them tomorrow"), acquaintance ("we know each other, not deeply"), distant ("connected, but I barely know them"), never met ("I would not recognise them"). With a count of exchanges I offer a first guess from counts only; you correct every one, because counts miss years of working side by side.
6. Apply the cap: at most three names per organisation carried forward, and you choose which three.
7. You pick a run of about 10, each with a reason in your words. I show rows in the order you ask for and never mark one as "best". If every pick is close, I say so; the choice stays yours. Names you considered and left go on a set-aside list with a reason about the brief, never about the person.

## Output Format
```markdown
# Warm Network Map
Brief: [help with what] | To meet: [roles in situations] | Export date: [date] | Rows read: [number]
## Rows
| Name | Title, organisation | Visible match and reason | Fit (I set) | Closeness (I set, my words) |
|---|---|---|---|---|
| [name] | [title, organisation] | [match: reason / no visible match / needs research] | [fits / maybe / not for this brief] | [close / acquaintance / distant / never met] |
## Organisations capped at three
- [organisation]: [names I kept]
## My run of about 10
| Name | My reason, in my words | Write by |
|---|---|---|
| [name] | [reason] | [date] |
## Set aside for a later run
| Name | Reason (about this brief) | Look again on |
|---|---|---|
| [name] | [reason] | [date] |
Closeness says how well I know someone, never what they are worth.
## Decision
[Your name] confirms the run by [date]; nobody is contacted until then.
```

## Done When
- The brief is written before any name is read.
- Every fit and every tier is set by you.
- No organisation has more than three names.
- The run holds about 10 names, each with your reason.

## Quality Bar
- Only title, organisation and connection date are read; nothing is inferred about a person.
- No score, weight, ranking or "top" label anywhere; no guess at who might buy.
- Set-aside reasons are about this brief, never about the person.
- The file stays private and is deleted on the date you set.
- Your own contacts from your own export; you set fit and closeness, choose the names and write to them yourself.

## Next
Run start-reconnect-message (Reconnect Message) to prepare the first note to someone on your run.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
