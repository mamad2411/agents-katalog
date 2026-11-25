---

name: saga-pattern-visualization-pattern
description: Visualize saga transaction flows with step states, compensation paths, and forward/backward progress indicators
category: design
triggers:
  - saga pattern visualization pattern
tags: [design, saga, visualization, transaction, visualize]
version: 1.0.0
---

# saga-pattern-visualization-pattern

Saga pattern visualizations must render two parallel timelines: the forward execution path (T1→T2→T3→Tn) and the compensation path (C3→C2→C1) that unwinds completed steps in reverse order when a later step fails. Each step node should expose four visual states — Pending (gray/dashed), Executing (pulsing blue), Completed (solid green), Failed (red), Compensating (amber, reverse arrow), Compensated (strikethrough green) — so viewers can distinguish "never ran" from "ran and rolled back." Use directed arrows with distinct stroke styles: solid for forward transitions, dashed reversed arrows for compensation hops, and dotted for choreography events flowing through a broker.

For orchestrator-flow visualizations, center a coordinator node with radial fan-out to participant services; annotate each edge with the command name (e.g., `ReserveInventory`) and response type (`Confirmed`/`Rejected`). For choreography-swarm visualizations, draw participants on a ring with the event bus as a central hub, and animate event envelopes traveling between them — this makes the absence of a central coordinator legible. For compensation-ledger visualizations, render a append-only ledger strip below the step timeline where each entry shows `{sagaId, stepId, direction: forward|compensate, timestamp}`, letting viewers scrub through ledger state to replay recovery.

Always surface the saga-level invariant panel: current saga state (Running/Compensating/Completed/Aborted), pivot step (the step after which compensation is no longer possible for non-compensatable actions), and a consistency gauge showing how many participants have acknowledged the current phase. Color-code by saga instance ID with stable hashing so concurrent sagas remain distinguishable when overlaid.
