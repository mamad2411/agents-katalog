---
name: dynamic-reassignment
description: "Reassign tasks to alternative specialist agents when the primary specialist fails. Handles rate limits with backoff and persistent failures with agent switching. Triggers on: agent failure, delegation failure, rate limit during task, specialist crash."
---

# Dynamic Reassignment Skill

> ⟳ **When specialists fail, try alternatives before escalating.**
>
> Transient failures (rate limits) retry with backoff. Persistent failures (bad output, crashes) trigger reassignment to alternative agents. Checkpoints preserve progress across switches.

## Triggers

- Agent delegation failure
- Rate limit during task execution
- Context overflow during implementation
- Verification contract failure
- "fallback", "reassign", "alternative agent"

## Bundled Resources

- `data/fallback-chains.yaml` — Default fallback chains for all task types

---

## Fallback Chain Lookup

When delegating a task, determine the fallback chain:

1. **Read `~/.config/opencode/data/fallback-chains.yaml`** for toolkit defaults
2. **Check `project.json → agents.fallbackChains`** for project overrides
3. **Merge chains** (project takes precedence) unless `override: true`
4. **Determine task type** from files and description:
   - `*.tsx`, `*.jsx` → `react-component`
   - `*_test.go` → `go-tests`
   - `*.spec.ts` in `e2e/` → `playwright-tests`
   - `*.test.tsx` → `react-tests`
   - `Dockerfile*` → `docker`
   - Default → `generic`

---

## Failure Detection

Use verification contracts to detect failure:

| Outcome | Detection | Action |
|---------|-----------|--------|
| Success | All `verificationContract.criteria` pass | Task complete |
| Verification failure | One or more criteria fail | Try alternative |
| Rate limit | Error contains "429", "rate limit", "quota" | Retry with backoff |
| Context overflow | Agent reports context limit | Checkpoint → fresh session |
| Crash/error | Agent throws exception | Try alternative |

---

## Rate Limit Handling

Rate limits are transient — retry same agent with exponential backoff:

```
⟳ Rate limited, retrying in 30s... (1/3)
```

**Backoff schedule:** 30s → 60s → 120s (3 retries max)

After 3 retries exhausted:
1. If alternatives exist → switch to next in chain
2. If no alternatives → escalate to user

---

## Alternative Selection

When a specialist fails with non-transient error:

1. **Create checkpoint** (per session-log skill)
2. **Look up fallback chain** for task type
3. **Find next alternative** not already tried
4. **Show status:**
   ```
   ⟳ Switching to go-tester (react-tester failed: verification failed)
   ```
5. **Delegate to alternative** with checkpoint in prompt
6. **Record attempt** in `chunk.json` → `reassignment.attempts[]`

Try ALL alternatives in the chain before escalating.

---

## Reassignment State

Track reassignment attempts in `chunk.json`:

```json
{
  "reassignment": {
    "taskId": "US-003",
    "taskType": "react-tests",
    "currentAgent": "jest-tester",
    "attempts": [
      {
        "agent": "react-tester",
        "startedAt": "2026-02-28T10:00:00Z",
        "endedAt": "2026-02-28T10:15:00Z",
        "outcome": "verification_failed",
        "error": "3 tests failed: DarkModeToggle click handler",
        "retryCount": 0
      }
    ],
    "checkpointRef": "chunk.checkpoint"
  }
}
```

---

## Context Overflow Handling

Context overflow needs fresh context, not retry:

1. **Create checkpoint immediately**
2. **Do not retry same agent** (won't help — context is full)
3. **Show status:**
   ```
   ⟳ Context limit reached, starting fresh session with checkpoint
   ```
4. **Delegate same task to same agent** with fresh context + checkpoint
5. **If fresh session also hits limit:** task is too large — escalate with suggestion to break down

---

## Escalation Protocol

When ALL alternatives are exhausted, escalate to user:

```
═══════════════════════════════════════════════════════════════════════
                    TASK REQUIRES YOUR ATTENTION
═══════════════════════════════════════════════════════════════════════

Task: US-003 - Add dark mode toggle

Attempted:
  1. react-dev (primary) — Failed: verification failed (3 tests)
  2. developer (alternative) — Failed: context overflow
   
Checkpoint saved with:
  - 3 completed steps
  - 2 pending steps
  - 1 decision recorded

Options:
  [R] Retry with different approach (describe what to try)
  [M] Fix manually (I'll provide the checkpoint context)
  [S] Skip this task for now
  [A] Abandon PRD and start fresh

> _
═══════════════════════════════════════════════════════════════════════
```

**User responses:**
- **R (Retry):** Prompt for different approach, restart with primary agent
- **M (Manual):** Output full checkpoint context for copy-paste
- **S (Skip):** Mark story as skipped, continue to next story
- **A (Abandon):** Stop PRD execution, preserve state for later

---

## Reassignment Flow Summary

```
Task Delegation
       │
       ▼
Primary Agent Executes ──────┐
       │                     │
       ▼                     │
Verification Contract        │
       │                     │
   ┌───┴───┐                 │
   │       │                 │
SUCCESS  FAILURE             │
   │       │                 │
   │    Rate limit? ──YES──► Retry with backoff (max 3)
   │       │                     │
   │      NO                  Exhausted?
   │       │                     │
   │    Context overflow? ─► Fresh session with checkpoint
   │       │
   │    Create checkpoint
   │       │
   │    Alternative available?
   │       │
   │    ┌──┴──┐
   │   YES   NO
   │    │     │
   │ Switch  ESCALATE
   │    │
   │    └────────────────────┘
   │
   ▼
Task Complete
```
