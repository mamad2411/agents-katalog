---
name: yolo-brief
description: Use to record a new feature in a YOLO repo, or to cancel one. Writes workspace/features/<slug>/brief.md with a goal and checkable success criteria, taken from an approved design spec when one exists. Triggers on "track this as a feature", "write a brief for X", "track it from that spec", "yolo brief", "cancel the X feature". Does not plan or build anything.
---

# yolo-brief

Record what a feature is and how you'll know it works. Designing, planning and building
happen however you like; this skill only writes the brief. Rules: `../../yolo/conventions.md`.

## Procedure
1. **Derive the slug** (conventions *Naming*). Before writing, check for an existing match:
   list `workspace/features/*`, compare case-insensitively, and scan existing briefs' `goal`
   for the same change (slugs drift: `csv-export` vs `export-csv`).
   - Match found → don't write a second brief. Show that feature's status (`yolo-status`)
     and update the existing brief only if the user is changing its goal or criteria.
   - Slug taken by an unrelated feature → suffix it and say so.
2. **Look for a design spec.** Use one if the user points to it, if
   `workspace/features/<slug>/spec.md` exists in this checkout or on the feature branch
   (`git show feature/<slug>:workspace/features/<slug>/spec.md`), or if a spec for this
   feature was written and approved earlier in this conversation. Read it before writing
   anything.
3. **Fill the brief** from `../../yolo/templates/brief.md`:
   - `goal`: one sentence on what the user can do once it ships.
   - `success_criteria`: observable, checkable behaviors. With a spec, take them from its
     acceptance criteria, requirements or testing section, rewording any that can't be
     checked. Ask the user only about gaps. Without a spec, ask one short question if the
     user hasn't said how they'd know it works. Vague criteria make `yolo-verify` useless.
   - `refs`: repo-relative paths to the spec and plan (by convention
     `workspace/features/<slug>/spec.md` and `plan.md`, which may live only on the feature
     branch) and any ticket.
   - `milestone`, `depends_on`: only if the user mentions them.
   - `created_at`: the current time, ISO 8601 UTC, with real hours and minutes.
4. **Commit** it alone: `git add workspace/features/<slug>/brief.md && git commit -m "yolo: brief <slug>"`.
   Status is now `planned`.
5. **Hand over.** Tell the user the next step is theirs, and print the two lines they need
   (if `feature/<slug>` already exists, e.g. the spec was written there, print
   `git switch feature/<slug>` instead of creating it):

   ```
   git switch -c feature/<slug> <base_branch>
   /goal feature/<slug> has a commit "yolo: verify <slug>" with trailer YOLO-Verified: true, and the yolo-verify output shows each success criterion in workspace/features/<slug>/brief.md as met with real test or command output; no existing test was deleted or weakened; or stop after 30 turns. Work: implement <slug> from its brief, test-first, then run yolo-verify.
   ```

   The goal line is optional: it keeps the session working until verification passes. The
   checker only reads the conversation, which is why the line demands real output, guards
   the tests and caps the turns. Suggest a larger turn cap for big features.

## Cancel
Set `cancelled: true` in the brief's front-matter and commit (`yolo: cancel <slug>`). Never
delete a brief.

## Constraints
- Writes only `brief.md`. No branches, no specs, no plans, no code.
