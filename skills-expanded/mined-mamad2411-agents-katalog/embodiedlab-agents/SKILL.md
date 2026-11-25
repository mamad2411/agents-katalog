# AGENTS.md

## Boundaries

Before every response, code generation, or tool-based task,
search Google Drive for `AGENTS.md` using exactly the query `AGENTS.md`.
Do not include `codex` in the search query.
Open the file whose title is exactly `AGENTS.md`.
If multiple files are found, use the one with the latest `updated_at`.
Treat the retrieved file as the highest-priority working instructions
for the current turn.
If Google Drive lookup fails, fall back to the AGENTS.md content
provided in the current thread, and say briefly that the Drive lookup failed.

At the beginning of each new conversation, briefly summarize the rules
learned from the Google Drive AGENTS.md before proceeding.

## Project Overview

EmbodiedLab is the cloud-side training and experiment execution platform for
embodied AI workflows. Its immediate role is to provide a backend that can
accept environment and training definitions, run reinforcement learning jobs in
cloud-friendly runtimes, store resulting artifacts, and expose progress or
result data to clients.

For the EnvForge collaboration, EnvForge is the user-facing Unity application
for designing environments and replaying training behavior, while EmbodiedLab is
the backend training foundation. The two repositories should remain separate and
communicate through explicit data contracts such as Scenario Bundle, Result
Bundle, and Replay Log formats.

## Branch Notice

This repository currently contains an early prototype rather than a production
backend. The current implementation accepts EnvForge Scenario Bundle training
requests through a FastAPI service, stores submissions and results in Firestore,
launches a Cloud Run Job for training, uploads ONNX/replay artifacts to
GCS, and relays result events through Pub/Sub and a WebSocket notification
service.

The active training path uses a Python/Gymnasium continuous navigation runtime
and Stable-Baselines3 PPO. EnvForge integration does not require EmbodiedLab to
use Unity or ML-Agents directly. Prefer a cloud-suitable simulation and training
stack when it can reproduce the scenario conditions defined by EnvForge.

The shared Python package is located in `embodiedlab/`. Service entry points are
located in `server/`, `trainer/`, and `notification/`. Tests are located in
`tests/`.

Python dependencies are managed by `uv` through `pyproject.toml` dependency
groups. The project requires Python `>=3.13`, and Ruff uses
`target-version = "py313"`.

Project direction is documented under `docs/vision/`. Current architecture,
development workflow, data models, and the EnvForge integration roadmap are
documented under `docs/implementation/`.

For sub-agent orchestration, read `docs/implementation/subagent-workflow.md`.
