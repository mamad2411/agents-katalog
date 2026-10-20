# /gnomon-run — Run GNOMON Full E2E

One-command launcher for the GNOMON odometry module. Validates datasets, runs tests, replays sequences, generates showcase, and tears down cleanly.

## Usage

```
/gnomon-run                  # Full E2E: test → replay → showcase
/gnomon-run test             # Run all tests + lint + type check
/gnomon-run replay           # Replay all available datasets
/gnomon-run showcase         # Regenerate showcase from existing artifacts
/gnomon-run server           # Start FastAPI server locally
/gnomon-run status           # Show dataset + artifact + test status
/gnomon-run ros2             # Start ROS2 node (docker compose --profile ros2)
```

## Instructions

### Module Info
- **Path**: `/Users/ilessio/Development/AIFLOWLABS/R&D/05-GaRLILEO`
- **Source**: `src/gnomon/`
- **Port**: 8000 (FastAPI)
- **Docker replay**: `docker compose -f docker-compose.replay.yml run --rm gnomon-replay`
- **Docker ROS2**: `docker compose --profile ros2 up anima-gnomon-ros2`
- **Datasets**: `dataset/` (Upstair, SlopeStair, MoCap-E, MoCap-H + more)

### TEST Mode
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/05-GaRLILEO

# Full test suite
uv run ruff check src/ scripts/ tests/ gnomon_node/
uv run mypy src/gnomon
uv run pytest tests/ -q -m 'not integration'

# Server smoke
uv run python -c "
from gnomon.server import app
from gnomon import __version__
assert app.version == __version__
routes = [r.path for r in app.routes if hasattr(r, 'path')]
for r in ['/health', '/baselines', '/portfolio/report', '/replay/jobs']:
    assert r in routes
print('Server smoke: PASS')
"
```

### REPLAY Mode
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/05-GaRLILEO

# Validate datasets
uv run python scripts/check_replay_dataset.py dataset/SlopeStair

# Dry-run batch plan
uv run python scripts/run_mvp_replay_batch.py dataset --dry-run

# Replay one sequence (skip Docker build if image exists)
GNOMON_REPLAY_SKIP_BUILD=1 \
GNOMON_ARTIFACT_NAME=SlopeStair \
GNOMON_SEQUENCE=garlileo \
GNOMON_DATASET_NAME=SlopeStair \
GNOMON_BAG_DIR="$(pwd)/dataset/SlopeStair" \
GNOMON_BAG_FILE=SlopeStair.db3 \
docker compose -f docker-compose.replay.yml run --rm gnomon-replay
```

### SHOWCASE Mode
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/05-GaRLILEO
make showcase
```

### SERVER Mode
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/05-GaRLILEO
uv run uvicorn gnomon.server:app --host 0.0.0.0 --port 8000 --reload
# Then open: http://localhost:8000/docs
```

### STATUS Mode
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/05-GaRLILEO

# Datasets
ls -lh dataset/*/
uv run python scripts/check_replay_dataset.py dataset/SlopeStair

# Artifacts
ls artifacts/baselines/
for seq in artifacts/baselines/*/; do
  name=$(basename "$seq")
  poses=$(wc -l < "$seq/garlileo_output/poses.txt" 2>/dev/null || echo 0)
  echo "$name: $poses poses"
done

# Tests
uv run pytest tests/ -q --tb=no 2>&1 | tail -3
```

### ROS2 Mode
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/05-GaRLILEO
docker compose --profile ros2 up -d anima-gnomon-ros2
```

### Full E2E (default)
1. Run all tests (lint + types + pytest)
2. Validate all datasets in dataset/
3. Replay any datasets without existing artifacts
4. Generate showcase
5. Print summary

### Required Assets
- **Datasets** (from GaRLILEO Google Drive):
  - `dataset/Upstair.db3` (3.4GB) — HAVE
  - `dataset/SlopeStair/SlopeStair.db3` (4.6GB) — HAVE
  - `dataset/MoCap-E/MoCap-E.db3` (31MB) — HAVE
  - `dataset/MoCap-H/MoCap-H.db3` (18MB) — HAVE
  - More at: https://drive.google.com/drive/folders/1DKv5wsgmUSl4cpXZz6PRJBOkWcTw9zzi
- **Docker image**: `gnomon-ros2:latest` (pre-built, 3.94GB)

### Quick Reference
| Item | Value |
|------|-------|
| Path | `/Users/ilessio/Development/AIFLOWLABS/R&D/05-GaRLILEO` |
| Port | 8000 |
| Health | `http://localhost:8000/health` |
| Docs | `http://localhost:8000/docs` |
| Tests | `uv run pytest tests/ -q` |
| Lint | `uv run ruff check src/` |
| Showcase | `make showcase` |
| Replay | See REPLAY Mode above |
