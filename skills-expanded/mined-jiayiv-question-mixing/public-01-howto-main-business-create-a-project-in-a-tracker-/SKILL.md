---
name: create-a-project-in-a-tracker
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 10min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Create a project in a tracker so work has a named home, owner, scope, and starting workflow.

## Preconditions

- You can access the project tracker.
- The project name, owner, team, and basic purpose are known.
- You know whether the project should be public to the workspace or limited to specific members.

## Steps

1. **Open the project area.** [BRANCH: Jira | Asana | Linear | generic] open Projects in Jira, Teams or Portfolios in Asana, Projects in Linear, or the workspace project list in a generic tracker. → *Expect:* the project list or project creation button is visible.
2. **Start a new project.** Choose New project, Create project, or Add project. → *Expect:* a project setup form opens.
3. **Enter the project identity.** Add the project name, short description, owner, team, and key if the tool asks for one. → *Expect:* the form identifies the project clearly.
4. **Choose the workflow.** Select a template, board type, issue status set, or default task workflow. → *Expect:* the project has statuses or sections for tracking work.
5. **Set access.** Add the people or groups who should view or edit the project. → *Expect:* only intended members are listed.
6. **Create the project.** Save or create the project. → *Expect:* the new project opens with an empty board, list, or issue view.
7. **Add a starter task.** Create one task for kickoff, planning, or backlog capture. → *Expect:* the project can accept work items.

## Decision points

- If the project is temporary → use a lightweight template and avoid custom fields.
- If the project spans teams → add shared viewers before work begins.
- If naming conventions exist → match the prefix, key, or portfolio structure.

## Failure modes & recovery

- **F1 Duplicate project:** detect by a name or key conflict warning → recover by opening the existing project or choosing the approved unique name.
- **F2 Missing permission:** detect a disabled create button or access error → recover by asking a workspace admin or project admin to create it.
- **F3 Wrong visibility:** detect unintended members or public access → recover by editing project permissions immediately.

## Verification

The tracker shows a project whose name matches the filename-level request, with an owner, workflow, intended access list, and at least one starter task.

## Variations

- [BRANCH: Jira | Asana | Linear | generic] Jira may require project keys and schemes; Asana emphasizes teams and templates; Linear emphasizes team, status workflow, and project lead; generic trackers usually ask for name, owner, and members.

## Safety & privacy

Project titles and descriptions may expose customer, roadmap, or staffing details. Use neutral names when visibility is broad.
