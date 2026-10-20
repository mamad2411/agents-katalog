---
name: internal-network-assessment
description: Internal network assessment planning and low-impact validation — scope-bound CIDR/host enumeration, service discovery, AD read-only enumeration, BloodHound-safe review, and passive network mapping with strict no-scan-expansion, no-credential-attack, and no-lateral-movement boundaries.
disable-model-invocation: true
risk: caution
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft, network-map]
---

# Internal network assessment — planning and low-impact validation

Use this skill for authorized internal network assessment on explicitly scoped CIDR ranges, VLANs, or host lists. Perform read-only discovery, service enumeration, Active Directory read-only enumeration, and passive network mapping. All probes are low-rate and scope-bound. Never expand scanning beyond the authorized subnet, run aggressive port scans against production hosts, exploit discovered services, use captured credentials for lateral movement, or attempt credential attacks — those behaviors are prohibited unless separately approved and the relevant disabled-default categories are unlocked.

## Required inputs

- Written scope defining exact CIDR ranges, host lists, VLAN IDs, excluded hosts/subnets, allowed probe types, rate limits, testing window, and prohibited methods.
- Explicit confirmation that scanning expansion, credential attacks, lateral movement, service exploitation, SMB relay, Kerberoasting, AS-REP roasting, password spraying, and NTLM-relay attacks are prohibited unless separately approved for destructive validation.
- Network topology context: whether the assessment is on a lab network, production segment, isolated VLAN, or full internal network. Production networks require stricter rate limits and explicit host exclusions.
- Valid authorization cache for the target CIDR range or enumerated hosts.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target` (validate every CIDR, host, and VLAN against scope).
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview — inject rate-limit args from scope metadata.
5. `pentest_agent_execute_tool` for read-only execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — scope validation and host discovery planning

1. Normalize the CIDR ranges from scope: verify that the provided subnets, host lists, and VLAN boundaries are machine-parseable. If scope is free-text, extract IP ranges conservatively and flag any ambiguous entries for operator review.
2. Confirm excluded hosts and subnets: out-of-scope targets within the CIDR range must be explicitly excluded before any scanning begins. If scope lists "all hosts in 10.0.1.0/24 except 10.0.1.1, 10.0.1.5", those exclusions must be mapped into the scanning tool configuration.
3. Set rate-limit parameters: production networks require conservative timing (`--min-rate 100` or lower, `--max-retries 1`, `-T2` or `-T3`). Lab networks may allow faster rates if scope permits. Record the rate-limit decisions.
4. Validate all scan targets against scope: every IP, hostname, CIDR block, and service must be within the authorized scope. If host discovery reveals hosts that were not in the original scope, do not add them to the scan — flag them for operator review.

### Phase 2 — host discovery (ARP and ICMP)

1. Perform ARP-based host discovery for local network segments where the testing machine has Layer 2 adjacency. ARP is the fastest and most reliable discovery method and generates minimal noise. Use catalog tools with `-sn` flag for ping sweep.
2. For non-adjacent segments (across routers), use ICMP echo and TCP SYN discovery on common ports (80, 443, 22, 445, 139, 3389). ICMP-only discovery may miss hosts that block ICMP but have open TCP services.
3. Record discovered hosts: MAC addresses (for local segments), IP addresses, and whether the host responded to ARP, ICMP, or TCP. Do not perform OS fingerprinting during discovery — defer to Phase 3.
4. Do not use broadcast or multicast discovery techniques beyond standard ARP unless explicitly approved. Do not send malformed packets or use fragmentation-based evasion.

### Phase 3 — port and service discovery (read-only)

1. For each discovered host, perform TCP port scanning on a limited port set: start with the top 100-200 most common ports unless scope specifies full port range (1-65535). Full port scans on production networks require explicit approval.
2. For each open port, perform service version detection: banner grabbing, service-probe responses, and TLS certificate inspection. Record service name, version, and any version-specific vulnerabilities from the catalog.
3. Check for common internal services: SMB (139/445), LDAP (389/636), RDP (3389), SSH (22), databases (1433 MSSQL, 3306 MySQL, 5432 PostgreSQL, 27017 MongoDB, 6379 Redis), HTTP/HTTPS (80/443/8080/8443/8000/3000), printers (9100/515/631), and SNMP (161).
4. Do not perform UDP scanning on production networks without explicit approval — UDP scans are slow, unreliable, and can trigger IDS alerts. Do not perform service exploitation or version-specific attack scripts.
5. Record all discovered services with version evidence and open ports.

### Phase 4 — Active Directory read-only enumeration

1. Identify domain controllers from service discovery: LDAP (389/636), Kerberos (88), and global catalog (3268/3269) indicate Windows domain controllers. Check SMB service on potential DCs for `SYSVOL` and `NETLOGON` shares.
2. Perform anonymous/read-only LDAP enumeration: query the RootDSE for `namingContexts`, `defaultNamingContext`, `supportedLDAPVersion`, and `domainControllerFunctionality`. This requires no credentials and reveals domain structure, functional level, and forest topology.
3. If scope permits and credentials are provided, enumerate domain users, groups, computers, and service principal names (SPNs). SPN enumeration reveals service accounts — record these but do not request Kerberos service tickets (TGS) unless Kerberoast validation is separately approved and scope-allowed.
4. If BloodHound collector tools are available and scope permits read-only collection, run BloodHound data collection with provided credentials. BloodHound maps Active Directory attack paths by enumerating users, groups, computers, ACLs, sessions, and trust relationships. This is a read-only operation that generates query traffic — confirm the domain controller can handle the query load.
5. Review BloodHound output for attack-path visibility but do not exploit any path. Record high-value targets, privilege-escalation vectors, and misconfigurations as findings.
6. Do not run credential attacks, password spraying, Kerberoasting (TGS-REQ with offline cracking), AS-REP roasting, DCSync, NTLM relay, or token-manipulation attacks.

### Phase 5 — internal web and API discovery

1. Identify HTTP/HTTPS services from service discovery. Probe each web service for: HTTP title, status code, redirect behavior, server/technology headers, and whether authentication is required.
2. Check for internal web applications: development servers, staging environments, admin panels, monitoring dashboards (Grafana, Kibana, Prometheus), CI/CD tools (Jenkins, GitLab, Drone), and internal wikis/documentation platforms.
3. Record application URLs, technology stacks, and authentication requirements. Note applications that use default credentials or no authentication — flag as findings but do not attempt login.
4. Check for cleartext HTTP services transmitting sensitive data: internal applications that use HTTP instead of HTTPS may expose tokens, credentials, or session identifiers on the network segment.
5. Do not test authentication bypass, SQL injection, XSS, or any active web-application testing unless separately approved through web-application scope and the vulnerability validation skills. This skill covers discovery and mapping only.

### Phase 6 — database and storage service discovery

1. Identify database services from port scanning. For each database service, record the type, version, and whether authentication is required.
2. Test anonymous/empty-password access on databases where scope permits read-only connection testing: MongoDB without auth, Redis without `requirepass`, MySQL/MariaDB anonymous users, and PostgreSQL `trust` authentication. A successful anonymous connection is a high finding — record the database type and whether data was visible, but do not enumerate tables, query data, or extract information beyond confirming access.
3. Check for database administration interfaces: phpMyAdmin, pgAdmin, MongoDB Express, Redis Commander. These are web-based database management tools often deployed without authentication on internal networks.
4. Do not dump database contents, modify data, or create users even if anonymous access is confirmed.

## Decision points

- **Escalate on anonymous LDAP access exposing domain structure**: full AD tree visible without credentials → high information-disclosure; enables targeted attacks.
- **Escalate on critical service with default/empty credentials**: database, admin console, or network device with no authentication → high; critical if the service contains production data.
- **Escalate on production database without authentication**: MongoDB/Redis/Elasticsearch accessible without credentials → critical.
- **Escalate on exposed management interfaces without auth**: Grafana, Kibana, Jenkins, or monitoring dashboards → high.
- **Escalate on cleartext credentials in internal HTTP traffic**: basic-auth or form-login over HTTP → high.
- **Escalate on SMB shares with anonymous read access**: `IPC$`, `SYSVOL`, or custom shares readable without credentials → high.
- **Downgrade on open HTTP port without sensitive data exposure**: informative — internal hardening gap.
- **Downgrade on SNMP public community string readable**: informative unless sensitive OIDs are exposed.

## Prohibited behavior

- Expanding scan scope beyond authorized CIDR ranges, VLANs, or host lists.
- Running aggressive Nmap NSE scripts (`smb-vuln-*`, `http-sql-injection`, `dns-zone-transfer`) without explicit approval.
- Performing credential attacks: password spraying, Kerberoasting, AS-REP roasting, DCSync, NTLM relay, pass-the-hash, or token manipulation.
- Exploiting discovered services: no SQL injection, command injection, RCE exploitation, or configuration modification.
- Using captured or discovered credentials for lateral movement or privilege escalation.
- Exploiting anonymous database access to dump or modify data.
- Enumerating SMB shares or LDAP directories beyond confirming read access.
- Downloading files from exposed shares or internal web applications.

## Stop conditions

- Host discovery reveals out-of-scope hosts → flag but do not scan; exclude from all subsequent phases.
- Anonymous database access confirmed on production system → stop, high/critical finding, do not enumerate data.
- Credential-less access to domain controller administrative shares → stop, critical finding.
- Service version indicates a known critical RCE vulnerability → stop, record finding, do not exploit.
- Scan rate triggers IDS/IPS alerts or network congestion → stop, reduce rate or wait for approved window.
- Evidence contains credentials, tokens, PII, or database contents → redact immediately.

## Evidence — internal network assessment matrix

For each engagement, record:

```text
Engagement: <scope hash> | Mode: <mode>
Scope: <CIDR ranges, host lists, VLANs>
Exclusions: <hosts/subnets explicitly excluded>
Rate limits applied: <min-rate, max-retries, timing template>
Testing window: <hours allowed | unrestricted>

