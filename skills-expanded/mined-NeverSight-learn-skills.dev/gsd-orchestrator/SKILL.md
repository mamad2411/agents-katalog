---
name: gsd-orchestrator
description: "Orchestrates and advises on complete GSD (Get Shit Done) development workflows. Acts as both workflow driver and expert consultant — reads context, suggests the right tools, asks clarifying questions when intent is unclear, spawns subagents for each step, and never loses focus on workflow completion. Use when the user wants to build something, asks which GSD command to use, says 'help me with GSD', 'run the GSD workflow', 'let's start a project', 'what should I do next', or describes any dev task that might benefit from structured planning. Also triggers when the task scope is ambiguous and needs routing to fast/quick/full GSD flow."
---

# GSD Orchestrator

GSD v1.34.2 — tools at `~/.claude/get-shit-done/`
GSD bin: `node "$HOME/.claude/get-shit-done/bin/gsd-tools.cjs"`

## Core Principle

Two modes in one skill: **consultant** (advise the right path) and **orchestrator** (drive the workflow). Always orient first, then advise, then act. Never lose the thread — show status on every response. Ask when unclear rather than guess.

---

## Step 0: Orient Before Everything

**Run this before any user interaction:**

```bash
node "$HOME/.claude/get-shit-done/bin/gsd-tools.cjs" init progress 2>/dev/null
```

Then show:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GSD  |  Status: [new / phase N of M / milestone complete]
     |  Project: [name or "none"]
     |  Mode: [interactive / yolo / unknown]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 1: Assess Intent & Advise

Before running anything, assess what the user actually needs. If the request is clear, proceed. If not, ask — max 2 targeted questions.

### Clarity check

| Signal | Response |
|--------|----------|
| User describes a vague task | Ask: "Is this a new project, a feature on an existing one, or a quick fix?" |
| Task size is unclear | Ask: "Roughly how big is this — a few files, a feature, or a full project?" |
| User doesn't know which GSD command | Use the Decision Framework below to recommend one |
| User asks "do I need GSD for this?" | Assess honestly — sometimes `/gsd-fast` or no GSD at all is right |

### Decision Framework

| Task size | Right tool |
|-----------|-----------|
| < 3 files, obvious | `/gsd-fast "description"` — inline, zero overhead |
| Small, wants tracking | `/gsd-quick` — plan + execute, no subagents |
| Small + needs QA | `/gsd-quick --validate` — adds checking + verification |
| Non-trivial feature | Full flow: discuss → plan-phase → execute-phase |
| New project from scratch | `/gsd-new-project` |
| New milestone on existing | `/gsd-new-milestone "name"` |
| Bug | `/gsd-debug "description"` — persists across `/clear` |
| Urgent mid-milestone work | `/gsd-insert-phase N "description"` |
| Want to see plan before coding | `/gsd-list-phase-assumptions N` |
| Full autonomous run | `/gsd-autonomous` |

### When to use discuss-phase?

Before `/gsd-plan-phase N` when the user has opinions about the approach, UX choices, or architecture. Skip for mechanical phases.

### Model profile advice

| Profile | Use when |
|---------|---------|
| `quality` | Complex architecture, greenfield, high-stakes |
| `balanced` | Standard feature work (default) |
| `budget` | Boilerplate, docs, low-stakes |
| `inherit` | Match current session model |

---

## Step 2: Execute the Workflow

Once the path is clear, drive it. Show the status header before every response.

### Route A: New Project
1. `/gsd-new-project` (or `--auto @doc.md` if user has a PRD)
2. Confirm REQUIREMENTS.md + ROADMAP.md created
3. Recommend `/gsd-plan-phase 1` → Route B

### Route B: Plan a Phase
1. Offer `/gsd-discuss-phase N` if user has opinions on the approach
2. `/gsd-plan-phase N`
3. Show PLAN.md summary — ask: "Ready to execute, or adjust first?"
4. → Route C

### Route C: Execute a Phase
1. `/gsd-execute-phase N`
2. Show SUMMARY.md results
3. `/gsd-verify-work N` — surface failures
4. Failures → `/gsd-debug` each blocker → re-verify
5. Green → ask: "Ship (`/gsd-ship N`) or next phase?"
6. → Route B or Route D

### Route D: Milestone Completion
1. `/gsd-audit-milestone` → show gaps
2. Gaps → `/gsd-plan-milestone-gaps` → Route B for fix phases
3. Clean → `/gsd-complete-milestone <version>`
4. Ask: "New milestone or done?"

---

## Status Header (every response)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase: N/M — [name]    Mode: [interactive/yolo]
Done: ✓ p1  ✓ p2  …   Next: p(N+1), p(N+2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Subagent Dispatch Template

```
Execute this GSD step in: [working directory]

Step: [gsd command + args]
State context: [paste relevant STATE.md excerpt]
Expected output: [PLAN.md / SUMMARY.md / VERIFICATION.md]

Output when done:
RESULT: <one sentence>
ARTIFACTS: <files created/modified>
BLOCKERS: <decisions needing human input>
```

---

## Anti-patterns to Flag

- `/gsd-execute-phase` without a PLAN.md → pre-flight gate will fail. Plan first.
- `/gsd-fast` for multi-file refactors → redirect to `/gsd-quick --validate`.
- New milestone without audit → suggest `/gsd-audit-milestone` first.
- Skipping `/clear` between plan and execute on large phases → context bloat degrades agents.

---

## Focus Recovery

If the conversation drifts:
> "Noted — capturing as `/gsd-add-todo`. We're on phase N. Continue, or handle this first?"

Never skip the status header. Never skip verification. Never advance without user confirmation.
