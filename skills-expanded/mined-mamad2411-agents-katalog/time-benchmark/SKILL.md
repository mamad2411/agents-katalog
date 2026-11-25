---
name: time-benchmark
description: walk the user through a low/medium/high effort A/B/C throughput benchmark on their current model
user-invocable: false
---
<!-- tested with: claude code v2.1.122 -->

# /time-benchmark

guided A/B/C benchmark: run the same fixed task three times at different effort levels, record active time and tool count, compare to the time rule's matrix.

**this skill never switches effort automatically.** it prompts the user to run `/effort <level>` between runs and reads back the session's actual effort (which may differ from what was requested, per the rule's fallback behavior).

## what to do when invoked

1. **explain the plan to the user.** three runs, same task, the user changes effort between each. plan the task first (something reproducible, 3-5 min active at low).

2. **pick a fixed task.** default: "read `plugins/cc/rules/time.md` and summarize the effort matrix in 5 bullets". the user can substitute anything bounded and read-heavy.

3. **run A (low):**
   - ask the user: "please run `/effort low` then say 'go'".
   - wait.
   - on 'go', confirm active effort by the same resolution chain as `/time-estimate` (env → flag → session → settings → default). record the effort the session actually reports.
   - start a timer. run the fixed task. stop the timer.
   - record: wall seconds, estimated active seconds (subtract user-idle gaps when visible), tool count, any thinking indicators.

4. **run B (medium):** repeat with `/effort medium`.

5. **run C (high):** repeat with `/effort high`.

6. **report**:

   ```
   benchmark: model=<model>, task="<task>"

   run  requested  actual  wall(s)  active(s)  tools  tools/min  vs low
   A    low        low     180      170        17     6.0        1.00× baseline
   B    medium     medium  230      220        18     4.9        0.82×
   C    high       high    310      290        19     3.9        0.66×

   rule predicts for this model: low=0.87×, medium=0.70×, high=0.55×
   your measured: low=1.00 ref, medium=0.82× (+17%), high=0.66× (+20%)

   your throughput holds up better than the rule predicts at higher effort.
   consider running at high more often; the quality trade may be worth it.
   ```

7. **note fallbacks.** if `requested` and `actual` differ (e.g. `xhigh` requested but session reports `high` on opus 4.6), label the row and explain: per the rule's "fallback behavior (official)", unsupported levels silently fall back.

## rules

- never auto-switch effort. only the user runs `/effort`.
- never report a single-number throughput. always compare to the baseline run (A).
- if the task produces different outputs at different effort levels, that's signal, not noise. flag it.
- keep the task bounded. if any run exceeds 10 min active, abort that run and pick a smaller task.

## why this exists

the model × effort matrix in `plugins/cc/rules/time.md` is a generic baseline. your task mix, model, and repo environment may shift the real multipliers. a 10-minute benchmark gives you local data to trust when the generic matrix feels off.
