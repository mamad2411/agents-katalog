# AGENTS.md

## Purpose
- This repo has two tracks: a Pygame chess UI (`src/chesspoint72/app`, `src/chesspoint72/ui`) and a UCI engine + orchestration stack (`src/chesspoint72/engine`, `mcp_orchestrator`).
- Optimize for protocol-correct, measurable engine work; avoid speculative refactors that bypass existing seams.

## Architecture At A Glance
- UI flow: CLI in `src/chesspoint72/main.py` builds `GameConfig` -> `GameController.run()` drives event loop and rendering.
- State model: `GameState` (`src/chesspoint72/models.py`) is the legality gate (`push_move`, `push_uci`) and owns move history.
- Engine boundary: UI calls external engines only through `UciEngineClient` (`src/chesspoint72/engine/uci_client.py`).
- UCI protocol server: `UciController` (`src/chesspoint72/engine/uci_controller.py`) handles `uci/isready/position/go/quit`; subclasses bind position/go behavior.
- Current engine executable (`src/chesspoint72/engine/main.py`) is a shim using python-chess and random legal moves.
- Search seam is pluggable: `Search`, `Evaluator`, `MoveOrderingPolicy`, `PruningPolicy`, `TranspositionTable`.

## Entry Points And Commands
- Install dev deps: `pip install -e .[dev]`.
- Run UI: `python -m chesspoint72.main --engine /path/to/engine --engine-color black --movetime 0.2`.
- Run engine (UCI stdio): `python -m chesspoint72.engine`.
- Run MCP server: `python -m mcp_orchestrator.mcp_server`.
- Run tests: `pytest`.

## Project-Specific Patterns
- Prefer dataclasses for stateful adapters (`GameConfig`, `GameState`, `UciEngineClient`, TT entries).
- Keep protocol parsing separate from search internals: `UciController` for dispatch, search code behind board/search abstractions.
- Engine internals use custom `Move` (`src/chesspoint72/engine/types.py`), not `chess.Move`; convert only at boundaries.
- `NegamaxSearch` (`src/chesspoint72/engine/negamax.py`) expects fast make/unmake, zobrist hashing, and legal move generation.
- Move ordering is heuristic-first (`src/chesspoint72/engine/move_sorter.py`, `src/chesspoint72/engine/heuristics.py`); preserve TT-first and killer/history behavior.

## Required Validation Workflow (`CLAUDE.md`)
- Move-generation changes: MUST run `run_perft` (see `mcp_orchestrator/mcp_server.py`, `validators/perft_runner.py`).
- Search/eval changes: MUST run `play_sprt_match` and use LLR decision as acceptance criterion.
- Tactical-strength-impacting changes: MUST run `run_tactics` using an EPD suite (`tournaments/epd_suite.py`).
- Before finishing: append prompt/process + token-efficiency notes to `AI_PROCESS.md`.

## Integration Points
- External engines are invoked via python-chess (`chess.engine.SimpleEngine`) and subprocess wrappers (`validators/uci_parser.py`).
- Orchestrator tools return `{ok, ...}` / `{ok: false, error}` dict contracts; keep stable for automation.
- Tool telemetry is written by `@track(...)` in `mcp_orchestrator/metrics.py` to `mcp_orchestrator/metrics/calls.jsonl`; dashboard depends on this schema.

## Where To Implement Changes
- UI turn/input flow: `src/chesspoint72/app/controller.py`; rendering/square mapping: `src/chesspoint72/ui/renderer.py`.
- UCI protocol behavior: `src/chesspoint72/engine/uci_controller.py`, `src/chesspoint72/engine/main.py`.
- Search/ordering/pruning/TT: `src/chesspoint72/engine/negamax.py`, `src/chesspoint72/engine/move_sorter.py`, `src/chesspoint72/engine/transposition.py`.
- Regression anchors: `tests/test_engine_base.py`, `tests/test_controller.py`, `tests/test_models.py`, `tests/test_uci_client.py`.
