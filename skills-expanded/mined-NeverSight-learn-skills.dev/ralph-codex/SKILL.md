---
name: ralph-codex
description: Run a standalone, native-hook-based Ralph loop for Codex. Use when Codex should keep coordinating, executing, and verifying work across turns until one verified outcome is ready, without relying on conductor, tmux, or project-specific runtime state.
---

# Ralph Codex

Use `$ralph-codex` when the work should not stop at one assistant turn.

## Workflow

1. In the target repo, start the local loop:
   - from the skill directory, run `bash scripts/ralph_loop.sh start --goal "<goal>"`
   - optional guardrail: `bash scripts/ralph_loop.sh start --goal "<goal>" --max-turns 12`
   - start re-installs this skill's native hook entries automatically
3. Let Codex keep iterating. The hooks inject the current Ralph contract on session start and prompt submit, then the `Stop` hook re-primes the next turn automatically.
4. Inspect or end the loop with:
   - `bash scripts/ralph_loop.sh status`
   - `bash scripts/ralph_loop.sh stop`
   - `bash scripts/ralph_loop.sh resume`

## Rules

- Use it only for persistence-first work that needs repeated execution and verification.
- Keep the loop focused on one verified outcome. If the user changes direction, stop and restart with a new goal.
- Do not rely on model-native delegation semantics. This skill is just a native-hook continuation loop.
- Leave `max_turns` unset unless you explicitly want a hard stop guardrail.
- End cleanly by either running the stop command or emitting a line that is exactly `RALPH_DONE` only after one verified outcome is actually ready. Both paths remove this skill's hook entries automatically.
- Treat hooks as experimental and unavailable on Windows.

## Outputs

The loop writes repo-local state under `.codex-ralph/`:

- `state.json`
- `events.tsv`
- `run.log`
