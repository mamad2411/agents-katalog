---
name: docker-rootless-mode
description: >
  Install, operate, and harden Docker Engine in rootless mode: user namespaces,
  dockerd-rootless-setuptool, systemd user units, slirp4netns/pasta networking, storage
  drivers, and known limitations vs rootful Docker. Use when setting up rootless Docker,
  troubleshooting non-root dockerd, comparing rootless security boundaries, fixing rootless
  port/network/storage issues, or reducing host impact of a compromised container runtime on
  owned developer or lab hosts.
---

# Docker Rootless Mode

## Scope And Authorization

- **In scope:** Developer workstations and lab hosts you administer; optional rootless in controlled servers.
- **Out of scope:** Forcing rootless on multi-tenant prod without testing networking/storage limits; privilege escalation research beyond owned hosts.
- Rootless reduces—not eliminates—risk from container breakout.
- Redact host usernames/paths in shared docs if sensitive.
- Pair with `docker-compose-security`, `dockerfile-best-practices`, and `code-quality-standards`.

## When To Use

- Developers need Docker without rootful daemon.
- Policy: no long-running root dockerd on laptops.
- Isolating untrusted builds slightly better under user namespaces.
- Troubleshooting rootless networking (ports <1024, performance).
- Comparing rootless vs Podman rootless for DevEx.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Compose hardening | `docker-compose-security` |
| Distroless images | `distroless-image-adoption` |
| K8s node runtime | CRI-O/containerd node skills |
| Dockerfile authoring | `dockerfile-best-practices` |
| Code quality baseline | `code-quality-standards` |

## Security model

| Aspect | Rootless behavior |
| --- | --- |
| dockerd UID | Runs as user; uses user namespaces |
| Host root | Compromised container ≠ automatic host root (better than rootful) |
| Kernel exploits | Still dangerous |
| Privileged containers | Restricted/limited |
| Networking | slirp4netns/pasta user-mode; different performance |
| cgroup | Depends on cgroup v2 delegation |

## Workflow

### 1. Confirm scope and success criteria

1. Distro, cgroup v2, systemd user lingering needs.
2. Success: `docker info` shows rootless; `docker run hello-world` works; compose stacks for dev work; known limitations documented.
3. Decide if VPN/corporate network affects slirp.

### 2. Prerequisites

```bash
# uidmap, dbus user session, cgroup v2 often required
cat /proc/self/uid_map
# sysctl may need:
# kernel.unprivileged_userns_clone=1  (distro-dependent)
# Enable lingering for user services
loginctl enable-linger "$USER"
```

1. Install Docker packages per official rootless docs for your OS version.
2. Ensure `/etc/subuid` and `/etc/subgid` have ranges for the user.

### 3. Install rootless dockerd

```bash
dockerd-rootless-setuptool.sh install
# export PATH and DOCKER_HOST as instructed, e.g.:
export PATH="$HOME/bin:$PATH"
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock
docker info | grep -i rootless
```

1. systemd user unit: `systemctl --user enable --now docker`
2. Persist env in shell rc carefully for the user only.

### 4. Networking and ports

| Topic | Guidance |
| --- | --- |
| Ports < 1024 | Often cannot bind without config; use high ports |
| Performance | slirp slower than kernel bridge; pasta may improve |
| Expose to LAN | Explicit; understand rootless IP visibility |
| Compose | Works with DOCKER_HOST set |

```bash
docker run --rm -p 8080:80 nginx:alpine
curl -sS -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8080
```

### 5. Storage and features

1. Overlay storage in user home; disk growth under `~/.local/share/docker`.
2. Some options unsupported: certain privileged modes, SELinux interactions, GPU—verify matrix.
3. Rootless cannot use some rootful-only kernel features—document for developers.

### 6. Hardening tips

1. Still avoid docker.sock mounts into untrusted containers.
2. Do not run rootless daemon world-accessible socket permissions.
3. Keep engine updated; user namespaces are security-boundary sensitive.
4. Separate untrusted builds from personal docker data when possible.

### 7. Troubleshoot, verify, hand off

| Issue | Check |
| --- | --- |
| Cannot start | subuid/subgid, userns sysctl, lingering |
| Permission denied socket | DOCKER_HOST, XDG_RUNTIME_DIR |
| Slow network | pasta/slirp config |
| Disk full | prune under user data dir |

```bash
docker info
docker context ls
systemctl --user status docker
```

1. README for developers: install steps + limitations vs rootful CI.
2. Apply org security baseline on the host OS too.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Install | Official setuptool + subuid | Random curl\|root scripts |
| Env | User systemd + DOCKER_HOST | Mixed rootful/rootless confusion |
| Expectation | Reduced host impact | “Unbreakable containers” |
| Ports | 8080+ | Assume :80 bind works |
| Sock | Private to user | chmod 777 docker.sock |
| Disk | Monitor user docker dir | Ignore home fill |

## Output Checklist

- [ ] Prerequisites (userns, subuid, cgroup) met
- [ ] Rootless dockerd installed and enabled
- [ ] `docker info` shows rootless
- [ ] Sample container networking verified
- [ ] Limitations documented for team
- [ ] Disk path and prune policy known
- [ ] Socket permissions restricted
- [ ] Host OS still patched
- [ ] Dev onboarding notes updated
- [ ] Residual risks accepted

## Rules

- Rootless is defense-in-depth, not a full security boundary against kernel bugs.
- Do not expose user docker.sock broadly.
- Test required workloads before mandating rootless fleet-wide.
- Owned hosts only.
- Focus on rootless engine ops vs image authoring neighbors.
