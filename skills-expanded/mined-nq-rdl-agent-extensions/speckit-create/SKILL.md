---
name: speckit-create
license: CC-BY-4.0
compatibility: >-
  spec-kit extensions, manifest schema_version "1.0". Manifest rules read from
  source at v0.12.0 through v1.0.12 (2026-09-29); version-specific rules are
  marked. Not tested by running the installer.
description: >-
  Scaffold a new GitHub spec-kit extension — the extension.yml manifest,
  commands/*.md, an optional config template, and .extensionignore — valid by
  construction. Use when creating a spec-kit extension, authoring a
  speckit.<id>.<cmd> command, adding a quality-gate/integration/hook to the
  Spec-Driven-Development workflow, or when the user runs /speckit-dev:create.
  spec-kit ships no `specify extension init`, so this fills the scaffolding gap.
  Distinct from Claude Code plugins/skills and from OpenCode extensions.
argument-hint: "What extension to scaffold? (e.g. 'jira integration that creates issues after /speckit.tasks')"
user-invocable: true
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Create a spec-kit extension

> **Verify-canonical guard.** spec-kit moves fast (v0.12.0 to v1.0.12 in three
> months) and predates the model's training cutoff. Before writing any manifest, read
> `references/extension-schema.rst` AND re-check the live
> [extensions reference](https://github.github.io/spec-kit/reference/extensions.html)
> and [development guide](https://raw.githubusercontent.com/github/spec-kit/main/extensions/EXTENSION-DEVELOPMENT-GUIDE.md)
> for drift. Prefer the official `extensions/template/` over recall.

## User input

`$ARGUMENTS` = a one-line brief for the extension (what it does, which workflow
phase it hooks). If empty, ask for: the extension **id** (kebab), one-line
**purpose**, and whether it needs a **hook** (which phase) or just **commands**.

## Procedure

1. **Pick the id** — `^[a-z0-9-]+$` (lowercase, digits, hyphens; no `_`, no
   uppercase, no spaces). This is the namespace for every command
   (`speckit.<id>.<cmd>`).
2. **Copy the skeleton** from `assets/starter-extension/` and rename `my-extension`
   → your id throughout (`extension.yml`, command filenames, config name).
3. **Fill `extension.yml`** using the schema table below. Emit strict
   `X.Y.Z` versions and a `>=X.Y.Z` `speckit_version`.
4. **Author each command** as `commands/<cmd>.md` — frontmatter `description`
   (required), optional `tools`, optional `scripts.sh`/`scripts.ps`; body uses
   `$ARGUMENTS` and `{SCRIPT}`. Register it under `provides.commands` with a
   name matching `^speckit\.<id>\.<cmd>$`.
5. **Add a hook** only if the extension reacts to a workflow phase — bind under
   top-level `hooks:` (see the phase list in the schema reference). Prefer
   `optional: true` + a `prompt:` so it never runs silently.
6. **Validate** with `/speckit-dev:validate` before installing.
7. **Test locally**: `specify extension add --dev ./<dir>` in a spec-kit project,
   then `specify extension list` and invoke the command.

## Manifest schema — the load-bearing rules (source-verified)

| Field | Rule |
|---|---|
| `schema_version` | must be exactly `"1.0"` (constant compare, not a range) |
| top-level required | `schema_version`, `extension`, `requires`, `provides` |
| `extension.{id,name,version,description}` | all required |
| `extension.id` | `^[a-z0-9-]+$` |
| `extension.version` | parsed by Python `packaging` (PEP 440); emit strict `X.Y.Z` |
| `extension.effect` | optional **enum** `read-only \| read-write` |
| `extension.category` | optional free string (`docs/code/process/integration/visibility`) |
| `requires.speckit_version` | required version specifier, e.g. `">=0.12.0"` |
| provides | ≥1 of `provides.commands`/`templates`/`scripts`, top-level `hooks`, or top-level `events` (spec-kit ≥0.16.2; older releases accept a subset) |
| `provides.commands[].name` | `^speckit\.[a-z0-9-]+\.[a-z0-9-]+$` |
| `provides.commands[].file` | path **relative** to the extension root (no `..`, no absolute) |
| `provides.commands[].aliases` | free-form (not pattern-enforced) — still keep the `speckit.<id>.*` shape |
| `hooks.<event>` | one entry or a list; each: `command`, `priority` (int ≥1, default 10), `optional`, `prompt`, `description` |

**Hook events (20):** `before_`/`after_` × `specify`, `plan`, `tasks`,
`implement`, `analyze`, `checklist`, `clarify`, `constitution`, `taskstoissues`,
`converge`. The development guide lists 18; the core `converge` command also reads
`before_converge`/`after_converge`. Upstream accepts any key, so a typo installs
and never fires.

**Traps:** `tags`/`defaults` are read but **not** validated — don't rely on them
for correctness.

## Canonical sources

See `references/canonical-sources.rst`. Cite docs by name/section at point of use
(e.g. "Development Guide → Manifest Schema Reference").
