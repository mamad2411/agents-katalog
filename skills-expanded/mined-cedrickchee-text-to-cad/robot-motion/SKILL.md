---
name: robot-motion
description: Robot motion setup, generation, and validation for URDF-based inverse kinematics and path planning. Use when Codex needs to install ROS 2 or MoveIt 2 dependencies, run or test the local motion server, generate CAD Explorer motion artifacts for a `.urdf`, create MoveIt/SRDF/kinematics/planning sidecars, debug IK or path-planning behavior, or validate robot motion commands.
---

# Robot Motion

Use this skill after a robot URDF exists and the task needs local motion behavior: IK, path planning, MoveIt configuration, websocket motion-server debugging, or ROS dependency setup. Any valid repo-local `.urdf` can be used when `gen_motion()` names links, joints, frames, and end effectors that exist in that file.

## Workflow

1. Start from an existing valid `.urdf`.
2. Generate motion artifacts from a Python source with zero-arg `gen_motion()` using `scripts/gen_motion_artifacts/cli.py`.
3. Verify the local motion environment with `scripts/check-motion-server.sh` when it may already exist; run `scripts/setup.sh` only when dependencies are missing or stale.
4. Run the websocket motion server with `scripts/run-motion-server.sh`.
5. Test protocol, artifact generation, and provider logic before handing off motion behavior.
6. For CAD Explorer handoff of motion-enabled `.urdf` entries, defer to the CAD skill and keep motion-specific metadata here.

## CAD Explorer Handoff

Read `.agents/skills/cad/SKILL.md`, then only load its `references/rendering-and-explorer.md` when a task needs an Explorer URL. If unavailable, use [cad-skill](https://github.com/earthtojake/cad-skill). Do not duplicate Explorer startup or URL syntax in this skill. Link the repo-local `.urdf` when motion artifacts or URDF targets were generated or changed, or when the user asks for browser review. Keep motion-specific Explorer metadata and motion-server behavior here.

## Commands

Run from the robot project repository root. If the current working directory is somewhere else, set `ROBOT_MOTION_REPO_ROOT` to the robot project root.

```bash
python .agents/skills/robot-motion/scripts/gen_motion_artifacts/cli.py <robot-urdf-source.py> --summary
```

```bash
.agents/skills/robot-motion/scripts/setup.sh
.agents/skills/robot-motion/scripts/check-motion-server.sh
.agents/skills/robot-motion/scripts/run-motion-server.sh
```

The runtime is host-agnostic but Conda/RoboStack/Jazzy-based. The setup script creates or updates the dedicated conda environment from `environment.yml`, installs `server/` in editable mode, and runs `motion_server --check`. Use any conda-compatible installation available through `ROBOT_MOTION_CONDA_EXE`, `CONDA_EXE`, `PATH`, or a common Miniforge/Miniconda/Anaconda install root. Do not install ROS or MoveIt packages into the repo CAD `.venv`, system Python, or system package managers.

Use `ROBOT_MOTION_REPO_ROOT`, `ROBOT_MOTION_CONDA_ENV_NAME`, `ROBOT_MOTION_CONDA_EXE`, `ROBOT_MOTION_HOST`, or `ROBOT_MOTION_PORT` only when a task needs non-default repository root, environment, conda executable, host, or port settings.

## Motion Artifacts

Use `references/motion-artifacts.md` when creating or editing `gen_motion()` envelopes, motion-owned sidecars, generated file expectations, or solve-vs-plan command choices.

## Motion Server

The browser talks to `motion_server` over a direct local websocket, defaulting to `ws://127.0.0.1:8765/ws`. Vite does not start or supervise the server.

The server package lives in `server/`. It validates requested URDF files against repo-local robot-motion explorer metadata and `robot-motion/motion_server.json`, loads MoveIt sidecars from `robot-motion/`, and dispatches `urdf.solvePose` / `urdf.planToPose` to providers.

## Troubleshooting

If `check-motion-server.sh` cannot find conda, locate an existing `*/bin/conda` and rerun with `ROBOT_MOTION_CONDA_EXE=/path/to/conda`. Do not run setup merely because conda discovery failed.

In sandboxed agent environments, binding or connecting to the local websocket may fail with `PermissionError` on `127.0.0.1:<port>`. Rerun the server or smoke-test command with the environment's approved out-of-sandbox/local-network mechanism; change `ROBOT_MOTION_PORT` only when the port is actually occupied.

## Tests

Run focused tests after changes:

```bash
PYTHONPATH=.agents/skills/robot-motion/server ./.venv/bin/python -m unittest discover .agents/skills/robot-motion/server/tests
PYTHONPATH=.agents/skills/robot-motion/scripts ./.venv/bin/python -m unittest discover .agents/skills/robot-motion/scripts/gen_motion_artifacts/tests
```

MoveIt adapter tests should stay isolated so they pass without a sourced ROS shell unless a test explicitly requires ROS.

## References

- Motion artifact specs: `references/motion-artifacts.md`
