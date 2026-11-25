# /anima-docker-serve — Add Universal Docker Serving to Any ANIMA Module

## Purpose

Add the standardized ANIMA Docker serving setup to any module repository. This creates the files needed to serve the module as a Docker container with ROS2 node (primary) + FastAPI (secondary), auto-downloading weights from HuggingFace.

## Usage

```
/anima-docker-serve                    # Run in a module repo directory
/anima-docker-serve --module azoth     # Specify module name explicitly
```

## What It Does

1. **Reads** `anima_module.yaml` from the repo to get module identity
2. **Creates** `Dockerfile.serve` — multi-stage build (anima-base → anima-serve → module)
3. **Creates** `docker-compose.serve.yml` — profiles: serve, ros2, api, test
4. **Creates** `.env.serve` — module-specific environment defaults
5. **Creates** `src/{module}/serve.py` — module's AnimaNode subclass (if not exists)
6. **Verifies** the setup builds and the health endpoint responds

## Prerequisites

- Module repo must have `anima_module.yaml` at root
- Module repo must have `pyproject.toml` with installable Python package
- Module must have a HuggingFace repo at `ilessio-aiflowlab/project_{module_name}` with weights
- If ROS2 messages exist: `{module}_msgs/` directory with `.msg`/`.srv` files

## Architecture

```
THREE-LAYER DOCKER PATTERN (D-034, D-035):

  anima-base (ghcr.io/robotflow-labs/anima-base:jazzy)
    = ros:jazzy-ros-base + CycloneDDS + anima_msgs + uv

  anima-serve (ghcr.io/robotflow-labs/anima-serve:jazzy)
    = anima-base + anima_serve Python package
    = FastAPI health/ready/info + HF weight downloader
    = AnimaNode base class + GPU detection + MCAP hooks

  anima-{module} (per module)
    = anima-serve + module code + module msgs + module node
```

## Files Created

### `Dockerfile.serve`

```dockerfile
ARG ANIMA_SERVE_IMAGE=ghcr.io/robotflow-labs/anima-serve:jazzy

# Stage 1: Build module ROS2 messages (if they exist)
FROM ghcr.io/robotflow-labs/anima-base:jazzy AS msgs-build
ARG MODULE_NAME
WORKDIR /ws/src
COPY ${MODULE_NAME}_msgs/ ${MODULE_NAME}_msgs/ 2>/dev/null
WORKDIR /ws
RUN if [ -d /ws/src/${MODULE_NAME}_msgs ]; then \
      . /opt/ros/jazzy/setup.sh && \
      . /ws/install/setup.sh && \
      colcon build --packages-select ${MODULE_NAME}_msgs \
        --cmake-args -DCMAKE_BUILD_TYPE=Release; \
    fi

# Stage 2: Module serving image
FROM ${ANIMA_SERVE_IMAGE} AS serve
ARG MODULE_NAME
ARG MODULE_VERSION=1.0.0
ARG HF_REPO
ARG SERVE_PORT=8000

# Install module Python package
WORKDIR /app
COPY pyproject.toml uv.lock* ./
COPY src/ src/
COPY configs/ configs/ 2>/dev/null
RUN uv pip install --system --no-cache "." 2>/dev/null || \
    uv pip install --system --no-cache -e "." 2>/dev/null || true

# Copy module ROS2 messages (if built)
COPY --from=msgs-build /ws/install/ /ws/module_install/ 2>/dev/null
RUN if [ -d /ws/module_install/lib ]; then \
      printf '\nsource /ws/module_install/setup.bash' >> /ros_setup.sh; \
    fi

# Copy module ROS2 node (if exists)
WORKDIR /ws/src
COPY ${MODULE_NAME}_node/ ${MODULE_NAME}_node/ 2>/dev/null
WORKDIR /ws
RUN if [ -d /ws/src/${MODULE_NAME}_node ]; then \
      . /opt/ros/jazzy/setup.sh && \
      . /ws/install/setup.bash && \
      colcon build --packages-select ${MODULE_NAME}_node; \
    fi

# Module identity + manifest
COPY anima_module.yaml /etc/anima/module.yaml
ENV ANIMA_MODULE_NAME=${MODULE_NAME}
ENV ANIMA_MODULE_VERSION=${MODULE_VERSION}
ENV ANIMA_HF_REPO=${HF_REPO}
ENV ANIMA_SERVE_PORT=${SERVE_PORT}

EXPOSE ${SERVE_PORT}

HEALTHCHECK --interval=10s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${SERVE_PORT}/health || exit 1

CMD ["anima-serve", "start"]
```

### `docker-compose.serve.yml`

