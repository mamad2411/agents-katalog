---
name: uxui-workflow
description: Run the full requirements → UX → UI workflow for a new product, app, website or feature. Phase 1 interviews the user and frames the problem (requirements.md). Phase 2 explores three solution concepts and maps the chosen one (ux-brief.md, design-brief.md). Phase 3 designs the UI with the rule of three on a Claude Design canvas in the conversation (3 directions, pick one, 3 variations, pick one), then locks a design system. The user makes every decision; the AI does the legwork. Use when the user wants to start a new project or design something from scratch, says "UX/UI workflow", "design workflow", "double diamond" or "requirements to UI", or invokes /uxui-workflow. Also use to resume the workflow when requirements.md or design-brief.md already exists.
license: MIT. Complete terms in LICENSE.txt
metadata:
  author: Jad (AI Tooltip)
  version: "1.0"
  guide: https://aitooltip.com/uxui-skill
---

# UX/UI workflow: requirements → UX → UI

Three phases. Each one goes wide, then narrows down. Phases 1 and 2 are the double diamond: first find the right problem, then the right solution. Phase 3 is a small diamond of its own, run with the rule of three.

| Phase | Diamond | Instructions | Output |
|---|---|---|---|
| 1. Requirements | Discover → Define: the right problem | `phases/1-requirements.md` | `requirements.md` |
| 2. UX discovery | Develop → Deliver: the right solution | `phases/2-ux-discovery.md` | `ux-brief.md`, `design-brief.md` |
| 3. UI | Directions → Variations: the rule of three | `phases/3-ui.md` | a Design canvas with every round, a design system, `ui-progress.md` |

## Ground rules (every phase)

- **The user makes every decision.** You do the legwork: find the questions, generate the options, compare them, write things up. Recommend an option with reasons; never pick it for them.
- **Go wide, then narrow down.** Generate options first, then converge on the one the user picks.
- **Stop at every 🛑 and wait.** Never answer your own checkpoint or assume a yes.
- **Stay in the current phase.** No screens, layouts or visuals before phase 3. If a new feature comes up after phase 1, note it and ask whether to add it to `requirements.md`; don't slip it in.
- **Read one phase file at a time.** Read only the instructions for the phase you're in, and don't read ahead.

## Where to start

Look for the workflow files in the project root. If you can't see files, ask the user to attach any they have.

1. **If the user named a phase** (for example `/uxui-workflow ui`, "start at phase 2", "just the rule of three"), go there. First check that its input exists: phase 2 needs `requirements.md`, phase 3 needs `design-brief.md`. If it's missing, say so and offer to run the earlier phase, or to work from something the user pastes.
2. **Otherwise, start from the files that exist:**
   - `ui-progress.md` → phase 3, on the canvas it links to, at the round it records
   - `design-brief.md` → phase 3
   - `requirements.md` but no `design-brief.md` → phase 2
   - neither → phase 1
3. **When resuming,** say in one line what you found and where you'll pick up, and wait for a yes. For example: "Found requirements.md for [project]. Picking up at phase 2, UX discovery. OK?"

Then read that phase's file and follow it.

## Show where you are

Open every phase with a one-line header, and add a new one when the phase switches from going wide to narrowing down:

> **Phase 1 · Requirements** · Discover (go wide)

The user should always know which phase they're in and whether you're opening options up or closing them down.

## Between phases

When a phase's instructions are done:

1. **Save the output** in the project root. If you can't write files, give each one as a complete downloadable markdown file.
2. **Recap** in 3–5 bullets what the user decided in this phase.
3. 🛑 **Ask before moving on:** start the next phase now, or stop here? Tell them they can pick up later in a new conversation with `/uxui-workflow`, because the files carry everything forward. If this conversation is already long, recommend starting fresh.
4. **Only on a yes,** read the next phase file and start it.

The workflow is done when the phase 3 screens are approved.
