---
name: intel-mitre-coveragemap
description: "Intel Mitre Coveragemap."
domain: cybersecurity
---

|
| Command and Scripting Interpreter | T1059 | Very High | Requires script block logging |
| Phishing | T1566 | Very High | Email gateway integration |
| Valid Accounts | T1078 | High | Baseline behavior needed |
| Process Injection | T1055 | High | Requires Sysmon or EDR |
| Lateral Movement (RDP/SMB) | T1021 | High | Network segmentation visibility |
| Scheduled Task/Job | T1053 | High | Event log collection |
| Data Encrypted for Impact | T1486 | High | File system monitoring |
| Ingress Tool Transfer | T1105 | Medium | Network traffic analysis |

### Step 5: Build Detection Roadmap

```
Quarter 1: Close Critical Gaps (Score 0, High Prevalence)
  Week 1-2: Enable missing data sources
  Week 3-4: Build and test rules for top 5 gap techniques
  Week 5-8: Validate with adversary emulation
  Week 9-12: Tune and operationalize

Quarter 2: Improve Partial Coverage (Score 25-50)
  - Upgrade existing rules with enrichment
  - Add secondary detection methods
  - Validate with purple team exercises

Quarter 3: Mature Good Coverage (Score 50-75)
  - Add behavioral analytics
  - Implement detection-as-code pipeline
  - Cross-technique correlation rules

Quarter 4: Excellence (Score 75-100)
  - Continuous testing with BAS tools
  - Automated coverage regression testing
  - Red team validation
```

## Automated Coverage Assessment

### Data Source to Technique Mapping

```python
# Map available data sources to detectable techniques
DATA_SOURCE_TECHNIQUE_MAP = {
    "Windows Security Event Log": [
        "T1110", "T1078", "T1053.005", "T1098", "T1136",
        "T1070.001", "T1021.001", "T1543.003"
    ],
    "Sysmon": [
        "T1055", "T1059", "T1003", "T1547.001", "T1036",
        "T1218", "T1105", "T1071"
    ],
    "Network Traffic (Firewall/IDS)": [
        "T1071", "T1048", "T1105", "T1572", "T1090",
        "T1571", "T1573"
    ],
    "DNS Logs": [
        "T1071.004", "T1568", "T1583.001", "T1048.003"
    ],
    "Email Gateway": [
        "T1566.001", "T1566.002", "T1534"
    ],
    "Cloud Audit Logs": [
        "T1078.004", "T1537", "T1530", "T1580",
        "T1087.004", "T1098.001"
    ],
}
```

## Reporting Dashboard Queries

### Coverage Summary by Tactic

```spl
| inputlookup mitre_coverage_lookup
| stats avg(score) as avg_score count(eval(score=0)) as no_coverage
    count(eval(score>0 AND score<50)) as partial
    count(eval(score>=50 AND score<75)) as good
    count(eval(score>=75)) as excellent
    count as total
    by tactic
| eval coverage_pct=round((total - no_coverage) / total * 100, 1)
| sort -coverage_pct
```

## References

- [CyberDefenders - MITRE ATT&CK for SOC & DFIR Analysts](https://cyberdefenders.org/blog/mitre-attack-framework/)
- [MITRE ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/)
- [CardinalOps - SIEM Detection Coverage Report 2025](https://www.helpnetsecurity.com/2025/06/09/siem-detection-coverage/)
- [Datadog - Cloud SIEM MITRE ATT&CK Map](https://www.datadoghq.com/blog/cloud-siem-mitre-attack-map/)
- [Picus Security - MITRE ATT&CK Framework Guide](https://www.picussecurity.com/mitre-attack-framework)
