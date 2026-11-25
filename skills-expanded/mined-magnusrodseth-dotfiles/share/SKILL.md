---
name: share-skill
description: Package an installed Claude Code skill into a shareable zip in a fresh temp folder, then open that folder in Finder. Use when the user says "/share-skill <name>", "share the X skill", "bundle/export/package a skill to send someone", or wants a skill zipped up to hand off.
disable-model-invocation: true
argument-hint: [skill-name]
allowed-tools: Bash(bash *), Bash(open *)
---

# Share Skill

Package one installed skill into a `.zip` inside a fresh temp folder and open that folder in Finder, ready to hand off.

## Steps

1. **Identify the target skill** from the user's request. They may write `/share-skill the /humanize skill`, `share humanize`, or give a path. Extract the bare skill name (strip a leading `/`, ignore filler like "the" and "skill"). If no skill is named, ask which one.

2. **Run the packager**, passing the name. Use this skill's own base directory (shown when the skill loaded) for the script path:

   ```bash
   bash "<this-skill-base-dir>/scripts/share-skill.sh" <skill-name>
   ```

   The script takes either a bare name (`humanize`), a slash-command name (`/humanize`), or a path, absolute or relative, to a directory holding a `SKILL.md`. A path is tried verbatim first, so an absolute path works from any working directory. Failing that it searches `./.claude/skills`, `./.agents/skills`, `$CLAUDE_CONFIG_DIR/skills`, `~/.claude/skills` and `~/.agents/skills`. It then dereferences symlinks so the archive is self-contained, excludes junk (`.DS_Store`, `.git`, `*-cache*`, `node_modules`, `__pycache__`), zips it, drops the zip in a fresh temp folder, and opens that folder in Finder.

3. **Report** the `Zip:` and `Folder:` paths from the script output. Tell the user Finder is open on that folder, and that a recipient installs the skill by unzipping into `~/.claude/skills/` (personal) or a project's `.claude/skills/` (project), then starting a new session.

## Notes

- Output lands in a readable, date-stamped folder: `/tmp/shared-skills/<skill-name>_<YYYY-MM-DD_HHMMSS>/<skill-name>.zip`.
- The zip's top-level folder is the skill name, so it unzips to `<skill-name>/SKILL.md`.
- The Finder step is macOS-only; the zip is still built on other platforms.
- For richer distribution (versioning, bundling agents/hooks/MCP, a marketplace), package as a plugin with a `.claude-plugin/plugin.json` instead. See https://code.claude.com/docs/en/plugins. This skill covers the common case: a single skill, zipped, to send.
