---
name: vaaet-pipeline-architecture
description: Assess, design, review, or safely evolve VAAET ML architecture. Use for VAAET layer boundaries, video-pipeline changes, Pipe-and-Filter design, potential Producer-Consumer optimization, performance profiling, or concurrency decisions in vision workflows.
---

# VAAET Pipeline Architecture

## Architecture position

Keep layers as VAAET's principal architecture:

| Layer | Responsibility |
| --- | --- |
| `vaaet-ml/notebooks/` | Colab UI and workflow orchestration only |
| `vaaet-core/src/vaaet/vision/` | Video, YOLO, tracking, motion, speed, HUD, telemetry |
| `vaaet-core/src/vaaet/features/`, `inference/`, `artifacts.py` | 19 features, state policy, bundle validation and portable inference |
| `vaaet-ml/src/vaaet_ml/data/` | Input sources, persistence, dataset artifacts, HITL, lineage |
| `vaaet-ml/src/vaaet_ml/training/`, `evaluation/` | Lifecycle, training and laboratory validation |

Preserve `vaaet.vision.analyze_video()` as the portable shared boundary for collection and inference. Keep notebooks thin; core owns video behavior and ML owns laboratory workflows.

Read ADR-0021, ADR-0026, ADR-0027, and ADR-0013 through ADR-0019 before architectural changes. Read ADR-0022 for future serving with YOLO. Do not change the 19 `FEATURE_COLS`, state semantics, MLP, thresholds, schema, or bundle v3 without explicit authorization and an ADR.

## Current state: do not misrepresent it

VAAET currently has a synchronous, ordered frame loop in `analyze_video()` with logical filters:

```text
read frame → optical flow → YOLO detection → SORT tracking
→ speed/motion → minute telemetry → optional prediction → HUD/video write
```

This is not an implemented concurrent Pipe-and-Filter or Producer-Consumer runtime. There are no computation queues between these stages. The review queue and SQLAlchemy connection pool are unrelated to frame-processing concurrency.

Describe the current implementation as a layered batch/video pipeline with logical stages. Describe Pipe-and-Filter and Producer-Consumer below as future, conditional design options only.

## Pipe-and-Filter: preferred internal organization

Use Pipe-and-Filter inside the vision workflow when a requested change benefits from independently testable stage contracts. Keep stages ordered and make each input/output explicit:

```text
FramePacket → DetectionPacket → TrackingPacket → MotionPacket
→ TelemetryRecord → PredictionRecord → RenderedFrame/PersistenceBatch
```

Implement filters as narrow functions or classes in `vaaet.vision`, not as notebook cells. Preserve `frame_index`, clip identity, capture time, FPS, and any state required for deterministic recovery. Validate malformed packets at stage boundaries and include the stage name in redacted errors/logs.

Do not split the following stateful chain across unordered workers:

- SORT tracking, optical flow, speed smoothing, stationary detection, and minute accumulation.
- Classification policy and incident persistence, which require complete, ordered minutes.
- Any operation that could alter the order of a clip's frames or telemetry rows.

## Producer-Consumer: future and narrowly scoped

Consider a local, in-process bounded queue only after profiling shows that decode/CPU preparation starves a single YOLO GPU worker or that output encoding blocks it. The first candidate boundary is:

```text
ordered frame producer → bounded local queue → one GPU detection consumer
```

An optional second boundary may sit after ordered results and before video encoding or an idempotent persistence batch. Do not introduce Kafka, Celery, a remote broker, a persistent worker fleet, or cross-runtime queues for the current Colab workflow.

If implementation is authorized, require all of the following:

1. Use a small bounded queue to provide backpressure and protect Colab RAM.
2. Keep one GPU consumer unless measured evidence supports batching; never duplicate model memory blindly.
3. Carry monotonic frame IDs and restore output order before tracking, rendering, telemetry, or persistence.
4. Define sentinels, timeout/error propagation, cancellation, resource release, and deterministic shutdown.
5. Keep `pipeline_run` metadata redacted; make persistence explicit and idempotent.
6. Measure baseline versus candidate on the same representative clip: throughput, latency, peak RAM/VRAM, dropped/reordered frames, telemetry equivalence, and output-video correctness.

Reject the change if throughput does not improve materially, RAM approaches the Colab budget, ordering cannot be proven, or tests show behavior drift.

## Do not apply these patterns here

- Do not apply Producer-Consumer to training, dataset ingestion planning, HITL catalog resolution, frozen holdouts, or input locks. Those workflows require snapshots, checksums, fixed partitions, and reproducibility rather than streaming concurrency.
- Do not make asynchronous persistence an implicit side effect of inference. Preserve workflow roles and explicit opt-in persistence.
- Do not use queues as a way to bypass artifact validation, human confirmation of Accident, or promotion gates.

## Change workflow

For a proposal or implementation request:

1. Inspect existing stage boundaries and profile the current path first.
2. State the measured bottleneck and the exact proposed boundary.
3. Ask for authorization before a major architectural refactor.
4. Preserve public APIs where possible; otherwise propose an ADR and migration/test plan.
5. Add focused unit tests for packet ordering, backpressure, shutdown/error propagation, and output equivalence.
6. Run Ruff, tests, compilation, notebook syntax checks, Markdown-link checks, and `git diff --check`.

Report the result as an evidence-based decision: keep synchronous, adopt a local bounded boundary, or reject the optimization.
