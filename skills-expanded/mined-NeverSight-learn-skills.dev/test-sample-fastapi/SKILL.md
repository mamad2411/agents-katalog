---
name: test-sample-fastapi
description: Build aerospike-py and run sample-fastapi integration tests to verify changes work in a real FastAPI application
disable-model-invocation: true
---

# Test Sample FastAPI

Verifies that the sample-fastapi app works correctly after changes to aerospike-py by building locally and running tests.

## Project Structure

```
examples/sample-fastapi/
├── app/
│   ├── main.py              # FastAPI app (manages AsyncClient via lifespan)
│   ├── config.py             # Configuration
│   ├── dependencies.py       # FastAPI dependencies (Request.app.state.aerospike)
│   ├── models.py             # Pydantic models
│   └── routers/
│       ├── records.py        # CRUD endpoints
│       ├── batch.py          # Batch operations
│       ├── operations.py     # operate operations
│       ├── indexes.py        # Index management
│       ├── truncate.py       # truncate
│       ├── udf.py            # UDF management
│       ├── cluster.py        # Cluster info
│       ├── admin_users.py    # User management
│       ├── admin_roles.py    # Role management
│       ├── users.py          # User CRUD
│       ├── numpy_batch.py    # NumPy batch endpoints
│       └── observability.py  # Metrics/tracing endpoints
├── tests/
│   ├── conftest.py           # TestContainers-based Aerospike server + FastAPI TestClient
│   ├── test_records.py       # CRUD tests
│   ├── test_batch.py         # Batch tests
│   ├── test_operations.py    # operate tests
│   ├── test_indexes.py       # Index tests
│   ├── test_truncate.py      # truncate tests
│   ├── test_udf.py           # UDF tests
│   ├── test_cluster.py       # Cluster info tests
│   ├── test_health.py        # Health check tests
│   ├── test_admin_users.py   # User management tests
│   ├── test_admin_roles.py   # Role management tests
│   ├── test_users.py         # User CRUD tests
│   ├── test_numpy_batch.py   # NumPy batch tests
│   └── test_observability.py # Metrics/tracing tests
└── pyproject.toml            # uv.sources: aerospike-py = { path = "../.." }
```

## Steps

### 1. Build aerospike-py
Build the Rust native module from the project root:
```bash
cd /Users/ksr/github/aerospike-py && uv run maturin develop --release
```
If the build fails, analyze the error and suggest a fix.

### 2. Sync sample-fastapi Dependencies
Reflect the built aerospike-py in sample-fastapi:
```bash
cd /Users/ksr/github/aerospike-py/examples/sample-fastapi && uv sync --extra dev
```
Since `[tool.uv.sources]` in `pyproject.toml` has `aerospike-py = { path = "../.." }`, the just-built package is automatically used.

### 3. Check Aerospike Server
Verify a local Aerospike server is running:
```bash
docker ps | grep aerospike || podman ps | grep aerospike
```
- If running, proceed as-is (conftest.py tries connecting to `AEROSPIKE_HOST`/`AEROSPIKE_PORT` env vars or default `127.0.0.1:3000`)
- If not running, TestContainers will automatically create a container, so just verify the Docker/Podman daemon is running

### 4. Run Tests
Run the sample-fastapi tests:
```bash
cd /Users/ksr/github/aerospike-py/examples/sample-fastapi && uv run pytest tests/ -v
```

### 5. Report Results
- If all tests pass: confirm the changes work correctly in the FastAPI app
- If any tests fail:
  - List failed test names and error messages
  - Analyze the relationship with aerospike-py changes
  - Suggest fix direction (distinguish between aerospike-py issues vs sample-fastapi issues)

## Test Infrastructure Details

### conftest.py Key Fixtures

| Fixture | Scope | Description |
|---------|-------|------|
| `aerospike_container` | session | Starts Aerospike CE 8.1 via TestContainers. Reuses existing local server if available. Returns `(container, port)`. |
| `jaeger_container` | session | Jaeger all-in-one container for tracing tests. Returns `(container, otlp_port, ui_port)`. |
| `aerospike_client` | session | Sync client (for data setup/teardown). Uses `POLICY_KEY_SEND`. |
| `client` | session | FastAPI `TestClient`. Creates `AsyncClient` in lifespan. Defaults to `OTEL_SDK_DISABLED=true`. |
| `cleanup` | function (autouse) | Automatic record cleanup after each test. Append keys to `keys` list for automatic deletion. |

### TestContainers Behavior

1. Attempts TCP connection to `AEROSPIKE_HOST`/`AEROSPIKE_PORT` env vars or default `127.0.0.1:3000`
2. If successful, reuses existing server (no container creation)
3. If unsuccessful, automatically creates an Aerospike CE container on a random port
4. Waits for `heartbeat-received` log, then waits an additional 2 seconds
5. Mounts custom `aerospike.template.conf` for access-port configuration

### FastAPI TestClient Behavior

The `client` fixture in conftest.py overrides the FastAPI app's lifespan:
1. Sets `OTEL_SDK_DISABLED=true` env var (test without Jaeger)
2. Sets `aerospike_py.set_log_level(LOG_LEVEL_INFO)` log level
3. Initializes tracing with `aerospike_py.init_tracing()`
4. Creates `AsyncClient` and stores it in `app.state.aerospike`
5. After tests, calls `AsyncClient.close()` + `shutdown_tracing()`

## CI Execution

Runs as `tox -e fastapi` in the CI `feasibility` job:
- Python 3.13, using Aerospike latest service container
- `AEROSPIKE_PORT=3000` environment variable
- Dependency group: `test-fastapi` (pytest, pytest-asyncio, fastapi, httpx)
