---
name: orchestration-methodology
description: "Orchestrate an Executor agent through the Architect/Executor pattern - discovery-first exploration, isolation before delegating, non-blocking parallel delegation, complexity-scaled monitoring/intervention, real verification (not just reading the report), and defect telemetry. Use when coordinating development work delegated to another agent."
---
<!-- GENERATED FROM SKILL.template.md — DO NOT EDIT BY HAND. Run generate_binding.py to regenerate. -->

# orchestration-methodology

This skill is for the **Architect** (the orchestrating AI) coordinating an
**Executor** (a fast, semi-autonomous coding agent) through discovery,
isolation, non-blocking parallel delegation, monitoring/intervention, and
issue tracking. Protocol-agnostic: whether the Architect drives the
Executor over MCP, a CLI wrapper, or by hand (see the sibling
`task-delegation` skill for the manual path), the six phases below are the
same methodology. Concrete tool names for a specific binding (e.g. Kilo
over MCP) live in that binding's own repo - see
[`kilo-mcp`](https://github.com/primax79/kilo-mcp)'s `mcp-orchestrator`
skill for the fully concrete version this skill was distilled from.

## Role discipline: delegate, don't implement

You are the architect/orchestrator, not the implementer. When a task is
scoped for delegation (a plan/macroplan task, or any request to "implement
X" that this skill's description matches), implementation work goes
through the delegation channel - not your own file-edit tools. This holds
even when a task looks small or fast to do yourself; "it's simple, I'll
just do it" is exactly how delegation gets silently skipped. If the delegation channel
is unavailable or fails, stop and say so instead of implementing in its
place - don't silently fall back to doing the work yourself.

The one exception is **verification-phase minor fixes**: while reviewing a
Final Report (Phase 5 below), you may correct a small, obvious issue
yourself directly in the Executor's worktree - a typo, a wrong import, a
misnamed variable - without a full round-trip. Anything bigger than a
handful of lines, or that touches actual logic, goes back to the Executor via
a corrective follow-up into the same session, not a direct edit. When
in doubt, delegate rather than fix it yourself.

## Logic and Behavior

- **Phase 1 - Discovery:** Explore the repository using the Executor's
  semantic search capability (if it has one) before designing solutions.
  Do not guess filenames. Confirm the Executor's engine/model and
  credentials are ready before dispatching anything.
- **Phase 2 - Isolation:** delegation typically has **no isolation and no
  locking by default** - it runs directly in the target working directory,
  and nothing stops a second concurrent writer (another delegated task, or
  your own `git` commands) from racing it in the exact same tree. This is
  not hypothetical: it has caused a real incident (a live git race that
  reset a branch and nearly dropped in-progress work while the orchestrator
  was doing its own git surgery in the same checkout the Executor was still
  committing to). Default to isolating:
  - Prefer a single delegation call that also creates isolation (e.g. a
    `isolation='worktree'`-style parameter) over a two-step
    create-worktree-then-delegate combo - one step, harder to forget.
  - Create the worktree standalone only when you need it to exist before
    deciding what to delegate into it.
  - Skip isolation only for a single trivial, quick edit - and even then,
    if the delegation response warns that another task is already running
    against that exact directory, treat it as a stop sign: wait for the
    other task, isolate, or pick a different directory. Never proceed past
    it assuming it's a false alarm.
  - The same risk runs in the other direction too: before running your
    **own** `git` commands (rebase, reset, checkout, history rewrites)
    against a directory, check whether a delegated task is still running
    there first - a still-running task in that `working_directory` is
    exactly the same hazard.
  - **Worktree isolation does NOT isolate shared host resources.** Two
    parallel isolated tasks (e.g. comparing two approaches on the same
    feature) still run on the same machine, sharing ports, container names,
    and any file each task's own tooling might write outside its worktree.
    Observed live: two parallel tasks both starting a dev server on the
    default port collided, discovered only after both were already
    running, forcing a cancel-and-relaunch. Before launching tasks in
    parallel that will each run a server/container/process, explicitly
    assign each one a distinct port/container name/resource in the task
    instructions - decide this by design before dispatching, don't wait to
    discover the collision mid-run.
  - **Worktree isolation does NOT isolate the repository's own configuration.**
    `.git/config` is shared by every worktree of a repo, so a delegated task that
    runs `git config` - or any tool that runs it on your behalf, e.g. `husky
    init` setting `core.hooksPath` - writes into the configuration the user's
    *own* checkout reads. Observed live: a lint-and-hooks task, correctly
    isolated in its own worktree, was one command away from installing a
    pre-commit hook on the user's working checkout of applications in daily
    production use, where a broken hook would have blocked their real commits.
    Any task that would touch repo-level configuration must be instructed to
    create the files and **document the activation command instead of running
    it**, and to prove it didn't by showing `git config --get <key>` returning
    empty. Activation is the user's call, not the task's.
- **Phase 3 - Delegation:** dispatch implementation work through the
  delegation channel. Prefer non-blocking delegation that returns
  immediately with a task handle - never block the conversation waiting on
  it. Pass whatever focus files were found during discovery, configure any
  skills/capabilities the task needs, and dispatch tasks in parallel across
  worktrees when independent. For work that spans multiple dependent steps
  or sessions, write it up first as a macroplan (see the
  `macroplan-authoring` skill) and delegate one task file at a time - each
  task file is already scoped, self-contained, and has its own
  verification section, which maps directly onto one well-formed
  delegation call.
- **Phase 4 - Monitoring & Intervention:** scale how closely you watch a
  task to its complexity/risk:
  - **Small, well-scoped tasks:** a single final-result check is enough.
  - **Large, multi-file, or high-risk tasks:** poll live progress
    periodically - prefer a source that reads the Executor's own live
    plan/commentary/cost, not just an OS-level heuristic (elapsed time,
    whether the process exists) - the latter tells you the task is running,
    not what it's actually doing.
  - **A "WORKING" verdict from the OS-level heuristic is not enough on its
    own - always cross-check it against cost/tokens/plan before trusting
    it.** That heuristic proves a socket is open to the model, not that the
    call is converging: a task can sit "connected, long call in progress"
    for many minutes while burning real cost on every turn. The tell is a
    low CPU-time/elapsed-time ratio (seconds of CPU across many minutes of
    wall clock - waiting on the network, not computing) combined with a
    ballooning cost/token count and no recorded plan, especially after a
    corrective delegation that resumed a prior session: it usually means
    the task is re-reading its own accumulated context every turn instead
    of acting on it. Observed live: a corrective delegation resuming a
    failed session ran 50+ minutes and \$7+ in cost with under two minutes
    of CPU time and no plan ever recorded - cancelled and redone directly
    rather than left to keep burning. Make this cross-check routine, not
    something reached for only once a task already looks slow.
  - **If a task drifts off-spec or looks stuck:** cancel it (a hard stop,
    not a graceful abort). Review the resulting workspace diff for partial
    changes, then either revert or continue with a corrective delegation
    call that resumes the **same session** - full memory of what was
    already built, instead of starting blind.
  - **Don't go idle after dispatching - check back proactively, don't wait
    to be asked.** Non-blocking delegation returning a task handle
    immediately means control comes back to you well before the work is
    done; if you just end your turn there, nothing polls the task until
    the user happens to ask "how's it going?" - observed live: a task that
    had already completed sat unreported until the user prompted a check.
    If your host exposes a self-scheduled wakeup mechanism, use it to
    check progress again after a delay sized to the task (don't poll every
    few seconds - that's wasted cycles for a multi-minute build; a longer
    interval, or a couple of spaced checks, is enough). If no such
    mechanism exists in your host, at minimum say explicitly in your
    response that the task is still running and how the user can check on
    it themselves, instead of implying you'll follow up when you have no
    way to.
- **Phase 5 - Verification & Review: NEVER trust the Final Report alone.**
  Inspect the actual resulting diff/workspace status, then actually
  **execute** what was built - reading the report or the diff is not
  verification, it's a summary. Across real delegation rounds, deviations
  that never surfaced from the report alone only showed up by running the
  code: a file committed that should have been gitignored, a cited source
  path that didn't exist anywhere in the codebase (invented for
  plausibility), a citation pointing at the right method but the wrong
  line, DB column types guessed from convention instead of read from the
  real DDL already available. Calibrate to what was built:
  - **Backend**: actually start the app against a real seeded database,
    don't just read the model annotations - a schema-validation mode that
    passes silently is much stronger evidence than a visual read. Hit the
    endpoints with real calls (200/401/etc.), don't assume them from the
    controller code.
  - **Frontend**: actually run the build and test suite (headless browser
    if needed), don't stop at reading the source files.
  - **Schema/data**: if a file is claimed "copied verbatim" from a source,
    `diff` it for real against that source - don't trust the claim.
  - **Infra**: if there's a compose file, actually bring it up, wait for
    the healthcheck, and query the resulting service/DB for real.
  - See the `task-spec-authoring` skill for calibrating verification depth to
    task risk in more detail.
- **Phase 5b - Verify the integration, not only the tasks.** Every task in a
  batch can be green in its own worktree and the merged result still be broken:
  tasks branched from the same commit cannot see each other. Observed live: two
  tasks in one batch each declared their own `BBox` type in the same library;
  lint and unit tests stayed green in both worktrees **and after the merge**,
  and only the application build caught it (a duplicate-export error on the
  library's barrel file). The integration gate is therefore not the union of the
  tasks' own criteria: after every merge run lint, tests, **and a full build of a
  consuming application**, and treat that as the batch's real acceptance.
- **Phase 6 - Closure & Telemetry:** if defects are found, log them (vital
  for continuous prompt/specification tuning - see `delegation-roi-analysis`)
  and request a fix.
  - **Merging: always checkout the target branch explicitly first.**
    Running `git merge --no-ff <feature-branch> -m "..." <target>` without
    checking out `<target>` first is a real, observed mistake - the
    trailing `<target>` argument gets interpreted as another branch to
    merge IN, not as the destination, so the merge silently lands on
    whatever branch you happened to be on. Correct sequence, every time:
    `git status --short` (clean) → `git checkout <target>` (explicit,
    never implicit) → `git merge --no-ff <feature-branch> -m "..."` →
    `git log --oneline --graph -6` (confirm the merge landed where
    intended). Remove the worktree once merged and no longer needed
    (`git worktree remove <path>`).

## Scaffolding steps can write configuration for *your* harness

When a delegated task runs a project generator, review what it actually
committed file by file, not just the files you asked for. Observed live: a
mainstream framework's `create-workspace` command emitted 51 files of agent
configuration for six different AI harnesses, including a settings file for the
orchestrator's own harness that registered an external plugin marketplace,
enabled a plugin from it, and added a third-party analytics domain to the
sandbox's allowed-domains list.

Treat tool-authored harness, permission, or sandbox configuration as something
to remove, not to silently adopt: the user didn't ask for it, and you cannot
consent to a change in your own permissions on their behalf. Removing is the
conservative direction; keeping it requires asking. Then say what you removed
and why, rather than quietly cleaning up.

## Track task state as a path, not a label

"Done" is the state that lies. Keep at least these distinctions, and let only
the orchestrator move a task between them - an Executor may only *deliver*:

| state | means |
| --- | --- |
| in progress | the Executor is working |
| **delivered** | it committed and reported. The criteria have been checked by nobody but their author |
| **verified** | you re-ran the acceptance criteria yourself and they passed |
| integrated | merged, with the post-merge gate (lint + tests + build) green |
| **done with a caveat** | it works but carries a known defect - requires a written note saying what it is and who pays for it |
| bounced | a criterion failed; it goes back into the *same* Executor session with the failing criterion quoted verbatim |
| blocked | an unresolved upstream question makes it unspecifiable - must name the question |

The rule carrying the weight: **there is no direct path from "in progress" to
"done."** "Delivered" always sits in between, and leaving it costs a re-run.
Publish this vocabulary somewhere durable - a status file in the repo - if the
work spans more than one session: a progress table whose only states are
done/not-done cannot express "integrated but never actually opened in a
browser," which is exactly the state most likely to be wrong.

Remember: if the Executor exposes semantic codebase search as a standing
capability, it's useful for your own exploration and Q&A too - use it even
when you are not delegating anything.
