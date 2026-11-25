---
name: dinoctor-director
description: How to direct a good animated video in the Dinoctor app with the Dinoctor MCP tools - plan the story, pick a style, write the script, build scenes and shots (place, cast, actions, camera, light, text, transitions), check every shot with look_at_shot, add voice and music, and render. Use whenever the person asks to make, edit or finish a video, reel, short, explainer, ad or story in Dinoctor, or when the Dinoctor tools (open_dinoctor, get_project, add_shot, look_at_shot, render...) are available and the person wants a video.
---

# Directing a video in Dinoctor

Dinoctor is a free desktop app that makes animated videos. You direct it through its MCP tools while the person
watches the window. A project has scenes, a scene has shots, and each shot has a place, a cast, actions, text, a
camera move, lighting and a transition into the next shot.

Your job is to make a video that looks directed, not assembled: a clear hook, one idea per shot, moving cameras,
characters that act, readable text, and cuts that flow.

## Golden rules

1. **Never spend the person's money without a clear yes.** Tools that cost credits or usage (`generate_*`,
   `remove_background`, `relight`, `speak`, `style_job` build/fix/continue) answer with a price first.
   Tell the person the price in one line and wait. Only then call again with `confirm: true`.
   Destructive steps (`new_project`, `set_style` on a project with work, `delete_style`, `templates` delete) also
   need a yes.
2. **Never guess ids.** Every place, character, object, action, emotion, camera, light, text preset, animation and
   transition id comes from `library` for the project's style. Ask for one category at a time and use `search` to
   keep answers small (`library {category: "cameras", search: "zoom"}`).
3. **Look after you build.** After each shot (or each few changes) call `look_at_shot` at a moment or two in the shot and
   fix what's wrong: people cut off at the frame edge, text over faces, an empty frame, a dark shot, two characters
   on top of each other. Don't tell the person a shot is done before you've looked at it.
4. **Everything is undoable**, so make bold choices, but keep the person in the loop: `go_to` the shot you work
   on so they see it.
5. **Keep it short.** Most shots are 2 to 4 seconds. A 30 second video is about 8 to 12 shots.

## The workflow

### 1. Start
- `open_dinoctor`, then `status` and `get_project`.
- If the project already has work, ask before replacing it. `new_project {style, format, confirm}` starts fresh.
- Ask (or decide, if the person said "you choose") just these: what it's about, how long, **vertical** (Reels,
  Shorts, TikTok) or **horizontal** (YouTube), and voice-over or text only.

### 2. Pick the style
- `list_styles` shows every style with what it's for. Match the topic: playful stories suit cartoon or pixel
  styles; serious explainers suit documentary-like styles.
- `set_format` for vertical or horizontal.
- `samples {action: "list"}` shows ready-made recipes and whole films for the style. Starting from a good sample
  (`samples {action: "add", id}`) and changing it is often better than building from zero. Fill its empty picture
  spots with `fill_spot` (see `samples {action: "needs"}`).

### 3. Plan before you build
Write a short beat list for yourself (not a tool call):
- **Hook (first 2 seconds):** the most surprising picture or line. No logos or "hi, today we...".
- **Middle:** one idea per shot, each shot answering the last one.
- **End:** a payoff and, if the person wants one, a call to action.
Give each beat a place, who is in it, what they do, and how the camera moves.

### 4. Script and shots
- `script {action: "write", lines}` (5 to 15 words each, one line per shot) puts the script in and makes the shots for
  you, each sized to its line. Or pass `topic` to let Dinoctor write it (this uses the person's own Claude usage;
  say so first).
- Without a script, build with `add_scene` (a new place or moment) and `add_shot` (the next beat).
- `get_project` after building to get every shot id.

### 5. Direct each shot
Do these per shot, then `look_at_shot`:
- **Place:** `set_place {preset}`. Keep the same place across a scene so it feels like one location; change place
  when the scene changes. Add a few scenery items for depth (far items have negative z).
- **Cast:** `set_cast {op: "add", ref}`. Two or three characters at most. Spread them (x about -4 to 4), face them
  toward each other or the action, and use z to put one in front of another instead of side by side every time.
- **Acting:** `direct_cast` gives each shot something happening: an action (`type` from library actions) timed with
  `when` or `at`, an `emotion` that changes at the key moment, `talk` while a line is spoken, `look` toward whoever
  speaks. A shot where nobody moves feels dead.
- **Camera:** `set_camera {move, strength}`. Vary it: push-ins for emphasis, wide shots to show the place, close
  moves on faces for feelings, a quick move for energy. Don't use the same move on two shots in a row. For a
  precise move, use camera `set_keyframes`.
- **Light:** `set_light {preset}` for the mood (warm day, night, spooky...). Keep the light steady inside a scene.
- **Text:** `set_text` for the hook line, key numbers and short punchlines. Big and short (2 to 5 words), away from
  faces, near the top (y 15 to 25) or as captions near y 84. Pick a text preset and an animation from library.
  In the Documentary style a text can stand in the world like a person (`depth`, near + / far -, and behind people) and
  take the scene's light (`lit: true`). Any text can turn (`rotation`), blend (`blend_mode`, `opacity`) and get
  `effects` (blur, brightness, contrast, colour, black and white). `\n` in the words starts a new line.
- **Transition:** `set_transition {id}`. Mostly cuts; a matching or punchy transition on the big moments only.
  Ready-made combos add an end-of-shot move before the transition.
- **Fine control:** `set_keyframes` animates anything over time (a character crossing the frame, text growing, a light
  dimming), including a text's opacity, rotation, effects and depth, the Documentary focus distance (`dof:shot`, after
  `set_camera {focus}`) and the background picture (`backdrop:shot`). `edit_project` changes any field directly; read
  `how_to` once before using it.

### 6. Pictures (optional, paid)
If the style has no character or object that fits, `generate_picture` (kind character, background or picture)
make one (price first). `generated_pictures` + `put_picture` reuse earlier ones for free. `upload` brings in the
person's own pictures, videos and sounds. `draw` (action describe first, then draw a character, object or place) lets you draw simple
characters, objects and places yourself for free.

### 7. Sound
- **Voice:** `voices` to pick one, then `speak` (price first) makes the voice and fits each shot to its line;
  captions follow the words. `own_voice` uses the person's recording for free.
- **Music:** `music {path}` adds the person's file, lowered under the voice automatically.
- **Sound effects:** Dinoctor adds them from what happens in each shot. `sound_effects` turns them up, down or
  off, or swaps one.

### 8. Check, then render
- `look_at_shot {film: true, seconds}` at several moments across the whole film.
- `render {quality: "draft"}` first to check timing (quick), `render {action: "status"}` every 10 to 30 seconds.
- Then `render {quality: "final"}` and give the person the file path. `save_project` so nothing is lost.

## Units that trip people up
- Shot length and keyframe `at` are in **seconds**.
- Actions, emotions, talk, looks and text `at` / `from` / `to` / `until` are **percent of the shot** (0 to 100).
- Text x and y are percent of the frame (50, 50 is the middle).

## When something fails
Tool errors are one plain sentence that says what to do instead (a wrong id lists the valid ones). Fix the call
and try again. If Dinoctor isn't open, call `open_dinoctor`. `look_at_shot` doesn't work while a render runs, so wait for `render {action: "status"}` to say it's done.
