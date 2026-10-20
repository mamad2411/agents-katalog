---
name: gremlin-chaos-engineering-configuration
description: >
  Configures Gremlin-specific chaos engineering attacks — installing the
  Gremlin agent/sidecar, defining resource, state, and network attacks via
  the Gremlin API/CLI or Terraform provider, scoping blast radius with
  targets and halt conditions, and running Gremlin Scenarios for
  multi-step failure sequences. Use when the user asks to "configure a
  Gremlin attack," "set up the Gremlin agent in Kubernetes/EC2," "write a
  Gremlin Scenario," "scope a Gremlin blast radius/halt condition," or
  "use Gremlin to test our failover." For the general chaos-engineering
  principles (steady-state hypothesis, game days, tool-agnostic blast
  radius scoping) this configures against, use the SRE
  chaos-engineering-and-resilience-testing skill instead.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: iac-and-automation-tooling
  maturity: stable
---

# Gremlin Chaos Engineering Configuration

## Purpose

Gremlin is a commercial, cross-platform fault-injection tool that runs
attacks via a lightweight agent (a Kubernetes DaemonSet/sidecar, a host
daemon on EC2/on-prem, or an ECS task) and a central control plane that
handles targeting, scheduling, and halting attacks — distinct from
Kubernetes-native tools like Chaos Mesh/LitmusChaos in that it works
consistently across Kubernetes, VMs, and bare metal without needing a
different tool per platform. This skill covers the Gremlin-specific
mechanics: installing the agent, defining attacks (resource, state,
network) via the CLI/API/Terraform provider, scoping targets and halt
conditions, and composing multi-step Scenarios. The *why* — steady-state
hypotheses, blast-radius philosophy, game-day facilitation, and
graduating to production — is covered generically in
[chaos-engineering-and-resilience-testing](../../../site-reliability-engineering/skills/chaos-engineering-and-resilience-testing/SKILL.md)
and is not repeated here; apply that skill's principles using Gremlin as
the execution tool.

## When to use

- Standing up Gremlin in a Kubernetes cluster, EC2 fleet, or ECS
  environment for the first time (agent installation, team/target
  configuration).
- Defining a specific Gremlin attack — CPU/memory/disk/IO resource
  attack, a state attack (process kill, shutdown, time travel), or a
  network attack (latency, packet loss, blackhole, DNS) — via the
  Gremlin CLI, API, web UI, or Terraform provider.
- Scoping an attack's blast radius using Gremlin's targeting (exact hosts/
  containers, a percentage of a target group, tag-based selection) and
  configuring a halt condition.
- Composing a multi-step Gremlin **Scenario** that chains several attacks
  in sequence to simulate a more complex failure (e.g., an AZ
  degradation followed by a dependency timeout).
- Migrating an existing Kubernetes-native chaos setup (Chaos Mesh/
  Litmus) to Gremlin for cross-platform consistency, or vice versa.

## Prerequisites & environment

- A Gremlin account/team with API key or Client ID/Secret credentials,
  scoped to the specific team that owns the target infrastructure —
  never a single account-wide credential shared across unrelated teams.
- The Gremlin agent installed on every target:
  - **Kubernetes:** the `gremlin` Helm chart, deployed as a DaemonSet so
    every node runs an agent capable of attacking pods/containers
    scheduled there.
  - **EC2/on-prem (Linux):** the `gremlind` daemon installed via package
    manager, requiring host-level capabilities (it needs privileged
    access to inject resource/network faults, so scope the host/IAM
    permissions around it deliberately).
  - **ECS:** the Gremlin ECS integration, run as a sidecar container in
    the task definition.
- Network egress from the agent to Gremlin's control plane (or a
  configured on-premises relay for network-restricted environments).
- The same automated abort/observability wiring called for generically in
  [chaos-engineering-and-resilience-testing](../../../site-reliability-engineering/skills/chaos-engineering-and-resilience-testing/SKILL.md) —
  Gremlin's own halt conditions (below) are necessary but should be paired
  with your own SLI-based alerting, not relied on alone.

## Step-by-step guidance

1. **Install the agent scoped to the intended blast-radius environment**
   — start in a non-production namespace/cluster/ASG, not org-wide:
   ```bash
   # Kubernetes: install via Helm, scoped to a specific namespace's
   # nodes by targeting later at the attack level, not by limiting
   # agent install (the agent itself is typically cluster-wide, but
   # attacks are scoped per-attack in step 3)
   helm repo add gremlin https://helm.gremlin.com
   helm install gremlin gremlin/gremlin \
     --namespace gremlin --create-namespace \
     --set gremlin.secret.managed=true \
     --set gremlin.secret.type=secret \
     --set gremlin.team_id="$GREMLIN_TEAM_ID" \
     --set gremlin.secret_key="$GREMLIN_SECRET_KEY"
   ```

