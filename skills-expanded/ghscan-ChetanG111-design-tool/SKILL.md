# PROMPT ORCHESTRATION SKILL

This directory contains specialized instructions and allowances for the AI model depending on the requested layout type.

## LOADING RULES

When building a prompt, the orchestrator must load the specific "allowed" file corresponding to the selected `layout-type`.

| Layout Type | File to Load | Purpose |
|-------------|--------------|---------|
| `hero` | `hero_allowed.txt` | Defines expressive techniques allowed for high-impact hero sections. |
| `landing-page` | `hero_allowed.txt` | Currently uses hero rules for the primary section. |

## FILE STRUCTURE

- **system-prompt.txt**: The base deterministic UI renderer instructions.
- **[type]_allowed.txt**: Context-specific visual permissions that are prepended to the user's prompt.
