---

name: sidecar-proxy-visualization-pattern
description: Visualize sidecar proxy topology as paired app+proxy nodes with intercepted traffic flows and policy overlays.
category: design
triggers:
  - sidecar proxy visualization pattern
tags: [design, sidecar, proxy, visualization, node, visualize]
version: 1.0.0
---

# sidecar-proxy-visualization-pattern

Render each workload as a two-part unit: a primary application container and its co-located sidecar proxy, drawn as nested or tightly-grouped nodes inside a shared pod boundary (dashed outline). Traffic arrows must always enter and exit through the sidecar, never the app directly — this visually enforces the "transparent interception" invariant. Use distinct stroke styles for inbound vs outbound legs (e.g., solid for ingress, dashed for egress) and color-code by protocol (HTTP/gRPC/TCP) so mTLS upgrades and protocol sniffing decisions are legible at a glance.

Overlay cross-cutting concerns as toggleable layers rather than baking them into the base topology: mTLS handshake indicators on edges, retry/timeout badges on proxy nodes, circuit-breaker state (closed/open/half-open) as node fill color, and rate-limit token buckets as small gauges. For the control plane (xDS/Envoy-style), draw it as a separate pane pushing config down to all sidecars via dotted lines — this makes the "config distribution" vs "data plane traffic" distinction obvious and mirrors the Istio/Linkerd mental model users already carry.

Interactive affordances should let users click a sidecar to see its inbound/outbound listener chain, filter chains, and cluster assignments in a side panel. Animate individual requests as pulses traveling app→sidecar→network→remote sidecar→remote app, pausing briefly at each hop so viewers can observe where latency, policy checks, and telemetry emission actually happen. This hop-by-hop animation is the single most effective way to teach why the sidecar pattern exists.
