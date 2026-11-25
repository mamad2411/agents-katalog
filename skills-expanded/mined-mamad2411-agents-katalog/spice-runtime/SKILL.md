---
name: spice-runtime
description: Route for Spice decision runtime and `spice-hermes-bridge`. Use when the task mentions Spice, spice-runtime, Spice decision layer, spice-hermes-bridge, or Chinese triggers such as Spice 决策层、Spice 决策运行时、决策层 runtime.
tags: [spice, decision-runtime, bridge, hermes, agent, runtime]
version: 1
---

# Spice Runtime / Bridge

Purpose
- Route Spice runtime and `spice-hermes-bridge` tasks to the locally reviewed source snapshot.
- Keep decision-layer review separate from runtime bring-up and external messaging demos.

Local source
- ~/.hermes/external-repos/Spice/reviewed-source
- Upstream: https://github.com/Dyalwayshappy/Spice

Safe workflow
1. Read the reviewed `README.md`, `README_zh.md`, and both `pyproject.toml` files first.
2. Treat the local source as a reviewed snapshot. Full git checkout hung in this environment, so do not assume unreviewed files outside the snapshot are present locally.
3. Before `pip install spice-runtime`, `pip install -e .`, or bridge bring-up, keep the work inside an isolated venv and inspect any newly needed source paths first.
4. Do not run `spice setup`, `scripts/start_all.sh`, `hermes gateway run`, `ngrok`, WhatsApp ingress, or GitHub polling demos unless the user explicitly asks for runtime bring-up and confirms external integration scope.
5. Treat bridge demos, webhook exposure, and executor handoff as security-sensitive because they can touch messaging accounts, public tunnels, and downstream agent execution.

Chinese route triggers
- Spice, spice-runtime, spice runtime, spice-hermes-bridge, Spice decision layer, Spice 决策层, Spice 决策运行时, 决策层 runtime
