---
name: forge-skillhub
description: Use this skill whenever the user needs to discover, install, publish, remove, or update Agent skills through Forge SkillHub, or mentions the `skillhub` CLI, Forge-skillHub, a skill registry, or sharing a skill with a team. Use it for the complete Forge skill lifecycle rather than external registries.
---

# Forge SkillHub

Forge SkillHub is ForgeTeam's private skill registry. Use the official
`@forge-team/skillhub` CLI (`skillhub`) for all registry actions. Do not use
an external registry endpoint.

## Registry, authentication, and coordinates

The default Forge-skillHub registry is `http://127.0.0.1:8080`. Resolve a
different deployment in this order:

1. `--registry <url>` on the command
2. `SKILLHUB_REGISTRY`
3. `~/.skillhub/config.json`
4. The default local address

Authenticate once before publishing or remotely deleting:

```bash
skillhub login --token <forge-api-token> --registry <forge-skillhub-url>
skillhub whoami
```

Tokens resolve in this order: `--token`, `SKILLHUB_TOKEN`, then the encrypted
local registry entry in `~/.skillhub/credentials.json`. Prefer `skillhub login`
or `SKILLHUB_TOKEN`; never put a token in project files or user-facing output.

Use `namespace/slug` as a skill coordinate. A bare slug defaults to the
`global` namespace; `@namespace/slug` and `namespace--slug` are also accepted.

## Forge-skillHub API routes

The CLI owns these calls. This table is the canonical address mapping when an
integration must call Forge-skillHub directly.

| Lifecycle action | Forge-skillHub route |
| --- | --- |
| Search | `GET /api/cli/v1/skills/search?q=<query>&limit=<n>` |
| Resolve version | `GET /api/cli/v1/skills/{namespace}/{slug}/resolve` |
| Download | `GET /api/cli/v1/skills/{namespace}/{slug}/versions/{version}/download` |
| Upload / publish | `POST /api/cli/v1/skills/{namespace}/publish` |
| Pre-publish validation | `POST /api/cli/v1/skills/{namespace}/publish/validate` |
| Remote delete | `DELETE /api/cli/v1/skills/{namespace}/{slug}` |

All authenticated calls use `Authorization: Bearer <forge-api-token>`.

## Discover and install

Search Forge-skillHub first, then install the selected coordinate into the
right Agent scope. Prefer project scope unless the user explicitly asks for a
personal installation.

```bash
skillhub search "pdf processing" --limit 20 --json
skillhub install global/pdf-processor --scope project --agent codex
skillhub list --agent codex
```

`--agent codex --scope project` installs into `.codex/skills/`; Claude Code
uses `.claude/skills/`. Use `--version <version>` for a pinned release and
`--force` only when replacing an existing installation. The CLI records each
install in the skill's `.skillhub/metadata.json` and in
`~/.skillhub/inventory.json`.

If no suitable Forge skill exists, tell the user and continue with the task or
create a new skill when requested; do not silently fall back to another
registry.

## Upload and publish

A publishable package needs a `SKILL.md` at its root with valid `name` and
`description` frontmatter. Forge SkillHub accepts either a skill directory
(which the CLI packages) or an existing ZIP archive.

```bash
# Check the package without changing the registry
skillhub publish ./my-skill --namespace forge-team --dry-run

# Upload a new version to Forge-skillHub
skillhub publish ./my-skill --namespace forge-team --visibility namespace-only
```

Visibility is `public`, `namespace-only`, or `private`; default to the least
permissive visibility that meets the user's sharing intent. On success, report
the returned `namespace/slug@version` and install command.

## Download, delete, and update

```bash
# Download and install a release from Forge-skillHub
skillhub install forge-team/my-skill --scope project --agent codex

# Remove one local Agent installation
skillhub remove forge-team/my-skill --agent codex

# Delete the registry skill; requires publish ownership and explicit intent
skillhub remove forge-team/my-skill --remote --hard

# Replace a local install with a newly published release
skillhub install forge-team/my-skill --version 1.2.0 --scope project --agent codex --force

# Update the Forge CLI itself
skillhub update
```

There is no separate remote "update skill" API: publish a new version, then
install that version with `--force` for each target. `skillhub update` updates
the CLI package (`@forge-team/skillhub`), not installed skills. Remote deletion
is destructive; confirm the coordinate and use `--hard` only after the user
has explicitly authorized it. For non-interactive commands, `--hard` is
required.

## Failure handling

- `401`: run `skillhub login --token <forge-api-token>` or set
  `SKILLHUB_TOKEN`, then verify with `skillhub whoami`.
- `403`: the current user lacks namespace access or ownership; do not retry
  with another user's token.
- Registry unreachable: verify `SKILLHUB_REGISTRY` or pass the correct
  `--registry <forge-skillhub-url>`.
- Existing local skill: verify its source with `skillhub list`, then use
  `--force` only if replacing it is intended.
- Inventory out of sync: run `skillhub doctor` to rebuild the local inventory.

Use `--json` when another program needs structured output. Preserve request IDs
from Forge-skillHub error messages when reporting an issue to registry owners.
