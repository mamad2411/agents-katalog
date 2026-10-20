---
name: capabilities-drop-all
description: >
  Linux capability hardening for owned containers/hosts: drop all capabilities, add back
  only required ones, no-new-privileges, seccomp/AppArmor notes, and verification. Use
  when Docker/K8s securityContext capabilities drop ALL, CAP_NET_BIND_SERVICE only,
  or least-privilege container hardening — not for escaping others' containers.
---

# Capabilities Drop All

## Scope And Authorization

- **In scope:** Linux hosts and container platforms you operate.
- **Out of scope:** Capability abuse for unauthorized privilege escalation on systems you do not own.
- Test in staging — dropping caps can break binding ports, tracing, or filesystem ops.
- Pair with container image hardening and `code-quality-standards` for deploy manifests.

## When To Use

- Hardening Docker/Podman/Kubernetes workloads to least privilege.
- CIS/K8s baseline: `drop: ["ALL"]` then selective `add`.
- Replacing privileged pods with fine-grained capabilities.
- Verifying a process actually lacks dangerous caps (`CAP_SYS_ADMIN`, raw, etc.).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full K8s PSS / Pod Security | kubernetes security skills |
| Seccomp profile authoring deep dive | seccomp skills if present |
| NetworkPolicy microseg | network policy skills |
| Host Linux privilege escalation lab | `linux-privilege-escalation` (lab only) |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Notes |
| --- | --- |
| Capabilities | Split root into units (`CAP_NET_BIND_SERVICE`, …) |
| Bounding set | Caps that can ever be gained |
| Effective/Permitted/Inheritable | Runtime process sets |
| `drop: ALL` | Start from zero in container specs |
| `no_new_privs` | Blocks privilege gain via setuid |
| Privileged | Essentially disables isolation — avoid |

## Workflow

### 1. Confirm scope and success criteria

1. Workload list, required kernel features (ptrace, net admin, bind <1024).
2. Success: workloads run with `drop ALL`; minimal adds; no privileged; verified via status files.
3. Rollback plan if production breaks on cap absence.

### 2. Inventory current privileges

```bash
# On node/host process
grep Cap /proc/1/status
capsh --decode=$(grep CapEff /proc/1/status | awk '{print $2}')
# Docker
docker inspect "$CID" --format '{{json .HostConfig.CapAdd}} {{json .HostConfig.CapDrop}} {{.HostConfig.Privileged}}'
# K8s
kubectl get pod "$POD" -o jsonpath='{.spec.containers[*].securityContext}'
```

1. Flag `privileged: true`, `CAP_SYS_ADMIN`, hostPath mounts, `allowPrivilegeEscalation: true`.
2. Note entrypoint user (non-root preferred).

### 3. Baseline functional tests

1. Record smoke tests before dropping caps.
2. Identify if app binds :80/:443 as non-root (needs `NET_BIND_SERVICE` or reconfigure >1024 + port map).

### 4. Apply drop-all patterns

**Docker Compose / run:**

```bash
docker run --rm \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  --security-opt=no-new-privileges:true \
  -u 10001:10001 \
  myimg:prod
```

**Kubernetes:**

```yaml
apiVersion: v1
kind: Pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 10001
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: app
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop: ["ALL"]
          add: ["NET_BIND_SERVICE"]  # only if required
        readOnlyRootFilesystem: true
```

**Common required adds (use sparingly):**

| Capability | Sometimes needed for |
| --- | --- |
| `NET_BIND_SERVICE` | Bind low ports |
| `NET_RAW` | Ping/some discovery (prefer remove) |
| `CHOWN` / `DAC_*` | Rare entrypoint fixups (prefer fix image) |
| `SYS_PTRACE` | Debug sidecars only in non-prod |
| `SYS_ADMIN` | Almost always wrong for apps |

1. Prefer listening on 8080 and host/LB map to 80 over adding caps.
2. Init containers that need caps should not force app container caps.
3. Combine with read-only root FS and seccomp RuntimeDefault.

### 5. Verify

```bash
# Inside container
cat /proc/self/status | rg Cap
capsh --print
# Expect minimal effective set
# Negative: cannot load net modules / mount etc.
```

1. App smoke tests pass.
2. Admission: Kyverno/OPA policy requiring drop ALL (optional org control).
3. Runtime scanner (Trivy K8s, kube-bench) findings reduced.

### 6. Break/fix loop

| Symptom | Direction |
| --- | --- |
| Permission denied bind | High port or add `NET_BIND_SERVICE` only |
| Cannot chown at start | Fix image perms at build; don’t add `CHOWN` lightly |
| Healthcheck needs ping | TCP healthcheck instead of `NET_RAW` |
| eBPF/observability agent | Separate DaemonSet with explicit caps, not app pod |

### 7. Hand off

1. Document required capabilities per service in README/Helm values.
2. Policy as code: deny privileged + require drop ALL.
3. Apply `code-quality-standards` to manifests/Helm.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Default | drop ALL | Drop nothing |
| Add | One justified cap | `add: [SYS_ADMIN]` habit |
| User | non-root + no-new-privs | root + privileged |
| Ports | 8080 + Service | Must bind 80 inside as root |
| Policy | Admission enforce | Manual hope |
| Debug | Temporary profiled pod | Permanent ptrace on prod app |

## Output Checklist

- [ ] Workloads inventoried for privileged/caps
- [ ] Functional baseline captured
- [ ] `drop: ALL` applied with minimal adds
- [ ] `allowPrivilegeEscalation: false` / no-new-privileges set
- [ ] Non-root user configured where possible
- [ ] `/proc/self/status` verification recorded
- [ ] Smoke tests green
- [ ] Exceptions documented with owner
- [ ] Admission policy considered
- [ ] `code-quality-standards` on IaC

## Rules

- Start from zero capabilities; add only with justification and owner.
- Privileged mode is not an acceptable substitute for debugging in prod.
- Prefer app config changes over powerful caps.
- Authorized environments only.
- Broader pod security baselines live in K8s security skills.
