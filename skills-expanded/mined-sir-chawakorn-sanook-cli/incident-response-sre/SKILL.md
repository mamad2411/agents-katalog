---
name: incident-response-sre
description: Drives live incident response and postmortems SRE-style: severity triage (P0–P3), log/metric/trace correlation to find what changed, safe mitigation, comms updates, and blameless postmortem with action items. Triggers during an active incident/outage, on-call triage, or writing a postmortem afterward.
when_to_use: incident/outage เกิดอยู่, on-call ต้อง triage, service degraded, หรือเขียน postmortem หลังเหตุ
---

## When to Use

- An active incident is happening: errors spiking, latency up, partial/full outage, data not flowing, customers reporting breakage.
- On-call triage: an alert fired and you must decide severity + whether to page humans.
- A service is degraded but not down (elevated error rate, slow tail latency, queue backlog growing).
- After the incident is resolved and you need to write a blameless postmortem.

Do NOT use for routine bug fixing with no live blast radius, planned maintenance, or feature work — use normal debugging instead.

## Steps

**Phase A — Stabilize first, diagnose second (mitigation before root cause).**

1. **Declare + triage severity.** Pick one and state it explicitly with scope:
   - **P0** — full outage / data loss / security breach / money-affecting. Mitigate now, page on-call.
   - **P1** — major feature down or broad degradation, no full workaround.
   - **P2** — partial degradation, workaround exists, limited users.
   - **P3** — minor / cosmetic / single-user, no urgency.
   Write impact in user terms: *what* is broken, *who/how many* affected, *since when*. If you can't quantify yet, say "scope unknown, treating as P1 until proven smaller" — never downgrade on a guess.

2. **Build the "what changed" timeline.** Most incidents are caused by a recent change. List, with timestamps, the last 24–48h of:
   - deploys / releases / rollbacks (check CI/CD history, git log, image tags)
   - config / feature-flag / env-var changes
   - infra changes (scaling, DB migration, cert rotation, DNS, dependency upgrade)
   - traffic shifts (spike, new client, retry storm, upstream outage)
   Overlay the incident start time against this. The change immediately preceding the symptom onset is your prime suspect.

3. **Correlate signals — logs + metrics + traces together, not in isolation.**
   - **Metrics** tell you *where/when* (which service, which endpoint, error-rate vs latency vs saturation — the golden signals). Find the first metric that broke and its exact start time.
   - **Logs** tell you *what* (the actual error string, stack trace, status code). Grep the failing service around the metric break time; read the FIRST errors, not the loudest.
   - **Traces** tell you *which hop* in the request path failed (DB? upstream dep? timeout? auth?).
   Pin all three to the same time window. A latency spike + DB connection-pool-exhausted logs + traces stalling at the DB call = one coherent story.

4. **Hypothesis-driven correlation — don't oversimplify.** Form 2–3 candidate root causes from the timeline + signals. For each, state the one observation that would confirm or kill it, then check that observation. Beware: correlation ≠ cause (a deploy at the same time may be innocent); the loudest error may be a downstream *symptom*, not the source. Keep going until the signal chain is coherent end-to-end — stop only when remaining hypotheses are killed.

5. **Mitigate with the safest reversible action FIRST — before any permanent fix.** Prefer, in order: roll back the suspect deploy/config → disable the suspect feature flag → scale up / add capacity → shed load / rate-limit / shut a non-critical path → failover. Reversible mitigation is allowed even before root cause is 100% confirmed if it's safe and likely to help. **Never** apply an irreversible action (drop/delete data, force-push, destructive migration) as a mitigation — escalate to a human first. Confirm recovery via the same metric that broke in step 3, not by assumption.

6. **Post status comms.** Short, factual, no blame, on a cadence (e.g. every 30 min while P0/P1). Each update: current impact → what's being done → next update time. On resolution: "mitigated/resolved at <time>, root cause <known/under investigation>, monitoring." State unknowns plainly — don't speculate publicly.

**Phase B — After recovery: blameless postmortem.**

7. **Write the postmortem** (only after the incident is mitigated/closed). Required sections:
   - **Summary** — one paragraph: what broke, impact, duration.
   - **Timeline** — UTC timestamps from detection → mitigation → resolution, including key diagnostic steps.
   - **Impact** — quantified (users, requests, $, SLO/error-budget burn).
   - **Root cause + contributing factors** — the trigger AND the conditions that let it become an incident (missing alert, no rollback path, silent dependency). Multiple factors usually, not one.
   - **What went well / what was slow** — detection time, mitigation time, gaps in tooling/visibility.
   - **Action items** — each is concrete, *owned*, *dated*, and prioritized (P0/P1...). Distinguish "prevent recurrence" from "detect faster" from "mitigate faster". No vague "be more careful".

8. **Blameless language.** Attack the system, never the person. "The deploy step had no automated canary check" not "X deployed bad code". People act reasonably given the info they had; if a human could cause an outage with a normal action, the *system* lacked a guardrail.

9. **Feed back into a runbook.** If this incident class can recur, capture the detection signal → mitigation steps → verification as a reusable runbook so next time is faster. Convert the highest-value action item into a guardrail (alert, canary, rollback automation, flag).

## Common Errors

- **Chasing root cause while the system burns.** Mitigation (rollback/flag-off) comes before diagnosis. A reverted deploy that buys 30 min is worth more than the perfect RCA mid-outage.
- **Trusting the loudest error.** The error filling the logs is often a downstream *symptom* (cascading timeouts, retry amplification). Trace upstream to the first failure in time, not the most frequent.
- **"Deploy at the same time = the cause."** Temporal coincidence is a hypothesis, not proof. A config change, traffic spike, or expiring cert can hide behind an innocent deploy. Verify the causal link.
- **Premature severity downgrade.** "Probably just a few users" → it's the whole region. When scope is unknown, hold the higher severity until you've *measured* it smaller.
- **Irreversible "fix" under pressure.** Deleting rows / dropping a table / force-pushing / running a destructive migration to "clear the bad state" turns a recoverable outage into permanent data loss. Escalate to a human before anything irreversible.
- **Looking at one signal only.** Metrics-only = you see the *symptom* but not *why*. Logs-only = you miss the blast radius. Traces-only = you miss the trend. The story lives at the intersection, pinned to one time window.
- **Blameful postmortem.** Naming who-did-it makes people hide info next time and kills the learning. The action item is a missing guardrail, never a missing person.
- **Action items with no owner/date.** "Improve monitoring" never ships. Each item needs a name, a date, and a priority, or it's decoration.
- **Declaring "fixed" without watching recovery.** Mitigation applied ≠ recovered. Confirm on the exact metric that originally broke before standing down.

## Verify

- **During incident:** the metric that first broke (step 3) is back to baseline AND held there for a sustained window — not a momentary dip. Error rate / latency / saturation confirmed normal on the dashboard, not assumed.
- **Mitigation safety:** every action taken was reversible, or a human explicitly approved any irreversible one. You can state how to undo each.
- **Severity correct in hindsight:** measured impact matches (or was higher than) the declared severity — you didn't under-call it.
- **Postmortem complete:** all required sections present; root cause has ≥1 contributing factor beyond the trigger; every action item has owner + date + priority; language is blameless (no person named as cause).
- **Loop closed:** at least one action item became a real guardrail (alert/canary/rollback/flag) or a runbook so the same incident is faster/prevented next time.
