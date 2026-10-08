---
name: everden-playtest
description: Run Everden visual/play gates in the browser — screenshots, PLAYTEST rows, AGENT_RUNS log. Use when touching presentation, scenes, click-nav, or before bumping Experience % in PROGRESS.md. Does NOT substitute human T8 playtests or Nick eye tests.
---

# Everden Playtest (agent)

You are a **playtester**, not a unit-test runner. Your job is to **play the build visually** and log honest results.

## Before you start

1. Read `docs/systems/VISUAL_QA_AGENTS.md` (rubrics + agent types).
2. Read latest `docs/playtests/AGENT_RUNS.md` (known failures).
3. Ensure dev server: `npm run dev` (note port).
4. **Fresh save:** clear `everden_save_v1` via browser CDP or manual step.

## Visual scout procedure (default)

Use **cursor-ide-browser** MCP:

1. `browser_navigate` → dev URL
2. `browser_lock` before multi-step play
3. Start game (species → Enter Reedwater Basin)
4. **G1** — screenshot causeway spawn
5. **G2** — click canvas 3 times on walkable ground; confirm movement + debug ring
6. Walk to Lilymarket exit — **G3** screenshot; if exit not findable in 60s → FAIL discoverability
7. **G4** — click Pip (or walk + E); screenshot dialogue with portrait
8. Return to causeway — **G5** screenshot
9. `browser_unlock` when done

Score each gate and overall PASS / BORDERLINE / FAIL per rubric in `VISUAL_QA_AGENTS.md`.

## Persona scripts

### Fresh player (5 min)

- Do not read source files during play.
- Time: seconds until first successful NPC dialogue.
- List: "debug sandbox" tells (floating slab, art stack, label soup, invisible exits).

### Quest runner

Execute `docs/PLAYTEST.md` rows 4–10 with fresh save. Screenshot on every fail.

### Combat tester

Rows 11–14: Blackfen, diplomacy, abilities, flee, enemy turn advance.

### District explorer

Full causeway hub loop: lilymarket, croakend, mudwall, ferry_rest. Screenshot each district HUD name.

## Log output

Append to `docs/playtests/AGENT_RUNS.md`:

- Next `AR-NNN` id
- Verdict, gate checklist, FAIL bullets, screenshots taken
- Explicit: `Nick eye test: pending / pass / fail`

## What you must not do

- Mark T8 human playtests complete
- Increase Experience % in PROGRESS.md on FAIL or with gates G3/G4 not run
- Claim "BG3 feel" without screenshot evidence
- Skip browser because `npm test` passed

## Task tool launch template

When parent delegates, use `subagent_type: generalPurpose` with prompt:

```
Everden playtest — [visual-scout | fresh-player | quest-runner | combat-tester | district-explorer]
Read: docs/systems/VISUAL_QA_AGENTS.md + .cursor/skills/everden-playtest/SKILL.md
Dev URL: http://localhost:PORT
Fresh save required.
Append AGENT_RUNS.md with AR-NNN.
Return: verdict, gate table, blockers, screenshot descriptions.
Do not bump PROGRESS Experience %.
```
