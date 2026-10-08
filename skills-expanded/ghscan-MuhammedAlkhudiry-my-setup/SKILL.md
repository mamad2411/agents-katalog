---
name: saved-work
description: Use to save, resume, update, or archive a plan, interview result, or progress tracker; for deliberately postponed work use $tech-debt.
---

Save documents as `~/plans/<project>/<slug>.md`. Use the project's lowercase name, not a worktree or clone folder name. In a connected repository
without that folder, use the repository's existing plan location. When no writable location exists, return the complete document and state that it
was not saved.

Preserve the supplied content. Start each file with `created`, `updated`, `project`, `description`, `status`, and `type` frontmatter, and refresh
`updated` on every save.

## Types

- `plan` for work to do. This is the default.
- `interview` for a completed interview's decisions.
- `tracker` for progress through work that spans sessions, such as a review, walkthrough, or upgrade.

## Status

- Use `pending` for work that has not started, `progress` for work currently underway, and `done` for completed work.
- To archive a `done` document, move it into the project's `archive/` folder.
