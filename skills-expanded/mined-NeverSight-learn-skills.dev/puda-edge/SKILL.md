---
name: puda-edge
description: Creating an edge client to integrate any machine into PUDA. Use when scaffolding a new machine edge service, writing a machine driver, or setting up the NATS-based communication layer for a machine
---

# Puda Edge

## Goal

Scaffold and implement an edge service that integrates any machine (with a working SDK or API) into PUDA with NATS messaging. 

## Repository Structure

```
<machine-name>/
├── pyproject.toml          # workspace root — declares edge as a member
├── .gitignore
├── uv.lock
└── edge/
    ├── pyproject.toml      # edge package dependencies
    ├── main.py             # entry point: config, NATS client, EdgeRunner
    ├── <machine_name>.py   # machine driver: public command methods
    └── Dockerfile          # optional, for containerised deployment
```

### Root `pyproject.toml`

Declares the uv workspace with `edge` as a member:

```toml
[tool.uv.workspace]
members = ["edge"]
```

### Edge `pyproject.toml`

```toml
[project]
name = "<machine-name>-edge"
version = "0.1.0"
description = "Edge service for the '<machine-name>' machine"
readme = "README.md"
requires-python = ">=3.14"
dependencies = [
    "puda-comms>=0.0.10",
    "pydantic>=2.12.5",
    "pydantic-settings>=2.12.0",
    "python-dotenv>=1.2.1",
    # add machine-specific SDK packages here
]
```

## `main.py` — Entry Point

`main.py` handles configuration, driver initialisation, NATS connection, and the run loop. It follows this exact pattern:

### 1. Configuration via pydantic-settings

Define a `Config(BaseSettings)` class that reads from a `.env` file. Fields:

| Field | Type | Purpose |
|---|---|---|
| `machine_id` | `str` | Unique machine identifier in PUDA |
| `nats_servers` | `str` | Comma-separated NATS server URLs |
| `<machine>_ip` (or similar) | `str` | Machine-specific connection address |

Add a `nats_server_list` property that splits the comma-separated string:

```python
@property
def nats_server_list(self) -> list[str]:
    return [s.strip() for s in self.nats_servers.split(",") if s.strip()]
```

Wrap construction in `load_config()` that exits the process on failure.

### 2. `async def main()`

1. Load config
2. Instantiate the machine driver and call `driver.startup()`
3. Create `EdgeNatsClient(servers=..., machine_id=...)`
4. Define a `telemetry_handler` coroutine that publishes heartbeat/health/position
5. Create `EdgeRunner(nats_client=..., machine_driver=..., telemetry_handler=..., state_handler=...)`
6. Call `runner.connect()` then `runner.run()`

### 3. Retry loop

Run `asyncio.run(main())` in a `while True` loop. Catch `KeyboardInterrupt` (log and continue) and general `Exception` (log and sleep 5 s before retry).

### Template

```python
import asyncio
import logging
import sys
import time
from pydantic_settings import BaseSettings, SettingsConfigDict
from puda_comms import EdgeNatsClient, EdgeRunner
from <machine_module> import <MachineClass>

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    force=True,
)
logger = logging.getLogger(__name__)


class Config(BaseSettings):
    machine_id: str
    nats_servers: str
    # add machine-specific fields (IP, port, serial path, etc.)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @property
    def nats_server_list(self) -> list[str]:
        return [s.strip() for s in self.nats_servers.split(",") if s.strip()]


def load_config() -> Config:
    try:
        return Config()
    except Exception as e:
        logger.error("Failed to load configuration: %s", e, exc_info=True)
        sys.exit(1)


async def main():
    config = load_config()
    logger.info("Config: machine_id=%s", config.machine_id)

    driver = <MachineClass>(...)
    driver.startup()

    edge_nats_client = EdgeNatsClient(
        servers=config.nats_server_list,
        machine_id=config.machine_id,
    )

    async def telemetry_handler():
        await edge_nats_client.publish_heartbeat()
        await edge_nats_client.publish_health({})

    runner = EdgeRunner(
        nats_client=edge_nats_client,
        machine_driver=driver,
        telemetry_handler=telemetry_handler,
        state_handler=lambda: {},
    )
    await runner.connect()
    logger.info("==================== %s Edge Service Ready ====================", config.machine_id)
    await runner.run()


if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            logger.warning("Received KeyboardInterrupt, but continuing to run...")
            time.sleep(1)
        except Exception as e:
            logger.error("Fatal error: %s", e, exc_info=True)
            time.sleep(5)
```

