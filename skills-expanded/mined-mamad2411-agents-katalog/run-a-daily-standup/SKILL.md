---
name: run-a-daily-standup
domain: business
locale: [generic]
interface: mixed
difficulty: basic
est_time: 15min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Run a short daily standup that surfaces progress, priorities, and blockers without turning into a full planning meeting.

## Preconditions

- The team, meeting time, and standup format are known.
- The current board, sprint, or task list is available.
- Someone is responsible for capturing blockers and follow-ups.

## Steps

1. **Open the work board.** [BRANCH: Jira | Asana | Linear | generic] open the sprint board, project list, Linear team view, or generic task board. → *Expect:* current work is visible.
2. **Start on time.** State the focus: yesterday or last update, today's priority, and blockers. → *Expect:* participants know the format.
3. **Go person by person or work item by work item.** Ask for brief updates and keep discussion to facts. → *Expect:* progress and plans are heard quickly.
4. **Capture blockers.** Record each blocker with an owner and follow-up action. → *Expect:* blockers do not disappear after the meeting.
5. **Park deep discussions.** Move detailed design, debugging, or planning topics to follow-up conversations. → *Expect:* the standup stays within the timebox.
6. **Confirm next actions.** Repeat owners for blockers, handoffs, and urgent tasks. → *Expect:* everyone knows what happens after standup.
7. **Update the board.** Move tasks, adjust owners, or add notes discovered during standup. → *Expect:* the tracker matches the team's current state.

## Decision points

- If many blockers appear → schedule a separate unblock session immediately after standup.
- If updates are stale → ask people to update the tracker before the next standup.
- If remote participants cannot attend → use an async written standup with the same prompts.

## Failure modes & recovery

- **F1 Meeting drifts:** detect detailed debates during standup → recover by parking the topic and naming a follow-up owner.
- **F2 Blockers lack owners:** detect blockers listed without follow-up → recover by assigning an owner before ending.
- **F3 Board is outdated:** detect task status contradicting verbal updates → recover by updating the tracker during or immediately after the meeting.

## Verification

After the standup, the board reflects current work and every blocker has an owner, next action, and follow-up path.

## Variations

- Async standup: collect written updates by a deadline and only meet for blockers.
- Kanban team: walk the board from blocked or closest-to-done work backward.
- Support team: include queue health, urgent tickets, and handoff risks.

## Safety & privacy

Low risk. Avoid discussing sensitive customer, HR, or security details in channels where not all attendees should hear them.
