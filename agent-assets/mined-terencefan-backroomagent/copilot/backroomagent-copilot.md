# BackroomAgent Guidelines

## System Architecture
Text-adventure game system composed of three main services:
1.  **Agent Core**: Python monolith (`backroom_agent/`) exposing a FastAPI server (`server.py`) and orchestrating LangGraph logic (`graph.py`).
2.  **Frontend**: React + Vite application (`frontend/`) simulating a retro terminal interface.
3.  **Data Pipeline**: Go service (`go_agent/`) and Python Subagents (`backroom_agent/subagents/`) for data scraping and analysis.

## Critical Data Protocols
**Strict type synchronization** is enforced across the stack. The source of truth is `PROTOCOL.md`.
Any change to Game State, Events, or Item schemas must be reflected simultaneously in:
- `PROTOCOL.md` (Definition)
- `backroom_agent/protocol.py` (Python Pydantic Models)
- `frontend/src/types.ts` (TypeScript Interfaces)
- `go_agent/agent/model/state.go` (Go Structs for generation)

## Development Workflows
- **Backend Server**: `make server` (runs `backroom_agent.server` on port 8000).
- **Frontend**: `make client` (runs `frontend` dev server on port 5173).
- **Format & Lint**: `make format` runs Black, Isort, **Pyright**, and ESLint. **Always run this before committing.**
- **Agent Testing**: Use `scripts/run_agent.py` to run agents in isolation (DM loop).
- **Graph Visualization**: `make graph` generates Mermaid/PNG graphs in `tmp/` for debugging agent flows.

## Key Code Patterns

### LangGraph Control Flow (`backroom_agent/graph.py`)
The main game loop is a directed graph:
1.  **Router Node**: Delegates to task nodes based on `route_event`.
2.  **Task Nodes**: `Init`, `Inventory`, `Generate` (Main LLM logic).
3.  **Process Node**: Parses LLM output for `LogicEvent`.
4.  **Dice Node**: Executes `d6`/`d20`/`d100` rolls if `LogicEvent` is present.
    - **Loop**: Dice output feeds back into `Generate` node for narrative resolution.
5.  **Summary/Suggest Node**: Standardizes outputs and generates next-step suggestions.

### Python Strict Typing
The codebase enforces static type checking via **Pyright** (the engine behind Pylance).
- **Setup**: Configured in `pyproject.toml`. Runs via `make format`.
- **TypedDict vs Pydantic**: Graph state is a `TypedDict` (`backroom_agent.state.State`), but logic events are Pydantic models (`backroom_agent.protocol`).
- **Casting**: Use `typing.cast` when accessing complex objects from the State dict to satisfy the type checker.
  ```python
  logic_event = state.get("logic_event")
  if logic_event:
      logic_event = cast(LogicEvent, logic_event) # Essential for type safety
  ```
- **Optional Handling**: Explicitly annotate `Optional` types and use assertions (`assert self.x is not None`) after initialization methods.

### Vector Store (`backroom_agent/utils/vector_store/`)
- Uses a custom `PickleVectorStore` for lightweight, file-based persistence.
- **Lazy Loading**: Embeddings/Models are loaded only when needed. Ensure resources are initialized before use.
- **Incremental Updates**: The store supports partial updates via `update_index`.

### Frontend Logic Locking (`useGameEngine.ts`)
To prevent spoilers (narrative appearing before dice animation finishes):
- `lastLogicMsgIdRef` tracks active logic/dice events.
- `tryProcessQueue` **blocks** incoming message chunks if a Logic Event is pending verification.
- Only `DICE_ROLL` chunks can bypass the lock to trigger animation.

### Subagents (`backroom_agent/subagents/`)
Specialized agents (e.g., `level_agent`) run as independent graphs for specific tasks like data ingestion.
- **Structure**: Each subagent has its own `graph.py`, `state.py`, and `nodes/` folder.
- **Isolation**: They do not share the main game loop state but may share `utils` and `tools`.

## Best Practices
- **Configuration**: Use `backroom_agent.constants`. Avoid raw `os.getenv`.
- **Dependency Management**: New dependencies must also include type stubs (e.g., `types-requests`) in `requirements.txt`.
- **References**: Item/Entity refs are strictly strings (IDs), not nested objects.

### Logging Standards
All services must adhere to the logging standards defined in the `logger-generator` skill (`.github/skills/logger-generator/SKILL.md`).
- **Dual Output**: Colored console for development + Daily rotating plain-text files for production.
- **Format**: Must include Timestamp (ms), Level, File:Line, and Module.
- **Python**: Use the pre-configured `backroom_agent.utils.logger`.

### Automated Version Control
You MUST perform a git commit at the end of EVERY task execution or turn that involves code modifications.
1.  **Summarize**: Generate a concise summary of the task completed.
2.  **Commit**: Execute `git add .` followed by `git commit` using the `git-committer` skill standards.
3.  **Report**: Inform the user that the task has been summarized and committed.



