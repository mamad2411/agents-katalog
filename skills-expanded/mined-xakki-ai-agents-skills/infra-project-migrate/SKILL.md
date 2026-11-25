---
name: infra-project-migrate
description: 'Plan and verify an authorized migration of a named project, its services or data between hosts or runtimes. Use when moving a project to another environment. RU: перенос проекта на другой хост.'
disable-model-invocation: true
---

# Project migration

Use for moving a named project, its services or data between environments. Obtain source, destination, interfaces, ownership, scope and acceptance from the task and runtime. A plan, copy, startup, data synchronization, traffic cutover and source retirement are distinct phases; a connection or credential does not authorize any of them by itself.

Inventory relevant code and staged/untracked work, runtime configuration, secret references, data stores, queues, jobs, service identities and external dependencies. Include hidden or ignored material only when necessary and authorized; do not expose or copy secrets by default. Preserve unrelated work. A commit, push or particular infrastructure stack is not an assumed prerequisite.

Before an authorized transfer, establish capacity, permissions, consistency, recoverable backup and the supported transfer/restore method. Reconcile unique identities, schedules and in-flight work to avoid duplicate consumers or conflicting writes. Keep an actionable rollback plan for source, destination and any writes after synchronization; do not delete or retire source data without the relevant authority and evidence.

Validate the actual requested destination behavior and data scope through supported interfaces. Distinguish configuration checks, readiness, restored data and live end-to-end evidence; report unavailable checks and deferred cutover or cleanup. Do not assume fixed hostnames, credentials, paths or agent-specific commands.

For persistent state, traffic cutover or network boundaries, consult [data and cutover verification](references/data-and-cutover.md).
