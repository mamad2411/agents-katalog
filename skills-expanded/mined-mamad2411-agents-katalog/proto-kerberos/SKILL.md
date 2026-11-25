---
name: proto-kerberos
description: Kerberos configuration review without credential attacks — realm metadata, encryption type audit, delegation posture, ticket lifetime policy, pre-authentication requirements, and service principal name inventory. No Kerberoasting, AS-REP roasting, Pass-the-Ticket, or delegation exploitation by default.
disable-model-invocation: true
risk: caution
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Kerberos assessment — safe configuration review

Use this skill to review authorized Kerberos realm configuration, encryption type policy, delegation posture, ticket lifetime settings, pre-authentication requirements, and service principal name hygiene. All checks are read-only configuration review. Never request service tickets for offline cracking, request AS-REP responses for user accounts, forge or replay tickets, or abuse delegation — these are disabled-default credential attacks and require separate config unlock plus per-engagement consent.

## Required inputs

- Written scope naming the Kerberos realm, domain controllers authorized for read-only query, approved service account (read-only, unprivileged), and explicit list of allowed query types.
- Explicit permission for authenticated Kerberos queries using the approved service account. The account must have no more than domain-user privileges.
- Valid authorization cache for each domain controller and the realm.
- List of prohibited query types, explicitly including: Kerberoasting (service ticket request for offline cracking), AS-REP roasting (pre-auth disabled account enumeration), Pass-the-Ticket, Pass-the-Hash, Silver Ticket, Golden Ticket, DCSync, delegation abuse (S4U2Self/S4U2Proxy exploitation), and ticket replay.
- Separate disabled-default approval before any credential capture, ticket request for cracking, relay, coercion, lateral movement, or persistence workflow.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target` for each domain controller and the realm.
3. `pentest_agent_check_authorization` before any query.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools are used.
5. `pentest_agent_execute_tool` for all execution — use the most read-only, least intrusive tool available.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — realm metadata and configuration baseline

Using approved read-only service account or unauthenticated queries where possible:

1. **Realm identification**: determine the Kerberos realm name (usually the AD domain name in uppercase). Validate against scope.
2. **Domain controller discovery**: enumerate KDCs (Key Distribution Centers) for the realm via DNS `_kerberos._udp.<domain>` SRV records. Only query DCs explicitly listed in scope.
3. **Encryption type enumeration**: query supported encryption types (etype). This is a configuration check — it does not request tickets.
   - Using the approved service account, list supported etypes via `msDS-SupportedEncryptionTypes` attribute on domain controller computer objects (LDAP read — use the AD enumeration workflow if approved).
   - Flag weak encryption types: DES-CBC-CRC (etype 1), DES-CBC-MD5 (etype 2/3), RC4-HMAC (etype 23). RC4 is still widely used but should be flagged for migration to AES.
   - AES128-CTS-HMAC-SHA1-96 (etype 17) and AES256-CTS-HMAC-SHA1-96 (etype 18) are preferred.
   - Check if RC4 is disabled at domain level: look for `msDS-SupportedEncryptionTypes` with RC4 bit not set.
4. **Ticket lifetime policy**: query the domain's Kerberos policy via LDAP or `net accounts` equivalent (through executor, read-only). Record:
   - Maximum ticket lifetime (default 10 hours). Longer lifetimes increase the window for ticket theft and replay.
   - Maximum renewal lifetime (default 7 days). Shorter is more secure.
   - Service ticket lifetime.
   - User ticket lifetime.
   - Clock skew tolerance (default 5 minutes). Too large increases relay attack window.
5. **Pre-authentication policy**: check whether pre-authentication is required by default. This is a domain-wide policy — do not enumerate individual user pre-auth status (that would be AS-REP roasting, which is disabled-default).
   - Pre-authentication prevents unauthenticated attackers from requesting an AS-REP for any user and cracking it offline.
   - If pre-authentication is not required by default, flag as critical finding.

### Phase 2 — service principal name (SPN) inventory (read-only)

Service Principal Names link services to accounts in the domain. Reviewing the SPN list is a configuration audit — it does not involve requesting service tickets.

1. Enumerate SPNs via LDAP read with the approved service account:
   - Filter: `(servicePrincipalName=*)`.
   - Return attributes: `sAMAccountName`, `servicePrincipalName`, `userAccountControl`, `adminCount`, `memberOf`, `lastLogonTimestamp`.
   - Do NOT return: `unicodePwd`, `supplementalCredentials`, `msDS-KeyCredentialLink`.
2. From the SPN list, identify:
   - **High-value SPNs** (adminCount=1 or memberOf privileged groups): service accounts with Domain Admin or equivalent privileges. These are prime Kerberoasting targets if an attacker gains a foothold — flag as high finding.
   - **Stale SPNs**: accounts with `lastLogonTimestamp` older than 90 days that hold SPNs. Flag for cleanup.
   - **Duplicate SPNs**: same SPN registered to multiple accounts. This causes Kerberos authentication ambiguity and potential service impersonation.
   - **Weak cipher SPN accounts**: accounts that support RC4 as a supported encryption type. Flag for AES migration.
3. Record: total SPN count, high-value SPN count, stale SPN count, duplicate SPN count, RC4-capable SPN count.
4. **Do not request service tickets** (TGS) for any of these SPNs. SPN inventory is a read-only LDAP attribute query — Kerberoasting starts when you request `TGS-REP` for an SPN and crack it offline. This skill stops before that step.

### Phase 3 — delegation configuration audit

Kerberos delegation allows a service to impersonate a user to other services. Misconfigured delegation is one of the most common AD privilege escalation paths.

1. **Unconstrained delegation**: enumerate computers with `TrustedForDelegation` flag (`userAccountControl:1.2.840.113556.1.4.803:=524288`).
   - Unconstrained delegation allows the service to impersonate any user to any service.
   - If a Domain Controller has unconstrained delegation, this is a critical finding.
   - If a non-tier-0 server has unconstrained delegation and is compromised, the attacker can capture and replay TGTs from any user authenticating to that server.
2. **Constrained delegation**: enumerate accounts with `msDS-AllowedToDelegateTo` attribute populated.
   - Constrained delegation limits which services the delegation target can access.
   - Check if constrained delegation allows delegation to high-value services: `krbtgt`, `ldap`, `cifs` on Domain Controllers, `http` on sensitive web applications.
   - Protocol transition (`TrustedToAuthForDelegation` flag): allows a service to obtain a ticket for any user without that user authenticating — effectively, it can impersonate anyone. Flag as high finding if combined with constrained delegation to sensitive services.
3. **Resource-based constrained delegation (RBCD)**: enumerate computers with `msDS-AllowedToActOnBehalfOfOtherIdentity` set.
   - RBCD allows the specified account to impersonate any user to the target computer.
   - Check the trustee account's privileges: if a low-privilege account has RBCD rights over a high-value target, flag as high finding.
4. **Shadow credentials**: check for `msDS-KeyCredentialLink` on high-value accounts. This attribute allows certificate-based authentication as an alternative to passwords — an attacker who modifies it can authenticate as the target user. Flag as high finding for privileged accounts with this attribute set (it should be rare and intentional).

### Phase 4 — Kerberos policy hardening checks

These are configuration review items — no active exploitation:

1. **AES-only enforcement**: check if the domain or specific accounts enforce AES-only (RC4 disabled). This significantly reduces Kerberoasting effectiveness because RC4-crackable tickets are the easiest to crack.
2. **Service account password length**: recommend minimum 25-character random passwords for service accounts. Short or weak service account passwords enable fast Kerberoasting cracking.
3. **Group Managed Service Accounts (gMSA)**: recommend gMSA for service accounts where possible. gMSA provides automatic password rotation and removes the risk of static service account passwords.
4. **Protected Users group**: recommend adding high-value accounts (Domain Admins, service accounts with delegation) to the Protected Users group. This group enforces: AES-only Kerberos, no DES/RC4, no delegation (constrained or unconstrained), no NTLM fallback, shorter ticket lifetime.
5. **Kerberos armoring (FAST)**: check if Kerberos Flexible Authentication Secure Tunneling is enforced. FAST protects Kerberos AS-REQ/AS-REP exchanges from offline cracking by encrypting the pre-authentication exchange with the KDC's public key.

### Phase 5 — cross-realm trust review

If the scope includes cross-realm or forest trust review:

1. Enumerate domain trusts via LDAP: `(objectClass=trustedDomain)`.
2. For each trust, record: trust direction (inbound, outbound, bidirectional), trust type (parent-child, forest, external, realm), trust attributes (filtering enabled, quarantined, etc.).
3. Flag trusts where:
   - SID filtering is disabled (attackers in trusted domain can forge SIDs to gain Enterprise Admin access).
   - Selective authentication is disabled (any user in trusted domain can authenticate to trusting domain).
   - The trust is to an external domain or realm with lower security posture.
4. Do not exploit cross-realm trust relationships (no ticket forwarding, referral ticket abuse, or inter-realm TGT forgery).

## Decision points

- **High-value SPN with RC4 support**: medium finding — potential for fast Kerberoasting if a foothold is obtained. Recommend AES migration and Protected Users group.
- **Unconstrained delegation on Domain Controller**: critical finding — enables DCSync-style attack via printer bug or coercion. Recommend removing delegation or upgrading to constrained delegation.
- **Pre-authentication not enforced**: critical finding — AS-REP roasting is trivial. Require pre-authentication by default.
- **RC4 not disabled**: medium finding — increases Kerberoasting speed (RC4-crackable tickets vs AES). Recommend enforcing AES-only.
- **Escalate to credential attack workflow**: do NOT do this from this skill. Kerberoasting, AS-REP roasting, and delegation exploitation are disabled-default. If operator needs them, route to policy review and explicit unlock process.
- **Downgrade to report-only**: when no authenticated read access is available and unauthenticated checks are exhausted.

## Prohibited behavior

- **Kerberoasting**: requesting service tickets (TGS-REP) for SPNs and attempting offline cracking. This is a credential attack — disabled-default.
- **AS-REP roasting**: enumerating accounts with pre-authentication disabled and requesting AS-REP responses for offline cracking. Disabled-default.
- **Pass-the-Ticket**: capturing and reusing Kerberos tickets for lateral movement. Disabled-default (lateral movement + credential theft).
- **Pass-the-Hash**: using NTLM hashes to authenticate via Kerberos (overpass-the-hash). Disabled-default.
- **Silver Ticket**: forging service tickets with captured service account hashes. Disabled-default (persistence + privilege escalation).
- **Golden Ticket**: forging TGTs with KRBTGT hash. Disabled-default (persistence + privilege escalation).
- **DCSync**: replicating domain credentials from a Domain Controller. Disabled-default (credential theft).
- **Delegation abuse**: exploiting unconstrained/constrained/RBCD delegation for privilege escalation. Disabled-default.
- **S4U2Self/S4U2Proxy exploitation**: using protocol transition to impersonate users. Disabled-default.
- **Ticket replay**: capturing and replaying Kerberos tickets within their validity window. Disabled-default.
- **Requesting any TGT or TGS for offline processing.**
- **Accessing `KRBTGT` account attributes or hashes.**
- **Running `mimikatz`, `secretsdump`, `ntdsutil`, or similar credential dumping tools.**

## Stop conditions

- Any command would request a TGS for a service (Kerberoasting) → stop, explain it's disabled-default.
- Any command would enumerate per-user pre-authentication status (AS-REP roasting) → stop.
- Any command would export or manipulate ticket caches → stop.
- Account lockout risk detected → stop all authenticated queries.
- Evidence would include hashes, tickets, passwords, or Kerberos key material → redact and stop that data collection path.
- Domain Controller performance impact (high LDAP query load) → reduce query rate, stop heavy enumeration.

## Evidence — Kerberos configuration record

For each authorized realm:

```text
Realm: EXAMPLE.COM
Domain Controllers queried: [DC01, DC02]
Service account: (hash — redacted)

