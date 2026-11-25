---
name: proto-smb
description: SMB share and protocol security review for scoped hosts — SMB version and signing posture, null-session enumeration boundaries, share access audit, known-vulnerability detection (EternalBlue, SMBGhost), and hardening assessment. No credential spray, pass-the-hash, NTLM relay, EternalBlue exploitation, or secrets dump.
disable-model-invocation: true
risk: caution
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# SMB assessment — safe configuration and exposure review

Use this skill to review authorized SMB/CIFS services for version exposure, signing posture, null-session enumeration boundaries, share access audit, known-vulnerability detection, and hardening gaps — without credential spray, pass-the-hash, NTLM relay, EternalBlue/SMBGhost exploitation, or secrets dump. All checks are read-only protocol and configuration review. Never authenticate with guessed/harvested credentials, relay authentication, or exploit SMB vulnerabilities.

## Required inputs

- Written scope naming authorized SMB hosts, NetBIOS names, IP ranges, allowed check types (version detection, signing check, share enumeration, null-session test, vulnerability detection), rate limits, and testing window.
- Explicit permission for null-session (unauthenticated) share enumeration attempt. Without this, only SMB version, signing, and vulnerability detection are allowed.
- Explicit permission for authenticated share access if read-only credentials are provided. The test account must be a low-privilege domain user with no administrative access to any server.
- Valid authorization cache for each SMB host.
- List of prohibited share types: do not access `ADMIN$`, `C$`, `IPC$` beyond metadata. Do not browse or download from user home shares or departmental shares.
- Separate disabled-default approval before any credential spray, pass-the-hash, NTLM relay, coercion (PetitPotam/PrinterBug), EternalBlue/SMBGhost exploitation, or secrets dump (SAM, LSA, NTDS).

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target` for each SMB host.
3. `pentest_agent_check_authorization` before any active SMB connection.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools (nmap, smbclient, smbmap, crackmapexec) are used.
5. `pentest_agent_execute_tool` for all execution.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — service discovery and version fingerprinting

1. Confirm SMB ports are open:
   - Port 139 (NetBIOS session service), port 445 (SMB over TCP).
   - `nmap -p 139,445 --open <host>` through `pentest_agent_execute_tool`.
2. SMB version and OS fingerprint:
   - `nmap -sV -p 139,445 --script smb-os-discovery <host>` — identifies SMB version (SMBv1, SMBv2, SMBv3), OS, hostname, domain/workgroup, and FQDN.
   - Or use `crackmapexec smb <host>` (safe fingerprint mode — CME queries SMB without authentication and reports OS, hostname, signing status).
3. SMB signing check:
   - `nmap -p 445 --script smb-security-mode <host>` — reports whether SMB signing is required, enabled (but not required), or disabled.
   - Signing disabled → high finding. This enables NTLM relay attacks (if an attacker can coerce authentication to a relay server, they can relay to this host because it doesn't require signed packets).
   - Signing enabled but not required → medium finding. The server accepts signed packets but does not enforce them — an attacker can downgrade.
   - Signing required → positive control.
4. SMBv1 detection:
   - `nmap -p 445 --script smb-protocols <host>` — reports which SMB dialect versions are negotiated.
   - SMBv1 enabled → critical finding. SMBv1 is the vector for EternalBlue, WannaCry, and numerous other critical vulnerabilities. It has been deprecated since 2014 and should be disabled on all systems.
   - Record: all supported SMB dialect versions (1.0, 2.0.2, 2.1, 3.0, 3.0.2, 3.1.1).

### Phase 2 — null-session (unauthenticated) enumeration

Only if scope explicitly permits null-session testing:

1. Attempt unauthenticated SMB connection:
   - `smbclient -L //<host> -N` — lists shares without credentials.
   - `smbmap -H <host>` — alternative tool, shows share names and permissions.
2. If shares are listed without credentials:
   - Record: share names, share types (disk, printer, IPC, administrative), and any access-level indicators (READ, WRITE — these are permission flags, do not test write).
   - Flag any non-default share visible anonymously → medium finding (information disclosure).
   - Flag any share with reported READ access via null session → high finding (unauthenticated file access).
3. Do NOT browse share contents, list files, or download from shares via null session. The goal is to confirm the exposure, not harvest data.
4. Do NOT enumerate users, groups, or domain information via `enum4linux` or `rpcclient` unless scope explicitly permits RPC enumeration. RPC enumeration is an AD assessment workflow, not part of this skill.

### Phase 3 — authenticated share audit (read-only)

Only if scope provides read-only credentials and explicitly permits authenticated share access:

1. List shares with credentials:
   - `smbclient -L //<host> -U <domain>/<user>%<password>`
   - `smbmap -H <host> -u <user> -p <password>`
