---
name: agent-workspace-migrate
description: 'Plan or perform authorized migration of agent skills, instructions, hooks and configuration across consumers. Use when moving agent setup between tools or hosts. RU: перенос настроек агента.'
license: MIT
disable-model-invocation: true
---

# Agent workspace migration

Classify each requested artifact by actual consumer contract: directly reusable, convertible, runtime-specific or transient/private. Inventory source and destination, collision handling, symlink targets, tracked and untracked state, and supporting files before changes. Keep secret stores, histories and caches out of portable content unless explicitly in scope; an installation of instructions does not authorize actions they describe.

Preserve the existing Git index, unrelated edits and unique destination content. Check tracked path-to-path identity and modes when relocating; a sorted hash multiset cannot detect swapped paths. Update active references without rewriting historical evidence. Never assume a readable symlink is a writable alias: atomic replacement can replace the link itself, and staging through a directory link may fail after earlier writes.

Verify from the actual target consumer using its documented discovery and permission interfaces. File presence, successful copying, installation, registration and runtime behavior are separate claims. For plugins, compare the loaded artifact with the intended candidate: a Git-based installer may use committed source rather than dirty working-tree bytes. Respect the task's explicit exclusions and defer installation or activation when requested.
