# /petra-run — Run PETRA Full E2E

One-command launcher for the PETRA Depth Foundation Model module.

## Usage

```
/petra-run                  # Full E2E: start → test → demo → stop
/petra-run start            # Just start the services
/petra-run test             # Run all tests (assumes already started)
/petra-run demo             # Run a demo inference
/petra-run stop             # Tear down everything
/petra-run status           # Check what's running
```

## Instructions

### Module Info
- **Path**: /Users/ilessio/Development/AIFLOWLABS/R&D/project_petra
- **Source**: src/petra/
- **Engine**: src/petra/mlx_backend.py (MLXPetraBackend)
- **Port**: 8034 (FastAPI)
- **Docker service**: petra
- **Venv**: .venv/bin/python

### START Mode
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/project_petra

# Option 1: Docker (recommended)
docker compose up -d
# Wait for health
until curl -sf http://localhost:8034/health; do sleep 1; done
echo "PETRA is healthy"

# Option 2: Local (for development)
.venv/bin/uvicorn petra.server:create_app --factory --host 0.0.0.0 --port 8034
```

### TEST Mode
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/project_petra

# Unit + integration tests
.venv/bin/python -m pytest tests/ -v --tb=short --cov=src/petra --cov-report=term-missing

# Linter + type check
.venv/bin/ruff check src/ tests/
.venv/bin/mypy src/ --ignore-missing-imports

# Health check (if Docker running)
curl -sf http://localhost:8034/health | python3 -m json.tool
```

### DEMO Mode
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/project_petra

# Feature extraction with real DeFM weights
.venv/bin/python -c "
import torch
from petra.mlx_backend import MLXPetraBackend
from petra.config import PetraConfig
cfg = PetraConfig()
backend = MLXPetraBackend(cfg)
backend.load_model('data/external/checkpoints/defm_vit_s14.pth')
depth = torch.rand(1, 1, 224, 224).to(backend.device, backend.dtype)
features = backend.extract_features(depth)
print(f'Features: {features[\"embedding\"].shape}, mean={features[\"embedding\"].mean().item():.4f}')
"

# API demo (requires server running)
python3 -c "
import json, random, urllib.request
data = [random.uniform(0.1, 50.0) for _ in range(224*224)]
payload = json.dumps({'depth_data': data, 'height': 224, 'width': 224})
req = urllib.request.Request('http://localhost:8034/features', data=payload.encode(), headers={'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req, timeout=30)
result = json.loads(resp.read())
print(f'API features: {len(result[\"embedding\"])} dims, {result[\"processing_time_ms\"]:.1f}ms')
"
```

### STOP Mode
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/project_petra
docker compose down
```

### STATUS Mode
```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/project_petra
docker compose ps
curl -sf http://localhost:8034/health 2>/dev/null && echo "Healthy" || echo "Not running"
```

### Full E2E (default — runs all steps)
1. Start services (Docker or local)
2. Wait for health check
3. Run all tests (273 expected)
4. Run demo inference with real DeFM weights
5. Print results summary
6. Stop services

### Required Assets
- `data/external/checkpoints/defm_vit_s14.pth` (82MB) — symlinked from /Volumes/AIFlowDev/
- `data/external/checkpoints/defm_vit_l14.pth` (1.2GB) — symlinked from /Volumes/AIFlowDev/

### Quick Reference
| Item | Value |
|------|-------|
| Path | `/Users/ilessio/Development/AIFLOWLABS/R&D/project_petra` |
| Port | 8034 |
| Health | `http://localhost:8034/health` |
| Docs | `http://localhost:8034/docs` |
| Docker | `docker compose up -d` |
| Tests | `.venv/bin/python -m pytest tests/ -v` |
| Lint | `.venv/bin/ruff check src/` |
