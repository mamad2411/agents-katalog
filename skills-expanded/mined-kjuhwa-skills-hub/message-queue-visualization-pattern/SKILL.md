---

name: message-queue-visualization-pattern
description: Canvas-based rendering pattern for animating message flow through producers, queues, and consumers
category: design
triggers:
  - message queue visualization pattern
tags: [design, message, queue, visualization, canvas]
version: 1.0.0
---

# message-queue-visualization-pattern

Message queue visualizations share a three-lane spatial layout: producers on the left emitting discrete message tokens, a central queue/topic region showing the buffer as an ordered array of slots, and consumers on the right pulling or receiving messages. Each message is rendered as a colored shape (circle for standard, diamond for priority, square for pub/sub broadcast) with a payload ID and timestamp overlay. Animate transitions using easing functions (cubic-bezier) over fixed durations (300-600ms) so the eye can track individual messages; avoid linear interpolation which makes enqueue/dequeue feel mechanical.

For queue-conductor-style FIFO views, render the buffer as a horizontal strip with head/tail pointers and a visible "watermark" line showing high-water backlog. For priority-queue-puzzle, use vertical stacking sorted by priority score with color gradients (red=high, blue=low) and show the re-heapify animation when a higher-priority message arrives. For topic-pubsub-monitor, draw fan-out edges from topic to N subscribers with per-subscriber offset cursors and lag indicators. Always expose play/pause/step controls and a speed slider (0.25x-4x) so users can freeze complex multi-consumer states.

Keep a separate "trace lane" below the main canvas that logs each enqueue/dequeue event with monotonic sequence numbers — this disambiguates visually identical messages and is essential when students debug ordering guarantees. Use requestAnimationFrame driven by a simulation clock (not wall clock) so pause actually pauses and step advances exactly one tick.
