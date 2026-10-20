---
name: chaos-engineering-and-resilience-testing
description: >
  Guides running chaos engineering experiments — defining a measurable
  steady-state hypothesis, controlling blast radius, and using
  fault-injection tools (Chaos Mesh, LitmusChaos, AWS Fault Injection
  Simulator) to proactively validate a system's resilience assumptions —
  plus running structured "game days" and graduating experiments from
  staging to controlled production runs. Use when a user asks to "run a
  chaos engineering experiment", "test what happens if we kill a pod/
  lose an AZ", "run a game day", "validate our failover actually works",
  or "find resilience gaps before a real incident does."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: site-reliability-engineering
  maturity: stable
---

# Chaos Engineering and Resilience Testing

## Purpose

Architectural resilience — "we have three replicas," "we failover across
availability zones," "the circuit breaker handles that dependency being
slow" — is an assumption until it has been deliberately tested under
real fault conditions; otherwise the first real test of that assumption
is an actual outage, at the worst possible time, with no rollback ready.
Chaos engineering is the discipline of injecting controlled failure into
a system to verify that a measurable steady-state hypothesis holds under
turbulent conditions, with blast radius deliberately limited so the
experiment itself never becomes the incident it was meant to prevent.
This skill covers defining a testable steady-state hypothesis, choosing
and scoping fault-injection tools, running a structured "game day"
exercise, and graduating experiments from staging to carefully controlled
production runs — deliberately, with the same change-management rigor as
a production deployment.

## When to use

- Validating that a specific redundancy/failover assumption (multiple
  replicas, multi-AZ, a circuit breaker, a retry policy) actually holds
  under real fault conditions rather than just on paper.
- Running a scheduled "game day" exercise across one or more teams.
- Before or after adopting a new dependency or failover design, to
  confirm the failure-handling behavior it's supposed to provide.
- Incidents keep surprising the team despite an architecture that "should
  have been resilient" — a sign the resilience claims were never
  actually tested.
- Deciding whether/how to graduate an experiment that has run cleanly in
  staging into a carefully scoped production experiment.

## Prerequisites & environment

- Existing steady-state dashboards/SLIs to compare against during the
  experiment — see
  [slo-sli-and-error-budget-design](../slo-sli-and-error-budget-design/SKILL.md)
  and the
  [Prometheus and Grafana monitoring stack](../../../observability-and-platform-extras/skills/prometheus-and-grafana-monitoring-stack/SKILL.md)
  skill for how these are typically built.
- A fault-injection tool matched to the environment: **Chaos Mesh** or
  **LitmusChaos** for Kubernetes-native experiments (pod kill, network
  delay/partition, IO stress); **AWS Fault Injection Simulator (FIS)**
  for AWS infrastructure-level faults (instance/AZ/RDS failover, network
  disruption); a commercial cross-platform option such as **Gremlin** is
  also common. Pick based on where the target system runs.
- An automated abort/rollback mechanism tied to the same steady-state
  metrics (not solely a human watching a dashboard and deciding to stop).
- Explicit blast-radius scoping ability: a label selector/namespace, a
  percentage of pods/instances, or a single availability zone — never
  "the whole production fleet" as a starting scope.
- Stakeholder sign-off and a scheduled window for any experiment that
  could have customer-visible impact, and awareness from the on-call/
  incident-response path that the experiment is running (so a real
  responder isn't confused about whether it's a drill or a genuine
  incident) — see
  [incident-response-and-on-call-management](../incident-response-and-on-call-management/SKILL.md).

## Step-by-step guidance

1. **Define a measurable steady-state hypothesis** tied to an existing
   SLI/SLO, not a vague expectation:
   ```
   Hypothesis: during the experiment, checkout success rate stays
   >= 99.5% and p99 latency stays < 400ms (same thresholds as the
   service's existing SLO dashboard).
   ```
   If you can't state the hypothesis as a number you're already
   measuring, define that measurement first — don't run the experiment
   against a vague "should be fine."

2. **Start with the smallest reasonable blast radius**, in a
   non-production environment first: a single pod/instance, a small
   percentage of traffic, a short duration — with an explicit automatic
   abort condition wired to the same steady-state metric, plus a manual
   kill switch as backup.

   > **Warning:** Running a chaos experiment with no blast-radius limit
   > and no automated abort condition — especially directly in
   > production — is a destructive action: it can turn a controlled
   > experiment into a genuine, uncontrolled outage with no faster path
   > to recovery than a real incident. Always scope blast radius
   > explicitly and always define an abort trigger *before* starting.

