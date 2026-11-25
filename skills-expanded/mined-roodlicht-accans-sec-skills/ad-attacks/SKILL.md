---
name: ad-attacks
description: Active Directory attack paths — BloodHound path analysis, Kerberos abuse (Kerberoasting/AS-REP roasting/silver/golden ticket classes), delegation flaws (unconstrained/constrained/RBCD), DCSync, ADCS ESC1-8 at pattern level, and Tier-0 hygiene as a defensive model.
---

# AD Attack Paths

> **RoE-only and lab discipline**: AD attacks usually touch the highest-privilege layer of an organization. Version-specific ticket-extraction recipes, vendor-tool output, and ready-to-run DCSync commands for production are not in this skill; they belong in a closed engagement workspace. The skill contains class names, BloodHound edge types, ATT&CK T-IDs, and defensive counterparts. Lab work happens in a separate AD test domain.

## When to use

Active Directory is the identity foundation of most enterprise networks. Path analysis and privilege escalation within AD follow fairly predictable patterns documented extensively by SpecterOps, Microsoft, and others. This skill provides the structural lens.

Triggers on:

- A question like "triage BloodHound output", "Kerberoasting in scope", "delegation flaws in our AD", "ADCS attack paths", "Tier-0 design".
- A red-team / pentest engagement where internal AD is in scope and a first foothold has been gained (see `post-exploit` for broader methodology; this skill is the AD-specific deepening).
- A purple-team exercise around AD detection tuning.
- A defensive context where you run BloodHound on your own AD and want to close attack paths.
- A migration or ADCS design review tied to `iso27001` or `nis2` Tier-0 requirements.

### When NOT (handoff)

- Initial access into the network → `phishing-sim`, `web-exploit-triage`, `recon-agent`. This skill starts with an existing domain user or computer account.
- Broader post-exploitation outside AD context → `post-exploit`. Lots of overlap; this skill is the AD-specific part.
- C2 infrastructure and beacon OPSEC → `c2-hygiene`. Mentioned as context, not developed here.
- Final reporting with CVSS → `pentest-reporter`.
- Detection-rule building on the techniques → `detection-engineer`. This skill provides the attack side and links to the detection opportunity.
- Cloud-IAM equivalents (Azure AD / Entra ID has its own pattern set): partly here (hybrid scenarios, ADFS, Entra Connect), pure cloud-IAM attacks belong elsewhere.
- Forensics after an AD incident → `forensics-assist` plus `ir-runbook`.

## Approach

Six phases. Phase 1 (BloodHound + scope) and phase 5 (Tier-0 design as a defensive framework) are the places where AD work succeeds or fails.

### 1. BloodHound path analysis

BloodHound (SpecterOps OSS, Apache-2) is the standard tool for AD graph analysis. Edges (relationships) between nodes (users, groups, computers, domains, ADCS objects) reveal attack paths instead of isolated misconfigs.

- **Collection**: SharpHound (Windows binary) or Rusthound / BloodHound-Python on a delivered AD context. Lab engagements use SharpHound; defensive self-assessment can use offline export.
- **Edge types** (class level):
  - `MemberOf`, `AdminTo`, `CanRDP`, `ExecuteDCOM`: direct-access relationships.
  - `GenericAll`, `GenericWrite`, `WriteDACL`, `WriteOwner`, `Owns`: DACL rights enabling owner takeover or password reset.
  - `ForceChangePassword`, `AddMember`, `AddSelf`: group/user mutations.
  - `AllowedToDelegate`, `AllowedToActOnBehalfOfOtherIdentity`: delegation edges (see phase 3).
  - `HasSession`: contains-credential indicator (legacy valuable for token impersonation).
  - `DCSync`: replicating-rights edge (critical).
  - `ADCSESC1` through `ADCSESC10`: ADCS templates with attack paths (see phase 4).
- **Cypher queries for path-finding**: shortest path to domain admins, shortest path from compromised user X to a Tier-0 asset, all edges of type Y in a domain. SpecterOps documents canonical queries.
- **Triage workflow**: rank all paths on (a) hop count, (b) edge types (DACL > session > membership), (c) realistic feasibility. Not every 1-hop edge is a quick win; some require specific tooling or admin action.

Defensive use: BloodHound on your own domain produces a prioritization list for hardening. Combine with `risk-register`.

### 2. Kerberos abuse classes

Kerberos has a number of canonical attack classes that show up in nearly every red-team report.

