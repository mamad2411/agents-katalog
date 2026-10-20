---
name: proto-snmp
description: SNMP exposure and configuration review for scoped network devices — version detection (v1/v2c/v3), community-string scope audit (read-only test with approved strings only), MIB-walk boundary assessment, encryption/auth posture for SNMPv3, and write-access detection. No community-string brute force, SNMP write, or bulk MIB dump.
disable-model-invocation: true
risk: caution
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# SNMP assessment — safe exposure and configuration review

Use this skill to review authorized SNMP services for version exposure, community-string posture (read-only audit with approved strings only), MIB-walk boundary enumeration, SNMPv3 encryption/auth configuration, and write-access detection — without community-string brute force, SNMP write, bulk MIB dump, or device reconfiguration. All checks use only community strings or credentials explicitly provided in scope. Never guess community strings, bulk-walk sensitive OID trees, or modify SNMP values.

## Required inputs

- Written scope naming authorized SNMP hosts, UDP port (default 161, plus 162 for traps if in scope), allowed SNMP versions, approved read-only community strings or SNMPv3 credentials, allowed OID branches for enumeration, rate limits, and testing window.
- Explicit permission for SNMP enumeration using the provided community strings. Do NOT use well-known defaults (`public`, `private`, `community`, `admin`, `manager`) unless they are explicitly listed in the scope as the configured community strings.
- Explicit permission for MIB-walk or bulk OID enumeration. Without this, only `sysDescr` (OID .1.3.6.1.2.1.1.1.0) and `sysObjectID` queries are allowed.
- Valid authorization cache for each SNMP host.
- List of prohibited OID branches: never query OID trees containing credentials, cryptographic keys, user passwords, SNMPv3 user tables, or device configuration that may contain secrets.
- Separate disabled-default approval before any community-string brute force, SNMP write operations, SNMPv3 credential cracking, or device reconfiguration.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target` for each SNMP host.
3. `pentest_agent_check_authorization` before any active SNMP query.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools (nmap, snmpwalk, snmpget, onesixtyone) are used.
5. `pentest_agent_execute_tool` for all execution.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — service discovery and version fingerprinting

1. Confirm SNMP port is open:
   - UDP port 161 (SNMP agent), UDP port 162 (SNMP traps — notification receiver). SNMP is UDP-based, so port scanning is slower and less reliable.
   - `nmap -sU -p 161,162 --open <host>` through `pentest_agent_execute_tool`. Use `--host-timeout` and rate-limit to avoid UDP scan flood.
2. SNMP version and basic system identification:
   - Only if a community string is explicitly provided in scope: `snmpget -v2c -c <community> <host> sysDescr.0 sysObjectID.0 sysUpTime.0 sysContact.0 sysName.0 sysLocation.0`.
   - This queries the system group (MIB-2) and identifies the device type, vendor, OS, and configured contact/location.
   - Record: device description, vendor, OS version, uptime, contact, name, location.
   - Flag: `sysContact` or `sysLocation` revealing internal personnel or physical locations → low finding (information disclosure).
   - Flag: `sysDescr` revealing detailed OS version, patch level, or hardware model → low finding (fingerprinting aid).
3. If no community string is provided, stop at port confirmation. Do NOT test default community strings unless explicitly listed in scope.
4. If the scope provides SNMPv3 credentials, query: `snmpget -v3 -l authPriv -u <user> -a SHA -A <auth-pass> -x AES -X <priv-pass> <host> sysDescr.0`.

### Phase 2 — SNMP version posture assessment

1. Determine which SNMP versions the host responds to:
   - SNMPv1 and SNMPv2c use community strings for authentication (no encryption, no user authentication). The community string is transmitted in cleartext.
   - SNMPv3 supports user-based authentication (MD5/SHA) and encryption (DES/AES).
2. If the host responds to SNMPv1/v2c queries → medium finding. These versions transmit all data (including community strings) in cleartext and offer no cryptographic integrity protection. SNMPv3 should be enforced for any device handling sensitive configuration data.
3. If the host also responds to SNMPv3 → positive control, but verify encryption:
   - `noAuthNoPriv` (no authentication, no encryption) → equivalent to v2c security. Medium finding.
   - `authNoPriv` (authentication, no encryption) → better, but data is still in cleartext. Low/medium finding.
   - `authPriv` (authentication + encryption) → positive control. AES-128 minimum, AES-256 preferred.
4. Flag deprecated algorithms in SNMPv3: MD5 authentication (use SHA-256), DES encryption (use AES).

### Phase 3 — MIB enumeration boundary assessment

Only if scope provides approved community strings/credentials and explicitly permits MIB enumeration:

1. Query the system group (safe metadata):
   - `snmpwalk -v2c -c <community> <host> system` — enumerates the system MIB (sysDescr, sysObjectID, sysUpTime, sysContact, sysName, sysLocation, sysServices).
   - This is the safest OID tree to query. It provides device identification without configuration exposure.
2. Query network interfaces (limited):
   - `snmpwalk -v2c -c <community> <host> ifDescr` — lists interface names.
   - `snmpwalk -v2c -c <community> <host> ifAdminStatus` — interface administrative status (up/down).
   - `snmpwalk -v2c -c <community> <host> ifOperStatus` — interface operational status.
   - Do NOT query `ifInOctets`, `ifOutOctets`, or other traffic counters unless scope permits — these reveal traffic volume data.
3. Query IP address table (limited):
   - `snmpwalk -v2c -c <community> <host> ipAdEntAddr` — lists IP addresses configured on the device.
   - `snmpwalk -v2c -c <community> <host> ipAdEntNetMask` — subnet masks.
   - Flag: IP addresses belonging to out-of-scope subnets → record observation but do NOT probe those subnets further.
4. Query routing table (only if scope explicitly permits):
   - `snmpwalk -v2c -c <community> <host> ipRouteDest` — route destinations. This can reveal internal network topology.
   - Limiting to first 20 entries is recommended. Do NOT dump the full routing table unless scope authorizes.
5. Do NOT query:
   - `hrSWRunName` (running processes) — reveals software inventory and potential vulnerable services.
   - `hrSWInstalledName` (installed software) — detailed software inventory.
   - User account tables, SNMPv3 user tables, community-string tables.
   - `tcpConnTable` / `udpTable` (active connections) — reveals live communication patterns.
   - Any Cisco-specific credential OIDs, configuration OIDs, or VPN-related MIBs.
6. For all enumeration, limit to 100 OIDs per query tree. Do NOT run unrestricted `snmpwalk .` (full MIB walk) unless scope explicitly authorizes a complete device inventory.

### Phase 4 — access control and write-access detection

1. Determine read vs. read-write community strings:
   - Provided community strings should be read-only. If scope provides a separate read-write community string, it is for detection only — do NOT use it for write operations.
   - To test if a community string has write access, query a safe writable OID. Do NOT actually write.
   - Use `snmpset` dry-run detection (if tool supports `-d` dump mode) or query a status OID with `snmpset -v2c -c <community> <host> sysContact.0 s "test"` — only if scope explicitly permits write-access detection and the test value being written is clearly non-destructive.
   - Without explicit scope permission, do NOT attempt any `snmpset` operation. Assume the provided string is read-only.
2. If write access is detected:
   - Critical finding — write access via SNMP allows device reconfiguration, denial-of-service, and potentially credential extraction.
   - Do NOT demonstrate write access by modifying any value. Record the capability as a finding.
3. Access control check:
   - SNMP should use access control lists (ACLs) to restrict which management stations can query the device. This is a server-side configuration — you can infer it if queries from one source IP succeed and another fail.
   - If no ACL is in place (queries from any IP succeed with the community string) → medium finding. Recommend restricting SNMP access to specific management IPs.

### Phase 5 — hardening assessment

1. **SNMP version**: SNMPv3 `authPriv` preferred. SNMPv1/v2c → medium finding (upgrade to v3).
2. **Community strings**: should not be the default `public`/`private`. If the provided strings are defaults → high finding.
3. **Encryption**: SNMPv3 with AES-256 and SHA-256 → positive. DES/MD5 → medium finding (weak algorithms).
4. **Access control**: SNMP should be restricted to authorized management stations via ACLs. No ACL → medium finding.
5. **Exposure**: SNMP (UDP 161) should never be exposed to the Internet. If the host has a public IP and SNMP is accessible → high/critical finding.
6. **Read-only vs read-write**: community strings should be read-only unless write access is strictly required and protected by ACLs and monitoring. Write access → high/critical finding.
7. **Sensitive OID exposure**: check if sensitive OID trees are blocked via SNMP views. If a full `system` MIB is accessible, that's normal. If process tables, user tables, or configuration OIDs are accessible, flag as medium/high finding.
8. **SNMP trap configuration**: SNMP traps (UDP 162) should be sent only to authorized management stations. Trap receivers are discoverable via `snmpTargetAddrTable` if readable — do NOT query this table unless scope explicitly permits.

## Decision points

- **Write access detected**: critical finding — device can be reconfigured via SNMP. Immediately notify operator. Do NOT write any value.
- **SNMPv1/v2c with default community string**: critical finding — trivial to enumerate and potentially reconfigure.
- **SNMP exposed to Internet**: critical finding — SNMP should never be Internet-accessible.
- **Process or user tables accessible via SNMP**: high finding — detailed system/account inventory exposed.
- **SNMPv3 with noAuthNoPriv**: medium finding — equivalent security to v2c. Upgrade to authPriv.
- **Read-only access with non-default community string**: low finding — operational best-practice is to use SNMPv3, but v2c with a strong community string and ACLs is common.
- **Proceed to MIB-walk**: only if scope explicitly authorizes full or limited MIB enumeration with specific OID boundaries.
- **Downgrade to port/system check only**: when no community strings are provided. Record port status and stop.

## Prohibited behavior

- Community-string brute force (`onesixtyone`, `hydra snmp`) — disabled-default. Only use strings explicitly provided in scope.
- SNMP write (`snmpset` modifying any value) — prohibited. Write-access detection should be passive or use safe read-only queries to infer access level.
- Full MIB walk (`snmpwalk .`) without explicit scope authorization and explicit OID boundaries — prohibited.
- Querying credential-related OIDs: SNMPv3 user tables (`usmUserTable`), community-string tables, Cisco VPN credentials, any OID containing passwords or keys.
- Querying process tables (`hrSWRunName`, `hrSWRunPath`), installed software tables, or connection tables without explicit authorization — these reveal detailed system internals.
- Bulk enumeration with high rate (flooding the device with SNMP requests) — rate-limit to maximum 10 queries per second. SNMP is UDP and easily overwhelms network devices.
- Using SNMP to retrieve device configuration for cloning or unauthorized access.

## Stop conditions

- Server does not respond to SNMP queries (port filtered or SNMP disabled) → stop, record as positive control.
- Provided community string returns `No response` or `Timeout` consistently → the string is likely incorrect or the device has ACLs blocking the query source. Do NOT guess strings.
- Query returns data that appears to contain credentials, passwords, or authentication tokens → stop querying that OID tree, redact output immediately, alert operator.
- Device shows signs of CPU or memory pressure from SNMP queries → stop and reduce query rate. SNMP is low-priority on many devices and can cause service degradation.
- Evidence would include internal IPs, routing tables, or network topology beyond scope → redact and stop.

## Evidence — SNMP service record

For each authorized SNMP host:

```text
Host: <host> (hash if redaction required)
Port: 161/UDP (open), 162/UDP (filtered)

