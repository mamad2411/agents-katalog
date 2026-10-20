---

name: schema-registry-visualization-pattern
description: Visualization patterns for schema registry evolution, compatibility, and dependency graphs
category: design
triggers:
  - schema registry visualization pattern
tags: [design, schema, registry, visualization]
version: 1.0.0
---

# schema-registry-visualization-pattern

Schema registry visualizations cluster around three complementary views: a **timeline view** that plots schema versions along a horizontal axis with version nodes colored by compatibility mode (BACKWARD=green, FORWARD=blue, FULL=purple, NONE=red) and annotated with breaking-change markers; a **compatibility matrix** that renders an NxN grid of writer-schema × reader-schema cells, each cell encoding pass/fail plus the specific rule violated (field-removed, type-narrowed, default-missing); and a **subject dependency graph** that uses a force-directed or Sugiyama layout to show subject → referenced-subject edges (Avro `references`, Protobuf imports), with node size proportional to version count and edge thickness proportional to cross-subject field reuse.

The visual grammar should make compatibility semantics legible at a glance. Use diffable field-level overlays on hover: added fields glow green, removed fields strike through red, type-changed fields pulse amber, and default-value changes show an inline `old → new` pill. For timeline views, collapse patch-level versions into expandable clusters to keep the axis readable when a subject has hundreds of versions. Always display the compatibility mode as a persistent badge on the subject header, because the same schema diff is "safe" or "breaking" depending on whether the subject is in BACKWARD, FORWARD, or FULL mode.

Interactivity should mirror the registry's check API: clicking any version pair runs a client-side simulated compatibility check and highlights the exact field paths that would fail, mapping them back to the Avro/Protobuf/JSONSchema rule codes (e.g., `avro-field-removed-no-default`, `protobuf-tag-renumbered`). Keep the rule-code taxonomy in a sidebar legend so users learn the registry's vocabulary while exploring.
