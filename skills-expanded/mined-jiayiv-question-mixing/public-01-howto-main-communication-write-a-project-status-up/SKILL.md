---
name: write-a-project-status-update
domain: communication
locale: [generic]
interface: web
difficulty: basic
est_time: 30min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Write a project status update that gives stakeholders current state, risks, decisions needed, and next actions without requiring a meeting.

## Preconditions

- A project with known scope, owner, dates, and stakeholders.
- Current information on milestones, blockers, decisions, and metrics.
- A shared channel, email thread, doc, or project tracker where updates belong.

## Steps

1. **Start with a status line.** Write "Status: Green/Yellow/Red" plus one sentence explaining schedule, scope, and confidence. → *Expect:* readers know the project state immediately.
2. **Summarize progress.** List the concrete work completed since the last update, using artifacts or metrics where possible. → *Expect:* stakeholders can see movement.
3. **Name risks and blockers.** State each risk, impact, owner, and date when it must be resolved. → *Expect:* unresolved issues are visible early.
4. **Call out decisions needed.** Use "Decision needed: approve X by Friday so Y can proceed." → *Expect:* decision-makers know exactly what action is required.
5. **List next actions.** Include owner, action, and due date for each near-term task. → *Expect:* the update creates accountability.
6. **Use consistent labels.** [BRANCH: internal update | client update] use internal project names for internal readers; translate jargon and remove internal blame for clients. → *Expect:* the update fits the audience.
7. **Send to the right audience.** Share in the agreed channel and tag only people who need to act or stay informed. → *Expect:* stakeholders receive it without unnecessary noise.
8. **Archive the update.** Link it from the project tracker or status doc. → *Expect:* future readers can find the update history.

## Decision points

- If the project is off track → state impact, recovery plan, and decision needed in the first few lines.
- If there is no change → send a brief no-change update with the next checkpoint.
- If leadership is the audience → lead with business impact before task detail.
- If information is uncertain → label it as an assumption and state when it will be confirmed.

## Failure modes & recovery

- **F1 Update hides bad news:** detect risks buried at the bottom → move risk and ask into the summary.
- **F2 Too much detail:** detect long task narration → link details and keep the main update scannable.
- **F3 No owner:** detect actions without names → assign owner and date or mark "owner needed."

## Verification

The update states green/yellow/red status, completed work, current risks, decisions requested, named next actions, and a date for the next update.

## Variations

- Executive update: use fewer bullets and emphasize impact, timeline, and decisions.
- Engineering update: include release, dependency, incident, and technical risk links.
- Client update: avoid internal blame and state what changes for the client.

## Safety & privacy

Low risk unless confidential roadmap, customer, financial, or personnel information is included. Share only with the intended audience.
