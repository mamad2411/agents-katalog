---
tags: [backend, session, lock, tree, blocking, chain]
name: session-lock-tree-blocking-chain-modeling
description: Model RDBMS blocking sessions as a directed graph and persist the resolved lock tree alongside the session snapshot
category: backend
version: 1.0.0
trigger: lock contention monitoring, blocking session analysis, RDBMS session graph
source_project: lucida-domain-dpm
---

# Session / Lock-tree blocking chain modeling

A point-in-time session snapshot plus a separate `lockList` encoding `blocker → blocked` edges. Reconstruct the blocking chain by walking edges from the root blockers, not by recursive SQL on the target (too expensive, version-specific).

## Shape
- Collect: `sessionList` (flat) + `lockList` (`blockingTid`, `blockedTid`) in one scrape.
- Resolve: BFS from sessions that appear as `blockingTid` but never as `blockedTid` (roots) to leaves.
- Store both the flat snapshot and the resolved tree — flat is queryable, tree is display-ready.
- For the history collection, persist only sessions that appear anywhere in the tree to keep volume bounded.

## Steps
1. Capture `sessionList` and `lockList` in the same collection tick to avoid skew.
2. Build `Map<Tid, Session>` and `Multimap<blockingTid, blockedTid>`.
3. Identify roots: `blockingTids − blockedTids`.
4. BFS from each root; produce `List<LockTreeNode>` (tid, children).
5. Persist `{sessionList, lockList, lockTree, collectedAt}` as one document.
6. Guardrail: a session can appear as both blocker and blocked — do NOT dedupe the edge set by tid alone.
