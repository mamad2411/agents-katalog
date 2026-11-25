---
name: help
description: Plugin help that answers questions about this plugin, finolabs-vibecode, in plain words (where to start, what it contains, how a skill, agent or script works, which skill fits your situation and the command to type next); it does not ask another agent for an opinion. Run only when the user asks for it.
disable-model-invocation: true
---

# Help: where do I start, what is here, which skill next?

Read [references/plain-language.md](references/plain-language.md) first to decide whether to use the beginner register in any mode, including how to handle a bare invocation. Then pick the mode that fits the user's question and read its reference:

**Advisory (agent judgment):** Talk to the user in the language they are using, including questions and option labels; keep command names, flags, file paths, skill names and other technical names unchanged.

| Mode | When | Read |
| --- | --- | --- |
| Start | New to the plugin or unsure how to begin | [references/start.md](references/start.md) |
| Contents | What the plugin contains or what exists for a purpose | [references/contents.md](references/contents.md) |
| Explain | How a named skill, agent or script works | [references/explain.md](references/explain.md) |
| Route | Which skill fits a situation, or which agent takes which work | [references/map.md](references/map.md) |
| Tips | Practical tips for everyday use | [references/tips.md](references/tips.md) |
| Troubleshoot | Something does not work as expected | [references/troubleshooting.md](references/troubleshooting.md) |

For one skill at a glance, read its page from the "Skill pages" list in [references/contents.md](references/contents.md), then its `SKILL.md`.

Read the target file before describing it so the answer is current.
The map lists every skill, including `setup` (with `add <feature>`, `instructions`, `check`, `scan` and `mode` subcommands) and the user-only `restore-point` save-and-restore command, plus `afk` for a time-boxed away mandate and `brb` as an older alias, `pause` (short name `gtg`) for draining work before a restart or shutdown, and `ask`, the older name of this skill.
`advisor` owns both one opinion and committees, `delegate` owns spec coordinator sessions, and `tidy` owns knowledge and handovers.
Read a procedure reference only when the question concerns that procedure. Answer and stop: invoke nothing; leave the how-to to the target skill when it runs.
On Codex the user types `$` instead of `/` for skill commands; Claude Code and Antigravity use `/`. Skills the user types, such as `setup`, may be missing from your own skill list; do not warn the user that they are missing.

The plugin also ships three agents instructed to leave project files unchanged: `reviewer`, `security-reviewer` and `navigator`; the map covers every distinct script name, every setup feature, review routing, receipts, judge, run hygiene, work records, context snapshots, quota on demand and advisory parallel slots.
