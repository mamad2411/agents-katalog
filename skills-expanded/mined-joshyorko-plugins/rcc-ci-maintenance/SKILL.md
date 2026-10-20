---
name: rcc-ci-maintenance
description: Use for RCC in GitHub Actions, Environment Artifact promotion/prewarm, ROBOCORP_HOME cache, pinned installs, maintenance, bot PRs, and cache hygiene.
---

# RCC CI Maintenance

Use this skill for RCC-powered CI and repository maintenance robots.

## First Inspection

1. Inspect workflow files before robot code: `.github/workflows/*.yml`, RCC install step, `ROBOCORP_HOME`, cache key, token permissions, commit/PR steps, runner labels, matrix settings, and artifact upload.
2. Inspect the maintenance robot root next: `automation/**/robot.yaml`, `conda.yaml`, allowlists, task entry points, and generated report path.
3. For production DocDB/RPA workflows, inspect ref/environment guards, queue-name setup, per-job credential loading, helper task calls, retry/outbox jobs, and whether live jobs accidentally use local `devdata` env files.
4. Confirm commit hygiene: cache dirs ignored, bot identity configured, branch naming explicit, and PR creation gated by detected changes.
5. If environment creation fails, use `$rcc-robots` for holotree and `conda.yaml` diagnostics.

## Operating Rules

- Pin RCC install versions in CI and include the RCC version plus robot/env config hashes in `ROBOCORP_HOME` cache keys.
- Pin the release-asset SHA-256 as well as the RCC version when downloading binaries. Bind promotion receipts to the exact source commit and binary digest.
- Disable telemetry in CI when the workflow pattern supports it.
- Load live secrets inside the RCC environment when helper code depends on robot packages; mask secret values and write to `GITHUB_ENV`, not cross-job outputs.
- For DocDB-backed worker matrices, count pending items from the queue, keep `fail-fast: false`, cap `max-parallel` to the runner scale set, and let workers atomically reserve from the shared queue.
- Store logs, screenshots, and summary artifacts in `if: always()` steps before dashboard/outbox jobs consume them.
- Add a safety guard that fails if RCC cache paths appear in `git status --porcelain`.
- Keep dependency maintenance allowlist-driven. Update only files and version families the allowlists name.
- Write maintenance reports as artifacts or ignored output files, then include useful summaries in bot PR bodies.
- Prefer branch + PR flow over direct pushes to the protected target branch.
- For Environment Artifacts, keep provider, consumer cache/materialization, coordinator state, and build staging in explicit isolated roots. Require trust/receipt checks and distinguish four-platform lifecycle evidence from Linux-only coordination/prewarm execution.

## References

- `references/room-of-requirement-maintenance.md`: sourced pattern from `joshyorko/room-of-requirement` maintenance robot and GitHub Actions workflow.
- `references/docdb-workflow-ci.md`: production DocDB/RPA GitHub Actions pattern for queue setup, helper calls, matrix workers, retry/outbox, and artifacts.
- `references/environment-artifact-ci.md`: v18.19.3 artifact promotion, native runtime, provider/trust, and coordination/prewarm CI evidence.
- `../rcc-workitems/references/docdb-rpa-patterns.md`: DocDB queue/outbox/helper details owned by the work-items skill.
- `../rcc-robots/references/rcc-command-recipes.md`: RCC command and cache background.
- `../rcc-robots/references/troubleshooting-validation.md`: CI and environment failure triage.
- `../rcc/references/source-map.md`: source evidence and inspected commit IDs.
