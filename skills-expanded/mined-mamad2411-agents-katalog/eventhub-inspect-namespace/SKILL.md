---
name: eventhub-inspect-namespace
description: Inspect Azure Event Hubs namespace configuration, tier, capacity model, networking, availability-zone behavior, geo-replication, event hubs, consumer groups, and account-level context. Use as the general Event Hubs entry point when namespace scope or configuration must be resolved.
---

# Inspect Namespace

1. Read `.digital-platform-ai/eventhub.yaml`, service metadata, environments, and relevant instructions.
2. Resolve the target namespace, region, tier, event hub, and consumer group.
3. Inspect:
   - namespace tier and capacity mode
   - throughput/processing capacity configuration
   - network/private endpoint settings
   - availability-zone posture
   - geo-replication configuration
   - event hubs and consumer groups
4. Identify whether the issue is namespace-, event-hub-, partition-, producer-, or consumer-scoped.
5. Route to focused Event Hubs skills based on evidence.
6. Do not modify namespace configuration unless explicitly authorized.

## Output
- Namespace Context
- Capacity/Region Configuration
- Event Hub Inventory
- Scope Assessment
- Recommended Next Skill
