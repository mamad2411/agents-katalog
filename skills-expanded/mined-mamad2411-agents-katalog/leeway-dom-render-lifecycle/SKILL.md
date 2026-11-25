---
name: leeway-dom-render-lifecycle
description: Browser DOM/style/layout/paint/composite lifecycle engineering for events, observers, scheduling, invalidation and zero-unnecessary-layout architecture.
license: MIT
---
# LeeWay DOM & Render Lifecycle
Understand event/input → script → style → layout → paint → composite. Avoid forced synchronous layout/read-write thrash; batch/schedule work; use observers appropriately; reduce DOM/style complexity. Transform/opacity often composite efficiently but do not guarantee GPU promotion or jank-free execution—measure the target browser/device.