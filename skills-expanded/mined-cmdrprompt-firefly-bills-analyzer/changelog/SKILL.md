---
name: changelog
description: "Use when adding or reviewing a CHANGELOG.md entry for a task. Defines the behavior-first style, TASK-ID referencing, grouping rules, and when in the workflow the entry must exist. Keywords: changelog, CHANGELOG.md, release notes, behavior-first."
---

# Changelog entries

`CHANGELOG.md` describes shipped behavior, not internal task bookkeeping.
Entries go under the `## [Unreleased]` section, grouped by Keep a Changelog
category (`### Added`, `### Changed`, `### Fixed`, ...) matching the
surrounding file.

## Style rules

- Behavior-first language: state what was added, changed, or fixed from the
  user's or consumer's point of view, and why it matters.
- TASK-ID as a suffix reference only, e.g. `... by hand. (TASK-045)`. Never
  lead with the TASK-ID.
- Do not write an entry that only says a task was completed.
- Group related work into one bullet rather than one bullet per sub-task.
- Match the voice and level of detail of the existing entries in the file.

## Workflow rules

- The entry is written before staging: `CHANGELOG.md` must be updated and
  included on the task file's `**Stage:**` line (or staged explicitly) before
  `make stage-current-task` runs.
- A task is not done without a changelog entry. Reviewers verify the entry
  exists and quote it in their report.
