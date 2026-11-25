---
name: chaos-test
description: Inject failures (network, latency, crashes) against a running service to verify resilience. Run after adding an external dependency (cache, queue, third-party API), before promoting a service to a higher SLO tier, or before a high-traffic event. Requires a running service — this is not a static resilience review.
kind: skill
pack: distributed-systems
allowed-tools: [Read, Grep, Glob, Bash]
---

# chaos-test

Prove resilience by breaking dependencies on purpose. Unit tests don't cover "Redis is down for 60 seconds".

## Premise

Real signals only. Every "PASSED" / "FAILED" cites a measured baseline + during-chaos + after-recovery comparison from the actual run. Hypothesis stated upfront with concrete numbers (error rate, p99). The fault injection cites the exact tool command (`toxiproxy-cli toxic add ...`, or `kubectl apply -f ...` under the named kubeconfig of § Target safety). Root cause cites `<path:line>` of the code that failed under contention. No "should be resilient" conclusions — either the metrics show it held, or they don't.

**Local first.** The default target is a throwaway stack on this machine: the service's dependencies in Testcontainers (or `docker run`) with Toxiproxy between the service and each dependency. A shared cluster, a staging account or a SaaS chaos tool is used only when the user names it in this session.

## Target safety (read first)

The machine's default kube context may point at a real managed cluster, and its default cloud profile at a real account. A chaos command that reaches either is an incident, not an experiment.

