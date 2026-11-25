---
name: renovate-config-patterns
description: Reusable Renovate config templates (domain-agnostic JSON assembly primitive)
category: Base Primitive
---

# Renovate Config Patterns Skill (v1)

> **Skill ID:** `renovate-config-patterns`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

A domain-agnostic base primitive for assembling Renovate configuration from parameterized templates. Provides reusable config patterns for common scenarios: base recommended, auto-merge with auto-rebase, monorepo setups, and language-specific patterns (JS/TS, Python, Docker, etc.).

## Composition Rationale

This skill is a **base primitive**. It owns ONLY the generic template assembly logic (JSON merge + template variable substitution). The primitive is domain-agnostic — it knows nothing about Renovate's specific config schema beyond the template files themselves.

Multiple composer skills (e.g., `renovate-dependent-branch-auto-rebase`, future `github-workflow-renovate`) will consume this primitive by shelling out to `scripts/generate-renovate-config.py` and providing the template name + parameters.

## Related Skills

- [`renovate-auto-rebase-detector`](../renovate-auto-rebase-detector/SKILL.md) — consumes generated configs to detect auto-rebase behavior
- [`renovate-dependent-branch-auto-rebase`](../renovate-dependent-branch-auto-rebase/SKILL.md) — composer that uses this base for config generation
- [`github-workflow-renovate`](../github-workflow-renovate/SKILL.md) — future composer for GitHub Actions workflow generation

## Source Rules

| Rule File | Scope Incorporated |
|---|---|
| [`ai-rule-standardization-rules.md`](../../../../ai-agent-rules/ai-rule-standardization-rules.md) | Skill-First Architecture, Layered Composition Mandate |
| [`scripting-language-selection-rules.md`](../../../../ai-agent-rules/scripting-language-selection-rules.md) | Tier-1 (Python) default for new scripts |
| [`skill-factory/SKILL.md`](../../../skill-factory/SKILL.md) | Industrial protocol for skill creation |

***

## 1. When to Apply

Apply this skill when you need to generate a Renovate configuration file from a known template with parameter substitution. Use cases:

- Generating a base Renovate config for a new repository
- Creating a Renovate config with auto-rebase enabled (`rebaseWhen: "behind-base-branch"`)
- Creating a Renovate config with auto-merge + auto-rebase for specific package types
- Generating monorepo-aware Renovate configs
- Generating language-specific configs (JS/TS, Python, Docker, etc.)

Do NOT apply when:
- You need to parse or validate an existing Renovate config (use `renovate-auto-rebase-detector` instead)
- You need to orchestrate a full auto-rebase workflow (use `renovate-dependent-branch-auto-rebase` instead)

***

## 2. Prerequisites

| Requirement | Minimum |
|---|---|
| Python | 3.12+ |
| Dependencies | `ruff` (lint), `pytest` (test) |
| Template files | Present in `scripts/templates/` |

***

## 3. Step-by-Step Procedure

### 3.1 Template Inventory

The skill ships with these template files in `scripts/templates/`:

| Template | Description | Key Parameters |
|---|---|---|
| `renovate-config-base.json.template` | Minimal recommended config (`extends: ["config:recommended"]`) | — |
| `renovate-config-automerge.json.template` | Auto-merge + auto-rebase enabled | `rebaseWhen`, `automergeSchedule`, `automergeStrategy` |
| `renovate-config-monorepo.json.template` | Monorepo-aware with package groups | `packageRules`, `baseBranchPatterns` |
| `renovate-config-docker.json.template` | Docker-specific with pin digests | `dockerfileMatch`, `pinDigests` |
| `renovate-config-python.json.template` | Python-specific with constraints filtering | `constraints`, `constraintsFiltering` |

### 3.2 Generation Script

**Script:** `scripts/generate-renovate-config.py`

**CLI Contract:**

```bash
python3 scripts/generate-renovate-config.py \
    --template <base|automerge|monorepo|docker|python> \
    --output <path> \
    --params <json-string> \
    [--validate]
```

**Parameters (via `--params` JSON):**

| Template | Required Params | Optional Params |
|---|---|---|
| `base` | — | `extends`, `schedule`, `timezone` |
| `automerge` | — | `rebaseWhen`, `automergeSchedule`, `automergeStrategy`, `automergeType`, `packageRules` |
| `monorepo` | `packageRules` (JSON array) | `baseBranchPatterns`, `schedule` |
| `docker` | — | `pinDigests`, `dockerfileMatch` |
| `python` | — | `constraints`, `constraintsFiltering` |

**Output:** Writes rendered JSON to `--output` path. Exits 0 on success, 1 on template not found / render error / validation failure.

**Validation (`--validate`):** Runs `renovate-config-validator` if available, otherwise basic JSON syntax check.

### 3.3 Template File Format

Templates are JSON files with `{{parameter}}` placeholders (Python `string.Template` syntax). Example:

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "rebaseWhen": "{{rebaseWhen}}",
  "automerge": {{automerge}},
  "automergeType": "{{automergeType}}",
  "automergeStrategy": "{{automergeStrategy}}",
  "automergeSchedule": {{automergeSchedule}},
  "packageRules": {{packageRules}}
}
```

Default values for optional parameters are provided in the script's `DEFAULTS` dictionary.

***

## 4. Composition by Higher-Level Skills

| Composer | Composition Mechanism |
|---|---|
| [`renovate-dependent-branch-auto-rebase`](../renovate-dependent-branch-auto-rebase/SKILL.md) | Calls `scripts/generate-renovate-config.py --template automerge --params '{"rebaseWhen": "behind-base-branch", "automerge": true}'` to generate config with auto-rebase enabled |
| [`github-workflow-renovate`](../github-workflow-renovate/SKILL.md) | (Future) Generates Renovate config as part of GitHub Actions workflow setup |

***

## 5. Acceptance Criteria

The skill is complete when:

1. All template files exist in `scripts/templates/` with `.template` extension
2. `scripts/generate-renovate-config.py` renders all templates correctly with provided params
3. Output is valid JSON matching Renovate schema (validated with `renovate-config-validator` if available)
4. Unit tests pass for each template with various parameter combinations
5. `CHANGELOG.md`, `TRACEABILITY.md`, `AGENTS.md` present and compliant
6. `skill-cross-reference-audit` passes

***

## 6. Related Conversations & Traceability

- Session 2026-09-19: Initial creation per implementation plan `2026-09-19-renovate-auto-rebase-documentation.md`
- Renovate config schema: https://docs.renovatebot.com/renovate-schema.json

***

## 7. Change History

| Timestamp | Summary of Changes | Rationale |
| :--- | :--- | :--- |
| [2026-09-19 16:00] | Initial skill v1 created | Base primitive for Renovate config template assembly |

---

## 8. Traceability

See [`TRACEABILITY.md`](TRACEABILITY.md) for session logs and provenance.

---

## 9. Changelog

See [`CHANGELOG.md`](CHANGELOG.md) for release history.