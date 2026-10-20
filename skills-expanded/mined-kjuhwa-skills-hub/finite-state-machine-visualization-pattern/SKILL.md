---

name: finite-state-machine-visualization-pattern
description: Render FSM states as a node graph with animated active-state highlighting and transition edge pulses driven by the current state variable.
category: design
triggers:
  - finite state machine visualization pattern
tags: [design, finite, state, machine, visualization, node]
version: 1.0.0
---

# finite-state-machine-visualization-pattern

For FSM visualizations (traffic-light, vending-machine, regex-matcher), model the UI as two layers: a static topology layer that draws all states as nodes and all legal transitions as directed edges, plus a dynamic overlay that highlights the single active state and pulses the edge corresponding to the last-fired transition. Bind the overlay to a single `currentState` reactive variable so every render derives visuals from state — never mutate node styles imperatively. Use distinct visual encodings per state kind: initial states get a double-border or arrow-in, accepting/terminal states get a filled ring, and error/trap states get a muted palette so they're visually recognizable without reading labels.

Position nodes using a deterministic layout (manual coordinates for small FSMs ≤10 states, or dagre/elk for generated graphs like regex-fsm-visualizer where states come from NFA→DFA conversion). For transitions, render self-loops as curved arcs above the node to avoid overlap with incoming edges, and label each edge with its trigger event (`COIN_INSERTED`, `TIMER_EXPIRED`, `char='a'`). When multiple transitions share source/target, stack labels with a small offset rather than overlapping. Keep the state list, transition table, and current-state indicator as sibling panels so users can cross-reference the graph against the tabular definition.

Animate transitions with a short (200–400ms) edge pulse and a node scale/glow on the destination — long animations make rapid FSM stepping feel laggy. Always preserve the previous state's position during the transition so the eye can track movement; never re-layout on state change. For regex-style FSMs where the graph is generated, memoize the layout computation keyed on the regex string so typing doesn't re-layout mid-animation.
