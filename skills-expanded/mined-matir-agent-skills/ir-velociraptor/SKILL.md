---
name: ir-velociraptor
description: Endpoint visibility, digital forensics, and incident response using Velociraptor Query Language (VQL).
metadata:
  version: 0.2.0
  category: incident-response
---
# Velociraptor Incident Response

## Quick Start
```bash
# Standalone mode (GUI)
velociraptor gui

# Create offline collector
velociraptor artifacts collect Windows.KapeFiles.Targets --output collection.zip
```

## Workflow
1. **Deployment**: Deploy Velociraptor clients or run a standalone GUI for triage.
2. **Investigation**: Select relevant VQL artifacts (Process, Network, Persistence) for the scenario.
3. **Hunting**: Create and execute hunts across the infrastructure for specific IOCs.
4. **Collection**: Use offline collectors for evidence preservation on target endpoints.
5. **Analysis**: Build timelines and correlate findings to identify TTPs and impact.

## Rules & Constraints
- **RULE-1**: Implement data minimization; only collect necessary forensic evidence.
- **RULE-2**: Encrypt evidence archives for transport and storage.
- **RULE-3**: Monitor endpoint performance impact during large-scale hunts.
- **RULE-4**: Document chain of custody for all forensic collections.

## When to Use
- Active incident response requiring endpoint evidence collection.
- Proactive threat hunting for indicators of compromise.
- Live response and digital forensics across enterprise infrastructure.

## When NOT to Use
- Network-only analysis without endpoint access.
- Real-time blocking (use EDR for automated prevention).

## References
- [Skill Manual](references/ir-velociraptor-manual.md)
- [VQL Reference](https://docs.velociraptor.app/vql_reference/)
- [Artifact Exchange](https://docs.velociraptor.app/exchange/)
