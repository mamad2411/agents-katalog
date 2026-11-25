---
name: vscode-setting-schema-discovery
description: Resolve the JSON Schema (enum values, default, description,
    per-value enumDescriptions, window-override defaults) of any VS Code
    or VS Code-family (Insiders, AntiGravity, Cursor, Codium, Windsurf)
    setting directly from the app bundle, bypassing online docs which
    frequently lag behind Insiders / forks.
category: VS Code & IDE Tooling
---

# VS Code Setting Schema Discovery Skill (v1)

This skill resolves the canonical schema of any VS Code setting by inspecting
the installed app bundle directly — independent of `code.visualstudio.com/docs`
which lags behind Insiders releases and is silent for forks (AntiGravity,
Cursor, Codium, Windsurf, etc.).

## 1. When to Apply

Apply when:

- A user asks "what does setting `X` do?" and you don't recognize it.
- A setting appears in a `settings.json` with a non-standard value and you
  need to confirm it is real (not a typo) and what its enum / default is.
- A setting was added in Insiders / a fork before the public docs were
  updated.
- You need to confirm which of two similar setting names is the real one
  (e.g., `workbench.editor.useModal` vs `workbench.editor.confirmDelete`).

Do NOT apply when:

- The setting is contributed by an **extension** — those live in each
  extension's `package.json` `contributes.configuration` block, NOT in
  `workbench.desktop.main.js`. See §4 Failure Modes.
- Official, version-matched documentation already specifies the schema.
- You only need the value the user already has (just read their
  `settings.json`).

## 2. Environment & Dependencies

| Tool | Check | Notes |
| :--- | :--- | :--- |
| `python3` | `python3 --version` | JSON parsing + brace-balance walking |
| `grep` | `grep --version` | Bundle search |
| A VS Code-family app bundle | see §3.1 | Auto-discovered or supplied via `--app` |

## 3. Operational Logic

### 3.1 Bundle Layout (per OS)

The script auto-discovers the first present location among:

| OS | Bundle path |
| :--- | :--- |
| macOS — VS Code Insiders | `/Applications/Visual Studio Code - Insiders.app` |
| macOS — VS Code Stable | `/Applications/Visual Studio Code.app` |
| macOS — AntiGravity | `/Applications/Antigravity.app` |
| macOS — Cursor | `/Applications/Cursor.app` |
| Linux — Insiders | `/usr/share/code-insiders/resources/app` |
| Linux — Stable | `/usr/share/code/resources/app` |
| Windows — Stable | `%LocalAppData%\Programs\Microsoft VS Code\resources\app` |
| Windows — Insiders | `%LocalAppData%\Programs\Microsoft VS Code Insiders\resources\app` |

For unlisted OSes / forks, pass `--app <path>` explicitly.

Inside the bundle, the two files that matter:

- `<app-dir>/out/vs/workbench/workbench.desktop.main.js` — the minified
  workbench bundle. Every setting registered by the workbench is emitted as
  an object literal keyed by `"<setting.key>":{...}`.
- `<app-dir>/out/nls.messages.json` — a flat JSON array. Localized strings
  in the JS bundle are emitted as `d(<N>,null)` placeholders; `N` is the
  array index.

### 3.2 Script

[`scripts/resolve-vscode-setting.py`](scripts/resolve-vscode-setting.py)
implements:

1. **Auto-discovery** of the bundle path (or honors `--app`).
2. **Brace-balanced extraction** of the schema object literal for the given
   key from `workbench.desktop.main.js` — regex is insufficient because the
   literal contains nested arrays/objects and string literals.
3. **NLS resolution** of every `d(<id>,null)` placeholder against
   `nls.messages.json`.
4. **Field extraction**: `type`, `enum`, `enumDescriptions`,
   `description` / `markdownDescription`, `default`, and any
   `<context>Window:{default:...}` window-override defaults (e.g.,
   `agentsWindow:{default:"all"}`).
5. **Markdown rendering** of the resolved schema as a small report.

Python 3.9+ per [`scripting-language-selection-rules.md` §2](../../../ai-agent-rules/scripting-language-selection-rules.md)
(Tier-1 default — cross-platform parity, no nested-heredoc hazard, no
shellcheck overhead, no encoding tax). Pure stdlib (`argparse`, `json`,
`pathlib`, `re`, `sys`); no third-party dependencies.

#### Invocation

```bash
python3 scripts/resolve-vscode-setting.py workbench.editor.useModal
python3 scripts/resolve-vscode-setting.py chat.mcp.autostart --app "/Applications/Visual Studio Code.app"
```

#### Sample output (real `workbench.editor.useModal`, VS Code Insiders, May 2026)

```text
# `workbench.editor.useModal`

Controls whether editors open in a modal overlay.

| Property | Value |
| :--- | :--- |
| type | `"string"` |
| default | `"some"` |
| default (agentsWindow) | `"all"` |

| Enum value | Description |
| :--- | :--- |
| `"off"` | Editors never open in a modal overlay. |
| `"some"` | Certain editors such as Settings and Keyboard Shortcuts may open in a centered modal overlay. |
| `"all"` | All editors open in a centered modal overlay. |
```

