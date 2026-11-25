---
name: acct-call-notes
description: Writes up sales call notes from your typed or dictated notes, readable on a phone, with what the customer said in their words, weak signals, commitments on both sides, the dated next step and what is missing. Use for "run acct-call-notes", "call notes", "sales call notes", "meeting notes from my customer call", "write up my call", "call summary", "clean up my notes", "notes after a customer meeting", part of the Claude for Account Executives Pack by 90n.
---

# Sales Call Notes

## When To Use
Your notes get written on Friday from memory and nobody reads them. Run this straight after a meeting, in person, on video or by phone: paste what you typed or dictated. It answers: what was said, who committed to what, and what is the next step?

## When Not To Use
To change the fields in your CRM, run CRM Update. To write to the customer, run Meeting Recap Email: these notes are internal. For the week as a whole, run Weekly Manager Update.

## Inputs
- Your raw notes, typed or dictated and pasted, in any order.
- The account, the date, the format, and who attended by name and job role.
- The objective you had going in (your Sales Call Plan, if you made one).
If you have none of this beyond the notes, I start from the notes alone and mark the output as a first draft.

## Approach
Notes built to decide and act, a common practice described here generically, in six parts: context, objective, what the customer said, weak signals, commitments, dated next step. Notes exist so that you, your manager and whoever covers the account can act on them, not to prove that work happened. The failure it prevents is the line nobody can use: "good call", "customer interested", "will follow up".

## Workflow
1. Only if the essentials are missing, I ask at most three questions: account, date and format; the objective of the meeting; the next step that was said out loud.
2. I sort your notes into the six parts. Nothing is added to what the notes say; a part with nothing in it reads "not in the notes".
3. The customer's words go in quotation marks only if they appear as such in your notes. Otherwise I paraphrase and mark it "paraphrased", with the speaker's job role.
4. Each stock phrase ("good call", "seemed keen", "will follow up") is replaced by the fact that justifies it, or by "to clarify" with the question for you.
5. Weak signals are things you observed (a new name mentioned, a date that moved, a question about terms), marked "to verify". They are observations about the deal, never a reading of someone's mood or character.
6. Each commitment becomes who, what, by when, on both sides. One with no owner or no date is flagged.
7. The dated next step goes on top, lines stay short enough for a phone, and the last section lists what is missing as questions for you. With Salesforce in Claude (beta) I can propose attaching the notes to the account; nothing is written without your approval. Any other CRM takes them by copy and paste.

## Output Format
```markdown
# Sales Call Notes
[Account] · [date] · [in person / video / phone] · [attendees, job roles]
## Dated step ahead
[Who] does [what] by [date]
## Context and objective
- Context: [context]
- Objective: [objective] · met: [yes / partly / no]
## What the customer said
- "[words from your notes]" ([job role])
- [idea] (paraphrased, [job role])
## Weak signals
- [observed fact] (to verify)
## Commitments
| Who | What | By when |
|---|---|---|
| [customer, job role] | [commitment] | [date] |
| [you] | [commitment] | [date] |
## To clarify
- [question for you]
## Decision
[You] reread and approve these notes today, and decide what goes into the CRM.
```

## Done When
- No stock phrase is left.
- Every commitment has an owner and a date, or is flagged, and the dated next step is on top.
- Every quotation appears word for word in your notes.

## Quality Bar
- Facts and the customer's words first; my interpretations are marked "to verify".
- No judgment of the customer's people: job roles, dated words, facts.
- Personal data is limited to what following the deal needs; if in doubt, check with a qualified adviser.
- Short: if the notes cannot be read in a minute, I cut.
- Nothing is added to what your notes say: what is missing is marked, never invented.

## Next
Run acct-crm-update (CRM Update) to carry these notes into your CRM without typing them twice.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