2. **Define a resource attack** (CPU, memory, disk, or IO exhaustion),
   scoped by an explicit target selector and a fixed duration — never an
   open-ended attack:
   ```bash
   # CLI: 80% CPU load on 1 container matching a label, for 60 seconds
   gremlin attack-container \
     --target-type Label \
     --target-labels app=payments-api \
     --target-exact 1 \
     cpu --cores 2 --length 60
   ```
   The `--target-exact 1` (or an equivalent explicit count/percentage)
   is the blast-radius control — never omit it in favor of an unscoped
   "all matching containers" attack, especially for a first run.

3. **Define a state attack** (process kill, container/host shutdown) to
   test restart/failover behavior specifically:
   ```bash
   gremlin attack-container \
     --target-type Label \
     --target-labels app=payments-api \
     --target-exact 1 \
     shutdown --delay 0
   ```
   This is the Gremlin equivalent of Chaos Mesh's `PodChaos` `pod-kill`
   action — validates the same restart/redundancy assumption, on
   whatever platform the agent runs on (Kubernetes, EC2, or bare metal).

4. **Define a network attack** to test timeout/circuit-breaker handling
   for a specific downstream dependency, rather than a blanket network
   outage:
   ```bash
   # Inject 300ms latency toward a specific downstream hostname only
   gremlin attack-container \
     --target-type Label \
     --target-labels app=payments-api \
     --target-exact 1 \
     latency --delay 300 --hostnames fraud-check.internal
   ```
   Scoping by `--hostnames` (or an equivalent egress-target filter) keeps
   the attack specific to the dependency under test, instead of
   degrading all of that service's network traffic indiscriminately.

5. **Always set an explicit halt condition** tied to a real health check
   or metric, in addition to the attack's own fixed `--length`:
   ```json
   {
     "haltCondition": {
       "type": "metric",
       "metricSource": "datadog",
       "query": "avg:checkout.error_rate{service:payments-api}",
       "comparator": ">",
       "threshold": 2.0
     }
   }
   ```
   > **Warning:** Running a Gremlin attack with no halt condition beyond
   > its fixed duration, especially in production, is a destructive
   > default — a fixed-duration attack still runs to completion even if
   > it's already causing real customer impact partway through. Always
   > pair a duration limit with a metric-based halt condition (or use
   > Gremlin's manual "Halt" action as an immediately-available backup,
   > never the sole safeguard).

6. **Compose a Scenario for a multi-step failure sequence**, chaining
   attacks with delays between them to simulate a realistic compound
   failure (e.g., degraded network to a dependency, followed by a pod
   kill on the retry-exhausted service):
   ```yaml
   # Gremlin Scenario definition (simplified structure)
   name: payments-dependency-degradation-then-restart
   steps:
     - type: attack
       attack:
         type: latency
         target: { labels: { app: payments-api }, exact: 1 }
         args: { delay: 300, hostnames: [fraud-check.internal] }
       delayBeforeNextStep: 120
     - type: attack
       attack:
         type: shutdown
         target: { labels: { app: payments-api }, exact: 1 }
         args: { delay: 0 }
   ```
   Use Scenarios specifically for compound failure modes worth testing
   together (e.g., "does the retry backoff behavior under dependency
   latency make things worse when combined with losing a replica"), not
   as a substitute for the simpler single-attack steps above.

7. **Use the Gremlin Terraform provider to version-control recurring
   attacks/scenarios** (e.g., a scheduled monthly game-day scenario)
   alongside other infrastructure-as-code, instead of only ever
   click-configuring them in the web UI:
   ```hcl
   resource "gremlin_scenario" "monthly_payments_gameday" {
     name = "payments-api-monthly-gameday"
     hypothesis = "checkout success rate stays >= 99.5% during a single replica loss combined with dependency latency"
     steps = [ /* ... */ ]
   }
   ```

## Best practices

- Always scope targets with an exact count or explicit percentage
  (`--target-exact`, a labeled subset), never Gremlin's broadest "all
  matching" default, especially outside of staging.
- Pair every attack's fixed duration with a real metric-based halt
  condition — duration alone is not a safety mechanism if the metric
  degrades before the timer runs out.
- Scope network attacks to the specific downstream hostname/port under
  test rather than blackholing all traffic, so the experiment isolates
  the one dependency behavior being validated.
- Reserve Scenarios for genuinely compound failure modes worth testing
  together; chain only as many steps as the hypothesis actually calls
  for, to keep the experiment's result interpretable.
- Manage recurring/scheduled attacks and scenarios as Terraform (or
  equivalent IaC) resources so they're reviewable and reproducible, not
  only configured ad hoc through the UI.
- Treat the Gremlin agent's host-level privileges (needed to inject real
  resource/network faults) as a security-sensitive install — scope
  credentials per team and restrict who can trigger attacks against
  production targets.

