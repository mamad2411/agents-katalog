---
name: code-config-audit
description: 'Trace configuration, defaults, generated catalogs, startup wiring and readiness across services and environments. Use when implementing or reviewing configuration. RU: конфигурация, настройки, готовность сервиса.'
license: MIT
---

# Configuration contracts

Use when implementing or reviewing configuration, defaults, generated catalogs, process wiring or readiness. Establish the exact requested change and whether the task permits mutation; a read-only review does not authorize restart, build, deployment or secret access.

Trace each relevant key from its authoritative source and precedence through parsing, overrides, serialization, generated projections, startup guard and actual consumers. Distinguish absent, explicitly empty, invalid, disabled and false values according to the documented contract. Keep saved configuration, effective settings and already-running or persisted process state separate. Preserve unrelated credentials without opening, printing or exporting them.

Use [configuration and rollout verification](references/rollout-verification.md) for defaults, configuration formats and generated artifacts, and [startup and readiness](references/startup-readiness.md) for credential-gated endpoints and cross-process state. Report exact evidence, observed runtime scope and reload requirements; static validation alone does not prove an activated service.

For registries and published catalogs, read [registry and catalog consistency](references/registry-and-catalog.md).
