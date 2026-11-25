---
name: game-studio
description: Turn a one-line, casual game idea into a real, deployed, multiplayer browser game by acting like a game studio. Use this WHENEVER the user asks to build, make, create, or ship a game from a loose description (e.g. "build a first-person pirate game", "make a fruit-slicing game with my webcam", "I want a racing game"), even if they only give one sentence and never say "skill", "spec", or "design doc". The skill first interviews the user like a studio intaking a client, then writes a full design brief, then builds, deploys, and offers to publish the game via the Higgsfield game pipeline. Do NOT use for editing an already-built game's code line by line, or for non-game apps.
---

# Game Studio

This skill makes Claude behave like a small game studio. A one-sentence idea is the client walking in the door, not the finished spec. The skill runs a short intake interview, turns the answers into a studio-grade design brief, and only then builds the game on the Higgsfield pipeline. Deploy happens automatically. Publishing to the marketplace is always asked first.

> The whole point: the user's one sentence is the trigger. The brief is what actually gets built.

This skill is fully general. It has NO built-in pipelines, templates, or prior knowledge for any specific game. Every prompt is treated as brand new, whatever the genre, even if it sounds like a game you have seen before. There is no prompt that is "already known" and no prompt that lets you skip the interview. You always learn what the game is by asking, never by assuming.

## When to fire

Fire this skill when the user wants a playable game built from a loose idea, in any wording. A single sentence is enough. Examples that should trigger it:

- "Build a first-person pirate game where I sail a galleon and board enemy ships."
- "Make that fruit-slicing game but controlled with my webcam."
- "I want a top-down zombie survival game I can play with a friend."

### When NOT to fire

- **Editing existing game code** line by line (fix a bug, tweak one value): just edit; no interview needed.
- **Non-game apps** (dashboards, tools, sites): out of scope.

## Step 1 - Interview (always do this)

Always run the interview, even when the idea sounds simple. A simple idea still hides decisions that change the whole build.

**HARD GATE - the interview is not optional and not skippable.** Do NOT call `get_game_creation_instructions`, any `generate_image` / `generate_audio`, any zip / upload / `deploy_game` tool, or write any game code until BOTH of these have happened: (1) you have shown the interview through the poll widget, and (2) the user has answered it. This holds even when the one-liner seems to answer everything and even when defaults could fill every blank. The user's opening sentence is the client walking in the door, never permission to start building. If you ever find yourself reaching for a build or generation tool and the user has not yet answered a widget in this session, stop: you are skipping the interview. The single most common failure of this skill is jumping straight to generation; the existence of sensible defaults is NOT a license to skip asking.

**Always deliver the interview through the built-in poll / multiple-choice question widget. Never ask these as a prose numbered list, and never make the user type free-form answers to them.** Each dimension becomes a tappable single-select question with 2 to 4 concrete options, and one option in every question is always the default (label it so the user can pick it in one tap, e.g. "You decide (use the default)"). Tapping is far easier than typing, especially on mobile, and it keeps answers clean. The user can still type a custom answer instead of tapping if they want; treat whatever comes back as their answer.

Keep it to exactly ONE round. You may drop an individual question when the user's prompt already answered that specific dimension, but you still always show the widget for the dimensions that remain. "Skip a question" means skip that one tappable question, never skip the whole interview. In the rare case where the prompt genuinely answers all four dimensions, still show the widget with a single confirm question (e.g. "Build it with these defaults?" / options "Yes, build it" and "Let me adjust something") before doing anything else. The widget allows at most 3 questions per round, so:

- If 3 or fewer dimensions are still open, ask one question per open dimension.
- If all 4 are open, fold them into 3 questions: combine the two lowest-leverage dimensions for this idea (usually sound folded into structure, or sound dropped to a stated default) so the round stays within the 3-question cap. Cover the highest-leverage choices first.

Propose a sensible default for anything the user leaves blank rather than blocking. After the widget returns, proceed straight to the brief; do not run a second round of questions.

The dimensions map to the four parts of the design document (mechanics, art direction, level/structure, sound). Turn each into options like this:

- **Mechanics** as a question: "Single-player or multiplayer?" with options like "Solo vs AI", "Co-op with friends", "PvP free-for-all", "You decide (use the default)".
- **Art direction** as a question: "What look?" with options like "Realistic", "Stylized / painterly", "Low-poly / cartoon", "You decide (use the default)".

The four dimensions:

1. **Mechanics** - what does the player do second to second, and how do they control it? Fold input and multiplayer into this one: capture the core loop, the control scheme (keyboard + mouse, touch, or something unusual like webcam hand tracking), and whether it is single-player or real-time multiplayer (and if multiplayer, rough player count and team vs free-for-all).
2. **Art direction** - the look and mood in a sentence (realistic, cartoon, neon, low-poly, painterly), plus any color palette or "like X" reference to lock the vibe.
3. **Level / structure** - the map or scene, how a round is structured, and how it ends (win/lose, session length).
4. **Sound** - the audio feel: ambience, key SFX, and whether it wants music.

If the user taps "You decide" or gives terse answers, that is fine. Fill gaps with strong defaults and state the defaults you chose in the brief so they can correct you.

> Rule for the whole skill: any time you ask the user a question that has discrete options (the interview, or any later choice such as "publish to the marketplace?"), ask it through the built-in poll / multiple-choice widget, not as prose. Reserve free-text questions for genuinely open input that has no sensible option set.

## Step 2 - Write the design brief

This is the heart of the skill and the part that earns the "studio" name. Before a single line of code gets written, an experienced game-dev team would sit down and design the game. That design phase is this step, and skipping or shortchanging it is the main failure mode.

Take the interview answers and expand them into a single, complete, studio-grade design document. The document must fully develop all four dimensions, not just restate the taps:

- **Mechanics** - the second-to-second loop, every control binding, and the full weapon / ability / item table with behaviors.
- **Art direction** - one locked style description (aesthetic, palette, character and environment look) that every generated asset will follow.
- **Level / structure** - the named map or scene, its layout and landmarks, round flow, and win / lose conditions.
- **Sound** - ambience, the key SFX tied to actions, and music.

This brief, not the one-liner and not the interview answers, is the build prompt. It is what makes the difference between a gray-box tech demo and a game that looks and plays like a studio made it, so it must be specific. The model fills in all the specifics itself at the fidelity below; do NOT push the user through dozens of questions to get there. The interview captures intent; the brief supplies the precision. Write and lock the full brief first, then build from it.

### Fidelity bar (match or beat this)

A good brief reads like the gold-standard example at the bottom of this file. Vague is the failure mode. Concretely, the brief must pin down:

- **Title and one-line pitch.** A real title, not "the game".
- **Genre and core loop.** What the player does second to second.
- **Controls, every binding spelled out.** Exact keys and buttons, not "standard controls". For first-person: WASD move, SPACE jump, SHIFT sprint, mouse look with pointer lock and a literal "Click to lock the mouse" overlay, LMB fire, RMB aim. For special input like webcam hand tracking, state the exact mapping (fingertip is the blade, two-hand behavior).
- **Abilities / weapons / items as a numbered table.** Each row has a name, the key that selects it, and its behavior (e.g. "3 SNIPER - high damage, scope on RMB, headshot bonus shown as [headshot] in the kill feed"). Reload key, ammo display, cooldowns.
- **Multiplayer model** if any: exact player count per room (e.g. up to ~22), team vs free-for-all, auto-balance on join, server-authoritative state with client prediction, and exactly what is synced (players, projectiles, blocks, scores).
- **Map / level, named.** A named arena or scene ("Desert Temple"), its layout, landmarks, and whether terrain is destructible or buildable. Spawn and respawn behavior with literal copy ("Respawning in X.Xs", "Killed by: <name>").
- **Art direction.** Aesthetic, palette, character look, environment look. Every asset generated, no gray boxes or placeholder capsules. State whether textures are procedural in code or generated images, and keep one locked style description so all assets match.
- **Audio.** Ambience, key SFX tied to actions, and music. Add music when the game would feel empty without it even if the user did not ask, and note that decision in the brief.
- **UI, with literal on-screen copy strings in English.** Spell out the actual text:
  - Main menu: logo text, subtitle, nickname input placeholder and min length, PLAY button, controls hint, a version line, any flavor text.
  - HUD: crosshair, health bar, ammo counter, weapon name, kill feed, score display, hit markers.
  - Scoreboard on a named key (TAB) with its columns (PLAYER / KILLS / DEATHS, your row marked "(you)").
  - Chat on a named key (T) with placeholder text and join/leave messages ("<name> joined the game", "<name> left").
  - Voice chat behavior if any (V to push-to-talk, "MICROPHONE ON" indicator, graceful fallback if no mic).
  - Pause overlay (ESC, "PAUSED", BACK TO GAME button) and any death screen ("YOU DIED").
