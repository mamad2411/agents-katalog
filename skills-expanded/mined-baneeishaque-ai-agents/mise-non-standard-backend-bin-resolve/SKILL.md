---
name: mise-non-standard-backend-bin-resolve
description: Base primitive — resolve the absolute on-disk binary path for a tool installed via a non-default
    mise backend (github:, ubi:, asdf:, http:, …) where `mise which <tool>` and `mise where <tool>@latest`
    both fail. Sibling of mise-tool-management Layer 2 (which assumes the standard backend).
category: Environment-Management
---

# mise Non-Standard Backend Bin Resolve (v1)

This is a **base primitive**. It returns ONE thing on stdout: the absolute
path to a binary that ``mise`` has installed via a non-default backend. It
is layered as a sibling of
[mise-tool-management](../mise-tool-management/SKILL.md) Layer 2 (which
covers the standard backend, where ``mise which <tool>`` Just Works).

## 1. When to Apply

Apply when ALL of the following hold:

- The user installed the tool via a non-default mise backend — the
  ``mise ls`` output shows a row with a ``backend:org/repo`` spec (e.g.,
  ``github:adwinying/php``, ``ubi:cli/cli``, ``asdf:rbenv/ruby``,
  ``http:...``).
- ``mise which <tool>`` returns: "`<tool>` is a mise bin however it is not currently active".
- ``mise where <tool>@latest`` returns: "`<tool>@latest` not installed".
- You need the absolute binary path — typically to feed it into another
  tool's configuration (an IDE setting, a launch config, a service unit
  file).

Do NOT apply when:

- The tool is installed via the standard backend — use ``mise which <tool>``
  directly (covered by
  [mise-tool-management](../mise-tool-management/SKILL.md) Layer 2).
- The tool is not installed at all — install it first.

## 2. Why `mise which` Fails for Non-Default Backends

`mise` resolves `mise which <tool>` only against tools currently **active**
in the cwd (per `mise.toml`, `mise use`, or shims). A non-default backend
install is registered in `~/.local/share/mise/installs/<backend>-<org>-<tool>/<version>/`
but is not necessarily active in any directory. The canonical resolution
path is `mise where '<full-spec>@<version>'` where the full spec INCLUDES the
backend prefix and the org/repo segment.

The shape of the install directory:

```text
~/.local/share/mise/installs/<backend>-<org>-<tool>/<version>/
                            └─ contains the <tool> binary (sometimes under bin/)
```

The ``mise ls --json`` output gives us all this directly: top-level keys
are the full specs (``"github:adwinying/php"``) and each entry carries an
``install_path`` field. The script consumes that JSON.

## 3. Operational Logic

Use the Python CLI:

- [scripts/mise_resolve_backend_bin.py](scripts/mise_resolve_backend_bin.py)

### 3.1 Reference invocations

```bash
# Simplest case — only one install matches the short name
python3 .agents/skills/mise-non-standard-backend-bin-resolve/scripts/mise_resolve_backend_bin.py \
    --tool php
# → /Users/<user>/.local/share/mise/installs/github-adwinying-php/8.5.6/php

# Disambiguating when multiple installs exist
python3 .agents/skills/mise-non-standard-backend-bin-resolve/scripts/mise_resolve_backend_bin.py \
    --tool php --backend github --version 8.5.6

# Reject not-yet-installed entries (failed downloads, etc.)
python3 .agents/skills/mise-non-standard-backend-bin-resolve/scripts/mise_resolve_backend_bin.py \
    --tool php --require-installed
```

Exit codes: ``0`` success, ``2`` ``mise ls`` failure, ``3`` no match,
``4`` ambiguous match, ``5`` entry missing ``install_path``, ``6`` binary
not under the install dir.

## 4. Tier & Craftsmanship

Tier 1 — Python 3.12+ per
[scripting-language-selection-rules.md](../../../ai-agent-rules/scripting-language-selection-rules.md)
§2. The script uses `subprocess.run([...], check=False, text=True, encoding='utf-8')`
to invoke `mise` (manual exit-code handling for layered diagnostics), and
`argparse` for CLI.

## 5. Composition by Higher-Level Skills

| Composer | Domain | Pipes into this skill via |
| :--- | :--- | :--- |
| [mise-backend-vscode-tool-bridge](../mise-backend-vscode-tool-bridge/SKILL.md) | mise non-standard backend → VS Code interpreter settings | one `mise_resolve_backend_bin.py` call to get the binary, then the result is fanned out via `vscode-multi-scope-setting-write`. |

## 6. Related Skills

- [mise-tool-management](../mise-tool-management/SKILL.md) — the parent skill covering trust,
  standard-backend selection, Python setup, and deprecation handling. This skill is a sibling
  of its Layer 2 specifically for non-default backends.
- [vscode-multi-scope-setting-write](../vscode-multi-scope-setting-write/SKILL.md) —
  the typical downstream consumer of the resolved binary path.
