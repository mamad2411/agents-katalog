---
name: intel-ioc-iocauto
description: "Intel Ioc Iocauto."
domain: cybersecurity
---

--|
| **IOC Enrichment** | Process of adding contextual intelligence to raw indicators from multiple external sources |
| **Composite Risk Score** | Weighted aggregate score combining multiple intelligence sources for disposition decisions |
| **Rate Limiting** | API request restrictions requiring throttling (VT free: 4/min, AbuseIPDB: 1000/day) |
| **GreyNoise RIOT** | Rule It Out — GreyNoise dataset of known benign services to reduce false positives |
| **Passive DNS** | Historical DNS resolution data showing domain-to-IP mappings over time |
| **Defanging** | Modifying IOCs for safe handling in reports (evil.com becomes evil[.]com) |

## Tools & Systems

- **VirusTotal**: Multi-engine malware scanner providing file, URL, IP, and domain analysis with 70+ AV engines
- **AbuseIPDB**: Community IP reputation database with abuse confidence scoring and ISP attribution
- **Shodan**: Internet-wide scanner providing open ports, banners, and vulnerability data for IP addresses
- **GreyNoise**: Internet noise intelligence distinguishing targeted attacks from opportunistic scanning
- **URLScan.io**: URL analysis platform capturing screenshots, DOM, and network requests for phishing detection

## Common Scenarios

- **Alert Triage Enrichment**: Auto-enrich all IPs in a notable event to determine if source is known malicious
- **Incident Scope Assessment**: Batch-enrich all IOCs from a compromised host to identify C2 infrastructure
- **Threat Intel Validation**: Enrich received IOC feed to validate quality before adding to blocking controls
- **Phishing URL Analysis**: Enrich URLs from reported phishing emails with URLScan and VT before user notification
- **False Positive Investigation**: Enrich flagged IP to determine if it belongs to CDN/cloud provider (legitimate)

## Output Format

```
IOC ENRICHMENT REPORT — IR-2024-0450
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Enrichment Time: 2024-03-15 14:30 UTC
IOCs Processed:  4

IP: 185.234.218[.]50
  Risk Score:   87/100 — MALICIOUS
  VirusTotal:   14/90 engines flagged malicious
  AbuseIPDB:    92% confidence, 347 reports
  Shodan:       Ports [22, 80, 443, 4444], Org: BulletProof Hosting
  GreyNoise:    malicious — known C2 infrastructure
  Action:       BLOCK immediately

DOMAIN: evil-c2-server[.]com
  Risk Score:   73/100 — MALICIOUS
  VirusTotal:   8/90 engines flagged
  URLScan:      5 scans, 4 malicious verdicts
  WHOIS:        Registered 3 days ago via Namecheap
  Action:       BLOCK and add to DNS sinkhole

HASH: a1b2c3d4e5f6...
  Risk Score:   91/100 — MALICIOUS
  VirusTotal:   52/72 engines (Cobalt Strike Beacon)
  MalwareBazaar: Tags: cobalt-strike, beacon, c2
  Action:       BLOCK hash, quarantine affected endpoints

IP: 45.33.32[.]156
  Risk Score:   5/100 — CLEAN
  VirusTotal:   0/90 engines
  GreyNoise:    benign — Shodan scanner
  Action:       No action required (known scanner)
```
