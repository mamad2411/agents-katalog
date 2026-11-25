---
name: proto-rdp
description: RDP exposure and hardening review for scoped hosts — Network Level Authentication (NLA) check, TLS configuration audit, encryption protocol enumeration, version fingerprinting, BlueKeep/DejaBlue vulnerability detection, and restricted-admin mode review. No brute force, login attempt, session hijack, or pass-the-hash.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# RDP assessment — safe exposure and configuration review

Use this skill to review authorized Remote Desktop Protocol services for NLA posture, TLS configuration, encryption strength, known-vulnerability exposure, and hardening gaps — without brute force, password guessing, session access, pass-the-hash, or BlueKeep exploitation. All checks are banner/configuration enumeration only. Never attempt to authenticate, interact with user sessions, or exploit known CVEs.

## Required inputs

- Written scope naming authorized RDP hosts, ports (default 3389, plus any non-standard ports), allowed check types (banner grab, NLA/TLS enumeration, vulnerability detection), rate limits, and testing window.
- Explicit permission for authenticated connection attempt if test credentials are provided. Test credentials must be user-owned or project-approved, and the test account must have no elevated privileges.
- Valid authorization cache for each RDP host.
- Separate disabled-default approval before any brute force, credential stuffing, pass-the-hash, session hijack, BlueKeep/DejaBlue exploitation, or lateral movement workflow.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target` for each RDP host.
3. `pentest_agent_check_authorization` before any active connection.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools (nmap, xfreerdp, rdesktop) are used.
5. `pentest_agent_execute_tool` for all execution.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — port and service discovery

1. Confirm RDP port is open:
   - Default port 3389, plus any non-standard ports specified in scope.
   - `nmap -p 3389,<non-standard-ports> --open <host>` through `pentest_agent_execute_tool`.
2. Service fingerprint:
   - `nmap -sV -p 3389 <host>` — identifies the RDP service and may detect the underlying OS.
   - Use `nmap --script rdp-enum-encryption -p 3389 <host>` to enumerate supported encryption protocols and NLA status.
3. Record: host, port, service banner, OS guess, encryption protocols, and NLA indicator.

### Phase 2 — NLA and authentication protocol review

Network Level Authentication (NLA) requires the client to authenticate before establishing a full RDP session. This is the single most important RDP hardening control.

1. Check NLA support:
   - `nmap -p 3389 --script rdp-enum-encryption <host>` reports whether CredSSP (NLA) is supported.
   - If NLA is not supported → high finding. Without NLA, the RDP server allocates resources before authentication, enabling pre-authentication denial-of-service and increasing the attack surface for credential brute force.
   - If NLA is supported and required → positive control. The server rejects connections that do not complete NLA.
2. Check for NLA downgrade:
   - Some servers support NLA but do not require it. This is a medium finding — an attacker can choose to bypass NLA.
   - Verify with `nmap --script rdp-enum-encryption` output: look for `CredSSP (NLA): supported` but also `"SSL"` or `"RDP Security"` protocol support without required CredSSP.
3. Check for Restricted Admin mode:
   - Restricted Admin mode allows network logon without storing credentials on the target, reducing credential theft risk. It is a positive control but also enables pass-the-hash — do not test pass-the-hash.
   - Detectability: Restricted Admin is a server-side setting, not directly detectable from the network without authentication. Note in the evidence that Restricted Admin mode status cannot be verified remotely without authentication.

### Phase 3 — encryption protocol audit

RDP supports multiple encryption layers. The strongest is TLS (with valid certificate) + CredSSP.

1. Check supported encryption protocols:
   - `nmap -p 3389 --script rdp-enum-encryption <host>` enumerates: `RDP Security` (native RDP encryption), `SSL` (TLS), `CredSSP` (NLA over TLS), `Early User Authorization`.
   - Preferred: `CredSSP` (NLA over TLS) only. `RDP Security` alone uses RC4 and is vulnerable to known weaknesses.
2. TLS certificate check:
   - `nmap --script ssl-cert -p 3389 <host>` to retrieve the RDP server's TLS certificate.
   - Check: validity period (not expired), hostname match (certificate CN/subjectAltName matches the target), issuer (trusted CA vs self-signed), key length (RSA 2048-bit minimum).
   - Flag: self-signed certificate → low/medium finding (man-in-the-middle risk is limited for RDP, but it reduces trust). Expired certificate → medium finding (operational hygiene).
   - Flag: weak key (RSA < 2048-bit, DSA, ECDSA with P-256 or weaker) → medium finding.
3. TLS version and cipher audit:
   - `nmap --script ssl-enum-ciphers -p 3389 <host>`
   - Flag: TLS 1.0/1.1 support → medium finding (deprecated, vulnerable to BEAST/POODLE-class attacks). TLS 1.2 minimum is required. TLS 1.3 is preferred.
   - Flag: weak ciphers (RC4, 3DES, EXPORT-grade, NULL, anonymous key exchange) → medium/high finding.
4. Check FIPS compliance:
   - If the environment requires FIPS 140-2 compliance, verify that only FIPS-approved algorithms are offered. Flag non-FIPS ciphers.

### Phase 4 — version and vulnerability detection

1. Operating system inference:
   - RDP version correlates tightly with Windows version. The `rdp-enum-encryption` NSE script and service banner typically reveal the underlying Windows version (Windows 7/2008 R2 → RDP 7.x, Windows 10/2016 → RDP 10.x, Windows 11/2022 → RDP 10.x+).
   - Record: inferred OS version from protocol negotiation.
2. Known vulnerability checks (read-only detection):
   - **MS12-020 (CVE-2012-0002)**: `nmap -p 3389 --script rdp-vuln-ms12-020 <host>`. Affects Windows XP/Server 2003. If detected, this is a critical finding — remote code execution without authentication. Do NOT exploit or send the proof-of-concept packet.
   - **BlueKeep (CVE-2019-0708)**: `nmap -p 3389 --script rdp-vuln-ms19-0708 <host>`. Affects Windows 7/Server 2008 R2 and earlier. If detected, this is a critical finding. Do NOT run public BlueKeep exploit scripts — detection via NSE is approved, exploitation is not.
   - **DejaBlue (CVE-2019-1181/1182)**: affects newer Windows versions (up to Windows 10 1903). NSE detection may be limited. Flag if the host runs an unpatched Windows 10 build before the August 2019 patch.
   - **CVE-2020-0609/0610** (RDP Gateway): if RDP Gateway (port 3391/443) is in scope, check for these UDS HTTP vulnerabilities.
3. End-of-life detection:
   - If the host runs Windows Server 2008/2008 R2 (EOL January 2020), Windows 7 (EOL January 2020), or Windows Server 2012/2012 R2 (EOL October 2023) → flag as high finding. End-of-life operating systems no longer receive security patches.
4. Do NOT run active exploitation tools (`bluekeep_poc.py`, `rdp_check.py`, Metasploit auxiliary modules that crash the target). Detection-only NSE scripts are acceptable; exploits are not.

### Phase 5 — hardening posture assessment

Based on the data collected:

1. **NLA required**: positive. NLA supported but not required: medium finding (enforce via Group Policy: `Require user authentication for remote connections by using Network Level Authentication`).
2. **TLS enforced**: positive. RDP Security (non-TLS) still available: medium finding. Configure `SecurityLayer` to `SSL` (TLS 1.0) or `2` (negotiate).
3. **Encryption level**: `High` or `FIPS Compliant` → positive. `Client Compatible` or `Low` → high finding (weak encryption, RC4 with 56-bit or 40-bit keys).
4. **Account lockout policy**: not directly testable from the network, but note that Windows account lockout applies to RDP logon attempts (via NLA). This provides brute-force resistance — but a dedicated attacker can still slow-spray.
5. **RDP exposed to Internet**: if the RDP port is reachable from a public IP (ask the operator or check via Shodan if scope permits), flag as high finding. RDP should never be directly exposed to the Internet without an RD Gateway, VPN, or IP restriction.
6. **Network-level restrictions**: recommend Windows Firewall rules to restrict RDP access to specific management IPs, RD Gateway for external access, and multi-factor authentication for all RDP logons.

## Decision points

- **BlueKeep vulnerability detected**: critical finding — RCE without authentication. Immediately notify operator. Do NOT run any exploit, even for proof-of-concept.
- **NLA not supported**: high finding — significant attack surface increase. Upgrade to critical if exposed to Internet.
- **RDP Security (RC4) forced, no TLS**: high finding — encryption can be decrypted. All RDP traffic potentially exposed.
- **Windows 7 / Server 2008 detected**: critical finding — EOL, unpatched vulnerabilities including BlueKeep.
- **Self-signed certificate + Internet-exposed RDP**: high finding — trust issue in high-risk context.
- **TLS 1.0 only**: medium finding — upgrade to TLS 1.2+.
- **Downgrade to port check only**: when NLA prevents protocol enumeration without authentication. Record that the server enforces NLA (positive) but limited enumeration was possible.

## Prohibited behavior

- Credential brute force (`hydra`, `crowbar`, `ncrack`, `crackmapexec rdp`) — disabled-default.
- Pass-the-hash via RDP (`xfreerdp /pth`, restricted admin mode abuse) — disabled-default (credential attack).
- BlueKeep/DejaBlue/MS12-020 exploitation — destructive exploitation, blocked. Detection-only scripts that do not crash the target are allowed.
- RDP session hijacking (`tscon`, `query session`, Metasploit session hijack) — requires SYSTEM-level access on target, prohibited.
- Pre-authentication denial-of-service (sending connection floods to non-NLA RDP) — DoS-class method, blocked in bug-bounty/red-team modes.
- Capturing RDP session screenshots, keystrokes, or clipboard data — prohibited unconditionally.
- Attempting to log in with default/guessed credentials — prohibited unless scope explicitly lists a specific credential pair to test.
- Running `xfreerdp` or `rdesktop` with connection parameters that would trigger an interactive session — banner/protocol check only.

## Stop conditions

- Server actively refuses connections (RDP port filtered or service stopped) → stop, record the block as a positive control.
- NLA check reveals the server has a valid TLS certificate with strong ciphers and requires NLA → the most critical checks are positive. Proceed to vulnerability detection only.
- BlueKeep detection returns positive → stop all RDP activity, record critical finding, alert operator immediately.
- Connection attempt triggers account lockout (unlikely from banner check, but if using test credentials) → stop all authenticated activity immediately.
- Evidence would include host identification that reveals internal naming schemes beyond scope → redact and stop.

## Evidence — RDP service record

For each authorized RDP host:

```text
Host: <host> (hash if redaction required)
Port: 3389

