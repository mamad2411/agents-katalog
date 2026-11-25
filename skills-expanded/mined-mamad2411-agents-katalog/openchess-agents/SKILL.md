# AGENTS.md

OpenChess is an open-source chess engine written in Rust.

## Context

- Early-stage project; prefer simple, correct Rust over premature optimization.
- Rust module layout and ownership: [ARCHITECTURE.md](ARCHITECTURE.md).
- Agent task board (Phase 2): [research/tasks.md](research/tasks.md) — Lichess/TB/search/throughput first; trained eval **last** ([research/phase2-nn-last-plan.md](research/phase2-nn-last-plan.md)).
- Phase 1 archive (complete SF-family stack + arena + Lichess CLI): [research/tasks-phase1.md](research/tasks-phase1.md).
- Design research lives in `research/` — read those when exploring search/eval ideas.
- Lichess bot integration (CLI only, no TUI): [research/LICHESS.md](research/LICHESS.md) · Phase 2 pillar **L2**.
- Bulk Bot-vs-Bot arena lab (`openchess arena`): [research/ARENA.md](research/ARENA.md) · shipped in Phase 1 (**P11**).
- Stockfish-family paradigm; copy structure from research, not magic constants. Speculative ideas stay in `research/uniqueideas.md`.

## Conventions

- Idiomatic Rust; keep modules small and focused.
- Prefer clarity in board representation, move generation, and search until benchmarks justify complexity.
- Follow standard rust doc standards.
