---
name: golang-ad-tiering
description: >
  Apply Active Directory administrative tiering with Go automation and services:
  tier-0/1/2 boundaries, PAW paths, credential hygiene, and inventory collectors.
  Use for owned AD forests and labs under authorization.
---

# Golang AD Tiering

## Research grounding

Runbook for **AD administrative tiering** (Microsoft ESAE-style tiers) where Go
tools inventory, validate, or enforce control-plane hygiene—not a substitute for
directory design expertise. Skill id: `golang-ad-tiering`.

## Scope And Authorization

- **In scope:** AD/Entra environments you own, labs, authorized assessments.
- **Out of scope:** attacking third-party directories or harvesting credentials.
- Prefer read-only LDAP/Graph first; write changes under change control.
- Redact UPNs, SIDs tied to people, and secrets from notes.
- Pair automation with `code-quality-standards`.

## When To Use

- Mapping or enforcing Tier 0 (DCs, identity systems), Tier 1 (servers), Tier 2 (workstations).
- Building Go collectors for privileged group membership, GPO links, or logon paths.
- Preventing tier violations (Tier 0 creds on Tier 2 hosts).
- Focus tokens: **golang, ad, tiering**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| App RBAC inside a Go API | `golang-access-control` |
| Periodic access review campaigns | `golang-access-reviews` |
| Windows host priv-esc (lab) | `windows-privilege-escalation` |
| Secrets program | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Tier 0 | DCs, AD CS, Entra Connect, identity vaults, privileged access workstations |
| Tier 1 | Member servers, app servers, bastions for servers |
| Tier 2 | User workstations, VDI |
| Control | No Tier 0 admin logon to lower tiers; separate accounts; PAW/SAW |
| Go tooling | LDAP search (`go-ldap`), Microsoft Graph, scheduled inventory jobs |
| Detection | Unusual privileged group adds; interactive logon of Tier 0 to Tier 2 |
| Pitfalls | Shared break-glass; RDP with domain admin to app servers; unconstrained delegation |

## Workflow

### 1. Confirm scope and success criteria

1. Forest/domain list, owner, authorization, production vs lab.
2. Success: documented tier model; no Tier 0 principals with interactive logon on Tier 2; inventory job green.
3. Break-glass accounts listed, monitored, dual-control.

### 2. Inventory

1. Privileged groups: Domain/Enterprise Admins, Builtin Admins, Account Operators, etc.
2. Service accounts with DCSync-equivalent rights; gMSA usage.
3. Hosts that are Tier 0 by role even if not DCs (PKI, AAD Connect).
4. Existing PAW and jump host topology.

### 3. Baseline

1. Export group memberships and adminCount users (hash snapshot).
2. Sample recent privileged logons (from SIEM) for tier violations.
3. Record accepted exceptions with owners.

### 4. Apply tiering controls (with Go assist)

1. Define account naming and OU strategy per tier (human process + automation).
2. Go inventory job example shape:

```go
// Pseudocode: bind LDAP read-only, page search for member of privileged groups
req := ldap.NewSearchRequest(
	baseDN, ldap.ScopeWholeSubtree, ldap.NeverDerefAliases, 0, 0, false,
	"(&(objectClass=user)(memberOf=CN=Domain Admins,...))",
	[]string{"dn", "sAMAccountName", "adminCount", "userAccountControl"},
	nil,
)
```

3. Enforce: deny logon rights via GPO for Tier 0 groups on Tier 1/2; restrict RDP.
4. Prefer gMSA/OPAQUE secrets for services; no Tier 0 passwords on Tier 2 software.
5. Go services that manage identity must run as Tier-appropriate identities (not Domain Admin).

### 5. Verify with evidence

```bash
go test ./internal/adinventory/... -count=1
go test ./... -race -count=1
govulncheck ./...

# Lab: confirm policy — privileged user cannot RDP to workstation (expected deny)
```

1. Re-export membership; diff against baseline after remediation.
2. Attempt controlled violation in lab only → blocked + alerted.
3. Redact exports before attaching to tickets.

### 6. Observe and harden

1. Alert on membership changes to Tier 0 groups; alert on Tier 0 interactive logon to lower tiers.
2. Review LAPS/gMSA coverage; kerberoastable SPNs on high-privilege accounts.
3. Quarterly access reviews for Tier 0 (`golang-access-reviews`).

### 7. Hand off

1. Publish tier diagram and account rules to identity runbook.
2. CODEOWNERS for automation repos; on-call for identity pipeline.
3. Schedule next inventory diff review.

## Tier rule summary

| Rule | Intent |
| --- | --- |
| Separate admin accounts | User email account ≠ admin |
| Logon restrictions | High tier creds never touch low tier hosts |
| PAW for Tier 0 | Admin work only from hardened workstations |
| Time-bound elevation | JIT/PIM where available |
| Monitor | Group change + anomalous logon |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Tier 0 ops | PAW + JIT | Domain Admin daily driver laptop |
| Automation | Read-only LDAP first | Hardcoded DA password in Go config |
| Service identity | gMSA least privilege | SQL service as Domain Admin |
| Evidence | Membership diffs + SIEM | “We use tiers” slide only |
| Topic fidelity | AD tiers + Go inventory | Generic go test only |

## Output Checklist

- [ ] Forest scope and authorization recorded
- [ ] Tier definitions and asset classification done
- [ ] Privileged inventory snapshotted
- [ ] Logon restrictions / PAW path documented
- [ ] Go collector or equivalent automation verified
- [ ] Detection for tier violations configured
- [ ] Exceptions owned with expiry
- [ ] `code-quality-standards` applied to automation

## Rules

- Authorized directory work only; evidence over guesses.
- Prefer reversible GPO/group changes with rollback.
- Focus on `golang-ad-tiering`; route app RBAC and generic reviews nearby.
- Never store Tier 0 credentials in git or chat.
