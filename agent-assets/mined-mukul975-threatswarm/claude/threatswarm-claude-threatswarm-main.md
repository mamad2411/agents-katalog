# Cybersecurity Workspace — Master Context

## Scope Enforcement (MANDATORY — ZERO EXCEPTIONS)
**ALL targets MUST be listed in `scope.txt` before any network tool runs.**
The `scope_check.py` hook enforces this automatically on every Bash command.
Add targets: IP, CIDR, or domain — one per line, comments start with `#`.

## Tool Paths
| Tool | Path / Command |
|------|----------------|
| nmap | `nmap` |
| Metasploit | `msfconsole`, `msfvenom` |
| Nuclei | `nuclei` |
| Amass | `amass` |
| Subfinder | `subfinder` |
| HTTPX | `httpx` |
| Feroxbuster | `feroxbuster` |
| SQLMap | `sqlmap` |
| Hashcat | `hashcat` |
| Hydra | `hydra` |
| Impacket | `impacket-*` (GetUserSPNs, secretsdump, psexec, etc.) |
| BloodHound | `bloodhound-python` |
| CrackMapExec | `crackmapexec` |
| Responder | `responder` |
| Bettercap | `bettercap` |
| Ghidra | `ghidra` (headless: `analyzeHeadless`) |
| Frida | `frida`, `frida-ps` |
| MobSF | `http://localhost:8000` (API) |
| Sliver | `sliver-client` |
| Havoc | `./havoc` |
| Burp Suite | `burpsuite` |

## Agent Delegation Table
| Attack Category | Agent | When to Delegate |
|-----------------|-------|-----------------|
| Port scan, service enum, web crawl | `recon` | First step on any target |
| Web app vulns (SQLi, XSS, LFI, SSRF) | `web-attacker` | Web ports open |
| AD, Kerberos, DCSync, BloodHound | `active-directory` | Domain environment |
| CVE exploit, get initial shell | `exploit` (after `vuln-researcher`) | Vulns identified |
| Privesc, lateral movement, persistence | `post-ex` | Shell obtained |
| ARP, MitM, SNMP, SMB relay | `network-ops` | Internal network |
| AWS, Azure, GCP, S3, IAM | `cloud-attacker` | Cloud targets |
| Docker, K8s, containers | `container-attacker` | Container environments |
| Domain intel, emails, breaches | `osint` | Passive recon phase |
| WiFi, WPA2, evil twin | `wireless-attacker` | Wireless testing |
| APK, iOS, Frida, ADB | `mobile-attacker` | Mobile app targets |
| REST, GraphQL, gRPC, Swagger | `api-attacker` | API surfaces |
| Binary RE, disasm, CTF | `reverse-engineer` | Binary analysis |
| Malware samples, IOCs, YARA | `malware-analyst` | Malware analysis |
| Phishing, pretexting, GoPhish | `social-engineer` | SE campaigns |
| AV bypass, AMSI, obfuscation | `evasion` | Post-access, AV present |
| Sliver, Havoc, MSF handler | `c2-operator` | C2 infrastructure |
| TLS, JWT, crypto, padding oracle | `crypto-attacker` | Crypto vulns |
| Firmware, IoT, UART, MQTT | `iot-attacker` | IoT/embedded devices |
| Hash cracking, wordlists | `password-attacks` | Hashes obtained |
| ATT&CK hunt, log queries | `threat-hunter` | Threat hunting |
| Incident triage, Volatility | `dfir` | Incident response |
| Hardening, Sigma, detection | `blue-team` | Defensive work |
| CVE research, PoC, CVSS | `vuln-researcher` | CVE investigation |
| CIS, PCI-DSS, NIST compliance | `compliance-scanner` | Compliance audits |
| Log parsing, anomaly detection | `log-analyst` | Log analysis |
| Pentest report generation | `report-writer` | Final deliverable |

**NEVER run active recon or exploitation in the main conversation thread.**
**ALWAYS delegate to the appropriate agent.**

## OPSEC Defaults
- External traffic: route through `proxychains` where possible
- Nmap timing: `-T3` maximum unless explicitly authorized for `-T4`
- No real PII exfiltration — reference paths only in evidence/
- Minimize footprint: staged payloads for initial access only

## Evidence Output Pattern
```
evidence/$(date +%Y%m%d)/$TARGET/{nmap,nuclei,web,creds,screenshots}/
```
All tool output goes here. Reference paths in findings, never copy raw data.