## Common pitfalls

- **Symptom:** An attack is launched against "all containers matching
  this label" with no exact count, and it ends up degrading the entire
  service fleet instead of the single instance intended.
  **Fix:** Always set an explicit `--target-exact` count or a bounded
  percentage (step 2) — never rely on a label selector alone to bound
  blast radius, since the number of matching targets can be larger (or
  grow) beyond what was intended at attack-definition time.

- **Symptom:** A network-latency attack is scoped by target container but
  not by destination hostname, and it ends up delaying *all* of that
  service's outbound traffic (including calls unrelated to the
  dependency being tested), causing broader impact than intended.
  **Fix:** Scope network attacks with `--hostnames`/port filters (step 4)
  to the exact dependency under test, not the target's entire egress
  traffic.

- **Symptom:** A resource attack runs its full fixed duration even though
  the service's error rate spiked well before the timer ended, because no
  halt condition beyond duration was configured.
  **Fix:** Always configure a metric-based halt condition alongside the
  duration (step 5) — a duration limit alone only bounds how long the
  attack runs, not whether it should stop early due to real impact.

- **Symptom:** A team builds an elaborate multi-step Scenario for their
  first-ever Gremlin experiment, and when it fails, it's unclear which
  of the several chained attacks actually caused the problem.
  **Fix:** Start with single, isolated attacks to validate one assumption
  at a time (steps 2-4); reserve Scenarios (step 6) for compound
  failure modes only after the individual attack types involved have
  already been validated separately.

- **Symptom:** Attacks and scenarios are all configured through the web
  UI by whoever happened to set them up, and nobody else on the team
  knows what's currently scheduled or how it's scoped.
  **Fix:** Move recurring/scheduled attacks to the Gremlin Terraform
  provider (step 7) so they're versioned, reviewable, and visible to the
  whole team like any other infrastructure change.

## Worked example

**Scenario:** The `payments-api` team, running on Kubernetes with the
Gremlin agent already installed as a DaemonSet, wants to validate the
same replica-loss resilience hypothesis used in the generic chaos skill's
worked example, but using Gremlin instead of Chaos Mesh, and additionally
test it combined with downstream latency.

1. **Hypothesis** (unchanged from the generic skill): checkout success
   rate stays ≥99.5% and p99 latency stays <400ms.
2. **Single-attack validation first**: a `shutdown` state attack targets
   exactly 1 of 3 `payments-api` pods (`--target-exact 1`), with a halt
   condition on `checkout.error_rate > 2%`. Result: passes, matching the
   earlier Chaos Mesh result — same underlying redundancy assumption,
   validated with a different tool.
3. **Second single-attack validation**: a `latency` network attack
   injects 300ms toward `fraud-check.internal` only (not blackholing all
   egress), again on 1 pod, halt condition on the same error-rate metric.
   Result: fails — same missing circuit-breaker timeout finding as
   before, now confirmed cross-tool.
4. **Compound Scenario, only after both pass/fail individually is
   understood**: after the circuit-breaker timeout fix ships, a Gremlin
   Scenario chains the latency attack followed 2 minutes later by the
   shutdown attack, to check whether losing a replica *while* the
   dependency is degraded (a more realistic simultaneous-failure
   scenario) still holds. Result: passes, giving higher confidence than
   either isolated experiment alone.
5. The Scenario is then captured as a `gremlin_scenario` Terraform
   resource and scheduled to re-run monthly as part of the team's
   recurring game-day cadence defined in
   [chaos-engineering-and-resilience-testing](../../../site-reliability-engineering/skills/chaos-engineering-and-resilience-testing/SKILL.md).

## Cross-references

- [chaos-engineering-and-resilience-testing](../../../site-reliability-engineering/skills/chaos-engineering-and-resilience-testing/SKILL.md) —
  the tool-agnostic principles (steady-state hypothesis, blast-radius
  philosophy, game days, graduating to production) this skill implements
  specifically with Gremlin.
- [infrastructure-post-deployment-validation-and-smoke-testing](../infrastructure-post-deployment-validation-and-smoke-testing/SKILL.md) —
  the same health/smoke-check thinking used for halt conditions here
  applies to verifying a deployment actually worked.
- [ansible-playbook-and-role-design](../ansible-playbook-and-role-design/SKILL.md) —
  a reasonable way to automate installing/configuring the Gremlin agent
  consistently across a fleet of existing hosts.
