---
name: update-a-project-timeline
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

Update a project timeline so dates, dependencies, and stakeholder expectations reflect current reality.

## Preconditions

- You can edit the project timeline, roadmap, or schedule.
- Current task status, blockers, and date changes are known.
- Stakeholders who must approve major changes are identified.

## Steps

1. **Open the timeline view.** [BRANCH: Jira | Asana | Linear | generic] open Timeline, Roadmap, Project milestones, or the generic schedule view. → *Expect:* project dates and dependencies are visible.
2. **Review current status.** Compare completed, in-progress, blocked, and not-started work against the existing dates. → *Expect:* schedule gaps are visible.
3. **Update task dates.** Adjust start dates, due dates, milestone dates, or target dates for affected work. → *Expect:* the visual timeline reflects current estimates.
4. **Check dependencies.** Move dependent tasks or mark dependency conflicts caused by date changes. → *Expect:* downstream effects are visible.
5. **Add a change note.** Document what changed, why, and who approved or requested it. → *Expect:* the timeline history explains the update.
6. **Notify stakeholders.** Share the revised dates and any decision needed. → *Expect:* stakeholders know the updated schedule.

## Decision points

- If the change affects a committed external date → get approval before publishing the new timeline.
- If estimates are uncertain → mark dates tentative and add a review checkpoint.
- If dependencies create a conflict → escalate the tradeoff instead of hiding the dependency.

## Failure modes & recovery

- **F1 Timeline changed silently:** detect stakeholders surprised by dates → recover by posting a change note and update summary.
- **F2 Dependency broken:** detect dependent work starts before prerequisite work ends → recover by adjusting dates or adding a blocker.
- **F3 Wrong scope moved:** detect unrelated tasks shifted during drag editing → recover by reviewing changed items and reverting only the incorrect dates.

## Verification

The project timeline shows updated dates, dependency impacts, and a written explanation or notification for the change.

## Variations

- [BRANCH: Jira | Asana | Linear | generic] Jira Advanced Roadmaps and Asana Timeline emphasize date ranges; Linear emphasizes project target dates and milestones; generic tools may use Gantt or calendar views.

## Safety & privacy

Low risk. Timeline updates may affect commitments and staffing expectations, so document approval for major changes.
