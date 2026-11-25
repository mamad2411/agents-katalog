---

name: pub-sub-visualization-pattern
description: Canvas-based visualization showing topic channels, publishers fanning out messages to multiple subscribers with animated message particles
category: design
triggers:
  - pub sub visualization pattern
tags: [design, pub, sub, visualization, canvas]
version: 1.0.0
---

# pub-sub-visualization-pattern

Pub-sub systems benefit from a three-column layout: publishers on the left, topic/channel brokers in the middle, and subscriber groups on the right. Each publisher emits colored message particles that travel to the broker node, get tagged with a topic label, then fan out along curved Bezier paths to every subscriber bound to that topic. Use distinct hues per topic (e.g., "news.sports" = amber, "news.weather" = cyan) so overlapping flows remain readable, and render subscriber nodes with a small badge counter showing received message count.

The broker node should visually expose its internal topic registry — a stacked list of active topics with subscriber counts — so viewers understand the indirection. Animate message delivery in two phases: publish (publisher → broker, ~300ms) and dispatch (broker → all subscribers in parallel, ~500ms with slight stagger per subscriber to convey fan-out). When a subscriber is offline or has a full queue, render the message particle as dashed/faded and drop it at the subscriber boundary with a small "×" marker rather than silently discarding.

For pub-sub-newsroom, pub-sub-radio-tower, and pub-sub-event-bus-lab, the shared visual vocabulary is: pulsing broker hub, topic-colored particles, fan-out curves, and per-subscriber inbox badges. Always expose subscription lifecycle (subscribe/unsubscribe) as visible edge creation/removal so users can see the decoupling contract — publishers never know who is listening, which is the whole point of pub-sub and must be reinforced by the rendering.
