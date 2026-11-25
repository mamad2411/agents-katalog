---
name: mockups
description: "Use when the visual identity of the Power Apps app is approved and it is time for stage 4 of the pipeline: the Image Mockups Agent lists every screen, the navigation, loading, errors and empty states, and, with the user's authorization, the script generates one image per screen through the OpenAI API. Also redoes only the affected screens when the prototype came back with an adjustment. Do not use before /pp-en:design, or to draw a screen in YAML (use `powerapps-canvas`)."
user-invocable: true
disable-model-invocation: true
---

# /pp-en:mockups — Image Mockups Agent

Stage 4 of the pipeline, block **2. Identity and experience**. The `pp-en:mockups-agent` agent builds the
screen inventory and the image spec; you check, ask for authorization and generate the images.
Generating images costs money and sends the screen text to OpenAI: **only with the user's "go ahead"**.

`KIT` = `${CLAUDE_PLUGIN_ROOT}`. Output format: `KIT/skills/power-platform/references/output-format.md`.
State script: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/estado.py"`.
Models: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/modelos.py"`.
Image script: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/desenhar-mockups.py"`.
Key, model and error details: `KIT/skills/power-platform/references/mockups.md`.

## Before starting

1. `estado.py comecar mockups`. Exit 1: show the output and stop.
2. Check that `docs/planning/prd.md` and `ux-design-system.md` exist, with hex in section 3.
3. **Mode:**
   - **new**: `docs/planning/mockups/mockups.json` does not exist;
   - **resume**: the spec exists and the inventory was already checked ("Inventory checked" line in
     `screen-inventory.md`), but images are missing (e.g. the session stopped to set the key): go
     straight to step 4;
   - **adjustment**: the stage is *reopened* and the open round of `prototype-adjustments.md` has
     `screen` items. With no `screen` items, just confirm, go to the gate and close with the note "no screen change".

## Steps

1. **Agent.** Show `◆ Calling the Image Mockups Agent...` and call the subagent
   `pp-en:mockups-agent` (model: `modelos.py de mockups-agent`; empty line, do not pass `model`) passing:
   - `RAIZ`: the project root;
   - `KIT`: the value of `${CLAUDE_PLUGIN_ROOT}`;
   - `MODO`: `new` or `adjustment`, and in `adjustment` the round's `screen` items.
2. **Judge the deliverable** (`KIT/skills/power-platform/references/subagents.md`, "Judging the deliverable"):
   - `desenhar-mockups.py docs/planning/mockups/mockups.json --simular` must end in
     `0 error(s)` (the agent does not run scripts: the proof is yours);
   - every P0 `FR-xx` in `prd.md` appears in at least one screen in the table;
   - the frame follows the navigation in section 2.1 of `ux-design-system.md`.
   Error or gap: revision, with the `--simular` output or the requirement with no screen. Record it with
   `estado.py veredito mockups --agente mockups-agent --resultado <...> --motivo "..."`.
3. **Screen review** (checkpoint): show the screen table the agent returned (id, screen, roles,
   priority) and the frame in up to 8 lines. "Is any screen or state missing? Type 'approved'
   or say what to change." Change: call the agent again with the request. Approved: write
   "Inventory checked: <date>" in `screen-inventory.md`.
4. **Decision to generate** (checkpoint, `AskUserQuestion`). First, read in `brainstorm.md` the answer
   about sending the screen description to OpenAI: if it was "no", skip to option 3 without asking.
   Show the `# model · size · quality` line and the total of images from `--simular`:
   1. "Generate all N images (Recommended)";
   2. "Generate only the P0 screens (M images)";
   3. "Don't generate: go to the prototype without images".
   Say along with it: it costs per image (price on OpenAI's page) and the screen text goes out to OpenAI,
   with no real data.
5. **Key.** Check without showing it:
   `python -c "import os; print('set' if os.environ.get('OPENAI_API_KEY') else 'missing')"`.
   Missing: `Action in the environment` checkpoint with the step by step from
   `KIT/skills/power-platform/references/mockups.md` §2 (`setx OPENAI_API_KEY "<your-key>"` on Windows, `export` on macOS/Linux). Say
   that they must **close and reopen Claude Code in a new terminal** and run `/pp-en:mockups` again:
   the work done so far stays on disk. Never ask for the key in the conversation. Stop here.
6. **Generate:** `desenhar-mockups.py docs/planning/mockups/mockups.json` (P0 only: `--telas` with the
   ids; adjustment: `--telas <ids> --sobrescrever`). Read the last line: `N error(s)`. Error `M101`:
   table in section 6 of the same `mockups.md`.
7. **Image review** (checkpoint): ask them to open `docs/planning/mockups/mockups.md`.
   An image is not a source of color or measurement: judge structure and flow. Adjusting one screen: edit the
   item in the spec and generate only that one (`--telas <id> --sobrescrever`).

## Exit gate

- [ ] `screen-inventory.md` with frame, navigation map and every P0 screen, checked by the user.
- [ ] `--simular` with `0 error(s)` (paste the last line in the summary).
- [ ] Images generated **or** the decision not to generate recorded in the inventory (who decided, why, date).

## Closing

1. `estado.py concluir mockups --nota "<N> screens, <M> images"` (without images: `"<N> screens; images
   waived: <reason>"`).
2. Commit if `git_commit_por_etapa`: `pp(mockups): screen inventory and mockups`. The images go
   in the commit; the key never.
3. Summary and the "Next step" block the script printed.
