---
name: critic-dispatch
description: "Control when @critic runs during PRD work to balance thoroughness vs speed. Triggers on: critic mode, when to review, code review batching, critic dispatch."
---

# Critic Dispatch Skill

> Control when @critic runs during PRD work to balance thoroughness vs speed.

## Triggers

- Starting PRD execution
- After completing a story (to check if critic should run)
- "critic mode", "when to review", "code review batching"

## Applicable Agents

- **builder** — orchestrating PRD execution and story completion
- **developer** — when self-reviewing after significant changes

---

## Configuration Cascade

Resolved in order (highest priority first):

1. **CLI flag** — `--critic-mode=strict` (one-off override)
2. **Project-level** — `project.json` → `agents.criticMode`
3. **Hardcoded fallback** — `balanced`

---

## Critic Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `strict` | Run @critic after every story | High-risk projects (payments, auth, security) |
| `balanced` | Run @critic every 2-3 stories | Default — catches issues without excessive overhead |
| `fast` | Run @critic once at end of PRD | Greenfield projects, low-risk changes, speed priority |

---

## Balanced Mode Logic

- Run critic after story 2, then every 3 stories (story 5, 8, 11, etc.)
- If PRD has ≤2 stories, behave like `fast` (one critic run at end)
- Always run critic at PRD completion regardless of mode

### Formula

```
shouldRunCritic = (storyNumber == 2) || (storyNumber > 2 && (storyNumber - 2) % 3 == 0)
```

### Examples

| Story # | Run Critic? | Reason |
|---------|-------------|--------|
| 1 | No | First story, wait for context |
| 2 | Yes | First checkpoint |
| 3 | No | Too soon after 2 |
| 4 | No | Still building |
| 5 | Yes | 3 stories since last review |
| 6 | No | Continue |
| 7 | No | Continue |
| 8 | Yes | 3 stories since last review |

---

## Implementation

### At PRD Start

1. Determine critic mode from config cascade
2. Log: `"Critic mode: [mode]"`

### After Each Story Completes

```python
if criticMode == "strict":
    run @critic
elif criticMode == "balanced":
    if storyNumber == 2 or (storyNumber > 2 and (storyNumber - 2) % 3 == 0):
        run @critic
elif criticMode == "fast":
    # Skip until PRD completion
```

### At PRD Completion (All Modes)

```python
run @critic  # Final review before PR
```

---

## Critic Invocation

When running @critic:

1. **Pass relevant context:**
   - Files changed since last review
   - Story descriptions completed
   - Test results summary

2. **Wait for completion:**
   - Address blocking issues before continuing
   - Log advisory issues for later

3. **Track in `chunk.json`:**
   ```json
   {
     "lastCriticRun": {
       "afterStory": 2,
       "timestamp": "2026-02-28T10:00:00Z",
       "blockers": 0,
       "advisories": 3
     }
   }
   ```

---

## Override Examples

### CLI Override (One-Off)

```bash
# Run critic after every story for this session
builder --critic-mode=strict

# Skip intermediate reviews, only final
builder --critic-mode=fast
```

### Project-Level Configuration

```json
// docs/project.json
{
  "agents": {
    "criticMode": "strict"
  }
}
```
