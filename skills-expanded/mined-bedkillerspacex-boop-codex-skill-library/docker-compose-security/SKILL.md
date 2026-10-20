---
name: docker-compose-security
description: >
  Review and harden docker-compose files for privileged mode, host port publishing, secrets,
  volume mounts, networks, and capability grants. Use when docker-compose.yml security,
  privileged containers, docker.sock mounts, Compose secrets, host network mode, or
  authorized Compose misconfig review.
---

# Docker Compose Security

## Scope And Authorization

- **In scope:** Compose stacks you own (dev, lab, prod-like).
- **Out of scope:** Weakening isolation on shared infrastructure you do not administer; mounting host docker.sock without risk acceptance.
- Prefer secrets via Compose secrets/tmpfs over env files in git.
- Redact compose files that embed tokens before sharing.
- Pair with `dockerfile-best-practices`, `docker-rootless-mode`, `secrets-management-hygiene`, and `code-quality-standards`.

## When To Use

- Reviewing `docker-compose.yml` / `compose.yaml` before production-like deploy.
- Findings: privileged, `docker.sock`, host network, sensitive host path mounts.
- Moving from bind-mounted secrets to Docker secrets / external secret stores.
- Hardening developer compose so it is not a root backdoor to the laptop.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Dockerfile authoring | `dockerfile-best-practices` |
| Multi-stage builds | `docker-multi-stage-builds` |
| Distroless runtime | `distroless-image-adoption` |
| Rootless engine | `docker-rootless-mode` |
| K8s PodSecurity | Kubernetes security skills |
| Code quality baseline | `code-quality-standards` |

## High-risk Compose patterns

| Pattern | Risk |
| --- | --- |
| `privileged: true` | Near-host root |
| `/var/run/docker.sock` mount | Full Docker control = host |
| `network_mode: host` | Host network namespace |
| `pid: host` / `ipc: host` | Namespace escape aid |
| `volumes: /:/host` | Host FS read/write |
| `cap_add: SYS_ADMIN` | Dangerous capabilities |
| Published `0.0.0.0:5432` | DB on all interfaces |
| Secrets in environment + git | Credential leak |

## Workflow

### 1. Confirm scope and success criteria

1. Compose files (override files included), environments, who can `docker compose up`.
2. Success: no unjustified privileged/sock mounts; secrets not in git; ports bound intentionally; least capabilities; networks segmented.
3. Dev-only exceptions documented with expiry.

### 2. Inventory compose files

```bash
find . -name 'compose*.yml' -o -name 'docker-compose*.yml' -o -name 'compose.yaml'
rg -n "privileged:|docker.sock|network_mode:|cap_add:|pid:|ipc:|volumes:|secrets:" -g '*compose*'
```

1. Merge mental model of `compose.override.yml` and profiles.
2. List images and whether they run as root.

### 3. Reduce privilege

```yaml
# Prefer
services:
  api:
    image: ghcr.io/org/api:1.2.3
    user: "65532:65532"
    read_only: true
    tmpfs: ["/tmp"]
    cap_drop: ["ALL"]
    security_opt:
      - no-new-privileges:true
    # no privileged, no sock
```

1. Replace privileged with specific `cap_add` only if required; justify each.
2. Remove docker.sock; use DinD carefully in CI only with isolation, not on prod app containers.

### 4. Networks and ports

```yaml
services:
  db:
    ports:
      - "127.0.0.1:5432:5432"  # not 0.0.0.0 for local-only
    networks: [backend]
  api:
    networks: [frontend, backend]
networks:
  frontend:
  backend:
    internal: true  # when no egress needed
```

1. Avoid host network unless device access requires and is ticketed.
2. Do not publish admin UIs publicly by default.

### 5. Secrets and env

```yaml
secrets:
  db_password:
    file: ./secrets/db_password.txt  # gitignored
services:
  db:
    secrets: ["db_password"]
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
```

1. `.env` for compose interpolation: gitignore; never commit prod secrets (`direnv-dotenv-security`).
2. Prefer external secret managers in real prod (Swarm secrets/K8s)—Compose file secrets are a step up from plaintext yml.

### 6. Volumes

1. Bind mounts: least path; avoid mounting `/`, `/var/run`, host home entire.
2. Use named volumes for data; backup policy.
3. Mount configs read-only (`:ro`).

### 7. Verify and hand off

```bash
docker compose config  # render final
# Manual review checklist against high-risk table
docker compose up -d
docker compose ps
```

1. Scan images; pin digests where possible.
2. Document exceptions (e.g. CI docker.sock) with owners.
3. Apply `code-quality-standards` to any entrypoint scripts.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Priv | cap_drop ALL + small adds | privileged true |
| Sock | Not mounted in apps | App container + docker.sock |
| Ports | 127.0.0.1 or internal net | 0.0.0.0:6379 open |
| Secrets | secrets/tmpfs/manager | Password in compose committed |
| FS | read_only + tmpfs | RW root FS always |
| Image | Pinned digest/tag policy | latest everywhere |

## Output Checklist

- [ ] All compose/override files reviewed
- [ ] Privileged/sock/host ns justified or removed
- [ ] Capabilities minimized
- [ ] Ports and networks least exposure
- [ ] Secrets not in git; loading path secure
- [ ] Volumes least privilege / ro where possible
- [ ] Non-root user where image allows
- [ ] `docker compose config` validated
- [ ] Exceptions ticketed with expiry
- [ ] Residual risk documented

## Rules

- Compose convenience must not equal host root by default.
- Treat docker.sock as superuser.
- Pin images and drop caps.
- Owned stacks only.
- Focus on compose security posture, not general K8s.
