---
name: vscode-multi-scope-setting-write
description: Base primitive — idempotently write a VS Code setting into one or more scope files (folder
    .vscode/settings.json and/or workspace .code-workspace) so the configuration behaves identically
    whether VS Code opens the directory as a folder or as a multi-root workspace.
category: VS Code & IDE Tooling
---

# VS Code Multi-Scope Setting Write (v1)

This is a **base primitive**. It mutates the JSON of one or more VS Code scope
files in one idempotent call. It is the SSOT for the scope cascade — composer
skills (e.g., [mise-backend-vscode-tool-bridge](../mise-backend-vscode-tool-bridge/SKILL.md))
delegate scope-write mechanics here.

## 1. When to Apply

Apply when ANY of:

- The user is running VS Code via a `.code-workspace` file. **Workspace
  settings override folder settings**; writing only to one scope creates a
  silent inconsistency between "open as folder" and "open as workspace" modes.
- A setting must be present in both a per-repo `.vscode/settings.json` AND a
  shared workspace file (e.g., a centralized `<private-config-repo>` repo
  that contains a multi-root `.code-workspace`).
- Migrating settings from one scope into another while preserving the
  cascade semantics.

Do NOT apply when:

- You only need to write user-scope settings — that's
  [vscode-settings-promotion](../vscode-settings-promotion/SKILL.md) (which
  also handles `workbench.settings.applyToAllProfiles` enforcement).
- You need to discover what setting key/value is valid — that's
  [vscode-setting-schema-discovery](../vscode-setting-schema-discovery/SKILL.md).

## 2. Scope Cascade (the rule this skill enforces)

VS Code resolves a setting from highest to lowest precedence:

```text
1. Workspace File (.code-workspace, "settings" block)   ← HIGHEST
2. Folder Settings (<folder>/.vscode/settings.json)
3. User Settings (~/Library/.../Code/User/settings.json on macOS, etc.)
4. Default Settings (built-in)                          ← LOWEST
```

Consequence: if a workspace is open, scope 2 is INERT for any key set at
scope 1. The operator must write to BOTH scopes whenever the operator wants
the setting to persist regardless of how the folder is opened later.

## 3. Operational Logic

Use the Python CLI under `scripts/`:

- [scripts/write_vscode_setting.py](scripts/write_vscode_setting.py) — the
  core writer. Idempotent; supports string / bool / int / float / json
  value coercion; auto-detects whether each `--scope` is a folder
  `.vscode/settings.json` or a `*.code-workspace` and writes to the correct
  nesting level (top-level vs `"settings"` block).
- [scripts/detect_vscode_scopes.py](scripts/detect_vscode_scopes.py) —
  helper for enumerating plausible scope paths given a folder root and an
  optional `--workspace` hint.

### 3.1 Single-setting, multi-scope invocation (reference)

```bash
python3 .agents/skills/vscode-multi-scope-setting-write/scripts/write_vscode_setting.py \
    --key php.validate.executablePath \
    --value "<toolbase>/php" \
    --value-type string \
    --scope "<workspace-root>/<php-repo>/.vscode/settings.json" \
    --scope "<workspace-root>/<private-config-repo>/<workspaces>/<project>.code-workspace"
```

Re-running the same command produces no diff on either scope (idempotency
contract).

## 4. Tier & Craftsmanship

Scripts are **Tier 1 — Python 3.12+** per
[`scripting-language-selection-rules.md`](../../../ai-agent-rules/scripting-language-selection-rules.md)
§2. The Tier-2 PowerShell craftsmanship rules in
[`skill-factory/SKILL.md`](../skill-factory/SKILL.md) §2.2.1 items 2–8 do
NOT apply.

Python conventions followed (per Scripting Language Selection Rules §2.3):

- Byte-safe I/O via `Path.read_bytes` / `Path.write_bytes` + explicit UTF-8.
- `argparse` for CLI.
- Module docstring carries the SSOT citation and tier justification.
- `subprocess` is unused here (pure file-mutation primitive).

## 5. Composition by Higher-Level Skills

| Composer | Domain | Pipes into this skill via |
| :--- | :--- | :--- |
| [mise-backend-vscode-tool-bridge](../mise-backend-vscode-tool-bridge/SKILL.md) | mise non-standard backend → IDE interpreter wiring | one `write_vscode_setting.py` invocation per (key × scope) pair, after resolving the binary via `mise-non-standard-backend-bin-resolve`. |

When a new composer is added, append its row here so the dependency graph
stays bidirectionally discoverable (per
[ai-rule-standardization-rules §Layered Composition Mandate](../../../ai-agent-rules/ai-rule-standardization-rules.md)).

## 6. Related Skills

- [vscode-settings-promotion](../vscode-settings-promotion/SKILL.md) — for promoting
  profile-specific settings to user scope with `applyToAllProfiles` enforcement.
- [vscode-setting-schema-discovery](../vscode-setting-schema-discovery/SKILL.md) — for
  confirming a setting name and its valid values before writing.
- [skill-factory](../skill-factory/SKILL.md) §2.0 — Layering Decision rationale that
  motivated splitting this primitive out from the composer.
