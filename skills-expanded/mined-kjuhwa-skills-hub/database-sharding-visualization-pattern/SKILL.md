---

name: database-sharding-visualization-pattern
description: Canvas-based rendering pattern for visualizing shard topology, key distribution, and routing decisions in database sharding systems
category: design
triggers:
  - database sharding visualization pattern
tags: [design, database, sharding, visualization, canvas]
version: 1.0.0
---

# database-sharding-visualization-pattern

When visualizing database sharding architectures, structure the UI around three concurrent layers: (1) a shard topology layer showing physical/logical nodes as distinct visual containers with capacity indicators, (2) a key-space layer overlaying the hash ring or range partitions with color-coded ownership boundaries, and (3) an animated routing layer that traces individual query paths from the router through hash computation to the destination shard. Use HTML Canvas or SVG with requestAnimationFrame for smooth transitions, and render the hash ring as a circular 0–2^32 keyspace with virtual node markers (typically 100–200 vnodes per physical shard) to make consistent hashing visually coherent.

Expose interactive controls for the three primary failure/rebalance scenarios operators actually care about: adding a shard (show only affected key ranges migrating, not the entire dataset), removing a shard (show redistribution to neighbors on the ring), and hot-spot detection (highlight shards exceeding a load threshold in red with pulse animation). Each control should immediately replay the last batch of simulated keys so users see cause-and-effect. Include a side panel with per-shard metrics — key count, request rate, storage bytes — updated in real time from the simulation tick, and annotate the ring with the specific hash function in use (MD5, Jump Hash, Rendezvous) since the choice dramatically changes distribution properties.

Keep the color palette consistent across all three apps: one hue per shard (stable across re-renders via `shardId → HSL` mapping), red-only for overload/errors, dimmed grey for decommissioned nodes. This lets users build a mental model that transfers between the router-centric view (shard-router-visualizer), the ring-centric view (consistent-hash-ring), and the traffic-flow view (shard-traffic-simulator) without re-learning the visual language.
