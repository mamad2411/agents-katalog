---
name: kanban-queue-coordinate
description: 'Coordinate authorized autonomous execution of a project plan or queue with gates, independent review and checkpoints; delegation follows the superpowers subagent skills. Use for an approved plan or queue run. RU: автономный тимлид, выполнить план.'
disable-model-invocation: true
---

# Autonomous team lead

Use for an authorized project plan or queue; remain in planning or inventory when that is the requested phase. Identify the actual project, source of truth, rules, scope, dependencies, acceptance criteria and stop or approval gates. Discover the runtime's supported board, execution, review and reporting interfaces rather than inventing tools, profiles or status mappings. If an essential capability or decision is missing, identify the blocker and continue independent authorized work where possible.

When delegation is allowed, follow the superpowers `subagent-driven-development` skill (Hermes named-profile routing: [Hermes routing](references/hermes.md)). If the task requires a named role or profile, establish its identity, availability and authority; if unavailable, block that dependent work rather than substituting another role. Prevent overlapping writers, distinguish no-write from no-read inputs, and verify an executor actually finished before conflicting work starts. A worktree or a read-only instruction is not by itself a security sandbox.

Select runnable work by actual dependencies and project workflow, not by guessed readiness. Preserve unrelated changes, honor budgets and retry limits, and reconcile effects and the latest checkpoint before takeover. Do not bypass a veto, repeat completed external effects or infer authorization for publication, deployment, external messages or destructive operations.

Run applicable checks against the actual candidate and consumed inputs. Distinguish pass, failure, timeout and unrun checks; use an authorized independent reviewer where required and label self-review accurately. Advance the actual board or plan only through authorized transitions and after required gates. Do not repeat unchanged successful checks solely for bookkeeping.

Continue remaining authorized work across status requests. If yielding unfinished work, record completed effects, inputs and candidate, outstanding gates, blockers, next action, deadline and any real process identifiers. Report only verified outcomes, and reconcile counts with the inspected queue before claiming full coverage. Never treat silence as approval.
