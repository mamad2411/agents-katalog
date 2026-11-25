---
name: config-reference-docs
description: Create structured CONFIG_REFERENCE.md documents for YAML/JSON config files that lack inline comments or have
  grown past ~400 lines.
metadata:
  hermes:
    triggers:
    - config reference
    - config doc
    - config.yaml documentation
    - CONFIG_REFERENCE.md
    - reference doc creation
    - documentation gap
    - no inline comments config
    tags:
    - documentation
    - configuration
    - reference
    - reading
    related_skills:
    - project-documentation-standards
version: 1.0.0
author: Hermes Agent
license: MIT

---

# Config Reference Documentation

Create structured reference documents for configuration files that have grown beyond scannable size or have zero inline comments.

## When to Use

- A project's config file exceeds ~400 lines or ~30 top-level sections
- The config file has zero inline comments
- A directory README describes *what* files exist but not *what each section does*
- Users or agents need to tune config values but can't guess semantics from key names alone

## Workflow

### 1. Structural Analysis

Parse the config with `yaml.safe_load()` and extract:
- Total top-level sections (drives doc scope)
- Largest sections by sub-key count (need most explanatory text)
- Sections with nested dicts (need sub-section descriptions)
- List-valued sections (flat lists vs lists of dicts)

### 2. Group by Domain

Group sections by functional domain, not alphabetically:

| Domain | Example Sections |
|--------|-----------------|
| Agent Behavior | agent, approvals, compression |
| Model & Providers | model, fallback_model, delegation, auxiliary |
| Communication | discord, telegram, gateway, api_server |
| Execution | terminal, code_execution, browser |
| Storage & Memory | memory, skills, curator |
| Automation | cron, kanban |
| Security | security, privacy, secrets |
| Voice/Speech | voice, tts, stt |
| Display | display, streaming |

### 3. Extract Key Defaults

Per section, document: purpose (1 line), key keys (2-5 most important with current values), shape (dict/list/scalar).

### 4. Add Registry Catalog

If the config has plugin/server registries (e.g. `mcp_servers`), create categorized listings with command type, timeout range, and purpose.

### 5. Add Tuning Patterns

Include a goal-to-change table mapping user intents to config changes.

### 6. Cross-Reference Directory README

- Fix stale line counts
- Add table row pointing to the new doc
- Add Related Documentation link

## Anti-Patterns

- Do NOT document sections alphabetically — group by domain
- Do NOT create when the config has good inline comments (duplicates effort)
- Do NOT create when config has <10 top-level sections (directory README is enough)
- Do NOT create for generated configs never manually edited (upstream docs are responsible)
