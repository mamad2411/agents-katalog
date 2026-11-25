---
name: hashicorp-nomad-scheduling-and-configuration
description: >
  Configures HashiCorp Nomad job specifications, scheduler types, and
  cluster topology as a lighter-weight alternative to Kubernetes for
  scheduling containers, binaries, and batch/system workloads. Use when
  the user asks to "write a Nomad job spec," "choose service vs. batch
  vs. system scheduler in Nomad," "compare Nomad to Kubernetes for our
  use case," "set up Nomad server/client topology," "add a Nomad
  update/canary deployment strategy," or "run non-containerized
  workloads under a scheduler."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: serverless-and-alternative-compute
  maturity: stable
---

# HashiCorp Nomad Scheduling and Configuration

## Purpose

Nomad is a single-binary, general-purpose scheduler that runs
containers, standalone binaries, Java applications, and VMs under one
job specification format, with a notably simpler operational model than
Kubernetes — one binary for both server and client roles, no separate
etcd cluster to operate, and a smaller set of core concepts (jobs,
task groups, tasks, scheduler types). It is not a Kubernetes
replacement in every case: Kubernetes' ecosystem (CRDs, service mesh
integrations, the broader operator pattern) is deeper, and most
organizations already standardized on Kubernetes won't switch wholesale.
Nomad earns its place where the operational simplicity, mixed
containerized/non-containerized workload support, or lower
resource/operational overhead is the deciding factor — this skill
covers writing job specs, choosing scheduler types, and the cluster
topology decisions specific to Nomad.

## When to use

- Writing or reviewing a Nomad job specification (HCL) for a service,
  batch, or system workload.
- Deciding whether a workload/environment is better served by Nomad or
  Kubernetes, when neither is already an unchangeable given.
- Configuring Nomad server/client topology, including federation across
  regions/datacenters.
- Setting up a rolling update, canary, or blue/green deployment strategy
  for a Nomad job.
- Running mixed workloads (containers alongside raw-exec binaries,
  Java, or VM tasks) under a single scheduler.

## Prerequisites & environment

- Nomad servers (an odd number, typically 3 or 5, for Raft quorum) and
  one or more Nomad client nodes — check the specific Nomad version's
  documented Raft protocol version and autopilot defaults, since
  cluster-management behavior has changed across major versions.
- A driver enabled on client nodes for each task type in use (`docker`,
  `exec`, `raw_exec`, `java`, `qemu`) — `raw_exec` in particular is
  disabled by default and, when enabled, allows a task to run as an
  arbitrary unsandboxed process on the client host, so enable it only
  where that trust level is genuinely intended.
- Consul (optional but common) for service discovery and health checks
  referenced from job specs via the `service` stanza; Vault (optional)
  for dynamic secrets injected into tasks via the `template` stanza.
- ACLs enabled and bootstrapped for any cluster handling anything
  beyond a local experiment — Nomad's ACL system is opt-in and not
  enabled by default on a fresh cluster.
- The `nomad` CLI matching (or compatible with) the cluster's server
  version.

## Step-by-step guidance

1. **Choose the scheduler type per job based on the workload's actual
   lifecycle**, not defaulting to `service` for everything:
   - `service` — long-running processes that should be restarted on
     failure and kept at a target count (the Nomad analog of a
     Kubernetes `Deployment`).
   - `batch` — run-to-completion workloads (the Nomad analog of a
     Kubernetes `Job`), optionally on a `periodic` schedule (the analog
     of a `CronJob`).
   - `system` — one instance per eligible client node (the Nomad analog
     of a Kubernetes `DaemonSet`), for node-level agents like log
     shippers or monitoring exporters.
   - `sysbatch` — batch semantics but run once per eligible node,
     combining `system`'s node-scoping with `batch`'s run-to-completion
     semantics.

