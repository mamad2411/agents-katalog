---
name: falco-runtime-rules-basics
description: >
  Deploy and tune Falco runtime rules on owned hosts/Kubernetes: syscall noise,
  priorities, allowlists, exceptions, and SIEM routing. Use when Falco rules,
  falcoctl, modern engine tags, or container runtime detections—not general eBPF
  profiling (see ebpf-observability-basics).
---

# Falco Runtime Rules Basics

## Scope And Authorization

- **In scope:** Nodes/clusters you operate with approval for kernel/eBPF/driver sensors.
- **Out of scope:** Installing runtime sensors on systems without authorization.
- Falco can generate high volume—tune before paging humans.
- Auto-response (kill pod) is dangerous; prefer detect+alert until mature.
- Pair with `ebpf-observability-basics` for probe safety and `code-quality-standards` for custom rules.

## When To Use

- Deploying Falco or Falcosidekick pipelines.
- Reducing false positives from default rules.
- Writing custom rules for org-specific sensitive paths.
- Mapping priorities (WARNING/ERROR/CRITICAL) to on-call.
- Detecting shell in container, unexpected network tools, sensitive file reads.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Continuous CPU profiling | `ebpf-profiler-prod` |
| Generic eBPF observability | `ebpf-observability-basics` |
| Network IDS only | network detection skills |
| K8s admission policy | admission controller skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Rules | YAML conditions on syscall/k8s fields |
| Exceptions | Allowlist legit admin/debug paths |
| Priority | Match business severity |
| Scope | Namespace/image/user filters |
| Output | JSON to SIEM; drop noisy tags |
| Updates | Pin rules versions; review changelogs |

## Workflow

### 1. Confirm scope and success criteria

1. Cluster/host list, driver (modern eBPF), on-call owners.
2. Success: high-signal alerts for agreed scenarios; FP rate acceptable; no silent drop of critical rules.

### 2. Inventory installation

```bash
kubectl -n falco get ds,deploy,cm
falco --version 2>/dev/null || true
# Rules config maps / falcoctl artifacts
```

1. List enabled rules files and custom overlays.
2. Confirm output channel (stdout, sidekick, OTEL).

### 3. Baseline noise

1. Run 24–72h in observe mode; top rules by count.
2. Identify expected ops (helm, CI deploy, backup agents).
3. Measure CPU overhead on nodes.

### 4. Tune rules and exceptions

```yaml
# Custom exception sketch (syntax varies by rules version—validate)
- rule: Write below binary dir
  # prefer append exceptions rather than disable entire rule
  exceptions:
    - name: legit_package_manager
      comm: [apk, apt-get, yum]
```

```yaml
- rule: Detect shell in prod API pod
  desc: Shell spawned in payments namespace
  condition: >
    spawned_process and container
    and k8s.ns.name=payments
    and proc.name in (bash, sh, zsh)
    and not proc.pname in (pause)
  output: "Shell in payments (user=%user.name pod=%k8s.pod.name)"
  priority: WARNING
  tags: [custom, mitre_execution]
```

1. Disable only with ticket if rule is irrelevant; prefer exceptions.
2. Tag custom rules; keep in Git with review.
3. Never ship secrets in `output` fields.

### 5. Response model

| Priority | Response |
| --- | --- |
| INFORMATIONAL | Metrics only |
| WARNING | Ticket / slack |
| ERROR | On-call business hours |
| CRITICAL | Page + playbook |

1. Auto-mitigation only after low FP and clear blast radius.
2. Playbooks: shell in prod, crypto miner syscalls, sensitive file read.

### 6. Verify with evidence

1. Lab namespace: run `kubectl exec` shell → expect alert.
2. Confirm exception for known batch job does **not** alert.
3. SIEM contains structured fields for correlation.

```bash
# Generate controlled event in lab only
kubectl -n lab run falco-test --image=busybox --rm -it --command -- sh -c 'sleep 2'
```

### 7. Hand off

1. Rules ownership and update cadence.
2. Dashboard: alerts/min, top rules, node CPU.
3. Quarterly attack simulation for critical detections.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Tuning | Exceptions + tags | Disable all noisy rules |
| Response | Priority-routed | Page on every default rule |
| Custom | Git-reviewed YAML | SSH edit on node |
| Scope | Sensitive ns first | Global kill-pod automation day one |
| Overhead | Measured | Ignore node CPU regressions |

## Output Checklist

- [ ] Falco deploy and rules inventory done
- [ ] Noise baseline captured
- [ ] Exceptions documented
- [ ] Custom high-value rules added
- [ ] SIEM routing verified
- [ ] Lab detection evidence recorded
- [ ] Response playbooks linked
- [ ] Residual risk noted

## Rules

- Authorized clusters/hosts only.
- Detect first; automated kill only with mature process.
- Pin and review rule pack upgrades.
- Redact sensitive command lines in shared alerts when needed.
- Profiling ≠ Falco → eBPF profiler skill.
