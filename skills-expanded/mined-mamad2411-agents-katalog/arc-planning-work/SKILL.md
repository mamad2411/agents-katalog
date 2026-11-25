---
name: arc-planning-work
description: Implementation planning for existing tracked work items. Use when asked to plan an existing GitHub issue, Agile Accelerator story, or PRD before coding begins. Produces ordered tasks, file-level changes, test strategy, acceptance-criteria mapping, and synchronized docs/<ID>-IMPLEMENTATION_PLAN.md plus docs/<ID>-progress.txt artifacts. Do not use to create new user-story backlogs.
---
# Arc Planning Work

Create implementation plans before coding. The leading word is **read-before-plan**: inspect the work item and relevant code before proposing tasks.

For the shared plan template, load [PLAN_FORMAT.md](PLAN_FORMAT.md). For destination-specific commands, load [GITHUB_MODE.md](GITHUB_MODE.md), [AGILE_ACCELERATOR_MODE.md](AGILE_ACCELERATOR_MODE.md), or [PRD_MODE.md](PRD_MODE.md) after mode detection. For synchronized `docs/` plan and progress artifacts, follow `arc-implementation-plan-progress/references/output-contract.md`.

## Steps

1. **Detect the planning source.**
   - GitHub mode: issue number/URL, `#123`, or explicit GitHub issue request.
   - Agile Accelerator mode: `W-000000` work item or Salesforce Agile Accelerator story.
   - PRD-to-plan mode: the user asks for an implementation plan from an existing PRD document.
   - If ambiguous, ask where the work item is tracked before planning.

   Completion criterion: the plan has exactly one source mode, or the response stops with a destination/source clarification question.

2. **Read the source item.**
   - Fetch the issue/story/PRD body and comments where relevant.
   - Preserve the source's acceptance criteria, constraints, and context.
   - Do not create new stories/issues; this skill plans existing work.

   Completion criterion: every acceptance criterion or scenario from the source is available for mapping, or missing source access is reported as a blocker.

3. **Analyze the codebase.**
   - Read files referenced by the work item.
   - Search for related components, routes, models, tests, docs, and similar implementations.
   - Identify dependencies, risks, and likely test locations.

   Completion criterion: every planned task cites concrete files/areas or explicitly states why the file path is unknown.

4. **Draft the implementation plan.**
   - Use ordered, atomic tasks.
   - Include specific file changes and test strategy.
   - Map each acceptance criterion to one or more tasks and verification methods.
   - Name the feature branch using the source ID when available.

   Completion criterion: another agent can implement the plan without re-discovering scope or asking basic sequencing questions.

5. **Publish the plan to the source.**
   - GitHub: comment on the issue.
   - Agile Accelerator: append to `agf__Details__c` and update status where appropriate.
   - PRD-to-plan: write `./plans/<feature>.md` or the user-specified plan path.
   - Update sprint plan docs if the repo has a matching `docs/sprints/` plan.

   Completion criterion: the plan is posted/written to the requested destination, or the exact permission/tooling blocker is reported.

6. **Create synchronized `docs/` plan and progress artifacts.**
   - Resolve `<ID>` from the source work item: use the tracked ID when available (e.g. `W-000025`, `issue-42`), otherwise a short kebab-case slug from the work item title.
   - Ensure `docs/` exists in the project root.
   - Write `docs/<ID>-IMPLEMENTATION_PLAN.md` following `arc-implementation-plan-progress/references/output-contract.md` (map the drafted plan into required sections: product goal, baseline, milestones with acceptance criteria, risks, and immediate next steps).
   - Create or update `docs/<ID>-progress.txt` with `arc-implementation-plan-progress/scripts/init_progress_txt.sh docs/<ID>-IMPLEMENTATION_PLAN.md docs/<ID>-progress.txt`, or follow the contract template manually when the script is unavailable.
   - Keep both `docs/` artifacts synchronized with what was published in step 5.

   Completion criterion: `docs/<ID>-IMPLEMENTATION_PLAN.md` and `docs/<ID>-progress.txt` exist with the same `<ID>` prefix and synchronized phase coverage.

## Boundaries

- Use `arc-creating-user-stories` to create new GitHub issue backlogs of user stories.
- Use `arc-defining-work` to create new work items across destinations after asking the user where to create them.
- Use `arc-prd-to-issues` when the target output is new GitHub issues from a PRD, not an implementation plan.
- Do not start coding until the user approves the plan.
