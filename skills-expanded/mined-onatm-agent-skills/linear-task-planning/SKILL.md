---
name: linear-task-planning
description: Use when generating, decomposing, creating, or updating implementation tasks in Linear through the official Linear MCP. Requires a reviewed preview before every mutation.
---

# Linear Task Planning

Turn approved engineering plans into clear, self-contained Linear issues. Use the official Linear MCP for discovery and mutations. Do not implement code or edit project files.

## Source Authority

Read only the project material needed for the requested scope. Resolve conflicts in this order unless the project says otherwise:

1. Accepted architecture decisions.
2. Architecture and component designs.
3. Roadmap phase gates and phase plans.
4. The user's current instruction.

Do not generate implementation work that depends on an unresolved decision. Create a decision or research issue only when the source plan explicitly allows it or the user approves it.

## Discover Linear Context

Use Linear MCP read tools before proposing work:

- Identify the workspace and candidate team.
- Find an existing project before proposing a new one.
- Read available statuses, labels, milestones, cycles, and issue relationships.
- Search for matching issue titles and source identifiers to prevent duplicates.
- Ask the user when team or project placement is ambiguous.

Never invent Linear IDs, status names, labels, projects, or relationships.

## Decompose Work

Generate tasks from one approved phase, work package, or implementation plan at a time.

- Target roughly half a day to three engineering days per issue.
- Split work above five days or work containing independent contracts.
- Preserve prerequisite order and capability gates.
- Prefer a vertical, observable outcome over vague layer activity.
- Separate reusable harnesses, research decisions, persisted-format changes, and migrations when independently deliverable.
- Do not add speculative features, abstractions, or compatibility work.

Each issue must be implementable without hidden decisions and contain:

- Outcome.
- Scope.
- Non-goals.
- Prerequisites and dependencies.
- Affected contracts or components.
- Proposed implementation steps when established by source material.
- Failure cases.
- Required tests and benchmarks.
- Documentation impact.
- Acceptance evidence.

Include project-specific correctness requirements from contributor guidance and design docs. For database work, this may include crash recovery, deterministic concurrency, branch reachability, denied security paths, compatibility fixtures, or correctness-oracle benchmarks.

## Preview Before Mutation

Before creating or updating anything, show:

- Target team and project.
- Proposed issue titles and concise outcomes.
- Initial statuses, labels, and milestone or cycle placement.
- Parent, sub-issue, blocking, and related relationships.
- Existing issues that will be reused or updated.
- Ambiguities or decisions requiring review.

Ask for explicit approval. Read-only discovery does not require approval; every create or update does.

## Write Idempotently

After approval:

1. Recheck matching issues immediately before creation.
2. Reuse or update only confident matches.
3. Create issues with the approved descriptions and placement.
4. Add relationships only when supported by the source plan.
5. Do not assign owners unless explicitly requested.
6. Do not silently alter existing issue scope or status.

If a mutation partially fails, stop, report what succeeded with URLs, and propose the smallest recovery action. Do not retry creates blindly.

## Verify

Read the resulting Linear objects and confirm:

- Expected issue count.
- Titles and descriptions.
- Team, project, status, labels, and milestone or cycle.
- Parent and dependency relationships.
- No obvious duplicates.

Return a concise summary with issue URLs, skipped work, unresolved questions, and any verification gaps.
