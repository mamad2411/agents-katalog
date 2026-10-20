---
name: set-a-project-milestone
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 8min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Create or update a project milestone so a major delivery point has a name, target date, and linked scope.

## Preconditions

- You can edit the project.
- The milestone name and target date are known.
- The tasks or issues that belong to the milestone are identifiable.

## Steps

1. **Open the project plan.** [BRANCH: Jira | Asana | Linear | generic] open Versions or Releases in Jira, Milestones or Goals in Asana, Project milestones in Linear, or the project roadmap in a generic tracker. → *Expect:* milestone or release controls are visible.
2. **Create the milestone.** Choose New milestone, Add release, or similar. → *Expect:* a milestone form opens.
3. **Enter milestone details.** Add the name, target date, owner, and short outcome statement. → *Expect:* the milestone describes a concrete delivery point.
4. **Link relevant work.** Attach tasks, issues, epics, or sections that make up the milestone scope. → *Expect:* the milestone shows related work items.
5. **Save the milestone.** Commit the milestone or release record. → *Expect:* the milestone appears on the project timeline, roadmap, or milestone list.
6. **Share the update.** Post a brief note in the project channel or tracker comments. → *Expect:* stakeholders know the milestone exists and what it covers.

## Decision points

- If the target date is uncertain → mark it tentative or use a planning milestone.
- If scope is larger than one milestone → split into smaller milestones with separate outcomes.
- If the milestone is externally promised → confirm the date with the accountable owner before saving.

## Failure modes & recovery

- **F1 Milestone too vague:** detect a name like "Phase 2" with no outcome → recover by adding a deliverable-focused name and description.
- **F2 Missing linked work:** detect an empty milestone scope → recover by adding the tasks or documenting that scope is still pending.
- **F3 Date conflict:** detect a target date that conflicts with the timeline → recover by adjusting the date or escalating the conflict.

## Verification

The project shows a milestone with a name, target date, owner or responsible team, and linked work items.

## Variations

- [BRANCH: Jira | Asana | Linear | generic] Jira often represents milestones as versions or releases; Asana may use milestones as task types; Linear supports project milestones; generic tools may use roadmap markers.

## Safety & privacy

Low risk. Milestone names and dates can reveal roadmap intent, so restrict visibility for sensitive launches.
