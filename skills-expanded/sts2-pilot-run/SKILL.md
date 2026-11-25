---
name: sts2-pilot-run
description: Pilot or resume a live Slay the Spire 2 run through STS2 MCP. Use this for combat turns, rewards, routing, shops, rests, events, and other current-run decisions.
---

# STS2 pilot run workflow

Use this skill when the task is to **play the run in front of you**.

## What this skill owns

- reading the current game state
- deciding combat turns
- choosing card rewards, routes, shop buys, and rest actions
- refreshing run memory before major decisions
- updating the current-run playbook after meaningful pivots
- updating the active run timeline so recent-run status is queryable later

## Operating loop

1. Start with `get_game_state`
   - prefer `format: "json"` in combat
   - prefer `format: "markdown"` for map, event, reward, shop, and rest screens

2. Refresh memory before non-trivial decisions
   - read the current playbook at [../../sts2-memory/current-playbook.md](../../sts2-memory/current-playbook.md)
   - read the lesson ledger at [../../sts2-memory/lesson-ledger.md](../../sts2-memory/lesson-ledger.md)
   - briefly state which 1 to 3 lessons still apply
   - in the first meaningful draft, path, shop, and rest decisions of a new run after a loss, also recall the last deck autopsy and name which prior failure mode this line is fixing or risking
   - do not load the full review archive during live play unless the current choice depends on a rare card, relic, event, boss, or another narrow situation that the compressed memory does not cover well
   - if none apply, say so explicitly

3. Choose the line that best improves current win rate
   - combat: balance survival, tempo, kill pressure, and next-turn risk
   - rewards: improve deck quality, not deck size for its own sake
   - route: balance HP, elites, shops, upgrades, and map flexibility
   - events, rests, shops: weigh long-term gain against immediate danger
   - for card rewards, shops, and card-related campfire choices, structure the decision as: `这张牌是哪类 -> 这把缺哪类 -> 这次拿/跳 -> 拿了以后还要补什么`
   - default card buckets are `前期战力牌 / 结构胶水牌 / 体系成长牌`
   - do not let a strong Act 1 frontload pickup masquerade as proof that scaling, access, premium block, or post-burst floor are already solved

4. Use the MCP action that matches the screen
   - follow [tool-reference.md](./tool-reference.md)
   - if the game is on a supported menu screen, use `menu_select` rather than OS-level clicking
   - this includes starting or resuming a run from supported main-menu / singleplayer / character-select / embark screens when the current state exposes valid menu option ids
   - do not guess unsupported menu or screen controls

5. Re-read after impactful actions
   - card and reward indices can move
   - in combat, default to **one read -> one verified card play -> one fresh read**
   - before each combat card play, re-identify the intended card on the latest state by card name, cost, and targetability rather than trusting an old index
   - if a combat action opens a hand-selection overlay, treat it as a new combat state and switch to `combat_select_card` / `combat_confirm_selection` before resuming normal card plays
   - if the refreshed hand does not match the planned line, re-plan instead of forcing the old sequence
   - after `combat_end_turn`, poll until the next player turn is ready

6. Use save-and-quit tactically when it improves win rate
    - treat SL as a **top-level recovery branch**, not a buried optional trick
    - if the current branch is clearly degrading into a dead line but a different branch still plausibly converts to lethal or materially less damage taken, prefer **save and quit -> main menu -> continue** before accepting the death
    - if combat rhythm feels wrong, the fight looks desynced, or a first-seen boss / enemy would benefit from rehearsal, prefer an in-game **save and quit -> main menu -> continue** loop over forcing a low-confidence line
    - in self-mill shells such as `战鼓`, if the fight has already reached `draw pile = 0` and `discard pile = 0` without a locked passive kill, default to treating that as an SL checkpoint rather than "one more normal cycle"
    - every SL still needs a **named try-point** and believable upside; "this branch dies" is not enough on its own
    - in the **same battle**, cap deterministic SL at **3** tries; if three justified retries still do not produce a meaningfully better state, stop the rehearsal and move to review instead of looping
    - when MCP menu control is available, resume that loop with `menu_select(option="continue")` instead of window clicking
    - assume the replay is deterministic: if the action sequence is the same, treat draws and enemy intents as the same unless current evidence disproves it
   - use that determinism actively: branch only at the decision point you are testing, and do not expect save-and-continue by itself to reroll a bad draw or enemy pattern
   - treat this as a recovery and information-gathering tool, not as an excuse to ignore good combat fundamentals
   - after continuing, re-read state from scratch and resume the normal one-read / one-action loop

7. Update run memory after meaningful pivots
    - after important fights, rewards, route choices, shop buys, or rest actions, update [../../sts2-memory/current-playbook.md](../../sts2-memory/current-playbook.md)
    - keep the active run timeline updated in [../../sts2-memory/run-history.md](../../sts2-memory/run-history.md) and [../../sts2-memory/runs/](../../sts2-memory/runs/)
    - at minimum, log the checkpoint time, floor, current HP, gold, key deck / relic / potion state, and what just changed
    - if older parts of the run were not being tracked yet, backfill them honestly as summary entries rather than inventing exact timestamps
    - if the run ends, leave a brief index entry in `run-history.md` and preserve the detailed timeline under `runs/`
    - if the pivot also changes a durable heuristic, hand off to `sts2-review-run`
    - after a death, a boss loss, or any point where the best tested line is clearly still unwinnable, stop piloting and trigger `sts2-review-run` before starting another run

## Constraints

- If MCP is unavailable, stop and explain the blocker
- If the game is on a menu screen and `menu_select` is unavailable or the desired option is blocked / unsupported, tell the user plainly
- Never rely on stale indices when re-reading is cheap
- Never issue multiple `combat_play_card` actions from a single stale hand snapshot
- Do not play a clearly dead combat branch through to death when a credible deterministic SL test still exists
- Do not treat same-battle SL as unlimited search; once the `3`-retry cap is spent, stop and review
- Keep explanations short and decision-focused