Operating system: Windows Server 2019 (inferred from RDP v10.6 protocol)

NLA:
  CredSSP (NLA): supported and required (positive)
  Downgrade risk: none — NLA enforced

Encryption:
  Protocol priority: CredSSP > TLS 1.2 > (RDP Security disabled)
  TLS version: 1.2 (AES-256-GCM)
  RDP Security (RC4): not offered (positive)
  Certificate: valid (internal CA), CN=<host>.contoso.local, RSA 2048-bit, expires 2025-09-01
  Weak ciphers: none

Vulnerability detection:
  BlueKeep (CVE-2019-0708): not vulnerable (Windows Server 2019 not affected)
  MS12-020 (CVE-2012-0002): not vulnerable
  EOL status: Windows Server 2019 (mainstream support until 2024, extended until 2029)

Exposure:
  Internet-exposed: no (internal IP 10.x.x.x)
  Network restriction: Windows Firewall limits RDP to management subnet

Findings:
  [MEDIUM] RDP exposed to all internal hosts (no IP restriction beyond firewall rule)
  [LOW] Self-signed/internal CA certificate — medium trust in non-Internet context
  [INFO] NLA enforced — positive control
  [INFO] TLS 1.2 with strong ciphers — positive control
  [INFO] No known CVEs detected — positive
