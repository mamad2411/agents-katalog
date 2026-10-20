---
name: intel-ioc-indicators-hunt
description: "--| | **IOC** | Indicator of Compromise — observable network or host artifact indicating potential compromise | | **Enrichment** | Process of adding contextual data to a raw IOC from multiple intelligence sources | | **Defanging** | Modifying IOCs (replacing `."
domain: cybersecurity
---

--|
| **IOC** | Indicator of Compromise — observable network or host artifact indicating potential compromise |
| **Enrichment** | Process of adding contextual data to a raw IOC from multiple intelligence sources |
| **Defanging** | Modifying IOCs (replacing `.` with `[.]`) to prevent accidental activation in documentation |
| **False Positive Rate** | Percentage of benign artifacts incorrectly flagged as malicious; critical for tuning block thresholds |
| **Sinkhole** | DNS server redirecting malicious domain lookups to a benign IP for detection without blocking traffic entirely |
| **TTL** | Time-to-live for an IOC in blocking controls; IP indicators should expire after 30 days, domains after 90 days |

## Tools & Systems

- **VirusTotal**: Multi-engine malware scanner and threat intelligence platform with 70+ AV engines, sandbox reports, and community comments
- **AbuseIPDB**: Community-maintained IP reputation database with 90-day abuse report history
- **MalwareBazaar (abuse.ch)**: Free malware hash repository with YARA rule associations and malware family tagging
- **URLScan.io**: Free URL analysis service that captures screenshots, DOM, and network requests for phishing URL triage
- **Shodan**: Internet-wide scan data providing hosting provider, open ports, and banner information for IP enrichment

## Common Pitfalls

- **Blocking shared infrastructure**: CDN IPs (Cloudflare 104.21.x.x, AWS CloudFront) may legitimately host malicious content but blocking the IP disrupts thousands of legitimate sites.
- **VT score obsession**: Low VT detection count does not mean benign — zero-day malware and custom APT tools often score 0 initially. Check sandbox behavior, MISP, and passive DNS.
- **Missing defanging**: Pasting live IOCs in emails or Confluence docs can trigger automated URL scanners or phishing tools.
- **No expiration policy**: IOCs without TTLs accumulate in blocklists indefinitely, generating false positives as infrastructure is repurposed by legitimate users.
- **Over-relying on single source**: VirusTotal aggregates AV opinions — all may be wrong or lag behind emerging malware. Use 3+ independent sources for high-stakes decisions.
