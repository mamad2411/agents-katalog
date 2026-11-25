---
name: lessons-learned
description: >-
  Accumulated engineering lessons from real production incidents across the
  owner's projects. Load PROACTIVELY during development, code review, and
  planning of any feature that sends notifications, handles errors, or runs
  on a schedule - and whenever a new incident is analyzed, append its lesson
  here. Trigger on "check for repeat incidents", "lessons", or when
  implementing notification/alert/email logic.
---

# Lessons learned (production incidents)

Rules distilled from real incidents. When developing or reviewing, walk this
list against the change. When a new incident is analyzed, append a dated
entry: symptom, root cause, rule.

## Notifications and recurring events

**Rule: every automated notification path MUST have all three of:**
1. a diff against the last NOTIFIED state (not the last observed state),
2. a per-entity cooldown window,
3. persistence of that state OUTSIDE process memory (DB/Redis) so restarts
   don't reset it.

- **2026-07 "16 identical weather emails/day".** A 15-minute scan
  diffed the forecast against the previous observation and mailed every
  follower per flip; an oscillating forecast (Spa weekend) mailed on every
  crossing of the threshold. Fix: diff vs last-notified snapshot + 6h
  per-race cooldown. Cache/prediction invalidation stays keyed to raw
  observations - only the outbound notification is debounced.
- **2026-06 "5 model-fallback admin alerts in one evening".** The
  6-hour email cooldown lived in process memory; every deploy reset it, and
  fallbacks cluster exactly around deploys. Fix: Redis SET NX EX gate keyed
  by alert type; in-memory throttle is only the Redis-down fallback.
- Checklist for any watcher/scanner: What happens if the source flaps
  A→B→A→B? What happens after a deploy mid-incident? Does suppressed
  notification still update internal state so a real trend fires later?

## Email deliverability

- **2026-07 the transactional email provider: 30% of monthly sends "blocked".** Tests and dev
  environments sent real emails through the production provider key to
  example.com addresses; the provider blocklisted them and sender reputation
  paid for it. Rule: test/dev environments MUST use a noop email adapter enforced in
  code (not just .env convention); assert in CI that the provider key is
  absent/ignored under pytest.
- Bulk/notification email needs List-Unsubscribe + List-Unsubscribe-Post
  headers (Gmail/Yahoo bulk-sender requirements) and a per-category
  unsubscribe, with transactional (verification/reset) never suppressible.
- Per-category sender addresses (notifications@, account@, news@) keep one
  category's reputation damage from sinking the others.

## Error handling

**Rule: no failure may be invisible.** Every except/catch must log with
context at the right level; every "nothing happened" path needs a log line an
operator can find. A swallowed rejection in a UI component needs a visible
error state, not a silent null render.

- **2026-07 model fell back to stub silently for hours.** Boot-time
  R2 load failure had no retry and the hot-reload watcher (a) watched a
  legacy loader with a wrong manifest key and (b) was never even scheduled in
  lifespan. Users saw seed data with no banner. Rules: background watchers
  must be provably scheduled (test that lifespan starts them); self-heal
  loops must retry the REAL load path; degraded mode must be visible to
  users (badge) and operators (health endpoint field).
- **2026-07 an auth middleware `except Exception: pass`** kept stale
  JWT claims when the DB blipped and let deleted/blocked users keep access.
  Rule: auth fallbacks must fail closed on "user not found" and log the
  degradation path.
- Magic links in email must never mutate state on GET - corporate mail
  scanners prefetch links. GET renders a confirm page; the POST mutates.
  State transitions behind them need an atomic claim (UPDATE ... WHERE
  status='pending', check rowcount) or concurrent clicks double-fire mass
  emails.

## Process

- Pyright "Import could not be resolved" across a whole repo usually means
  the session has no venv wired - verify with the project's own test suite
  before "fixing" imports.
- A test that passes alone but fails in the suite: shared mutable state
  (same DB rows/keys across tests). Use unique per-test identifiers.
