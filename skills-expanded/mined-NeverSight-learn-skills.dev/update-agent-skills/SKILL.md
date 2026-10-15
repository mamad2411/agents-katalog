---
name: update-agent-skills
description: Update agent skills installed with the `skills` CLI. Use when asked to refresh installed skills, keep a project's skills current, or troubleshoot cases where `npx skills update` reports that everything is up to date. For project-scoped installs, a no-change update must immediately run the bundled reinstall script so tracked skills from `skills-lock.json` are reinstalled without extra investigation.
---

# Update Agent Skills

## Goal

Refresh installed agent skills with the standard `skills` CLI workflow.

Use the normal update command first. If the skills were installed with project scope and the CLI does not detect upstream changes, reinstall each tracked project skill explicitly from its recorded source.

For project-scoped installs, treat a no-change `npx skills update` result as a mandatory fallback trigger. Do not wait for separate proof that a specific skill is stale.
Prefer the bundled reinstall script over manual command discovery. It already knows how to read `skills-lock.json`, filter to installed project skills, batch by repository, and pass non-interactive flags.

## Detect the Installation Scope

1. Check whether the target skills are project-scoped or global.
   - Project-scoped installs usually have a local `skills-lock.json` and one or more agent skill directories such as `.agents/skills/`, `.claude/skills/`, or `.augment/skills/`.
   - Global installs are typically tracked outside the project, for example in `~/.agents/.skill-lock.json` or `$XDG_STATE_HOME/skills/.skill-lock.json`.

2. Check which skills are actually managed by the `skills` CLI.
   - Use `skills-lock.json` or the relevant global lock file as the source of truth.
   - Do not assume custom or manually copied skills are tracked.
   - For project-scoped installs, consider the installed skill directories under `.agents/skills/`, `.claude/skills/`, or `.augment/skills/`.

## Standard Update Flow

1. Run:

```bash
npx skills update
```

2. Branch on the installation scope and the command result:
   - If the install is global and `npx skills update` succeeds, stop there unless the user explicitly asked for a forced reinstall.
   - If the install is project-scoped and the command clearly reports that one or more tracked skills were updated, stop there.
   - If the install is project-scoped and the command reports `All skills are up to date`, or otherwise makes no tracked-skill changes, go directly to the fallback flow below.

3. Do not use a presence check in the installed project skill directories to decide whether the fallback is needed. Presence only tells you which tracked skills exist locally and therefore must be reinstalled.
4. Do not pause to inspect `npx skills add --help`, read the CLI source, or rediscover flags unless the bundled script fails. That investigation slows the task down and is unnecessary for the normal fallback path.

## Fallback Flow for Project-Scoped Skills

1. Open `skills-lock.json`.
2. Treat `skills-lock.json` as the source of truth for tracked skills.
3. Cross-check it against the installed project skill directories and only keep skills that are both:
   - listed in `skills-lock.json`
   - present in at least one supported directory such as `.agents/skills/`, `.claude/skills/`, or `.augment/skills/`
4. The bundled script lives inside the installed `update-agent-skills` skill directory, not in the user's project `scripts/` folder.
5. Prefer the bundled script for the reinstall loop and run it immediately after a no-op project-scoped update. Resolve it from the installed skill path first:

```bash
for dir in .agents/skills .claude/skills .augment/skills; do
  candidate="$dir/update-agent-skills/scripts/reinstall_project_skills_from_lock.sh"
  if [ -x "$candidate" ]; then
    "$candidate" --project-root .
    break
  fi
done
```

6. If the script is installed under `.agents/skills/update-agent-skills/`, prefer calling that path directly instead of searching the whole workspace.
7. If the script is not present in those standard installed skill paths, fall back to the manual grouped reinstall flow immediately. Do not use broad `find` or `rg` searches across the workspace just to rediscover the same script.
8. The script is the fast path because it batches skills that share a repository and uses `-y` to avoid interactive prompts.
9. If you do not use the script, and `npx skills update` was a no-op for a project-scoped install, reinstall every matching skill manually. Do not stop after inspecting just one skill, and do not conclude success merely because the directories are present.
10. For each matching skill or skill group that shares a repository, read its `source` and reinstall it explicitly.

```bash
npx skills add [repository] --skill [skill]
```

11. Prefer the non-interactive form when reinstalling manually:

```bash
npx skills add [repository] --skill [skill1] [skill2] ... -y
```

12. Repeat that command for every matching repository or skill. Do not stop after the first one, and do not guess missing repositories manually.

Example loop:

```text
group tracked installed skills by repository:
  npx skills add [repository] --skill [skill1] [skill2] ... -y
```

Example:

```bash
npx skills add https://github.com/code-sherpas/agent-skills --skill atomic-design update-agent-skills write-persistence-representations -y
```

13. If the `sourceType` is `github` and the `source` is recorded as `owner/repo` such as `github/awesome-copilot`, convert it to the repository form expected by the CLI, for example `https://github.com/owner/repo`.

## Interactive Choices

If the CLI prompts for installation details:

- Agent selection: choose the default option unless the task says otherwise.
- Scope: choose `Project` for project-scoped updates.
- Installation method: choose `Symlink`.

## Validation

Before finishing:

1. Confirm the target skill directory now contains the updated skill content.
2. Confirm the refreshed skill still matches the source and the expected skill name.
3. If the install was project-scoped and `npx skills update` returned `All skills are up to date`, call out that this no-op result triggered the explicit reinstall loop.
4. Do not report success based only on the fact that the skill directories already existed before the reinstall.
5. If the bundled script was unavailable or failed and you had to fall back to manual commands, call that out explicitly.

## Report the Outcome

When finishing the task:

- State whether `npx skills update` worked or the fallback reinstall flow was needed.
- State which skills were refreshed and from which repository.
- State whether the update was project-scoped or global.
