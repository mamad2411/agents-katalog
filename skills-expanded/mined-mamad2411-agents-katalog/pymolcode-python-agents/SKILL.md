# python/ — Core Python Package

**Main package for pymolcode.** Contains CLI, agent orchestration, PyMOL bridge, skill system, and authentication.

## Structure

```
python/
├── cli.py              # Main CLI entry (auth, ultrawork commands)
├── agent/              # LLM agent orchestration
│   ├── agent.py        # Agent core logic with memory integration
│   ├── provider.py     # LLM provider abstraction (OAuth + API keys)
│   ├── orchestrator.py # Hephaestus orchestrator (NEW)
│   ├── background.py   # Background agent manager (NEW)
│   ├── tools.py        # Tool definitions (includes memory tools)
│   └── types.py        # Agent type definitions
├── auth/               # OAuth authentication (NEW)
│   ├── __init__.py     # Module exports
│   ├── oauth.py        # OAuth 2.0 flows (PKCE, device code)
│   ├── token_store.py  # Secure token storage (~/.pymolcode/auth.json)
│   └── providers.py    # Provider OAuth configs (10 providers)
├── memory/             # Memory system (YAML-based persistence)
│   ├── store.py        # MemoryStore class
│   ├── tools.py        # MemoryReadTool, MemoryWriteTool
│   └── policy.py       # MemoryPolicy for security
├── bridge/             # JSON-RPC bridge server
│   ├── server.py       # Bridge server main
│   ├── handlers.py     # Request handlers
│   └── analysis.py     # Analysis utilities
├── pymol/              # PyMOL integration
│   ├── executor.py     # Command executor
│   ├── panel.py        # GUI panel plugin
│   └── runtime.py      # PyMOL runtime wrapper
├── session/            # Session management
│   ├── config.py       # Configuration handling
│   ├── schema.py       # Session schemas
│   └── bootstrap.py    # Session initialization
├── skill/              # Skill system
│   ├── base.py         # Skill base classes
│   ├── builtin.py      # Built-in skills
│   ├── registry.py     # Skill registry
│   └── bridge/         # Multi-source skill discovery (NEW)
│       ├── __init__.py     # Module exports
│       ├── discovery.py    # Skill discovery engine
│       └── omo_adapter.py  # Oh-My-OpenCode adapter
├── workflow/           # Agentic workflows (NEW)
│   ├── __init__.py     # Module init
│   └── ultrawork.py    # One-command workflow execution
├── validation/         # Validation utilities (NEW)
│   ├── __init__.py     # Module init
│   └── hash_edit.py    # Hash-anchored command validation
├── protocol/           # JSON-RPC protocol
│   ├── framing.py      # Content-Length framing
│   ├── spec.py         # Protocol specification
│   └── errors.py       # Error types
├── persistence/        # State persistence
└── plugins/            # Plugin loader system
```

## Entry Points

| Module | Function | Called By |
|--------|----------|-----------|
| `cli.py` | `main()` | `pymolcode` console script |
| `bridge/server.py` | `main()` | `pymolcode-bridge` console script |
| `pymol/panel.py` | `__init_plugin__()` | PyMOL plugin entry point |

## New Modules (OAuth + Agentic)

### Authentication (`auth/`)

- **OAuthManager** (`oauth.py`): OAuth 2.0 flows with PKCE support
- **TokenStore** (`token_store.py`): Secure file-based token storage
- **Providers** (`providers.py`): Configs for OpenAI, Google, GitHub Copilot, Anthropic, etc.

### Agentic Layer (`agent/`)

- **Hephaestus** (`orchestrator.py`): Discipline orchestrator for drug discovery
- **BackgroundAgentManager** (`background.py`): Parallel task execution

### Workflow (`workflow/`)

- **run_ultrawork** (`ultrawork.py`): One-command agentic workflow

### Skill Bridge (`skill/bridge/`)

- **SkillDiscovery** (`discovery.py`): Multi-source skill discovery
- **OmOAdapter** (`omo_adapter.py`): Oh-My-OpenCode skill adapter

### Validation (`validation/`)

- **HashValidator** (`hash_edit.py`): Hash-anchored command validation

## Key Files

| File | Purpose |
|------|---------|
| `auth/oauth.py` | OAuth 2.0 flows (device code, authorization code) |
| `auth/token_store.py` | Secure token storage in ~/.pymolcode/auth.json |
| `agent/orchestrator.py` | Hephaestus orchestrator with two-stage review |
| `agent/background.py` | Semaphore-gated parallel execution |
| `memory/tools.py` | Memory read/write tools |
| `memory/store.py` | YAML-based memory storage |
| `bridge/handlers.py` | JSON-RPC method implementations |
| `skill/bridge/discovery.py` | Multi-source skill discovery |
| `skill/bridge/omo_adapter.py` | Oh-My-OpenCode integration |

## Memory System

The memory system provides persistent knowledge storage for the agent:

- **Storage Format**: YAML files in `memory/` directory
- **Components**:
  - `memory.yaml` - Main memory (preferences, knowledge)
  - `lessons.yaml` - Lessons learned from mistakes
  - `now.yaml` - Active todos and priorities
  - `YYYY-MM-DD.yaml` - Daily session notes
- **Integration**: Memory tools registered via `ToolRegistry.register_memory_tools()`
- **Security**: `MemoryPolicy` redacts sensitive data and enforces size limits

## Hephaestus Orchestrator

The Hephaestus orchestrator (`agent/orchestrator.py`) provides:

- **Planning**: Break goals into concrete implementation steps
- **Delegation**: Dispatch tasks to category-specific specialists
- **Review Gates**: Two-stage review (spec compliance + code quality)
- **Completion Enforcement**: Drive all tasks to completion

**Preferred Models**: Claude Opus 4.6/4.5, GPT-5.3/5.2 Codex, GLM-5, Kimi K2.5

## Conventions

- All modules use `from __future__ import annotations`
- Pydantic v2 models for all data structures
- Async functions throughout (no blocking calls)
- Structured logging via `structlog`

## Anti-Patterns

- **NO** direct `pymol.cmd` calls outside `pymol/executor.py`
- **NO** synchronous I/O in async functions
- **NO** hardcoded paths → use `session/config.py` settings
- **NO** untyped dict returns → use Pydantic models

## Testing

```bash
pytest tests/python/           # Unit tests for this package
pytest --cov=python tests/    # Coverage report
```

## Notes

- CLI spawns PyMOL subprocess with plugin injection via temp script
- Bridge uses Content-Length framed JSON-RPC over stdio
- Agent tools integrate with MCP (Model Context Protocol)
- Memory system uses YAML format for persistence (see `memory/` module)
- Agent system prompt includes memory context for learning from mistakes
- OAuth tokens stored in `~/.pymolcode/auth.json` with 0o600 permissions
- Provider resolution order: explicit env → config → env vars → token store