Device identification:
  sysDescr: Cisco IOS Software, Version 17.3.5, RELEASE SOFTWARE (fc2)
  sysObjectID: .1.3.6.1.4.1.9.1.XXXX
  Vendor: Cisco Systems
  sysUpTime: 45 days 03:22:15.00
  sysContact: noc@example.com (redacted if PII concern)
  sysName: core-sw-01.example.com
  sysLocation: Datacenter Floor 3, Rack 12

SNMP versions:
  v1: responds
  v2c: responds (primary)
  v3: not available (medium finding — upgrade to v3 authPriv)

Community string: <non-default, provided in scope — hash redacted>
Access level: read-only (confirmed by inability to access read-write OIDs)

MIB enumeration (authorized, limited):
  System group: accessible (normal)
  Interfaces: ifDescr accessible — 48 ports (expected for switch)
  IP addresses: ipAdEntAddr accessible — 3 IPs (management, VLAN2, VLAN10)
  Routing table: not queried (explicitly excluded)
  Process table: not queried (explicitly excluded)
  Sensitive OIDs: no credential/configuration OIDs observed in limited walk

Exposure:
  Internet-accessible: no (internal IP 10.x.x.x)
  ACL: restricted to management subnet (10.x.x.0/24) — inferred from successful query
  Write access: no (positive)

