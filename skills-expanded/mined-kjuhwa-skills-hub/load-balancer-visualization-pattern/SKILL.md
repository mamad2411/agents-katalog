---

name: load-balancer-visualization-pattern
description: Canvas/SVG-based real-time visualization for load balancer request distribution across backend pools
category: design
triggers:
  - load balancer visualization pattern
tags: [design, load, balancer, visualization, canvas, svg]
version: 1.0.0
---

# load-balancer-visualization-pattern

Render the load balancer topology as a three-layer visual hierarchy: incoming request stream (left), the balancer node with its active algorithm badge (center), and a fan-out of backend servers with health/load indicators (right). Each backend should expose at least four visual channels — a fill-level bar for current connection count, a color ramp (green→amber→red) for CPU/latency, a pulsing ring when a request is actively being serviced, and a dimmed/struck-through state for unhealthy or drained nodes. Draw the routing decision as an animated path from the balancer to the chosen backend, with the path color keyed to the algorithm (round-robin=blue, least-connections=green, weighted=purple, ip-hash/consistent-hash=orange) so viewers can trace why each request landed where it did.

For consistent-hash-ring specifically, layer a second view that shows the hash ring as a circle with virtual nodes as tick marks on the circumference; when a request arrives, draw an arc from the request's hash position clockwise to the owning virtual node. When nodes are added or removed, highlight only the arc segments whose ownership changed — this is the visual payoff that distinguishes consistent hashing from modulo sharding and must be preserved. Always keep a small "algorithm comparison" sidebar with live counters (requests served, std-dev of load, rebalance cost) so viewers can connect the animation to quantitative outcomes.

Keep the animation frame budget tight: cap request particles at ~200 concurrent, use `requestAnimationFrame` with a fixed timestep for the simulation and interpolate rendering between ticks, and debounce backend metric redraws to 10 Hz. Use a single `<canvas>` for particles and an overlay SVG for static topology — mixing everything in SVG collapses at >50 concurrent requests.