Host discovery:
  Hosts discovered: <count>
  Discovery method: <ARP | ICMP | TCP-SYN | mixed>
  Out-of-scope hosts flagged: <count>

Service discovery:
  Hosts with open ports: <count>
  Common services found: <SMB count, LDAP count, HTTP count, DB count, RDP count, SSH count>
  Domain controllers identified: <count — hostnames/IPs>
  Critical services (default/empty auth): <count — types>

Active Directory:
  Anonymous LDAP access: <yes — domain info exposed | no>
  Domain functional level: <level>
  BloodHound collection run: <yes — findings count | no — not authorized>
  SPN accounts discovered: <count>
  High-value targets from BloodHound: <count — types>

Internal web:
  HTTP/HTTPS services: <count>
  Admin/management interfaces: <count — types>
  Services without authentication: <count — URLs>

Database:
  Database services: <count>
  Anonymous access confirmed: <count — types>
  DB admin interfaces: <count — URLs>

Overall risk: <critical | high | medium | low>
```

Never store: raw LDAP query results with user/group names, BloodHound JSON with full ACL/Session graph, database connection strings or contents, SMB share file listings with sensitive filenames, cleartext credentials or session tokens, or internal hostname-to-IP mappings in full detail (hash or summarize).

## Report handoff

1. `pentest_agent_record_finding` for: anonymous LDAP access exposing domain structure, exposed management interfaces without auth, databases with anonymous/empty-password access, SMB shares with anonymous read, cleartext services transmitting credentials, default/empty credentials on infrastructure services, SNMP with public community string, and critical vulnerability indicators on exposed services.
2. Reference the internal network assessment matrix.
3. Recommend: segment the network so production, development, and management interfaces are on separate VLANs; enforce 802.1X or NAC for network access; require authentication on all databases, management interfaces, and admin panels; disable anonymous LDAP binding on domain controllers; apply SMB signing and disable SMBv1; use LDAPS (LDAP over TLS) and require channel binding; restrict SNMP to read-only with strong community strings or SNMPv3; enable firewall rules to limit service exposure to authorized segments only; and rotate credentials on any service found with default authentication.
