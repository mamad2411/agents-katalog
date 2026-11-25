---
name: agent-project-sync
description: 'Resolve project identity or synchronize an installed asset using the runtime''s authorized interfaces. Use when a project must be identified or an installed copy refreshed. RU: реестр проектов.'
disable-model-invocation: true
---

# Project registry and asset synchronization

When the task depends on a project location, obtain its identity and path from the user's scope or available registry interface. Verify the returned workspace is the intended accessible project and distinguish local and remote copies. Never infer a project or register a location solely from a similar name.

When synchronization is requested, resolve the maintained source, installed target, direction, owning files and applicable permissions. Inspect relevant dirty or staged work and compare the actual candidate; the existence of two copies is not permission to overwrite either. Preserve unrelated changes and secrets. Use supported update interfaces, verify resulting versions and behavior at the appropriate boundary, and report differences, blockers and whether already-running processes need a reload. Do not assume a runtime-specific registry, host path, symlink or cache layout.