## `<machine_name>.py` — Machine Driver

This file defines a single class whose **public methods are the commands** the machine can execute. `EdgeRunner` discovers them via `getattr`, so each public method name becomes a command name in PUDA.

### Design Rules

1. **Only basic JSON-serializable parameter types.** The communication layer serialises everything as JSON. Method parameters must be primitive types only: `str`, `int`, `float`, `bool`, `list`, `dict`. **Never use enums, dataclasses, or custom objects as parameter types.** If the underlying SDK uses enums, convert from strings inside the method body (see biologic's `_convert_irange_string` pattern).

2. **Required lifecycle methods:**
   - `__init__(self, ...)` — accept connection info (IP, port, serial path, etc.) and store it. Do **not** connect yet.
   - `startup(self)` — establish the actual connection to the machine. Called once from `main.py` before the run loop.

3. **Optional lifecycle methods:** `connect()`, `disconnect()`, `shutdown()` as needed.

4. **Command methods** — each public method (not prefixed with `_`) is a command. Convention:
   - Accept `params: dict[str, Any]` as the first argument for the command's parameters.
   - Accept `**kwargs` for additional options (e.g. `channels`, `retrieve_data`).
   - Return a `dict[str, Any]` with the result data.
   - Log the invocation at INFO level.

5. **Document parameters thoroughly** in the docstring: name, type, valid range, units, required vs default. This documentation is the contract that protocol generators rely on.

### Template

```python
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class <MachineClass>:
    def __init__(self, <machine>_ip: str):
        self.<machine>_ip = <machine>_ip
        self._device = None

    def startup(self):
        if self._device is not None:
            return
        # initialise connection to the machine SDK/API
        self._device = ...
        logger.info("Machine started at %s", self.<machine>_ip)

    # --- Commands (public methods = PUDA commands) ---

    def <CommandName>(self, params: dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        <Short description of the command.>

        Args:
            params: Dictionary containing:
                - <param_name>: <description> (<type>, <range/constraints>). [Required | Default: <val>]
            **kwargs: Additional keyword arguments.

        Returns:
            Dictionary containing the result data.
        """
        logger.info("Running <CommandName>: params=%s, kwargs=%s", params, kwargs)
        # call underlying SDK, return results as dict
        ...
```

### String-to-enum conversion pattern

When the underlying SDK requires enum values, accept strings from JSON and convert internally:

```python
def _convert_some_enum(value: str):
    """Convert a string like 'EnumType.member' or 'member' to the SDK enum."""
    if not isinstance(value, str):
        return value
    name = value.split(".")[-1]
    try:
        return getattr(sdk_module.EnumType, name)
    except AttributeError:
        raise ValueError(f"Invalid value: {value}")
```

Then call this converter at the top of the command method before passing params to the SDK.

## Dockerfile (Optional)

For containerised deployment:

```dockerfile
FROM python:3.14-slim-bookworm
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY pyproject.toml uv.lock ./
COPY edge/ ./edge/

WORKDIR /app/edge
RUN uv sync --frozen --no-dev --no-install-project --package <machine-name>-edge

CMD ["uv", "run", "python", "main.py"]
```

Add system dependencies (`udev`, `libgl1`, etc.) as needed for the machine SDK.

## Checklist

When creating a new edge service:

1. Create the repo structure (root `pyproject.toml`, `edge/` folder)
2. Write `edge/<machine_name>.py` with the driver class — public methods are commands, params use only basic types
3. Write `edge/main.py` following the Config → driver → EdgeNatsClient → EdgeRunner pattern
4. Write `edge/pyproject.toml` with `puda-comms` and machine SDK dependencies
5. Add `.env.example` with required environment variables (`MACHINE_ID`, `NATS_SERVERS`, machine-specific vars)
6. Add `.gitignore` (exclude `.env`, `__pycache__`, `.venv`, etc.)
7. Optionally add a `Dockerfile` for container deployment

## Reference Implementations

- [PUDAP/biologic](https://github.com/PUDAP/biologic) — electrochemical testing device (full driver with many commands)
- [PUDAP/opentrons](https://github.com/PUDAP/opentrons) — liquid handler (minimal skeleton)