---
name: mo-watchdog
description: Observe one target or scan all reachable Herdr, Orca, and Paseo sessions for limits, overload, failures, questions, work, and completion; nudge only an explicitly authorized exact target.
license: MIT
---

# Watch backend sessions

Read [Watchdog behavior](references/watchdog.md) completely. Start only after the
user explicitly requests observation.

Use `scripts/mo-watchdog.sh target --backend <backend> --session <id>` for one
session or `scripts/mo-watchdog.sh scan` for all reachable supported backends.
Observation is read-only. An explicit nudge additionally requires
`--nudge <message>` and exact target authorization; the script re-reads native
state and suppresses the nudge when that state changed. It reserves a bounded
private digest before delivery and suppresses the same message, an ambiguous
attempt, or a saturated unchanged state across later invocations. Nudges return
after native delivery; agent completion is observed separately.

Do not inspect tracked project content or private provider state. Report the
native locator, classified state and action. Pattern misses are refined from
observed failures rather than hidden behind a support claim.
