---
name: intel-indicator-ioc
description: "Intel Indicator Ioc."
domain: cybersecurity
---

--|
| **SOAR** | Security Orchestration, Automation, and Response — platform for automating security workflows and integrating disparate tools |
| **Enrichment Playbook** | Automated workflow sequence that adds contextual intelligence to raw security events |
| **Rate Limiting** | API provider restrictions on request frequency (e.g., VT free: 4 requests/minute); pipelines must respect these limits |
| **Composite Confidence Score** | Single score aggregating signals from multiple enrichment sources using weighted formula |
| **Fan-out Pattern** | Parallel execution of multiple enrichment queries simultaneously to minimize total enrichment latency |

## Tools & Systems

- **Cortex XSOAR (Palo Alto)**: Enterprise SOAR with 700+ marketplace integrations including VT, MISP, Shodan, and AbuseIPDB
- **Splunk SOAR (Phantom)**: SOAR platform with Python-based playbooks; native Splunk SIEM integration
- **Tines**: No-code SOAR platform with webhook-driven automation; cost-effective for smaller teams
- **TheHive + Cortex**: Open-source IR/enrichment platform with observable enrichment via Cortex analyzers

## Common Pitfalls

- **Blocking on enrichment latency**: If enrichment takes >5 minutes, analysts start working unenriched alerts, defeating the purpose. Set timeout limits and provide partial results.
- **No caching**: Querying the same IOC 50 times generates unnecessary API costs. Cache enrichment results for 24 hours by default.
- **Ignoring API failures silently**: Failed enrichment calls should be logged and trigger fallback logic, not silently produce empty results that appear as clean IOCs.
- **Automating blocks on enrichment score alone**: Composite scores contain false positives; require human confirmation for blocking decisions against shared infrastructure.
