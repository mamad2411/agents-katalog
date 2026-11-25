---
name: quick-fix
description: Fast troubleshooting triage for common, obvious issues. What is broken, what changed, the usual suspect for the failure class, the smallest fix, and when to escalate. Use for routine breakage (dependency errors, config typos, unset env vars, stale state) when a full debugging protocol would be overkill. Escalate to hypothesis-debugging when the fast pass fails.
license: MIT
---

# Quick Fix

A fast triage pass for common, well-understood failure classes. Most issues are routine and do not need a full investigation. When the fast pass fails, escalate to a real debugging protocol.

**Tradeoff**: bias toward speed over rigor. For routine breakage only. The moment the issue stops being routine, stop and escalate.

## 1. What is broken

Pin the problem to one sentence. Get the exact error text and the line it points at, not a paraphrase. If there is no error, add a log and reproduce.

## 2. What changed

Did it ever work? If yes, what changed since: a dependency bump, a config edit, an environment switch, a pulled update? Check `git diff` and `git log`. Revert the suspected change in isolation and retest.

## 3. Most common causes for this class

- Dependency or version error: wrong version, missing install, lockfile drift, stale `node_modules`.
- Config typo or wrong value: misspelled key, wrong path, wrong port, wrong environment file.
- Environment variable missing or unset in the process that runs the code.
- Path or working directory: relative path resolved from an unexpected cwd.
- Stale state or cache: build cache, dist output, old process bound to the port.
- Permissions: file mode, ownership, missing sudo.

## 4. The smallest fix

Change the least possible. Fix the one thing. No new abstractions, validators, or error handling the issue did not require. Re-run against the repro and confirm it now passes.

## 5. When to stop and escalate

Escalate when two or three quick fixes have not resolved it, the cause is not a common class, the failure is intermittent, or the fix would touch code you do not understand. Escalate to the hypothesis-debugging protocol: reproduce, isolate, hypothesize, instrument, fix, verify.

---

See full content at https://github.com/HermeticOrmus/quick-fix-skills.
