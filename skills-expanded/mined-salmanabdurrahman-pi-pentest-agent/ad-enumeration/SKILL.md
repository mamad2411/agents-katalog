---
name: ad-enumeration
description: Scope-bound Active Directory enumeration — review approved read-only LDAP, SMB, and Kerberos data without credential capture or lateral movement.
disable-model-invocation: true
risk: caution
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Active Directory enumeration — read-only approved review

Use this skill to review Active Directory structure, users, groups, computers, trusts, delegation, GPOs, and ACLs when scope explicitly authorizes authenticated read-only queries. All queries must use approved credentials, stay within named domain controllers and organizational units, and never collect credential material.

## Required inputs

- Written scope naming the domain, domain controllers, organizational units, approved query types (LDAP, SMB share listing, Kerberos user enumeration), approved service account with read-only privileges, rate limits, testing window, and detection/escalation contact.
- Explicit permission for authenticated AD queries. Separate disabled-default approval required before any credential capture, cracking, relay, coercion, lateral movement, persistence, or wireless-adjacent workflow.
- Valid authorization cache for each domain controller and domain.
- List of prohibited query types: password spraying, brute force, credential stuffing, hash capture, ticket request, secret dumping, service disruption.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target` for each DC and domain.
3. `pentest_agent_check_authorization` before any query.
4. `pentest_agent_build_command` for dry-run argv preview.
5. `pentest_agent_execute_tool` for execution — use the most read-only, least intrusive tool available.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — safe domain baseline

Start with the minimum query set to understand domain topology:
- Domain trusts and forest membership (LDAP: `(objectClass=trustedDomain)`).
- Domain functional level.
- Password policy (lockout threshold, minimum length, complexity, history).
- Domain controller list and OS versions.
- Privileged group membership: Domain Admins, Enterprise Admins, Schema Admins, Administrators, Account Operators, Backup Operators, Server Operators, DnsAdmins.

Use ADSI, LDAPsearch, or equivalent with explicit read-only bind. If the catalog provides an approved enumeration tool, route through `pentest_agent_execute_tool`. Never send raw `ldapsearch` or `netexec` through raw bash.

### Phase 2 — user and computer inventory

With explicit scope approval:
- User count, enabled/disabled ratio, adminCount=1 users.
- Service accounts (SPN holders) — record count and naming patterns, never request tickets.
- Computer count, OS distribution, last logon summary.
- Stale objects: users and computers with no logon in > 90 days.

Limit attributes to: `sAMAccountName`, `userAccountControl`, `memberOf`, `servicePrincipalName`, `adminCount`, `lastLogonTimestamp`, `operatingSystem`. Never request `unicodePwd`, `dBCSPwd`, `lmPwdHistory`, `ntPwdHistory`, `supplementalCredentials`, or `userPassword`.

### Phase 3 — delegation and ACL review

- Unconstrained delegation computers: `userAccountControl:1.2.840.113556.1.4.803:=524288`.
- Constrained delegation: `msDS-AllowedToDelegateTo` entries.
- Resource-based constrained delegation: computers with `msDS-AllowedToActOnBehalfOfOtherIdentity` set.
- Risky ACLs: check for GenericAll, WriteDacl, WriteOwner, ForceChangePassword, AddMember on privileged objects. Do not enumerate full ACL on every object — sample from high-value targets (Domain Admins group, Domain object, DC computer objects).

### Phase 4 — GPO and configuration review

- GPO count and links to OUs.
- Check for GPP passwords: SYSVOL XML files containing `cpassword` attributes.
- LAPS configuration: `ms-Mcs-AdmPwd` attribute presence.
- Kerberos configuration: max ticket lifetime, max renewal, enforcement of AES-only.

### Phase 5 — share and service enumeration

Only when scope explicitly authorizes SMB share listing:
- Enumerate shares on approved hosts.
- List share names and access levels — do not list file contents unless specifically authorized.
- Record any world-readable shares containing sensitive-looking names: `passwords`, `backup`, `config`, `IT`, `HR`, `Finance`.

## Decision points

- **Stop before credential material**: if any query returns hashes, tickets, passwords, or secrets in output → redact immediately, stop that query line.
- **Escalate on policy weakness**: reversible encryption enabled, pre-Windows 2000 compatible access, no LAPS, GPP passwords found → medium/high finding.
- **Escalate on delegation risk**: unconstrained delegation on non-tier-0 hosts, constrained delegation to DC services, resource-based delegation writable by non-admin → high finding.
- **Downgrade to report-only**: when scope limits enumeration to provided static data (CSV/JSON export) with no live queries.

## Prohibited behavior

- Password spraying, brute force, credential stuffing, hash capture, ticket request, secret dumping, file modification, service disruption, or lateral movement.
- Accessing user files, mailboxes, shares, tickets, registry secrets, or directory data beyond approved read-only attributes.
- Running noisy scanners without scope, rate, and executor approval gates.
- Enumerating out-of-scope domains, forests, or organizational units.
- Storing raw directory data containing user principal names, group memberships, or computer names unless scope explicitly allows.

## Stop conditions

- Account lockout risk, authentication error spike, or domain controller performance impact.
- Sensitive share content appears (passwords, private keys, PII).
- Query suggests escalation to credential capture, cracking, relay, or lateral movement → policy-only, do not proceed.
- Evidence would include hashes, tickets, passwords, or confidential directory data → redact and stop.

## Evidence — enumeration matrix

Record per query domain:

```text
Domain: <domain FQDN>
DC: <DC hostname, redacted if required>
Query type: <LDAP user list | LDAP group membership | SMB share list | ...>
Attributes requested: <list>
Result summary: <count of objects | group size | share count>
Risk flags: <none | GPP password | unconstrained delegation | stale admin | ...>
Data redacted: <yes — UPNs removed | no — scope allows>
Confidence: <confirmed | needs-review>
```

Aggregate into a domain security posture summary. Include:
- domain topology and trust map (high-level);
- privileged group hygiene findings;
- delegation configuration risks;
- GPO/password policy gaps;
- recommended remediation per finding class.

Never store: raw LDAP output, unredacted user/computer/group names (unless scope allows), hashes, tickets, passwords, GPP cpassword values, or private keys.

## Report handoff

1. `pentest_agent_record_finding` for each confirmed misconfiguration, delegation risk, GPP exposure, or policy weakness.
2. Package findings for both AD operations team (remediation) and detection team (monitoring).
3. Recommend: LAPS deployment, delegation cleanup, privileged group hygiene, GPO audit, AES-only Kerberos enforcement, and regular read-only enumeration cadence.
4. Explicitly note that no credential attacks were performed and no hashes/tickets were collected.