2. Record: all share names, share types, and access-level indicators.
   - Flag: administrative shares (`ADMIN$`, `C$`, `D$`, `IPC$`) — these are normally present but should only be accessible to administrators. If the read-only test account can access them, flag as critical finding.
   - Flag: shares with names like `Users`, `Home`, `Departments`, `Finance`, `HR` — these may contain sensitive data. Do NOT browse them unless scope explicitly lists them as authorized for directory listing.
   - Flag: shares with `Everyone` or `Authenticated Users` Full Control → high finding (overly permissive access).
3. For shares explicitly authorized for directory listing in scope:
   - Limit listing to top-level directory only (`smbclient //<host>/<share> -U <user>%<password> -c "ls"` with a depth limit).
   - Do NOT recursively spider shares. Do NOT download files.
   - Record: top-level directory names only. Do not record file names unless scope permits.
4. Do NOT mount shares (`mount -t cifs`). Do NOT download, upload, modify, or delete any files.

### Phase 4 — known vulnerability detection (read-only)

1. **EternalBlue (MS17-010 / CVE-2017-0144)**:
   - `nmap -p 445 --script smb-vuln-ms17-010 <host>` — detection only.
   - If vulnerable: critical finding. Affects Windows 7/Server 2008 R2 and earlier (unpatched). Do NOT run `eternalblue_exploit7.py` or any Metasploit exploit module.
2. **SMBGhost (CVE-2020-0796)**:
   - Affects Windows 10 v1903/v1909 and Windows Server 2019 (unpatched for March 2020 patch).
   - NSE detection may be limited. Flag if the host runs an affected build without the March 2020 security update.
   - Do NOT run SMBGhost RCE or LPE exploits.
3. **SMBleed (CVE-2020-1206)**:
   - Information disclosure in SMBv3.1.1 decompression. Affects Windows 10 v1903/v1909.
   - If detected via version/build inference, flag as medium finding. No active exploitation.
4. **Other SMB CVEs**:
   - `nmap --script "smb-vuln-*" -p 139,445 <host>` — run the full SMB vulnerability detection suite. Review NSE script output. Any `VULNERABLE` result → record finding, do NOT exploit.
5. **End-of-life detection**:
   - If SMB OS discovery reveals Windows Server 2008/2008 R2 or Windows 7 (EOL January 2020) → critical finding.
   - Windows Server 2012/2012 R2 (EOL October 2023) → high finding.

### Phase 5 — hardening posture assessment

1. **SMB signing**: required → positive. Enabled not required → medium finding (recommend enforcing via Group Policy: `Microsoft network server: Digitally sign communications (always)`). Disabled → high finding.
2. **SMBv1**: disabled → positive. Enabled → critical finding (disable via `Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol` or Group Policy).
3. **SMBv2/v3 encryption**: SMB 3.0+ supports AES-based encryption for data in transit. This is a server-side configuration. Check if the server supports SMB 3.1.1 (which always offers encryption). If SMB 3.x is available, recommend enabling SMB Encryption for sensitive shares.
4. **Null session restrictions**: `RestrictNullSessAccess` registry key (Windows) should be set to 1 to prevent anonymous share enumeration. Tested above — if null session returned share list, this is not configured.
5. **Guest account**: the built-in Guest account should be disabled. On modern Windows, it is disabled by default.
6. **Network-level restrictions**: recommend Windows Firewall or network ACLs to restrict SMB access to specific management and domain-controller subnets. SMB should never be exposed to the Internet (port 445 blocked at the perimeter).

## Decision points

- **SMBv1 enabled**: critical finding — disable immediately. SMBv1 is the most attacked SMB protocol and the vector for WannaCry/EternalBlue.
- **EternalBlue (MS17-010) vulnerable**: critical finding — full remote code execution with SYSTEM privileges. Patch immediately.
- **SMB signing disabled**: high finding — enables NTLM relay attacks. Require SMB signing across the domain.
- **Null session returns share list**: medium/high finding — information disclosure. Restrict via `RestrictNullSessAccess` and firewall rules.
- **Administrative shares accessible to low-privilege account**: critical finding — likely misconfiguration. Normal users should not access `C$`, `ADMIN$`.
- **Share with Everyone Full Control**: high finding — any domain user can read/write. Review share permissions.
- **Proceed to detailed share content review**: only if scope explicitly permits directory listing for specific shares with depth limits. Do NOT spider or download.
- **Downgrade to version/signing check only**: when null session is blocked and no credentials are available. Record the security posture from network-observable data.

## Prohibited behavior

