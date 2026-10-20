---
name: rcc-robots
description: Use for RCC automation projects, robot.yaml, conda.yaml, Holotree, Environment Artifact use, freezes, bundles, templates, envs, and tasks.
---

# RCC Robots

Use this skill for RCC-backed automation projects and runtime/environment work once the task is clearly about a `robot.yaml` project. Here, `robot` is the RCC packaging/runtime convention, not a claim that Robocorp owns the architecture or current product direction. Keep literal package/API names such as `robocorp.tasks`, `robocorp.workitems`, `robocorp-browser`, and `ROBOCORP_HOME` when the project uses them. Use `$rcc-core` for RCC source, installation, endpoint, Holotree/cache, Environment Artifact lifecycle/provider/trust/coordination, or template catalog work before a task starts.

Retain ownership of `robot.yaml`, `conda.yaml`, holotree, freeze files, task runtime, and artifacts. Route `.robot` suite mechanics to `$rcc-robot-framework` and `RPA.*` library selection to `$rcc-rpaframework`.

## First Inspection

1. Locate the robot root by finding `robot.yaml`; inspect nearby `conda.yaml`, `devdata/*.json`, `.gitignore`, freeze files, and output/artifacts policy.
2. Read `robot.yaml` before task code: tasks, `devTasks`, `environmentConfigs`, `artifactsDir`, `PATH`, `PYTHONPATH`, and ignored files decide how RCC runs the project.
3. Read `conda.yaml` next: channels, Python version, `uv`, pip packages, `rccPostInstall`, and environment variables.
4. For work-item robots, compare task names with role-specific env files and helper tasks such as `SeedDocDB`, `RunDocDBHelper`, queue/index diagnostics, and artifact export.
5. Inspect task entry points only after config: `tasks.py`, `src/**`, tests, scripts, and any templates copied into the project.

## Operating Rules

- Run or request `rcc ht vars -r robot.yaml` first when startup fails; it separates RCC/holotree resolution from Python/task failures.
- For host/RCC health before a `robot.yaml` project exists, prefer `rcc diagnostics --quick --json` and `$rcc-core`.
- Prefer `environmentConfigs` with platform freeze fallbacks for reproducible contained automation. Use single `condaConfigFile` only for simple local work.
- For uv-native environments, preserve the exact declared Python and uv versions. RCC v18.18+ isolates inherited `UV_*` settings, uses `UV_NO_CONFIG=1`, disables implicit Python downloads after staging, and requires dependency inventory plus strict checks before recording layers.
- Environment Artifact publication remains opt-in. Keep the source environment, immutable Artifact, provider, consumer-local materialization, and execution receipt separate; do not add remote publication to a baseline robot template.
- Use RCC environment commands for Python checks, not host Python.
- Keep helper scripts that need robot dependencies behind `rcc task script` or a declared `robot.yaml` task, especially in CI.
- Use `ROBOT_ROOT` and `ROBOT_ARTIFACTS` for raw path resolution; in `robocorp.tasks`, prefer `get_output_dir()` and `get_current_task()`.
- If changing package pins, verify PyPI or source metadata in the current run. Keep shared template pins consistent.
- Do not steer users toward upstream Robocorp/Sema4.ai platform paths unless the task explicitly targets those interfaces; this skill assumes RCC-first local/CI automation by default.

## References

- `references/rcc-command-recipes.md`: command selection, `robot.yaml`, `conda.yaml`, holotree, bundles, and cache hygiene.
- `references/robot-project-recipes.md`: Josh automation-project templates, Python/browser/work item/UV-native patterns, and template release behavior.
- `references/troubleshooting-validation.md`: environment, dependency, runtime, work item, Action Server, and repo validation playbooks.
- `references/hooks.md`: optional Claude Code hook assets and command guardrails for RCC projects.
- `../rcc-workitems/references/docdb-rpa-patterns.md`: DocDB-backed production robot task surface, helper task boundary, local smoke ladder, and CI queue semantics.
- `../rcc/references/python-library-audit.md`: cross-source Python library map, examples, and source refresh workflow.
- `../rcc/references/source-map.md`: source evidence for current recipes.
- `../rcc-core/references/rcc-source-recipes.md`: RCC CLI/source, holotree/cache, endpoint, template, and remote-cache orientation.
- `../rcc-core/references/environment-artifacts.md`: robot/package publication, private-home acquisition, offline archives/bundles, consumer rebasing, execution receipts, and warm reuse.
- `../rcc-core/references/providers-and-trust.md`: provider profiles, cache server, credentials, and artifact trust.

## Assets And Scripts

- Robot templates live in `assets/templates/`.
- HITL Assistant + work item starter lives in `assets/templates/hitl-assistant/`.
- Optional Claude hook assets live in `assets/claude-hooks/`; use only when mirroring Claude Code hook behavior.
- Run `python3 plugins/rcc/skills/rcc-robots/scripts/validate_robot.py path/to/robot.yaml` for static robot config validation when PyYAML is available.
- Run `python3 plugins/rcc/skills/rcc-robots/scripts/env_check.py --skip-network` for quick local RCC/project health checks.
