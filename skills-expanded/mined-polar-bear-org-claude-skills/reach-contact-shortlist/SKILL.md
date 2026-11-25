---
name: reach-contact-shortlist
description: Builds a contact shortlist for one organisation, with the roles that live with the problem, the people publicly named in those roles with name, role and source only, the one or two you choose to write to and the warm path for each. Use for "run reach-contact-shortlist", "contact shortlist", "who should I contact at this company", "find the right person", "who would care about this", "who is the decision maker", "which role do I write to", "who to email at this company", part of the Claude Guide for Outreach Pack by 90n.
---

# Contact Shortlist

## When To Use
You know the company and not who there would care. So the message goes to the most senior name you can find, or to an info@ address. This answers: which roles live with the problem I help with, who is publicly named in them, and which one or two people do I choose?

## When Not To Use
If you want to know who you already know there, run Warm Path Check; that comes first. This skill does not research a person: once you have chosen someone, Identity Check and Person Research Brief do that.

## Inputs
- Your Company Research Brief, or the organisation's name and what you help with.
- The public pages to read: the organisation's own team or leadership page, press releases, a conference programme, an article that names people. Never LinkedIn.
- Your Warm Path Check for this account, if you have one.
If you have none of this, I start from the organisation's own website and your two-line brief, and mark the shortlist as a first draft.

## Approach
Roles in a buying decision, described generically: someone feels the problem, someone signs, someone can block, someone uses the work. You write to the role that lives with the problem, which is rarely the most senior name on the page. People are listed with name, role and source only, following the data minimisation principle the UK Information Commissioner's Office describes: hold the least personal data you need for your purpose. Rules on holding people's details vary; check with a qualified adviser. The failure it prevents: a careful message to a chief executive who forwards it to nobody.

## Workflow
1. Ask at most three questions: what problem you help with, which role felt it in your past work, and which public pages I may read.
2. Name the roles first, before any person: who feels the problem, who signs, who could block, who uses the work. Take them from your Ideal Client Profile where you have one, and mark each as "seen in my work" or "assumed".
3. Read the pages you pointed to, read only, and list the people publicly named in those roles. For each: name, role as the page states it, the link and its date. Nothing else.
4. Gather no email addresses, phone numbers, photos, career histories or personal profiles. If a role has no public name, write "no public name found": that is a result.
5. Add the warm path for each person from your own check: someone who could introduce you, or none.
6. You choose one or two people to write to and say why in a line about their role and the problem. I do not pick, order or compare the people.
7. Everyone you did not choose is deleted from the working list, not kept "for later".

## Output Format
```markdown
# Contact Shortlist
Organisation: [name] | Problem you help with: [one line] | Pages read: [number] | Date: [date]
## Roles that live with the problem
| Role in the decision | Why this role | Seen in my work or assumed |
|---|---|---|
| [feels the problem / signs / can block / uses the work] | [one line] | [seen / assumed] |
## People publicly named in those roles
| Name | Role as stated | Source (link, date) | Warm path |
|---|---|---|---|
| [name, or "no public name found"] | [role] | [link, date] | [who could introduce you, or none] |
## You chose
- [name]: [why this role, in one line]
## Decision
[Your name] chooses the one or two people to write to and deletes the rest of the list, by [date].
```

## Done When
- Roles were named before any person was looked for.
- Every person has a name, a role and a dated source, and nothing more.
- One or two people are chosen, by you, with a reason about the role.
- No contact details were gathered and unchosen names are removed.

## Quality Bar
- Organisation pages and other public pages only; nothing from LinkedIn, nothing behind a login, no enrichment.
- A role is a part in a decision, never a view of the person holding it.
- People are never ordered, compared or marked as more or less likely to answer.
- Points on holding personal data are questions for you: check with a qualified adviser.
- Claude lists public names with sources; you choose the people.

## Next
Run reach-identity-check (Identity Check) to confirm the research will be about the right person.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
