---
name: ad-bloodhound-review
description: Offline BloodHound graph review — analyze user-provided AD data for privilege escalation paths, delegation risk, ACL edges, and tiering gaps without active collection.
disable-model-invocation: true
risk: report-only
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: conditional
evidence-outputs: [notes, redacted-evidence, finding-draft]
---

# BloodHound data review — offline privilege path analysis

Use this skill to analyze user-provided BloodHound/SharpHound graph exports, LDAP dumps, or AD assessment data for privilege escalation paths, delegation risks, ACL weaknesses, Kerberoastable account exposure, session-based attack paths, and tiering violations. This skill never collects AD data itself — it reviews data that was already collected through approved, out-of-band means.

## Required inputs

- User-provided BloodHound JSON/ZIP export, SharpHound output, LDAP query results, or equivalent AD graph data. The data must have been collected through a separately authorized process.
- Written scope naming the domain, forests, organizational units, approved data sources, and review boundaries. Scope must be explicit that active AD collection was separately authorized.
- Explicit confirmation that no credential capture, cracking, relay, coercion, lateral movement, or persistence is within scope of this review.
- Known detection/escalation contact for any findings that suggest immediate remediation priority.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`. The target here is the domain/forest under review, not a live host to probe.
3. `pentest_agent_check_authorization` — must confirm authorization covers data review, not active collection.
4. No `pentest_agent_execute_tool` calls that touch live AD infrastructure. Catalog tools for data analysis (Neo4j Cypher querying, JSON parsing) may be used locally if pre-approved.
5. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — data intake and validation

1. Confirm the data source, collection date, collector identity, and collection scope match the authorization record.
2. Validate that the data file does not contain raw credentials, plaintext passwords, Kerberos tickets, NTLM hashes, or private keys. If it does, redact immediately and notify the user — do not store or analyze unredacted credential material.
3. Extract high-level statistics: domain count, user count, computer count, group count, privileged group membership size, delegation configuration summary.
4. Identify the data freshness. Data older than 30 days should carry a staleness warning in all findings.

### Phase 2 — privilege escalation path discovery

Analyze the graph for attack paths to high-value targets:
- **Shortest paths to Domain Admins**: from every non-privileged user, find paths ≤ 3 hops. Flag any path that exists.
- **Paths to other privileged groups**: Enterprise Admins, Schema Admins, Backup Operators, Account Operators, Server Operators.
- **ACL-based escalation**: GenericAll, GenericWrite, WriteDacl, WriteOwner, ForceChangePassword, AddMember edges that allow a lower-privilege principal to control a higher-privilege principal.
- **DCSync rights**: any principal with Replication-Get-Changes / Replication-Get-Changes-All on the domain object.

### Phase 3 — delegation and session risk

- **Unconstrained delegation**: computers with `TrustedForDelegation` flag — any ticket sent to these can be captured and reused.
- **Constrained delegation**: services allowed to impersonate users to specific target services. Flag risky target services (LDAP on DC, CIFS on DC, HTTP on high-value servers).
- **Resource-based constrained delegation**: computers where a lower-privilege principal can write `msDS-AllowedToActOnBehalfOfOtherIdentity`.
- **DA sessions**: Domain Admin sessions on non-tier-0 computers — these computers are credential-theft targets.
- **Kerberoastable accounts**: accounts with SPNs. Flag those with `adminCount=1` (highest risk) and those with old encryption types (RC4).

### Phase 4 — tiering and group hygiene

- **Tier-0 boundary violations**: non-tier-0 accounts with admin access to tier-0 assets.
- **Nested group membership**: users reaching DA through indirect group nesting (≥ 3 levels deep).
- **Foreign security principals**: cross-forest principals with privileged access in the target domain.
- **Disabled accounts with privileged group membership**.
- **Stale privileged accounts**: adminCount=1 users with no recent logon.
- **Service accounts in privileged groups**: SPN accounts directly in DA or equivalent.

### Phase 5 — remediation roadmapping

For each finding class, produce a remediation recommendation:
1. **Path elimination**: specific ACL removals, group membership changes, or delegation resets.
2. **Detection guidance**: Windows Event IDs, Sysmon rules, or SIEM queries that would detect exploitation of each path.
3. **Priority ordering**: sort by (blast radius × exploitability) / remediation effort.

## Decision points

- **Recommend active validation only when**: the finding is high-severity, the path is fully understood from graph data, and active validation would use read-only LDAP queries with explicit scope approval. Never recommend credential capture, cracking, or lateral movement from this skill.
- **Escalate to blue-team handoff**: all findings should be packaged for the defensive team — include detection rules, not exploitation steps.
- **Stop on credential exposure**: if analyzed data contains hashes, tickets, or passwords, redact, notify user, and stop analysis of that data subset.

## Prohibited behavior

- Collecting AD data, running SharpHound/BloodHound collectors, or executing any LDAP/SMB/Kerberos queries against live domain controllers.
- Requesting Kerberos tickets, cracking hashes, relaying authentication, or dumping credentials — even for "validation."
- Providing lateral movement steps, credential attack recipes, or persistence techniques.
- Storing unredacted graph data containing user principal names, group memberships, or computer names in evidence unless scope explicitly allows it.
- Recommending active attack paths without also providing the equivalent detection rule and remediation.

## Stop conditions

- Analyzed data contains raw hashes, tickets, passwords, or private keys → redact, notify, stop.
- Finding requires active credential attack to validate → downgrade to policy-only recommendation.
- Data source, collection method, or authorization cannot be confirmed → stop, ask user to verify.

## Evidence

Append analysis summary per finding class:

```text
Finding class: <shortest DA path | ACL escalation | unconstrained delegation | kerberoastable admin | tier violation>
Severity: <critical | high | medium | low>
Affected principals: <count + representative examples, redacted if needed>
Path summary: <source → edge type → ... → target>
Detection guidance: <event IDs | SIEM query | Sysmon rule>
Remediation: <specific ACL/group/delegation change>
Data freshness: <collection date> | staleness warning: <yes | no>
```

Redact all hashes, tickets, passwords, user principal names (unless scope allows), and internal hostnames (unless scope allows). Hash-format data should be replaced with `[REDACTED-HASH]`.

## Report handoff

1. `pentest_agent_record_finding` for each confirmed privilege escalation path, delegation risk, or tiering violation.
2. Package findings for both remediation team (what to fix) and detection team (how to detect).
3. Include data freshness caveat and collection method in every finding.
4. Recommend: tiering model enforcement, privileged access workstation rollout, delegation cleanup, regular BloodHound review cadence, and detection rule deployment.
