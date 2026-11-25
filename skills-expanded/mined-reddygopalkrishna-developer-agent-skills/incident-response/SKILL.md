---
name: incident-response
description: Guides production incident handling - assess severity, mitigate first (roll back, disable a flag, scale, fail over), then diagnose from recent changes, metrics, logs and traces, keep a timestamped timeline, draft status updates, and write a blameless postmortem with owned action items. Use when production is down or degraded, errors or latency spike, an alert fires, users report an outage, or the user asks for an incident review or postmortem. Not for debugging in local or development environments.
license: MIT
---

# Incident Response

Restore service first; find the root cause second. During an incident the agent investigates, proposes and records. A human approves every action that changes production.

## Hard safety rules

- **Read-only investigation is fine** once the user asks for help: dashboards, logs, traces, `kubectl get/describe/logs`, read-only queries, `git log`.
- **Never run a production-changing action without explicit confirmation for that specific action.** This includes rollbacks, deploys, restarts, scaling, feature flag changes, failovers, config or DNS changes, cache flushes, queue purges, and data fixes. For each one, present: the exact command, the expected effect, the blast radius, and how to undo it. Then wait.
- **Draft, never send.** Status page posts, chat announcements, customer emails and tickets are drafted for a human to send.
- **Protect data.** Do not paste secrets, tokens or personal data from logs into chat, tickets or the postmortem. Redact.

## Workflow

1. **Triage (first few minutes).** What is broken, for whom, since when? Confirm it is real and not a monitoring failure. Assign a severity (table below). Make sure a human incident commander is named and an incident channel or doc exists. Start the timeline.
2. **Check recent changes first.** Most incidents follow a change. Look at, in order:
   - Deploys of the affected service and its dependencies (app and infrastructure).
   - Config changes, feature flag changes, secret or certificate rotations.
   - Dependency and cloud provider status pages.
   - Traffic changes: spikes, a new client, a bot, a marketing event.
   - Scheduled jobs, data migrations, backfills.
   - Expiring certificates, domains, quotas, credits.
3. **Mitigate with the fastest reversible option,** even before the root cause is certain (table below). If an incident started right after a deploy, rolling back is usually the right first move. Propose it; get approval.
4. **Verify the mitigation.** Error rate, latency and saturation are back at baseline, and the user-visible symptom is gone. Keep watching for at least 15-30 minutes.
5. **Diagnose the root cause** once service is stable (or in parallel, by someone else, if no mitigation is available).
6. **Communicate on a fixed cadence** (see severity table). Send an update even when there is no news. Templates in [references/status-updates.md](references/status-updates.md).
7. **Resolve** when metrics have been stable for the agreed period. Record follow-ups as tickets.
8. **Postmortem** within about five business days for SEV1 and SEV2. Template in [references/postmortem-template.md](references/postmortem-template.md).

## Severity

Use the organization's own definitions if they exist (search the repo and wiki for runbooks, "severity", "SEV", on-call docs). Otherwise use this typical scale:

| Level | Meaning | Typical response |
|---|---|---|
| SEV1 | Full outage, data loss or corruption, security breach, major revenue impact | All hands now; updates about every 30 min; leadership and customer comms |
| SEV2 | Major feature down or severe degradation for many users; no easy workaround | On-call plus owning team now; updates every 30-60 min |
| SEV3 | Partial degradation, small set of users, workaround exists | Owning team during working hours; updates as status changes |
| SEV4 | Cosmetic or very low impact | Normal ticket |

When unsure between two levels, pick the higher one; downgrading later is cheap.

## Roles

| Role | Does | Does not |
|---|---|---|
| Incident commander (human) | Coordinates, sets priorities, approves actions, decides when resolved | Debug hands-on |
| Operations lead | Investigates and executes approved mitigations | Make changes nobody else knows about |
| Communications lead | Writes and sends status updates internally and externally | Speculate about root cause publicly |
| Scribe | Keeps the timeline | Filter out "unimportant" events |

The agent's role is investigator and scribe: gather data, rank hypotheses, draft commands and updates, and keep the timeline.

## Mitigation options

