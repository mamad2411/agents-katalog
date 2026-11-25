---
name: rcc
description: Route RCC-family work across core, Environment Artifacts, providers, robots, work items, Action Server, CI/cache, and maintenance automation.
---

# RCC Router

Use this skill to triage RCC-family tasks. Load the specialist skill that matches the actual work, then continue there.

Treat RCC as the center of gravity for this stack. Frame the domain as RCC-managed contained automation built around `rcc`, `robot.yaml`, holotree environments, work item adapters, and local/CI execution. Keep literal dependency and API names such as `robocorp.tasks`, `robocorp.workitems`, `robocorp-browser`, and `ROBOCORP_HOME` when current code uses them, but treat Robocorp/Sema4.ai references as upstream dependency or interface history unless the task explicitly targets those upstream services or packages. Do not assume upstream Robocorp/Sema4.ai defines new feature direction or active open-source leadership for this stack.

## Route By Task

- Use `$rcc-core` for RCC itself: command selection, install/source orientation, Holotree/cache internals, Environment Artifacts, providers, trust, lifecycle/leases, build coordination/prewarm, endpoint/profile configuration, templates, bundles, remote cache/client behavior, and failures before a robot task starts.
- Use `$rcc-robots` for RCC-backed automation projects using the `robot.yaml` packaging/runtime convention: `conda.yaml`, environment configs, freeze files, task runtime, templates, artifacts, and task debugging.
- Use `$rcc-robot-framework` for `.robot` suites and resources, Robot CLI/Rebot, custom Robot libraries, results, and RCC `robot_tests` acceptance work.
- Use `$rcc-rpaframework` for `RPA.*` library selection, keyword recipes, package/platform needs, and interoperability with `robocorp.*` libraries.
- Use `$rcc-workitems` for classic `robocorp.workitems`, `actions-work-items`, producer/consumer/reporter flows, local SQLite/file queues, custom adapters, Redis, DocumentDB, and Yorko Control Room adapters.
- Use `$action-server` for `joshyorko/actions` packages, `package.yaml` v2, PyPI `actions-core` and `actions-runtime`, `actions.mcp`, Docker/Compose builds and deployments, OpenAPI/MCP exposure, secrets, dev tasks, action tests, and typed responses.
- Use `$rcc-ci-maintenance` for RCC in GitHub Actions, `ROBOCORP_HOME` cache, pinned RCC install, scheduled maintenance automation, allowlist dependency maintenance, bot PR flows, and CI cache hygiene.

## Router Rules

- Do not keep detailed command recipes in this router. Load one specialist skill and its references.
- Route `rcc env`, `rcc provider`, and `rcc cache serve` to `$rcc-core`. If the artifact problem is specifically a robot/package configuration or task-runtime problem, pull in `$rcc-robots` after the RCC lifecycle boundary is clear.
- If a task crosses boundaries, start with the skill that owns the failing surface. Examples: a failing `rcc ht vars` before suite execution starts belongs to `$rcc-core`; a broken `robot.yaml` environment belongs to `$rcc-robots`; a wrong assertion in `robot_tests/ht_hash.robot` belongs to `$rcc-robot-framework`; choosing `RPA.Tables` versus a Python library belongs to `$rcc-rpaframework`.
- Treat artifact publication, provider-profile replacement/removal, lifecycle repair, cache-provider administration, and coordinator release as state-changing operations. Inspect first and keep credentials out of command lines, files, logs, receipts, and provenance.
- For DocDB-backed RPA systems that mix queue naming, helper scripts, retry, outbox, dashboards, or GitHub Actions matrix workers, start with `$rcc-workitems`; pull in `$rcc-robots` or `$rcc-ci-maintenance` only after the queue boundary is clear.
- Keep canonical edits under `plugins/rcc/skills/<skill>/`. Treat top-level `skills/` and `.agents/skills/` as generated views.
- Do not prototype marketplace servers, MCP servers, web services, daemons, or new runtime products from this plugin. `action-server` covers normal action-package work only.
- When the user explicitly asks to expose Dagger to agents, use `references/dagger-mcp.md` and `scripts/rcc-dagger-mcp`. The installed plugin uses its bundled RCC module by default; use `RCC_DAGGER_REPO` only when the user asks for a different checkout.
- If Docker or Dagger is unavailable, or the task does not need Dagger isolation, use the normal `rcc` binary directly. Start with `$rcc-core` for binary/version/install checks and run `rcc version` or the relevant `rcc ...` command in the active project context.

## Shared References

- `references/python-library-audit.md`: cross-source Python library evidence, example gaps, and refresh commands for RCC-family recipes.
- `references/source-map.md`: source evidence for RCC plugin refreshes.
- `../rcc-core/references/environment-artifacts.md`: Environment Artifact identity, compatibility, lifecycle, archives, leases, repair, and warm reuse.
- `../rcc-core/references/providers-and-trust.md`: providers, `cache serve`, enterprise transport, trust carriers/policy, receipts, and legacy `rccremote` boundaries.
- `../rcc-core/references/build-coordination.md`: shipped coordination/prewarm CLI, state model, limitations, and evidence boundaries.
- `references/agent-prompt-examples.md`: short prompts that point future agents at the right specialist skill.
- `references/dagger-mcp.md`: opt-in bridge for exposing a local RCC Dagger module through Dagger's MCP server.
- `../rcc-workitems/references/docdb-rpa-patterns.md`: production DocDB/RPA queue, helper, retry, outbox, artifact, and CI patterns from the local BPS example.
