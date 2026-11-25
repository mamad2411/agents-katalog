---
name: skilo
description: Use this skill when the user wants to share, install, inspect, publish, claim, or troubleshoot agent skills with Skilo links, refs, bundles, or tool-native skill directories.
---

# Skilo

Use Skilo as the sharing layer for agent skills.

## When to use this skill

Use this skill when the user wants to:

- share a local skill or all skills from a supported tool
- install a skill from a Skilo link, registry ref, GitHub source, `.skl` bundle, or local path
- publish or claim a skill in the Skilo registry
- inspect or verify a skill before installation
- understand which native skill directories a tool uses
- troubleshoot Skilo CLI, API, share-link, or install-target behavior

## Core workflow

1. Identify the source.
   Local path, `SKILL.md`, Skilo share link, `namespace/name`, GitHub source, direct URL, or `.skl` bundle.
2. Choose the operation.
   `share`, `add`, `import`, `inspect`, `publish`, or `claim`.
3. Choose explicit install targets when installing.
   Prefer tool flags over assumptions when the user names a target environment.
4. Verify before risky installation.
   Use `skilo inspect` when the source is untrusted or the user asks to review first.

## Commands

### Share

```bash
npx skilo-cli share ./my-skill
npx skilo-cli share claude
npx skilo-cli share codex -y
```

Useful options:

- `--one-time`
- `--expires 1h`
- `--uses 5`
- `--password`

### Install

```bash
npx skilo-cli add https://skilo.xyz/s/abc123 --cc
npx skilo-cli add namespace/skill-name --codex
npx skilo-cli import github:user/repo#skills/my-skill --oc
npx skilo-cli import ./skill.skl --openclaw
```

`add` and `install` are interchangeable.

## Native target flags

- `--cc` / `--claude-code` -> Claude Code
- `--codex` -> Codex
- `--cursor` -> Cursor
- `--amp` -> Amp
- `--windsurf` -> Windsurf
- `--oc` / `--opencode` -> OpenCode
- `--cline` -> Cline
- `--roo` -> Roo
- `--openclaw` -> OpenClaw

If no explicit target flag is given, default to Claude Code.

## Native install directories

- Claude Code: `~/.claude/skills/`
- Codex: `~/.agents/skills/`, `~/.codex/skills/`
- Cursor: `~/.cursor/skills/`
- Amp: `~/.config/agents/skills/`
- Windsurf: `~/.codeium/windsurf/skills/`
- OpenCode: `~/.config/opencode/skills/`
- Cline: `~/.cline/skills/`
- Roo: `~/.roo/skills/`
- OpenClaw: `~/.openclaw/skills/`

## Publishing and trust

```bash
npx skilo-cli publish
npx skilo-cli claim namespace/skill-name --token <claim-token>
npx skilo-cli inspect https://skilo.xyz/s/abc123
```

Key trust rules:

- share links can be anonymous and claimed later
- inspect untrusted skills before installation
- checksums and publisher metadata should be surfaced when available

## Troubleshooting

- If a share link resolves in the API but not on the site, check the site bundle and API base URL.
- If `npx` behaves strangely, verify the installed package version and clear stale `_npx` cache.
- If installs land in the wrong place, confirm the target flag and the tool’s native skill directory.
- If a custom domain is flaky, test the worker host directly to separate DNS from application failures.
