---
name: wait-for-token-usage
description: "Budget-aware working mode for long sessions: poll the Claude plan usage (5h burst + weekly), park the session before the 5h cap is hit, and auto-resume after the window resets. Only use when explicitly invoked."
license: Vibecoded
---

# Wait for token usage to reset

Normal sessions must NOT do this. Only follow this skill when the user explicitly invoked it,
because parking the session for hours is a big commitment that should always be a deliberate choice.

Goal: run a long piece of work to completion without ever slamming into the 5 hour rate limit
mid-task. Instead of getting cut off, you stop a bit early, sleep until the window resets
(at zero token cost), then pick the work back up.

This skill drives [`claude_usage.py`](../../claude_usage.py), which is what actually talks to the
usage endpoint. See that project's README for flags, caching and exit codes.

## 0. Local personalisation

@personalisation.md

If that import produced nothing, read `personalisation.md` from this skill's own directory yourself
(the same directory as this `SKILL.md`). The file is gitignored, so it exists only on machines where
someone set it up, and it overrides anything below it: the exact command to run the script, whether
the sandbox can see it at all, and any threshold the user prefers. If it is absent, carry on with the
defaults in this file and do not go looking for it a second time.

## 1. Read the current usage

Primary command (live fetch, 5 minute internal cache, so calling it is cheap):

```sh
claude-usage --pretty --utc --no-autorefresh | jq '.["five_hour","seven_day"]'
```

If `personalisation.md` gave you a different command, use that one instead. Otherwise, if
`claude-usage` is not on PATH, call the script directly with whatever interpreter is available
(`python /path/to/claude_usage.py ...`, or `uv run /path/to/claude_usage.py ...`). Ask the user for
the path once rather than guessing, and prefer the cache fallback below over hunting the filesystem.

Why those flags:

- `--utc` keeps `resets_at` as raw ISO-8601. Without it the script rewrites it to
  `Thu 06 Aug 2026, 21:00 (CEST)`, which `date -d` refuses to parse, so the sleep math breaks.
- `--no-autorefresh` stops the script from launching a real `claude` process for 20s to refresh an
  expired OAuth token. Never let that happen from inside a session.
- `--pretty` is only cosmetic, drop it if you pipe straight into `jq`.

**Fallback, and you may well need it.** If the Bash sandbox or the permission rules hide the
directory the script lives in, the command above dies with `No such file or directory`. That is a
sandbox policy, not a bug: read-denies are implemented as empty tmpfs mounts over the path, so an
`allowRead` nested inside a denied subtree is silently ignored (it shows up in the effective policy
but no bind-mount restores it). Do not try to "fix" it on your own, just use the cache file.

The cache is written under the platform user cache dir and is readable even when the repo is not.
Claude Code's status line typically refreshes it on every prompt render, so it is normally under
5 minutes old:

```sh
CACHE="${XDG_CACHE_HOME:-$HOME/.cache}/claude_usage/usage.json"
jq '.["five_hour","seven_day"]' "$CACHE"
stat -c 'cache mtime: %Y' "$CACHE"   # compare with `date +%s`
```

If the cache is more than ~15 minutes old, say so out loud and treat the numbers as a floor, not a
fact: real usage can only be higher than what a stale cache reports, so round your caution up.

## 2. What the numbers mean

`utilization` is a percentage (float, 0 to 100). `resets_at` is a UTC ISO-8601 timestamp (with `--utc`).

| key | meaning |
| --- | --- |
| `five_hour` | the burst window, the one that actually stops you. Resets on a rolling 5h schedule. |
| `seven_day` | the weekly all-model cap. Reset can be days away. |
| `limits[]` | per-limit detail. Look for `kind: "weekly_scoped"` with a `scope.model`: a model specific weekly cap (Opus, Fable) can be higher than `seven_day` and bite first. |

So the check is really: `max(five_hour, seven_day, every limits[].percent)`.

## 3. Thresholds

- **`five_hour` >= 90%**: stop taking on new work and park (section 5).
- **`five_hour` >= 80%**: do not start anything expensive (subagent fan-out, workflows, full test
  suites, large file rewrites). Finish and commit what is in flight, then re-check.
- **any weekly limit >= 90%**: do NOT park. The reset may be days out. Stop, tell the user which
  limit and when it resets, and let them decide.

Tune these if the user asks; they are defaults, not physics.

## 4. Checking cadence

Checking costs one cheap bash call, but doing it every turn is noise. Use:

- once at the start, so you know the budget you are working with,
- before any expensive step (subagents, workflows, long builds or test runs),
- after roughly every 10 tool calls, or after any single step that clearly burned a lot,
- and every few steps once anything is past 75%.

## 5. Parking until the reset

Announce it to the user first (current %, the local reset time, what you will resume). Then:

1. Commit anything committable. Never park on a dirty tree you cannot reconstruct.
2. Write a short resume note so a fresh context can pick up: what is done, what is next, which
   files. Scratchpad file or `TaskCreate` tasks, either is fine.
3. Launch the wait as a **background** Bash call, using the `resets_at` you just read:

```sh
RESET='2026-08-06T19:00:00+00:00'   # five_hour.resets_at from the check above
TARGET=$(( $(date -d "$RESET" +%s) + 120 ))   # +2min of margin, the reset is not instant
until [ "$(date +%s)" -ge "$TARGET" ]; do sleep 60; done
echo "five_hour window reset, target was $(date -d "@$TARGET")"
```

Call it with `run_in_background: true`. It costs zero tokens while it waits, and the harness
re-invokes you when it exits.

**Never use a foreground sleep.** Foreground `sleep` is blocked by the harness, and even if it were
not it would hold the turn open for hours.

Optionally fire a `PushNotification` when you park, so the user knows the session went quiet on
purpose rather than crashed.

## 6. Waking up

When the background wait completes:

1. Re-read the usage (section 1). Do not assume the reset happened.
2. If `five_hour` is still >= the pause threshold, the background command was probably killed early
   (long background jobs can be capped). Just park again with the new `resets_at`. This loop is
   self-healing by design, so a premature wake costs one small turn, not correctness.
3. Otherwise re-read your resume note and continue exactly where you stopped. Say one line about
   the new budget, then get back to work; no recap of the whole session.

## 7. Ending

When the work is done, or when the user says stop, drop out of this mode: report the final usage
numbers and stop polling.
