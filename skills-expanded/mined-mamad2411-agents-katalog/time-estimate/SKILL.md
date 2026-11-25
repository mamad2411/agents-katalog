---
name: time-estimate
description: estimate CC active time for a task using the time rule, with dynamic effort resolution
argument-hint: <task description>
user-invocable: false
---
<!-- tested with: claude code v2.1.122 -->

# /time-estimate

produce a realistic CC active-time estimate for the given task, grounded in `plugins/cc/rules/time.md`. never guesses effort level.

## what to do when invoked

1. **resolve active effort**, highest-precedence first. stop at the first rung that returns a value:
   - `echo "${CLAUDE_CODE_EFFORT_LEVEL:-}"` (env var)
   - `--effort` flag, if visible via process context
   - `/effort` session state, if already set this session
   - `effortLevel` key in `~/.claude/settings.json`, then any project-scoped `.claude/settings.json` under the repo root
   - otherwise, model default

   cite the rung that supplied the answer. if ambiguous, ask the user rather than guess.

2. **resolve active model** from the session's model id (e.g. `claude-opus-4-7`).

3. **classify session mode** using the table in the rule:
   - quick fix: single-file edit, typo, config tweak
   - standard: feature work, refactor, small module
   - marathon: migration, infra build, multi-file refactor

4. **apply the multiplier** from the model × effort matrix in the rule. quote the baseline at `low`, then scale.

5. **return the estimate** in the rule's format:
   - `CC: <range>` (always a range, never a single number)
   - effort rung cited (e.g. "rung 4, settings.json")
   - session mode named
   - your-time estimate for review
   - confidence (high / medium / low)
   - risks that could 2× the number

6. if the task breaks into sub-phases, estimate each and sum. flag which phases parallelize via subagents (1.8-2.2×) and which stay serial.

## rules to respect

- never quote a single number. always a range.
- never assume `xhigh` or `low` without checking.
- always distinguish CC time from your time.
- if on opus 4.7 with heavy work, offer the effort trade: `xhigh` is ~30% slower than `high` for throughput-bound work.
- never suggest fast mode on opus 4.7 or sonnet 4.6.

## example output shape

```
task: add logout button with tests

effort: low (rung 4, ~/.claude/settings.json)
model: claude-opus-4-7 (0.87× baseline)
mode: standard

CC: 12-18 min active
your time: ~10 min review
confidence: medium

phases:
  P1 find auth module (serial): 2-3 min
  P2 write button + route (serial): 4-6 min
  P3 tests (parallel via subagent): 3-5 min wall, ~6-9 min work
  P4 verify (serial): 3-4 min

risks that 2×: auth module structure unclear, test framework unfamiliar
```

## notes

the rule's matrix is a generic baseline. for personal calibration, run `/time-calibrate`.
