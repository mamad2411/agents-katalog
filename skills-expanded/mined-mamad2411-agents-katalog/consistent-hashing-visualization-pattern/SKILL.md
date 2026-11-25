---

name: consistent-hashing-visualization-pattern
description: Ring-based SVG/Canvas rendering pattern for visualizing consistent hashing node placement and key distribution
category: design
triggers:
  - consistent hashing visualization pattern
tags: [design, consistent, hashing, visualization, node, canvas]
version: 1.0.0
---

# consistent-hashing-visualization-pattern

For consistent-hashing visualizations (hash-ring-visualizer, rebalance-simulator, vnode-load-balancer), render the hash space as a circular ring using SVG polar coordinates: convert each hash value `h` in `[0, 2^32)` to an angle `θ = (h / MAX_HASH) * 2π`, then place nodes/keys at `(cx + r*cos(θ), cy + r*sin(θ))`. Use distinct visual layers: outer ring for physical nodes (larger radius, bold markers), inner ring for virtual nodes/replicas (smaller, color-coded by owner), and innermost scatter for keys (tiny dots colored by their assigned node). This layering makes ownership arcs visually obvious — each key's color should match the first clockwise node encountered.

Interaction affordances matter more here than in other visualizations because the core insight of consistent hashing is *locality under change*. Provide toggles for: (a) add/remove node with animated key migration showing only affected keys changing color, (b) vnode count slider that re-renders the ring with N replicas per physical node to demonstrate load smoothing, and (c) a distribution histogram panel adjacent to the ring showing per-node key counts updated live. Highlight the arc owned by a hovered node by drawing a thick stroke between its predecessor hash and its own hash — this teaches the "I own everything up to me clockwise" rule visually.

Keep the hash function deterministic and seedable (FNV-1a or MurmurHash3 in JS) so that the same seed produces identical rings across reloads — essential for comparing before/after states in rebalance demos. Avoid `Math.random()` for key placement; use a seeded PRNG so screenshots are reproducible and tutorial narratives stay coherent.
