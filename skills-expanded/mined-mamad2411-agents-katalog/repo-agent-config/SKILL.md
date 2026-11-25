---
name: repo-agent-config
description: Build or maintain shared agent configuration for a repository. Use when adding or reviewing AGENTS.md, CLAUDE.md, GEMINI.md, .agents/skills, .codex, .gemini, .claude, MCP files, hooks, or other per-repository configuration for Claude Code, Codex, Gemini CLI, and Antigravity.
---

# Build Repo Agent Config

Use this skill to set up agent config inside a normal application, library, or
tooling repository. Keep one canonical source for shared repo instructions, and
use `.agents/skills` as the canonical place for repo-local skills. Add
tool-specific files only when a tool needs a native discovery path or actual
tool-specific behavior. For dotfiles or agent-config repos that publish
user-global skills, keep that user-global source separate from repo-local
workspace skills; do not symlink it into `.agents/skills` unless duplicate
workspace loading is intentional.

## Default Layout

Start with this structure:

```text
AGENTS.md                  # Canonical repo instructions.
.agents/
  skills/<skill>/SKILL.md  # Canonical repo-scoped Agent Skills.
```

Add these only when needed:

| Path | Add when | Notes |
|---|---|---|
| `CLAUDE.md` | Claude users need native repo instructions | Prefer symlink or a tiny pointer to `AGENTS.md`; do not duplicate content. |
| `GEMINI.md` | Gemini users cannot rely on `context.fileName = ["AGENTS.md", "GEMINI.md"]` | Prefer symlink or pointer. Avoid if Antigravity would load both `AGENTS.md` and `GEMINI.md`. |
| `.codex/config.toml` | The repo needs Codex-specific settings, MCP, sandbox, fallback instruction filenames, or project hooks | Keep personal model/provider choices out of shared repo config. |
| `.codex/hooks.json` or `.codex/rules/*.rules` | The repo needs Codex lifecycle enforcement or exec-policy rules | Hooks/rules load only for trusted Codex projects. Prefer repo-relative scripts. |
| `.gemini/settings.json` | The repo needs Gemini-specific settings, sandbox profile, context filenames, or MCP config | Keep auth, secrets, and personal UI prefs out. |
| `.gemini/sandbox.Dockerfile` or `.gemini/sandbox-*.sb` | The repo needs Gemini sandbox customization | Mention the command/env required to use it in `AGENTS.md`. |
| `.agents/mcp_config.json` | Antigravity workspace MCP servers are needed | Keep secrets in environment variables, not committed JSON. |
| `.agents/rules/*.md` | Antigravity workspace rules need activation metadata or behavior that should not always load | Keep durable cross-agent repo rules in `AGENTS.md`; use Antigravity rules for tool-specific activation. |
| `.claude/settings.local.json` | A developer needs local Claude permissions or experiments | Usually do not commit; prefer user-local state. |

## Instruction Files

- Put repo-wide durable instructions in root `AGENTS.md`.
- Put subtree-specific instructions in nested `AGENTS.md` only when the subtree
  really differs.
- Use `CLAUDE.md` and `GEMINI.md` as adapters, not second sources of truth.
- If symlinks are acceptable in the repo, use `CLAUDE.md -> AGENTS.md` and,
  only when necessary, `GEMINI.md -> AGENTS.md`.
- If symlinks are undesirable for a cross-platform team, make adapter files
  short pointers that say the canonical instructions are in `AGENTS.md`.

Avoid `.agents/AGENTS.md` as an instruction adapter. Current mainstream
repo-local uses of `.agents/` include skills, Antigravity workspace rules, and
Antigravity workspace MCP config; root `AGENTS.md` is the clearer canonical
instruction path.

## Migration Workflow

When converting an existing repo, do not start by editing prose. First inventory
the actual adapter/config state, then migrate to the target layout:

1. Inventory repo-local agent files and directories: `AGENTS.md`, `CLAUDE.md`,
   `GEMINI.md`, `.agents/`, `.claude/`, `.codex/`, and `.gemini/`. Use
   `ls -la`, `ls -l`, and `readlink` so symlinks, real files, empty
   directories, and local-only settings are visible.