### 3.3 Manual (script-less) procedure

When the script is unavailable, the equivalent manual procedure is:

1. Capture the schema fragment with a Python one-liner that does the brace
   walk (regex alone stops at the first `}` and may truncate nested
   objects):

    ```bash
    python3 -c "import sys; src=open('<app-dir>/out/vs/workbench/workbench.desktop.main.js',encoding='utf-8',errors='replace').read(); i=src.find('\"<setting.key>\":{'); print(src[i:i+800])"
    ```

2. Note every `d(<N>,null)` placeholder in the fragment.
3. Resolve each in Python:

    ```bash
    python3 -c "import json; m=json.load(open('<app-dir>/out/nls.messages.json')); [print(i,'=>',repr(m[i])) for i in [5400,5401,5402,5403]]"
    ```

4. Compose the schema by hand.

This is exactly the workflow that originally discovered the missing
`workbench.editor.useModal` schema during the session that authored this
skill — see [Traceability](#7-traceability).

## 4. Failure Modes

| Symptom | Root cause | Remedy |
| :--- | :--- | :--- |
| `setting '<key>' not found in <bundle>` | Setting is contributed by an extension, not by core workbench | Grep each installed extension's `package.json` `contributes.configuration` block under `~/.vscode/extensions/` (or `~/.vscode-insiders/extensions/`) |
| `nls.messages.json not found` | Bundle layout differs (older VS Code, or a fork using non-standard out path) | Pass `--app` to the actual `resources/app` directory; if still missing, inspect `out/` for an alternate NLS filename (`nls.metadata.json`, `nls.keys.json`) |
| Brace-balance fails | Setting key matched inside a comment / template literal in the minified bundle | Re-grep with a more specific anchor (e.g., `"<key>":{type:`); if a fork heavily customized the registry, fall back to the manual `grep` in §3.3 |
| Resolved description is `<unresolved nls id N>` | Bundle and `nls.messages.json` are out of sync (partial install) | Reinstall the VS Code app; the two files MUST come from the same build |
| `"useModal"` typo-like setting still resolves | The fork's bundle genuinely registers it (e.g., AntiGravity-specific addition) | Confirm the bundle path the script used — the output line `_Resolved from: ..._` identifies the exact app |

## 5. Prohibited Behaviors

- **DO NOT** answer "this setting is fake / unknown" without running the
  bundle probe first. Online docs lag behind Insiders by weeks; absence
  from `code.visualstudio.com` is NOT evidence of absence from the product.
- **DO NOT** hand-edit `workbench.desktop.main.js` or `nls.messages.json`
  to test schema hypotheses — they are signed-bundle artifacts and tampering
  may break Code on next launch.
- **DO NOT** publish probe outputs that include real absolute user paths;
  apply the [Redaction & Portability Skill](../redaction-portability/SKILL.md)
  before committing artifacts.

## 6. Related Skills

- [Tool Config Schema Probe](../tool-config-schema-probe/SKILL.md) — the
  complementary skill for discovering an opaque tool's **on-disk config
  file path and shape**. This skill answers "what shape does VS Code
  accept?"; that skill answers "where does the tool write?".
- [Anti Gravity Version Checker](../antigravity-version-checker/SKILL.md) —
  AntiGravity uses the same bundle layout; this skill applies unchanged
  with `--app /Applications/Antigravity.app`.
- [VS Code Settings Promotion](../vscode-settings-promotion/SKILL.md),
  [VS Code Settings Indent Override](../vscode-settings-indent-override/SKILL.md) —
  both reason about VS Code settings; consult this skill first whenever an
  unfamiliar setting key appears.
- [Redaction & Portability](../redaction-portability/SKILL.md) — required
  before committing probe outputs that contain real paths.

## 7. Traceability

- Initial session that authored this skill: investigated
  `workbench.editor.useModal` (selected in a user's settings.json) that did
  not appear in any public VS Code docs. The bundle-probe workflow revealed
  it as a real Insiders setting with `enum: ["off","some","all"]` and a
  special `agentsWindow:{default:"all"}` override. That investigation IS
  this skill.

***

## Related Skills

- [mise-backend-vscode-tool-bridge](../mise-backend-vscode-tool-bridge/SKILL.md) — downstream
  consumer that maintains a `LANGUAGE_BUILTIN_KEYS` table of per-language built-in interpreter
  settings. Use this skill to confirm each candidate key is real and to capture its enum /
  default before adding a new language row to the bridge's table.
- [vscode-multi-scope-setting-write](../vscode-multi-scope-setting-write/SKILL.md) — pair this
  schema discovery with the multi-scope writer when you have a confirmed key and need to write
  it across the workspace-vs-folder cascade.
