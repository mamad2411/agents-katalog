---

name: actor-model-visualization-pattern
description: Render actor mailboxes, supervision trees, and message flows as live, inspectable graphs
category: design
triggers:
  - actor model visualization pattern
tags: [design, actor, model, visualization]
version: 1.0.0
---

# actor-model-visualization-pattern

Actor-model apps benefit from a split-pane visualization where the left pane shows the supervision hierarchy as a collapsible tree (root supervisor → child supervisors → worker actors) and the right pane shows per-actor mailbox state (queue depth, current message, processed count, restart count). Each actor node should expose four visual states via color coding: `running` (green), `processing` (pulsing blue), `restarting` (amber with a countdown to backoff expiry), and `stopped` (gray). Message envelopes animate along parent→child edges with a short trail so causal order is visible even when throughput is high.

For the mailbox view, render the FIFO queue as a horizontal strip of message cards with sender PID, message type, and enqueue timestamp; when an actor dequeues, slide the head card into a "current" slot and fade it out on completion. Include overlays for the three invariants that matter in actor debugging: (1) one-message-at-a-time per actor (highlight violations in red), (2) let-it-crash boundaries (draw a dashed ring around supervised subtrees and flash the ring on restart), and (3) mailbox backpressure (gradient fill intensifying as queue depth approaches the configured bound).

Keep the visualization driven by an append-only event log (ActorSpawned, MessageSent, MessageReceived, ActorCrashed, ActorRestarted, ActorStopped) rather than by polling actor state. This makes the view replayable: scrubbing a timeline slider re-derives the tree and mailbox state at any past instant, which is essential for explaining supervision semantics to users who are new to the model.
