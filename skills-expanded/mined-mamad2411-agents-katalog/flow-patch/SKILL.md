---
name: flow-patch
description: Small bounded change with micro-spec, subagent TDD, and per-task review. Invoke with /flow-patch.
disable-model-invocation: true
---

# Flow Patch

Single bounded change (roughly ≤3 files, one concern). Larger → `/flow-spec`.

The micro-spec stays inline in chat — no spec file, no plan file. **You orchestrate only: subagents write the code.** Every task is reviewed before the next one starts.

Resolve `flow-shared` via path resolver in `flow-shared/SKILL.md`.

## 1. Micro-spec

Present inline in chat. Do not write a file.

```markdown
## Micro-spec

**Problem:**
**Success criteria:**
**Files:**
**Out of scope:**

### Task 1: [name]
**Change:** [what to build]
**Acceptance:** [observable behavior that proves it works]
```

One task per commit-sized step. Every Success criterion is covered by some task's Acceptance. Each task must stand alone — a subagent gets only what you paste, so write the briefing for someone who has never seen this conversation.

## 2. Approval

Review the micro-spec before executing it. All names and paths in the micro-spec must be confirmed against the codebase before proceeding. Iterate with user as needed until there are no open questions or ambiguity. Get the user's OK before dispatching.

## 3. Execute (subagents)

Follow `flow-shared/references/execute-loop.md`. Task text comes from the inline micro-spec — paste it into the prompt; do not tell subagents to read chat history.

## 4. Verify

Run the project's usual checks — tests, lint, typecheck, formatters, build — whichever exist. Check each Success Criterion. Report pass/fail. Stop — user owns merge/push.