## Environment Variables
| Variable | Purpose | Default |
|----------|---------|---------|
| `LHOST` | Attacker IP for callbacks | `10.10.14.1` |
| `LPORT` | Listener port | `4444` |
| `DOMAIN` | Target AD domain | (set per engagement) |
| `DC_IP` | Domain controller IP | (set per engagement) |
| `SCOPE_FILE` | Path to scope file | `./scope.txt` |
| `EVIDENCE_DIR` | Evidence base directory | `./evidence` |
| `WORDLISTS` | SecLists base path | `/usr/share/seclists` |

## Anti-Patterns (Claude MUST NEVER Do These)
1. Run any network tool without target being in `scope.txt`
2. Store plaintext passwords — hashes + location references only
3. Exfiltrate real PII from target systems
4. Run `-T5` nmap or DoS-class attacks without explicit written authorization
5. Execute exploits in the main conversation thread (always delegate to `exploit` agent)
6. Write credentials to `reports/` or `evidence/` in cleartext — use `[REDACTED]`
7. Push engagement data to public repos — `evidence/` and `loot/` are gitignored
8. Run `rm -rf` on evidence directories — preserve everything
9. Attempt to bypass scope_check.py hook
10. Connect to C2 infrastructure outside the authorized scope
11. Modify scope.txt mid-engagement without documenting the change
12. Run phishing campaigns against unauthorized targets

## Cybersecurity Skills Plugin (mukul975/Anthropic-Cybersecurity-Skills)

This workspace has the `cybersecurity-skills` skill pack installed. Agents MUST use these
skills proactively — invoke them with the Skill tool before starting any specialized task.

### Skill → Agent Mapping (invoke the skill FIRST, then execute commands)

