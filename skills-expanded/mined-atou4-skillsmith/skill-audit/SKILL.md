---
name: skill-audit
description: Audit installed agent skills across ~/.claude/skills, ~/.codex/skills and ~/.agents/skills for broken symlinks, duplicates, drift between agents, malformed SKILL.md files, and unknown provenance. Use when the user asks "what skills do I have", "clean up my skills", "why is this skill missing in Codex", or after installing or removing a pack.
---

# Skill audit

Read-only. The audit never deletes, moves or edits a skill; it reports, and the user decides.

## Run

```bash
python3 -I <this skill's folder>/scripts/audit.py
```

Optional: pass extra skill roots as arguments. Output is Markdown on stdout.

## What it reports

| Finding | Meaning |
|---|---|
| **Broken symlink** | A skill entry whose target no longer exists. The agent will not load it. |
| **Missing in an agent** | Present in one root but not another (for example in Claude but not Codex). Often a link that was never made. |
| **Duplicate name, different target** | The same skill name resolves to different folders in different roots. One agent may run an older copy. |
| **User-managed** | A real directory, not a symlink. Probably written or edited by hand; installers must not overwrite it. |
| **Malformed** | No SKILL.md, no `name` or `description` in frontmatter, or `name` differs from the folder name. |
| **Origin** | Where a symlink points (`~/.agents/skills`, another tool's folder, or elsewhere). |

## After running

1. Summarize counts per finding, then list only the findings, not every healthy skill.
2. For each, propose a fix as a command but do not run it. Typical fixes: recreate a link, delete a dead link, rename a folder to match its `name`.
3. Never recommend removing a user-managed skill. Removal applies only to what the user explicitly names.
4. Offer the `skill-sync` skill to apply the fixes, with approval for each change.
5. Remind the user that skill changes appear after restarting the session.
