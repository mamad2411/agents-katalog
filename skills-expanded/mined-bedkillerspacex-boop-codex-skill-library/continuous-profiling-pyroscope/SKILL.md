---
name: continuous-profiling-pyroscope
description: >
  Operate continuous profiling with Grafana Pyroscope (or Grafana Cloud Profiles):
  agents/SDKs, profile types (CPU, alloc, goroutine, lock), labeling, sampling cost,
  storage retention, and using profiles to fix production hotspots. Use on owned
  services for performance engineering — not for profiling third-party systems without
  authorization; pair with observability-metrics-tracing.
---

# Continuous Profiling (Pyroscope)

## Scope And Authorization

- **In scope:** applications and infrastructure you operate.
- **Out of scope:** attaching profilers to systems without ownership/authorization; shipping profiles that leak PII/secrets in labels.
- Start with low sample rates in prod; watch CPU overhead.
- Pair with metrics/traces (`observability-metrics-tracing`) and `code-quality-standards` for fixes.

## When To Use

- Continuous **CPU/memory/lock** profiles in staging/prod.
- Investigating regressions after deploy; comparing profile diffs.
- Tokens: Pyroscope, continuous profiling, pprof, eBPF, wall vs CPU, profile labels.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Metrics/traces core | `observability-metrics-tracing` |
| Load testing only | k6/load skill |
| APM vendor-specific non-Pyroscope | that vendor’s runbook |
| Security vuln scanning | SAST/DAST skills |

## Profile Types (common)

| Type | Answers |
| --- | --- |
| CPU | Where CPU time goes |
| Alloc / heap | Allocation hotspots, leak clues |
| Goroutine / thread | Concurrency storms |
| Lock / mutex | Contention |
| Wall (where supported) | Time including block/IO |

## Workflow

### 1. Confirm goals and success

1. Services, languages, latency/CPU SLOs, retention, who can view profiles (may include code paths).
2. Success: profiles flow continuously; overhead within budget; at least one regression diagnosed via profile diff.
3. Access control on Pyroscope UI (SSO).

### 2. Choose collection mode

| Mode | When |
| --- | --- |
| Language SDK / pprof pull | Go net/http/pprof, Java async-profiler integrations |
| Grafana Alloy / agent | Central scrape or push |
| eBPF (where supported) | Low-touch multi-language nodes — validate privileges |

```bash
# Go example: expose pprof (bind localhost or protect network!)
# then scrape with Alloy/Pyroscope config
curl -s http://127.0.0.1:6060/debug/pprof/profile?seconds=5 -o cpu.pprof
```

Never expose unauthenticated pprof on the public Internet.

### 3. Deploy Pyroscope backend

1. Self-host Pyroscope or use Grafana Cloud Profiles.
2. Configure retention, multi-tenancy, object storage if required.
3. Authn/z on query path; network policies for write path.

### 4. Labeling discipline

| Label | Guidance |
| --- | --- |
| `service_name` | Required stable ID |
| `namespace` / `pod` | K8s context |
| `version` / `git_sha` | Diff deploys |
| User IDs | **Avoid** high-cardinality PII |

### 5. Investigate with profiles

1. Baseline profile for healthy period.
2. Compare after deploy or during incident (diff view).
3. Map top frames to code; confirm with trace/metrics correlation.
4. Ship fix; verify profile cost drops.

### 6. Cost and safety controls

1. Sample rate / collection interval trade-off.
2. Disable heavy profiles (e.g. frequent heap) if overhead high.
3. Secure pprof endpoints (mTLS, localhost, network policy).
4. Redact path labels that include tokens/query secrets.

### 7. Hand off

1. Runbook: “CPU pegged” → open Pyroscope → filter service/version → top functions.
2. Dashboard links from Grafana to profiles.
3. On-call training with one known regression example.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Exposure | Auth’d profiles UI; locked pprof | Public `:6060/debug/pprof` |
| Labels | service+version | user_id on every sample |
| Use | Diff before/after deploy | Only local once-a-year pprof |
| Overhead | Measured budget | Max sampling everywhere |
| Privacy | No secrets in stacks/labels | Profile raw request URLs with tokens |

## Output Checklist

- [ ] Services and profile types selected
- [ ] Collection mode deployed securely
- [ ] Backend retention/auth configured
- [ ] Labels low-cardinality and useful
- [ ] Overhead measured acceptable
- [ ] Investigation runbook + Grafana links
- [ ] pprof not Internet-exposed
- [ ] Residual privacy risks noted

## Rules

- Owned systems only.
- Treat profiles as sensitive production data.
- Prefer continuous low-overhead over rare heavy dumps alone.
- Focus on **Pyroscope continuous profiling**; general OTel metrics/traces are companion skills.
