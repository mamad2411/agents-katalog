---
name: Data Source Mapper
description: Map MITRE ATT&CK techniques to required data sources across Windows, Linux, cloud, network, and EDR telemetry. Includes CIM, ECS, Sigma, and KQL (Sentinel) field mapping comparisons.
---

# Data Source Mapper Skill

## Configuration

- `$SIEM_PLATFORM` - Target SIEM: `splunk`, `sentinel`, `elastic`, `sigma`
- `$SECURITY_CONTENT_PATH` - Path to detection content repository

## Overview

Every detection rule depends on specific telemetry. This skill maps ATT&CK techniques to the data sources that make detection possible, and compares field naming across common schemas (Splunk CIM, Elastic ECS, Sigma, and Sentinel/MDE).

## Data Source Catalog

### Windows Endpoint

| Data Source | Key Events | Detects | Collection Method |
|-------------|-----------|---------|-------------------|
| **Windows Security Events** | 4688 (Process), 4624/4625 (Logon), 4672 (Privileges) | Execution, Credential Access, Lateral Movement | Windows Event Forwarding, Splunk UF, Winlogbeat |
| **Sysmon** | 1 (Process), 3 (Network), 7 (Image Load), 11 (File Create), 13 (Registry) | Nearly all endpoint techniques | Sysmon + log forwarder |
| **PowerShell Logging** | 4104 (Script Block), 4103 (Module), 800/600 (Classic) | T1059.001, T1546.013, obfuscation | GPO: Script Block Logging |
| **WMI Trace** | WMI-Activity/Operational | T1047, T1546.003 | Built-in ETW provider |
| **Windows Defender** | 1116 (Detection), 1117 (Action) | Malware execution attempts | Windows Event Log |
| **ETW Providers** | Microsoft-Windows-DNS-Client, etc. | DNS, TLS, RPC activity | Custom ETW collection |

### Linux Endpoint

| Data Source | Key Events | Detects | Collection Method |
|-------------|-----------|---------|-------------------|
| **auditd** | SYSCALL, EXECVE, PATH, USER_AUTH | Execution, File Access, Auth | auditd rules + forwarder |
| **syslog** | auth.log, secure, messages | Authentication, sudo, cron | rsyslog/syslog-ng |
| **journald** | SystemD unit events | Service persistence, execution | journalctl export |
| **osquery** | Scheduled queries | File integrity, process, network | osquery daemon |
| **eBPF** | Process, file, network events | Fine-grained kernel telemetry | Cilium Tetragon, Tracee |

### Cloud

| Data Source | Key Events | Detects | Collection Method |
|-------------|-----------|---------|-------------------|
| **AWS CloudTrail** | API calls (Management + Data events) | IAM abuse, resource manipulation | S3 → log forwarder |
| **AWS GuardDuty** | Threat findings | Recon, credential compromise | EventBridge → SIEM |
| **Azure Activity Log** | ARM operations | Resource changes | Diagnostic Settings |
| **Azure AD Sign-in Logs** | Sign-in events, MFA | Credential abuse, brute force | Diagnostic Settings |
| **GCP Audit Logs** | Admin Activity, Data Access | IAM, resource access | Log Router → SIEM |
| **O365 Unified Audit Log** | Mail, SharePoint, Teams | BEC, data exfiltration | Management API |

### Network

| Data Source | Key Events | Detects | Collection Method |
|-------------|-----------|---------|-------------------|
| **Zeek** | conn.log, dns.log, http.log, ssl.log, files.log | C2, exfil, lateral movement | Network tap / span port |
| **Suricata** | alert, flow, dns, http, tls | Known signatures + protocol anomalies | Inline or passive |
| **DNS Logs** | Query/response | C2 over DNS, DGA | DNS server logs, passive DNS |
| **Firewall Logs** | Allow/deny, NAT | Lateral movement, exfil | Syslog from firewall |
| **Proxy / WAF Logs** | HTTP requests, URL categories | Web-based C2, initial access | Proxy log export |
| **NetFlow / IPFIX** | Flow records | Volume anomalies, beaconing | Router/switch export |

### EDR / XDR

| Data Source | Key Events | Detects | Collection Method |
|-------------|-----------|---------|-------------------|
| **CrowdStrike Falcon** | ProcessRollup2, NetworkConnect, DnsRequest | Broad endpoint coverage | Falcon Data Replicator (FDR) |
| **Microsoft Defender for Endpoint** | DeviceProcessEvents, DeviceNetworkEvents | Broad endpoint coverage | Streaming API or Sentinel |
| **SentinelOne** | Process, File, Network telemetry | Broad endpoint coverage | API export |
| **Carbon Black** | Process, Netconn, Filemod | Broad endpoint coverage | Event Forwarder |

## Field Mapping Comparison: CIM vs ECS vs Sigma vs Sentinel