- **Every Bash block that may run `kubectl`, `helm` or a chaos-mesh CLI starts with this line**, before anything else in the block:
  ```bash
  export KUBECONFIG="$CHAOS_KUBECONFIG"; [ -n "$CHAOS_KUBECONFIG" ] && [ -s "$CHAOS_KUBECONFIG" ] && [ "$(cd "$(dirname "$CHAOS_KUBECONFIG")" && pwd)/$(basename "$CHAOS_KUBECONFIG")" != "$HOME/.kube/config" ] && [ "$(kubectl config current-context)" = "$CHAOS_CONTEXT" ] || { echo "HALT: CHAOS_KUBECONFIG/CHAOS_CONTEXT unset, empty, the default file, or naming a context the user did not give"; exit 1; }
  ```
  `CHAOS_KUBECONFIG` is a kubeconfig file and `CHAOS_CONTEXT` a context name, **both given by the user in this session** (a throwaway kind cluster's kubeconfig in a scratch folder qualifies). `kubectl config current-context` only reads that file.
- **Halt** — run nothing on a cluster — when `CHAOS_KUBECONFIG` is unset or empty, when it is `~/.kube/config`, when its current context is not the `CHAOS_CONTEXT` the user named, or when the user named no context at all. Say which, and print the commands that would have run.
- **Never** rely on the default context, pass `--context` to switch into one the user did not name, or loop over binaries with `version` (some cluster tools contact the current context on any invocation).
- **Docker.** `docker`, `pumba` and Testcontainers act on the current Docker endpoint. Run `docker context show` first and halt unless it is the local engine (`default`, `desktop-linux`, `colima` or `orbstack`) with `DOCKER_HOST` unset.
- **Cloud.** No default cloud profile and no real credentials: a cloud-side experiment (Gremlin, AWS FIS) runs only against an account and profile the user names, and is out of scope otherwise.
- Starting a VM or Docker engine (colima, Docker Desktop) is a side effect: say so in the report, and stop what this run started.

## Halt conditions

- Refuse to declare "resilient" without baseline + during-chaos + recovery numbers captured.
- Refuse to run chaos in prod without explicit window + customer comms confirmed.
- Halt on every § Target safety condition: no named kubeconfig and context for a cluster step, a non-local Docker endpoint, an unnamed cloud account.
- Halt if synthetic load is < 10% of prod RPS — failure modes won't surface.
- Don't claim a fix works without re-running the same experiment after the patch.
- Always verify cleanup of chaos rules (`toxiproxy-cli list`; on a named cluster, `kubectl get networkchaos` behind the § Target safety line) after each run.

## When to use

- After adding a new external dependency (cache, queue, third-party API).
- Before promoting a service to a higher SLO tier.
- Before a high-traffic event (sale, campaign, launch).
- After incidents to verify the fix actually closes the failure mode.

## Prerequisites

- **Default:** the service running locally against its real dependencies in containers — Testcontainers in the project's test stack, or `docker run` / compose — with Toxiproxy (`ghcr.io/shopify/toxiproxy`, v2.12.0 on 2025-03-18) in front of each dependency, plus a traffic generator. Testcontainers ships a Toxiproxy module for the major languages; read its package name in the registry before installing it.
- **Optional, only when the user names the target:** a staging environment with realistic data, or a cluster reached through the § Target safety kubeconfig.
- One of these chaos tools installed:
  - `toxiproxy` (`brew install toxiproxy` — homebrew-core; the old `shopify/shopify` tap path is retired) — TCP-layer faults. The local default.
  - `pumba` — Docker-container chaos (kill, pause, netem) on the local engine.
  - `chaos-mesh` — Kubernetes-native chaos (network partitions, pod kills), on a named kubeconfig only.
  - `gremlin` — SaaS chaos with prod-grade safety, on a named account only.
- Observability: metrics dashboard (Grafana/Datadog) + structured logs to confirm hypotheses.
- Approved blast-radius limits + a "stop button" (revoke the chaos rule).

## Procedure (one experiment at a time)

1. Pick **one** hypothesis: "If Redis is unavailable for 60s, the app serves cached data from DB and error rate stays < 1%."
2. Define success criteria — concrete numbers: error rate < 1%, p99 < 2x baseline, no page errors visible to user.
3. Stand up the local target (skip when the user named a staging or cluster target), and point the service at the proxy port instead of the dependency:
   ```bash
   docker context show   # halt unless local (§ Target safety)
   docker network create chaos-net
   docker run -d --name chaos-redis --network chaos-net redis:7-alpine
   docker run -d --name chaos-toxiproxy --network chaos-net -p 8474:8474 -p 26379:26379 ghcr.io/shopify/toxiproxy:2.12.0
   toxiproxy-cli create -l 0.0.0.0:26379 -u chaos-redis:6379 redis
   ```
4. Capture baseline (5 minutes of synthetic load with no chaos):
   ```bash
   k6 run --duration 5m --vus 50 load.js | tee baseline.txt
   ```
5. Inject the failure with a precise scope:
   ```bash
   # toxiproxy (local default): cut Redis for 60s
   toxiproxy-cli toxic add redis -t timeout -a timeout=0 --downstream
   sleep 60
   toxiproxy-cli toxic remove redis -n timeout_downstream

   # pumba (local engine only): kill one container at random
   pumba kill --signal SIGKILL re2:^api-
   ```
   On a cluster the user named, chaos-mesh runs in its own block, which starts with the § Target safety line:
   ```bash
   export KUBECONFIG="$CHAOS_KUBECONFIG"; [ -n "$CHAOS_KUBECONFIG" ] && [ -s "$CHAOS_KUBECONFIG" ] && [ "$(cd "$(dirname "$CHAOS_KUBECONFIG")" && pwd)/$(basename "$CHAOS_KUBECONFIG")" != "$HOME/.kube/config" ] && [ "$(kubectl config current-context)" = "$CHAOS_CONTEXT" ] || { echo "HALT: CHAOS_KUBECONFIG/CHAOS_CONTEXT unset, empty, the default file, or naming a context the user did not give"; exit 1; }
   kubectl apply -f experiments/redis-partition.yaml
   ```
6. Run the same load profile during the experiment.
7. Compare metrics during the window: error rate, p50/p95/p99, retry counts, queue depths, DB pool usage, log-level mix.
8. Record the verdict — hypothesis HOLDS or FAILED — and either close out or file a fix.
9. Clean up: `toxiproxy-cli list` shows no toxics; `docker rm -f chaos-toxiproxy chaos-redis && docker network rm chaos-net` for what step 3 started; on a named cluster, `kubectl get networkchaos` (behind the § Target safety line) shows none.
10. Re-run after the fix to confirm.

## Experiment catalogue

**Network**
- 500ms added latency on DB calls → does p95 stay within SLO?
- 5% packet loss on external API → do retries kick in, or does it hang?
- Full disconnect for 60s → does circuit breaker open + recover?

**Dependencies**
- Kill Redis → cache fallback works? error rate stays low?
- Kill one DB replica → traffic fails over without read errors?
- Exhaust DB connection pool → graceful 503 or hard crash?

**Process**
- Random pod kill → in-flight requests drain or drop?
- OOM kill → auto-restart works + alerts fire?
- Deploy during load → zero-downtime verified?

## Output

```
Experiment: Redis outage for 60s (toxiproxy timeout)
Target: local (docker context default; chaos-redis behind chaos-toxiproxy:26379)
Hypothesis: error rate < 1%, p99 < 2x baseline (200ms), zero user-visible errors.

Baseline (5m, 50 VUs):     error 0.02%   p50 38ms   p95 88ms   p99 121ms
During chaos (60s):        error 18%     p50 410ms  p95 1.8s   p99 4.2s    FAILED
After recovery (5m):       error 0.04%   p50 41ms   p95 92ms   p99 130ms

Root cause:
  Fallback path calls DB without timeout; pool exhausted under retry storm.

Action items:
  1. Add 200ms timeout on the DB fallback path (<modules-root>/cache/fallback.<ext>).
  2. Cap concurrent DB calls during the cache outage with a bulkhead.
  3. Re-run experiment after fix — must show error rate < 1%.
```

## False positives / gotchas

- Synthetic load that doesn't match prod traffic shape gives misleading results — record and replay real traces if possible.
- Chaos in dev with `--vus 5` tests almost nothing — failure modes appear under contention.
- Chaos tools often leak rules if killed mid-run — always verify cleanup with `toxiproxy-cli list`, and on a named cluster `kubectl get networkchaos` behind the § Target safety line.
- A kubectl line that "only reads" (`get`, `describe`) still reaches whatever context is current: it takes the § Target safety line like any other.
- Never run destructive chaos on prod without an explicit window + customer comms — even "safe" experiments have surprised teams.
- A single passing run isn't proof — re-run weekly. Drift in dependencies turns a green experiment red.
