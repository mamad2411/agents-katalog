---
name: Subagent-Driven Development
description: Guidance for assigning, coordinating, and reviewing focused subagent work.
---

# Subagent-Driven Development

> Fresh agents per task. Two-stage review. Status protocol. No context bleeding.

## Triggers

- Multi-domain task requiring parallel agent work
- `/sc:spawn` produces a task hierarchy to execute
- User requests agent-based task delegation
- Complex implementation spanning multiple technical domains

## Core Principles

### 1. Fresh Agent Per Task

Each subagent gets a **fresh context** with only what it needs:
- The specific task description
- Relevant file paths and content
- Acceptance criteria with a test that defines "done"
- No leaked context from other tasks

**Why**: Context bleeding causes agents to make assumptions from unrelated tasks, producing subtle bugs.

### 2. Status Protocol

Every subagent MUST report status using exactly one of these:

| Status | Meaning | Action Required |
|--------|---------|-----------------|
| `DONE` | Task complete, all tests pass | Proceed to review |
| `BLOCKED` | Cannot proceed, needs external input | Orchestrator resolves blocker |
| `NEEDS_CONTEXT` | Missing information to complete task | Provide specific context requested |
| `DONE_WITH_CONCERNS` | Complete but with flagged issues | Review concerns before accepting |

### 3. Two-Stage Review

Every subagent's output goes through **two reviews** before acceptance:

**Stage 1: Spec Compliance**
```
- Does the output match the task description exactly?
- Are all acceptance criteria met?
- Does the test that defines "done" pass?
- Are there any out-of-scope changes?
```

**Stage 2: Code Quality**
```
- Does the code follow project conventions?
- Are there security issues? (injection, auth, secrets)
- Is error handling adequate?
- Is the code testable and maintainable?
```

If either stage fails, the subagent output is **rejected with specific feedback**.

## Domain Grouping Strategy

When spawning multiple agents, group by domain to minimize cross-cutting concerns:

| Domain | Typical Tasks |
|--------|---------------|
| **Data Layer** | Schema, migrations, queries, ORM models |
| **API Layer** | Routes, controllers, validation, serialization |
| **Business Logic** | Services, domain models, rules |
| **Infrastructure** | Docker, CI/CD, deployment, monitoring |
| **Frontend** | Components, state, routing, styling |
| **Testing** | Test infrastructure, fixtures, mocks |

**Rule**: Tasks within the same domain can share an agent. Tasks across domains MUST use separate agents.

## Orchestration Pattern

```
1. DECOMPOSE: Break the task into domain-grouped subtasks
2. SPEC: Write acceptance criteria + failing test for each subtask
3. DISPATCH: Launch one agent per domain group (parallel where independent)
4. MONITOR: Collect status from each agent
5. REVIEW: Two-stage review of each agent's output
6. INTEGRATE: Merge outputs, run full test suite, resolve conflicts
7. VERIFY: Trigger verification-before-completion
```

## Integration

- Task decomposition comes from `/sc:spawn`
- Each subtask follows `test-driven-development`
- Reviews follow `/review` command patterns
- Final integration uses `verification-before-completion`
- Use `git-worktrees` for isolation when agents modify overlapping files
