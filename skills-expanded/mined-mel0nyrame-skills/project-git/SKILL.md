---
name: project-git
description: Use when reviewing Git changes, committing, pushing, recording Git delivery, or delivering explicitly requested PR/MR updates.
---

# Project Git

Perform the authorized delivery stages. Commits, pushes, PR/MR publication, and external tracker edits have separate scopes; a request for one stage does not authorize later stages.

## 1. Inspect scope and evidence

Read applicable repository, subtree, contribution, and Git rules. Inspect `git status --short --branch`, unstaged changes, and staged changes. Identify this task's changes and preserve other work.

Resolve title format and language through [naming conventions](references/CONVENTIONS.md#select-conventions). Reuse validation that still covers the current diff; run focused checks when evidence is missing or invalidated. Report only checks actually run and their results.

Check changed prose against current repository facts and references, and affected decisions against their rationale and implementation. Use `project-prose` or `project-adr` for deeper review when available; these checks and required project checks still apply without them.

## 2. Commit the requested changes

Group changes by intentions that can be explained and reverted independently. Keep tests, lockfiles, migrations, and generated outputs with the source they support. Before committing on an ordinary project's default branch, switch to a compliant work branch. Coordinate renaming pushed or shared branches explicitly.

For each group:

1. Stage explicit paths or interactive hunks.
2. Review the staged stat and full diff. Confirm one intention, the resolved title convention, and absence of secrets, debug residue, conflict markers, or accidental artifacts.
3. Commit with hooks enabled; inspect the commit and remaining working tree.

Include repository-required delivery records with their implementation. Read [recording conventions](references/TRACKER.md) when linking delivery records or changing an authorized tracker. A commit-only request ends with the commit result, validation, and remaining changes.

## 3. Push the requested commits

Follow pre-push rules. Verify remote, target branch, upstream, and outgoing commits; establish the normal upstream on the first push. Reuse still-valid checks unless policy requires another run.

Keep hooks enabled. Force pushes, history rewrites, and remote-ref deletion need explicit target-and-scope authorization. On failure, preserve a recoverable state and report completed actions, sanitized errors, and the smallest repair.

## 4. Deliver requested PR/MR changes

Use the external [pr skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/pr) for the body and project conventions for the title. Report a missing writing dependency as an incomplete step.

Create or update the request through available platform tools using the authorized repository, base, head, and scope. If platform access is unavailable, retain the draft and report the gap. Verify the hosted result before reporting completion or a PR/MR URL. Comments and other tracker writes require their own explicit scope.