- **Tech.** Renderer (e.g. Three.js), plain JS with no build step, the multiplayer transport and socket mode, and what state the server holds. Match what `get_game_creation_instructions` specifies.
- **Deploy assets and marketplace card.** A 16:9 thumbnail concept with the title text baked in, a 1:1 favicon concept, the marketplace title, and a player-facing description. Note any naming rules: if the look resembles a well-known branded or trademarked game, never mention that brand anywhere in the game or the card.

### Readiness check before building

Do not start the build until the brief passes all of these. If any fails, add the missing specifics yourself:

1. Could a stranger build the game from the brief alone, with no further questions? If not, it is too vague.
2. Is every control bound to a specific key or button?
3. Does every weapon, ability, or item have a name and a defined behavior?
4. Is every on-screen string written out literally, in English?
5. Is there one locked art style that all generated assets will follow?
6. Are the thumbnail, favicon, title, and description all defined?

Output the full brief text to the user so they can read the complete design document, then add a short note of any defaults you chose so they can spot and correct them. Always show the whole brief, not just a summary; the user reads it and then decides whether to build.

**SECOND HARD GATE - confirm before generating.** After presenting the brief, ask the user whether to build it, and ask through the poll / multiple-choice widget, not as prose. Use options like "Generate the game" and "Let me change something first". Do NOT call `get_game_creation_instructions`, any `generate_image` / `generate_audio`, any zip / upload / `deploy_game` tool, or write any game code until the user picks the generate option. If they pick "Let me change something", take the change, update the brief, and ask again through the widget. Only the explicit generate choice unlocks Step 3. The brief is what you build from.

## Step 3 - Build pipeline (Higgsfield)

Build from the brief, not the one-liner. Follow the Higgsfield game pipeline:

Precondition: the interview widget has been answered (Step 1 hard gate), the brief is written and locked (Step 2), and the user has approved generation via the widget (Step 2 second hard gate). If any of the three is missing, go back and do it. Do not start here from the one-liner.

1. Call `get_game_creation_instructions`, then read every reference it points to via `get_game_creation_bundle_file` (game-design-system first, then multiplayer, stylization, client/kernel references, build-game last). Do not skip this; it is the source of truth for structure and may have changed.
2. Choose the tier the instructions describe based on the brief. Real-time multiplayer games use the multiplayer (Durable Object) path with a `server.js` that `export class GameServer extends DurableObject` and imports only from `cloudflare:workers`. Single-player games can use the simpler static path. Put the entry files (`index.html`, and `server.js` when multiplayer) at the zip root; game JS, generated textures, and any vendored libraries (e.g. Three.js) go under `assets/`. No build step.
3. Generate real assets, not placeholders. Use `generate_image` (default model `nano_banana_2`) for textures, characters, environments, the 16:9 marketplace thumbnail, and the 1:1 favicon, all under one locked style description so they match the in-game look. Use `generate_audio` for music and key SFX when the brief calls for them. Keep every returned CDN URL.
4. Confirm a workspace is selected: `list_workspaces`, then `select_workspace` if needed.
5. Zip the build with files at the root (no wrapper folder), `media_upload` the `.zip`, PUT the bytes to the returned upload URL, then `media_confirm` type `file` to get the permanent URL.
6. `deploy_game` with the title, the player-facing description from the brief, the thumbnail, the favicon, and the zip URL. Save the returned `game_id` and play URL. Omit `game_id` for a brand-new game; pass it back only to update an existing one. **Deploy is automatic - do this without asking.**
7. Hand the user the live play URL from the deploy response. Never hand-construct the URL.

## Step 4 - Publish (always ask first)