2. **Write the job spec with explicit resource requests and a matching
   scheduler type**:
   ```hcl
   job "checkout-api" {
     datacenters = ["dc1"]
     type        = "service"

     group "api" {
       count = 3

       network {
         port "http" { to = 8080 }
       }

       service {
         name = "checkout-api"
         port = "http"
         check {
           type     = "http"
           path     = "/healthz"
           interval = "10s"
           timeout  = "2s"
         }
       }

       task "api" {
         driver = "docker"

         config {
           image = "registry.example.com/checkout-api:2.3.0"
           ports = ["http"]
         }

         resources {
           cpu    = 500
           memory = 512
         }
       }
     }
   }
   ```
   The `service` stanza's `check` block registers a Consul health check
   (if Consul is integrated) so downstream service discovery only
   routes to instances passing it — the Nomad equivalent of a
   Kubernetes readiness probe gating Service endpoint membership.

3. **Configure an update strategy for rolling deploys, rather than
   accepting the scheduler's default all-at-once replacement**:
   ```hcl
   group "api" {
     count = 6

     update {
       max_parallel     = 2
       min_healthy_time = "30s"
       healthy_deadline = "5m"
       auto_revert      = true
       canary           = 1
     }
     # ... network/service/task as above
   }
   ```
   `canary = 1` deploys one canary allocation running the new version
   alongside the existing ones; `auto_revert = true` automatically rolls
   back to the last stable version if the new allocations don't reach
   healthy status within `healthy_deadline` — the same intent as a
   Kubernetes `Deployment`'s `maxSurge`/`maxUnavailable` combined with a
   readiness-gated rollout, expressed in Nomad's own vocabulary.

4. **Use `constraint` and `affinity` stanzas to place workloads
   deliberately**, not leave every allocation schedulable anywhere:
   ```hcl
   constraint {
     attribute = "${node.class}"
     value     = "compute-optimized"
   }

   affinity {
     attribute = "${meta.rack}"
     value     = "rack-2"
     weight    = 50
   }
   ```
   `constraint` is a hard requirement (the allocation won't schedule
   anywhere that doesn't match); `affinity` is a soft preference scored
   during placement — use `constraint` for genuine hardware/driver
   requirements and `affinity` for preferences that shouldn't block
   scheduling entirely if unmet.

5. **Configure server/client topology and federation deliberately** for
   multi-region deployments — each region runs its own Nomad server
   cluster (its own Raft quorum), federated together for cross-region
   visibility and job dispatch, rather than a single global server
   quorum spanning regions (which would suffer Raft consensus latency
   across the WAN):
   ```hcl
   # server config fragment
   server {
     enabled          = true
     bootstrap_expect = 3
   }
   ```
   Federation is established by joining servers across regions via
   `server_join` / `nomad server join`, not by adding cross-region
   nodes to the same Raft quorum.

6. **Decide Nomad vs. Kubernetes per environment/workload class**, not
   as an org-wide either/or: Nomad tends to fit environments needing a
   simpler operational model, mixed container/non-container workloads
   on the same scheduler, or edge/constrained-resource deployments where
   Kubernetes' control-plane footprint is disproportionate; Kubernetes
   tends to fit environments already invested in its ecosystem (CRDs,
   service mesh, a large operator library) where that depth outweighs
   Nomad's simplicity. Running both for different workload classes in
   the same organization is a legitimate outcome, not an inconsistency
   to eliminate.

## Best practices

- Set explicit `resources { cpu, memory }` on every task — an
  under-specified task can be bin-packed onto a client node far more
  aggressively than the workload can actually tolerate, the same risk
  as an unset Kubernetes pod resource request.
- Use `canary` + `auto_revert` on any job whose failure is
  user-visible, not just a plain rolling update with no health
  validation gate before proceeding to the next batch.
- Enable ACLs and Consul/Vault integration (via the `service` and
  `template` stanzas) rather than relying on network-level isolation
  alone — a cluster with ACLs disabled trusts every client with a
  network path to the API with full control-plane access.
- Keep `raw_exec` disabled unless a specific, understood workload needs
  unsandboxed process execution; prefer the `docker` or `exec` (chroot/
  cgroup-isolated) drivers for anything that doesn't have that
  requirement.
- Version-control job specs (HCL) the same as any other deployment
  artifact, and apply them through `nomad job plan` (a dry-run diff)
  before `nomad job run`, mirroring `terraform plan`/`apply` discipline.
- Reassess the Nomad-vs-Kubernetes decision per new workload class
  rather than assuming whichever was chosen first is right for
  everything going forward — the two are not mutually exclusive across
  an organization's overall estate.

## Common pitfalls

- **Symptom:** A job update replaces all allocations at once, and a bad
  release causes a full outage instead of a partial one.
  **Fix:** No `update` stanza (or one with `max_parallel` set too high
  relative to `count`) was configured; add `max_parallel`, `canary`,
  and `auto_revert` so a bad release is caught on a small subset of
  allocations before it reaches the full fleet.

- **Symptom:** Nomad client nodes are running arbitrary unsandboxed
  processes that shouldn't have host-level access.
  **Fix:** The `raw_exec` driver was enabled without a specific need;
  disable it on client nodes that don't require it, and restrict which
  jobs/operators can target clients where it remains enabled.

- **Symptom:** A multi-region Nomad deployment suffers slow leader
  elections or degraded API responsiveness after adding servers in a
  distant region to what was assumed to be a single cluster.
  **Fix:** Servers across regions were joined into a single Raft quorum
  instead of being federated as separate per-region server clusters;
  reconfigure each region with its own `bootstrap_expect`-sized quorum
  and federate them, rather than spanning one quorum across a
  high-latency WAN link.

- **Symptom:** An operator with only a network path to the Nomad API
  (no credentials) is able to submit or stop jobs.
  **Fix:** ACLs were never bootstrapped on the cluster (Nomad ACLs are
  opt-in); bootstrap the ACL system, issue scoped tokens per
  team/service, and require a valid token for all job-management
  operations going forward.

- **Symptom:** A batch job scheduled with `periodic` runs multiple
  overlapping instances when a run takes longer than the scheduled
  interval.
  **Fix:** The job's `periodic` stanza defaults (or an explicit
  `prohibit_overlap = false`) allow overlapping runs; set
  `prohibit_overlap = true` if concurrent runs of the same periodic job
  would corrupt shared state or duplicate work.