- **Kerberoasting (T1558.003)**. Service accounts with an associated SPN can have TGS tickets requested by any authenticated user. The ticket contains a password-derived encrypted blob, offline-crackable if the password is weak (RC4-encrypted is faster to crack than AES). Defensive: all service accounts gMSA, RC4 disabled, audit Kerberos Service Ticket Operations (Event 4769 with TicketEncryptionType 0x17 for RC4).
- **AS-REP roasting (T1558.004)**. Accounts with the `DONT_REQ_PREAUTH` UAC flag release an AS-REP without pre-auth, also offline-crackable. Defensive: pre-auth required on every account, audit which accounts have this flag.
- **Pass-the-Ticket (T1550.003)**. Reuse a stolen TGT/TGS ticket on a different machine. Detection via 4768/4769 events in odd contexts.
- **Silver Ticket (T1558.002)**. TGS ticket forged with the service-account NTLM hash → service access without touching a DC. Defensive: tier-0 isolation, password rotation on service accounts.
- **Golden Ticket (T1558.001)**. TGT forged with the krbtgt hash → domain-admin-level access for a long time. Detection via anomalous-TGT lifetime, krbtgt account use as a client identifier; defense via double krbtgt rotation (procedure from SpecterOps + Microsoft).
- **Diamond/Sapphire Ticket**: variant on Golden, request shape less recognizable. Recent class, detection rule set still in motion.

General Kerberos discipline: monitor pre-auth events, ticket encryption types (RC4 as a red flag), use of krbtgt by service accounts.

### 3. Delegation flaws

Delegation lets a service act on behalf of a user. Misconfig is a high-impact attack path.

- **Unconstrained Delegation**. A service account with the `TRUSTED_FOR_DELEGATION` UAC flag receives a TGT from every user that signs in alongside. Attacker forces an admin (the printer-spool-service trick) to connect and steals the TGT. Defensive: minimize unconstrained delegation, audit accounts with this flag.
- **Constrained Delegation (S4U2Self / S4U2Proxy)**. A service can only delegate to specific services. Attack: if the compromised account has constrained-delegation rights to a Tier-0 service, a TGS can be forged for any user name (S4U-Self/Proxy trick).
- **Resource-Based Constrained Delegation (RBCD)**. The destination resource decides who may delegate via the `msDS-AllowedToActOnBehalfOfOtherIdentity` attribute. Attack: GenericWrite on a computer object → write your own account as trusted → use S4U to impersonate to that computer object. SpecterOps' "RBCD" research is canonical.

Defensive: minimize delegation rights, use Authentication Policies and Authentication Policy Silos to exclude tier-0 accounts from impersonation.

### 4. DCSync, AD CS, and high-impact attack paths

- **DCSync (T1003.006)**. An account with the `Replicating Directory Changes` right can pose as a DC and pull password hashes, including krbtgt. Defensive: only DCs and specific replication accounts hold this right, audit Event 4662 with directory-replication rights.
- **AD CS (Active Directory Certificate Services)**: a major attack surface since 2021 after SpecterOps' "Certified Pre-Owned" paper. ESC1 through ESC10+ classes. At pattern level:
  - **ESC1**: certificate template allows client-supplied SAN → request a cert with an admin SAN, authenticate as admin.
  - **ESC2**: any-purpose EKU → request authenticator cert.
  - **ESC3**: enrollment-agent abuse.
  - **ESC4**: vulnerable template permissions (write-DACL on the template).
  - **ESC5**: PKI-objects DACL misconfig.
  - **ESC6**: EDITF_ATTRIBUTESUBJECTALTNAME2 flag on the CA.
  - **ESC7**: vulnerable CA permissions.
  - **ESC8**: NTLM relay to AD CS web enrollment.
  - **ESC9 / ESC10**: newer variants around the `userCertificate` attribute and LDAP pre-auth.

Tools: Certify (offensive, lab-only), Certipy (Python port), PSPKIAudit (defensive). Defensive: ADCS template audit, web-enrollment off, EDITF flag off, mark tier-0-only templates explicitly.

### 5. Tier-0 hygiene as a defensive framework

Microsoft's Tier model (since ~2014, refreshed in the Enterprise Access Model) is the structural defense against all the classes above.

- **Tier-0**: identity systems — DCs, ADFS servers, Entra Connect, ADCS CAs, PKI keys, krbtgt. Compromise here = domain takeover.
- **Tier-1**: server OS, application platforms, business data.
- **Tier-2**: workstations, end-user devices.

**Rule**: a higher-tier account must never log on interactively to a lower-tier system. A Tier-0 admin on a Tier-2 laptop = Tier-0 credential-theft risk.

Implementation:

- **Authentication Policies + Silos** within AD: block Tier-0 accounts from logging in on non-Tier-0 systems.
- **Privileged Access Workstations (PAW)** for Tier-0 work.
- **Just-In-Time access** for admin rights (Azure AD PIM / on-prem equivalent).
- **No service accounts in Domain Admins**, as strict as possible.
- **gMSA** (group-Managed Service Accounts) for service accounts: passwords managed by AD, rotation automatic, not kerberoastable.

The Tier model is the anchor of an audit report: per BloodHound edge that leads to Tier-0, the design question "why is this path allowed to exist".

### 6. Verification-loop and handoff

Layer 1: scope (all BloodHound collection within RoE? all techniques explicitly permitted?), assumptions (path feasibility confirmed at pattern level, not just edge presence?), gaps (Tier-0 impact claims supported?). Layer 2: ATT&CK T-IDs correct, BloodHound edge-type names match the current BloodHound version (CE / 4.x), ADCS ESC classification verified against the SpecterOps paper, no invented Kerberos encryption types or UAC flag names.

Handoff:

- `pentest-reporter`: finding format with ATT&CK mapping per used technique.
- `purple-ops` / `detection-engineer`: detection opportunity per step (which Event ID, which Sigma rule).
- `policy-drafter`: input for Access Control Policy and Privileged Access Policy.

## Output

```
AD Attack Path Assessment — <domain>
Foothold:        <user context, machine, privileges>
RoE scope:       <Tier reach, which systems, which techniques>

BloodHound path analysis:
  Collection source:     <SharpHound/Rusthound/BloodHound-Python> + date
  Shortest paths to DA:  <N paths, shortest = M hops>
  Tier-0 reachable:      <yes/no, via which edges>
  Top-N highest-impact paths, ranked:
    Path-1: <description + edges>
    Path-2: ...

Kerberos flaws:
  Kerberoastable accounts:    <N>, <which with RC4 tickets>
  AS-REP roastable:           <N>
  RC4 tickets in use:         <% of TGS>
  Pass-the-Ticket evidence:   <if observed>

Delegation issues:
  Unconstrained:              <N machines/accounts>
  Constrained without Tier-0 isolation: <list>
  RBCD misconfig:             <on what>

DCSync + AD CS:
  DCSync rights outside DC:   <accounts/groups>
  ADCS vulnerable templates:  <ESC classification per template>

Tier-0 hygiene:
  Authentication Policies + Silos: <present/absent>
  PAW use:                         <present/absent>
  Service accounts in Tier-0:      <N>
  gMSA coverage:                   <%>

Per finding:
  Severity:        <Critical/High/Medium>
  ATT&CK:          <T-IDs>
  D3FEND counter:  <relevant>
  Detection opp.:  <Event-ID + signal shape>

Cleanup status:
  <no persistence created | persistence-X cleaned up>

Verification-loop: ...
```

## References

- **BloodHound + SpecterOps blog** — [https://bloodhound.specterops.io/](https://bloodhound.specterops.io/) and [https://specterops.io/blog/](https://specterops.io/blog/). Canonical source for edge types and attack-path research.
- **MITRE ATT&CK — Kerberos** — [https://attack.mitre.org/techniques/T1558/](https://attack.mitre.org/techniques/T1558/) and sub-techniques.
- **SpecterOps "Certified Pre-Owned"** — [https://specterops.io/wp-content/uploads/sites/3/2022/06/Certified_Pre-Owned.pdf](https://specterops.io/wp-content/uploads/sites/3/2022/06/Certified_Pre-Owned.pdf). Canonical ADCS ESC paper.
- **Microsoft Enterprise Access Model** — [https://learn.microsoft.com/en-us/security/privileged-access-workstations/privileged-access-access-model](https://learn.microsoft.com/en-us/security/privileged-access-workstations/privileged-access-access-model). Tier-0 architecture.
- **Microsoft — krbtgt password reset** — [https://github.com/microsoft/New-KrbtgtKeys.ps1](https://github.com/microsoft/New-KrbtgtKeys.ps1). Official krbtgt rotation procedure.
- **MITRE D3FEND — Kerberos defenses** — [https://d3fend.mitre.org/](https://d3fend.mitre.org/).
- **PSPKIAudit** — [https://github.com/GhostPack/PSPKIAudit](https://github.com/GhostPack/PSPKIAudit). Defensive self-assessment for ADCS.
- **Microsoft Authentication Policies + Silos** — [https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/how-to-configure-protected-accounts](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/how-to-configure-protected-accounts).
- **CIS Microsoft Active Directory Benchmark** — [https://www.cisecurity.org/](https://www.cisecurity.org/). Configuration baselines.

## Categories

- pentest
