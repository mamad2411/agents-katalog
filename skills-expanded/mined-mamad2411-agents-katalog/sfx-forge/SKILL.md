---
name: sfx-forge
description: Generate sound effects for games using ElevenLabs API. Use this skill whenever the user mentions sound effects, SFX, audio generation, game sounds, or wants to create/export audio assets for a game project. Also triggers when the user has a SOUND_DESIGN.md or asks about generating sounds from prompts. Handles the entire pipeline — analyzing game code, writing sound design docs, generating AI audio variants, and letting the user pick favorites in a browser UI.
---

# SFX Forge

Generate game sound effects using the ElevenLabs Sound Effects API. Creates multiple variants per sound, presents a browser UI for the user to listen and compare, then exports the selected files ready to drop into the project.

You drive the entire workflow — the user only interacts with the browser to listen and choose.

## Setup (automatic)

SFX Forge lives in its own repo. On first use, clone it and set it up. Skip this if it's already cloned.

```bash
# Clone to a predictable location
SFX_FORGE_PATH="$HOME/.sfx-forge"
if [ ! -d "$SFX_FORGE_PATH" ]; then
  git clone https://github.com/filippello/sfx-game-maker.git "$SFX_FORGE_PATH"
  cd "$SFX_FORGE_PATH"
  python3 -m venv .venv
  source .venv/bin/activate
  pip install requests python-dotenv
fi
```

The user needs an ElevenLabs API key. Check if `$SFX_FORGE_PATH/.env` exists. If not, ask the user for their key and create it:

```
ELEVENLABS_API_KEY=sk_...
```

## Agentic Workflow

### Step 0: Ensure a Sound Design Document Exists

Check if the game project has a `SOUND_DESIGN.md`. If it exists, read it and skip to Step 1.

If it doesn't exist, generate one by analyzing the game's codebase:

1. **Explore the codebase** — understand the game's genre, aesthetic, and tech stack. Search for UI events, state transitions, combat/action moments, and menu interactions.
2. **Find existing audio references** — grep for `.mp3`, `.wav`, `.ogg`, `Audio`, `Sound`, `play(`, `SFX` to see what sounds are already expected in the code.
3. **Define the sonic identity** — establish the overall vibe (acoustic vs synthetic, dark vs bright, realistic vs stylized) based on the game's visual style and theme.
4. **Write `SOUND_DESIGN.md`** in the game project root:

```markdown
# [Game Name] — Sound Design

Aesthetic: **[2-3 word vibe]**.
[1-2 sentences on overall sonic identity]

---

### 1. `sound_name.mp3`
**Moment**: [When this plays]

> **Prompt**: [Rich ElevenLabs prompt. Physical source + environment + mood + duration. Max 450 chars.]
```

Sound categories to check for: UI (clicks, hovers, toggles), navigation (transitions, menus), game flow (start, turn, countdown, end), actions (attack, defend, use item), feedback (success, fail, level up), combat (hit, miss, death), ambient (background loops), music stings (victory, defeat).

Prompt guidelines: describe the physical source ("metal hitting wood"), environment ("in a closed room"), mood ("tense"), use comparisons ("like a revolver click"), and always end with duration. Min 0.5s, max 30s, max 450 chars.

### Step 1: Generate sounds.json

Read the `SOUND_DESIGN.md` and write `sounds.json` to the sfx-forge folder:

```json
{
  "sound_name": {
    "prompt": "The ElevenLabs prompt (max 450 chars)",
    "duration": 2.0,
    "desc": "When this plays in the game"
  }
}
```

Keys in snake_case — they become the final filenames.

### Step 2: Generate variants

```bash
cd "$SFX_FORGE_PATH" && source .venv/bin/activate && python generate.py
```

Creates 3 variants (v1, v2, v3) per sound in `sounds/<name>/`.

### Step 3: Start server and open browser

```bash
lsof -ti:8420 | xargs kill 2>/dev/null; true
cd "$SFX_FORGE_PATH" && source .venv/bin/activate
nohup python server.py > /tmp/sfx-forge.log 2>&1 &
sleep 2
curl -s -X POST http://localhost:8420/api/reset > /dev/null
open http://localhost:8420/review.html
```

Tell the user:
> "I opened the sound review UI in your browser. Play the variants for each sound and select the best one. If none work, click 'None' or 'Regenerate' to try new variants with modified prompts. Click **Done Reviewing** when you're finished."

### Step 4: Wait for the user

Poll until done:

```bash
curl -s http://localhost:8420/api/status
```

Returns: `{ "total": 18, "selected": 15, "regenerate": 2, "pending": 1, "done": false }`

Wait until `done` is `true`. Selections auto-save to `selections.json` on disk.

### Step 5: Finalize

```bash
cd "$SFX_FORGE_PATH" && source .venv/bin/activate && python finalize.py --auto
```

Copies selected variants to `output/<name>.mp3`.

If any sounds need regeneration, read `selections.json` for the user's notes. Rewrite the prompts in `sounds.json` incorporating the feedback, run `python generate.py --only <name>`, then reset and re-open the browser for another review round.

### Step 6: Copy to project

Copy files from `$SFX_FORGE_PATH/output/` to the game's sound assets folder (e.g. `public/assets/sounds/`).

### Step 7: Cleanup

```bash
kill $(lsof -ti:8420) 2>/dev/null; true
```

## Regeneration

The user can regenerate sounds directly from the browser UI:

- **Modify**: appends their notes to the original prompt ("Additional direction: less reverb")
- **New prompt**: replaces the prompt entirely with what the user writes

This happens in real-time via the server — no CLI needed.
