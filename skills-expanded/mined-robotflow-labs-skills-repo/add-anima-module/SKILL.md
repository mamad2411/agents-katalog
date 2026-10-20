# /add-anima-module — Generate Standardized anima_module.yaml

Use this skill when: a module needs its `anima_module.yaml` created or updated to match the v1.0 schema. Every ANIMA module MUST have this file.

## What It Does

1. Reads `CLAUDE.md`, `pyproject.toml`, `ASSETS.md`, existing `anima_module.yaml`
2. Generates a complete `anima_module.yaml` following the v1.0 schema
3. Validates all required fields are present
4. Pushes to GitHub repo
5. Pushes to HuggingFace repo (if it exists)

## Schema v1.0 — Required Structure

```yaml
schema_version: "1.0"

module:
  name: <lowercase_name>              # REQUIRED: a-z0-9_- only
  version: <semver>                   # REQUIRED: e.g. 1.0.0 or 0.1.0
  display_name: "<NAME> — <Tagline>"  # REQUIRED: human-readable
  description: "<what it does>"       # REQUIRED: one-line description
  category: <domain.subdomain>        # REQUIRED: see categories below
  license: Apache-2.0                 # REQUIRED
  paper: "<paper title, venue>"       # optional

capabilities:
  provides:
    - type: <capability>              # REQUIRED: what this module DOES
      subtype: <specific>             # REQUIRED

interface:
  inputs:
    - name: <input_name>              # REQUIRED: at least 1
      ros2_type: <msg_type>           # REQUIRED
      encoding: [<formats>]           # optional
      min_hz: <number>                # optional
  outputs:
    - name: <output_name>             # REQUIRED: at least 1
      ros2_type: <msg_type>           # REQUIRED
      typical_hz: <number>            # optional
  parameters:                         # optional
    - name: <param>
      type: <int|float|string|bool>
      default: <value>
      required: <true|false>

hardware:
  platforms:                          # REQUIRED: at least 1
    - name: nvidia_jetson
      backends: [tensorrt, onnxruntime_cuda]
    - name: apple_silicon
      backends: [coreml, mlx]
    - name: linux_x86
      backends: [onnxruntime_cuda, onnxruntime_cpu]

performance:
  profiles:                           # REQUIRED: at least 1 (estimate if unknown)
    - platform: <platform_name>
      model: <model_variant>
      backend: <backend>
      fps: <number>
      latency_p50_ms: <number>
      vram_mb: <number>               # optional

safety:
  failure_mode: <returns_empty|last_valid|safe_stop|escalate>  # REQUIRED
  timeout_ms: <number>                # REQUIRED: minimum 100
  health_topic: /anima/<name>/health  # REQUIRED: starts with /

composability:
  pairs_well_with:                    # REQUIRED (can be empty [])
    - category: <domain.subdomain>
  conflicts_with: []                  # REQUIRED (can be empty [])

container:
  image: ghcr.io/robotflow-labs/anima-<name>:<version>  # REQUIRED
  port: <number>                      # optional (default 8080)
  grpc_port: <number>                 # optional
```

## Categories Reference

| Domain | Subdomains |
|--------|-----------|
| perception | object_detection, segmentation, depth_estimation, place_recognition, scene_understanding, slam, point_cloud, pose_estimation, tracking |
| manipulation | vla, grasping, trajectory_planning, agentic, tactile |
| navigation | path_planning, obstacle_avoidance, exploration |
| planning | trajectory, task_planning, motion_planning |
| simulation | generation, environment, physics |
| training | post_training, sim_human, reinforcement_learning, distillation |
| evaluation | benchmark, memory_eval, safety_eval |
| coordination | multi_robot, fleet, memory |
| tooling | compression, certification, export |
| defense | adversarial_detection, adversarial_attack, signal_processing, threat_detection |
| healthcare | surgical, pathology, diagnostics, monitoring, drug_discovery |

## How to Fill Unknown Fields

- **performance**: Estimate based on model size. Small model (<100M params): fps=30, latency=20ms. Large model (>1B params): fps=5, latency=200ms.
- **interface.inputs**: Read the module's data pipeline — what does `process()` accept? Map to ROS2 message types.
- **interface.outputs**: What does the module return? Map to standard or custom ROS2 msgs.
- **hardware.platforms**: If module uses PyTorch → linux_x86 + nvidia_jetson. If lightweight → add apple_silicon.
- **safety.failure_mode**: Most perception modules → `returns_empty`. Control modules → `safe_stop`. Coordination → `escalate`.

## Execution Steps

1. Read `CLAUDE.md` — get module purpose, paper reference, category
2. Read `pyproject.toml` — get name, version, description
3. Read `ASSETS.md` — get model info, data dependencies
4. Read existing `anima_module.yaml` — preserve any existing correct fields
5. Read `src/*/serve.py` — infer interface from process() signature
6. Generate complete `anima_module.yaml` following schema v1.0
7. Validate: all required fields present, health_topic starts with `/`, timeout >= 100
8. Write file
9. `git add anima_module.yaml && git commit -m "[MODULE] Add/update anima_module.yaml v1.0" && git push`
10. If HF repo exists: `huggingface-cli upload <repo> anima_module.yaml anima_module.yaml`

## Validation Checklist

- [ ] `schema_version` is exactly `"1.0"`
- [ ] `module.name` is lowercase, matches directory name
- [ ] `module.version` is valid semver
- [ ] `module.category` uses `domain.subdomain` format from categories list
- [ ] `capabilities.provides` has at least 1 entry with type + subtype
- [ ] `interface.inputs` has at least 1 entry with name + ros2_type
- [ ] `interface.outputs` has at least 1 entry with name + ros2_type
- [ ] `hardware.platforms` has at least 1 entry with name + backends
- [ ] `performance.profiles` has at least 1 entry with platform, model, backend, fps, latency_p50_ms
- [ ] `safety.failure_mode` is one of: returns_empty, last_valid, safe_stop, escalate
- [ ] `safety.timeout_ms` >= 100
- [ ] `safety.health_topic` starts with `/anima/`
- [ ] `composability.pairs_well_with` exists (can be `[]`)
- [ ] `composability.conflicts_with` exists (can be `[]`)
- [ ] `container.image` follows `ghcr.io/robotflow-labs/anima-<name>:<version>`
