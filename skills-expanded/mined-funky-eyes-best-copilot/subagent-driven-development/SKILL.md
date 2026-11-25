---
name: subagent-driven-development
description: "Compatibility entrypoint for delegated execution of approved tasks. Canonical dispatch and review rules live in the PM and role workflows."
user-invocable: false
---

# Delegated Development Compatibility Entry

Keep this route for installed configurations; do not treat it as a separate development methodology.

PM uses `senior-project-expert-workflow` to dispatch independently scoped tasks to role workflows. Each implementation packet must carry the approved Spec Bundle references, frozen write set, acceptance checks, RED test or reproducible check, verification command, reviewer lanes, and state-sync target. Reviewers receive evidence-only packets and never approve their own work. Parallel execution is allowed only for satisfied dependencies and non-overlapping write sets.

## Minimal Dispatch Record

```markdown
- Task ID: <T-...>
- Owner agent: <technical-architect | developer | frontend-designer | root-cause-fixer | specification-writer>
- Reviewer agents: <independent lanes>
- Spec refs: <requirements.md, design.md, tasks.md anchors>
- Write set / dependencies: <paths and task IDs>
- Acceptance / RED / verification: <checks and command>
- Progress row: <current status and evidence location>
- State sync: <tasks.md and current-workstreams.md paths>
```

PM must reconcile each handback into the matching Progress Ledger row. A task is not complete merely because an agent returned; its required review, verification, and state synchronization must be recorded.

Use fresh, file-backed packets rather than long chat history. Refresh changed-file and evidence refs before review/fix dispatch. Repeated missing-context or blocker results require PM re-analysis, not another blind dispatch.

The shared handback and closeout rules come exclusively from `core-workflow-contract`.
