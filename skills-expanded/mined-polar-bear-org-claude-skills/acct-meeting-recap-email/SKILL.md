---
name: acct-meeting-recap-email
description: Drafts the meeting recap email to the customer, with what you understood of their situation, what each side committed to with dates, one next step and one check question, internal notes kept out. Use for "run acct-meeting-recap-email", "recap email", "meeting recap email", "follow-up email after a meeting", "summary email to the customer", "confirm what we agreed in writing", "email after a sales call", part of the Claude for Account Executives Pack by 90n.
---

# Meeting Recap Email

## When To Use
The customer no longer remembers what was agreed when you follow up. Run this after a meeting, the same day. It answers: how do you confirm in a few lines what each side committed to do?

## When Not To Use
The internal write-up, with your weak signals and assumptions, is Sales Call Notes: this email goes to the customer. After a proposal has been sent, run Proposal Follow-Up.

## Inputs
- Your call notes from the meeting.
- The recipients on the customer side, by name and job role, and who to copy.
- An email you already wrote to this customer, if you have one, so the draft keeps your tone.
If you have none of this, I start from the commitments and the next step as you dictate them, and mark the output as a first draft.

## Approach
A recap of mutual commitments with a question that invites correction: common practice, described generically. You write what you understood, what each side promised and what comes next, then ask the customer to put you right. A commitment confirmed in writing holds better than a memory, and the check question makes the email an exchange and not minutes. The failure it prevents: the follow-up that opens with "as agreed" on a point the customer never took in.

## Workflow
1. I ask at most three questions: who receives it and who is copied, what tone you have with this customer, and whether there is a point that should not be put in writing.
2. I sort the notes: what goes to the customer (the situation as understood, commitments, next step) and what stays internal (weak signals, assumptions, competitors named, your impressions, anything on price not yet agreed). Nothing internal crosses over, and I list what I held back so you can check.
3. What I understood: the customer's situation in two or three sentences, in their words where your notes have them.
4. What we agreed: commitments on both sides, each with who, what and by when. Yours come first.
5. Next step: one only, dated, with its owner.
6. One check question that invites correction ("have I summarised your situation correctly?"), not a closing push.
7. I read it against stock phrases: no "just following up", no "hope this finds you well", no flattery, no false urgency. You rewrite it in your own words and send it when you decide.

## Output Format
```markdown
# Meeting Recap Email (draft)
**To:** [name, job role] · **Copy:** [names]
**Subject:** Our meeting of [date]: recap and next step
Hello [name],
**What I understood**
[Two or three sentences on the customer's situation]
**What we agreed**
- On my side: [what], by [date]
- On your side: [who], [what], by [date]
**Next step**
[What], on [date], [who]
[Check question]
[Your sign-off]
## Held back as internal
- [item kept out of the email]
## Decision
[You] reread, rewrite and send this draft yourself, at the time you choose.
```

## Done When
- Nothing internal is in the email, and the held-back list is there to check.
- Every commitment has who, what and by when.
- There is one next step, and it is dated.
- The email reads in under a minute.

## Quality Bar
- I attribute to the customer no commitment that is not in your notes.
- No price, figure or deadline that is not in your notes.
- A plain tone and a plain sign-off; no familiarity you do not have with this person.
- Nothing is sent or scheduled: it is a draft.
- You reread it and send it yourself; nothing that was not said appears in it.

## Next
Run acct-proposal-brief (Proposal Brief) to prepare the proposal from what was agreed.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
