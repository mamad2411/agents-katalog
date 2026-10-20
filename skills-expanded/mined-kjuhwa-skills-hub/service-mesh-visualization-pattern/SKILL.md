---

name: service-mesh-visualization-pattern
description: Rendering sidecar proxies, control plane, and east-west traffic flows as an interactive topology graph
category: design
triggers:
  - service mesh visualization pattern
tags: [design, service, mesh, visualization]
version: 1.0.0
---

# service-mesh-visualization-pattern

Service mesh visualization requires a layered rendering approach: the data plane (sidecar proxies attached to each workload) sits on one visual tier, while the control plane (xDS/pilot components issuing config) hovers above with dashed config-push arrows pointing down to each sidecar. Render services as rounded rectangles with an attached proxy "ear" (small hexagon) to make the sidecar pattern visually explicit — users should never confuse a service node with its proxy. Use directed edges for L7 request flows with color-coding by protocol (HTTP blue, gRPC purple, TCP gray) and animate packet dots along the edge to convey live throughput.

For mesh-traffic-visualizer and sidecar-proxy-playground, the topology graph should support drill-down: clicking a sidecar reveals its listener/cluster/route config (Envoy-style), and clicking an edge reveals the retry policy, circuit breaker state, and mTLS handshake status. Overlay mode is critical — toggle between traffic-view (RPS, latency heatmap on edges), security-view (mTLS enabled/disabled per edge, SPIFFE identity on nodes), and policy-view (which AuthorizationPolicy or VirtualService applies to each edge). Use force-directed layout with namespace clustering so services in the same namespace gravitate together.

The mesh-policy-composer variant extends this by making edges clickable policy targets: drag-and-drop a policy card onto an edge to attach it, with immediate visual feedback showing affected traffic flows highlighted. Persist camera position and expanded nodes in URL query params so users can share specific mesh views. Always show a legend panel explaining sidecar/ingress-gateway/egress-gateway iconography — mesh topology is unfamiliar to many users and implicit symbolism fails.
