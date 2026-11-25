---
license: CC-BY-4.0
compatibility: >-
  spec-kit extension manifests, schema_version "1.0". Rules read from the
  ExtensionManifest source at v0.12.0, v0.14.0, v0.15.0, v0.16.2, v1.0.0 and
  v1.0.12 on 2026-09-29; other releases were not checked. The isolated installer
  oracle passed its 15-fixture matrix on v1.0.12 only, on 2026-09-29.
description: >-
  Lint a GitHub spec-kit extension (extension.yml, commands/*.md) and say, per
  finding, whether `specify extension add` would reject it or it is only a local
  convention. Use before install or publish, when debugging an install rejection,
  when asked whether the real installer accepts an extension, or when the user runs
  /speckit-dev:validate.
argument-hint: "Path to the extension directory to validate (e.g. ./my-extension)"
user-invocable: true
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Validate a spec-kit extension

> **Verify-canonical guard.** The labels below come from reading spec-kit's
> `ExtensionManifest` and install code at the tags in `compatibility:`. The
> 15-fixture installer oracle confirmed install outcomes on v1.0.12 only; it
> did not execute extension hooks. If the user's `specify version` is outside those
> tags, or a finding decides whether to block a release, re-read
> `src/specify_cli/extensions/__init__.py` at their tag (or run the oracle below)
> before calling it a rejection. Details: `references/validation-rules.rst`.

## User input

`$ARGUMENTS` = path to the extension directory (contains `extension.yml`).

## Report every finding with one of three labels

- **Rejects** — `specify extension add` stops with an error (`ValidationError`, or
  `CompatibilityError` for `speckit_version`), from the version noted, if any.
- **Warns** — upstream accepts it but prints a warning or rewrites the value.
- **Local** — upstream accepts it silently; this repository flags it because it
  breaks later or is a portability convention. Never describe a Local finding as
  an installer rejection.

| Check | Label |
|---|---|
| `extension.yml` is UTF-8 YAML whose root is a mapping | Rejects |
| `schema_version`, `extension`, `requires`, `provides` present; `schema_version` is the **string** `"1.0"` (unquoted `1.0` is a float) | Rejects |
| `extension.id`, `name`, `version`, `description` present **and strings** (unquoted `version: 1.0` fails) | Rejects (type check from v0.16.2; earlier a raw `TypeError`) |
| `id` matches `^[a-z0-9-]+$` and is not a core command name (`plan`, `tasks`, `specify`, `converge`, …) | Rejects |
| `version` parses as PEP 440 | Rejects |
| `version` is strict `X.Y.Z` (`1.0` parses) | Local |
| `effect`, if present, is `read-only` or `read-write` | Rejects |
| `category`, if present, is a non-empty string | Rejects |
| `requires.speckit_version` present, a non-empty string, a valid specifier, and satisfied by the installed CLI | Rejects |
| At least one of `provides.commands`, top-level `hooks`, top-level `events`, `provides.templates`, `provides.scripts` | Rejects (v0.12–0.14: commands or hooks only; 0.15 adds events; templates/scripts present by v0.16.2) |
| Each command has `name` and `file`; `file` is relative with no `..` | Rejects |
| Command name `speckit.<id>.<cmd>` with the middle segment equal to `extension.id` | Rejects, except `speckit.<cmd>` and `<id>.<cmd>`: **Warns** and renamed to `speckit.<id>.<cmd>` |
| Duplicate command or alias names; aliases not a list of path-safe strings | Rejects |
| Command `file` exists | Local — a missing file is skipped silently at registration |
| Command file frontmatter has `description` | Local — registration falls back to an empty description |
| Hook value is a mapping or non-empty list; each entry has `command`; `priority` is an int ≥ 1 | Rejects |
| Hook event name is one of the 20 core events: `before_`/`after_` × `specify`, `plan`, `tasks`, `implement`, `analyze`, `checklist`, `clarify`, `constitution`, `taskstoissues`, `converge` | Local — any key is accepted; an unknown one never fires. `before_converge`/`after_converge` are real (read by the core `converge` command) though the development guide lists only 18 |
| Hook `command` names a command the extension provides | Local |
| `provides.config[].template` files exist | Local |

End with a compact table (check → label → PASS/FAIL → offending value), a verdict
that counts **Rejects** separately from **Warns** and **Local**, and the exact fixes.

## Upstream-installer oracle (optional)

The table above is not proof that the installer accepts an extension. To confirm,
run the pinned installer in a throwaway project — see
`references/installer-oracle.rst` for the commands and fixtures. Requirements:

- **Version:** `specify-cli` 1.0.12 from tag `v1.0.12` (or the user's own pinned
  tag, recorded in the report).
- **Isolation:** a new temporary directory holding the project, `HOME`,
  `XDG_CONFIG_HOME`, `XDG_CACHE_HOME`, `XDG_DATA_HOME`, and the uv cache/tool dirs;
  an emptied environment (`env -i`), so no tokens or credentials are visible.
- **Scope:** never install into, modify, or `specify init` the user's project; use a
  copy of the extension. No `catalog add`, no publishing, no pushes.
- **Network and scripts:** network only to fetch the pinned installer and its
  Python dependencies; run only `specify version`, `specify init` in the temporary
  project, and `specify extension add --dev`. Do not run extension scripts or hooks.
- **Authorization:** fetching and executing the upstream installer needs the
  user's explicit approval in this session; a request to "validate" alone is not
  approval.
- **Cleanup:** delete the temporary directory and confirm it is gone.

If approval, network, a Python ≥3.11 interpreter, or isolation is unavailable,
report **"installer oracle: not run"** with the reason, keep the labels above as
source-derived, and do not claim the installer accepted or rejected anything.

## Canonical sources

See `references/validation-rules.rst` and `references/canonical-sources.rst`.
