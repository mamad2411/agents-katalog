# Hosted multi-tenant implementation task contract

This directory contains the executable implementation plan for `../README.md`.
These instructions apply to every taskfile below this directory.

## 1. Canonical architecture and precedence

Before implementing any task, read:

1. `../README.md` sections 0, 5, 7, 30, 33, and 34.
2. `00-INDEX.md`.
3. The assigned `Txx-*.md` task completely.
4. Any package-local `AGENTS.md` covering files you will touch.

If a taskfile conflicts with the architecture decision register, stop and write
the conflict into the task result rather than silently changing the design.

The architecture decisions are intentional constraints. In particular:

- hosted mode is additive; standalone OpenFork must keep working;
- one tenant gets one hosted SQLite database initially;
- tenant credentials never fall back to ambient process-global auth or env;
- browser clients never talk directly to hosted OpenFork;
- directory/session IDs are selectors, not tenant authority;
- OS child-process isolation is independent of application tenant isolation;
- shared mode stays opt-in until the production-readiness closeout task passes.

## 2. Worktree and branch isolation

The OpenFork and PresGen repositories can both contain unrelated concurrent
work. Never assume a dirty path belongs to this campaign.

For concurrent execution:

- one implementation task = one dedicated branch/worktree per repository it
  modifies;
- record the base commit(s) in the task result before editing;
- inspect `git status` and focused diffs before touching an already-modified
  file;
- do not use broad `git restore`, `git checkout -- .`, `git clean`, or mass
  formatter commands;
- stage explicit paths only;
- do not amend or rewrite another task's commits;
- integration/merge conflicts are owned by the integration task, not hidden by
  choosing `ours`/`theirs` wholesale.

If a dedicated worktree is unavailable, serialize the tasks that share files.
Do not run them concurrently in one dirty checkout.

## 3. Scope discipline

Every taskfile has an **Owned surfaces** section. Treat it as a write lease, not
permission to refactor the neighborhood.

You may read anything needed to understand behavior. You may edit outside the
owned surfaces only when an unavoidable dependency is proven. If that happens:

1. record the extra path and reason in the result file;
2. inspect for concurrent changes first;
3. keep the change minimal;
4. notify the integration owner because ownership has changed.

Do not combine cosmetic cleanup, unrelated optimizations, or broad code-style
changes with security/isolation work.

## 4. Safety rules

Never weaken an existing security boundary to make a test pass.

Forbidden shortcuts include:

- request-time mutation of `process.env` or XDG globals to switch tenants;
- accepting caller-controlled tenant/directory headers as authority;
- one shared `auth.json` in hosted mode;
- raw provider secrets as cache keys, log fields, metric labels, or IDs;
- globally caching credential-bearing provider clients without a proven
  tenant-safe identity;
- reusing the current PresGen assumption that all events from one OpenCode
  process belong to one user;
- putting active SQLite WAL files on NFS/SMB for multi-node writers;
- making hosted mode the default before `T18` closes all mandatory gates.

If a requested feature cannot be made tenant-safe in the current task, disable
it in hosted mode and keep the per-session compatibility lane.

## 5. Performance rules

This campaign exists partly to remove duplicated server overhead, so security
patches must not casually replace process duplication with another unbounded
resource.

For new caches, queues, registries, streams, or pools:

- define ownership scope;
- define a bound or eviction policy;
- define cleanup/finalization;
- define cancellation semantics;
- define metrics or at least test-visible counters where meaningful.

Do not claim a performance improvement without a measured baseline and the
exact benchmark command/configuration.

## 6. Generated API rule

When changing OpenFork HTTP API surfaces, follow
`packages/opencode/AGENTS.md` exactly:

- protocol-only changes require `packages/client` generation;
- unified OpenFork route changes require `packages/sdk/js` generation;
- never hand-edit generated SDK output.

Generated files belong in the same task only when they are the required output
of that task's API change.

## 7. Validation hierarchy

Each task lists task-specific validation. In addition:

1. run the narrowest unit/integration tests for edited behavior;
2. run package type checks for edited TS packages;
3. run security/adversarial tests specified by the task;
4. run benchmark probes specified by the task;
5. only then run broader suites when cost is justified.

Record commands and pass/fail results. "Looks correct" is not validation.

If the environment prevents a required test, record the blocker and leave the
task gate open. Do not convert an unrun test into a pass.

## 8. Mandatory task result

Every implementation task must create or update:

`../results/<TASK-ID>.md`

with this structure:

```markdown
# <TASK-ID> result

## Status
PASS | PARTIAL | BLOCKED | FAIL

## Base commits
- OpenFork: <sha or N/A>
- PresGen: <sha or N/A>

## Commits
- <sha> <summary>

## Changed paths
- ...

## What changed
- ...

## Validation
| Command / probe | Result | Evidence |
| --- | --- | --- |

## Security / isolation evidence
- ...

## Performance evidence
- ...

## Deviations from taskfile
- none / ...

## Remaining risks / follow-ups
- ...

## Gate conclusion
<which exit criteria are actually satisfied>
```

Do not mark a task PASS until every mandatory exit criterion is satisfied.

## 9. Commit discipline

Prefer small, reviewable commits split by mechanism:

- tests/harness first when practical;
- substrate or API contract;
- implementation;
- generated output if required;
- docs/result evidence.

Commit messages should explain the architectural mechanism, not just the file
changed. Never stage unrelated dirty paths.

## 10. Handoff discipline

At task completion, include in the result file:

- exact downstream tasks now unblocked;
- any changed assumptions those tasks must know;
- new APIs/types they should use;
- compatibility flags and default values;
- benchmark/security evidence location;
- unresolved questions that require a human decision.

The next agent should not need private chat context to continue.

