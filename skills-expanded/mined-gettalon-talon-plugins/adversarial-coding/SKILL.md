---
name: adversarial-coding
description: "GAN-style multi-agent coding with Planner → Generator → Evaluator loop. Usage: /adversarial-coding <goal> [--budget 50] [--max-iterations 20]"
user-invocable: true
---

# Adversarial Coding — GAN-Style Multi-Agent Development

Inspired by Anthropic's research on multi-agent coding. Three agents work in adversarial loop: Planner expands requirements, Generator implements features, Evaluator tests and critiques. The system iterates until quality goals are met or checkpoints trigger user review.

## Arguments

Parse `$ARGUMENTS` for:
- `<goal>` — One-line goal (e.g., "build a retro game editor", "create a browser-based DAW")
- `--budget <dollars>` — Max cost before auto-pause (default: 50)
- `--max-iterations <n>` — Max Planner→Generator→Evaluator cycles (default: 20)
- `--quality-threshold <1-10>` — Minimum Evaluator score to ship (default: 7)
- `--no-playwright` — Disable Playwright testing (use tests + AI review only)

If arguments are missing, ask the user for the goal.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MAIN ORCHESTRATOR                                │
│                                                                     │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐                  │
│  │ PLANNER  │─────▶│GENERATOR │─────▶│EVALUATOR │                  │
│  │ (Plan)   │      │ (Code)   │      │ (Test)   │                  │
│  └────┬─────┘      └────┬─────┘      └────┬─────┘                  │
│       │                 │                 │                        │
│       │    feedback     │    bugs/issues  │                        │
│       └◀────────────────┴─────────────────┘                        │
│                                                                     │
│  State: .adversarial/                                               │
│  ├── spec.md           # Full specification                         │
│  ├── tasks.json        # Feature checklist with status              │
│  ├── evaluator-log.md  # Test results + AI review notes             │
│  └── checkpoint.json   # {cost, iterations, stuckCount, status}     │
└─────────────────────────────────────────────────────────────────────┘
```

## Setup Phase

1. **Create state directory**: `mkdir -p .adversarial`
2. **Initialize checkpoint.json**:
   ```json
   {
     "goal": "<user's goal>",
     "budget": <budget>,
     "iterations": 0,
     "stuckCount": 0,
     "totalCost": 0,
     "status": "running"
   }
   ```
3. **Detect project type**:
   - Check for `package.json` → Node/JS project
   - Check for `Cargo.toml` → Rust project
   - Check for `pyproject.toml` or `requirements.txt` → Python project
   - Check for `.html` files with JS → Web project (Playwright eligible)
4. **Create initial spec.md** with user's goal as placeholder

## Main Loop

Run this loop until checkpoint triggers pause:

```
┌─────────────────────────────────────────────────────────────────┐
│ ITERATION N                                                      │
│                                                                  │
│ 1. SPAWN PLANNER (subagent_type: Plan)                          │
│    Input: goal + current spec.md + evaluator feedback           │
│    Output: Updated spec.md with refined features                │
│    Task: "Expand this goal into detailed spec. Consider         │
│           evaluator feedback. Break into numbered features."    │
│                                                                  │
│ 2. SPAWN GENERATOR (subagent_type: general-purpose)             │
│    Input: spec.md + tasks.json                                  │
│    Output: Code changes + updated tasks.json                    │
│    Task: "Implement next incomplete feature from tasks.json.    │
│           For independent features, spawn parallel workers."    │
│                                                                  │
│ 3. SPAWN EVALUATOR (subagent_type: feature-dev:code-reviewer)   │
│    Input: Code changes + spec.md                                │
│    Output: evaluator-log.md with:                               │
│      - Test results (npm test / cargo test / pytest)            │
│      - Playwright results (if web project)                      │
│      - AI code review findings                                  │
│      - Quality score (1-10)                                     │
│      - List of bugs/issues to fix                               │
│                                                                  │
│ 4. UPDATE CHECKPOINT                                            │
│    - Increment iterations                                       │
│    - Update stuckCount (if same bugs repeat)                    │
│    - Estimate cost (iterations × ~$2-5)                         │
│                                                                  │
│ 5. CHECK PAUSE CONDITIONS                                       │
│    Pause and notify user if:                                    │
│    • stuckCount >= 3 (stuck on same issue)                      │
│    • totalCost >= budget                                        │
│    • All tasks complete AND quality >= threshold                │
│    • Planner wants to expand scope (asks permission)            │
│                                                                  │
│ 6. REPEAT or PAUSE                                              │
└─────────────────────────────────────────────────────────────────┘
```

## Agent Specifications

### PLANNER Agent

**Type**: `Plan` (read-only, no code changes)

**Responsibilities**:
- Expand one-line goal into comprehensive specification
- Break spec into numbered, testable features
- Accept evaluator feedback and refine spec
- Flag scope expansion requests (don't auto-expand)

**Output format** (spec.md):
```markdown
# <Goal Title>

