---
name: prototype
description: "Use when the screen inventory and mockups of the Power Apps app are ready and it is time for stage 5 of the pipeline: the HTML Mockup Generator Agent builds a navigable prototype (an index.html that opens offline) on top of the mockups, and the user approves it or asks for adjustments. Once approved, the pipeline moves on to architecture; with adjustments, it goes back to /pp-en:design. Do not use before /pp-en:mockups, or to build the real screen (use `/pp-en:build`)."
user-invocable: true
disable-model-invocation: true
---

# /pp-en:prototype — HTML Mockup Generator Agent

Stage 5 of the pipeline, block **2. Identity and experience**. The `pp-en:prototype-agent` agent builds the
navigable prototype from the approved mockups, the component catalog and the tokens. You
check it and bring the design question to the user: **prototype approved?**

`KIT` = `${CLAUDE_PLUGIN_ROOT}`. Output format: `KIT/skills/power-platform/references/output-format.md`.
State script: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/estado.py"`.
Models: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/modelos.py"`.
Verifier: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/verificar-prototipo.py"`.
Captures: `python "${CLAUDE_PLUGIN_ROOT}/skills/power-platform/scripts/capturar-telas.py"`.

## Before starting

1. `estado.py comecar prototype`. Exit 1: show the output and stop.
2. Check that `docs/planning/screen-inventory.md`, `mockups/mockups.json` and
   `ux-design-system.md` exist. PNGs are desirable, not mandatory (without images the verifier warns V013).
3. **Mode:** *adjustment* if the stage is *reopened* and the open round of `prototype-adjustments.md` has
   `behavior` or `screen` items; otherwise *new*.

## Steps

1. **Agent.** Show `◆ Calling the HTML Mockup Generator Agent...` and call `pp-en:prototype-agent`
   with `RAIZ`, `KIT` (the value of `${CLAUDE_PLUGIN_ROOT}`) and `MODO` (`new` or `adjustment`; in `adjustment`, the round's items).
   Model: `modelos.py de prototype-agent` (empty line: do not pass `model`).
2. **Judge the deliverable** (`KIT/skills/power-platform/references/subagents.md`, "Judging the deliverable"):
   `verificar-prototipo.py docs/planning/prototype --mockups docs/planning/mockups/mockups.json`
   must end in `0 error(s)`, and every screen in the inventory has its `<section data-tela>`.
   Then **look** (`KIT/skills/power-platform/references/visual-verification.md`):
   `capturar-telas.py docs/planning/prototype/index.html` and open each image; check the
   table in §2. For different roles, `--perfil <key>` on the screens that change by role.
   Error, missing screen or visual defect: revision, with the output or the image and the region. Record it with
   `estado.py veredito prototype --agente prototype-agent --resultado <...> --motivo "..."`.
3. **Open it for the user.** Offer to open the file (`start "" "docs/planning/prototype/index.html"`
   on Windows, `open` on macOS, `xdg-open` on Linux) or the double click. Explain in 3 lines:
   - the role selector at the top shows the app as each role sees it;
   - the guided tour walks through the screens;
   - "Compare with the mockup" opens the source image;
   - the "Navigation" selector switches the menu live (the one marked "(design)" is the chosen one);
     preferring another pattern is an adjustment item.
4. **Prototype approved?** (`Review` checkpoint, `AskUserQuestion`):
   - "Approved: go to architecture";
   - "Needs adjustments".
5. **Approved:** ask who approved (name or role) and write in `screen-inventory.md`:
   "Prototype approved by <who> on <date>".
6. **Adjustments:** collect one item at a time (which screen, what to change, why) until the user says
   they are done. Write in `docs/planning/prototype-adjustments.md` a new section `## Round N — <date>`
   with the table `| # | Screen | Request | Class | Status |` (class blank: design classifies).
   In the next round, mark as `done` the items from the previous one that the new prototype resolved.

## Exit gate

- [ ] `verificar-prototipo.py` with `0 error(s)` (last line in the summary; V013 warnings explained).
- [ ] Every screen in the inventory has `<section data-tela>` with its source `data-mockups`.
- [ ] Screens captured and looked at (`visual-verification.md`), or "not verified" if there is no browser.
- [ ] Approval recorded in the inventory **or** adjustment round recorded.

## Closing

- **Approved:** `estado.py concluir prototype --nota "approved by <who>"`. The next step is
  architecture.
- **Adjustments:** `estado.py reabrir design --motivo "prototype adjustments, round N (<k> items)"`. The
  script reopens design, mockups and prototype and points to `/pp-en:design`: it is the "Adjust" loop back of the design.
- Commit if `git_commit_por_etapa`: `pp(prototype): <approved | adjustments round N>`.
- Summary and the "Next step" block the script printed.
