---
name: ad-kerberoast-validation
description: Policy-gated Kerberoast risk assessment — review SPN inventory, encryption types, and service account hygiene without requesting tickets or cracking material.
disable-model-invocation: true
risk: disabled-default
allowed-modes: [red-team, offensive, grey-hat]
authorization-required: yes
evidence-outputs: [policy-note, approval-record]
disabled-category: credential-stuffing
---

# Kerberoast risk validation — policy-only assessment

Use this skill to assess Kerberoasting risk posture from approved read-only data: SPN inventory, service account encryption types, password policy, and delegation configuration. This skill never requests Kerberos service tickets, never handles ticket material, and never cracks hashes. Active Kerberoasting (requesting TGS, cracking) requires separate disabled-default unlock, explicit scope, per-engagement consent, and approval for destructive risk.

## Required inputs

- Written scope explicitly naming the domain, approved data sources (LDAP read-only query, offline SPN export, config review), approved review methods, and a clear statement that no ticket request or cracking is within scope.
- Repository config unlock for `credential-stuffing` disabled-default category.
- Per-engagement consent and valid authorization cache.
- Read-only LDAP export, BloodHound data, or admin-provided SPN inventory document.
- Known detection/escalation contact.

## Required gates

1. Repo config unlock for disabled-default category (`credential-stuffing`) via `pentest_agent_validate_policy`.
2. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
3. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
4. `pentest_agent_check_authorization` before any data review.
5. No `pentest_agent_execute_tool` calls that request tickets, handle hashes, or run cracking tools. Policy analysis only.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — SPN inventory and classification

From approved read-only data, build an SPN inventory:
1. List every account with `servicePrincipalName` set.
2. Classify each by:
   - **Account type**: user account vs computer account.
   - **Privilege level**: `adminCount=1` (high-value target), member of Domain Admins or equivalent.
   - **Encryption type**: RC4 (weakest), AES128, AES256.
   - **Service type**: HTTP, MSSQL, CIFS, LDAP, exchange, custom.
   - **Account age and password age**: old accounts with stale passwords are higher risk.
   - **Delegation flags**: unconstrained or constrained delegation on the account.

### Phase 2 — risk scoring

Score each SPN account on risk factors:
- **Highest risk**: `adminCount=1` + RC4 encryption + aged password + unconstrained delegation.
- **High risk**: `adminCount=1` + RC4 encryption.
- **Medium risk**: non-privileged user + RC4 encryption + weak password policy.
- **Low risk**: computer account + AES-only + regular password rotation.

Prioritize remediation recommendations by risk score.

### Phase 3 — password policy and encryption assessment

- Domain password policy: minimum length, complexity requirements. If minimum length < 12 or complexity is disabled, service account passwords may be crackable.
- Kerberos encryption policy: is AES enforcement configured? Are there RC4 exceptions?
- Service account password rotation: manually managed vs group-managed (gMSA).
- Stale service accounts: SPN accounts with no recent logon may have neglected passwords.

### Phase 4 — remediation recommendations

For each risk tier, recommend:
1. **Immediate**: migrate highest-risk SPN accounts to gMSA; enforce AES-only Kerberos; rotate passwords.
2. **Short-term**: increase password length for all service accounts; audit SPN inventory quarterly; remove unused SPNs.
3. **Long-term**: deploy Managed Service Accounts everywhere; enforce AES-only domain-wide; implement Kerberoast detection rules (Event ID 4769 with RC4 ticket encryption from non-DC sources).

## Decision points

- **Never recommend active Kerberoasting** from this skill. If the assessment suggests active validation is needed, the user must separately unlock disabled-default, scope the exact ticket request, and approve destructive risk.
- **Escalate to active preparation**: provide a precise scope outline for what would need to be authorized for active Kerberoasting — specific accounts, approval steps, detection coordination.
- **Stop on credential exposure**: if review data contains ticket material, hashes, or passwords → redact, stop, notify user.

## Prohibited behavior

- Requesting Kerberos service tickets (TGS) — even with `GetUserSPNs.py -request`.
- Handling, storing, or analyzing ticket material (`.kirbi`, `.ccache`, hashcat-format hashes).
- Cracking hashes with hashcat, John, or any other tool.
- Collecting credentials, coercing authentication, relaying, or dumping secrets.
- Expanding from risk assessment into exploitation without fresh scope, unlock, and approval gates.
- Storing SPN names, account names, or encryption type details in evidence unless scope allows.

## Stop conditions

- Next step would require ticket request, hash handling, or password cracking → policy-only, stop.
- Evidence would include ticket material, hashes, or passwords → redact and stop.
- Domain controller impact risk, account lockout, or detection alert from passive review activity → stop.

## Policy — when active Kerberoasting may be considered

Active Kerberoasting (requesting TGS, cracking offline) requires ALL of:
1. Repo config unlock for `credential-stuffing` disabled-default category.
2. Explicit written scope naming the exact accounts, domain controllers, and time window.
3. Per-engagement consent with destructive-risk approval.
4. Valid authorization cache.
5. Detection/escalation contact notified before activity begins.
6. All ticket material handled in memory or encrypted storage; never written to unencrypted evidence.
7. Cracked passwords stored only as redacted hashes; plaintext passwords never stored in evidence.

Without ALL seven gates, active Kerberoasting is prohibited.

## Evidence

Append policy assessment per finding:

```text
Finding class: <high-risk SPN account | weak encryption | gMSA gap>
Risk tier: <highest | high | medium | low>
Account type: <user SPN | computer SPN>
Privilege level: <adminCount=1 | privileged group | standard>
Encryption type: <RC4 | AES128 | AES256>
Recommendation: <migrate to gMSA | enforce AES | rotate password | remove SPN>
Data source: <LDAP export date | BloodHound data date | admin-provided inventory>
```

Redact SPN names, account names, and domain FQDN unless scope allows. Replace with type-classified summaries: `[3 adminCount=1 SPN accounts with RC4]`.

## Report handoff

1. `pentest_agent_record_finding` for each high-risk SPN configuration.
2. Include remediation roadmap prioritized by risk score.
3. Note: no tickets were requested, no hashes were cracked, no credentials were collected.
4. Provide detection rule recommendations so blue team can monitor for Kerberoasting activity.
5. Recommend: gMSA migration plan, AES enforcement timeline, SPN audit cadence, and Kerberoast detection deployment.