## Overview
<2-3 sentence description>

## Features

### Feature 1: <name>
- Description: <what it does>
- Acceptance criteria:
  - [ ] <testable criterion 1>
  - [ ] <testable criterion 2>
- Priority: critical/high/medium/low

### Feature 2: ...
```

### GENERATOR Agent

**Type**: `general-purpose` (full tool access)

**Responsibilities**:
- Implement features one at a time
- Update tasks.json with progress
- For independent features, spawn parallel workers
- Follow existing codebase patterns

**Parallel execution rules**:
- Features with no shared files → spawn workers
- Features modifying same files → sequential
- Max 3 parallel workers

**Output**: Code changes + updated tasks.json:
```json
{
  "features": [
    {"id": 1, "name": "...", "status": "complete"},
    {"id": 2, "name": "...", "status": "in_progress"},
    {"id": 3, "name": "...", "status": "pending"}
  ]
}
```

### EVALUATOR Agent

**Type**: `feature-dev:code-reviewer` or `general-purpose`

**Responsibilities**:
1. **Run tests**: Detect and run project's test suite
2. **Playwright** (if web): Click through user flows
3. **AI review**: Check for bugs, security, code quality
4. **Score**: Give 1-10 quality rating
5. **Report**: List specific issues to fix

**Test detection**:
```bash
# Node
npm test || yarn test || pnpm test

# Rust
cargo test

# Python
pytest || python -m pytest

# Generic
make test
```

**Playwright mode** (for web projects):
- Launch browser
- Navigate to app
- Execute user flows from spec
- Screenshot failures
- Report interaction bugs

**Output format** (evaluator-log.md):
```markdown
# Evaluation Report — Iteration N

## Test Results
- Unit tests: PASS (42/42)
- Integration tests: FAIL (3/5)
  - Error: ...

## Playwright Results (if applicable)
- Login flow: PASS
- Dashboard load: FAIL — timeout waiting for #app
- Screenshot: screenshots/iter-3-failure.png

## Code Review
- [CRITICAL] SQL injection in user.go:45
- [HIGH] Missing error handling in api.ts:102
- [MEDIUM] Inconsistent naming in utils.js

## Quality Score: 6/10

## Issues to Fix
1. Fix SQL injection — user.go:45
2. Add timeout handling — api.ts:102
3. ...
```

## Checkpoint System

### Pause Conditions

| Condition | Action |
|-----------|--------|
| `stuckCount >= 3` | Pause — same bug won't fix. Ask user for guidance. |
| `totalCost >= budget` | Pause — budget exceeded. Ask: continue or ship? |
| All complete + score >= threshold | Done — ship it! |
| All complete + score < threshold | Continue iterating (up to max-iterations) |
| Planner scope expansion | Pause — ask user to approve new features |

### User Notification at Pause

```
⏸️  ADVERSARIAL CODING PAUSED

Reason: <stuck/budget/complete/scope>

📊 Status:
- Iterations: N / M
- Cost: ~$X / $Y budget
- Quality: 6/10 (threshold: 7)
- Features: 3/5 complete

🐛 Current Issues:
1. SQL injection in user.go:45
2. ...

Options:
[Continue] [Ship as-is] [Adjust direction] [Stop]
```

## Simplicity Rules

- Generator prefers small, focused commits
- Evaluator rejects over-engineering
- If stuck 3+ times, simplify the approach
- Never add dependencies without user approval

## Output Format

After each iteration, print:
```
[#03] ⚙️  Planner: refined spec (5 features)
[#03] 🔨 Generator: implemented Feature 2 (auth flow)
[#03] 🧪 Evaluator: tests PASS, Playwright FAIL, score 6/10
[#03] 📊 Cost ~$12, stuck=1, 2 bugs to fix
```

## Stopping

The loop stops when:
- User interrupts (Ctrl+C)
- All features complete AND quality >= threshold
- Max iterations reached
- User chooses "Ship as-is" or "Stop" at checkpoint

## File Structure After Run

```
.adversarial/
├── spec.md              # Final specification
├── tasks.json           # Feature completion status
├── evaluator-log.md     # All evaluation reports
├── checkpoint.json      # Final state
└── screenshots/         # Playwright failure screenshots (if any)
```

## Example Usage

```bash
# Build a game editor (like Anthropic's demo)
/adversarial-coding "build a retro pixel art game editor with tile map support"

# With constraints
/adversarial-coding "create a browser-based DAW" --budget 100 --max-iterations 30

# Skip Playwright for backend project
/adversarial-coding "build a REST API for user management" --no-playwright
```
