---
name: intel-feeds-feedintegr
description: "Intel Feeds Feedintegr."
domain: cybersecurity
---

--|
| **STIX 2.1** | Structured Threat Information Expression — standardized JSON format for sharing threat intelligence objects |
| **TAXII** | Trusted Automated eXchange of Indicator Information — transport protocol for sharing STIX data via REST API |
| **TIP** | Threat Intelligence Platform — centralized system for aggregating, scoring, and distributing threat intelligence |
| **IOC Scoring** | Process of assigning confidence values to indicators based on source reliability and corroboration |
| **Feed Deduplication** | Removing duplicate IOCs across multiple sources while preserving multi-source attribution |
| **IOC Expiration** | Time-to-live policy removing aged indicators (IP: 30 days, Domain: 90 days, Hash: 1 year) |

## Tools & Systems

- **MISP**: Open-source threat intelligence platform for feed aggregation, correlation, and sharing
- **AlienVault OTX**: Free threat intelligence sharing platform with community pulse feeds
- **Abuse.ch**: Suite of free threat feeds (URLhaus, MalwareBazaar, Feodo Tracker, ThreatFox)
- **OpenCTI**: Open-source cyber threat intelligence platform supporting STIX 2.1 native storage
- **TAXII2 Client**: Python library for connecting to STIX/TAXII 2.1 servers for automated indicator retrieval

## Common Scenarios

- **New Feed Onboarding**: Evaluate feed quality, map fields to STIX, configure automated ingestion pipeline
- **Multi-SIEM Distribution**: Push normalized IOCs from MISP to Splunk, Elastic, and Sentinel simultaneously
- **False Positive Reduction**: Score IOCs by source count and age, expire stale indicators automatically
- **Feed Quality Audit**: Compare detection match rates across feeds to identify highest-value sources
- **Incident IOC Sharing**: Package investigation IOCs as STIX bundle and share with ISACs via TAXII

## Output Format

```
THREAT INTEL FEED STATUS — Daily Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Date:         2024-03-15
Total IOCs:   45,892 active indicators

Feed Health:
  Feed                  IOCs    Matches  Match Rate  Status
  Abuse.ch URLhaus      12,340  47       0.38%       HEALTHY
  AlienVault OTX        18,567  23       0.12%       HEALTHY
  Abuse.ch Feodo        1,203   12       1.00%       HEALTHY
  CISA AIS              8,945   8        0.09%       HEALTHY
  CrowdStrike Intel     4,837   31       0.64%       HEALTHY

Actions Today:
  New IOCs ingested:    1,247
  IOCs expired:         892
  Duplicates removed:   156
  SIEM matches:         121 notable events generated
  False positives:      3 (CDN IPs removed from feed)
```
