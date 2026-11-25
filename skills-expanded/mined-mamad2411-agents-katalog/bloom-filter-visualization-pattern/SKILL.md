---

name: bloom-filter-visualization-pattern
description: Visualizing bloom filter bit arrays, hash function mappings, and false-positive regions for interactive exploration
category: design
triggers:
  - bloom filter visualization pattern
tags: [design, bloom, filter, visualization]
version: 1.0.0
---

# bloom-filter-visualization-pattern

When building an interactive bloom filter explorer, render the underlying bit array as a grid of cells (typically 64-256 bits visible) where each cell reflects its 0/1 state with distinct colors — empty cells neutral, set cells filled, and newly-flipped cells highlighted briefly on insertion. Overlay hash function outputs as colored connector lines or arrows from the input token down to the k bit positions it maps to, using one color per hash function (h1, h2, h3) so users can trace which hash caused which bit flip. This makes the "multiple hashes → multiple bits" invariant visually self-evident rather than abstract.

For query operations, animate the lookup sequence: highlight the k target bits in order, and resolve to either "definitely not present" (any bit is 0, shown in red) or "possibly present" (all bits are 1, shown in amber — never green, since false positives are possible). Surface a live fill-ratio gauge and a computed false-positive probability `(1 - e^(-kn/m))^k` updated after every insertion so users watch the FPR curve climb as the filter saturates. Collision/race variants should additionally color bits that are "shared" by multiple inserted items differently, making the source of false positives tangible.

Keep the visualization deterministic and replay-friendly: expose m (bit array size), k (hash count), and the hash seeds as URL-encoded parameters, and provide step-forward/step-back controls over the operation log. This lets users pause mid-insertion to inspect which hashes are about to fire, which is far more instructive than instant commits.
