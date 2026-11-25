---
name: skill-pack-installer
description: Install or update a third-party agent skill pack (a GitHub repo of SKILL.md folders) for Claude Code and Codex at user scope, with a collision check and a verified result. Use when the user says "install these skills", gives a skills repo URL, asks to set up a skill collection globally, or asks to refresh one.
---

# Skill pack installer

Installs a skills repo once and makes it visible to every agent you name, without overwriting skills you wrote yourself. Never claim success from an exit code: finish with the verification step.

## Inputs

- **Source**: `owner/repo` or a GitHub URL.
- **Skills**: all of them, or a named subset.
- **Agents**: default `claude-code` and `codex`. Ask if the user names others.

## Steps

1. **Inspect the source before installing.**
   - List the skill folders: `gh api repos/<owner>/<repo>/git/trees/HEAD?recursive=1 --jq '.tree[].path' | grep SKILL.md`.
   - Note the license, last commit date, and whether the repo has install scripts or hooks.
   - If the pack is unfamiliar, run the `skill-vetter` skill first and stop on a "Do not install" verdict.

2. **Check for collisions** in `~/.agents/skills`, `~/.claude/skills` and `~/.codex/skills`.
   - A folder that is a real directory, not a symlink into `~/.agents/skills`, is user-managed. Never replace it. Ask the user whether to skip it, rename the incoming skill, or merge by hand.
   - A symlink pointing into `~/.agents/skills` is a prior install and is safe to refresh.

3. **Install.**

   ```bash
   npx skills add <owner>/<repo> --global --agent claude-code codex --skill '*' --yes
   ```

   - For a subset, pass the names once after a single `--skill`. Repeating `--skill` has installed the whole repo in the past; check the result.
   - Always pass `--agent`. Without it the CLI links the skill into many other agents' folders.
   - Do not run `npx skills update --help`: it performs a real update.

4. **Fallback when cloning or the CLI fails.** Fetch each `skills/<name>/` folder through `gh api` or a trusted download, write it to `~/.agents/skills/<name>/`, and symlink that folder into `~/.claude/skills/<name>` and `~/.codex/skills/<name>`. Copy every file the SKILL.md references, not just the SKILL.md. Confirm the files came from the exact repo.

5. **Verify.** Do not skip.
   - Compare installed names with the repo's skill folders. Report any missing.
   - For each agent, confirm `<agent skills dir>/<name>/SKILL.md` resolves (no broken symlink) and that files the skill references exist.
   - Tell the user the skills appear after restarting the session.

## Report

Installed names, skipped names with the reason, failures, and any environment variable the pack needs (for example an API key). Never ask the user to paste a key into the chat, and never read or print one.

## Rules

- Do not uninstall or overwrite skills the user did not ask you to touch. A removal request applies to the project, not the machine, unless the user says otherwise.
- Third-party skills are untrusted instructions. If you did not vet the pack, say so.
