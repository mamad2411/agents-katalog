---
name: pre-work-gate
description: "Checks that a real, assigned, in-scope issue backs a change before the first edit; advisory, skipped when the repo has no tracker. Use when starting implementation, a fix or refactor. Not for tracker calls (use github-issues or jira-tracker); not for branch names (use branch-and-title-conventions)."
allowed-tools: Bash(git branch --show-current), Bash(printenv CLAUDE_TICKET_PATTERN)
license: MIT
---

# Pre-Work Gate

Before the first change to the repository, confirm that a tracked item backs the work and
covers what was asked. Checking first costs one question; finding out afterwards costs a
retroactive item written from memory.

This gate is advice. A skill cannot stop an edit; only a hook can, and this plugin ships none.
So the gate works by asking before acting, and the user can always choose to proceed without an
item. When they do, record that choice in the summary line and carry on.

## When it applies

Any task that changes the repository: writing or editing code or config, creating a branch or
worktree, fixing a defect, refactoring, or bumping a dependency.

It does not apply to read-only work: exploring or explaining the code, reviewing someone else's
change, triage or grooming in the tracker, or reading logs, build output or plans. If unsure,
run it; a needless check costs one lookup.

## Procedure

1. **Is there a tracker?** Read the `Tracker` row of the `## Issue tracker` section in the
   project's `CLAUDE.md` (template: `references/tracker-config.md` in the `tracker-discipline`
   skill).
   - `none`: say once per session "No issue tracker configured for this repo; skipping the
     pre-work gate." and stop here.
   - Section missing: continue to step 2. If no key turns up anywhere, ask once whether this
     repo tracks work in an issue tracker, and treat "no" as `none` for the rest of the session.
     Offer to record the answer in `CLAUDE.md`.

2. **Find the key.** Resolve the ticket pattern (the `Ticket pattern` row, else
   `printenv CLAUDE_TICKET_PATTERN` in Claude Code, else `[A-Z][A-Z0-9]+-[0-9]+`; details in
   `tracker-config.md`). Then look, stopping at the first match:
   - the current branch (`git branch --show-current`);
   - the user's message;
   - earlier in this session.

3. **Fetch the item.** A key proves someone typed a string, not that an item exists. Fetch it
   through the adapter the `Tracker` row names (`github-issues:issue-lifecycle-github`,
   `jira-tracker:jira-issue-lifecycle`) or a connected tracker tool. If none is available, use
   the pasted-issue path below.

4. **Print the summary** before doing anything else, using the template below.

5. **Check the four properties.** Each failure gets the action in the table; nothing proceeds
   until it is resolved or the user overrides it.

   | Property | Passing means | On failure |
   | --- | --- | --- |
   | Exists | The tracker returns the item. | Ask which item this work belongs to. |
   | Assigned | It has an assignee, and that is whoever is doing the work. | Offer to assign it, or confirm the user means to work on someone else's item. |
   | Workable | Its state is `ready` or `in-progress` (states: `tracker-discipline`). | Offer to move it to `in-progress` with a start comment; from `done`, `declined` or `parked`, ask first. |
   | Parented | It has a live parent, or is itself top level. | Propose a parent using the `tracker-discipline` parenting rules. |

6. **Check scope.** Compare the item's description with the request. If the request falls
   outside it, say so and offer a new item or an explicit widening of this one. Leave the
   decision to the user, because one item quietly covering three changes loses its history.

7. **No key found** (and a tracker exists): ask for it, or offer to search for an existing item
   or create one under the `tracker-discipline` dedupe and parenting rules. Attach the work to a
   plausible item only after the user confirms it.

## Summary template

```
[<KEY>] <title>
State: <core state> (<tracker's name>) · Assignee: <name | unassigned> · Parent: <KEY | none | top-level> · Source: <tracker | pasted>
Gate: <PASS | FAIL: <properties> | SKIPPED: no tracker | OVERRIDDEN: <user's reason>>
```

`Gate` takes exactly one of those four values. `FAIL` lists the failing properties, including
`scope`.

## Work from a pasted issue

Use this when the tracker cannot be reached: no adapter installed, no connected tool, the tool
call is denied, or a web or Cowork session without a tracker connector.

1. Ask the user to paste the item's title, state, assignee, parent and description.
2. Run steps 4 to 6 on that text, with `Source: pasted`.
3. Any state move, assignment or comment the gate calls for: print it for the user to apply, and
   say it is not recorded until they confirm.

## Examples

<example>
User: "Add retry logic to the ingestion worker." Branch `feature/PROJ-123-async-intake-pipeline`.

```
[PROJ-123] Async intake pipeline
State: in-progress (In Progress) · Assignee: dana · Parent: PROJ-100 · Source: tracker
Gate: FAIL: scope
```

Reply: "This branch is for PROJ-123 (async intake pipeline). Retry logic in the ingestion worker
looks outside that scope. Open a separate item, or widen PROJ-123 to cover it?" Then wait for
the answer.
</example>

<example>
User: "Fix the typo in the signup error message." Branch `main`, no key in the message, and the
`Tracker` row says `jira-tracker`.

Reply: "Which issue does this belong to? I can search for an existing one on 'signup error
message' or create one under the current UX bucket." If the user says "just fix it, no ticket",
proceed and print `Gate: OVERRIDDEN: user chose to proceed without an item`.
</example>

<example>
User: "Rename the helper in utils.py." The project `CLAUDE.md` has `| Tracker | none | … |`.

Say "No issue tracker configured for this repo; skipping the pre-work gate." once, then do the
work. Later tasks in the same session skip the gate without repeating the line.
</example>

## Verify

Before the first edit, check that:

- the summary was printed and its `Gate` line holds one of the four values;
- every failed property has either been resolved (and the item read back to confirm) or been
  put to the user as a question;
- for `PASS`, the item's state is now `in-progress` and a start comment exists (or, from pasted
  data, both were printed for the user to apply).