3. **Write the experiment definition.** Chaos Mesh example — killing one
   pod, once, scoped to a label selector and namespace:
   ```yaml
   apiVersion: chaos-mesh.org/v1alpha1
   kind: PodChaos
   metadata:
     name: payments-api-pod-kill
     namespace: payments
   spec:
     action: pod-kill
     mode: fixed
     value: "1"                 # exactly one pod, not a percentage of all
     selector:
       namespaces:
         - payments
       labelSelectors:
         app: payments-api
     scheduler:
       cron: "@once"
   ```
   A LitmusChaos experiment expresses the same idea as a
   `ChaosEngine`/`ChaosExperiment` CR referencing the `pod-delete`
   experiment with a scoped `appinfo` selector. AWS FIS expresses an
   infrastructure-level equivalent as an experiment template targeting
   specific EC2 instances/AZs by resource tag, with a `stopCondition`
   bound to a CloudWatch alarm — the FIS `stopCondition` is the
   equivalent of the automated abort trigger and should always be set,
   never left as "none."

4. **Run the experiment while watching the steady-state dashboard
   live.** If the hypothesis holds, gradually increase blast radius on
   subsequent runs (more pods, longer duration, an added fault type). If
   it breaks, abort immediately via the automated trigger or the manual
   kill switch, treat the deviation like a real incident (declare
   severity, assemble IC/roles per
   [incident-response-and-on-call-management](../incident-response-and-on-call-management/SKILL.md)),
   and drive the finding through the same action-item process as
   [blameless-postmortem-and-root-cause-analysis](../blameless-postmortem-and-root-cause-analysis/SKILL.md).

5. **Run a structured "Game Day"** — a scheduled, cross-team exercise
   combining multiple fault scenarios (e.g. an AZ outage simulated
   together with a downstream dependency timeout) with an explicit
   facilitator, observers, and a scribe, run exactly like a live
   incident drill using the same IC/Comms/Tech-Lead roles from
   [incident-response-and-on-call-management](../incident-response-and-on-call-management/SKILL.md).
   Announce it in advance to anyone who might otherwise mistake it for a
   real incident, and debrief immediately afterward while details are
   fresh.

6. **Graduate to production only deliberately** — after repeated clean
   runs in staging, with progressively larger (but still bounded) blast
   radius, explicit stakeholder sign-off, off-peak scheduling, and an
   automated abort trigger wired to real production SLIs (not solely
   human judgment in the moment). Treat a production chaos experiment
   with the same change-management rigor as a deployment — announced,
   scheduled, with a rollback path ready; the traffic-shifting/rollback
   mechanics in
   [blue-green-canary-deployments](../../../devops/skills/blue-green-canary-deployments/SKILL.md)
   are a reasonable abort mechanism for experiments that involve routing
   traffic away from an affected instance/AZ.

7. **Feed findings back deliberately.** A broken assumption becomes a
   tracked action item through the postmortem process, not just a
   Slack message. A *validated* assumption becomes documented evidence
   supporting the organization's
   [disaster-recovery-and-backup-strategy](../../../cloud/skills/disaster-recovery-and-backup-strategy/SKILL.md)
   — chaos engineering is how DR/HA assumptions get empirically tested,
   rather than asserted in a document that's never been exercised.

## Best practices

- Never run an experiment without an automated abort condition tied to
  a real SLI — a human "keeping an eye on it" is not a substitute for a
  wired trigger, especially once experiments reach production.
- Vary fault type deliberately across the maturity path: start with
  process/pod kill, then network latency/partition, then a downstream
  dependency failure/timeout, and only later a full AZ/region loss
  (coordinated with the DR plan) — each fault type tests a different
  resilience mechanism.
- Keep game days blameless and educational, same as postmortems — the
  point is to find gaps in the system, not to test individual
  responders' performance.
- Chaos engineering *validates* DR/HA assumptions empirically; it
  doesn't replace having an actual DR strategy and runbook in the first
  place — see
  [disaster-recovery-and-backup-strategy](../../../cloud/skills/disaster-recovery-and-backup-strategy/SKILL.md)
  for designing that plan.
- Graduate blast radius gradually and reversibly rather than either
  never running production experiments at all, or jumping straight to a
  large-scope production test.
- Track chaos-experiment findings through the same action-item
  ownership/due-date discipline as postmortems — an unaddressed finding
  is a known, undocumented risk.

## Common pitfalls

- **Symptom:** A chaos experiment is run directly against production
  with no blast-radius limit and no abort condition, and it causes a
  full, customer-visible outage that takes as long to recover from as a
  genuine incident would have.
  **Fix:** Always scope blast radius explicitly (a label selector, a
  fixed count/percentage, a single AZ) and always define an automated
  abort trigger tied to a real SLI before the experiment starts; rehearse
  in staging first and graduate deliberately (steps 2 and 6).

