---
name: intel-analysis-landscape
description: "-|"
domain: cybersecurity
---
-|
"""
    for i, tech in enumerate(data.get("common_techniques", [])[:15], 1):
        actors = ", ".join(tech["actors_using"][:3])
        report += f"| {i} | {tech['technique']} | {tech['name']} | {actors} |\n"

    vectors = data.get("attack_vectors", {})
    report += f"""
## Attack Vectors
### Primary Vectors
"""
    for v in vectors.get("primary", []):
        report += f"- {v}\n"
    report += "\n### Emerging Vectors\n"
    for v in vectors.get("emerging", []):
        report += f"- {v}\n"

    report += """
## Recommendations
1. Prioritize detections for the top 10 techniques used by sector-targeting groups
2. Conduct threat-informed red team exercises mimicking identified actors
3. Join sector ISAC for real-time threat sharing
4. Implement controls for identified initial access vectors
5. Review supply chain security posture for sector-specific risks
"""
    with open(f"threat_landscape_{data['sector']}.md", "w") as f:
        f.write(report)
    print(f"[+] Sector report saved: threat_landscape_{data['sector']}.md")

generate_sector_report(assessment)
```

## Validation Criteria

- Sector-specific threat actors identified and profiled
- Common techniques across actors analyzed and ranked
- Attack vectors mapped for the target sector
- Emerging threats identified based on recent intelligence
- Comprehensive sector threat report generated
- Recommendations actionable for security investment decisions

## References

- [MITRE ATT&CK Groups](https://attack.mitre.org/groups/)
- [Verizon DBIR](https://www.verizon.com/business/resources/reports/dbir/)
- [CrowdStrike Global Threat Report](https://www.crowdstrike.com/global-threat-report/)
- [FS-ISAC Financial Sector](https://www.fsisac.com/)
- [H-ISAC Healthcare Sector](https://h-isac.org/)
- [CyCognito: Threat Intelligence Lifecycle](https://www.cycognito.com/learn/threat-intelligence/)
