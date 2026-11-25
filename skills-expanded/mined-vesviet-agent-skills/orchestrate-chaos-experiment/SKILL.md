---
name: orchestrate-chaos-experiment
description: Plan, execute, and verify controlled chaos engineering experiments and game days. Use when validating system resilience, steady-state hypotheses, automated failover, blast radius containment, or disaster recovery under injected faults.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Orchestrate Chaos Experiment

Use this skill when planning, executing, and evaluating controlled fault injection experiments, steady-state hypothesis validations, and game day drills.

## When to Use

- validating high-availability failover and circuit-breaker behavior under partial outages
- executing scheduled Game Day drills to test on-call runbooks and automated recovery
- testing upstream/downstream resiliency against injected network latency, packet loss, or partition
- verifying pod crash-loop recovery, node failure evacuation, and horizontal pod autoscaling
- measuring actual Mean Time to Detect (MTTD) and Mean Time to Mitigate (MTTM) during simulated faults

## Core Rules

- define and record quantitative steady-state hypothesis SLIs (P99 latency, error rate, throughput) before any fault injection; an experiment without a baseline hypothesis is an outage, not a drill
- strictly bound failure injection blast radius to canary pods, staging clusters, or maximum 10% of production traffic replicas; never inject unisolated global faults
- configure automated abort triggers and circuit-breakers that halt fault injection immediately if error budget burn rate exceeds 14.4x (1h window) or user error rate exceeds 1%
- require multi-stakeholder approval, an on-call SRE, an active Observer, and a pre-verified manual kill switch before executing production game day drills
- use certified declarative chaos operators (Chaos Mesh, LitmusChaos) with validated CRD manifests; never execute ad-hoc, unversioned destructive shell scripts
- emit an immutable post-drill postmortem capturing injected fault parameters, steady-state deviation, failover duration, and prioritized remediation actions
- refer to `references/chaos-engineering-guide.md` for declarative CRD manifests, fault taxonomies, and game day execution protocols

## Suggested Process

### 1. Formulate Steady-State Hypothesis
Establish quantitative baseline SLIs during normal operating conditions:
- request throughput (RPS) and error rate (<0.1%)
- latency distribution (P95/P99 thresholds)
- downstream dependency availability and queue processing lag

### 2. Design Fault Scenario & Scope Blast Radius
Select failure mode and define containment parameters:
- fault type: pod termination (`PodChaos`), network delay/partition (`NetworkChaos`), CPU/memory pressure (`StressChaos`), or I/O latency (`IOChaos`)
- scope: namespace-bounded, label-selected canary instances (<=10% capacity)
- duration: time-boxed fault window (default 2 to 5 minutes)

### 3. Arm Automated Abort & Pre-Flight Checks
Configure safety mechanisms:
- wire automated rollback monitors to Prometheus/OTel alerts
- test manual abort script (`kubectl delete -f <chaos-manifest.yaml>`)
- verify distributed tracing and eBPF telemetry are actively streaming

### 4. Execute Controlled Injection
Deploy the declarative chaos manifest into the target environment. Monitor real-time logs, socket drops, and health probes.

### 5. Observe System Resilience & Measure Failover
Track behavior against the steady-state hypothesis:
- did redundant replicas take over traffic seamlessly?
- did circuit breakers trip within configured timeout thresholds?
- measure MTTD (first alert signal) and MTTM (traffic stabilization)

### 6. Roll Back & Emit Drill Report
Confirm complete teardown of injected faults. Verify system returns to baseline steady-state. Document results, discrepancies, and preventative action items.

## Checklist

- [ ] steady-state hypothesis defined with quantitative baseline SLIs (throughput, P99 latency, error rate)
- [ ] declarative fault injection manifest authored using Chaos Mesh or LitmusChaos schemas
- [ ] blast radius bounded to <=10% replica capacity and verified namespace labels
- [ ] automated abort criteria and emergency kill switch tested and verified
- [ ] game day drill schedule and on-call stakeholder notifications completed
- [ ] distributed tracing and eBPF socket observability confirmed active
- [ ] post-fault recovery verified with system returned to baseline steady-state
- [ ] drill findings, MTTD/MTTM metrics, and remediation items documented

## Failure Modes

- **Runaway blast radius**: Injected fault affects non-target production workloads. Mitigation: enforce explicit namespace isolation labels, network policies, and hard-stop `duration` limits in chaos CRDs.
- **Alert storm masking**: Chaos test triggers alert cascades that blind on-call responders. Mitigation: define alert inhibition rules during drill windows and route chaos telemetry to dedicated drill dashboards.
- **State corruption / split-brain**: Injected partition causes permanent storage desynchronization. Mitigation: forbid stateful volume corruption without pre-verified point-in-time snapshots and replica backups.
- **Abort mechanism failure**: Operator CRD hangs during teardown. Mitigation: verify direct pod kill/restart fallback scripts before initiating any experiment.

## Output Contracts

When completing a chaos experiment or Game Day drill, emit:

- **`contracts/schemas/incident-report.json`** — Machine-readable drill outcome report capturing timeline, MTTD/MTTM metrics, steady-state deviation, and preventative action items. Set `produced_by_role: sre`.

## Security Guardrails (OWASP ASI)

- **ASI02 Tool Misuse & Exploitation**: Chaos CRD mutations require privileged cluster access; enforce strict RBAC, admission webhooks, and read-only execution audits.
- **ASI05 RCE Guard**: Reject dynamic chaos manifests constructed from external or untrusted user input; use declarative, peer-reviewed YAML templates only.
- **ASI08 Cascading Failures**: Prevent cascading outages by enforcing single-experiment concurrency and immediate automated abort triggers.
- **ASI09 Human-Agent Trust Exploitation**: Require explicit human SRE authorization before executing any production chaos injection; never automate unapproved production outages.

## Related Skills

- **add-telemetry-instrumentation**: Instrument eBPF and OTel metrics required for steady-state baseline tracking
- **incident-report**: Document drill postmortems and track reliability action items
- **debug-runtime-platform**: Diagnose container and platform health during fault injection
- **troubleshoot-service**: Isolate application-level bottlenecks surfaced during stress drills
- **system-design**: Review architecture redundancy, failover topologies, and circuit-breaker patterns