- **Symptom:** The team declares an experiment "passed" or "failed" based
  on a vague feeling ("seemed fine") rather than a specific measurement,
  and later a real incident reveals the same failure mode the experiment
  supposedly already covered.
  **Fix:** Define the steady-state hypothesis as a concrete number tied
  to an existing SLI/SLO before running anything (step 1) — if it can't
  be stated numerically, the experiment isn't ready to run yet.

- **Symptom:** The team runs chaos experiments only in staging, year
  after year, because "production is too risky," and a real production
  incident later reveals a failure mode that staging never actually
  represented (different scale, different traffic mix, different AZ
  topology).
  **Fix:** Graduate deliberately with small, reversible, well-announced
  production experiments (step 6) rather than treating "never in
  production" as a permanent policy — validated staging behavior does
  not guarantee production behavior at real scale.

- **Symptom:** A game day surfaces a real gap (e.g. a circuit breaker
  with no configured timeout), it's discussed in the debrief, and then
  nobody revisits it — six months later a real incident hits the exact
  same gap.
  **Fix:** Run every chaos/game-day finding through the same
  action-item tracking as a postmortem (owner, ticket, due date) rather
  than letting it live only in a debrief doc.

- **Symptom:** Every experiment so far has only ever killed an
  application pod; the team has never tested a downstream dependency
  timing out, a full AZ loss, or a DNS failure — exactly the failure
  modes most likely to cause a real major outage.
  **Fix:** Deliberately vary fault type across experiments (pod kill →
  network latency/partition → downstream dependency failure → AZ/region
  loss) instead of repeating the same, easiest experiment.

## Worked example

**Scenario:** the `payments-api` team wants to validate that losing one
of three replicas doesn't cause customer-visible impact, given a
configured `PodDisruptionBudget`.

1. **Hypothesis:** checkout success rate stays ≥99.5% and p99 latency
   stays <400ms, measured against the service's existing SLO dashboard.
2. **Experiment 1 (staging → prod, small blast radius):** the Chaos Mesh
   `PodChaos` definition from step 3 kills exactly one of three
   `payments-api` pods, once, with an automatic abort if error rate
   crosses 2% during a 5-minute observation window. Result: steady state
   holds — the deployment's redundancy behaves as claimed.
3. **Experiment 2 (new fault type):** a `NetworkChaos` experiment injects
   200ms of latency toward the downstream fraud-check dependency to test
   timeout/circuit-breaker handling. Result: the hypothesis breaks — the
   circuit breaker had no configured timeout, and checkout latency spikes
   past the SLO threshold with customer-visible impact. The experiment is
   aborted via the automated trigger, treated as an incident, and the gap
   becomes a tracked postmortem action item (add an explicit timeout and
   fallback path to the fraud-check client).
4. **Quarterly Game Day:** after both the pod-kill and dependency-timeout
   fixes are validated individually, a full AZ-loss scenario is simulated
   using AWS FIS against a non-production account mirroring the
   production topology, run as a live-incident-style drill with IC/Comms/
   Scribe roles, validating that the documented DR pilot-light failover
   in
   [disaster-recovery-and-backup-strategy](../../../cloud/skills/disaster-recovery-and-backup-strategy/SKILL.md)
   actually works end to end — before ever attempting a comparable
   experiment in the real production account.

## Cross-references

- [capacity-planning-and-load-testing](../capacity-planning-and-load-testing/SKILL.md) — load/stress testing finds capacity ceilings under expected traffic; chaos experiments find failure-handling gaps under fault conditions — the two are complementary, not substitutes for each other.
- [incident-response-and-on-call-management](../incident-response-and-on-call-management/SKILL.md) — game days rehearse the same IC/Comms/Scribe roles used in a real incident, and a broken experiment should be handled through the same process.
- [blameless-postmortem-and-root-cause-analysis](../blameless-postmortem-and-root-cause-analysis/SKILL.md) — chaos and game-day findings should be tracked through the same owned, due-dated action-item process as any other incident.
- [blue-green-canary-deployments](../../../devops/skills/blue-green-canary-deployments/SKILL.md) — traffic-shifting/rollback mechanics are a practical abort path for experiments that involve routing production traffic away from an affected instance or AZ.
- [environment-promotion-strategy](../../../devops/skills/environment-promotion-strategy/SKILL.md) — graduating an experiment from staging to controlled production runs mirrors the same gated-promotion thinking used for releases.
- [disaster-recovery-and-backup-strategy](../../../cloud/skills/disaster-recovery-and-backup-strategy/SKILL.md) — chaos engineering is how DR/HA assumptions get empirically validated; this skill exercises the plan, it doesn't replace designing it.
