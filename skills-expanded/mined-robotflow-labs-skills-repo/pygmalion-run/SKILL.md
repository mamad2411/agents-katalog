# /pygmalion-run — Run PYGMALION Full E2E

One-command launcher for the PYGMALION VLA module. Starts services, runs tests, demos inference, and tears down cleanly.

## Usage

```
/pygmalion-run                  # Full E2E: start → test → demo → stop
/pygmalion-run start            # Just start the services
/pygmalion-run test             # Run all tests (assumes already started)
/pygmalion-run demo             # Run a demo inference
/pygmalion-run stop             # Tear down everything
/pygmalion-run status           # Check what's running
/pygmalion-run ros2             # Start with ROS2 profile
```

## Instructions

### Module Info
- **Path**: /Users/ilessio/Development/AIFLOWLABS/R&D/project_pygmalion
- **Source**: src/pygmalion/
- **Engine**: src/pygmalion/vla_pipeline.py (custom scaffold) + src/pygmalion/lerobot_integration.py (official SmolVLA)
- **Server**: src/pygmalion/server.py (FastAPI)
- **Port**: 8030 (FastAPI)
- **Docker service**: pygmalion (docker-compose.yml)
- **Model**: lerobot/smolvla_base (907 MB, HuggingFace Hub cache)

### START Mode
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/project_pygmalion

# Option 1: Docker (recommended)
docker compose up -d pygmalion
# Wait for health
until curl -sf http://localhost:8030/health; do sleep 2; done
echo "PYGMALION is healthy"

# Option 2: Local (for development)
uv run python scripts/run_server.py

# Option 3: With GPU
docker compose --profile gpu up -d pygmalion-gpu
```

### TEST Mode
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/project_pygmalion

# Unit + integration tests
uv run python -m pytest tests/ -v --tb=short --cov=src/pygmalion --cov-report=term-missing

# Linter
uv run ruff check src/ tests/ scripts/

# Format check
uv run ruff format --check src/ tests/

# Health check (if Docker running)
curl -sf http://localhost:8030/health | python3 -m json.tool
```

### DEMO Mode
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/project_pygmalion

# 1. Run a bootstrap recording (captures 5 camera frames)
uv run python scripts/bootstrap_record.py --task "pick up the cube" --frames 5 --json

# 2. Evaluate recording with official SmolVLA policy
uv run python scripts/evaluate_recordings.py --runtime official --latest --local-files-only --json

# 3. Export recording to LeRobot format
uv run python scripts/export_recordings_to_lerobot.py \
  --repo-id local/bootstrap_observation \
  --output-root data/exports/bootstrap_observation \
  --latest --json

# 4. Camera smoke test (quick hardware check)
uv run python scripts/camera_smoke_test.py
```

### STOP Mode
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/project_pygmalion
docker compose down
docker compose --profile gpu down 2>/dev/null || true
```

### STATUS Mode
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/project_pygmalion
docker compose ps
curl -sf http://localhost:8030/health 2>/dev/null && echo "Healthy" || echo "Not running"
```

### Full E2E (default — runs all steps)
1. Start services (Docker or local)
2. Wait for health check at :8030/health
3. Run all 162 tests with coverage
4. Run demo: bootstrap recording → eval → export
5. Print results summary
6. Stop services

### Required Assets

| Asset | Size | Download |
|-------|------|----------|
| `lerobot/smolvla_base` | 907 MB | `huggingface-cli download lerobot/smolvla_base` |
| `svla_so100_pickplace` | ~450 MB | `huggingface-cli download --repo-type dataset lerobot/svla_so100_pickplace --local-dir data/datasets/svla_so100_pickplace` |
| `svla_so100_stacking` | ~585 MB | `huggingface-cli download --repo-type dataset lerobot/svla_so100_stacking --local-dir data/datasets/svla_so100_stacking` |

### Quick Reference
| Item | Value |
|------|-------|
| Path | `/Users/ilessio/Development/AIFLOWLABS/R&D/project_pygmalion` |
| Port | 8030 |
| Health | `http://localhost:8030/health` |
| Docs | `http://localhost:8030/docs` |
| Docker | `docker compose up -d pygmalion` |
| Tests | `uv run python -m pytest tests/ -v` |
| Lint | `uv run ruff check src/` |
| Coverage | 76% (162/162 tests) |
| PR | https://github.com/RobotFlow-Labs/anima-pygmalion/pull/1 |
