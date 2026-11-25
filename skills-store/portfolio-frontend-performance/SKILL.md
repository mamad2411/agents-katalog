---
name: portfolio-frontend-performance
description: "Measure and improve animated frontend or WebGL performance."
---

# portfolio-frontend-performance

Preserve visual intent and measure before/after on comparable environments. Prefer transform/opacity animation, limit layout work, and manage will-change deliberately. Lazy-load heavy work when it improves actual rendering behavior; follow installed Next.js docs for client dynamic imports and image loading APIs.

Record browser/device/renderer, viewport/DPR, warm-up, and frame-time distribution. Headless software rendering is not a device benchmark. Reuse hot-loop allocations, dispose owned resources, and cap DPR as appropriate. Installed telemetry packages are not evidence of exported measurements.
