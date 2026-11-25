---
name: skill-project-brain
description: Manage reusable project brain files so agents can resume work across conversations without rescanning the whole repository.
category: workflow
---

# Skill: Project Brain

Use when checking, creating, refreshing, or querying `memory` memory.

## Core files

```text
.maestro/knowledge/project.yaml
.maestro/knowledge/index.yaml
.maestro/registry/components.yaml
.maestro/registry/agents.yaml
.maestro/knowledge/test-policy.yaml
.maestro/runtime/workflow-state.yaml
.maestro/knowledge/components/<component-id>.yaml
```

## Rules

```text
Read memory index before opening detailed memory files.
Read project brain before scanning source.
Prefer partial refresh over full rescan when stale areas are known.
Refresh .maestro/knowledge/index.yaml after durable memory changes.
Record confidence for inferred facts.
Never store secrets, raw tokens, passwords, or long logs.
Link durable facts to source task or onboarding evidence.
```

## Staleness triggers

```text
Workspace/package config changed
Service folder added, removed, or moved
Framework or package manager changed
API/event/schema contract changed
Test policy changed
Generated coder scope changed
```
