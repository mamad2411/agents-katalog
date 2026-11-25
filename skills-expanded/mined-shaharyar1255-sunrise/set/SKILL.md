---
name: set
description: Set or change the local time your Claude 5-hour usage window starts each day, by creating a cloud routine that primes it. Use when the user runs /sunrise:set, or asks to set, prime, anchor, or schedule their session start time or window reset time.
---

# sunrise: set your session start time

The user wants their Claude **5-hour usage window** to start at a chosen local time each day, so resets land predictably. You achieve this by creating a **cloud routine** (the same thing the built-in `/schedule` creates) that sends one tiny no-op message four times a day, five hours apart. Each message starts or refreshes the 5-hour window, keeping it primed.

A plugin cannot run on a timer itself — only a cloud routine runs 24/7 (even with the user's machine off). So your job here is to compute the schedule and create that routine.

Requested start time (may be empty): **$ARGUMENTS**

Follow these steps in order.

## 1. Parse the start hour
From "$ARGUMENTS", determine the **start hour** in 24-hour local time.
- Accept forms like `9am`, `9`, `09:00`, `9:00am`, `21`, `6am`, `18:30`.
- Default the minute to **:07** unless the user specified one. (An off-:00 minute avoids the top-of-hour rush and reliably lands just after each window boundary.)
- If "$ARGUMENTS" is empty or genuinely ambiguous, ask the user: "What local time should your Claude window start each day?" Then continue once they answer.

## 2. Compute the four daily ping times (local)
The window lasts 5 hours, so prime four times a day:
- T1 = start hour
- T2 = (start + 5) mod 24
- T3 = (start + 10) mod 24
- T4 = (start + 15) mod 24

All four use the same minute. This keeps a window primed for ~20 hours a day; the one unavoidable ~4-hour gap (because 24 is not divisible by 5) lands overnight when the start hour is the user's wake time.

## 3. Confirm before creating anything
Show the user, in their **local** time:
- The four ping times T1–T4.
- That their window will then reset at (start+5), (start+10), (start+15), (start+20) mod 24.
- That this uses ~4 of their 15 daily routine runs and needs a **Claude Pro or Max** plan with Claude Code routines.

Ask them to confirm. If they decline, stop and change nothing.

## 4. Create (or update) the routine
Invoke the built-in **`schedule`** skill (the `/schedule` routine creator) to make a **recurring** cloud routine with exactly these parameters:
- **name:** `sunrise`
- **schedule:** every day at T1, T2, T3, T4 **local** time. (The routine system converts local to a UTC cron. A single cron `MINUTE H1,H2,H3,H4 * * *` in UTC works, since all four pings share one minute.)
- **model:** `claude-opus-4-8` — must be a heavy model. Lighter models like **Haiku do NOT anchor the 5-hour usage window** (the window silently never starts); Opus does. The prompt is trivial, so the cost is ~one token regardless of model.
- **git repositories / sources:** none. This routine performs no work and needs no repo.
- **prompt:** `Output exactly: ok. Do not read files, run commands, use tools, or change anything. Then stop.`

**Idempotency:** First check the user's existing routines (the `schedule` list capability). If a routine named `sunrise` already exists, **update** that one's schedule instead of creating a duplicate.

**Eligibility:** If the routine system reports the user is not eligible (routines unavailable, or not on Pro/Max), tell them plainly that this feature requires a Claude Pro or Max plan with Claude Code routines enabled, and stop — don't retry in a loop.

## 5. Report
Confirm it's live and show:
- The local ping times (T1–T4) and the resulting reset times.
- The manage/route link returned by the routine system (e.g. the `claude.ai/code/routines/...` URL).
- How to change it later: run `/sunrise:set <new time>` again (it updates the same routine). To turn it off, pause or delete the routine at https://claude.ai/code/routines.

Keep the final summary short.
