---
name: create-local-skill
description: Scaffold a new user-local skill in ~/.codex/skills (and optionally ~/.claude/skills), then offer to promote it to a personal fork of agentic-skills
type: execution
version: v0.2
---

# Create Local Skill

Invoke as `$create-local-skill`.

Scaffold a new **user-local** skill directly into `~/.codex/skills/<name>/` (and optionally `~/.claude/skills/<name>/`) as a real directory. The upstream agentic-skills repo is not touched. At the end, offer to **promote** the skill by copying it into the user's personal fork.

`npx skillpacks uninstall-global` only removes skillpacks-owned skill installs whose source is inside the agentic-skills repo, so user-authored real directories are safe from upstream sync.

## Process

1. Parse `<skill-name>` and optional description from arguments. If missing, ask for:
   - Skill name (kebab-case)
   - One-line description
   - Type (default `execution`)
   - Whether to also create a Claude version in `~/.claude/skills/<name>/`

2. Validate `$HOME/.codex/skills/<name>`:
   - If it is a symlink into `agentic-skills/base/` or `agentic-skills/packs/`, refuse — it would shadow a repo-managed skill.
   - If it is a real dir or user-owned symlink, confirm before overwriting.

3. Write `~/.codex/skills/<name>/SKILL.md`:

   ```markdown
   ---
   name: <name>
   description: <description>
   type: <type>
   version: v0.0
   ---

   # <Title>

   Invoke as `$<name>`.

   <1-2 sentence purpose statement.>

   ## Workflow

   1. <step>
   2. <step>
   3. <step>

   ## Output

   <what the skill produces>
   ```

4. Optionally mirror to `~/.claude/skills/<name>/SKILL.md` (Claude frontmatter convention — no `Invoke as` line; add `argument-hint` if relevant).

5. Report created paths and remind the user of the runner-specific reload path. Claude Code should run `/reload-skills` first; `/clear` starts a new empty-context conversation and can pick up the refreshed registry; restart if the top-level `.claude/skills` directory did not exist at session start or the skill is still invisible. Codex should start a fresh Codex CLI session if the `$` skill list remains stale.

6. Ask: "Would you like to promote this skill to your personal fork of agentic-skills?"

   If yes:
   - Ask for the path to their fork. If they don't have one, explain: fork on GitHub and clone, or `git remote set-url origin <their-repo>` to repoint an existing clone.
   - Verify with `git -C <path> rev-parse --show-toplevel`.
   - Copy the skill into `<fork>/base/codex/<name>/` (and `<fork>/base/claude/<name>/` if applicable), or into a `<fork>/personal/...` subtree if the user prefers to segregate personal skills.
   - If the skill is promoted into a fork's `base/` or `packs/` tree, also update that fork's `tests/harness/bench-coverage.ts` and add either a deterministic custom setup under `tests/layer4/setups/` or an explicit blocked row with `blocked_reason` and `next_command`.
   - For promoted custom setups, include a deterministic quality rubric when practical, or record why quality scoring is blocked/deferred instead of adding a subjective rubric.
   - Recommend `pnpm --dir tests bench:coverage` before the promoted skill is committed.
   - Run `git status` in the fork and suggest a commit message. Do not commit or push — leave that to the user.

7. Safety note: pushing to the upstream agentic-skills repo requires write access. Plain clones without access are rejected at the remote; forks push to the user's own repo. Cannot route a user's experimental skill into the shared upstream.

## Notes

- Never write into this repo's `base/` or `packs/` directories. Target paths are always under `$HOME/.codex/skills`, `$HOME/.claude/skills`, or an explicitly-supplied personal fork path.
- Do not create extra docs beyond `SKILL.md` unless asked.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.