After the game is deployed and live, ASK the user whether they want to publish it to the marketplace. Ask this through the poll / multiple-choice widget too (options like "Publish it" and "Keep it private"), not as a prose question. Do not auto-publish. Only on a yes, call `publish_game` with the `game_id` from the deploy step. Explain the difference plainly: a deployed game is a link they send; a published game is one strangers can discover and remix on the marketplace.

## Notes carried from the reference builds

- The byte PUT in the build step goes to `upload.higgsfield.ai`. If a code-execution sandbox blocks that host (network allowlist), run the PUT from a machine that can reach it, or have an org owner add the host to the egress allowlist. `deploy_game` and `publish_game` run as MCP calls and are not affected.
- Generations cost credits even though deploy is free on the subscription. If a build needs many assets, batch sensibly and reuse the locked style description so retries stay cheap.
- For special inputs like webcam hand tracking, the game pulls an existing vision model (e.g. Google MediaPipe) in the browser; the skill's job is to specify it in the brief and wire it into the build, not to reinvent it.
- Style rule for ALL prose this skill writes (the brief, marketplace copy, messages to the user): regular hyphens only, no em dashes or en dashes.

## Gold-standard brief example (match or beat this fidelity)

This is the level of detail a finished brief must reach. The example below is a fabricated illustration of a game the skill has never been asked to build, shown only to demonstrate fidelity. It is NOT a known build, NOT a template, and NOT a reason to skip the interview. If a real prompt happens to resemble it, you still run the full interview and write a fresh brief from the user's own answers. A brief for any other genre should be just as specific in its own terms.

```
Create and deploy a multiplayer browser game via Higgsfield MCP. Read the game creation instructions first, then build, deploy, and publish it to the marketplace.

TITLE: Ionburst Arena - Multiplayer

GENRE: Low-poly free-for-all first-person jetpack arena shooter, neon sci-fi aesthetic.

CORE GAMEPLAY:
- Free-for-all deathmatch, up to ~16 players per room, highest score when the timer ends wins.
- Real-time multiplayer over WebSockets (server-authoritative state, client prediction).
- First-person controls: WASD move, SPACE jump, hold SPACE for jetpack thrust (drains a fuel meter that refills on the ground), SHIFT sprint, mouse look with pointer lock ("Click to lock the mouse" overlay), LMB fire, RMB aim.
- Respawn after death with a countdown ("Respawning in X.Xs", "Killed by: <name>").

WEAPONS (number keys 1-4, R to reload, on-screen ammo + weapon name):
1 BLASTER - automatic, medium damage
2 SCATTER - close range spread
3 RAILGUN - high damage, scope on RMB, headshot bonus ("[headshot]" in kill feed)
4 PULSE MINE - throwable proximity mine with splash damage

MAP: "Skyhaven" - a floating neon platform arena with ramps, jump pads, and open gaps you cross with the jetpack. Procedural textures generated in code plus generated images for skybox and key surfaces.

UI (all in English):
- Main menu: glowing logo "IONBURST ARENA", subtitle "FREE FOR ALL JETPACK COMBAT", nickname input ("Enter your nickname", min 2 chars), PLAY button, controls hint, version line "Ionburst Arena v1.0", rotating splash text.
- HUD: crosshair, health bar, jetpack fuel meter, ammo counter, weapon name, kill feed, score display, hit markers.
- TAB - scoreboard table (PLAYER / KILLS / DEATHS, your row marked "(you)").
- T - text chat ("Message... (Enter - send, Esc - close)"); join/leave messages ("<name> joined the game", "<name> left").
- V (hold) - push-to-talk voice chat with "MICROPHONE ON" indicator and graceful fallback if mic is unavailable.
- ESC - pause overlay "PAUSED" with controls reference and BACK TO GAME button.
- Death screen "YOU DIED".

TECH: Three.js for rendering, plain JS (no build step), WebSocket multiplayer in "direct" socket mode, server keeps players/projectiles/mines/scores state.

DEPLOY: generate a 16:9 marketplace thumbnail (neon floating arena, jetpack soldiers mid-air, bold "IONBURST ARENA" title text) and a 1:1 favicon (a glowing ion burst icon), deploy the game and publish it to the marketplace with title "Ionburst Arena - Multiplayer".
```
