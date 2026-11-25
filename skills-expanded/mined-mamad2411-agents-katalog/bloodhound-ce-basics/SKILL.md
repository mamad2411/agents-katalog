---
name: bloodhound-ce-basics
description: >
  BloodHound Community Edition for owned Active Directory labs: deploy CE, collect with
  SharpHound/AzureHound under authorization, ingest into neo4j/BHAPI, run attack-path
  queries (Shortest Path to DA, Kerberoastable, ACL edges), and export findings for
  remediation. Use when BloodHound CE, SharpHound, AD attack paths, owned lab graph
  analysis — not against production domains without written authorization.
---

# BloodHound CE Basics

## Scope And Authorization

- **In scope:** AD / Entra ID environments you own, lab forests, CTF ranges, or written-scope red/purple team assessments.
- **Out of scope:** Unauthorized collection against third-party domains, credential stuffing, or using paths to attack systems outside engagement scope.
- Collection is **active** enumeration — get explicit authorization; schedule after-hours if production.
- Redact domain names, admin UPNs, computer names, and path screenshots in public notes.
- Pair remediations with AD hardening skills and `code-quality-standards` for any automation scripts.

## When To Use

- Standing up BloodHound CE (Docker or supported install) for a lab or engagement.
- Running SharpHound (on-prem AD) or AzureHound (Entra) collectors within scope.
- Finding paths to Domain Admin, high-value targets, dangerous ACLs, Kerberoastable SPNs, unconstrained delegation.
- Producing evidence packs for AD tiering / ACL cleanup workstreams.
- Teaching or purple-team validation of detection coverage for enumeration.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| AD CS / Certipy lab abuse paths | `certipy-adcs-lab` |
| Windows host privilege escalation | `windows-privilege-escalation` |
| Generic recon methodology | `recon-and-methodology` |
| Production break-glass / PAM design | `boundary-hashicorp-basics` or org PAM skill |
| Implementation quality for scripts | `code-quality-standards` |

## Domain Focus

| Component | Role |
| --- | --- |
| BloodHound CE | UI + API + graph analysis (community edition) |
| Neo4j (or bundled graph) | Stores nodes/edges from collectors |
| SharpHound | On-prem AD collector (session, ACL, trust, etc.) |
| AzureHound | Entra ID / AzureRM graph edges |
| Cypher / built-in queries | Path finding and inventory |
| High-value targets (HVTs) | Mark DCs, DA groups, tier-0 assets |

## Workflow

### 1. Confirm scope and success criteria

1. Record forest/domain FQDN, engagement window, allowed collector hosts, data retention, and whether Azure is in scope.
2. Success: CE running; collection ingested; at least one validated attack path or clean negative; findings mapped to owners.
3. Define **stop rules**: no password spraying, no exploitation beyond agreed TTPs unless authorized.

### 2. Deploy BloodHound CE (lab example)

```bash
# Follow current CE compose docs for your version; example pattern only
git clone https://github.com/SpecterOps/BloodHound.git  # or official CE release assets
cd BloodHound  # or extracted release
# Configure .env with strong passwords for neo4j / BH; never commit real secrets
docker compose up -d
# UI typically https://localhost:8080 (verify compose ports for your tag)
```

1. Set unique admin password; disable default demos on shared lab hosts.
2. Restrict UI to VPN/lab network; do not expose BloodHound to the public Internet.
3. Note version of CE + collector compatibility.

### 3. Collect under authorization

**SharpHound (domain-joined Windows lab host example):**

```powershell
# Run only on authorized engagment/lab hosts
.\SharpHound.exe -c All --outputdirectory C:\BHOut --zipfilename lab_collection
# Stealthier / scoped examples (adjust to RoE):
.\SharpHound.exe -c Session,SessionLoop --Loop --Loopduration 00:30:00
.\SharpHound.exe -d lab.example --ldapusername 'collector' --ldappassword '***'
```

**AzureHound (when Entra is in scope):**