The same telemetry is named differently across schemas. This table maps common fields across all four platforms.

### Process Creation Fields

| Concept | Splunk CIM | Elastic ECS | Sigma (Generic) | Sentinel / MDE (KQL) |
|---------|-----------|-------------|-----------------|---------------------|
| Process name | `process_name` | `process.name` | `Image` | `FileName` |
| Command line | `process` | `process.command_line` | `CommandLine` | `ProcessCommandLine` |
| Process ID | `process_id` | `process.pid` | `ProcessId` | `ProcessId` |
| Parent process name | `parent_process_name` | `process.parent.name` | `ParentImage` | `InitiatingProcessFileName` |
| Parent command line | `parent_process` | `process.parent.command_line` | `ParentCommandLine` | `InitiatingProcessCommandLine` |
| User | `user` | `user.name` | `User` | `AccountName` |
| Hostname | `dest` | `host.name` | `Computer` | `DeviceName` |
| File hash (SHA256) | `process_hash` | `process.hash.sha256` | `Hashes` | `SHA256` |
| Timestamp | `_time` | `@timestamp` | N/A | `Timestamp` |

### Network Connection Fields

| Concept | Splunk CIM | Elastic ECS | Sigma | Sentinel / MDE (KQL) |
|---------|-----------|-------------|-------|---------------------|
| Source IP | `src` | `source.ip` | `SourceIp` | `LocalIP` |
| Destination IP | `dest` | `destination.ip` | `DestinationIp` | `RemoteIP` |
| Destination port | `dest_port` | `destination.port` | `DestinationPort` | `RemotePort` |
| Protocol | `transport` | `network.transport` | `Protocol` | `Protocol` |
| Bytes out | `bytes_out` | `source.bytes` | N/A | `SentBytes` |
| Application | `app` | `network.application` | N/A | N/A |

### File Activity Fields

| Concept | Splunk CIM | Elastic ECS | Sigma | Sentinel / MDE (KQL) |
|---------|-----------|-------------|-------|---------------------|
| File path | `file_path` | `file.path` | `TargetFilename` | `FolderPath` |
| File name | `file_name` | `file.name` | `TargetFilename` | `FileName` |
| File hash | `file_hash` | `file.hash.sha256` | `Hashes` | `SHA256` |
| Action | `action` | `event.action` | N/A | `ActionType` |

### Key Sentinel / MDE Tables

| Table | Data Source | Use For |
|-------|-----------|---------|
| `DeviceProcessEvents` | MDE agent | Process creation and execution |
| `DeviceNetworkEvents` | MDE agent | Network connections |
| `DeviceFileEvents` | MDE agent | File creation, modification, deletion |
| `DeviceRegistryEvents` | MDE agent | Registry modifications |
| `DeviceLogonEvents` | MDE agent | Authentication events |
| `SecurityEvent` | Azure Monitor Agent (legacy) | Windows Security Event Log |
| `Syslog` | Azure Monitor Agent | Linux syslog |
| `SigninLogs` | Azure AD connector | Azure AD authentication |
| `AuditLogs` | Azure AD connector | Azure AD administrative changes |

## Technique to Data Source Mapping

### High-Priority Techniques

| Technique | Required Data Source(s) | Minimum Viable |
|-----------|------------------------|----------------|
| T1059.001 (PowerShell) | PowerShell 4104 + Sysmon 1 | PowerShell 4104 alone |
| T1059.003 (cmd.exe) | Sysmon 1 / Security 4688 | Security 4688 with cmd logging |
| T1003.001 (LSASS dump) | Sysmon 10 (ProcessAccess) | Sysmon 10 |
| T1053.005 (Sched. Task) | Security 4698/4702 + Sysmon 1 | Security 4698 |
| T1547.001 (Registry Run) | Sysmon 13 (Registry) | Sysmon 13 |
| T1021.001 (RDP) | Security 4624 Type 10 + Network | Security 4624 |
| T1071.001 (HTTP C2) | Zeek http.log / Proxy logs | Proxy logs |
| T1078.004 (Cloud Accounts) | Azure AD / CloudTrail | Cloud auth logs |

## Using Data Source Mappings

### For Detection Writing

1. Identify the technique your detection covers
2. Look up required data sources in the table above
3. Check which schema your SIEM uses (CIM, ECS, or native)
4. Map field names accordingly
5. Verify the data source is actually being collected in your environment

### For Gap Analysis

If you lack a data source, you lack detection capability for techniques that depend on it. Use this mapping to:

1. List all techniques you want to detect
2. Map each to required data sources
3. Compare against what you actually collect
4. Prioritize data source onboarding by technique coverage impact

### For Test Environment Planning

Use the data source mapping to determine what infrastructure your test lab needs. See the **Test Environment Builder** skill for building labs that produce specific data sources.