| Option | Use when | Watch out for |
|---|---|---|
| Roll back the last deploy | Start time correlates with a deploy | Database migrations that are not backward compatible: old code may fail against the new schema. Check first. |
| Disable a feature flag / kill switch | A new feature is implicated | Flags with side effects on data already written |
| Scale out or up | Saturation (CPU, memory, connections, queue depth) from load | Pushing the bottleneck to the database or a downstream service |
| Fail over or drain a region, zone or node | Failure is localized | Capacity of the remaining region; data replication lag |
| Restart | Leak, deadlock, stuck process; buys time | Destroys evidence. Capture a thread dump, heap stats or logs first if cheap. |
| Rate limit, shed load, or block a client | Traffic spike or abuse | Blocking legitimate users; communicate it |
| Revert config, renew certificate, restore a rotated secret | Config, certificate or secret change correlates | Caches holding the bad value |
| Pause non-critical consumers or batch jobs | Resource contention | Backlog to drain afterwards |
| Degrade gracefully | Serve cached or static content, disable expensive features | Make the degraded mode visible to users |

## Diagnosis

- **Broad to narrow.** Which endpoints, regions, versions, customers, hosts or pods? Compare against a healthy baseline (same time yesterday or last week).
- **RED per service** (rate, errors, duration) and **USE per resource** (utilization, saturation, errors).
- **Correlate the start time** with the change list from step 2.
- **Logs:** filter to the window and service, count by error message, find the first occurrence.
- **Traces:** open the slowest and failing traces and find which span or dependency dominates.
- **Read-only commands** that are usually safe:

  ```bash
  kubectl get pods -n <ns> -o wide
  kubectl describe pod <pod> -n <ns>
  kubectl logs <pod> -n <ns> --since=30m
  kubectl logs <pod> -n <ns> --previous          # last crashed container
  kubectl get events -n <ns> --sort-by=.lastTimestamp
  kubectl rollout history deployment/<name> -n <ns>
  git log --since="6 hours ago" --oneline
  ```

- **Common root causes:** bad deploy; config error; expired certificate; DNS; resource exhaustion (disk full, connection pool, file descriptors, memory, rate limits or quotas); dependency outage; retry storms; cache stampede after expiry or flush; poison message or bad input data; clock or time zone bugs; a scheduled job colliding with peak traffic.
- **Keep a hypothesis list** with evidence for and against each. Test the cheapest-to-check hypothesis first.

## Timeline

Record everything in UTC, as it happens:

```
14:02 UTC  Alert: checkout 5xx rate above 5% (source: monitoring)
14:05 UTC  IC: Priya. Declared SEV2. Channel #inc-checkout opened.
14:09 UTC  Observation: deploy of checkout v2026.11.03.2 finished 13:58
14:12 UTC  Proposed rollback to v2026.11.03.1; approved by IC
14:15 UTC  Rollback complete (ops lead ran it)
14:24 UTC  5xx back to baseline 0.2%; monitoring
```

Include detection, every action (who ran what), observations, decisions, and every communication sent.

## Postmortem

- **Blameless.** Describe what the system and process allowed, not who made a mistake. Ask "what made this action reasonable at the time?"
- **Root cause and contributing factors.** Incidents usually have several; list them all (the trigger, why it was not caught, why detection or mitigation was slow).
- **Action items** are specific, owned, dated and tracked in the issue tracker. Prioritize prevention, then faster detection, then faster mitigation. "Be more careful" is not an action item.
- **Measure** time to detect, time to mitigate, time to resolve.

## Anti-patterns

- **Debugging while users are down** when a rollback was available.
- **Uncoordinated changes** by several people at once without the incident commander.
- **Restarting everything** and losing the evidence.
- **Unlogged actions** that nobody can reconstruct later.
- **Silence** — long gaps without a status update.
- **Rolling back code past a non-backward-compatible migration.**
- **Declaring resolved too early,** before metrics stay stable.
- **Blame,** or action items without owners and dates.

## Done when

Incident:
- [ ] Metrics are at baseline for the agreed period and the symptom is gone.
- [ ] The timeline is complete with UTC timestamps.
- [ ] A final status update was drafted and approved.
- [ ] Follow-up tickets exist.

Postmortem:
- [ ] Impact is quantified (duration, users or requests affected, revenue or SLO budget if known).
- [ ] Timeline includes detection, mitigation and resolution times.
- [ ] Root cause and contributing factors are described without blame.
- [ ] Every action item has an owner, a due date and a ticket.

## References

- [references/status-updates.md](references/status-updates.md) — read when drafting internal or external status updates during an incident.
- [references/postmortem-template.md](references/postmortem-template.md) — read when writing the postmortem after the incident.
