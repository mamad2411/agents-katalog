---
name: only-skill-you-need
description: >
  The first and only skill a beginner should install. Bootstraps the rest of the
  agent skill stack for this project, then routes every task to the current best
  skill for that job. Keeps a dual ledger (global defaults + project overlay)
  so the same use-case never gets two skills and a worse skill never replaces a
  better one. This skill should be used when starting a new project, setting up
  Claude Code / Cursor / Codex / Copilot, asking "what skills should I use",
  "best skills right now", "bootstrap my skills", "the only skill I need",
  beginning any coding task where the right skill might already exist, or when
  the agent is about to write code without first checking the skill ledger.
---

# only-skill-you-need

Announce: `Using only-skill-you-need to [bootstrap | route this task]`.

This is the first skill. Do not skip it to "just start coding." Read the winners it names, then do the user's actual work.

Scripts live next to this file. Run them from the skill root (`SKILL.md`'s directory).

```bash
python scripts/cli.py detect --root <project>
python scripts/cli.py status --root <project>
python scripts/cli.py bootstrap --root <project> --offline
python scripts/cli.py route --root <project> --offline "<user task>"
python scripts/cli.py --self-check
```

`--offline` uses the bundled seed list. Omit it to live-search via `npx skills find`. Never pass `--apply` until the user says yes.

## Procedure

1. Run `detect`, then `status`.
2. If `project_ledger_empty` is true → **bootstrap path**. Print the proposed pack. **Stop and ask** before any install. After yes, run bootstrap with `--apply`, then `npx skills add` using the printed `install_commands` (or run those commands). Refresh STATUS.md.
3. Else run `route "<user task>"`.
4. **Read** each winner's `SKILL.md` (installed copy under `~/.claude/skills`, `~/.cursor/skills`, or `~/.agents/skills`) before doing the user's work.
5. Empty relevant slot → propose the live best from the route/bootstrap output. Wait. Install. Record via `--apply` or `occupy` through bootstrap.
6. Occupied slot + upgrade listed → **mention** the better skill. Do **not** replace it unless the user asks to switch.
7. Do the actual task following those skills.
8. Run `status` again so `.agents/only-skill-you-need/STATUS.md` is current.

## Sticky rules

- Empty slot → propose, install only after yes.
- Occupied slot → keep the installed skill.
- Same use-case → refuse a second install; it lands in `rejected[]`.
- Unknown source with under 100 installs → never propose.
- Project ledger wins over global per slot.

Do not invent a parallel registry. Installs go through `npx skills add <owner/repo> -s <skill> -g -y` plus `-a` only for agents `detect` found.

## More

- Slot taxonomy: [references/slots.md](references/slots.md)
- Scoring and sticky gate: [references/quality.md](references/quality.md)
- Stack packs: [references/bootstrap.md](references/bootstrap.md)
- Agent install paths: [references/agents.md](references/agents.md)
