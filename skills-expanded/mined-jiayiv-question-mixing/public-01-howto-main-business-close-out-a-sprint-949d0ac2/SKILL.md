---
name: close-out-a-sprint
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 20min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Close a sprint so completed work is recorded, unfinished work is handled, and the next planning cycle can start cleanly.

## Preconditions

- You can edit the sprint or iteration.
- The team has reviewed current task status.
- The next sprint, backlog, or holding area exists.

## Steps

1. **Open the active sprint.** [BRANCH: Jira | Asana | Linear | generic] open the active sprint, project section, cycle, or iteration view. → *Expect:* all sprint work items are visible.
2. **Review incomplete work.** Filter or scan for tasks not marked done. → *Expect:* unfinished work is identified.
3. **Confirm completed work.** Check that done items meet the team's definition of done. → *Expect:* only truly complete work is closed.
4. **Move unfinished work.** Send unfinished tasks to the next sprint, backlog, or explicit follow-up milestone. → *Expect:* no open task is stranded in the closed sprint.
5. **Record sprint notes.** Capture carryover, scope changes, notable wins, and blockers. → *Expect:* the sprint history explains the outcome.
6. **Close the sprint.** Use Complete sprint, Close cycle, or equivalent. → *Expect:* the sprint status changes to closed or completed.
7. **Share the closeout.** Post summary metrics, carryover, and follow-up items to the team. → *Expect:* the team has a shared record.

## Decision points

- If a done item lacks acceptance evidence → reopen or move it before closing.
- If carryover is large → flag planning or capacity issues for retrospective.
- If the tool asks where to move incomplete items → choose the next sprint only for committed follow-up work.

## Failure modes & recovery

- **F1 Closed with wrong items:** detect completed sprint contains incorrect done or open work → recover by reopening if possible or editing item sprint fields.
- **F2 Lost carryover:** detect unfinished tasks missing from next sprint or backlog → recover by searching the old sprint and moving them manually.
- **F3 No summary:** detect stakeholders asking what changed → recover by posting a closeout note with completed and carried work.

## Verification

The sprint is closed, done work remains recorded, unfinished work appears in the next sprint or backlog, and a summary is posted.

## Variations

- [BRANCH: Jira | Asana | Linear | generic] Jira uses Complete sprint; Linear uses cycles; Asana may use sections, milestones, or portfolios; generic trackers may use iteration status.

## Safety & privacy

Low risk. Closing a sprint changes reporting, so confirm status before closing if metrics are used externally.
