---
name: archive-a-completed-project
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 15min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Archive a completed project so active views stay clean while the project record remains retrievable.

## Preconditions

- You can edit or archive the project.
- The project is complete or formally canceled.
- Required closeout notes, files, and final status are available.

## Steps

1. **Open the project.** [BRANCH: Jira | Asana | Linear | generic] open the project, board, initiative, or workspace project page. → *Expect:* project settings and task lists are accessible.
2. **Confirm completion state.** Check that tasks are done, moved, or intentionally left open elsewhere. → *Expect:* no active work will be hidden by archiving.
3. **Add closeout notes.** Record outcome, final links, owner, and where follow-up work lives. → *Expect:* future readers can understand why the project ended.
4. **Check access and exports.** Save any required reports, files, or audit links before archiving. → *Expect:* required records remain available.
5. **Archive the project.** Use Archive, Close, Complete, or equivalent project setting. → *Expect:* the project leaves active lists and shows archived or completed status.
6. **Notify stakeholders.** Share that the project was archived and where to find records or follow-up work. → *Expect:* stakeholders know the project is no longer active.

## Decision points

- If open work remains → move it to another active project or backlog before archiving.
- If the project may restart soon → use completed or paused status instead of archive if that is the team convention.
- If records are needed for audits → export or link final reports before archiving.

## Failure modes & recovery

- **F1 Active work hidden:** detect tasks missing from active planning after archive → recover by reopening the project or moving tasks to an active location.
- **F2 Archive option unavailable:** detect no archive control → recover by asking a project admin or using the team's completed status.
- **F3 Lost reference material:** detect final docs or reports unavailable → recover by restoring the project or retrieving links from history.

## Verification

The project is marked archived or completed, active work has been moved or closed, and closeout notes identify final records and follow-up locations.

## Variations

- [BRANCH: Jira | Asana | Linear | generic] Jira may use archived projects or released versions; Asana has project archive; Linear has completed or canceled projects; generic tools may use status fields.

## Safety & privacy

Low risk. Archiving can hide work from active views, so confirm no live operational task depends on the project remaining visible.
