---
name: godot-narrative
description: Dialogue, quests and story state in Godot 4.7 - choosing Dialogue Manager, Dialogic, Yarn Spinner or Ink versus custom Resource dialogue, typewriter RichTextLabel boxes, choices with gamepad focus, portraits and voice blips, conditions and flags, quest logs, barks, cutscenes with Tween.tween_await, localized and accessible dialogue. Use for NPC conversations, branching stories or visual novels.
license: MIT
compatibility: Godot 4.7+ (GDScript and C#).
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# Narrative: Dialogue, Quests, Story State (4.7)

## Pick the dialogue format
| Option | When | Notes |
|---|---|---|
| **Dialogue Manager** (Nathan Hoad) | most games; writers like a screenplay-style text file | `.dialogue` files, branching, conditions, mutations that call your code, example balloons, CSV/PO translation export. **v4 needs Godot 4.6+**, v3 for older 4.x. GDScript and C# |
| **Yarn Spinner for Godot** | teams that already use Yarn, or that ship on several engines | the C# version is the stable one. The pure GDScript port (4.6+) was still beta/alpha in 2026, so don't ship on it without testing |
| **Ink** (GodotInk, C#) | heavy branching prose, writers using Inky | needs the .NET build |
| **Dialogic 2** | visual-novel style with an editor of characters, portraits and timelines | still **alpha** (4.5+), and the API changes between alphas. Pin the version |
| **Custom Resources** (reference) | small games, full control, no addon risk | `DialogueLineData` Resources edited in the inspector, or JSON/CSV exported from a spreadsheet |
Before installing, check that the addon release targets your Godot version (`godot-addons`). Look up an addon's API in its own docs, not from memory: the names change between majors.

## Architecture (any format)
```
GameState (autoload)    flags/variables Dictionary, saved with the game
DialogueRunner          walks the dialogue data, evaluates conditions, emits line/choices/ended
DialogueBox (CanvasLayer UI)  shows a line, typewriter, choices; knows nothing about story logic
QuestLog (autoload)     quests as Resources, progress via signals
```
- The **runner** emits `line_shown(speaker, text)`, `choices_shown(options)`, `dialogue_ended`. The **box** calls `runner.advance()` / `runner.choose(index)`. This split lets you reuse the box for barks, tutorials and cutscenes.
- Conversations pause gameplay through a state flag or `get_tree().paused`. Set the dialogue UI to `PROCESS_MODE_ALWAYS` (`godot-architecture`).
- Keep story state in **one** place (`GameState`) and save it with the save system. Use flags like `met_blacksmith`, counters like `gold`, and enums for quest stages.

## Conditions and effects in data
- In custom formats, conditions are strings (`"gold >= 10 and not met_king"`). Evaluate them with `Expression.parse(text, var_names)` then `execute(values, GameState, true, true)`. `const_calls_only = true` blocks calls with side effects. Parse once and cache.
- Never evaluate expressions from untrusted sources (mods, downloads) without `const_calls_only`.
- Effects (`set gold -= 10`, `give_item("key")`) are better as a small list of commands that your runner understands than as free code.

## Dialogue box essentials
- `RichTextLabel` with `bbcode_enabled`, `fit_content`, `visible_characters_behavior = TextServer.VC_CHARS_AFTER_SHAPING` (no jumping when words wrap). Typewriter: tween `visible_ratio` 0 → 1, or step `visible_characters` on a timer for per-character sounds and punctuation pauses.
- First press: finish the line (`visible_ratio = 1`). Second press: advance. Accept `ui_accept` and mouse/touch. Ignore input for ~0.1 s after a line appears so a held button doesn't skip text.
- Choices: build `Button`s in a `VBoxContainer`, call `grab_focus()` on the first one (gamepad), and add number keys for PC. Disable instead of hiding locked options when the player should see what they missed.
- Voice blips: an `AudioStreamRandomizer` with `random_pitch` ~1.1, played every 2–3 characters, with a different pitch per speaker.
- Portraits: a `TextureRect` per side, swapped by speaker and emotion keys (`"ana_happy"`), from a `Dictionary[StringName, Texture2D]` Resource.
- Name plate and color per speaker; text speed, auto-advance and font size in the settings.

## Localization
- Every line needs a stable **key**, not the English text as the key, so rewriting English doesn't break translations. Addons generate the keys and export CSV/PO.
- Custom data: store keys and call `tr(key)`. Plurals: `tr_n(singular, plural, n)`. Context: `tr(key, &"menu")`. Insert names with `format()` **after** translating.
- Test with pseudolocalization (`TranslationServer.pseudolocalization_enabled`) for 30–40 % longer text, and size boxes with `fit_content` (`godot-ui`).

## Quests
- `QuestData` Resource: `id`, `title`, `description`, `objectives: Array[ObjectiveData]` (`id`, `text`, `required`), `rewards`. Runtime progress lives in `QuestLog` (Dictionary id → progress), not in the Resource, which is shared.
- Gameplay emits generic events (`enemy_killed(kind)`, `item_collected(id)`, `talked_to(npc)`) on an event bus. The quest log listens and updates objectives, so gameplay code never knows about quests.
- Signals `quest_started`, `objective_updated`, `quest_completed` drive the HUD tracker and the journal UI.

## Barks and cutscenes
- Barks (short lines in the world): a `Label3D`/`Label` over the NPC, a pool of lines with a cooldown, never blocking input.
- Cutscenes: an `AnimationPlayer` with camera and character tracks plus **method call tracks** that start dialogue. Pause the animation until the dialogue ends: `await runner.dialogue_ended` in code, or in a Tween use `tween_await(runner.dialogue_ended)` (4.7) between steps.
- Skippable: `AnimationPlayer.advance()` to the end or `seek(length, true)`, then apply the final state (flags) the same way as when it plays out.

## Accessibility
Text speed options and instant text, auto-advance, high-contrast box, no information only in color, and screen-reader support: set `accessibility_live` on the line label (4.5+, AccessKit, experimental; `godot-ui`).

Dialogue Resources, runner with conditions, typewriter box, choices, GameState, quest log and cutscene await (compiled by the tests): [references/patterns.md](references/patterns.md)
