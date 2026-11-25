---
name: boundary-hashicorp-basics
description: >
  HashiCorp Boundary for owned privileged access: controllers/workers, auth methods,
  scopes, targets, host catalogs, credential injection (brokered/injected), session
  recording notes, and least-privilege grants. Use when deploying Boundary, replacing
  shared SSH bastions, or wiring Vault credential libraries — not for attacking others'
  Boundary clusters.
---

# Boundary HashiCorp Basics

## Scope And Authorization

- **In scope:** Boundary clusters and targets in environments you operate or are authorized to implement.
- **Out of scope:** Using Boundary credentials or discovery against systems outside ownership/RoE.
- Prefer lab/dev cluster before production break-glass cutover.
- Redact auth tokens, brokered credentials, and private host addresses in tickets.
- Pair secrets with Vault skills and `secrets-management-hygiene`; code with `code-quality-standards`.

## When To Use

- Replacing shared SSH bastion keys or VPN-wide lateral movement with per-session access.
- Introducing identity-based access to SSH, RDP, Kubernetes, or TCP targets via Boundary.
- Integrating OIDC/LDAP auth methods and Vault credential brokering/injection.
- Multi-scope org design (org → project → targets) for team isolation.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Vault policy / secrets engine deep dive | Vault-focused skills / `secrets-management-hygiene` |
| Generic PAM product comparison | org architecture docs |
| AD attack path analysis | `bloodhound-ce-basics` |
| Kubernetes RBAC alone | k8s RBAC skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Component | Role |
| --- | --- |
| Controller | API, auth, session orchestration; highly sensitive |
| Worker | Data plane proxy to targets; place near networks |
| Scope | Org/project hierarchy for multi-tenancy |
| Auth method | OIDC, password, LDAP — who can log into Boundary |
| Host catalog / set | Dynamic or static inventory of endpoints |
| Target | Address + port + credential sources + worker filter |
| Session | Time-bound connection via worker; prefer injected creds |

## Workflow

### 1. Confirm scope and success criteria

1. Record networks (prod/dev), identity provider, target types (SSH/PG/K8s), compliance (session recording?).
2. Success: users authenticate via SSO; reach only granted targets; no long-lived host passwords on laptops; audit trail for sessions.
3. Break-glass: offline emergency access documented without defeating Boundary entirely.

### 2. Deploy controllers and workers

```bash
# Version-pin Boundary; example install checks
boundary version
# Controllers need DB (Postgres), KMS for root/worker auth (cloud KMS or Transit)
# Workers need controller reachability + target network path
```

1. Separate controller plane (tight SG/NSG) from worker plane.
2. Use cloud auto-join / PKI worker auth per current HashiCorp docs for your version.
3. TLS everywhere; no public controller API without SSO + hard MFA at IdP.
4. Storage: Postgres HA; encrypt backups; restrict DB network path.

### 3. Identity and scopes

```bash
# Authenticate as initial recovery / admin (lab)
export BOUNDARY_ADDR="https://boundary.example.com:9200"
boundary authenticate password -auth-method-id ampw_... -login-name admin
# Org + project scopes
boundary scopes create -name eng -scope-id global
boundary scopes create -name prod-apps -scope-id o_...
```

1. Map IdP groups → Boundary roles/grants at least privilege.
2. Prefer OIDC; disable local passwords for humans in production when SSO is ready.
3. Example grant snippets (conceptual): allow `authorize-session` only on specific target IDs; no global `*` admin for developers.

### 4. Catalog hosts and define targets

```bash
# Static host catalog example
boundary host-catalogs create static -scope-id p_... -name "prod-ssh"
boundary hosts create static -host-catalog-id hcst_... -address "10.0.10.12"
boundary host-sets create static -host-catalog-id hcst_... -name "app-tier"
boundary host-sets add-hosts -id hsst_... -host id=hst_...

# Target
boundary targets create tcp -scope-id p_... -name "app-ssh" -default-port 22
boundary targets add-host-sources -id ttcp_... -host-source id=hsst_...
```

1. Dynamic catalogs (AWS/Azure/GCP plugins) reduce stale IPs — filter by tags.
2. Worker filters ensure sessions egress from the correct network segment.
3. Split targets per environment; never one target for all prod hosts.

### 5. Credentials: brokered vs injected

| Mode | User sees secret? | Prefer when |
| --- | --- | --- |
| Brokered | Yes (shown once) | Break-glass, limited protocols |
| Injected | No (Boundary injects) | SSH/RDP day-to-day |
| Application | App-specific | DB dynamic creds via Vault library |

```bash
# Credential store + library patterns depend on Boundary+Vault versions
# Prefer Vault SSH signed certs or dynamic secrets over static password libraries
boundary credential-stores create vault -scope-id p_... \
  -vault-address "https://vault.example.com" \
  -vault-token "$TOKEN"   # prefer better auth patterns than long-lived tokens
```

1. Short TTLs; no shared static root SSH keys.
2. Rotate Vault token/approle used by Boundary; store in controller config securely.
3. Deny clipboard exfil expectations — still treat brokered secrets as sensitive.

### 6. Client connect and verify

```bash
boundary authenticate oidc -auth-method-id amoidc_...
boundary targets list -scope-id p_...
boundary connect ssh -target-id ttcp_... -- -l deploy
# Or boundary connect with proxy env for TCP targets
boundary connect -target-id ttcp_...
```

1. Confirm user A cannot authorize-session on user B's project targets.
2. Confirm worker path: session should not hairpin through wrong region.
3. Audit: controller logs/events show user, target, worker, start/end.
4. If session recording enabled, verify storage encryption and access control.

### 7. Operate and hand off

1. Monitor controller health, DB, worker connection count, failed auth.
2. On-call: revoke role grants; cancel active sessions on offboarding.
3. Document recovery keys / initial auth storage in org secret system — not wiki plaintext.
4. Apply `code-quality-standards` to Terraform providers for Boundary resources.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Bastion replacement | Per-session injected SSH | Shared `bastion.pem` still on laptops |
| Scopes | Project per team/env | One global admin for all targets |
| Workers | Near targets, least network | Single worker with flat VPC allow-all |
| Creds | Vault dynamic / SSH CA | Static password library, 1 year TTL |
| API exposure | SSO + MFA + private | Password auth on public Internet |
| Offboarding | IdP revoke + session cancel | Wait for 12h token expiry only |

## Output Checklist

- [ ] Controllers/workers topology and KMS/DB documented
- [ ] OIDC/SSO auth method live; local admin limited
- [ ] Scopes and roles mapped to IdP groups
- [ ] Host catalogs and targets least-scoped
- [ ] Credential injection/brokering configured with short TTL
- [ ] Connect tests for allow and deny cases
- [ ] Audit/session recording storage reviewed
- [ ] Break-glass procedure written
- [ ] Offboarding runbook includes Boundary
- [ ] IaC follows `code-quality-standards`

## Rules

- Boundary is a privileged control plane — harden controllers like domain controllers.
- Prefer credential injection over long-lived secrets on admin workstations.
- Never expose controller API anonymously.
- Authorized environments only.
- Route pure Vault engine design to Vault skills; keep this on Boundary access paths.