```yaml
x-common: &common
  network_mode: host
  environment:
    - ROS_DOMAIN_ID=${ROS_DOMAIN_ID:-0}
    - RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
    - ANIMA_MODULE_NAME=${MODULE_NAME}
    - ANIMA_HF_REPO=${HF_REPO}
    - ANIMA_WEIGHT_FORMAT=${WEIGHT_FORMAT:-auto}
    - ANIMA_DEVICE=${DEVICE:-auto}
    - HF_TOKEN=${HF_TOKEN:-}
  volumes:
    - anima-weights:/data/weights
  restart: unless-stopped

services:
  serve:
    build:
      context: .
      dockerfile: Dockerfile.serve
      args:
        MODULE_NAME: ${MODULE_NAME}
        MODULE_VERSION: ${MODULE_VERSION:-1.0.0}
        HF_REPO: ${HF_REPO}
    <<: *common
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    profiles: [serve, gpu]

  ros2:
    build:
      context: .
      dockerfile: Dockerfile.serve
      args:
        MODULE_NAME: ${MODULE_NAME}
    <<: *common
    command: ["anima-serve", "start", "--ros2-only"]
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    profiles: [ros2]

  api:
    build:
      context: .
      dockerfile: Dockerfile.serve
      args:
        MODULE_NAME: ${MODULE_NAME}
    <<: *common
    command: ["anima-serve", "start", "--api-only"]
    profiles: [api]

  test:
    build:
      context: .
      dockerfile: Dockerfile.serve
      args:
        MODULE_NAME: ${MODULE_NAME}
    <<: *common
    command: >
      bash -c "
        source /opt/ros/jazzy/setup.bash &&
        source /ws/install/setup.bash &&
        uv run pytest tests/ -v --tb=short 2>/dev/null;
        echo '=== Health check ===' &&
        timeout 15 anima-serve start --api-only &
        sleep 8 &&
        curl -sf http://localhost:8000/health && echo ' PASS' || echo ' FAIL'
      "
    profiles: [test]

volumes:
  anima-weights:
    driver: local
```

### `.env.serve`

```bash
# ANIMA Module Serving Configuration
# Source: anima_module.yaml
MODULE_NAME={{module_name}}
MODULE_VERSION={{module_version}}
HF_REPO=ilessio-aiflowlab/project_{{module_name}}

# Runtime
DEVICE=auto           # auto|cuda|cpu|mps
WEIGHT_FORMAT=auto    # auto|trt|onnx|safetensors|pth
ROS_DOMAIN_ID=0
SERVE_PORT=8000

# HuggingFace (set HF_TOKEN for private repos)
# HF_TOKEN=hf_...
```

## Execution Steps

When `/anima-docker-serve` is invoked in a module directory:

1. **Read `anima_module.yaml`** — extract module name, version, category, ports
2. **Check HuggingFace** — verify `ilessio-aiflowlab/project_{name}` exists and has weight files
3. **Detect existing files** — check for `{name}_msgs/`, `{name}_node/`, `Dockerfile`, `docker-compose.yml`
4. **Create `Dockerfile.serve`** — using the template above, with module-specific ARGs
5. **Create `docker-compose.serve.yml`** — using the template above
6. **Create `.env.serve`** — with module identity from manifest
7. **Check for `src/{name}/serve.py`** — if missing, create a skeleton AnimaNode subclass
8. **Test build** — run `docker compose -f docker-compose.serve.yml --profile test run --rm test`
9. **Report** — show which profiles are available and how to use them

## Quick Commands After Setup

```bash
# Load env
set -a; source .env.serve; set +a

# Serve with full stack (ROS2 + FastAPI + GPU)
docker compose -f docker-compose.serve.yml --profile serve up -d

# ROS2 only (for ANIMA compiler pipelines)
docker compose -f docker-compose.serve.yml --profile ros2 up -d

# API only (debug/dev)
docker compose -f docker-compose.serve.yml --profile api up -d

# Run tests
docker compose -f docker-compose.serve.yml --profile test run --rm test

# Check health
curl http://localhost:8000/health

# Check ROS2 topics
ros2 topic list | grep /anima/
ros2 topic echo /anima/{module_name}/health --once
```

## Weight Format Selection

The serving framework auto-selects the best weight format available in HF:

| Priority | Format | Backend | When Used |
|----------|--------|---------|-----------|
| 1 | `.trt` / `.engine` | TensorRT | Jetson Thor / NVIDIA GPU (fastest) |
| 2 | `.onnx` | ONNX Runtime | Any GPU/CPU (portable) |
| 3 | `.safetensors` | PyTorch/MLX | Dev, training, Apple Silicon |
| 4 | `.pth` | PyTorch | Fallback (legacy format) |

Override with `WEIGHT_FORMAT=onnx` to force a specific format.

## Conventions

- **Port**: Each module uses port from `anima_module.yaml` → `container.port` (default 8000)
- **Health topic**: Always `/anima/{module_name}/health` with `ModuleHealth` message
- **Weights volume**: `anima-weights` Docker volume shared across all modules
- **GPU**: NVIDIA runtime auto-detected. Falls back to CPU if no GPU found.
- **CycloneDDS**: Always. Never FastDDS in Docker (multicast issues).
- **network_mode: host**: Always. Required for ROS2 DDS discovery.

## Related Decisions

- D-034: Every ANIMA module = ROS2 lifecycle node
- D-035: Manifest v2 = ROS2-native + ANIMA extension
- D-036: anima-agent-ros2 + NemoClaw security

## Related Skills

- `/ros2-node` — Adds ROS2 node layer (msgs + node packages) — run BEFORE this skill
- `/test-mvp-production` — Full MVP validation gate
- `/anima-hf-strategy` — Audit and fix HF repos
- `/anima-train` — Pre-flight checks for training runs
