---
name: missionforge-workflow
description: End-to-end MissionForge workflow — from mission initialization through decomposition, baseline capture, implementation, and reporting.
version: 1.0.0
author: loudiman
triggers:
  - missionforge workflow
  - missionforge full workflow
  - how to use missionforge
  - missionforge end to end
  - start a mission
---

# missionforge-workflow

The complete MissionForge workflow for managing AI-assisted software missions from start to finish. Use this as your reference for the full lifecycle.

## Install

```bash
pip install git+https://github.com/loudiman/Mission-Forge.git
# or from source:
pip install -e ".[dev]"
```

## Full Lifecycle

### Phase 1 — Initialize

Create the mission workspace and define the parent mission:

```bash
missionforge init MF-001
# Edit .missionforge/missions/MF-001/mission.yaml
missionforge mission MF-001 --validate
```

### Phase 2 — Decompose

Break the parent mission into independently-executable sub-missions:

```bash
missionforge decompose MF-001
# Creates sub-mission templates in sub-missions/
# Fill in each MF-001-A.yaml, MF-001-B.yaml, etc.
missionforge validate-submission MF-001 MF-001-A
missionforge validate-submission MF-001 MF-001-B
```

### Phase 3 — Baseline

Capture pre-implementation metrics for each sub-mission:

```bash
missionforge baseline capture MF-001-A
# Edit baseline.todo.json with measured values
missionforge baseline commit MF-001-A
```

Repeat for each sub-mission before writing any implementation code.

### Phase 4 — Plan

Generate or review the execution plan:

```bash
missionforge plan MF-001
```

### Phase 5 — Implement

Work through sub-missions in order. Use `next` to see what's up:

```bash
missionforge next MF-001
```

Check workspace status anytime:

```bash
missionforge workspace status
```

### Phase 6 — Report

Generate a mission report after implementation:

```bash
missionforge report MF-001
```

## Command Quick Reference

| Command | Purpose |
|---------|---------|
| `missionforge init <ID>` | Initialize mission workspace |
| `missionforge mission <ID> --validate` | Validate parent mission.yaml |
| `missionforge decompose <ID>` | Guided sub-mission decomposition |
| `missionforge validate-submission <ID> <SUB_ID>` | Validate a sub-mission file |
| `missionforge baseline capture <SUB_ID>` | Generate baseline.todo.json |
| `missionforge baseline commit <SUB_ID>` | Commit immutable baseline.json |
| `missionforge baseline reset <SUB_ID> --force` | Reset baseline for re-capture |
| `missionforge plan <ID>` | Generate execution plan |
| `missionforge next <ID>` | Show next sub-mission to implement |
| `missionforge report <ID>` | Generate mission report |
| `missionforge workspace status` | List all missions and their status |

## Global Options

```bash
--verbose, -v     # Enable DEBUG logging
--log-file PATH   # Write logs to file
```

## Mission ID Conventions

- Parent: `MF-001`, `PROJ-042`, `FG-123A`
- Sub-mission: `MF-001-A`, `MF-001-B`, `PROJ-042-C`

## Individual Skill Docs

- [`mission-init`](../mission-init/SKILL.md) — workspace initialization
- [`mission-validate`](../mission-validate/SKILL.md) — schema validation
- [`mission-decompose`](../mission-decompose/SKILL.md) — decomposition workflow
- [`baseline-capture`](../baseline-capture/SKILL.md) — baseline metrics