2. In agent-config or dotfiles repos, also inventory the managed source of truth
   and install mappings, such as `config/agent/**`, `docs/agent-config.md`, and
   `install-conf/dotbot.conf.yaml`. Root adapters may be absent because they are
   installed into user-level paths.
3. Choose the canonical instruction file. Default to root `AGENTS.md` unless the
   repo has a documented reason to use another source of truth.
4. Move durable shared instructions into the canonical file. Convert tool entry
   files to symlinks when the repo supports symlinks; use tiny pointer files only
   when symlinks are unsuitable.
5. Decide each hidden tool directory by behavior: keep it only if it contains a
   required runtime adapter, shared tool config, hook wiring, MCP config, or
   repo-local workspace skill path. Do not convert a managed user-global skill
   source into `.agents/skills` just because the repo contains skills. Remove
   empty obsolete directories and ignore local-only state such as
   `.claude/settings.local.json`.
6. Before renaming or deleting a live hook target, update adapters first; keep
   temporary compatibility only until sessions reload, then remove it and
   verify no stale references.
7. Verify the migration from filesystem evidence, not intent: `ls -l` /
   `readlink` for adapters, `ls -la` for tool directories, and VCS status/diff
   to confirm no generated, secret, or personal runtime state is tracked.

## Repo Skills

Use `.agents/skills/<name>/SKILL.md` as the canonical repo-scoped skills path
for normal app, library, and tooling repos. These skills travel with the
codebase and intentionally load only when working in that repo.

Keep user-global skills in user-level locations such as `~/.agents/skills`,
`~/.gemini/config/skills`, or `~/.gemini/antigravity-cli/skills`, or in a
dotfiles-managed source that links there. Do not symlink that user-global source
back into a repo's `.agents/skills` unless duplicate workspace visibility is
intentional.

Codex, Gemini CLI, and Antigravity support `.agents/skills` for workspace
skills. Prefer this over tool-specific workspace skill folders. Use
`.gemini/skills` only for Gemini-only workspace skills or legacy Gemini-only
layouts, and avoid keeping both paths with copied content.

Keep skills focused on reusable workflows. Do not turn `AGENTS.md` into a large
skill catalog; if a workflow has steps, references, scripts, or decision rules,
make it a skill.

## Tool-Specific Dirs

Use hidden tool directories for runtime behavior, not shared instruction prose:

- `.codex/`: Codex project config, hooks, rules, MCP, and Codex-only settings.
- `.gemini/`: Gemini project settings, sandbox files, and legacy Gemini skill
  compatibility.
- `.claude/`: usually local Claude state; commit only deliberate shared Claude
  settings after checking they contain no personal paths or permissions.
- `.agents/`: cross-agent workspace skills, Antigravity workspace rules, and
  Antigravity workspace MCP config.

When a setting affects all agents, put it in `AGENTS.md`. When it mechanically
enforces behavior for one tool, put it under that tool's directory.

## Review Checklist

1. Is there exactly one canonical repo instruction file?
2. Are adapter files symlinks or tiny pointers instead of copied prose? Verify
   actual filesystem state with `ls -l` / `readlink`; prefer symlinks when the
   repository supports them.
3. Are repo skills under `.agents/skills` unless a tool-specific path is truly
   required, and are user-global skill sources kept out of repo-local
   `.agents/skills`?
4. Are secrets, auth, trust state, generated files, logs, and personal UI prefs
   excluded?
5. Are tool-specific configs justified by actual behavior, not created for
   symmetry?
6. Are verification commands and project-specific workflow rules in `AGENTS.md`?
7. In dotfiles or agent-config repos, did the review include the managed source
   files and install mappings, not just root adapters?
8. After migration, are obsolete tool-specific directories removed or ignored
   when they no longer contain required runtime adapters?

Agent path support changes. Before changing claims about Claude, Codex, Gemini,
or Antigravity discovery paths, verify current official docs first.
