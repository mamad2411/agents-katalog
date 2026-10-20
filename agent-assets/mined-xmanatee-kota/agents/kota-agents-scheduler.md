# Scheduler Module

This directory owns the `scheduler` repo module — timed, recurring, and event-triggered reminders.

- Registers the `schedule` tool in the `management` tool group.
- The daemon scope runtime owns reminder state in its existing database and is
  the sole timer/event delivery owner. Scope composition imports legacy JSON
  once before starting delivery. Standalone clients do not open reminder stores.
- The tool resolves the module host's daemon scope provider at invocation time.
  It exposes reminder commands only; the daemon retains timer and firing APIs.
  It requires a daemon-hosted session; unknown scopes fail explicitly.
- Reminder delivery uses `schedule.fire` on the daemon's existing event stream,
  including its scope ID and replay cursor.

Weekly quota policy is opt-in through scheduler configuration. The workflow
runtime owns its independent admission hold; the selected harness reads the
authoritative account quota. Reserve one configured percentage per full UTC
day until reset, with no reserve in the final 24 hours. Active runs and their
required children may drain. Probe failures retain the last admission decision;
startup waits for a valid snapshot. Disabling the policy releases only its hold.
