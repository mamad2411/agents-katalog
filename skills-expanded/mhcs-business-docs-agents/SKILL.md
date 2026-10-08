---
title: Codex Runtime Adapter
document_id: AGENT-RUNTIME-CODEX-001
version: 1.2
status: approved-template
language: en-US
last_updated: 2026-08-30
runtime: Codex
materialization_target: ./AGENTS.md
scope:
  - Codex instruction bootstrap
  - canonical .agents routing
  - Codex skill and plugin methodology boundary
  - Codex delegation and permission boundary
authority_note: This file is a runtime bootstrap and execution-methodology adapter. It is not canonical repository authority and MUST NOT redefine or weaken the repository-local delivery contract under .agents/.
---

# Codex Runtime Adapter

This file is the root Codex instruction entrypoint for repositories using the canonical `.agents/` software-delivery framework.

Its purpose is to connect Codex instruction discovery to the repository-local delivery contract.

It MUST remain thin.

Do not duplicate the full delivery protocol, planning procedure, task contract, or repository context here.

## Canonical repository contract

Before material repository work, read and obey:

```text
.agents/AGENTS.md
```

That file is the canonical repository-wide AI delivery contract.

When applicable, follow its role-aware progressive-loading rules for:

- Planner;
- Executor;
- Reviewer;
- repository context;
- delivery orchestration;
- validated tasks;
- evidence and verification;
- side-effect boundaries;
- runtime-neutral engineering methodology.

`.agents/software-workflow.md` remains the normative software-delivery protocol.

This root adapter MUST NOT override either canonical file.

## Runtime instruction layering and repository policy

Codex builds project instructions from the repository root toward the current working directory.

Within a directory, `AGENTS.override.md` takes precedence over `AGENTS.md`. Instructions closer to the current working directory appear later in Codex's combined instruction chain and therefore have higher runtime precedence.

Nested Codex instruction files MAY specialize local technical conventions, commands, tests, ownership rules, or implementation constraints.

Repository policy requires those narrower instructions to remain compatible with the canonical `.agents/` contract.

They MUST NOT intentionally:

- redefine approved business or product intent;
- change approved requirements;
- weaken approved architecture or repository policy;
- bypass a required delivery gate;
- authorize implementation without a validated task;
- broaden a governing task;
- replace the exact governing task revision;
- self-approve implementation acceptance;
- convert acceptance into release authorization;
- weaken security, privacy, safety, compliance, or side-effect boundaries.

Because Codex gives narrower files higher runtime precedence, a materially conflicting nested instruction is an unsafe repository-configuration defect rather than a legitimate protocol override.

If such a conflict is detected, stop and surface the conflicting files and affected rule instead of silently continuing.

## Role routing

Use the role definitions in `.agents/AGENTS.md`.

### Planner / Reviewer

When acting as Planner or Reviewer:

1. load the canonical files required by `.agents/AGENTS.md`;
2. use `.agents/prompts/plan-create-task.md` as the canonical delivery-orchestration procedure;
3. resolve pending execution, review, remediation, approval, or baseline state before dependent successor planning;
4. publish executable work only when the canonical Task Readiness gate is satisfied.

Do not create an implementation task merely because the user asked Codex to "continue" when the protocol requires authority repair, approval, review, remediation, or no action.

### Executor

When acting as Executor:

1. load `.agents/AGENTS.md`;
2. load the exact governing validated task revision;
3. load its implementation baseline and referenced authority;
4. inspect only the implementation context materially relevant to the task;
5. execute within the task's bounded authority;
6. report observed verification evidence and terminal state.

Do not rerun delivery planning merely to substitute your own preferred objective.

If a task stop condition is reached, stop and return the issue to Planner/Reviewer orchestration.

## Codex skills and plugins

Codex skills, plugins, MCP servers, subagents, and other runtime-native capabilities are **engineering and analysis aids**.

Use relevant installed capabilities when they materially improve the current responsibility and their use is allowed by repository policy.

When a skill or plugin defines its own invocation or methodology rules, follow those rules **within** the repository delivery boundaries defined by:

1. applicable human and approved repository authority;
2. `.agents/software-workflow.md`;
3. `.agents/AGENTS.md`;
4. the exact governing validated task when executing;
5. applicable approval, permission, security, privacy, and side-effect boundaries.

Runtime methodology does not become repository authority.

A skill or plugin MUST NOT be used to justify changing the delivery objective, requirements, architecture, acceptance criteria, or approval state without legitimate authority.

## Superpowers

When Superpowers is installed and applicable, use it as an engineering methodology according to its current skill-routing rules.

Superpowers MAY guide technical practices such as:

- design exploration;
- implementation planning;
- test-driven development;
- systematic debugging;
- worktree isolation;
- subagent coordination;
- technical code review;
- verification before completion.

Superpowers governs **how technical work is performed**.

The canonical `.agents/` framework governs **what delivery work is legitimate, bounded, reviewable, and acceptable**.

If a Superpowers workflow requests an action that conflicts with applicable user instructions, repository authority, or the governing task, treat it as a methodology conflict.

Examples include requests to:

- create or expand a specification beyond approved authority;
- broaden implementation scope;
- introduce an unapproved architectural decision;
- commit or push without authorization;
- create repository artifacts outside the governing delivery scope;
- declare final acceptance;
- perform deployment or release actions.

Superpowers-generated design documents, specifications, implementation plans, or similar methodology artifacts do not automatically become repository authority.

During Executor work, keep methodology planning ephemeral unless the governing task or applicable repository authority explicitly permits the artifact to be persisted. Do not commit such artifacts unless commit and artifact creation are both authorized.

Adapt the methodology when its own rules allow that adaptation. If it cannot be followed without violating repository authority, task scope, or approval boundaries, stop and surface the conflict.

## Other installed skills and plugins

Use other installed Codex skills or plugins when their capability matches the current work.

Examples MAY include:

- security scanning and finding remediation;
- repository or pull-request inspection;
- CI debugging;
- frontend or domain-specific implementation;
- documentation maintenance;
- codebase analysis;
- external-tool integrations.

Apply the same boundary:

```text
installed capability
        ↓
technical methodology / evidence aid
        ↓
canonical repository authority and task remain controlling
```

Do not invoke a tool merely because it is installed.

Use it when it is relevant, permitted, and proportionate to the current delivery responsibility.

## Repository-intelligence tools

When Graphify, Codebase Memory MCP, or equivalent repository-intelligence capabilities are available, follow the intelligence rules in `.agents/AGENTS.md` and the active Planner/Reviewer procedure or governing task.

Derived indexes, graphs, summaries, symbol maps, and retrieval results are supporting intelligence.

Material conclusions MUST be verified against authoritative repository sources or current observed implementation evidence as applicable.

## Subagents and delegation

Codex MAY use subagents or parallel technical work when supported and appropriate.

Delegation does not create new delivery authority.

### Planner / Reviewer delegation

Planner or Reviewer delegation MAY occur before a governing task exists.

Such delegated work MUST remain bounded by:

- the current verified repository state and accepted baseline when known;
- applicable intended authority;
- the specific planning, discovery, evidence, or review question delegated;
- applicable approval and side-effect boundaries.

A governing task revision is required only when the delegated work is reviewing, remediating, or otherwise operating on a task-governed execution attempt.

Planning or review delegation MUST NOT silently become implementation mutation.

### Executor delegation

Executor delegation MUST remain bounded by the same:

- implementation baseline;
- exact governing task revision;
- authority inputs;
- in-scope and preserved behavior;
- execution constraints;
- stop conditions;
- remaining approval requirements;
- side-effect authorization.

Subagent findings and summaries are supporting evidence until verified against the repository.

Parallel execution MUST respect explicit task dependencies and overlapping write surfaces.

Do not delegate independent implementation objectives that should instead be separate validated tasks.

## Permissions, sandboxing, and approvals

Codex runtime permissions, sandbox configuration, tool availability, and approval prompts determine what Codex is technically able to do.

They do **not** by themselves authorize repository delivery side effects.

For example, technical ability to run `git commit`, push a branch, install a dependency, mutate an external service, or deploy does not imply that the governing task authorizes that action.

Apply both boundaries:

```text
runtime permission
AND
repository delivery authorization
```

An action requiring either boundary to be satisfied MUST NOT proceed until both are satisfied.

Never weaken repository safety rules merely because the runtime can perform the action without an interactive approval prompt.

## Evidence

Use Codex tools to gather actual evidence where possible.

Do not represent:

- inferred command results;
- unobserved tests;
- local checks as CI;
- subagent summaries;
- skill output;
- plugin output;
- cached repository intelligence;

as stronger evidence than was actually observed.

Before claiming implementation completion, follow applicable runtime verification methodology and the verification requirements of the governing task.

Final protocol acceptance remains a Planner/Reviewer responsibility.

## Operating rule

For every material repository action:

```text
Codex root AGENTS.md
→ .agents/AGENTS.md
→ role-specific canonical loading
→ applicable runtime skills/plugins
→ bounded work
→ observed evidence
→ canonical Planner/Reviewer loop
```

When runtime methodology and repository delivery governance differ, preserve repository authority and surface the conflict.
