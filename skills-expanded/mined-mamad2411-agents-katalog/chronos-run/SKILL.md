# /chronos-run — Run CHRONOS Full E2E

One-command launcher for the CHRONOS (Temporally Stable Depth) module. Starts services, runs tests, demos inference, and tears down cleanly.

## Usage

```
/chronos-run                  # Full E2E: start -> test -> demo -> stop
/chronos-run start            # Just start the services
/chronos-run test             # Run all tests (assumes already started)
/chronos-run demo             # Run a demo inference
/chronos-run stop             # Tear down everything
/chronos-run status           # Check what's running
/chronos-run ros2             # Start with ROS2 profile
```

## Instructions

### Module Info
- **Path**: /Users/ilessio/Development/AIFLOWLABS/R&D/project_chronos/
- **Source**: src/chronos/
- **Engine**: src/chronos/runtime.py (DepthRuntime)
- **Port**: 8012 (FastAPI via Docker), 8000 (local dev)
- **Docker service**: chronos-cpu
- **ROS2 service**: chronos-ros2 (profile: ros2) — NOT YET IMPLEMENTED

### START Mode
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/project_chronos

# Option 1: Docker (recommended)
docker compose up -d chronos-cpu
# Wait for health
until curl -sf http://localhost:8012/health; do sleep 1; done
echo "CHRONOS is healthy"

# Option 2: Local (for development)
uv run uvicorn chronos.server:app --host 0.0.0.0 --port 8000 --reload

# Option 3: Local with factory
uv run python -m chronos
```

### TEST Mode
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/project_chronos

# Unit + integration tests
uv run pytest tests/ -v --tb=short

# Linter
uv run ruff check src/ tests/

# Format check
uv run ruff format --check src/ tests/

# Health check (if Docker running)
curl -sf http://localhost:8012/health | python3 -m json.tool
```

### DEMO Mode
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/project_chronos

# Single frame depth prediction (requires server running)
curl -X POST http://localhost:8000/predict/single \
  -F "file=@test_image.jpg"

# Video depth pipeline
curl -X POST http://localhost:8000/depth/pipeline \
  -F "file=@test_video.mp4"

# MLX backend demo (Apple Silicon, no server needed)
uv run python -c "
from chronos.config import Config
from chronos.runtime import create_depth_runtime
from chronos.device import get_device_manager
import numpy as np

config = Config()
config.model.device = 'mlx'
dm = get_device_manager()
rt = create_depth_runtime(config, device_manager=dm)
print(f'Engine: {rt.engine_name}')
frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
result = rt.predict_image(frame)
print(f'Depth shape: {result.depth_map.shape}')
print(f'Depth range: [{result.depth_map.min():.3f}, {result.depth_map.max():.3f}]')
"
```

### STOP Mode
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/project_chronos
docker compose down
```

### STATUS Mode
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/project_chronos
docker compose ps
curl -sf http://localhost:8012/health 2>/dev/null && echo "Healthy" || echo "Not running"
```

### Full E2E (default — runs all steps)
1. Start services (Docker or local)
2. Wait for health check
3. Run all tests (uv run pytest)
4. Run demo inference
5. Print results summary
6. Stop services

### Required Assets
- **VDA-Small weights**: Already on AIFlowDev at `/Volumes/AIFlowDev/RobotFlowLabs/datasets/project_chronos/`
  - Video-Depth-Anything Base/Large/Small checkpoints (~2 GB total)
- **No other downloads required for basic inference**

### Quick Reference
| Item | Value |
|------|-------|
| Path | `/Users/ilessio/Development/AIFLOWLABS/R&D/project_chronos/` |
| Port (Docker) | 8012 |
| Port (local) | 8000 |
| Health | `http://localhost:8012/health` (Docker) or `:8000/health` (local) |
| Docs | `http://localhost:8000/docs` |
| Docker | `docker compose up -d chronos-cpu` |
| Tests | `uv run pytest tests/ -v` |
| Lint | `uv run ruff check src/` |
| Python | 3.12 (via .python-version) |
| Package mgr | uv |
