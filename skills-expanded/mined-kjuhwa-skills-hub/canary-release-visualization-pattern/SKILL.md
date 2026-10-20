---

name: canary-release-visualization-pattern
description: Split-lane visualization showing stable vs canary traffic flow with weighted percentage bands and promotion gates
category: design
triggers:
  - canary release visualization pattern
tags: [design, canary, release, visualization]
version: 1.0.0
---

# canary-release-visualization-pattern

For canary-release dashboards, render two horizontal lanes stacked vertically — the top lane represents the stable (v1) fleet receiving (100 − N)% of traffic, and the bottom lane represents the canary (v2) fleet receiving N%. Animate request tokens as small dots flowing left-to-right along each lane, with the spawn rate on each lane proportional to its weight. Color-code by version (stable = blue/neutral, canary = amber/accent) and let token color shift to red when it encounters an error on the canary side, so failure concentration is immediately visible without reading numbers.

Above the lanes, place a weight slider (0%→100%) tied to the canary percentage, with discrete stop markers at typical rollout stages (1%, 5%, 25%, 50%, 100%). Below the lanes, draw a promotion timeline strip with vertical gate markers — each gate shows the SLO check (error rate, p99 latency, saturation) that must pass before the weight advances. Gates that pass turn green and the canary band visibly widens; gates that fail flash red and the band snaps back to the prior step, making rollback kinetically obvious.

Supplement with a small side panel of live delta metrics (canary error rate − stable error rate, latency delta, etc.) rendered as diverging bars centered on zero. Red bars extending right mean canary is worse; green bars extending left mean canary is better. This delta-centric framing is what separates a canary viz from a generic traffic-split viz: users care about *relative* health, not absolute.