Encryption types:
  Supported: [AES256-CTS-HMAC-SHA1-96 (18), AES128-CTS-HMAC-SHA1-96 (17), RC4-HMAC (23)]
  Weak types present: RC4-HMAC (23) — not yet disabled
  DES: disabled (positive)

Ticket policy:
  Max ticket lifetime: 10 hours (default)
  Max renewal lifetime: 7 days (default)
  Clock skew: 5 minutes (default)

Pre-authentication: required by default (positive)

SPN inventory:
  Total SPNs: 142
  High-value SPNs (adminCount=1): 8 — accounts with elevated privileges
  Stale SPNs (> 90 days no logon): 23 — recommend cleanup
  Duplicate SPNs: 2 — service ambiguity risk
  RC4-capable SPNs: 98 — recommend AES migration

Delegation posture:
  Unconstrained delegation computers: 3 (including DC01 — CRITICAL)
  Constrained delegation accounts: 12
  Protocol transition allowed: 4 accounts (high risk)
  RBCD configured: 2 computers

Cross-realm trusts:
  Trusts: [CHILD.EXAMPLE.COM (bidirectional, forest), EXTERNAL.LOCAL (inbound, external)]
  SID filtering: enabled on all trusts (positive)
  Selective authentication: enabled on EXTERNAL.LOCAL (positive)
  Low-security trust: EXTERNAL.LOCAL — trust to external domain with unknown security posture

