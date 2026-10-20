# /anima-docker-ros2 — Docker + ROS2 Readiness for ANIMA Integration

**Purpose:** Ensure every module has complete Docker serving + ROS2 node infrastructure. Runs automatically as part of the ANIMA pipeline.

**RULE: No module ships without Docker + ROS2 ready.**

---

## WHEN THIS RUNS

This is chained into the ANIMA pipeline — called automatically by:
- `/anima-data-preflight` (Step 0 checks)
- `/anima-autopilot` (after code complete)
- `/anima-train` (after training, before export)
- `/anima-hf-strategy` (before push)

Can also be called standalone: `/anima-docker-ros2`

---

## CHECKLIST (all must pass)

```bash
MODULE_NAME=$(basename $(pwd) | sed 's/project_//')
echo "=== ANIMA Docker+ROS2 Check: ${MODULE_NAME} ==="

# 1. anima_module.yaml
[ -f "anima_module.yaml" ] && echo "[✅] anima_module.yaml" || echo "[❌] anima_module.yaml MISSING"

# 2. Dockerfile.serve
[ -f "Dockerfile.serve" ] && echo "[✅] Dockerfile.serve" || echo "[❌] Dockerfile.serve MISSING — CREATING"

# 3. docker-compose.serve.yml
[ -f "docker-compose.serve.yml" ] && echo "[✅] docker-compose.serve.yml" || echo "[❌] docker-compose.serve.yml MISSING — CREATING"

# 4. .env.serve
[ -f ".env.serve" ] && echo "[✅] .env.serve" || echo "[❌] .env.serve MISSING — CREATING"

# 5. serve.py (in src/ or root)
SERVE=$(find . -name "serve.py" -not -path "./.venv/*" | head -1)
[ -n "$SERVE" ] && echo "[✅] serve.py at $SERVE" || echo "[❌] serve.py MISSING — CREATING"

# 6. Registry entry
[ -f "/mnt/forge-data/anima-infra-main/registry/${MODULE_NAME}.yaml" ] && \
  echo "[✅] Registered in anima-infra-main/registry/" || \
  { echo "[❌] NOT in registry — copying"; \
    cp anima_module.yaml "/mnt/forge-data/anima-infra-main/registry/${MODULE_NAME}.yaml" 2>/dev/null; }
```

---

## AUTO-CREATE MISSING FILES

### Dockerfile.serve (if missing)
```dockerfile
FROM anima-serve:jazzy
LABEL org.opencontainers.image.source="https://github.com/RobotFlow-Labs/project_MODULE_NAME"

WORKDIR /anima

# Copy module code
COPY src/ ./src/
COPY configs/ ./configs/
COPY serve.py ./serve.py
COPY pyproject.toml ./pyproject.toml
COPY anima_module.yaml ./anima_module.yaml

# Install dependencies
RUN pip install --no-cache-dir -e ".[serve]" 2>/dev/null || pip install --no-cache-dir -e . || true

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f http://localhost:${SERVE_PORT:-8080}/health || exit 1

EXPOSE ${SERVE_PORT:-8080}
CMD ["python", "serve.py"]
```

### docker-compose.serve.yml (if missing)
```yaml
version: "3.8"
services:
  MODULE_NAME:
    build:
      context: .
      dockerfile: Dockerfile.serve
    image: anima-MODULE_NAME:latest
    container_name: anima-MODULE_NAME
    env_file: .env.serve
    ports:
      - "${SERVE_PORT:-8080}:${SERVE_PORT:-8080}"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    volumes:
      - ./configs:/anima/configs:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:${SERVE_PORT:-8080}/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### .env.serve (if missing)
```env
SERVE_PORT=8080
MODEL_PATH=/anima/checkpoints/best.pth
DEVICE=cuda:0
LOG_LEVEL=INFO
MODULE_NAME=MODULE_NAME
```

### serve.py (if missing)
```python
"""ANIMA Module Serving — MODULE_NAME"""
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="ANIMA MODULE_NAME", version="0.1.0")

@app.get("/health")
async def health():
    return {"status": "ok", "module": os.getenv("MODULE_NAME", "unknown")}

@app.get("/info")
async def info():
    return {"module": os.getenv("MODULE_NAME"), "version": "0.1.0"}

if __name__ == "__main__":
    port = int(os.getenv("SERVE_PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

---

## ROS2 NODE GENERATION

If the module needs a ROS2 node (check `anima_module.yaml` for `interface.inputs/outputs` with `ros2_type`):

```bash
# Use the cookiecutter template
cd /mnt/forge-data/anima-infra-main/anima-ros2-template

cookiecutter . \
  --no-input \
  module_name=${MODULE_NAME} \
  ModuleName=$(echo ${MODULE_NAME} | python3 -c "import sys; print(sys.stdin.read().strip().title().replace('_',''))")

# Copy generated ROS2 node into the module
cp -r ${MODULE_NAME}/ /mnt/forge-data/modules/project_${MODULE_NAME}/ros2/
```

The generated ROS2 package includes:
- `node.py` — ROS2 node with pub/sub from anima_module.yaml
- `launch.py` — ROS2 launch file
- `CMakeLists.txt` + `package.xml` — for colcon build
- Custom messages from the module's interface spec
- Tests for conversions and node lifecycle

---

## VERIFICATION

After creating/checking all files:
```bash
echo "=== DOCKER+ROS2 VERIFICATION ==="
echo "Dockerfile.serve: $(wc -l < Dockerfile.serve 2>/dev/null || echo 'MISSING') lines"
echo "docker-compose:   $(wc -l < docker-compose.serve.yml 2>/dev/null || echo 'MISSING') lines"
echo "serve.py:         $(find . -name 'serve.py' -not -path './.venv/*' | wc -l) files"
echo "anima_module.yaml: $(wc -l < anima_module.yaml 2>/dev/null || echo 'MISSING') lines"
echo "Registry:         $(ls /mnt/forge-data/anima-infra-main/registry/${MODULE_NAME}.yaml 2>/dev/null && echo 'YES' || echo 'NO')"
echo ""
echo "To build: docker compose -f docker-compose.serve.yml build"
echo "To run:   docker compose -f docker-compose.serve.yml up -d"
echo "To test:  curl http://localhost:8080/health"
```

---

## PIPELINE INTEGRATION

### In /anima-data-preflight (Step 0):
```
Check anima_module.yaml → Check registry → Check Docker files → Check data
```

### In /anima-autopilot (after code complete):
```
Code → Tests → /anima-docker-ros2 → Smoke test → Ready for training
```

### In /anima-train (after training):
```
Train → Eval → Export → /anima-docker-ros2 verify → /anima-hf-strategy → Push
```

### In /anima-hf-strategy (before push):
```
Verify Docker files exist → Export all formats → Push to HF
```

---

## DO NOT

- DO NOT ship a module without Dockerfile.serve
- DO NOT skip the registry check
- DO NOT hardcode ports (use SERVE_PORT env var)
- DO NOT include .venv, __pycache__, or datasets in Docker image
- DO NOT forget health check endpoint
- DO NOT build Docker images during training (wastes GPU time)
