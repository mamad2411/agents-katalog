---

name: hexagonal-architecture-visualization-pattern
description: Render the hexagon with domain core centered and ports/adapters radiating outward through driving/driven lanes
category: design
triggers:
  - hexagonal architecture visualization pattern
tags: [design, hexagonal, architecture, visualization]
version: 1.0.0
---

# hexagonal-architecture-visualization-pattern

Lay out the hexagonal architecture as a literal hexagon SVG with the domain core (use cases + entities) filling the center, driving ports (HTTP, CLI, gRPC) on the left three edges, and driven ports (DB, message bus, external API) on the right three edges. Each port is a labeled slot on the hexagon boundary; adapters dock into those slots from outside. Color-code by role: domain = neutral/dark for emphasis, ports = accent borders (dashed for driven, solid for driving), adapters = muted fills so the eye stays on the core. Animate a request token sliding from an outer adapter → through the port slot → into a use case → back out through a driven port, pausing briefly at each boundary so viewers see where translation happens.

For hexagonal-dependency-inverter specifically, overlay an arrow layer showing that all arrows point inward toward the domain — never outward. Dim any arrow that would violate DIP (e.g. domain importing adapter) to red and shake it when the user hovers a "show violations" toggle. For hexagonal-request-tracer, thread a persistent trace ID badge onto the token so it carries through every adapter hop, and render a side timeline showing port-entry/exit timestamps. Keep the hexagon geometry fixed across all three demos so users can compare topologies without re-orienting. Avoid box-and-arrow layouts — the hexagon shape itself is load-bearing pedagogy and reinforces that inside/outside is the primary axis, not layers.

Use SVG `<polygon>` for the hex, `<line>` for port slots positioned with trig (60° spacing), and CSS `transform: translate` along a parametric path for the request token animation. Keep adapter count per side ≤2 to avoid label collisions.
