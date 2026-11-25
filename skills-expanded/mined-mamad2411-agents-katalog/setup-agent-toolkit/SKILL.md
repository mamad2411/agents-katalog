---
name: setup-agent-toolkit
description: >-
  Safely inspect, preview, install, update, or repair Agent Toolkit skills,
  workers, and optional AGENTS.md or CLAUDE.md routing policy. Use when a user
  asks an agent to set up Agent Toolkit, Codex Maestro, Claude Maestro, global
  agent defaults, or project-scoped orchestration instructions. Default to
  read-only inspection and dry-run previews; protect existing developer
  configuration with conflict detection, explicit approval, backups, atomic
  writes, validation, and rollback guidance.
---

# Set up Agent Toolkit safely

Treat developer configuration as user-owned data. Inspect first, preview every
change, and mutate only the requested platform and scope.

## Safety contract

1. Start read-only. Identify the checkout, platform (`codex` or `claude`),
   scope (`global` or `project`), home directories, existing installations,
   instruction files, symlinks, and uncommitted repository changes.
2. Never print secrets or read unrelated credentials, environment files, or
   tokens. Do not edit `config.toml`, model settings, MCP settings, hooks,
   permissions, shell profiles, or environment variables.
3. Do not use an installer's `--force` option, delete an installation, replace
   a symlink, or overwrite an existing config unless the user approves the
   exact preview after conflicts and backups are explained.
4. Stop on malformed managed markers, unexpected file types, unreadable text,
   ambiguous homes, or content that cannot be preserved byte-for-byte outside
   the managed block. Report evidence instead of guessing.
5. Keep all edits inside Agent Toolkit destinations and the single requested
   instruction file. Preserve unrelated content and file permissions.

## Inspect and plan

Locate this repository and confirm the requested source exists:

- Codex skill: `plugins/codex/codex-maestro/skills/codex-maestro/`
- Codex implementation worker:
  `plugins/codex/codex-maestro/skills/codex-maestro/references/implementation-worker.toml`
- Codex exploration worker:
  `plugins/codex/codex-maestro/skills/codex-maestro/references/exploration-worker.toml`
- Claude skill: `plugins/claude/maestro/skills/maestro/`
- Claude agents: `plugins/claude/maestro/agents/`

Resolve destinations without changing them:

| Platform | Global skill | Project skill | Global policy | Project policy |
| --- | --- | --- | --- | --- |
| Codex | `~/.agents/skills/codex-maestro/` | `<repo>/.agents/skills/codex-maestro/` | `~/.codex/AGENTS.md` | `<repo>/AGENTS.md` |
| Claude | `~/.claude/skills/maestro/` | `<repo>/.claude/skills/maestro/` | `~/.claude/CLAUDE.md` | `<repo>/CLAUDE.md` |

Custom-agent destinations are `$CODEX_HOME/agents/` or `<repo>/.codex/agents/`
for Codex, and `~/.claude/agents/` or `<repo>/.claude/agents/` for Claude.
Inspect every individual destination before copying it. For Codex upgrades,
also report a legacy `luna-worker.toml` if present; do not delete or overwrite it
without a separate preview and approval.

For Codex, resolve `$CODEX_HOME` before falling back to `~/.codex`. On Windows
and WSL, treat each environment as a separate installation. Do not cross-write
between their homes.

If a destination already exists, compare it with the source. Report whether it
is identical, modified, older, or a symlink. An existing modified destination
is a conflict, not an invitation to replace it.

## Preview policy changes

Use the bundled deterministic editor. It writes nothing unless `--apply` is
present:

```text
python <this-skill>/scripts/configure_policy.py \
  --platform codex|claude \
  --scope global|project \
  [--project-root <repository>]
```

Show the complete target path and unified diff to the user. Explain any
existing managed block that will be updated. Request explicit approval before
running the same command with `--apply`. Approval to "set up the toolkit" does
not waive this preview checkpoint when an existing instruction file will be
modified.

The editor only creates or updates a marked Agent Toolkit block. It refuses
symlink targets and malformed or duplicate markers, creates a timestamped
backup of an existing file, preserves content outside the block, and replaces
the file atomically.

## Install after approval

For a new global Codex installation, run the existing installer without
`--force`:

```text
python plugins/codex/codex-maestro/skills/codex-maestro/scripts/install.py
```

Use `--link` only when the user wants a development checkout to remain the
live source. The installer installs the skill and both required Luna/max
worker definitions. Existing agent definitions remain user-owned; refuse to
replace them until the user approves the exact diff and verified backups. For
project scope, copy the requested skill directory to `.agents/skills/` and both
worker definitions to `.codex/agents/`. Use `--skill-only` or `--agent-only`
only when the user explicitly requests a partial lifecycle operation.

For Claude, copy or link `plugins/claude/maestro/skills/maestro/` to the selected
skills directory and copy the three Markdown definitions from
`plugins/claude/maestro/agents/` to the selected agents directory. Refuse replacement
when any destination exists. If the user approves replacement after reviewing
a diff, create a timestamped sibling backup first and verify it before changing
the destination. Recommend Claude Code 2.1.212 or later for the complete
subagent/worktree behavior described by the skill; model availability remains
provider- and organization-dependent.

If the user wants to reuse this setup workflow later, copy or link this
`setup-agent-toolkit` directory to `~/.agents/skills/setup-agent-toolkit/` only
when that destination is absent. If it exists, apply the same inspect, compare,
preview, approve, and backup rules; never replace it implicitly.

Never install both global and project copies unless requested. Never configure
both platforms merely because both sources exist.

## Validate and report

After applying changes:

1. Verify every destination exists and matches the intended source or approved
   managed policy block.
2. Parse Codex TOML and Claude YAML frontmatter, and confirm implementation
   workers cannot spawn nested agents while exploration workers are read-only.
3. Re-run the policy editor without `--apply`; expect no diff.
4. Confirm backups exist when pre-existing files were changed.
5. Tell the user to start a new agent task so skill discovery and base
   instructions reload.
6. Report paths changed, paths intentionally untouched, validation results,
   backup paths, and the exact rollback operation. Do not claim a model was
   selected or changed; configuration cannot switch an already-running root
   model.

To roll back an instruction file, restore the reported backup only after
previewing the reverse diff. If the file was newly created, remove only the
managed block or file after confirming no other content was added.
