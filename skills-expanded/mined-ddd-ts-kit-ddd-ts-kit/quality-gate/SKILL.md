---
name: quality-gate
description: >-
  Use before closing a slice or opening a pull or merge request, to merge the trunk into a
  branch, when asked whether the work is clean, done or ready, when a check, the guard or
  the pipeline reports a violation, or for a TODO(review).
allowed-tools:
  - Read
  - Edit
  - Bash(npm run verify)
  - Bash(npm run typecheck)
  - Bash(npm run lint *)
  - Bash(npm test *)
  - Bash(npm run test:coverage)
  - Bash(npm run test:e2e *)
  - Bash(npm run docs:check)
  - Bash(npm run regenerate)
  - Bash(npm run docs:generate)
  - Bash(npm run depcruise)
  - Bash(npm run deadcode)
  - Bash(npx ddd-ts-kit check *)
  - Bash(npx ddd-ts-kit verify-slice *)
  - Bash(npx ddd-ts-kit verify-merge)
  - Bash(npx ddd-ts-kit verify-merge *)
  - Bash(npx ddd-ts-kit merge-trunk)
  - Bash(npx ddd-ts-kit merge-trunk *)
  - Bash(npx ddd-ts-kit check)
  - Bash(npx ddd-ts-kit todo *)
  - Bash(npx ddd-ts-kit todo)
  - Bash(npx ddd-ts-kit status)
  - Bash(npx ddd-ts-kit story-check *)
  - Bash(npx ddd-ts-kit docs)
  - Bash(npx ddd-ts-kit explain *)
  - Bash(npx ddd-ts-kit acceptance *)
---

# Quality gate

The size and message of the commit are skill `ddd-ts-kit:commit-discipline`.

## Scope the run

| When | Run | Cost |
|---|---|---|
| after each write | nothing: the guard runs `check-file` and returns the violations (under the regulated profile it runs no program of the project: `npx ddd-ts-kit check` here, the pipeline and the commit gate hold it) | none |
| while iterating | `npx ddd-ts-kit verify-slice <context> --since <base>`: regenerate, the rules on the changed files, the specs of the context, the files near the size limit and the paths of the slice to stage (the pages of `docs/behaviour/` and the schema of the ORM the generator changed for the context included), in one run; a path it leaves out is never staged with the slice | seconds |
| before the commit that closes a slice | the two above, `npm run typecheck`, `npm run lint`, `npm run format:check` (`npm run format` settles it), `npx ddd-ts-kit todo <context> --brief` (nothing left but `TODO(review)`), `npx ddd-ts-kit check --commit-size` | under a minute |
| to bring the trunk into the branch | `npx ddd-ts-kit merge-trunk`: one merge commit from the branch's own diff, derived files settled, `verify-merge` on the result before its commit; on a stop, resolve each hunk keeping both sides, `git add`, `merge-trunk --continue` ("Bring the trunk in" below) | seconds |
| after a merge made otherwise | `npx ddd-ts-kit verify-merge`: each line, row done or test the merge lost, to restore from its side; it exits 1 on one (the pre-push hook and `verify-slice` run it too, and only warn in this version). A migration of the branch that sorts before the trunk's last always fails it, with the command that reorders it | a second |
| before a merge or a pull request | `npm run verify`, on the branch with the trunk merged in; each non-blocking remark of the review written as a `TODO(review)` or settled | everything |
| before the code of a story | `npx ddd-ts-kit acceptance <story> --gate written`: every slice row and criterion has a scenario, wrapped in `pending(...)`, locked and committed | seconds |
| before a story or a milestone is closed | `npx ddd-ts-kit story-check <code>` (`M1` for the rows `M1.*`): every row `done`, no marker of its own left; exits 1 with each blocker, why it is the story's, its `file:line` and its fix; then `npx ddd-ts-kit acceptance <story> --gate passing`: no scenario pending nor drifted from its lock, and each amendment it lists reported to the owner | seconds |

Layout is settled in this order: `npm run format`, then `npm run lint:fix`. Biome wraps a long
line, and the lint then asks for a blank line around the statement that now spans several lines:
that new finding is expected, never a conflict between the two. Never Prettier nor a bare
`npx biome` (without `--no`, it can fetch an unrelated package of that name); the guard refuses
both to a worker.

`npm run lint` (`ddd-ts-kit lint`) fails on a warning as on an error: fix it the same way. An
entry of `eslint-suppressions.json` is a finding the project recorded: once it is fixed the lint
fails until `npx eslint . --prune-suppressions` removes it; adding one (`--suppress-all`,
`--suppress-rule`) is a suppression.