## Worked example

**Scenario:** A batch data-processing job currently runs as a single
all-at-once Kubernetes `CronJob` but needs to move to a Nomad cluster
already running the organization's non-containerized legacy binaries,
with a scheduled hourly run that must never overlap with a still-running
previous execution.

```hcl
job "hourly-report-batch" {
  datacenters = ["dc1"]
  type        = "batch"

  periodic {
    cron             = "0 * * * *"
    prohibit_overlap = true
    time_zone        = "UTC"
  }

  group "report" {
    count = 1

    task "generate" {
      driver = "docker"

      config {
        image   = "registry.example.com/report-generator:1.2.0"
        command = "/app/generate-report.sh"
      }

      resources {
        cpu    = 1000
        memory = 1024
      }

      restart {
        attempts = 2
        interval = "10m"
        delay    = "30s"
        mode     = "fail"
      }
    }
  }
}
```
`prohibit_overlap = true` guarantees a new hourly invocation won't start
while a prior run (delayed by unusually large input data, for example)
is still executing; `restart` with `mode = "fail"` gives the task two
retry attempts within a 10-minute window before the allocation is
marked failed rather than retried indefinitely. The job is applied with
a dry-run first:
```bash
nomad job plan hourly-report-batch.nomad.hcl
nomad job run hourly-report-batch.nomad.hcl
```
`nomad job plan` shows the diff against the currently running job
definition (or confirms it as a new job) before anything is actually
scheduled, the same review step `terraform plan` provides for
infrastructure changes.

## Cross-references

- [knative-serverless-configuration](../knative-serverless-configuration/SKILL.md) — a Kubernetes-native scheduling/scaling model to compare against when deciding whether Nomad's simpler operational footprint is the better fit for a given workload.
- [dapr-distributed-runtime-configuration](../dapr-distributed-runtime-configuration/SKILL.md) — Dapr's sidecar building blocks can run on Nomad-scheduled tasks the same as on Kubernetes pods, for teams wanting consistent state/pub-sub/service-invocation APIs across both schedulers.
- [aws-lambda-packaging-and-configuration](../aws-lambda-packaging-and-configuration/SKILL.md) — a fully managed alternative to self-operating a Nomad (or Kubernetes) cluster at all, worth weighing when the workload doesn't need long-running processes or non-containerized task types.
