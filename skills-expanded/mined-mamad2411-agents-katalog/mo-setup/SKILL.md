---
name: mo-setup
description: Inspect and bring a project and its environment up to the Meta-O contract, including substantive knowledge, instructions, tooling, backend companions, and unsandboxed Codex, Claude Code, and OpenCode posture.
license: MIT
---

# Set up a project for Meta-O

Read [Project setup contract](references/project-setup.md),
[Backend contract](references/backend-contract.md), and
[Purpose and architecture contract](references/purpose-and-architecture.md)
completely. For a Python project also read
[Python QC profile](references/qc-python.md) completely; for a TypeScript or
JavaScript project also read
[TypeScript QC profile](references/qc-typescript.md). Read both for a mixed
Python/TypeScript project. Read only the applicable language profiles completely.

Detect the active backend through its native environment and status surface;
report unsupported or ambiguous environments. When asked, check every supported
backend. Check controls and companion skills separately: `herdr` plus `herdr`,
`orca`/`orca-cli` plus upstream `orchestration`, and `paseo` plus upstream
`paseo`.

When watchdog readiness is in scope, check mature `jq` and `flock` dependencies
separately from backend controls.

Use each backend's native companion source: installed `herdr`, Orca's
version-matched `orca skills` guide, and an installed or version-matched bundled
Paseo guide. Report the exact source separately from control discovery; do not
copy a bundled skill into personal configuration without explicit confirmation.
For Paseo, check native provider discovery for Codex, Claude Code and OpenCode;
daemon health alone is insufficient, and a provider command failure is not an
empty catalog. Report missing managed directories without creating personal
state or restarting the daemon silently.

Inspect knowledge, entry instructions, README, architecture reasons, backlog
quality, E2E and acceptance mapping, language/build config, mature complexity
and size linting, significant-code purpose, deterministic non-mutating QC, and
unsandboxed Codex/Claude Code/OpenCode posture. Do not create a backend fixture
document in ordinary projects.

If tracked repair is required, explain it and use a separate
`feature/meta-o-setup` branch based on up-to-date `develop`; never mix setup
repair into the current feature branch. Personal configuration changes require
explicit confirmation.
