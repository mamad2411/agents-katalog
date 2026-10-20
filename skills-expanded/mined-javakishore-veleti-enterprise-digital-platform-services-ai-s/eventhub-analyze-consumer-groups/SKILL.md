---
name: eventhub-analyze-consumer-groups
description: Analyze Azure Event Hubs consumer-group topology, isolation, shared streams, independent offsets, workload ownership, and scaling. Use when multiple applications consume the same event hub or when consumer-group design may cause interference or confusion.
---

# Analyze Consumer Groups

1. Identify all known consuming applications and consumer groups.
2. Map each group to its business/technical purpose.
3. Verify that independent workloads use independent consumer groups where appropriate.
4. Check for accidental consumer-group sharing that creates ownership competition.
5. Review checkpoint stores and processor instances per group.
6. Preserve independent replay and processing requirements.

## Output
- Consumer Group Map
- Ownership/Isolation Findings
- Checkpoint Scope
- Design Risks
- Recommended Topology
