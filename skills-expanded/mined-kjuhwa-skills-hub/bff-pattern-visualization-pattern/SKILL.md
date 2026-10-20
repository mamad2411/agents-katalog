---

name: bff-pattern-visualization-pattern
description: Visualize BFF fan-out by rendering per-client gateways as distinct swim lanes that aggregate multiple backend service calls into a single client response
category: design
triggers:
  - bff pattern visualization pattern
tags: [design, bff, visualization, visualize]
version: 1.0.0
---

# bff-pattern-visualization-pattern

Render the BFF topology as a three-column layout: clients (Web, Mobile, IoT) on the left, dedicated BFF nodes in the middle column, and shared backend microservices (User, Product, Cart, Inventory) on the right. Each BFF node owns its own swim lane so the viewer can visually separate which aggregations belong to which client shape. Draw inbound client→BFF edges as thick solid lines (one request), and BFF→backend edges as thinner dashed lines fanned out in parallel to emphasize that a single client call explodes into N backend calls.

Animate the request lifecycle in three phases so the fan-out/fan-in story is legible: (1) client request arrives at its BFF — highlight the inbound edge and pulse the BFF node, (2) BFF dispatches parallel calls to backends — animate dashed edges simultaneously with staggered arrival times reflecting each backend's latency, (3) BFF composes the trimmed/shaped response — collapse the dashed edges back into the BFF node, then fire a single outbound edge back to the client carrying a payload badge showing reduced size (e.g., "42 KB → 6 KB"). Color-code each BFF by client type (blue=Web, green=Mobile, orange=IoT) and reuse that hue on the outbound response edge so viewers track ownership at a glance.

Always surface three metric overlays on the canvas: per-BFF aggregation count (how many backends this request touched), tail latency (max of parallel backend calls, since BFF waits for the slowest), and payload shaping ratio (backend bytes in vs. client bytes out). These three numbers are the defining value props of the BFF pattern — without them the diagram looks like a generic gateway. Place them as floating labels attached to each BFF node, not in a side panel, so they move with the animation.
