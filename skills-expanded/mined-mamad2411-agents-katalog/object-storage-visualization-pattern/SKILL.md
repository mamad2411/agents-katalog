---

name: object-storage-visualization-pattern
description: Canvas/SVG patterns for visualizing object storage buckets, objects, and replication topologies
category: design
triggers:
  - object storage visualization pattern
tags: [design, object, storage, visualization, replication, canvas]
version: 1.0.0
---

# object-storage-visualization-pattern

Object storage visualizations must represent three distinct abstraction layers simultaneously: the flat bucket namespace (no true hierarchy), synthetic prefix-based "folders" derived from key delimiters (e.g., `photos/2026/`), and the underlying storage class tier (Standard, IA, Glacier, Deep Archive). Use a treemap or icicle chart for prefix exploration where rectangle area encodes cumulative object size and color encodes storage class — this maps naturally to how S3/GCS/Azure Blob actually organize data. Avoid tree-view UIs that imply real directories; instead render prefixes as breadcrumb pills with object-count badges so users retain the mental model that "folders" are a client-side illusion built from key prefixes.

For replication and cost views, use a node-link diagram where nodes are regional buckets (labeled with region code + storage class) and edges are replication rules annotated with RPO, filter prefix, and cross-region egress cost per GB. Animate object flow along edges using particle streams whose density reflects PUT rate, and color-code by replication status (PENDING / REPLICA / FAILED) — this is the only way users can spot stuck replication queues at a glance. For cost simulators, stack bars by cost component (storage, Class-A requests, Class-B requests, egress, early-deletion fees) because users consistently underestimate request and egress costs relative to raw storage.

Always expose the key schema explicitly in the UI (e.g., `{tenant}/{yyyy}/{mm}/{dd}/{uuid}.parquet`) because lifecycle rules, replication filters, and cost attribution all hinge on prefix patterns. Provide a "key pattern editor" with live preview showing which objects match — this is the single most valuable interaction across all three apps.
