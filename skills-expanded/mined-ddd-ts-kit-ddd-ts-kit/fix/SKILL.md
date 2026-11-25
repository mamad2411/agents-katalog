---
name: fix
description: >-
  Repairs one defect in its own worktree, proof first: a spec reproducing it at its layer,
  locked (`ddd-ts-kit acceptance <code> --lock`) and committed before any code, then the fix
  and its pull request. Run by the user with /ddd-ts-kit:fix.
argument-hint: "<fix code> [the defect in plain words, an issue key, an incident record]"
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Skill
  - Agent
  - AskUserQuestion
  - Bash(npx ddd-ts-kit *)
  - Bash(cd * && npx ddd-ts-kit *)
  - Bash(cd * && npm run *)
  - Bash(cd * && npm test *)
  - Bash(cd * && git *)
  - Bash(git worktree *)
  - Bash(gh pr create *)
---

# Repair one defect, its proof first

Fix: `$0`. Defect: `$ARGUMENTS`

A fix is a story with one row and no design review: its proof is a spec written before its
code, that the agent repairing the code cannot rewrite. The shared parts (the worktree, the
provisional decisions, the report, the pull request) are those of the story skill,
[../story/SKILL.md](../story/SKILL.md): read its sections 0, 8 and "While working" once, and
apply them here. `npx ddd-ts-kit story $0` says at any time where the fix stands; the guard
keeps the code of the contexts closed until the lock of phase 2 exists.

## 0. Its worktree

From the checkout of the trunk, after `git fetch`: `npx ddd-ts-kit story-scope $0 --kind fix`
(`--from <file>` when the defect comes from an issue export or an incident record on disk).
Then every command is `cd <worktree> && ...`. Copy
[../story/story-template.md](../story/story-template.md) to
`docs/architecture/stories/$0.md`: `## Statement` is the defect as it was reported, what was
expected and what happened, with the id of the audit entry, the trace or the request when the
report gives one; no `## Acceptance criteria` and no rows unless the fix turns out to be a
story (then stop, and say so to the owner). The statement is the criterion every later
judgement reads: write it before anything else.

## 1. Reproduce

Find the layer of the defect before writing a line: `npx ddd-ts-kit describe <context>`
for the use case and its aggregate; the audit trail (`audit.<context>` entries, by the subject
of the request) or the trace (by its id) when the report names one; `git log -S` on the rule
that broke. Then write the failing spec at that level, with the patterns of skill
`ddd-ts-kit:testing`:

| The defect lives in | Write |
|---|---|
| an invariant, a transition | an aggregate spec, `given(...).when(...).thenError(...)` or `thenEvents(...)` |
| a use case, a permission, a reaction | a handler spec through the test application, the fakes of its ports |
| an adapter | an integration spec of that adapter, or a case of its contract suite |
| a route, a contract, a journey | an end-to-end spec, or a scenario of `test/acceptance/` |

Name it after the defect, its code first: `it('#$0 refuses a cancellation after the
appointment started', ...)`. Run it (`npm test -- <file>`): it fails on an assertion that
states the expected behaviour, never on a `TypeError` or a missing import. A test that passes
reproduces nothing: the layer, the data or the statement is wrong, not the test.

## 2. Lock

List each spec under `## Regression` of `docs/architecture/stories/$0.md`, one item per path
relative to the project root (`- test/unit/appointment.aggregate.spec.ts`, or the spec next to
the code). `npx ddd-ts-kit acceptance $0 --gate written` names what is left; then
Before locking, run the formatter and the linter of the project on the specs (`npm run format`,
then `npm run lint -- <spec files>`) and fix what they report: a locked spec is not touched
again, and the close fails on a spec that fails them (a blank line the padding rule wants, a test
over the size the lint allows, logic in a test). `--lock` runs both on those files and refuses
to lock while they fail. Then
`npx ddd-ts-kit acceptance $0 --lock` records the fingerprint of each test in
`test/acceptance/<code>.acceptance.lock.json`. One commit, the story file, the specs and the
lock together: `test(<context>): $0 reproduce <defect>`. The guard opens the code of the
contexts once the lock exists.

## 3. Fix

Change the code until the locked specs pass and nothing else fails: `npm test -- <file>`, then
`npx ddd-ts-kit verify-slice <context> --since <base>`. The locked specs do not change to make the code pass,
and a sub-agent never writes them: the guard refuses it, and `npx ddd-ts-kit acceptance $0`
reports a change since the lock as a drift that no verdict lets through. A spec that turns out
wrong (a wrong expectation, or one that fails the lint) is not edited to pass: compare it with
`## Statement`. You, the session of the fix, write the new version, run `npx ddd-ts-kit
acceptance $0` (it reports the change with its subject and fingerprint; a change of layout alone
needs no verdict), launch the `ddd-ts-kit:acceptance-judge` agent on it with that subject and
fingerprint, the statement of the fix being the criterion (correct the statement first when it is
what is wrong), and lock again with `--lock` once it wrote `Verdict: amend`; a `refuse` means
restore the spec (git). A host without the agents of the plugin asks the owner to write the verdict. Commit the
fix on its own: `fix(<context>): $0 <what was wrong>`.

## 4. Close

As the story skill closes (its section 7): the trunk brought in with `merge-trunk`, the
`architecture-reviewer` agent on the diff (`--changed-since <base>`), `npm run verify`,
`npx ddd-ts-kit acceptance $0 --gate passing` (each locked test present, unchanged and no
longer pending; the runner proves it passes). Then `## Report` in the story file, as the story
template has it: what the defect was, where the fix lives and what else the spec covers, under
`## Origin` the issue key or the incident record the fix answers, each `D<n>` decision, and
`### Verification` with the last lines of `npm run verify` and of the test run, or `not
verified` for what could not run. Commit, push the branch, `gh pr create` with the report as
its body; give the owner the link, then stop.