- Credential spray or brute force (`crackmapexec smb <target> -u users.txt -p passwords.txt`, `hydra smb`) — disabled-default.
- Pass-the-hash (`crackmapexec smb <target> -H <hash>`, `impacket-psexec -hashes`, `evil-winrm -H`) — disabled-default (credential attack).
- NTLM relay (`ntlmrelayx.py`, `responder` + relay configuration) — disabled-default (credential capture + relay).
- Coercion attacks (PetitPotam, PrinterBug, DFSCoerce, ShadowCoerce) — disabled-default (authentication coercion).
- EternalBlue/SMBGhost/EternalRomance exploitation — destructive exploitation, blocked.
- Secrets dump (`impacket-secretsdump`, `crackmapexec smb --sam`, `crackmapexec smb --lsa`, `crackmapexec smb --ntds`) — disabled-default (credential theft).
- File upload, download, modification, or deletion via any share — prohibited unconditionally unless scope explicitly provides a dedicated test share and file for upload/download validation.
- Mounting shares to the local filesystem (`mount -t cifs`) — prohibited. This leaves local artifacts and may trigger antivirus.
- Spidering shares recursively (`crackmapexec smb -M spider_plus`) — prohibited unless scope explicitly authorizes full content discovery.
- Accessing user home shares, departmental shares, or any share likely to contain personal or sensitive data.

## Stop conditions

- Server returns `STATUS_ACCESS_DENIED` or `STATUS_LOGON_FAILURE` on authenticated connection → stop, do not guess credentials.
- Null session returns share list with sensitive share names (HR, Finance, Payroll, Legal) → stop, redact share names if they reveal sensitive organizational structure, alert operator.
- EternalBlue detection returns vulnerable → stop all SMB activity, record critical finding, alert operator immediately.
- A share is found to be anonymously writable (you observed a WRITE indicator in null session) → stop, do NOT test write. Record as critical finding.
- Evidence would include file names, share names, or directory structures that reveal sensitive data organization → redact and stop that enumeration path.
- Server rate-limits or throttles connections → respect the backpressure, do not retry aggressively.

## Evidence — SMB service record

For each authorized SMB host:

```text
Host: <host> (FQDN: <host>.contoso.local)
Ports: [139 (NetBIOS), 445 (SMB over TCP)]

SMB dialects: 2.0.2, 2.1, 3.0, 3.0.2, 3.1.1
  SMBv1: disabled (positive)
  SMB signing: required (positive)

Null session (unauthenticated):
  Share enumeration: refused (STATUS_ACCESS_DENIED — positive)
  Null session restricted: yes (positive)

Authenticated (read-only account — hash redacted):
  Shares:
    [IPC$] — IPC (default, administrative users only)
    [NETLOGON] — Disk, READ (domain-joined computers)
    [SYSVOL] — Disk, READ (domain-joined computers)
    [Shared] — Disk, READ (Authenticated Users)
    [Departments] — Disk, READ (Authenticated Users — medium finding: broad access)
  No administrative shares accessible to test account (positive)
  SMB encryption: available (SMB 3.1.1 — AES-128-GCM)

Vulnerability detection:
  MS17-010 (EternalBlue): not vulnerable
  SMBGhost (CVE-2020-0796): not vulnerable (Windows Server 2019, patched)
  EOL status: Windows Server 2019 (supported)

Findings:
  [MEDIUM] Departments share accessible to all Authenticated Users — broad read access
  [INFO] SMBv1 disabled — positive control
  [INFO] SMB signing required — positive control
  [INFO] Null session restricted — positive control
  [INFO] No critical CVEs detected — positive
```

Aggregate into an SMB security posture summary per host. Include: SMB version support, signing posture, null-session access, share inventory and permissions, known-vulnerability status, and recommended hardening.

Never store: share directory listings with file names, SMB packet captures with authentication data, NTLM challenge-response pairs, share content, user or group names from share ACLs, or hostnames of other SMB servers discovered during enumeration.

## Report handoff

1. `pentest_agent_record_finding` for each confirmed weakness: SMBv1 enabled, SMB signing disabled/not-required, null session accessible, EternalBlue/SMBGhost vulnerability, administrative shares accessible to low-privilege users, shares with overly broad permissions, EOL operating system.
2. Package findings with the host's overall SMB security grade: protocol posture, signing posture, access control, vulnerability status, and exposure score.
3. Recommend: disable SMBv1 on all systems, enforce SMB signing across the domain, restrict null-session access via `RestrictNullSessAccess` and firewall rules, apply MS17-010 and SMBGhost patches immediately, upgrade EOL operating systems, review share permissions (remove Everyone/Authenticated Users Full Control), enable SMB Encryption for sensitive shares, and restrict SMB access to authorized management subnets via firewall.
4. Explicitly note that no credential spray, pass-the-hash, NTLM relay, coercion, EternalBlue/SMBGhost exploitation, secrets dump, or file access/manipulation was performed — only safe SMB protocol configuration review and vulnerability detection.
