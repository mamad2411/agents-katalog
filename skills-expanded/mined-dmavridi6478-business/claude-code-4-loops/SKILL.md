---
name: claude-code-4-loops
description: The four kinds of loop you can create with Claude Code - turn-based (you prompt each step), goal-based (keeps going until a success condition is met), time-based (runs on a schedule) and proactive (event-driven, watches and responds) - with an example for each, which command or skill here creates it, and the guardrails each needs. Use when deciding how to automate a repeated Claude Code task, choosing between /loop, a routine, a hook or a GitHub Action, or designing an unattended agent. Source @shiva.bytes infographic "4 types of loops you can create with Claude Code" (Batch 101).
---

# 4 types of loops with Claude Code

| # | Loop | Who stops it | Example on the infographic | Build it with |
|---|---|---|---|---|
| 1 | **Turn-based** (human in control) | you, every turn | generate a REST API, review, ask for improvements | plain prompting; `/clarify-first` |
| 2 | **Goal-based** (works towards a goal) | the success condition | keep fixing failing tests until all tests pass | `/build-loop-until-tests-pass`, `/test-and-fix-loop`, `autonomous-loops`, `continuous-agent-loop` |
| 3 | **Time-based** (runs on a schedule) | the schedule, or loop exits when done | check application logs every 10 minutes | the `loop` skill (`/loop 10m ...`), routines (`/scheduled-routine`) |
| 4 | **Proactive** (event-driven) | the routine is cancelled | new GitHub issue, then analyse, assign, notify the team | PR and issue subscriptions, hooks, `build-iterated-agentic-loop` (GitHub Actions) |

## Guardrails by loop

1. **Turn-based:** none needed; the human is the control.
2. **Goal-based:** write the success condition as something a command can check (exit code, test count), set a maximum number of iterations and a budget, and forbid disabling tests to pass (that is cheating the goal).
3. **Time-based:** pick the longest interval that still catches the problem; each wake costs tokens. Stop after a few runs that find nothing.
4. **Proactive:** it acts without you present, so give it the least access that works, require approval for anything that sends, spends or deletes, and log every action. In this repo, outbound actions go through the OS approval gate.

## Pick the loop

- You want to review each result: **1**. You can state "done" as a check: **2**. You need to watch something regularly: **3**. Something external triggers the work: **4**.
- Related installed skills: `design-control-loop` (design a sensor, controller and actuator loop for your codebase), `build-iterated-agentic-loop` (turn a repeatable task into a skill plus a scheduled GitHub Actions workflow), `loop-design-check`, `/loop-start`, `/loop-status`.
