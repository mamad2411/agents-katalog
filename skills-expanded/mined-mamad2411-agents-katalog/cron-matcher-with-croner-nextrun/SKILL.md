---
name: cron-matcher-with-croner-nextrun
description: Implement minute-granularity cron matching by asking croner for the next run from 1 second before the current minute and checking if it falls inside the current minute.
category: automation
version: 1.0.0
version_origin: extracted
tags: [cron, scheduling, croner, timezone]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: packages/shared/src/automations/cron-matcher.ts
imported_at: 2026-04-18T00:00:00Z
---

# Minute-granularity cron matching with croner

## When to use
- You tick a scheduler every minute (or irregularly) and need to ask "does this cron fire right now?" without maintaining your own cron state.
- Need IANA timezone support (e.g. `Europe/Budapest` vs UTC).
- Don't want to write your own cron expression parser.

## How it works
1. Use [`croner`](https://www.npmjs.com/package/croner): `new Cron(expr, { timezone })`.
2. Floor the current `Date` to the start of its minute (`setSeconds(0, 0)`).
3. Ask croner `nextRun(startOfMinute - 1s)` - "when is the next fire after the last second of the previous minute?".
4. If that `nextRun` timestamp lies inside `[startOfMinute, startOfMinute + 60_000)`, it matches this minute.
5. Return false on parse error rather than throw - a malformed user cron shouldn't crash the scheduler.

## Example
```ts
import { Cron } from 'croner';

export function matchesCron(expr: string, timezone?: string): boolean {
  try {
    const job = new Cron(expr, timezone ? { timezone } : {});
    const now = new Date();
    const startOfMinute = new Date(now); startOfMinute.setSeconds(0, 0);
    const checkFrom = new Date(startOfMinute.getTime() - 1000);
    const nextRun = job.nextRun(checkFrom);
    if (!nextRun) return false;
    return nextRun.getTime() >= startOfMinute.getTime()
        && nextRun.getTime() <  startOfMinute.getTime() + 60_000;
  } catch {
    return false;
  }
}
```

## Gotchas
- "Check from 1s before" is crucial - if you ask `nextRun(startOfMinute)`, croner returns the NEXT fire, not the one inside the current minute.
- If your scheduler tick is more frequent than once per minute, you'll match multiple times within the same minute; dedupe by logging last-fired minute per cron expr.
- IANA zone names are case-sensitive; validate against `Intl.supportedValuesOf('timeZone')` before storing user config.
- Don't use 6-field (seconds) cron with this pattern - the +60s window assumption breaks.
