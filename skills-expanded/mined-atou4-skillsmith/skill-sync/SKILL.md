---
name: skill-sync
description: Fix drift between installed agent skills across ~/.claude/skills, ~/.codex/skills and ~/.agents/skills. Relinks skills missing from an agent, removes dead links and reconciles duplicate copies, always proposing each change and asking first. Use after skill-audit reports problems, or when the user says "sync my skills", "why is this skill missing in Codex", or "make Claude and Codex have the same skills".
---

# Skill sync

Acts on the findings of `skill-audit`. Nothing changes without the user's approval of that specific change. The canonical store is `~/.agents/skills`; the agent folders hold links into it.

## Steps

1. **Get the findings.** Run `python3 -I <skill-audit folder>/scripts/audit.py` and read the report. If `skill-audit` is not installed, say so and stop.

2. **Classify each finding and propose a fix. Show the exact command, run nothing yet.**

   | Finding | Proposed fix |
   |---|---|
   | Broken symlink | Delete the dead link (`rm <link>`), or repoint it if the user says where the skill moved. |
   | Missing in an agent, canonical copy exists in `~/.agents/skills` | `ln -s ~/.agents/skills/<name> <agent dir>/<name>` |
   | Missing in an agent, skill exists only as a real folder in another agent's directory | Ask: move it into `~/.agents/skills` and link from both, or leave it single-agent on purpose. Never decide silently. |
   | Duplicate name, different target | Show both copies side by side (`diff -rq`). Ask which wins. The loser is renamed `<name>.bak-<date>`, never deleted. |
   | `name` differs from folder name | Report only. Renaming changes how the skill is invoked; the user chooses the folder name or the `name` field. |
   | No SKILL.md | Report only. It may be a plugin or runtime folder the tool manages. |

3. **Skip user-managed folders.** A real directory the user wrote or edited by hand is never moved, replaced or merged unless the user names it. Many "missing in Codex" entries are deliberate (Claude-only skills); offer a per-skill choice and a "skip all" option.

4. **Apply only approved changes,** one at a time or in a batch the user confirmed, and keep a log of each command run with its result.

5. **Verify.** Re-run the audit. Report the counts before and after, and anything that did not change. Tell the user skills appear after restarting the session.

## Rules

- Never delete a skill folder. Dead links may be removed; everything else is renamed or left alone.
- Never overwrite an existing path. Check that the destination does not exist before `ln -s` or `mv`.
- Removal requests apply to the project, not the machine, unless the user says otherwise.
- Do not touch plugin-managed folders (`~/.claude/plugins/...`); those update through the plugin manager.