| Agent | Primary Skills to Invoke |
|-------|--------------------------|
| `recon` | `cybersecurity-skills:scanning-network-with-nmap-advanced`, `cybersecurity-skills:performing-subdomain-enumeration-with-subfinder`, `cybersecurity-skills:conducting-external-reconnaissance-with-osint` |
| `web-attacker` | `cybersecurity-skills:performing-web-application-penetration-test`, `cybersecurity-skills:exploiting-sql-injection-with-sqlmap`, `cybersecurity-skills:exploiting-sql-injection-vulnerabilities`, `cybersecurity-skills:exploiting-server-side-request-forgery`, `cybersecurity-skills:testing-for-xss-vulnerabilities`, `cybersecurity-skills:exploiting-idor-vulnerabilities`, `cybersecurity-skills:testing-for-xxe-injection-vulnerabilities`, `cybersecurity-skills:performing-web-application-vulnerability-triage` |
| `active-directory` | `cybersecurity-skills:exploiting-active-directory-with-bloodhound`, `cybersecurity-skills:exploiting-kerberoasting-with-impacket`, `cybersecurity-skills:exploiting-active-directory-certificate-services-esc1`, `cybersecurity-skills:conducting-domain-persistence-with-dcsync`, `cybersecurity-skills:exploiting-zerologon-vulnerability-cve-2020-1472`, `cybersecurity-skills:analyzing-active-directory-acl-abuse`, `cybersecurity-skills:conducting-pass-the-ticket-attack`, `cybersecurity-skills:performing-active-directory-penetration-test` |
| `exploit` | `cybersecurity-skills:exploiting-vulnerabilities-with-metasploit-framework`, `cybersecurity-skills:exploiting-ms17-010-eternalblue-vulnerability`, `cybersecurity-skills:exploiting-smb-vulnerabilities-with-metasploit`, `cybersecurity-skills:performing-privilege-escalation-on-linux` |
| `post-ex` | `cybersecurity-skills:performing-privilege-escalation-on-linux`, `cybersecurity-skills:performing-lateral-movement-with-wmiexec`, `cybersecurity-skills:performing-credential-access-with-lazagne`, `cybersecurity-skills:extracting-credentials-from-memory-dump` |
| `network-ops` | `cybersecurity-skills:performing-arp-spoofing-attack-simulation`, `cybersecurity-skills:conducting-man-in-the-middle-attack-simulation`, `cybersecurity-skills:performing-network-traffic-analysis-with-tshark`, `cybersecurity-skills:performing-network-packet-capture-analysis` |
| `osint` | `cybersecurity-skills:collecting-open-source-intelligence`, `cybersecurity-skills:performing-osint-with-spiderfoot`, `cybersecurity-skills:performing-open-source-intelligence-gathering`, `cybersecurity-skills:performing-dns-enumeration-and-zone-transfer`, `cybersecurity-skills:performing-ip-reputation-analysis-with-shodan` |
| `cloud-attacker` | `cybersecurity-skills:conducting-cloud-penetration-testing`, `cybersecurity-skills:performing-cloud-penetration-testing-with-pacu`, `cybersecurity-skills:performing-aws-privilege-escalation-assessment`, `cybersecurity-skills:auditing-aws-s3-bucket-permissions`, `cybersecurity-skills:auditing-gcp-iam-permissions`, `cybersecurity-skills:detecting-aws-iam-privilege-escalation` |
| `container-attacker` | `cybersecurity-skills:performing-kubernetes-penetration-testing`, `cybersecurity-skills:performing-container-escape-detection`, `cybersecurity-skills:auditing-kubernetes-cluster-rbac`, `cybersecurity-skills:scanning-docker-images-with-trivy`, `cybersecurity-skills:performing-docker-bench-security-assessment` |
| `wireless-attacker` | `cybersecurity-skills:conducting-wireless-network-penetration-test`, `cybersecurity-skills:performing-wifi-password-cracking-with-aircrack`, `cybersecurity-skills:performing-wireless-security-assessment-with-kismet` |
| `mobile-attacker` | `cybersecurity-skills:conducting-mobile-app-penetration-test`, `cybersecurity-skills:performing-android-app-static-analysis-with-mobsf`, `cybersecurity-skills:performing-dynamic-analysis-of-android-app`, `cybersecurity-skills:reverse-engineering-android-malware-with-jadx`, `cybersecurity-skills:intercepting-mobile-traffic-with-burpsuite`, `cybersecurity-skills:performing-mobile-app-certificate-pinning-bypass`, `cybersecurity-skills:analyzing-ios-app-security-with-objection` |
| `api-attacker` | `cybersecurity-skills:conducting-api-security-testing`, `cybersecurity-skills:performing-graphql-security-assessment`, `cybersecurity-skills:exploiting-idor-vulnerabilities`, `cybersecurity-skills:testing-api-for-broken-object-level-authorization`, `cybersecurity-skills:exploiting-mass-assignment-in-rest-apis`, `cybersecurity-skills:exploiting-jwt-algorithm-confusion-attack`, `cybersecurity-skills:performing-api-fuzzing-with-restler` |
| `reverse-engineer` | `cybersecurity-skills:performing-binary-exploitation-analysis`, `cybersecurity-skills:reverse-engineering-malware-with-ghidra`, `cybersecurity-skills:reverse-engineering-dotnet-malware-with-dnspy`, `cybersecurity-skills:analyzing-heap-spray-exploitation` |
| `malware-analyst` | `cybersecurity-skills:analyzing-linux-elf-malware`, `cybersecurity-skills:analyzing-macro-malware-in-office-documents`, `cybersecurity-skills:performing-malware-triage-with-yara`, `cybersecurity-skills:performing-malware-hash-enrichment-with-virustotal`, `cybersecurity-skills:extracting-iocs-from-malware-samples`, `cybersecurity-skills:performing-static-malware-analysis-with-pe-studio`, `cybersecurity-skills:analyzing-malware-behavior-with-cuckoo-sandbox`, `cybersecurity-skills:deobfuscating-powershell-obfuscated-malware` |
| `social-engineer` | `cybersecurity-skills:conducting-spearphishing-simulation-campaign`, `cybersecurity-skills:performing-phishing-simulation-with-gophish`, `cybersecurity-skills:conducting-social-engineering-pretext-call`, `cybersecurity-skills:executing-phishing-simulation-campaign` |
| `evasion` | `cybersecurity-skills:detecting-evasion-techniques-in-endpoint-logs`, `cybersecurity-skills:hunting-for-living-off-the-land-binaries`, `cybersecurity-skills:detecting-living-off-the-land-attacks` |
| `c2-operator` | `cybersecurity-skills:building-c2-infrastructure-with-sliver-framework`, `cybersecurity-skills:building-red-team-c2-infrastructure-with-havoc`, `cybersecurity-skills:analyzing-cobalt-strike-beacon-configuration`, `cybersecurity-skills:analyzing-command-and-control-communication` |
| `crypto-attacker` | `cybersecurity-skills:performing-ssl-tls-security-assessment`, `cybersecurity-skills:exploiting-jwt-algorithm-confusion-attack`, `cybersecurity-skills:testing-for-json-web-token-vulnerabilities`, `cybersecurity-skills:performing-cryptographic-audit-of-application` |
| `iot-attacker` | `cybersecurity-skills:performing-iot-security-assessment`, `cybersecurity-skills:performing-firmware-extraction-with-binwalk`, `cybersecurity-skills:performing-firmware-malware-analysis` |
| `password-attacks` | `cybersecurity-skills:performing-hash-cracking-with-hashcat`, `cybersecurity-skills:hunting-credential-stuffing-attacks` |
| `threat-hunter` | `cybersecurity-skills:building-threat-hunt-hypothesis-framework`, `cybersecurity-skills:hunting-for-cobalt-strike-beacons`, `cybersecurity-skills:hunting-for-command-and-control-beaconing`, `cybersecurity-skills:hunting-for-persistence-mechanisms-in-windows`, `cybersecurity-skills:performing-threat-hunting-with-elastic-siem`, `cybersecurity-skills:hunting-for-lateral-movement-via-wmi`, `cybersecurity-skills:detecting-lateral-movement-with-splunk` |
| `dfir` | `cybersecurity-skills:conducting-memory-forensics-with-volatility`, `cybersecurity-skills:performing-memory-forensics-with-volatility3`, `cybersecurity-skills:analyzing-memory-dumps-with-volatility`, `cybersecurity-skills:collecting-volatile-evidence-from-compromised-host`, `cybersecurity-skills:performing-disk-forensics-investigation`, `cybersecurity-skills:performing-linux-log-forensics-investigation`, `cybersecurity-skills:building-incident-timeline-with-timesketch`, `cybersecurity-skills:triaging-security-incident` |
| `blue-team` | `cybersecurity-skills:building-detection-rules-with-sigma`, `cybersecurity-skills:implementing-mitre-attack-coverage-mapping`, `cybersecurity-skills:configuring-windows-event-logging-for-detection`, `cybersecurity-skills:hardening-linux-endpoint-with-cis-benchmark`, `cybersecurity-skills:hardening-windows-endpoint-with-cis-benchmark`, `cybersecurity-skills:configuring-suricata-for-network-monitoring`, `cybersecurity-skills:implementing-endpoint-detection-with-wazuh` |
| `vuln-researcher` | `cybersecurity-skills:performing-vulnerability-scanning-with-nessus`, `cybersecurity-skills:performing-authenticated-vulnerability-scan`, `cybersecurity-skills:performing-cve-prioritization-with-kev-catalog`, `cybersecurity-skills:prioritizing-vulnerabilities-with-cvss-scoring` |
| `compliance-scanner` | `cybersecurity-skills:auditing-cloud-with-cis-benchmarks`, `cybersecurity-skills:implementing-pci-dss-compliance-controls`, `cybersecurity-skills:performing-nist-csf-maturity-assessment`, `cybersecurity-skills:performing-soc2-type2-audit-preparation` |
| `log-analyst` | `cybersecurity-skills:analyzing-security-logs-with-splunk`, `cybersecurity-skills:analyzing-linux-audit-logs-for-intrusion`, `cybersecurity-skills:analyzing-web-server-logs-for-intrusion`, `cybersecurity-skills:analyzing-windows-event-logs-in-splunk`, `cybersecurity-skills:analyzing-powershell-script-block-logging` |
| `report-writer` | `cybersecurity-skills:generating-threat-intelligence-reports`, `cybersecurity-skills:building-incident-response-playbook` |

### How Agents Use Skills

When any agent starts a task, it MUST:
1. Invoke the relevant `cybersecurity-skills:*` skill(s) via the Skill tool FIRST
2. Read the guidance returned by the skill
3. Apply that guidance to the specific target/task context
4. Then execute the actual tool commands

This ensures consistent, professional methodology across all engagements.

---

## Context Compaction Instructions
When context is compacted, preserve in the summary:
- Current target list and scope entries
- Open findings and their severity levels
- Tool output file paths (not raw output)
- Current phase of engagement (recon/exploit/post-ex/report)
- Active sessions and access levels obtained
