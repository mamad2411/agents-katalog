---
name: propose-rule
description: Proposes a generic lesson learned as a change to the shared knowledge repository, by committing one proposal file on its own proposal branch in this sandbox's clone. Use when the user asks to remember a rule for every project, or a mistake reveals a missing global or role rule.
---

# Propose a rule for the shared knowledge

This sandbox reads its rules read-only and proposes changes through its own clone
of the knowledge repository at `~/knowledge`. The clone has `main` checked out;
every proposal is one file on its own branch `proposal/<date>-<slug>-<hex>`. You
can commit there. You cannot fetch or push; the host does that on the next sync:
a sandbox start, or `ai-knowledge sync --all` run by the user on the host.

## When

- The user says a lesson should apply everywhere, not just to this project.
- A mistake happened that a global or role rule would have prevented.

Project-specific lessons go to project memory or the project's own rule files, not
here.

## Procedure

1. Confirm the clone is on `main` and clean:
   ```bash
   git -C ~/knowledge branch --show-current     # main
   git -C ~/knowledge status --porcelain        # must be empty before you start
   ```
   If `~/knowledge` is missing, the knowledge repository is not configured on this
   host; tell the user and stop. If it is on a `proposal/*` branch, run
   `git -C ~/knowledge checkout main` first.
2. Check for duplicates and prior rejections. Grep `~/knowledge/rules/`,
   `~/knowledge/roles/` and `~/knowledge/decisions.md` for the key words of the
   lesson. If it exists or was rejected, tell the user and stop.
3. Decide the scope: `global` for every agent, `role/<name>` for one kind of agent
   (planner, implementer, reviewer), `skill/<name>` for a procedure.
4. Start the branch and write the file. `<slug>` is lowercase words joined by `-`;
   `<project-id>` is the second word of `~/knowledge/.git/ai-knowledge-role`.
   ```bash
   git -C ~/knowledge checkout -b proposal/tmp-<slug> main
   ```
   File `~/knowledge/proposals/<YYYY-MM-DD>-<slug>.md`:
   ```markdown
   ---
   scope: global
   project: <basename of the project directory>
   project_id: <project-id>
   machine: <output of hostname>
   target: rules/global.md
   evidence: <what happened, one paragraph, factual>
   ---

   # <Short imperative title>

   <The rule text exactly as it should appear in the target file.>
   ```
   Prose only. No tool-specific syntax, no line numbers, no project names inside
   the rule text itself.
5. Commit only that file, then give the branch its final name, which ends in the
   first four characters of the commit, and return to `main`:
   ```bash
   git -C ~/knowledge add proposals/<YYYY-MM-DD>-<slug>.md
   git -C ~/knowledge commit -m "proposal: <slug>"
   git -C ~/knowledge branch -m proposal/<YYYY-MM-DD>-<slug>-$(git -C ~/knowledge rev-parse --short=4 HEAD | cut -c1-4)
   git -C ~/knowledge checkout main
   ```
   A branch left as `proposal/tmp-...` is never pushed; finish the rename.
6. Tell the user the proposal is committed on its branch and reaches the remote on
   the next sync (a sandbox start, or `ai-knowledge sync --all` on the host), and
   that the integrator decides whether it enters `main`. Once it is closed, the
   host deletes the branch here on a later sync.

## Never

- Commit on `main`. A pre-commit hook refuses it in this clone; the host would
  refuse to push it anyway.
- Change anything outside `proposals/` on a proposal branch. The host refuses to
  push such a branch and the proposal is stuck until the change is reverted.
- Run `git push`, `git fetch`, `git rebase`, or delete branches.
- Put project-specific content in a proposal.