```

Aggregate into an RDP security posture summary per host. Include: NLA posture, encryption protocol stack, TLS certificate and cipher audit, known-vulnerability status, exposure level, and recommended hardening steps.

Never store: RDP connection sequences with credentials, session screenshots, NLA challenge-response data, TLS private keys, or any data from an interactive RDP session.

## Report handoff

1. `pentest_agent_record_finding` for each confirmed weakness: no NLA, NLA not required, RDP Security (RC4) enabled, weak TLS version/ciphers, BlueKeep/MS12-020 vulnerability, Internet-exposed RDP, EOL operating system, missing network restrictions.
2. Package findings with the host's overall RDP security grade: NLA posture, encryption grade, vulnerability status, and exposure score.
3. Recommend: enforce NLA via Group Policy, disable RDP Security (force TLS), configure TLS 1.2+ with strong ciphers, deploy RD Gateway for external access, restrict RDP access to specific management IPs via firewall, apply all security patches (especially for BlueKeep/DejaBlue), upgrade EOL operating systems, enable multi-factor authentication for RDP, and enable account lockout policy.
4. Explicitly note that no brute force, credential testing, BlueKeep/DejaBlue/MS12-020 exploitation, pass-the-hash, session hijack, or interactive RDP session was performed — only safe banner, NLA, encryption, and vulnerability-detection checks.
