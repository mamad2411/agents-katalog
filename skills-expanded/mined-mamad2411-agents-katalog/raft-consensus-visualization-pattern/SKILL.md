---

name: raft-consensus-visualization-pattern
description: Multi-panel layout for visualizing Raft consensus state across leader election, log replication, and term progression
category: design
triggers:
  - raft consensus visualization pattern
tags: [design, raft, consensus, visualization, replication]
version: 1.0.0
---

# raft-consensus-visualization-pattern

Raft consensus visualizations should be organized around three synchronized panels that reflect the protocol's core mechanics: a cluster topology view showing nodes colored by role (Leader=gold, Follower=blue, Candidate=orange), a log/term timeline showing per-node state history, and an event stream showing RPC messages (RequestVote, AppendEntries) flowing between nodes. Each node should display its current term, votedFor, commitIndex, and lastApplied as a compact state card, with role transitions animated via color morphing rather than abrupt swaps so viewers can trace the causal chain.

Message flow must be rendered as directional arrows with explicit RPC type labels and acknowledgment status — failed/timed-out RPCs shown as dashed red lines, successful quorum acknowledgments as solid green. For leader election specifically, highlight the split-vote and majority-win scenarios with a vote-tally ring around each candidate. For log replication, use a horizontal log strip per node with matched indices aligned vertically, so divergence between leader and followers is visually obvious (mismatched entries highlighted, truncation points marked).

Term timelines should be the anchor axis — a horizontal band at the top showing term boundaries, election timeouts, and leader tenure per term. All three panels share this timeline via a playhead cursor, so scrubbing shows simultaneous state across topology, logs, and events. Speed controls (0.25x–4x) and step-forward buttons let viewers pause at critical moments like election timeout expiry, vote granting, or commit index advancement.
