---

name: domain-driven-visualization-pattern
description: Rendering bounded contexts, aggregates, and ubiquitous language as navigable maps with relationship overlays
category: design
triggers:
  - domain driven visualization pattern
tags: [design, domain, driven, visualization]
version: 1.0.0
---

# domain-driven-visualization-pattern

Domain-driven apps visualize three distinct layers that must be composable but independently inspectable: bounded contexts as containers (boxes with explicit seams), aggregates as clustered nodes inside those containers (with the aggregate root visually distinguished from entities and value objects), and ubiquitous-language terms as annotations that anchor to the nodes where they apply. Use SVG or canvas with a force-directed layout for the aggregate graph inside each context, but lock context containers to a grid or manual positions — contexts are strategic and should not drift, while aggregate internals are tactical and benefit from auto-layout. Overlay context-mapping relationships (Shared Kernel, Customer/Supplier, Conformist, Anti-Corruption Layer, Open Host Service, Published Language) as labeled edges between context boundaries, never between interior aggregates.

Invariant visualization belongs on the aggregate node itself: show each invariant as a pill or badge attached to the root, and when a simulated command violates it, flash the specific invariant red and draw a dotted line to the field(s) that caused the violation. For ubiquitous-language mining, render a term-occurrence heatmap where each term's dot size reflects frequency and color reflects the context it belongs to — a term appearing in multiple contexts with different colors is a visual flag for translation drift. Always provide a "zoom level" control that collapses aggregates into context-only view for strategic discussion, then expands to entity/value-object detail for tactical work; the same component tree should render both by toggling which layer is interactive.

Keep the legend persistent and context-relationship-aware: DDD diagrams are notoriously cryptic to non-practitioners, so hovering a U/D arrow should pop a tooltip explaining "Upstream context's model shapes the downstream's" rather than expecting the viewer to recall the notation.
