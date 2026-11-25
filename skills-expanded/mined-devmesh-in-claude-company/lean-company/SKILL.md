---
name: lean-company
description: Run one small piece of work through this company with the hierarchy and the paperwork cut to the bone and every gate fully intact - the CEO dispatches a developer directly, writes a ten-line brief, dispatches one deliberate audit, and merges on green. Use ONLY when the user types /lean-company. Anything touching a frozen surface, a migration, auth or billing or money, an invariant, or a second workstream belongs in /company instead.
disable-model-invocation: true
---

# /lean-company - the fast door, same gates

Cuts hierarchy and paperwork. Never cuts gates. A fast path that drops
gates is Claude Code with extra steps, which everyone already has.

The work: $ARGUMENTS

## Wrong door - stop and run /company

Not initialized. Frozen surface. Migration. Auth, billing, or money.
Invariant. Second workstream. One-way: does not come back.

## The run

1. Short spec to `company/specs/spec-<slug>.md`, then a pointer brief to
   `company/briefs/brief-<slug>.md` (spec link, owned paths, outcome). The
   spawn prompt carries the spec path plus the paths - not a restatement.
   `guard_spec` requires the brief file; it also survives this session dying.
2. Targeted Edit adding your entry in `company/state/active-task.json`.
   Classify honestly (`quick` or `feature`). Never rewrite the whole file.
3. One `developer` in a worktree
   (`git worktree add .claude/worktrees/<slug> -b task/<slug>`). Two only
   on disjoint paths. No tech-lead.
4. QA only if there is a screen to drive (four states). Else the tests are
   the evidence.
5. One `auditor` on purpose, once, on the finished diff. Delegated worktree
   work does not arm the self-authorship audit, and lean mode deleted the
   lead. Dispatch it by hand.
6. Run the gates that cover the change, or the suites this project's
   `CLAUDE.md` names. If you already ran them this session, stamp and
   merge. Do not re-run because the stamp file is stale.
7. Merge. Remove ONLY your entry. One RESUME row. Report what shipped.

No spec, no PM, no architect, no tech-lead, no witness curation, no
docs-librarian, no report template, no retrospective.
