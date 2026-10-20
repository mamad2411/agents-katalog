---
name: intel-feeds-threat-hunt
description: "--| | **STIX 2.1** | Structured Threat Information Expression — OASIS standard JSON schema for CTI objects including indicators, threat actors, campaigns, and relationships | | **TAXII 2."
domain: cybersecurity
---

--|
| **STIX 2.1** | Structured Threat Information Expression — OASIS standard JSON schema for CTI objects including indicators, threat actors, campaigns, and relationships |
| **TAXII 2.1** | Trusted Automated eXchange of Intelligence Information — HTTPS-based protocol for sharing STIX content between servers and clients |
| **IOC** | Indicator of Compromise — observable artifact (IP, domain, hash, URL) that indicates a system may have been breached |
| **TLP** | Traffic Light Protocol — color-coded classification (RED/AMBER/GREEN/WHITE) defining sharing restrictions for CTI |
| **Confidence Score** | Numeric value (0–100 in STIX) reflecting the producer's certainty about an indicator's malicious attribution |
| **Feed Fidelity** | Historical accuracy rate of a feed measured by true positive rate in production detections |

## Tools & Systems

- **ThreatConnect TC Exchange**: Aggregates 100+ commercial and OSINT feeds; provides automated playbooks for IOC enrichment
- **MISP (Malware Information Sharing Platform)**: Open-source TIP supporting STIX/TAXII; widely used by ISACs and government CERTs
- **OpenCTI**: Open-source platform with native MITRE ATT&CK integration and graph-based relationship visualization
- **Recorded Future**: Commercial feed with AI-powered risk scoring and real-time dark web monitoring
- **taxii2-client**: Python library for TAXII 2.0/2.1 client operations (pip install taxii2-client)
- **PyMISP**: Python API for MISP feed management and IOC submission

## Common Pitfalls

- **IOC age staleness**: IP addresses and domains rotate frequently; applying 1-year-old IOCs generates false positives. Enforce TTL policies.
- **Missing context**: Blocking an IOC without understanding the associated campaign or adversary can disrupt legitimate business traffic (e.g., CDN IPs shared with malicious actors).
- **Feed overlap without deduplication**: Ingesting the same IOC from five feeds without deduplication inflates indicator counts and SIEM rule complexity.
- **TLP violation**: Redistributing RED-classified intelligence outside authorized boundaries violates sharing agreements and trust relationships.
- **Over-blocking on low-confidence indicators**: Indicators with confidence below 50 should trigger detection-only rules, not blocking, to avoid operational disruption.
