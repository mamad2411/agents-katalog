---
name: meme-sounds
description: Pick and play a fitting meme sound effect (vine boom, bruh, airhorn, sad violin, and 38k more from DankMachine). Use when the user asks for a sound effect, a reaction sound, wants to celebrate or mourn a result with a sound, asks "what's the sound for <moment>", or wants sounds for a video, stream, Discord or meme. Also use when the user explicitly asks you to play a sound when something happens.
---

# Meme sounds

DankMachine has 38,000+ meme sounds, each with a short description of what it is and when to use it.

## Tools (from the dank-meme-sounds MCP server in this plugin)

- `find_reaction_sound` — best first call. Describe the moment in plain words ("tests finally passed", "awkward silence", "someone got roasted"); returns fitting sounds with what each means.
- `search_sounds` — by name or keyword ("vine boom", "minecraft", "anime wow").
- `get_trending_sounds` — what people play right now (`1h`, `24h`, `7d`).
- `random_sound`, `get_sound`, `list_categories`.
- `play_sound` — plays the sound out loud on the user's speakers.

## How to behave

1. Match the moment, not the keyword. Prefer `find_reaction_sound` with the situation; fall back to `search_sounds` for a named sound.
2. Only call `play_sound` when the user asked for audio or set up a rule like "play X when Y". Never play sounds unprompted in the middle of unrelated work, and never more than one at a time.
3. When suggesting sounds, give 1–3 options with their title and page link (`https://dankmachine.com/sound/<slug>/`), plus one line on why each fits.
4. Keep it light, but don't let the bit get in the way of the user's actual task.
5. If the MCP server is unavailable, use the free REST API instead: `https://dankmachine.com/api/v1/reaction?situation=<words>` or `/api/v1/search?q=<words>`, and play with `npx -y dank-meme-sounds play "<query>"`.

## Sound effects for coding sessions

If the user wants Claude Code to play sounds automatically (task done, needs input, session start), suggest adding hooks to their `~/.claude/settings.json`, for example:

```json
{
  "hooks": {
    "Stop": [{ "hooks": [{ "type": "command", "command": "npx -y dank-meme-sounds play \"vine boom\"" }] }],
    "Notification": [{ "hooks": [{ "type": "command", "command": "npx -y dank-meme-sounds play \"discord notification\"" }] }]
  }
}
```

Ask before editing their settings. The `play` command never fails a hook (it exits 0 when offline).

## Rights

Sounds are community meme clips with unverified rights: fine for personal use, fan edits and fun; recommend licensed audio for ads and client work. Removal requests: https://dankmachine.com/takedown/
