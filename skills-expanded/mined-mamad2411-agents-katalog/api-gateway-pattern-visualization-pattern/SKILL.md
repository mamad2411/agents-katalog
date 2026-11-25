---

name: api-gateway-pattern-visualization-pattern
description: Single-pane visualization showing client traffic funneling through a gateway layer that fans out to backend services with per-hop status
category: design
triggers:
  - api gateway pattern visualization pattern
tags: [design, api, gateway, visualization]
version: 1.0.0
---

# api-gateway-pattern-visualization-pattern

For api-gateway-pattern apps (traffic-router, rate-limiter, request-inspector), render a three-column topology: left column holds client pods (browsers/mobile/partner APIs) emitting requests as animated tokens, the center column is a single wide "gateway" rectangle with stacked sub-bands for each concern (auth → rate-limit → route-match → transform → forward), and the right column holds a grid of backend service boxes (users, orders, billing, inventory) each with an independent health pill. Tokens must visibly enter the gateway, traverse each sub-band with a brief pause colored by that stage's verdict (green=pass, amber=throttled, red=rejected, blue=inspected/mirrored), then exit to exactly one backend or terminate inside the gateway on reject.

Keep the gateway band taller than client/backend columns (roughly 55% of canvas height) because the pattern's story is what happens *inside* the gateway — the router variant animates the route-match band with matched path patterns lighting up, the rate-limiter variant animates a token bucket depleting next to the rate-limit band, and the inspector variant pops a side panel showing headers/body diffed against policy. A persistent top strip shows aggregate RPS, p50/p99 latency added by the gateway (never the backend's latency — that's a separate overlay), and a reject-reason breakdown. Avoid drawing direct client→backend arrows; the whole point is that the gateway is the only path, so any arrow bypassing it is a visual bug.

Color semantics stay fixed across all three apps so users switching between them build muscle memory: blue for ingress/inspection, purple for auth, amber for rate-limit/throttle, green for successful forward, red for reject/5xx, gray for mirrored/shadow traffic. Token size encodes payload bytes (log scale) and stroke encodes protocol (solid=HTTP, dashed=gRPC, dotted=WebSocket upgrade) so one legend works for all variants.