Findings:
  [CRITICAL] DC01 has unconstrained delegation — full domain compromise risk
  [HIGH] 8 high-value SPN accounts with RC4 support — potential fast Kerberoasting
  [MEDIUM] 98 of 142 SPN accounts still allow RC4 — AES migration recommended
  [MEDIUM] 23 stale SPN accounts — attack surface without active use
  [MEDIUM] 4 accounts with protocol transition allowed to sensitive services
  [LOW] Max ticket lifetime 10 hours — consider reducing to 4-6 hours
  [INFO] Pre-authentication enforced by default — positive
```

Aggregate into a Kerberos security posture summary per realm. Include: encryption type matrix, SPN hygiene metrics, delegation risk assessment, trust relationship audit, policy hardening gaps, and recommended remediation per finding class.

Never store: raw LDAP query output with user/computer names (unless scope allows), actual SPN values that reveal internal service paths, ticket data, hashes, encryption keys, password fields, or `msDS-KeyCredentialLink` raw data.

## Report handoff

1. `pentest_agent_record_finding` for each confirmed weakness: unconstrained delegation, protocol transition abuse risk, RBCD misconfiguration, high-value SPN exposure, weak encryption type support, missing pre-authentication, stale SPNs, cross-realm trust weakness.
2. Package findings for both AD operations team (remediation) and detection team (monitoring for abuse).
3. Recommend: remove unconstrained delegation, migrate to constrained delegation with least privilege, enforce AES-only Kerberos, add service accounts to Protected Users group, deploy gMSA for service accounts, enforce pre-authentication, audit and clean up stale SPNs, enable Kerberos armoring (FAST), reduce ticket lifetimes, enable SID filtering on all trusts, and conduct regular Kerberos posture reviews.
4. Explicitly note that no Kerberoasting, AS-REP roasting, Pass-the-Ticket, Pass-the-Hash, Silver/Golden Ticket, DCSync, delegation exploitation, or ticket cracking was performed — only safe configuration review. The findings above are architectural weaknesses observed from read-only enumeration; actual exploitation requires separate disabled-default unlock and explicit per-engagement consent.
