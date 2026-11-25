---
name: mise-backend-vscode-tool-bridge
description: Composer — wires a tool installed via a non-default mise backend (github:, ubi:, asdf:, http:, …)
    into the BUILT-IN VS Code interpreter settings for the language, across one or more scope files
    (folder .vscode/settings.json AND/OR workspace .code-workspace) — bypassing the Mise VS Code
    extension which auto-detects only the standard backend.
category: VS Code & IDE Tooling
---

# mise Backend → VS Code Tool Bridge (v1)

This is a **composer skill**. It does NOT reimplement any primitive — it
orchestrates two base skills:

```text
mise-backend-vscode-tool-bridge   (this composer)
├── mise-non-standard-backend-bin-resolve   (binary discovery)
└── vscode-multi-scope-setting-write        (settings mutation, scope cascade)
```

## 1. When to Apply

Apply when ALL of the following hold:

- A tool was installed via a non-default ``mise`` backend (see
  [mise-non-standard-backend-bin-resolve §1](../mise-non-standard-backend-bin-resolve/SKILL.md#1-when-to-apply)).
- The Mise VS Code extension is installed but the relevant per-language
  VS Code settings (e.g., ``php.validate.executablePath``) are blank or
  point to the wrong interpreter — typical symptom: the extension's
  auto-detection logic only recognizes the standard backend and silently
  ignores the non-default one.
- You want the configuration to behave identically whether the user opens
  the folder directly or via a ``.code-workspace`` (see
  [vscode-multi-scope-setting-write §2](../vscode-multi-scope-setting-write/SKILL.md#2-scope-cascade-the-rule-this-skill-enforces)).

Do NOT apply when:

- The tool is on the standard mise backend — use the Mise VS Code
  extension's auto-detection directly.
- Wiring third-party language extensions whose settings keys are not in
  the built-in interpreter set (e.g., Intelephense's
  ``intelephense.environment.phpPath``). The current composer only writes
  the **built-in** VS Code interpreter keys; for third-party extensions,
  pass each key explicitly via ``--extra-key`` (the underlying base skill
  supports any key) OR fork this composer with an extended table.

## 2. Architecture

The composer is a thin Python orchestrator that shells out to both base
scripts via ``subprocess.run`` using paths anchored on its own
``__file__`` (per
[ai-rule-standardization-rules §Portable Script Path Mandate](../../../ai-agent-rules/ai-rule-standardization-rules.md)).
This loose coupling means each base skill can be tested, audited, and
ported independently — the composer holds NO duplicated logic.

### 2.1 Built-in language → setting-key table

The composer ships a static table mapping each language to its **built-in**
VS Code interpreter settings:

| Language | Built-in setting keys |
| :--- | :--- |
| `php` | `php.validate.executablePath`, `php.debug.executablePath` |

Additional languages are easy to add — extend the
``LANGUAGE_BUILTIN_KEYS`` dict in
[scripts/bridge_mise_tool_to_vscode.py](scripts/bridge_mise_tool_to_vscode.py)
after confirming the keys via
[vscode-setting-schema-discovery](../vscode-setting-schema-discovery/SKILL.md).

## 3. Operational Logic

Use the Python CLI:

- [scripts/bridge_mise_tool_to_vscode.py](scripts/bridge_mise_tool_to_vscode.py)

### 3.1 Reference invocation (PHP, dual scope)

```bash
python3 .agents/skills/mise-backend-vscode-tool-bridge/scripts/bridge_mise_tool_to_vscode.py \
    --language php --backend github --version 8.5.6 \
    --scope "<workspace-root>/<php-repo>/.vscode/settings.json" \
    --scope "<workspace-root>/<private-config-repo>/.../<project>.code-workspace"
```

The composer prints the resolved binary path once, then writes each
``(key × scope)`` pair through the writer. Re-running is a no-op (every
write reports ``ALREADY-SET``) — the idempotency contract is preserved
end-to-end.

### 3.2 Adding extra keys for third-party extensions

```bash
python3 .agents/skills/mise-backend-vscode-tool-bridge/scripts/bridge_mise_tool_to_vscode.py \
    --language php --backend github --version 8.5.6 \
    --extra-key intelephense.environment.phpPath \
    --extra-key php-cs-fixer.phpPath \
    --scope "<workspace-root>/<php-repo>/.vscode/settings.json" \
    --scope "<workspace-root>/<private-config-repo>/.../<project>.code-workspace"
```

⚠ Confirm each extra key actually wants a PHP interpreter (not the tool's
own binary like `vendor/bin/phpstan`) BEFORE passing it. See
[vscode-setting-schema-discovery](../vscode-setting-schema-discovery/SKILL.md)
to verify.

## 4. Tier & Craftsmanship

Tier 1 — Python 3.12+ per
[scripting-language-selection-rules.md](../../../ai-agent-rules/scripting-language-selection-rules.md)
§2. Uses ``argparse``, byte-safe I/O via the writer base script,
``subprocess.run([sys.executable, ...], check=False, text=True, encoding='utf-8')``,
and `__file__`-anchored sibling-script discovery.

## 5. Composition Rationale

This composer was extracted from a live session in which the operator
manually wired ``github:adwinying/php@8.5.6`` into both a Flutter
sibling-repo workspace's `.code-workspace` and an unrelated PHP repo's
`.vscode/settings.json`. The session exposed two reusable primitives — mise
non-default-backend resolution and multi-scope VS Code setting writing —
that were split per
[skill-factory §2.0 Layering Decision](../skill-factory/SKILL.md#20-layering-decision-base-vs-composer).

## 6. Related Skills

- [mise-non-standard-backend-bin-resolve](../mise-non-standard-backend-bin-resolve/SKILL.md) (base, binary discovery).
- [vscode-multi-scope-setting-write](../vscode-multi-scope-setting-write/SKILL.md) (base, scope cascade writing).
- [mise-tool-management](../mise-tool-management/SKILL.md) (parent skill covering trust + standard-backend selection).
- [vscode-setting-schema-discovery](../vscode-setting-schema-discovery/SKILL.md) (consult
  before adding a new language row to the LANGUAGE_BUILTIN_KEYS table).
- [vscode-settings-promotion](../vscode-settings-promotion/SKILL.md) (sibling, covers user-scope + applyToAllProfiles).
