# Virtual HIL Framework - Gemini Context

This document provides essential context and instructions for AI agents working on the Virtual HIL (Hardware-in-the-Loop) Framework.

## Development Commands

### Package Management (uv)
```bash
uv sync                    # Install dependencies
uv sync --dev             # Install with dev dependencies
uv run <command>          # Run command in virtual environment
```

### Running Tests

```bash
# Run all Robot Framework tests
uv run robot --pythonpath ./libraries:./ecu_simulation --outputdir reports tests/

# Run specific test file
uv run robot --pythonpath ./libraries:./ecu_simulation --outputdir reports tests/functional/test_battery_monitoring.robot

# Run tests by tag
uv run robot --pythonpath ./libraries:./ecu_simulation --outputdir reports --include smoke tests/
uv run robot --pythonpath ./libraries:./ecu_simulation --outputdir reports --exclude slow tests/

# Run unit tests (pytest)
uv run pytest tests/ -v

# Run single unit test
uv run pytest tests/unit/test_battery_ecu.py::test_soc_calculation -v
```

### Starting ECU Server

```bash
# Start FastAPI ECU server (for HTTP-based testing)
uv run python -m ecu_simulation.battery_ecu_server

# Once running, access:
# - http://localhost:8000/docs (Swagger UI)
# - http://localhost:8000/health (Health check)
# - http://localhost:8000/ecu/status (Full ECU status)
```

### Docker

```bash
# Start all services
docker-compose up -d

# Start with specific profile
docker-compose --profile test up -d

# Run tests
docker-compose --profile test run --rm test-runner

# View logs
docker-compose logs -f ecu-server
docker-compose logs -f test-runner
```

### Code Quality

```bash
# Lint with ruff
uv run ruff check .

# Format with ruff
uv run ruff format .

# Type check with mypy
uv run mypy ecu_simulation/ libraries/
```

## Architecture Overview

This is a **Hardware-in-the-Loop (HIL) testing framework** for automotive ECUs that enables Software-in-the-Loop (SIL) testing through virtual ECU simulation.

### Three-Tier Architecture

```
┌─────────────────────────────────────────────────────┐
│  Test Layer: Robot Framework Tests / Python Tests   │
├─────────────────────────────────────────────────────┤
│  Library Layer: Robot Framework Libraries           │
│  - ECUSimulatorLibrary (direct Python imports)      │
│  - ECUSimulatorHTTPLibrary (HTTP REST API)          │
│  - CANLibrary, DiagnosticLibrary, FaultInjectionLib │
├─────────────────────────────────────────────────────┤
│  Simulation Layer: ECU Simulators                   │
│  - BatteryECU, DoorECU, CANInterface, DiagnosticSrv │
└─────────────────────────────────────────────────────┘
```

### Key Design Patterns

**Dual Interface Approach**: The framework supports two testing approaches:
1. **Direct Import** (`ECUSimulatorLibrary`): Libraries import ECU classes directly for unit testing
2. **HTTP REST API** (`ECUSimulatorHTTPLibrary`): Libraries communicate via HTTP for integration/HIL testing with separate processes

This enables realistic HIL testing where the test runner and ECU simulator run in separate processes, similar to real hardware setups.

### ECU Simulation Structure

All ECU classes follow this pattern:
- `__init__(config_path)`: Initialize with optional YAML config
- `start()` / `stop()`: Async lifecycle methods
- `check_faults()`: Return list of active fault codes
- `get_dtc()`: Return Diagnostic Trouble Code if any fault exists
- `to_dict()`: Export state as dictionary

### Communication Interfaces

- **CAN Interface** (`can_interface.py`): Virtual CAN 2.0 bus with message logging and callback registration
- **Diagnostic Server** (`diagnostic_server.py`): UDS (ISO 14229) diagnostic protocol implementation
- **FastAPI Server** (`battery_ecu_server.py`): REST API for HTTP-based testing

## Module Relationships

