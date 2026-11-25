---
name: automate
description: Turn a repetitive task into a reliable automation script. Scope the task and its frequency/inputs/outputs/edge cases, pick the simplest tool, implement the smallest version, add error handling and idempotency, dry-run then schedule. Use when the task is "automate this", "write a script for", or scheduling an unattended job.
license: MIT
---

# Automate

A protocol for turning a repetitive task into a reliable automation script.

**Tradeoff**: bias toward scoping and hardening over speed. For a one-off you will run once and watch, use judgment.

## 1. Scope the task before writing code

- What is the task, in one sentence? (Two sentences means two tasks; split them.)
- How often, and what triggers it (manual, schedule, file change, event)?
- Inputs and outputs, including exit code and side effects.
- Edge cases: empty input, partial input, already-done state, missing dependency, no network.
- Cost of running it twice, or failing halfway.

## 2. Pick the simplest tool that fits

Bash for file moves and CLI glue. Python for branching logic, structured data, and API calls. Makefile for dependent multi-step graphs. A scheduler (systemd timer or cron) wraps one of these for unattended runs. If the task is three shell commands, it is a script, not a program.

## 3. Implement the smallest version that works

Write the path that handles the real inputs first. No speculative flags or config for a single caller. Bash scripts open with `set -euo pipefail`.

## 4. Add error handling and idempotency

Validate inputs before acting. Make a second run a no-op, not a duplicate or corruption. Fail loud, never swallowing an error to keep a green exit code. Log what it did. Guard destructive steps.

## 5. Dry-run, then make it runnable on a schedule

Add a `--dry-run` that changes nothing and run it first. Test the edge cases deliberately. Schedule the verified script with absolute paths and explicit `PATH`, capture output to a log, and alert on non-zero exit.

---

See full content and worked examples at https://github.com/HermeticOrmus/automate-skills.
