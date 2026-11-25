---
name: lang-elixir
description: Elixir OTP behaviors, GenServer state isolation, supervisor strategies, and StreamData property testing.
---

# Elixir OTP Fault Tolerance Contract

## 1. Functional Core & Immutability
- Keep pure domain functions completely decoupled from process state.
- Handle pattern matches exhaustively; do not write catch-all `_` clauses that hide upstream protocol mismatches.

## 2. Process & Supervision Hygiene
- Every worker process must be part of an explicit supervision tree.
- Avoid bottleneck GenServers: do not execute long synchronous work inside `handle_call`.