Findings:
  [MEDIUM] SNMPv1/v2c in use — no encryption or authentication integrity. Upgrade to SNMPv3 authPriv.
  [LOW] sysContact reveals internal email address
  [INFO] Read-only access — positive control
  [INFO] ACL restricted to management subnet — positive control
  [INFO] No sensitive OIDs observed — positive
```

Aggregate into an SNMP security posture summary per host. Include: device identification, SNMP version support, community-string posture, access control, MIB exposure boundary, write-access status, and recommended hardening.

Never store: community strings (even hashed, unless the hash is required for authorization cache — store separately in auth cache, not in evidence), SNMPv3 user credentials, auth/priv keys, IP routing tables if out-of-scope, process listings, user account tables, or any raw MIB walk output containing configuration data.

## Report handoff

1. `pentest_agent_record_finding` for each confirmed weakness: default community string, write access, SNMPv1/v2c without v3 migration, Internet exposure, MIB process/user data exposure, missing ACLs, weak SNMPv3 algorithms (DES, MD5).
2. Package findings with the device's overall SNMP security grade: version posture, access-control posture, encryption posture, and exposure score.
3. Recommend: migrate to SNMPv3 authPriv with AES-256/SHA-256, replace default community strings with strong random strings (if staying on v2c), configure SNMP ACLs to restrict queries to authorized management stations, implement SNMP views to limit accessible OID trees, block SNMP (UDP 161/162) at the Internet perimeter, audit for write-access community strings and eliminate unless strictly required, enable SNMP trap authentication, and implement SNMP monitoring for unauthorized queries.
4. Explicitly note that no community-string brute force, no `snmpset` write operations, no full MIB walk, and no credential/configuration harvesting was performed — only safe SNMP system identification and access-control review using provided credentials.
