---
name: build-access-check
description: Record who can open a prototype link today and narrow it before testers arrive, producing the current sharing setting read off the screen, a list of what travels with the link, and an end date with the role who removes access. Use for "run build-access-check", "who can open my prototype link", "I pasted the link in a channel", "is my artifact public", "how do I share with testers only", "what sharing setting should I use", "when do I take the link down", part of the Claude for Product Builders Pack by 90n.
---

# Access and Sharing Check

## When To Use
You pasted the link in a channel and do not know who else can now open it. Or you are about to send it to testers and have not looked at the Share control since the day you made the prototype. It answers: who can open this today, what comes with it, and when does that stop?

## When Not To Use
Not for what is inside the prototype: real names and emails belong to Personal Data Check, and keys to Secrets and Keys Check. Not for the yes itself: Pre-Share Sign-Off records the named person's decision. This check is who can open it and for how long.

## Inputs
- The sharing setting as it reads on screen right now, copied word for word from the Share control
- Where the link has already been pasted or sent
- The testers by code or role, how many, and the date the test round ends
If you have none of this, I start from the surface the prototype was made on and the list of people who need it, and mark the output as a first draft.

## Approach
Three sources. Anthropic's help pages describe the sharing settings for artifacts and for Claude Design (https://support.claude.com/en/articles/9547008-publishing-and-sharing-artifacts ; https://support.claude.com/en/articles/14604416-get-started-with-claude-design). OWASP Top 10 2025 puts Broken Access Control first, as A01 (https://top10.owasp.org/2025). The GOV.UK Service Manual asks that a prototype shared online is protected so the public cannot find it and take it for the real service (https://www.gov.uk/service-manual/design/making-prototypes). The failure this prevents: a polished prototype, open to anyone with the link, forwarded twice, and read by a customer as something they can have.

## Workflow
1. Ask up to three questions: what does the Share control say today, where has the link already gone, and who needs to open it and until what date?
2. State today's setting in the product's own words, read from the screen and not from memory: only you, specific people invited, your organisation, anyone with the link. Options differ by plan, so you read them off; I do not guess them.
3. For a Claude Design prototype, note that designs start private and that sharing gives view, comment or edit access. Testers get view. Anyone with edit can change what the next tester sees.
4. List what travels with the link: stored data, and on Team and Enterprise plans the files in the chat an artifact was made in. Each one is a row.
5. Pick the narrowest setting that still lets the five testers in. "Anyone with the link" needs a written reason and a person who accepts it. Check with your engineering or security lead.
6. Check the label: a visible "prototype, not the product" on every screen a tester or a forwarded reader can reach, not only the first one.
7. Set the end date and the role who removes access. Write what stopping does: unpublishing a chat artifact deletes its stored data and it cannot be published again, so anything worth keeping is saved first.

## Output Format
```markdown
# Access and Sharing Check
Prototype: [name] · Surface: [Claude Design / artifact] · Checked by: [role] · Date: [date]
## Who can open it today
| Question | Answer as read from the Share control |
|---|---|
| Setting, word for word | [setting] |
| Access level given | [view / comment / edit] |
| Where the link has been pasted | [places or "nowhere yet"] |
| "Prototype, not the product" label on every screen? | [yes / no, with the screens missing it] |
## What travels with the link
| Item | Present? | Action before sharing |
|---|---|---|
| Stored data | [yes / no / not known] | [action] |
| Files in the chat it was made in | [list or "none"] | [action] |
| Anything to save before access ends | [items] | [stopping deletes stored data and the published link] |
## Setting chosen and end of access
| Testers (by code or role) | Narrowest setting that lets them in | Reason if wider | Access removed on | Removed by (role) |
|---|---|---|---|---|
| [T1 to T5] | [setting] | [reason or "not wider"] | [date] | [role] |
## Decision
[The builder sets the narrowest setting by [date]; the engineering or security lead, by role, agrees any setting wider than named people before the link is sent. Check with your engineering or security lead.]
```

## Done When
- The current setting is quoted from the screen, with the date it was read
- The chosen setting is the narrowest that lets the testers in, or the wider one has a reason and a name
- An end date and a role who removes access are filled in, and the label is confirmed on every screen

## Quality Bar
- Settings are read off the Share control each time; plans differ and settings get changed.
- Testers appear by code or role in the record, never by name.
- A narrow setting is not a statement that the prototype is safe to show. It answers who can open it.
- The narrowest access that lets testers in, a prototype label on every screen, and a date access ends. Check with your engineering or security lead.

## Next
Run build-share-sign-off (Pre-Share Sign-Off) to put the three checks on one page for a named person's yes.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
