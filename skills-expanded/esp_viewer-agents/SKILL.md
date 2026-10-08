# esp_viewer Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-04-20

## Active Technologies

- Python 3.9+ + FastAPI, uvicorn, PySide6, pyserial — declared in `pyproject.toml`

## Project Structure

```text
esp_viewer/
├── core/
│   ├── protocol.py      # CommandType, EventType, Packet, JsonRpc enums
│   ├── backend.py       # DeviceService (threading.Thread) — main business logic
│   ├── drivers.py       # SerialDriver / MockDriver — raw I/O only
│   └── mock_device.py   # MockDevice — in-process device simulator
├── web/
│   └── web_adapter.py   # WebAdapter — WebSocket bridge (FastAPI)
├── ui/
│   └── pyside_adapter.py # PySideAdapter — Qt bridge
└── __init__.py          # version string
pyproject.toml
CHANGELOG.md
docs/
├── protocol.md
└── agent_guide.md
```

## Commands

```bash
# Run with mock device (no hardware needed)
PYTHONPATH=. python3 -m esp_viewer --mock --web --force --profile esp_viewer/assets/examples/multi_plot_demo.json

# Run all tests
PYTHONPATH=. python3 -m unittest discover tests

# Build Vue frontend (only if web/src/ changed)
cd esp_viewer/web && npm run build
```

## Architecture

Three strict layers — do NOT short-circuit:
- **Device Layer** (`core/drivers.py`): raw I/O only
- **Engine Layer** (`core/backend.py`, `core/protocol.py`): parsing, IPC, business logic
- **Frontend Layer** (`web/`, `ui/`): rendering only — adapters are the only bridge

## Code Style

- Python 3.9+, 4-space indent, snake_case
- `CommandType` and `EventType` are `enum.Enum` in `core/protocol.py`
- All new `EventType` values go in `protocol.py`; all new `CommandType` values go in `protocol.py`
- `DeviceService._handle_command()` is the single dispatch point for all commands
- `BaseFrontendAdapter.on_event_received()` is the single dispatch point for all events

## Versioning (non-negotiable)

Every change MUST bump version in BOTH `pyproject.toml` AND `esp_viewer/__init__.py`, and add a `CHANGELOG.md` entry.

## Recent Changes

- 002-generic-rpc-transport: Added Python 3.9+, FastAPI, uvicorn, PySide6, pyserial

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
