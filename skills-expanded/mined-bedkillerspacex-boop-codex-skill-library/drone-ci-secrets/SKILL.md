---
name: drone-ci-secrets
description: >
  Manage secrets in Drone CI: repository/org secrets, secret plugins (Vault, Kubernetes),
  pull-request exposure policies, masking, image pull credentials, and least privilege for
  pipelines on owned Drone servers. Use when Drone secrets, drone vault, from_secret,
  DRONE_ secrets, or preventing secret leak on forked PRs — not for stealing CI credentials.
---

# Drone CI Secrets

## Scope And Authorization

- **In scope:** Drone instances, repos, and secret backends you administer.
- **Out of scope:** Extracting secrets from customers’ Drone; weakening PR isolation on shared infra without approval.
- Prefer external secret managers (Vault) over long-lived raw secrets in Drone UI when scale requires.
- Redact secret values in pipeline logs and tickets.
- Pair with `secrets-management-hygiene`, `dependency-pinning-strategies` for images, and `code-quality-standards`.

## When To Use

- Configuring Drone repository or organization secrets.
- Integrating Vault/Kubernetes secret extensions.
- Ensuring pull requests from forks cannot read production secrets.
- Rotating registry and cloud credentials used in pipelines.
- Auditing `.drone.yml` for secret misuse (`echo`, debug).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Org-wide secret platform design | `secrets-management-hygiene` |
| GitHub Actions secrets | GHA-specific skills |
| Docker Hub rate limits | `docker-hub-rate-limit-ci` |
| General SSDLC | `secure-sdlc-checklist` |
| Code quality baseline | `code-quality-standards` |

## Concepts

| Concept | Role |
| --- | --- |
| Repository secrets | Scoped to one repo |
| Organization secrets | Shared; careful grants |
| `from_secret` | Reference in pipeline YAML |
| Pull request events | Often should not get prod secrets |
| Secret plugins | External fetch at runtime |
| Runner trust | Runners see decrypted secrets—harden runners |

## Workflow

### 1. Confirm scope and success criteria

1. Drone version, runners (K8s/VM), repos, environments (prod vs PR).
2. Success: prod secrets unavailable to untrusted events; least privilege; rotation works; no plaintext in git.
3. Owners for each secret.

### 2. Inventory secrets and pipelines

```bash
rg -n "from_secret|secrets:|environment:" -g '.drone.yml' -g '*.drone.yml'
# CLI if available (owned server)
# drone secret ls --repository org/name
```

1. Classify: build-only vs deploy-prod.
2. Find long-lived cloud keys candidates for OIDC/short-lived.

### 3. Configure secrets safely

```yaml
# .drone.yml sketch
kind: pipeline
type: docker
name: default
steps:
  - name: build
    image: golang:1.22
    environment:
      GOPROXY:
        from_secret: goproxy_url
    commands:
      - go test ./...
  - name: deploy
    image: plugins/kubectl
    environment:
      KUBE_TOKEN:
        from_secret: kube_token_prod
    commands:
      - # deploy
    when:
      branch:
        - main
      event:
        - push
```

1. **Never** put secret values in YAML.
2. Restrict deploy steps with `when` on trusted events/branches.
3. Disable secret exposure on `pull_request` for production credentials (Drone settings / policy).

### 4. PR and fork policy

| Event | Secret policy |
| --- | --- |
| push to main | Deploy secrets OK if gated |
| PR same-repo | Limited secrets; prefer none for prod |
| PR fork | **No** prod secrets; untrusted code |

1. Document that untrusted PR pipelines can still exfil if secrets present—treat as hostile.
2. Use read-only tokens for PR CI when must build private modules.

### 5. External secret sources

1. Vault plugin: short-lived credentials; auth via AppRole/K8s auth carefully.
2. Avoid echoing vault responses.
3. K8s runners: use K8s secrets carefully; RBAC least privilege for runner SA.

### 6. Logging and image hygiene

1. Masking is not perfect—do not `env`/`printenv` in steps.
2. Pin pipeline images by digest (`docker-hub-rate-limit-ci` / pinning).
3. Pull secrets for private registries as dedicated pull creds, not personal PATs.

### 7. Rotate, audit, hand off

```bash
# Rotation checklist
# 1 create new secret value in store
# 2 update Drone secret
# 3 run pipeline
# 4 revoke old credential
```

1. Audit who can edit org secrets (Drone admins).
2. Alerts on pipeline failures after rotation.
3. Apply `code-quality-standards` to any custom plugins.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Storage | Drone secret / Vault | Token in `.drone.yml` |
| PRs | No prod secrets on forks | Same secrets all events |
| Scope | Per-env secrets | One god token |
| Logs | No printenv | Debug dump env |
| Images | Pinned | `:latest` with secret steps |
| Rotation | Scheduled | Eternal PATs |

## Output Checklist

- [ ] Secrets inventoried and classified
- [ ] YAML uses `from_secret` only
- [ ] PR/fork event policy blocks prod secrets
- [ ] Deploy steps gated on trusted events
- [ ] External vault/plugin configured if needed
- [ ] Runners hardened; admin list short
- [ ] No secret echo patterns in pipelines
- [ ] Rotation procedure tested
- [ ] Registry pull creds least privilege
- [ ] Residual risk documented

## Rules

- Untrusted pipelines must not receive production secrets.
- Runners are part of the secret trust boundary.
- Prefer short-lived credentials over eternal PATs.
- Owned Drone only; never exfiltrate secrets.
- Focus on Drone secret operations and PR isolation.
