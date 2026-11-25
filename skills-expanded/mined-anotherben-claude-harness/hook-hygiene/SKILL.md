---
name: hook-hygiene
description: >
  Use when reviewing, creating, enabling, disabling, or troubleshooting Codex
  hooks; when hooks may be adding context noise, hidden state, stale disabled
  entries, or surprise behavior; or when proposing a guardrail hook. Keeps hooks
  mechanical, low-noise, PreToolUse-first, deterministic, and separate from
  skill decision logic.
---

# Hook Hygiene

## Overview

Review hooks as mechanical guardrails, not workflow brains. Skills decide what good work looks like; hooks block dangerous actions cheaply.

## Policy

- Prefer no hook over a noisy hook.
- Prefer `PreToolUse` hooks for narrow blocking guards.
- Avoid `SessionStart`, `UserPromptSubmit`, `PostToolUse`, `Stop`, `PreCompact`, and `PostCompact` unless there is strong low-noise proof.
- Hooks must be deterministic, fast, local, and side-effect-minimal.
- Hooks should not inject large context, perform broad scans, call network APIs, or decide complex workflow routing.
- Do not encode full proof, diagnosis, issue routing, or PR closeout logic in hooks. Use skills for that.

## Good Hook Candidates

- Blocking dangerous write surfaces, such as production-looking env writes or guarded worktree mutations.
- Blocking forbidden command shapes, such as direct pushes to protected branches or unsafe bulk env replacement.
- Blocking protected file edits unless explicitly approved.
- Detecting stale disabled hook state after a hook config change.

## Bad Hook Candidates

- "Suggest a skill" context injectors.
- Long-running vault, GitHub, Render, browser, or repo scans.
- Agent planning, proof-chain evaluation, diagnosis, PR review, or issue routing.
- Automatic edits, formatting, branch creation, PR mutation, or merge actions.
- Anything whose failure would confuse a normal chat turn.

## Workflow

1. Inspect exact active hook config first, usually `~/.codex/hooks.json` and relevant repo `.codex/hooks.json`.
2. Inspect stale hook state entries in `~/.codex/config.toml` only when hook enablement or disablement behaves unexpectedly.
3. List active hooks, inactive scripts, timeout, trigger type, command, and purpose.
4. Classify each hook:
   - `KEEP`: narrow, useful, low-noise.
   - `DISABLE`: noisy, broad, stale, redundant, or workflow-brain logic.
   - `REWRITE`: useful goal but too broad or context-heavy.
   - `PROPOSE`: missing narrow guard.
5. For any proposed hook, define pass/block fixtures before editing.
6. After edits, prove with direct hook config reads and fixture commands. Do not rely on repo git status for global hook files.

## Output

```markdown
**Active hook posture:** <summary>
**Keep:** <hooks>
**Disable:** <hooks>
**Rewrite:** <hooks>
**Propose:** <hooks>
**Context/runtime burden:** <low/medium/high and why>
**Fixture proof needed:** <pass/block cases>
**Recommended change:** <none or exact scoped change>
```

Default recommendation for this machine: keep active hooks lean unless a repeated preventable mutation justifies a new narrow `PreToolUse` guard.
