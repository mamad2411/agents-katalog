---
name: vscode-settings-indent-override
description: Composer — apply per-key indent overrides to VS Code settings.json by piping through json-block-indent-override. Knows canonical paths and the post-promotion workflow.
category: VSCode-Configuration
---

# VS Code Settings JSON Indent Override Skill (v2) — Composer

This is the **top-level composer** in a 3-layer indent-override stack. It applies VS Code-specific
indent overrides to a `settings.json` by composing the
[json-block-indent-override](../json-block-indent-override/SKILL.md) skill, which itself composes
the [text-block-indent-override](../text-block-indent-override/SKILL.md) base primitive.

It is complementary to the [VS Code Settings Promotion skill](../vscode-settings-promotion/SKILL.md),
which handles profile → global promotion and now defaults to 2-space indentation.

***

## 1. Layer Stack

```
text-block-indent-override            ← base primitive (regex + indent rewrite, no format awareness)
  └─ json-block-indent-override       ← composer (JSON pattern, auto-quoted target keys, json.loads validation + rollback)
       └─ vscode-settings-indent-override   ← THIS skill (VS Code paths, known keys, post-promotion workflow)
```

***

## 2. Composition Rationale

| Concern | Owned by |
| :--- | :--- |
| Regex match + line re-indent | text-block-indent-override (base) |
| JSON block pattern + auto-quoting + parse validation | json-block-indent-override (middle) |
| VS Code profile paths + known keys + workflow with `vscode-settings-promotion` | **this skill** |

The composer script is a thin wrapper that adds no formatting logic — it forwards arguments to
the JSON composer. Inlining the JSON or text logic here would violate the SSOT contract.

***

## 3. Trigger Conditions

Invoke this skill when:

- A user wants a specific `settings.json` key's values indented to a non-standard depth (e.g. 6 or
  8 spaces) while the rest of the file stays at its current indent.
- After running `vscode-settings-promotion`, the promoted key's inner content needs a custom indent.
- Only specific sub-keys within a nested block need re-indenting (e.g. `approve`,
  `matchCommandLine` inside `chat.tools.terminal.autoApprove`'s per-command objects).

***

## 4. CLI Usage

Located at [`scripts/vscode-settings-indent-override.py`](./scripts/vscode-settings-indent-override.py).

```bash
python3 .agents/skills/vscode-settings-indent-override/scripts/vscode-settings-indent-override.py \
  --file    PATH_TO_SETTINGS_JSON \
  --key     TOP_LEVEL_JSON_KEY \
  --from-spaces N \
  --to-spaces   M \
  [--target-keys sub-key-1 sub-key-2 ...] \
  [--dry-run]
```

All arguments are forwarded to the JSON composer as-is. Validation, rollback, and `.bak` handling
are owned by the JSON composer.

***

## 5. Known Use Cases

### 5.1 `files.associations` — level-2 values at 6 spaces

```bash
python3 .agents/skills/vscode-settings-indent-override/scripts/vscode-settings-indent-override.py \
  --file "<user-home>/Library/Application Support/Code - Insiders/User/settings.json" \
  --key "files.associations" \
  --from-spaces 4 --to-spaces 6
```

### 5.2 `chat.tools.terminal.autoApprove` — `approve` / `matchCommandLine` at 8 spaces

```bash
python3 .agents/skills/vscode-settings-indent-override/scripts/vscode-settings-indent-override.py \
  --file "<user-home>/Library/Application Support/Code - Insiders/User/settings.json" \
  --key "chat.tools.terminal.autoApprove" \
  --from-spaces 6 --to-spaces 8 \
  --target-keys approve matchCommandLine
```

`--target-keys` is used so only the named sub-keys are re-indented — the per-command regex keys are
left at their original indent.

***

## 6. Canonical VS Code `settings.json` Paths

| Variant | Path |
| :--- | :--- |
| Insiders — default profile | `<user-home>/Library/Application Support/Code - Insiders/User/settings.json` |
| Insiders — named profile | `<user-home>/Library/Application Support/Code - Insiders/User/profiles/<profile-id>/settings.json` |
| Stable — default profile | `<user-home>/Library/Application Support/Code/User/settings.json` |
| Stable — named profile | `<user-home>/Library/Application Support/Code/User/profiles/<profile-id>/settings.json` |

If the file is symlinked to a `<private-config-repo>` SSOT repository, edits flow through the
symlink automatically — no extra step required.

***

## 7. Companion Change: `vscode-settings-promotion` 2-Space Default

During the same authoring run that produced this skill, `promote.py` in
[vscode-settings-promotion](../vscode-settings-promotion/SKILL.md) was patched:

- Default indent changed from `4` to `2` in `save_json()`.
- New `--indent N` flag for runtime override.

This guarantees the global `settings.json` is written with consistent 2-space indentation — the
base on which this skill's custom overrides operate.

***

## 8. Workflow: Promote Then Override

```bash
# Step 1: Promote from profile → global (2-space indent, post-patch default)
python3 .agents/skills/vscode-settings-promotion/scripts/promote.py \
  --profile  "<user-home>/Library/Application Support/Code - Insiders/User/profiles/<profile-id>/settings.json" \
  --global-settings "<user-home>/Library/Application Support/Code - Insiders/User/settings.json" \
  --keys "chat.tools.terminal.autoApprove"

# Step 2: Apply custom indent override via this composer
python3 .agents/skills/vscode-settings-indent-override/scripts/vscode-settings-indent-override.py \
  --file "<user-home>/Library/Application Support/Code - Insiders/User/settings.json" \
  --key "chat.tools.terminal.autoApprove" \
  --from-spaces 6 --to-spaces 8 \
  --target-keys approve matchCommandLine
```

***

## 9. Verification Protocol

1. **JSON Validity**: Performed automatically by the JSON composer (`json.loads`); rolled back on
   failure.
2. **Indent Check**: `grep '"approve"\|"matchCommandLine"' <settings.json> | sed 's/ /·/g'` — count
   leading dots to confirm the target spaces.
3. **SSOT Sync**: If `settings.json` is symlinked into `<private-config-repo>`, the symlink target
   is updated automatically.

***

## 10. Related Skills

- [text-block-indent-override](../text-block-indent-override/SKILL.md) — base primitive
- [json-block-indent-override](../json-block-indent-override/SKILL.md) — JSON-aware middle composer
- [vscode-settings-promotion](../vscode-settings-promotion/SKILL.md) — promote profile settings to
  global scope; patched to default to 2-space indent

