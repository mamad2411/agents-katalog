---
name: rigor
description: Apply a focused, evidence-driven engineering workflow to one concrete task.
disable-model-invocation: true
---

# Rigor

Take one concrete engineering task from request to evidence.

**Boundary.** Rigor starts with a concrete investigation, change, experiment, or review. Open-ended product discovery belongs to `/tracer-interview-me`; recommend that entry point and end Rigor when the decisions needed to define the task are still unknown.

## 1. Frame

Resolve four things from the request and repository context:

- **Outcome:** the answer, diagnosis, behavior, structural change, measurement, or verdict requested.
- **Finish line:** the observable condition that completes this task, including diagnosis-only and read-only limits.
- **Scope:** the affected system and the smallest plausible problem boundary.
- **Safety:** external effects, irreversible actions, material cost, sensitive data, production access, or unresolved product decisions.

**Complete when:** the finish line and authority boundary select one workflow without inventing product intent.

## 2. Scale

Choose the lightest level that protects the result. Every level preserves the finish line, safety boundary, and fresh-evidence requirement.

- **Light:** local, reversible work following an established pattern. Work directly and run the focused proof. Planning, delegation, and independent review are optional.
- **Standard:** work spanning files or boundaries, an uncertain mechanism, or a meaningful behavior change. State the verifiable unit order, inspect the completed diff against the request and existing contracts, and run focused plus repository-required checks.
- **High-risk:** security, permissions, money, destructive operations, concurrency, migrations, external compatibility, or a one-way architectural choice. Meet Standard gates, obtain fresh independent review of the named risk, and prove behavior at the strongest practical runtime boundary. Load Authority in step 4, plus Safety when its trigger is present. An unavailable independent review or runtime proof remains an unmet gate, so report the task as incomplete.

Adjacent playbook steps may collapse for Light work when every completion condition remains observable. Added ceremony must correspond to a named uncertainty, risk, or proof need.

**Complete when:** one level is justified by observed risk and every additional gate has a named purpose.

## 3. Route

Load exactly one primary playbook:

| Request shape | Playbook |
| --- | --- |
| Explain behavior, compare approaches, assess a concern, or answer a read-only question | [Investigation](playbooks/investigation.md) |
| Diagnose or fix incorrect behavior, a failing test, crash, or regression | [Bug fix](playbooks/bug-fix.md) |
| Add or change product or system behavior | [Feature](playbooks/feature.md) |
| Change structure while preserving behavior | [Refactoring](playbooks/refactoring.md) |
| Diagnose or improve measured speed, memory, throughput, or resource use | [Performance](playbooks/performance.md) |
| Settle an observable design or behavior question with throwaway code | [Prototype](playbooks/prototype.md) |
| Review a diff, branch, commit, or named files without changing them | [Review](playbooks/review.md) |

The requested finish line controls the route's stopping point. “Figure out what is wrong” selects Bug fix and stops after diagnosis; “fix it” continues through implementation and proof. The same distinction separates performance diagnosis from optimization.

Long-running programs, release operations, and product discovery sit outside these playbooks. Name that routing gap rather than approximating one of those workflows.

**Complete when:** the chosen playbook matches both the work type and the authorized stopping point.

## 4. Load triggered references

Read only the references whose trigger is present:

- **Shape:** Feature or Refactoring work that changes state, interfaces, or system boundaries → [Shape the system](references/shape.md).
- **Burden:** a refactor, abstraction, or expanding diff → [Reduce the burden](references/burden.md).
- **Evidence:** Bug fix, Performance, Review, or delegation → [Work from evidence](references/evidence.md).
- **Safety:** retries, migrations, concurrency, parallel writers, or a recurring failure → [Change safely](references/safety.md).
- **Alternatives:** a consequential open design choice or Prototype → [Explore consequential alternatives](references/alternatives.md).
- **Authority:** unresolved questions, external effects, high-risk work, parallelism, or subagents → [Autonomy and delegation](references/autonomy-and-delegation.md).

**Complete when:** every triggered branch has been read and irrelevant branches remain unloaded.

## 5. Execute

The selected playbook supplies the ordered steps. Hold these invariants throughout:

- **Scope:** inspect repository guidance and current work before mutation; preserve unrelated work.
- **Evidence:** keep observations, hypotheses, and unknowns distinct.
- **Restraint:** change only what the supported mechanism and finish line require.
- **Proof:** verify at the strongest practical boundary; compilation and self-report are supporting evidence.
- **Handoff:** report the outcome, evidence gathered now, and every material gap or unverified claim.

The lead agent owns scope, decisions, synthesis, and final claims.

**Complete when:** the playbook's Done criterion is met, the final worktree contains no unintended changes, and every completion claim has fresh evidence or an explicit unverified status.
