---
name: fly-io-machines-secrets
description: >
  Manage Fly.io Machines and secrets securely: fly secrets set/import, runtime env
  injection, Machines API identity, volume and network exposure, and rotation. Use when
  operating owned Fly apps/Machines, reviewing secret sprawl, or hardening production
  Fly deployments—not for accessing other orgs’ Fly accounts.
---

# Fly.io Machines Secrets

## Scope And Authorization

- **In scope:** Fly.io orgs/apps you own or administer with clear authorization.
- **Out of scope:** other tenants’ apps, stealing tokens, or unauthorized account access.
- Prefer staging apps for experiments; production secret changes need change control.
- Redact `FLY_API_TOKEN` and secret values from tickets and CI logs.
- Pair automation with `code-quality-standards` and `secrets-management-hygiene`.

## When To Use

- Setting or rotating **`fly secrets`** for Apps/Machines.
- Deploying **Machines** with env from secrets, not baked images.
- Reviewing who can read deploy tokens and Machines API.
- Distinguishing app-wide secrets vs per-machine config.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Org-wide secrets program | `secrets-management-hygiene` |
| General container security | container skills in catalog |
| CI OIDC patterns broadly | secrets/CI skills in catalog |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Notes |
| --- | --- |
| `fly secrets` | Stored by Fly; injected as env at runtime for VMs/Machines |
| Machines | Fine-grained VMs; scale-to-zero patterns; API-driven |
| Images | Should not contain secrets; pull private images with care |
| Tokens | `fly auth token` / deploy tokens—treat as prod credentials |
| Networking | Public services, WireGuard org network, `.internal` DNS |

## Workflow

### 1. Confirm scope and success criteria

1. Org, apps, regions, Machines vs classic scale model, data sensitivity.
2. Success: no secrets in git/images; least-privilege tokens; rotation works without downtime plan; Machines only expose intended ports.
3. Owners for deploy tokens and secret keys listed.

### 2. Inventory

```bash
fly version
fly apps list
fly machines list -a YOUR_APP
fly secrets list -a YOUR_APP   # names only; values not shown
```

1. Search repos for `FLY_API_TOKEN`, hardcoded DB URLs, `.env` committed.
2. CI: where tokens live (GitHub secrets, etc.).

### 3. Baseline risks

1. Secrets in Dockerfile `ENV` or baked config files.
2. Over-scoped org tokens in every pipeline.
3. Machines with public IPv6/services unintended.
4. Debug dashboards exposing env.

### 4. Apply secure secret and machine practices

```bash
# Set secrets (values via stdin/prompt preferred in interactive; CI via env)
fly secrets set DATABASE_URL="..." -a YOUR_APP
# Staging separate app:
fly secrets set DATABASE_URL="..." -a YOUR_APP_STAGING

# Deploy without embedding secrets in image
fly deploy -a YOUR_APP
```

```toml
# fly.toml review: services ports, http_service, mounts
# Ensure only intended internal ports published
```

1. **Separate staging/prod apps** and secrets.
2. Use short-lived deploy tokens where possible; scope to app.
3. Rotate: `fly secrets set` new value → rolling restart → invalidate old credential at provider.
4. Machines API: authenticate carefully; do not embed tokens in client apps.
5. Volumes: encrypt/sensitivity awareness; do not store sole copy of secrets only on volume without backup policy.
6. Prefer private images + controlled deploy over shipping `.env` files via `fly ssh sftp`.

### 5. Verify with evidence

```bash
# SSH into owned machine carefully — confirm env present without printing to shared logs
fly ssh console -a YOUR_APP -C 'printenv | cut -d= -f1 | sort'
# Ensure secret NAMES exist; do not dump values into CI transcripts
```

| Check | Expect |
| --- | --- |
| Git history | No live secrets |
| Image layers | No secret strings (scan owned images) |
| Public service | Only intended ports |
| Token scope | App-limited deploy token works; org-admin not required for routine deploy |

### 6. Observe and harden

1. Audit Fly org members and 2FA.
2. Alert on deploy token creation if process allows.
3. Periodic `fly secrets list` vs required keys (remove unused).

### 7. Hand off

1. Secret key inventory + rotation cadence.
2. Machine sizing/network diagram.
3. Apply `code-quality-standards` for deploy scripts.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Injection | `fly secrets` → runtime env | Secrets in git + Dockerfile |
| Tokens | App-scoped, rotated | Personal org-admin token in CI forever |
| Apps | Prod/stage separation | One app, shared secrets |
| Debug | Controlled `fly ssh` | Open public debug port with env dump |
| Machines | Least published services | Bind all interfaces casually |
| Logs | Redact | Print `DATABASE_URL` on boot |

## Output Checklist

- [ ] Apps/Machines inventory complete
- [ ] Secret names inventoried; values not logged
- [ ] No secrets in images/git evidenced
- [ ] Token scope and rotation plan
- [ ] Network exposure reviewed
- [ ] Staging/prod separation
- [ ] Org member access reviewed
- [ ] `code-quality-standards` applied

## Rules

- Owned Fly orgs only.
- Never paste live secrets into chat/tickets.
- Runtime injection beats bake-in.
- Coordinate with org secrets hygiene for broader policy.
