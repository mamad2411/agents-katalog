---
name: msk-analyze-brokers
description: Analyze Amazon MSK Provisioned broker topology, broker type, availability-zone distribution, Kafka configuration, broker health, CPU, network, partition load, and rolling changes. Use for broker-specific performance or availability investigations.
---

# Analyze Brokers

1. Confirm the cluster is Provisioned and identify Standard or Express broker type.
2. Map brokers across Availability Zones and inspect broker-level health and load.
3. Review relevant Kafka configuration and recent broker/configuration changes.
4. Inspect partition distribution and broker-specific hotspots.
5. Correlate broker evidence with producer, consumer, and storage signals.
6. Avoid raw-host tuning recommendations that AWS manages on behalf of MSK customers.

## Output
- Broker Topology
- Health/Load Findings
- Configuration Findings
- Hotspot Assessment
- Recommended Action
