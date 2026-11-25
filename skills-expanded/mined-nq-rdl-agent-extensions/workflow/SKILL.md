---
license: CC-BY-4.0
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
description: Prepare, resume and handle human gates for the executable RDL house-style Workflow from brainstorming through spec-kit, SDD, review, PR and MADR archival.
compatibility: Requires Claude Code dynamic workflows (2.1.154+) with plugin workflow support; written for the 2.1.274 Workflow runtime. Needs installed spec-kit, Superpowers and GitHub workflow skills.
---

The executable orchestrator is `/rdl-team:house-style`, registered from
[scripts/house-style.js](scripts/house-style.js). This skill prepares its inputs
and handles interactive boundaries; do not substitute a prose-only execution.
Verify the installed Workflow API against [canonical docs](https://code.claude.com/docs/en/workflows)
before running on another version. The script is native Workflow JavaScript,
not a Node CLI. Codex has no equivalent runtime; this entrypoint is Claude-only.

Read the target project's `/speckit.workflow.guide` for its house-style decisions.
Keep existing user authorizations. Run only stages in the requested scope.
The main session runs interactive brainstorming, clarify and remediation decisions;
Workflow agents cannot ask questions mid-run. By default, return user-only commands to the human for invocation.

Spec-kit commands carry `disable-model-invocation: true`, so invoke mode stops at
every generative stage. Ask the direct-mode question once, at `brainstorm` or
`frame`: authorise `generativeMode: "direct"` for specify, plan, tasks and analyze?
Recommend `direct` for agent-driven or cloud sessions. Record the answer in
`decisions` and the checkpoint, then pass it on every later stage; do not ask again:

```json
{"decision": "generativeMode", "value": "direct", "by": "<who>", "at": "<ISO time>", "scope": "<physicalWorktree>"}
```

The script uses direct mode for a unit only when `by`, `at` and a `scope` equal to
its `physicalWorktree` are present; an explicit `generativeMode` argument wins.
A recorded "no" (`"value": "invoke"`) or an explicit argument also stops the question.
`/data-request:triage` and `/data-request:lift` record the same shape with `scope`
set to the repository as `owner/name`. When you build a unit's `decisions`, replace
that scope with the unit's `physicalWorktree`, but only when that worktree is a
checkout of that repository (`git -C "$repo" remote get-url origin`). An unconverted
`owner/name` scope does not authorise direct mode.
Each unit's prompt omits decisions scoped to another unit's checkout.
Direct mode reads the exact target command instructions when Skill invocation is
unavailable. It keeps embedded human gates and tool permissions. Clarify, analyze
remediation choice and application, and constitution changes stay with the human
in the main session. Never modify command frontmatter to enable automation.
Routing `/speckit.*` through another agent (Codex, a subagent) to avoid
`disable-model-invocation` is not a workaround; direct mode is the supported path.

Invoke the Workflow tool with the registered name `rdl-team:house-style` and an
actual object as `args` (not a JSON-encoded string):

```json
{
  "stage": "brainstorm",
  "generativeMode": "invoke",
  "units": [{
    "id": "feature-name",
    "repo": "/absolute/target-worktree",
    "physicalWorktree": "/absolute/target-worktree",
    "branch": "main",
    "base": "origin/main",
    "checkpoint": "/absolute/target-worktree/.superpowers/rdl-workflow/feature-name.json",
    "request": "The user's requested change"
  }],
  "decisions": []
}
```

Stages, in order: `brainstorm`, `frame`, `specify`, `shape`, `execute`, `review`,
`pr`, `archive`. After each result, read its checkpoint and artifacts, handle its
`nextGate` in the main conversation, and pass the actual human answer with its
artifact/HEAD scope in `decisions`. On completion, continue to the next authorised stage if no human gate remains.
Never infer approval from elapsed time or from a `complete` status. Resume from recorded steps rather than replaying side
effects. Update the unit's `branch` after specify creates the feature branch.

Frame proposes epic units; the human approves the split. Assign each independent
unit a separate worktree and checkpoint before passing multiple units. The script
uses `parallel()` to run them and collects results for one human decision round.
Dependent units wait for their required parent artifact/commit. For specify,
start each checkout on its intended base and let spec-kit create the feature
branch; never pre-create an unused feature branch. Validate physical worktree
paths (including symlinks) before every launch: for each repo, obtain its Git
top-level directory with `git -C "$repo" rev-parse --show-toplevel`, then resolve
that directory with `cd -- "$root" && pwd -P`. Supply the result as
`physicalWorktree`; do not derive it by trimming the input path. The script
requires these identities and rejects duplicates before dispatching any agent.
Preflight rechecks the identity before writing even a checkpoint. If it changed,
refresh every unit's identity in the main session before retrying.

Use a canonical checkpoint path beneath `physicalWorktree`. Before launch, ensure
the exact checkpoint path is ignored and untracked. If needed, add its root-relative
pattern to the local exclusion file reported by `git rev-parse --git-path info/exclude`;
escape Git pattern metacharacters in the filename. Do not edit the project's
tracked `.gitignore` or silently relocate an existing checkpoint. Run
`bash <this-skill>/scripts/checkpoint.sh "$repo" "$checkpoint"` before creating
state, and before every subsequent write. The [validator](scripts/checkpoint.sh)
resolves the existing parent and rejects symlinks (including the final file),
paths outside the physical worktree, tracked files and unignored paths.
If validation fails, stop without writing state and correct the path in the main
session. Specify rechecks cleanliness after checkpointing and immediately before
running spec-kit. These filesystem checks are agent-executed; the Workflow DSL
cannot enforce filesystem operations itself.

Frame plans written before clarify are background only; `spec.md` and its
clarifications supersede them. Shape lists each contradiction in `plan.md`, and
analyze reports any that remain.

Workflow agents have no subagent-dispatch tool (observed on Claude Code 2.1.281),
and SDD needs a fresh implementer per task. So `execute` only prepares: it runs
task-bridge, records the bridged plan, its hash and task IDs in the checkpoint, and
returns `needs-human` with an SDD hand-off. If SDD phase commits are already
recorded, a rerun keeps the bridged plan and its hash. The main session then runs
`superpowers:subagent-driven-development` with `Agent`: one implementer and one
reviewer per `tasks.md` phase, TDD per task, then a final branch review. Record each
phase's commits in the checkpoint before the `review` stage. Keep the recorded
subagent-driven TDD decision; never fall back to `superpowers:executing-plans`
without a new human decision.

Brainstorm/write-plan/analyze use opus; specify/plan/tasks/execute use sonnet.
Effort intent is in prompts. SDD retains its internal task/reviewer model choices.
Review runs low passes with fixes, then high; high findings return to low after
repair. Three rounds bound a run; exhaustion returns to the human, never to PR.
The PR stage calls branch finishing and the thread-resolution skill, retaining
its PR URL. Archive requires merged-PR evidence and prepares a MADR follow-up;
opening a PR is not evidence that its spec can be retired.

On compression or a new session, read the checkpoint, validate repo/branch/HEAD,
source hashes and artifacts, then resume the first incomplete step. A stale
checkpoint requires reconciliation, not automatic replay or skipped gates.
Checkpoint writes are agent-mediated; review the recorded evidence on resume.
Full mode is the supported default. Constitution changes remain a main-session
project-governance decision, not an automatic per-feature step.
