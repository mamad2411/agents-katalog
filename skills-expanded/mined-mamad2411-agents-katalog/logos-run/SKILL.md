---
description: "Run LOGOS perception service — start, test, demo, stop"
---

# /logos-run — Run LOGOS Full E2E

One-command launcher for the LOGOS attribute-aware tracking service.

## Usage

```
/logos-run                  # Full E2E: start → test → demo → stop
/logos-run start            # Just start the services
/logos-run test             # Run all tests (assumes already started)
/logos-run demo             # Run demo preflight
/logos-run stop             # Tear down everything
/logos-run status           # Check what's running
/logos-run docker           # Build and run Docker
/logos-run e2e              # Run e2e validation with real detector
/logos-run zed              # Stream ZED 2i camera
```

## Instructions

### Module Info
- **Path**: /Users/ilessio/Development/AIFLOWLABS/R&D/04-VLM-GIST
- **Source**: src/logos/
- **Port**: 8000 (local) / 8004 (Docker)
- **gRPC**: 50051 (local) / 50054 (Docker)
- **Docker service**: logos-cpu / logos-gpu

### START Mode

```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/04-VLM-GIST

# Option 1: Local (development)
source .venv/bin/activate
PYTHONPATH=src uvicorn logos.server:app --host 0.0.0.0 --port 8000

# Option 2: Docker CPU
make run
# or: docker compose up -d logos-cpu

# Option 3: Docker GPU
make run-gpu
```

### TEST Mode

```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/04-VLM-GIST
source .venv/bin/activate
PYTHONPATH=src python -m pytest tests/ -v --tb=short --cov=logos
```

### DEMO Mode

```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/04-VLM-GIST
make preflight
# or: PYTHONPATH=src python scripts/demo_preflight.py
```

### E2E Mode (real detector + VLM)

```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/04-VLM-GIST
make e2e
# or manually:
PYTHONPATH=src LOGOS_DETECTOR_BACKEND=ultralytics LOGOS_DEVICE=cpu \
  LOGOS_VLM_PROVIDER=minimax MINIMAX_API_KEY=<key> \
  python scripts/demo_e2e_validate.py
```

### ZED Mode (camera stream)

```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/04-VLM-GIST
make zed-stream
# or: PYTHONPATH=src python scripts/zed_stream_worker.py --query "find all objects"
```

### DOCKER Mode

```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/04-VLM-GIST
make build && make run
curl http://localhost:8004/health
```

### STOP Mode

```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/04-VLM-GIST
make stop
```

### STATUS Mode

```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/04-VLM-GIST
docker compose ps
curl -sf http://localhost:8000/health 2>/dev/null && echo "Local: healthy" || echo "Local: not running"
curl -sf http://localhost:8004/health 2>/dev/null && echo "Docker: healthy" || echo "Docker: not running"
```

### Full E2E (default)
1. Start service locally
2. Wait for health
3. Run 92 tests
4. Run demo preflight
5. Print results
6. Stop

### Required Assets
- yolov8l-world.pt (91MB, in repo)
- MINIMAX_API_KEY in .env (for VLM vision)
- benchmark_assets/ (in repo)
- demo_assets/ (in repo)

### Quick Reference
| Item | Value |
|------|-------|
| Path | `/Users/ilessio/Development/AIFLOWLABS/R&D/04-VLM-GIST` |
| Port (local) | 8000 |
| Port (Docker) | 8004 |
| Health | `http://localhost:8000/health` |
| Docs | `http://localhost:8000/docs` |
| Demo | `http://localhost:8000/demo` |
| Investor | `http://localhost:8000/investor` |
| Tests | `pytest tests/ -v` (92 tests) |
| Coverage | 79% |