```
ecu_simulation/
├── battery_ecu.py          # Battery ECU (BMS) simulation
├── battery_ecu_server.py   # FastAPI wrapper for Battery ECU
├── door_ecu.py             # Door ECU (BDC) simulation
├── can_interface.py        # Virtual CAN bus
├── diagnostic_server.py    # UDS diagnostic server
└── rest_interface.py       # REST API (optional)

libraries/
├── ECUSimulatorLibrary.py        # Direct import interface
├── ECUSimulatorHTTPLibrary.py    # HTTP REST interface
├── CANLibrary.py                 # CAN communication
├── DiagnosticLibrary.py          # UDS diagnostics
└── FaultInjectionLibrary.py      # Fault injection
```

## Testing Workflow

### HTTP-Based Testing (Recommended for Integration)

1. Start ECU server: `uv run python -m ecu_simulation.battery_ecu_server`
2. In another terminal, run tests: `uv run robot tests/functional/test_battery_http.robot`
3. Server runs on `http://localhost:8000`

### Direct Import Testing (Unit Tests)

Use `ECUSimulatorLibrary` - tests directly import and instantiate ECU classes

### CI/CD Testing

The `.github/workflows/sil-ci.yml` workflow:
1. Starts ECU server in background
2. Runs health check to verify startup
3. Runs unit tests (pytest)
4. Runs Robot Framework tests
5. Stops ECU server (always)

## Important Implementation Notes

### Module Imports in Server Code

When running ECU modules via `python -m ecu_simulation.module_name`:
- Use full package imports: `from ecu_simulation.battery_ecu import BatteryECU`
- In uvicorn.run(), use full module string: `"ecu_simulation.battery_ecu_server:app"`

### Async Methods

ECU classes have async `start()`/`stop()` methods. When calling from synchronous code:
```python
import asyncio
await ecu.start()  # In async context
asyncio.run(ecu.start())  # In sync context
```

### Fault Detection

Faults are detected dynamically via `check_faults()`:
- Checks thresholds (voltage, temperature, SOC)
- Returns list of active fault codes
- `get_dtc()` formats first fault as DTC string (e.g., "BMS_OVERVOLTAGE_ACTIVE")

### Configuration

ECU behavior is configurable via `config/ecu_config.yaml` (optional). Default values are hardcoded if config is missing.

## Robot Framework Patterns

### Test File Structure

```robot
*** Settings ***
Documentation     Test description
Resource          ../../resources/common_keywords.robot
Resource          ../../resources/ecu_variables.robot
Library           ECUSimulatorHTTPLibrary    http://localhost:8000

Suite Setup       Start ECU Server
Suite Teardown    Stop ECU Server

*** Test Cases ***
Test Name
    [Documentation]    Test description
    [Tags]    smoke    battery
    # Test steps

*** Keywords ***
Custom Keyword
    # Implementation
```

### Common Test Tags

- `smoke` - Quick validation tests
- `critical` - Core functionality
- `battery` / `door` - ECU-specific tests
- `http` - HTTP API tests
- `integration` - Multi-component tests
- `slow` - Long-running tests

### Resource Files

Located in `resources/`:
- `common_keywords.robot` - Reusable keywords
- `ecu_variables.robot` - ECU constants and limits
- `test_data.robot` - Test data fixtures

## Docker Architecture

### Services

- `ecu-server`: FastAPI server (primary HTTP interface)
- `battery-ecu` / `door-ecu`: Legacy direct ECU sims (profile: `legacy`)
- `test-runner`: Runs Robot Framework tests (depends on `ecu-server`)
- `test-runner-legacy`: Legacy tests using direct imports (profile: `legacy-test`)

### Profiles

- `test`: Run HTTP-based tests
- `legacy`: Run legacy direct-import tests
- `with-api`: Include REST API service

## CAN Message IDs

| ID    | Message           | Description                      |
|-------|-------------------|----------------------------------|
| 0x100 | BMS_Status        | Battery pack status              |
| 0x101 | BMS_Cell_Data     | Individual cell voltages         |
| 0x102 | BMS_Fault         | Battery fault indication         |
| 0x200 | BDC_Door_Status   | Door open/closed and lock status |
| 0x201 | BDC_Door_Position | Door position percentage         |

## UDS Diagnostic Services

Supported services (ISO 14229):
- 0x10: Diagnostic Session Control
- 0x22: Read Data By Identifier
- 0x2E: Write Data By Identifier
- 0x14: Clear DTC
- 0x19: Read DTC
- 0x27: Security Access
- 0x31: Routine Control
- 0x3E: Tester Present
- 0x85: Control DTC Setting
