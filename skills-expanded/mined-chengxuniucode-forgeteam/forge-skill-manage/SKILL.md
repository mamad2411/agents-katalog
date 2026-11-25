---
name: forge-skill-manage
description: Use this skill when the user wants to create, find, install, publish, delete, or update an Agent skill through Forge SkillHub. It coordinates the end-to-end Forge skill lifecycle and delegates registry operations to the `forge-skillhub` skill and its `skillhub` CLI.
---

# Forge Skill Management

Use this skill to manage a skill from creation through Forge-skillHub
distribution. Registry actions must use `forge-skillhub` and the official
`skillhub` CLI; do not use external registry URLs.

## Preconditions

Forge-skillHub needs a valid API token for publishing and remote deletion.
Authenticate through the CLI, which stores the token outside the project:

```bash
skillhub login --token <forge-api-token> --registry <forge-skillhub-url>
skillhub whoami
```

The CLI uses the default local Forge-skillHub service at
`http://127.0.0.1:8080`; `--registry` or `SKILLHUB_REGISTRY` selects another
Forge deployment. Token precedence is `--token`, `SKILLHUB_TOKEN`, then
`~/.skillhub/credentials.json`.

## Create and publish a skill

1. Gather the purpose, trigger conditions, expected output, target Agent, and
   intended visibility. Use `skill-creator` to author or improve the skill.
2. Create the skill in the target Agent's project directory. For Codex use
   `.codex/skills/<skill-name>/`; for Claude Code use
   `.claude/skills/<skill-name>/`.
3. Ensure `SKILL.md` has `name` and `description` frontmatter and test the
   skill locally.
4. Ask whether the user wants to publish it. Publishing changes the shared
   registry, so do not publish without that intent.
5. Delegate to `forge-skillhub` and validate, then upload:

```bash
skillhub publish .codex/skills/<skill-name> --namespace <namespace> --dry-run
skillhub publish .codex/skills/<skill-name> --namespace <namespace> --visibility namespace-only
```

Report the returned coordinate and version, for example
`forge-team/json-helper@1.0.0`, and give the corresponding install command.

## Search and install

1. Delegate to `forge-skillhub` to search the Forge registry:

```bash
skillhub search "<keywords>" --limit 20 --json
```

2. Present relevant results using their `namespace/slug`, version, and
   summary. Let the user choose when more than one suitable result exists.
3. Install the chosen skill into the requested Agent scope. Default to the
   current project's Agent directory:

```bash
skillhub install <namespace>/<slug> --scope project --agent codex
skillhub list --agent codex
```

Use `--version <version>` for a pinned release. The CLI writes installation
metadata and inventory automatically; do not create lock files manually.

## Update and delete

For an installed skill, Forge uses a release-based update flow: publish a new
version to Forge-skillHub, then replace the local installation explicitly.

```bash
# Publish the new release
skillhub publish .codex/skills/<skill-name> --namespace <namespace>

# Download the selected release from Forge-skillHub and replace the local copy
skillhub install <namespace>/<skill-name> --version <version> --scope project --agent codex --force

# Remove only the local Codex copy
skillhub remove <namespace>/<skill-name> --agent codex

# Delete the remote Forge-skillHub skill only with explicit approval
skillhub remove <namespace>/<skill-name> --remote --hard

# Update the CLI executable, not installed skills
skillhub update
```

`skillhub update` updates `@forge-team/skillhub`; it is not a remote skill
version update. A remote delete is destructive and requires ownership. Confirm
the coordinate with the user before passing `--remote --hard`.

## Error handling and completion

- Authentication failure: run `skillhub login` and verify with `skillhub whoami`.
- Access denied: report the required namespace access or ownership; do not
  bypass permissions.
- Service connection failure: check `SKILLHUB_REGISTRY` or use the correct
  Forge-skillHub `--registry` address.
- Existing installation: inspect `skillhub list`, then use `--force` only for
  an intentional replacement.
- Stale local inventory: run `skillhub doctor`.

Complete the workflow by reporting the registry coordinate, published or
installed version, target directory, and the next command the user is likely to
need. Use `--json` when an automated caller needs structured output.