`check --changed-since` judges the changed files, and the findings whose cause is a changed file
(a handler not registered in the module file, an adapter not wired, a use case not declared:
they sit on one file and are repaired in another, and the `subjects` of the JSON name it) only: a cycle, an unused export or a rule
broken by the combination with the trunk escapes it, which is why the last run is `verify`, on
the whole tree, after merging the trunk. `npm run verify` chains types, lint, format, every spec with the coverage thresholds
(`npm run test:coverage`), end-to-end tests, the architecture rules, the import graph
(dependency-cruiser), dead code (knip) and documentation drift. Use
`npm run typecheck`, never `npx tsc`: the project compiles with the native compiler.
`npx ddd-ts-kit status` counts the `TODO(domain)`, `TODO(platform)`, `it.todo` and
`TODO(review)` left in each context: a gate is not passed while the slice still has one of the
first three.

## Bring the trunk in

When the rows of a branch are committed and the trunk moved, before its review and its merge, read [merge-trunk.md](merge-trunk.md) first: `npx ddd-ts-kit merge-trunk` only, never `git merge` alone; resolve each hunk it stops on keeping both sides, then `--continue`.

## Review remarks

For the findings of a review, a `TODO(review)` marker or the closing of a story, read [review-remarks.md](review-remarks.md) first: a blocking finding is fixed before the merge, a non-blocking one is settled at once or written as `TODO(review): #<row id> <remark>`.

## Coverage

When `npm run test:coverage` fails on a threshold, read [coverage.md](coverage.md) first: write the spec that reaches the lines, never an `exclude` or a `v8 ignore`.

## Read a violation

Each carries a rule id, a `file:line`, a message and a `fix` sentence. Open that file at that
line only. `npx ddd-ts-kit explain <rule-id>` gives the reason and a good and a bad example;
`check --explain` adds the reason of every rule a run reports, once each, without a call per rule.

| Rule family | Usual root cause | Fix |
|---|---|---|
| `layer/*` | logic or a type in the wrong layer | move it, or a port in `application/ports/` and an adapter |
| `context/*` | a context reaching into another | a contract in the upstream's `published-language/`, an integration event, a declared relationship (skill `ddd-ts-kit:context-map`) |
| `tree/*`, `naming/*` | a file made by hand | `ddd-ts-kit generate`, then move the logic |
| `language/*` | a name outside the glossary | the business word, or the term added first (skill `ddd-ts-kit:glossary`) |
| `ports/*`, `declarations/*`, `composition/*` | wiring by hand | skill `ddd-ts-kit:wiring`; a stale barrel is `npx ddd-ts-kit docs` |
| `domain-events/*` | a handler or an adapter dispatching events itself; a `before-commit` handler depending on a gateway, an external port, `Cache`, `Lock`, `RateLimiter`, `JobScheduler` or `EventBus` | `await repository.save(aggregate)` and nothing else: the unit of work dispatches at its end; `phase: 'after-commit'` when the effect may be lost, an integration event when it must not |
| `authz/*` | a use case without a permission, a right decided in the wrong layer | skill `ddd-ts-kit:access-control` |
| `events/*`, `scheduling/*` | a contract outside the published language, a consumer without a name, a job doing work | skill `ddd-ts-kit:integration-event`; a job only sends a command |
| `purity/*`, `clean/*` | a hidden dependency, unclear code | skill `ddd-ts-kit:clean-code` |
| `aspects/*`, `tracing/*`, `standard/*` | a technical concern inside business code | skill `ddd-ts-kit:cross-cutting` |
| `governance/*`, `config/*` | a suppression or a config entry without its reason or record | skill `ddd-ts-kit:deviation` |
| `test/*` | behaviour without a test, or a mock | skill `ddd-ts-kit:testing` |
| documentation drift | generated files not regenerated | `npm run regenerate`, commit them with the code |
| `event-sourcing/*`, `unrecorded ...` or `formerly recorded ... in stored-events.lock.json` from `docs:check` | a state change outside an apply method, a stored shape changed in place, a stored version not recorded, or recorded by 0.82.0 or earlier | skill `ddd-ts-kit:persistence`; a changed stored shape is a new version with its upcaster, and an unrecorded or formerly recorded one is recorded by `npx ddd-ts-kit docs --stored-events` (once final), never by hand |

Five ids are held by ESLint (`domain/*`, `application/*`): `npm run lint` reports them.

## Not without the owner's explicit agreement

A suppression, a lowered severity, a wider allow-list, an extra directory, a relaxed
pipeline, `any`, a non-null assertion, a skipped or deleted test, an acceptance scenario changed
while its criterion was not: skill `ddd-ts-kit:deviation`. Getting to green is never the
reason. A baseline of the errors (`check --baseline write`) is written by the owner, in a
terminal, never by you: the guard refuses it. `check --baseline prune` needs no agreement: it only
lowers what the baseline holds, after a fix.

## Report

The commands run and their real result, in a few lines. A failing gate is reported as
failing, with what remains and why.
