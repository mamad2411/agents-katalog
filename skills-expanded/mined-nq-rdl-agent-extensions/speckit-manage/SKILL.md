---
name: speckit-manage
license: CC-BY-4.0
compatibility: >-
  spec-kit `specify extension` CLI; semantics read from v1.0.12 source
  (2026-09-28/29). Flags change between releases: the installed `--help` wins.
description: >-
  Install, list, enable/disable, update, and configure GitHub spec-kit extensions
  and their catalog stack. Use for `specify extension` or
  `specify extension catalog` commands, wiring a team catalog, installing spec-kit
  itself, or editing .specify/extension-catalogs.yml / extensions.yml. Linting an
  extension or testing whether it installs → speckit-dev:validate; releasing one →
  speckit-dev:publish.
argument-hint: "What to manage? (e.g. 'install jira from our team catalog', 'add an internal catalog')"
user-invocable: true
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Manage spec-kit extensions

> **Verify-canonical guard.** CLI semantics below were re-verified against
> v1.0.12 source (2026-09-28); flags drift, so `--help` is authoritative. Confirm
> against `references/cli-and-catalogs.rst` and the live
> [extensions reference](https://github.github.io/spec-kit/reference/extensions.html)
> and [user guide](https://raw.githubusercontent.com/github/spec-kit/main/extensions/EXTENSION-USER-GUIDE.md).

## Install spec-kit

PyPI `specify-cli` and a pinned GitHub tag are both official install routes
(uv, pipx, or pip). Follow the
[installation guide](https://github.github.io/spec-kit/installation.html);
`specify version` confirms the CLI is on `PATH`.

## CLI surface

Run `specify extension --help`, `specify extension <cmd> --help`, and
`specify extension catalog --help` for the current commands and flags.
Non-obvious semantics:

- `add <path> --dev` — `--dev` is a boolean; the positional is the local
  directory. `--from <url>` installs from a URL, bypassing catalog lookup. To
  test whether an extension would install, don't install it into the user's
  project: use the isolated installer oracle in `/speckit-dev:validate`.
- Priority (`add --priority`, `set-priority <name> <N>`, `catalog add --priority`)
  — lower number wins; default 10.
- `list` shows installed extensions, enabled or disabled; browse catalogs with
  `search`. `list --json` emits installed extensions for scripting.
- `update` with no name updates every installed extension.
- `catalog add <https-url> --name <n>` writes the project
  `.specify/extension-catalogs.yml`. It is **discovery-only by default**; pass
  `--install-allowed` only for a catalog you own and vet. The built-in community
  catalog is discovery-only: vet an entry, then `add <name> --from <url>`.

## Catalog stack (precedence)

`SPECKIT_CATALOG_URL` env (replaces the whole stack with one URL) → project
`.specify/extension-catalogs.yml` (wins when it lists at least one catalog; an empty
list falls back to the defaults) → user `~/.specify/extension-catalogs.yml` →
built-in defaults (official + community). Lower `priority` number wins on id
conflicts. See
`assets/extension-catalogs.yml` for wiring a team catalog with
`install_allowed: true`.

## Config precedence (per extension)

extension defaults → `<ext>-config.yml` → `<ext>-config.local.yml` →
`SPECKIT_<EXT>_*` env.

## Commit vs gitignore

Commit `.specify/extensions.yml` + `.specify/extensions/*/<ext>-config.yml`.
Gitignore `.specify/extensions/.cache/`, `.specify/extensions/.backup/`,
`.specify/extensions/*/*.local.yml`, and `.specify/extensions/.registry`
(installation state).

## Canonical sources

See `references/cli-and-catalogs.rst` and `references/canonical-sources.rst`.
