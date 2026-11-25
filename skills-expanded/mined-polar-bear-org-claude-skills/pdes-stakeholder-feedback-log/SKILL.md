---
name: pdes-stakeholder-feedback-log
description: Builds a Stakeholder Feedback Log that puts every review comment in one table by role and objective, merges duplicates, sets conflicts side by side for the person who decides, proposes accept, decline or park with a reason, flags comments that undo an earlier round and drafts a reply per stakeholder. Use for "run pdes-stakeholder-feedback-log", "stakeholder feedback log", "sort design review feedback", "conflicting stakeholder comments", "three stakeholders gave opposite notes", "this round undoes the last one", "which feedback do I act on", "reply to review comments", part of the Claude for Product Designers Pack by 90n.
---

# Stakeholder Feedback Log

## When To Use
Three stakeholders gave three opposite notes and the next round undoes the last. Run it the day after a design review, before you move a single frame. It answers: which comments do I act on, which conflicts need a ruling, and who gives it?

## When Not To Use
If the notes came from a peer crit, use Critique Notes to Actions; a crit has no approver and you make the call on each note yourself. If one request is something you object to, such as a deceptive pattern, it needs more than a row in a table: use Design Pushback Brief.

## Inputs
- The comments as they were made, from chat, email, file comments or your notes, each with the role of the person who made it
- The objectives agreed for this work, and who approves it (by role), if you know
- The log or the list of accepted changes from earlier rounds, if this is not the first
If you have none of this, I start from the raw comments, mark the objectives and the Approver `[to confirm]` and mark the output as a first draft.

## Approach
Feedback triage against agreed objectives and one named Approver, using the roles of DACI from the Atlassian Team Playbook: a Driver gets a decision made by the date, one Approver makes the final decision, Contributors have a voice and no vote, the Informed are told afterwards. The log needs only the Approver named. The judgment behind it is that you are not the referee between two people who outrank you. The failure it prevents: round three brings back the card layout that round two removed, because both notes were "accepted" and nobody saw that they cancel out.

## Workflow
1. Ask up to three questions: what objectives were agreed for this work, who is the Approver, and is there an earlier round to check against?
2. One row per comment, verbatim where you pasted it, or a close paraphrase marked `[paraphrase]`. Each row gets its source by role and the objective it touches, or "none stated". A long message is split into its separate asks. I add no comment that nobody made.
3. Merge duplicates into one row and keep every role that raised it. Four roles saying the same thing is one item, and the Approver should see that it was four.
4. Find the conflicts: two comments that cannot both be done. Each goes to the Approver side by side, with the objective each one serves. You do not pick a winner, and neither do I.
5. Propose a status per row for you to confirm: accept, decline (the reason tied to an objective, a principle or evidence) or park (with a revisit date). "Prefer" is not a reason, on either side.
6. Check against earlier rounds. If a comment would undo a change already accepted, flag it for the Approver with the round it reverses.
7. Draft a short reply per stakeholder: what changes, what does not and why, what is waiting on the Approver. You read each one, correct it and send it yourself.

## Output Format
```markdown
# Stakeholder Feedback Log
**Review:** [name, date] | **Objectives:** [numbered list] | **Approver:** [role or to confirm] | **Round:** [number]
## Comments
| # | Source (roles) | Comment (verbatim or [paraphrase]) | Objective touched | Proposed status | Reason or revisit date |
|---|---|---|---|---|---|
| [1] | [role, role] | [comment] | [objective or none stated] | [accept / decline / park] | [reason] |
## Conflicts for the Approver
| Topic | Comment A (role) | Comment B (role) | Objective each serves | Approver's call |
|---|---|---|---|---|
| [topic] | [comment] | [comment] | [objectives] | [blank until decided] |
## Undoes an earlier round
| Comment # | Accepted change it reverses | Round |
|---|---|---|
| [#] | [change] | [round] |
## Replies to send
- [Role]: [what changes, what does not and why, what is with the Approver]
## Decision
[Approver, by role] rules on each conflict and each reversal by [date]; [designer] confirms the other statuses and sends the replies by [date].
```

## Done When
- Every comment is in the table with a source role and an objective or "none stated"
- Every conflict shows both sides and sits with the Approver
- Every decline has a reason and every park has a revisit date
- Reversals of earlier rounds are flagged, or the log says no earlier round was supplied

## Quality Bar
- Comments are logged by role; there is no tally of who gives good or bad feedback
- A decline cites an objective, a principle or evidence, never seniority
- The Approver's column stays blank until the Approver decides
- Replies state facts and next steps, never blame
- Claude logs only comments people made; conflicts go to the person who decides.

## Next
Run pdes-design-pushback-brief (Design Pushback Brief) for the requests you cannot accept.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
