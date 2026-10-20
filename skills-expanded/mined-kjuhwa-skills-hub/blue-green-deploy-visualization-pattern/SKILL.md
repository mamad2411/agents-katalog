---

name: blue-green-deploy-visualization-pattern
description: Dual-environment (Blue/Active vs Green/Idle) side-by-side canvas with traffic-router arrow and version badges for blue-green deployment dashboards
category: design
triggers:
  - blue green deploy visualization pattern
tags: [design, blue, green, deploy, visualization, deployment]
version: 1.0.0
---

# blue-green-deploy-visualization-pattern

Blue-green deployment UIs should render two mirrored environment panels horizontally — Blue (left, currently serving) and Green (right, staging the new version) — each showing a stack of instance cards with version tag (e.g. v1.4.2 vs v1.5.0), health status dot (healthy/warming/draining), and request-per-second counter. Place a load-balancer/router node above or between the panels with an animated directional arrow (or flowing dots) whose thickness or color encodes the traffic split percentage; during cutover, animate the arrow pivoting from Blue→Green over a configurable duration (3–10s) so users visually internalize the switch moment rather than seeing an instant state flip.

Use a color-locked legend: Blue = #3B82F6 and Green = #10B981 regardless of which side is currently active — do not recolor the "active" side, because the whole point of blue-green is that either color can be active. Instead indicate active status with a glowing border, a "LIVE" pill, and a solid (vs dashed) connection line from the router. Reserve red/amber only for failed health checks or rollback state. Always show a timeline/event strip at the bottom recording the last N switches with timestamps so the current active side has historical context.

Include three secondary panels: (1) a "pre-cutover checklist" (smoke tests passed, warm-up complete, DB migrations compatible), (2) a rollback button that is visually prominent only while the new side has been live for less than the rollback-window (e.g. 15 min), and (3) a connection-draining progress bar on the side being retired, since blue-green cutovers are not truly instant — in-flight requests on the old side must complete before it can be reclaimed.
