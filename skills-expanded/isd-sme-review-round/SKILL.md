---
name: isd-sme-review-round
description: Runs one review round of a course, producing the review brief for the gate, a comment sheet by lane, a consolidated comment table with conflicts set side by side for the decider, a change log and the reply to reviewers. Use for "run isd-sme-review-round", "consolidate these review comments", "two reviewers contradict each other", "comments arrived in four formats", "a reviewer reopened the objectives", "write the brief for this review round", "reply to the reviewers with what changed", "which comments are out of scope for this gate", part of the Claude for Instructional Designers Pack by 90n.
---

# SME Review Round

## When To Use
Comments arrive in four formats, two of them contradict each other, and one reopens the objectives. Use this for one round at one gate: before it, to tell reviewers exactly what to check, and after it, to turn what they sent into decisions. It answers one question: what do the reviewers say at this gate, and what do we do about it?

## When Not To Use
Setting the gates, the lanes and the decider once for the whole build is Review and Sign-Off Plan; this runs a single round under those rules. A short list of factual flags for the expert comes from AI Content Accuracy Check. The final gate on record is Release Sign-Off Record.

## Inputs
- The gate this round belongs to, the version under review, and the review plan if there is one.
- The reviewers by role and lane, and the name of the decider.
- After the round: every comment, pasted or attached in whatever form it came (tracked changes, emails, chat messages, notes from a call).
If you have none of this, I start by asking who decides, draft the brief from the version you describe, and mark the output as a first draft.

## Approach
The method is gate discipline: a build passes through a design proof, an alpha, a beta and a gold review, and each gate asks a narrower question than the last. The judgment is in holding that question when a senior reviewer wants a wider one. The failure this prevents is familiar: at beta, one comment rewrites an objective signed weeks ago, another asks for the opposite on the same screen, the designer quietly does both, and the course ships later and worse with nobody having decided anything.

## Workflow
1. Ask up to three questions: which gate this is, who the decider named in the plan is (if there is no plan, this name comes first), and what is already signed and not open.
2. Write the brief before the round: the gate and the one question it asks (design proof: right structure and treatment, on one sample; alpha: is the full content right; beta: were the corrections made, does it work in the real delivery setting; gold: defects only), each reviewer's lane, what is settled, the deadline, and how to comment: one comment, one place, one request. With it goes a comment sheet per lane (place, what is wrong, what you propose, must or should). Claude drafts both; you send them.
3. After the round, put every comment into one table, whatever format it came in. Merge duplicates and keep which roles raised them. Sort each: in lane and in scope, out of lane, or out of scope for this gate. Out-of-scope comments go to the change rule (more time, more budget or a cut elsewhere, chosen by the sponsor): parked with an owner, not lost and not slipped in.
4. Set conflicts side by side, both positions in the reviewers' own words. Claude never settles one and never blends the two into a compromise. The decider does, with a reason.
5. Fill the change log as decisions come back, then draft the reply telling reviewers what was done with what they sent.

## Output Format
```markdown
# SME Review Round
Course: [name, version] | Gate: [design proof / alpha / beta / gold] | Round [n] | The one question at this gate: [question] | Consolidated by: [designer, role], [date] | Decider: [name, role]
## Review brief
Comment sheet, one per lane, columns: place, what is wrong, what you propose, must or should.
| Reviewer (role) | Lane: what you check | Already settled, not open | Comments due |
|---|---|---|---|
| [role] | [accuracy of sections x to y] | [signed objectives, version] | [date] |
## Consolidated comments
| No. | Place | Comment (merged) | Raised by (roles) | Sorting (in lane and scope / out of lane / out of scope for this gate) |
|---|---|---|---|---|
| [1] | [screen] | [comment] | [roles] | [sorting] |
## Conflicts for the decider
| Place | Position A, in the reviewer's words (role) | Position B, in the reviewer's words (role) | Decider's ruling | Reason |
|---|---|---|---|---|
| [screen] | [quote] | [quote] | [decider fills] | [decider fills] |
## Change log
Out of scope for this gate, sent to the change rule: [comment, what it would reopen, cost in time, budget or a cut, sponsor's choice]
Reply to reviewers: [what was changed, what was not and why, what is parked and with whom, what the next gate will ask]
| Comment no. | Decision (accept / reject / park) | Reason | Decided by (role) | Done in version |
|---|---|---|---|---|
| [1] | [decision] | [reason] | [role] | [version] |
## Decision
Round consolidated by [designer, role] on [date]. [Decider name, role] rules on every conflict by [date]; [sponsor, role] chooses time, budget or a cut for each out-of-scope item by [date].
```

## Done When
- Every comment received appears in the table, merged or alone, with its sorting.
- Every conflict shows both positions and has a ruling with a reason, or is open with a date.
- Every comment has a line in the change log (accept, reject or park), and the reply to reviewers matches it line for line.

## Quality Bar
- A comment is never dropped for being late, out of lane or awkward; it is sorted and answered, and a signed item reopens only through the change rule, in writing.
- Comments are listed by role. There is no count or ranking of who commented most, late or wrongly.
- Legal or compliance comments that need a ruling go to the named reviewer for that lane: check with a qualified adviser.
- Claude consolidates the comments and never settles a conflict: the named decider does, and every comment gets an answer.

## Next
Run isd-learner-pilot-test (Learner Pilot Test) to put the corrected course in front of real learners.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
