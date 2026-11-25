---
name: build-share-sign-off
description: Gather the three pre-share checks onto one page for a go or no-go, producing a record of what is shared and with whom, each check with its result as run, and the named person's yes or no with the date access ends. Use for "run build-share-sign-off", "can I send the prototype now", "who signs off the share", "go or no-go before the user test", "I need a yes before I send the link", "pre-share checklist for my prototype", "record that the checks were done", part of the Claude for Product Builders Pack by 90n.
---

# Pre-Share Sign-Off

## When To Use
The checks are done in your head and nobody has actually said "yes, send it". Run this as the last step before a link reaches testers, colleagues or leaders. It answers: what exactly is going out, what did the checks find, and who has agreed?

## When Not To Use
If a check has not been run, run it first: Secrets and Keys Check, Personal Data Check, Access and Sharing Check. This page runs no check of its own, so with nothing behind it there is nothing to sign.

## Inputs
- The outputs of the three checks, pasted or uploaded, with their dates
- What is being shared, with whom (by code or role), on which surface and until when
- The role and name of the person who can say yes
If you have none of this, I start from a description of what you plan to send and to whom, write every check as "not run", and mark the output as a first draft.

## Approach
A go or no-go record built on the four questions of the OWASP Threat Modeling Cheat Sheet (https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html): "What are we working on?" "What can go wrong?" "What are we going to do about it?" "Did we do a good enough job?" They become the four sections of the page. The judgment is in the last one: it is answered by a person, never by the document. The failure this prevents: three careful checks, a link sent on a Friday, and on Monday nobody can say who agreed to it.

## Workflow
1. Ask up to three questions: what is being shared and with whom, where are the three check outputs, and who is the person who says yes?
2. Fill "What are we working on": what is shared, with whom, on which surface, until when. One prototype and one audience per page. A second audience is a second page.
3. Fill "What can go wrong" from the three checks only: keys, personal data, access. Each gets its result as run and its date. A check not run is written "not run", never passed. A check run before the last change to the prototype is written "run before the last change".
4. Fill "What are we going to do about it": anything real that remains and why, then for each risk who would notice a problem and how. "Nobody would notice" is a valid and useful row.
5. Leave "Did we do a good enough job" empty. I fill in the record from the checks; I never write the yes. The named role answers yes or no and dates it. Security points on the page: check with your engineering or security lead.
6. If the answer is no, list what must change and which check is run again. If yes, copy the end date from the access check and the role who removes access. No name, no share.

## Output Format
```markdown
# Pre-Share Sign-Off
Prototype: [name] · Prepared by: [role] · Date: [date]
## What are we working on?
| What is shared | With whom (code or role) | Surface | From | Until |
|---|---|---|---|---|
| [prototype, flow] | [T1 to T5] | [surface] | [date] | [date] |
## What can go wrong?
| Check | Result as run | Date run | Run after the last change? | Open items |
|---|---|---|---|---|
| Keys, passwords and tokens | [result or "not run"] | [date] | [yes / no] | [items] |
| Personal data | [result or "not run"] | [date] | [yes / no] | [items] |
| Access and sharing | [result or "not run"] | [date] | [yes / no] | [items] |
## What are we going to do about it?
| What real thing remains | Why it stays | What could go wrong | Who would notice, and how |
|---|---|---|---|
| [item or "nothing real remains"] | [reason] | [risk] | [role and signal] |
## Did we do a good enough job?
| Answer | Given by (role and name) | Date | Conditions |
|---|---|---|---|
| [yes / no, written by the approver] | [approver] | [date] | [conditions or "none"] |
## Decision
[The approver, by role and name, says yes or no to this share by [date]. On yes, access ends on [date] and [role] removes it. On no, [role] fixes [items] and the page is prepared again. Check with your engineering or security lead.]
```

## Done When
- The page names one prototype, one audience and one end date
- All three checks appear with a result as run, or the words "not run"
- The yes or no was written by the approver, with a date, and covers this prototype, this audience and this date range only

## Quality Bar
- No new check is run here: a gap sends you back to the check it belongs to, and "not run" or "run before the last change" is never rounded up to a pass.
- The approver is named because they decide. Nobody else is named, and the page does not say who caused a failed check.
- The page records a decision. It is never a statement that the prototype is safe or secure.
- Nothing holding real customer data or a live key is shared until a named person has checked it and said yes on this page.

## Next
Run build-test-recruitment-note (Tester Recruitment and Consent Note) to find five real target users and get their consent.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