```powershell
# Device code or app registration per engagement design
AzureHound.exe list all -o azure_out
```

1. Prefer dedicated low-priv collector account over DA credentials when possible.
2. Track collection time, host, user, flags used in the engagement log.
3. Transfer zips over approved channels; virus-scan per org policy.

### 4. Ingest and mark high-value targets

1. Upload zip via BloodHound CE UI (or API for automation).
2. Wait for analysis job completion; refresh node counts.
3. Mark Domain Controllers, DA/EA groups, backup servers, PKI, Azure Global Admin as owned/high value per CE workflow.
4. Optionally tag engagment-specific crown jewels.

### 5. Query attack paths (built-in + Cypher)

Typical analysis order:

1. **Shortest paths to Domain Admins** from owned principals (kerberoastable users, computers you control in lab).
2. **Dangerous privileges:** `GenericAll`, `WriteDacl`, `ForceChangePassword`, `DCSync`-capable rights.
3. **Delegation:** unconstrained / constrained / RBCD-related edges.
4. **Sessions:** where DA sessions land (admin workstation hygiene).
5. **Trusts:** outbound trusts that expand blast radius.

```cypher
// Example: paths to Domain Admins group (syntax may vary slightly by schema version)
MATCH p=shortestPath((n)-[:MemberOf|HasSession|AdminTo|GenericAll|GenericWrite|WriteDacl|WriteOwner|Owns|ForceChangePassword|AllExtendedRights*1..]->(m:Group))
WHERE m.name STARTS WITH 'DOMAIN ADMINS@' AND n <> m
RETURN p LIMIT 25
```

1. Save custom queries that match the engagement.
2. Export path screenshots + edge explanations for each finding (edge type → meaning → fix).
3. Validate one path in lab with intentional, authorized steps only — do not “prove” by destroying prod.

### 6. Remediate and re-collect

| Finding class | Typical remediation direction |
| --- | --- |
| Overbroad ACL on OU/user | Remove delegated rights; use nested groups + tiering |
| Unconstrained delegation | Disable or move to constrained/RBCD patterns |
| Kerberoastable high-priv | AES, long random passwords, gMSA, no DA SPNs |
| Session on tier-0 | Separate PAWs; no email/browse on DA hosts |
| Stale admins | Remove nested group chains; recertify membership |

1. After fixes, re-run collector and confirm path removed or lengthened.
2. File tickets with principal names, edge type, and evidence IDs.
3. Detect: ensure Defender/M365 or SIEM covers SharpHound-like LDAP volume if purple teaming.

### 7. Hand off and data disposal

1. Deliver path catalog + remediation owners + residual risk.
2. Per RoE: wipe collector output, CE database, and neo4j volumes after retention period.
3. Do not leave BloodHound exposed with engagement data.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Authz | Written scope + collector account | SharpHound on customer prod “to learn” |
| Exposure | Lab VPN only UI | CE on 0.0.0.0 with weak password |
| Analysis | Edge-explained paths + fix | Dump of 500 unprioritized paths |
| Creds | Least-priv collector | Paste DA password into ticket |
| Re-test | Second collection after ACL fix | Assume fixed without re-ingest |
| Azure | AzureHound only if Entra scoped | Pull tenant without cloud RoE |

## Output Checklist

- [ ] Authorization, domains/tenants, window, stop-rules recorded
- [ ] CE version deployed; UI not Internet-exposed
- [ ] Collector flags, host, identity logged
- [ ] Data ingested; HVTs marked
- [ ] Priority paths documented with edge semantics
- [ ] Remediations ticketed; re-collection plan set
- [ ] Data retention/disposal plan executed or scheduled
- [ ] Secrets and screenshots redacted for external reports

## Rules

- Active Directory collection without authorization is out of scope — always.
- Prefer analysis and remediation evidence over showy full-forest dumps.
- Never store engagement zips in public cloud buckets or chat.
- Route AD CS certificate abuse to `certipy-adcs-lab`; keep this skill on CE graph workflow.
- Lab practice first; production only under RoE.
