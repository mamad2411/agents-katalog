---
name: claude-brainrot
description: 'Always-on autonomous meme dropper. A UserPromptSubmit hook fires every user message and tells Claude to drop multiple memes per response — 1-3 image+sound combos plus 1-5 sound-only fires, scaled to response length. Every answer carries brainrot. No invocation needed; loads and stays active automatically. The roast lands through the meme itself, never words. Self-contained skill — catalogue and assets live in this skill folder.'
allowed-tools: Read Bash(afplay *) Bash(open *) Bash(cat *) Bash(test *)
hooks:
  UserPromptSubmit:
    - hooks:
        - type: command
          command: "${CLAUDE_PROJECT_DIR}/.claude/skills/claude-brainrot/scripts/remind-fire.sh"
          args: []
  PreToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          if: "Read(*/.claude/skills/claude-brainrot/images/*)"
          command: "${CLAUDE_PROJECT_DIR}/.claude/skills/claude-brainrot/scripts/block-cli-read.sh"
          args: []
  PostToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          if: "Read(*/.claude/skills/claude-brainrot/images/*)"
          command: "${CLAUDE_PROJECT_DIR}/.claude/skills/claude-brainrot/scripts/play-paired-sound.sh"
          args: []
    - matcher: "Bash"
      hooks:
        - type: command
          if: "Bash(*claude-brainrot/images/*)"
          command: "${CLAUDE_PROJECT_DIR}/.claude/skills/claude-brainrot/scripts/play-paired-sound.sh"
          args: []
---

# Claude Brainrot

Drop the right meme at the right moment. **Autonomous-only — Claude decides when, never the user.** No slug arguments, no manual invocation.

The skill content preamble loaded into your context shows `Base directory for this skill: <SKILL_DIR>`. Use that as the base for all path resolution.

The catalogue is at `<SKILL_DIR>/catalogue.json` with two pools — `images` and `sounds`. Each entry has a `slug`, `path` (relative to SKILL_DIR), `tags`, and a `vibe` text describing when to use it.

**Image-side flags (mutually exclusive):**
- `lock_sound: "<slug>"` — force a specific paired sound (e.g. skeleton ↔ skeleton, cooked-dog ↔ vine-boom).
- `silent: true` — fire image only, no sound.
- `preferred_sounds: [...]` — soft bias: hook picks from this array 80% of the time, falls back to tag overlap 20%.
- (none of the above) — pure tag-overlap pick from non-locked, non-standalone sounds.

**Sound-side flags:**
- `locked: true` — only fires when an image's `lock_sound` points here. Excluded from generic auto-pairing.
- `standalone: true` — never plays as an image-paired sound; reserved for sound-only fires from Claude.

## When to fire

**Every user turn fires memes.** The `UserPromptSubmit` hook injects a `<system-reminder>` wrapped in 🔔 markers on every prompt. There is no skip turn — always drop something.

**Density scales to your response length.** The reminder spells it out:
- **Short prose answer (no tool calls):** 1 image+sound combo  OR  1-2 sound-only fires
- **Medium response (a few tool calls):** 1-2 image+sound combos  +  2-3 sound-only fires sprinkled between calls
- **Long response (many tool calls, multi-step work, builds, deep reads):** 2-3 image+sound combos distributed across the response  +  3-5 sound-only fires throughout

**Critical scan habit:** the 🔔 signal may land at the **TAIL of the previous tool result** (not just the top of the user message), because the `UserPromptSubmit` hook output is appended to whatever buffer is open when the next user prompt arrives. **Before responding to any user message, scan the end of the most recent tool result for the 🔔 BRAINROT signal.** If you only check the user message you'll miss it.

**Pick the mood:** match the conversational moment to a tag, then read candidate `vibe` fields:
- Real shock moment → `shock`
- User confused / weird ask → `confusion`
- Big freakout / rage vibe → `rage`
- Joke landed / wanting to rage-bait the user → `laugh`
- Sarcastic disbelief / dunk-able moment → `bruh`
- Sudden attention beat / punctuation → `alert`

If no specific signal: default to `bruh` — it's the catch-all and most entries carry it.

## Tag vocabulary

`bruh`, `rage`, `laugh`, `alert`, `shock`, `confusion`

Each entry's `vibe` field is the human-readable trigger description — **read it and match the conversational moment**, then use tags to filter candidates.

## Selection algorithm

**Image+sound combo (the normal fire):**
1. Pick a mood tag based on the conversational moment.
2. Filter `images` whose `tags` contain that mood. Read each candidate's `vibe` and pick the best fit (or random if equally fitting).
3. **You only Read the image.** The hook picks the sound automatically:
   - If `silent: true` → no sound, image only.
   - If `lock_sound` set → that sound plays.
   - If `preferred_sounds` set → 80% pick from there, 20% tag overlap.
   - Otherwise → random pick from non-locked, non-standalone sounds whose tags overlap.
4. **Cooldown (your job):** track the last 3 image slugs fired this session. Don't repeat. If everything's on cooldown, pick from another related mood.

**Sound-only fire:**
1. Pick a mood tag.
2. Filter `sounds` whose `tags` contain that mood AND `locked != true`. (Standalone sounds — `standalone: true` — are ESPECIALLY appropriate here; they're built for this.)
3. Read the `vibe` and pick. Run `Bash afplay <absolute sound path> &`. The `&` is required for background play.
4. Same cooldown idea (last 3 sound slugs).

Variety is the point: don't keep re-picking fahhh / bruh. Rotate.

## How to emit memes

**Image (with auto-paired sound):**
- Write one short text line, then emit `Read <absolute image path>`, then write one short text line. The hook plays the sound. Done.
- **Multiple images in one response are fine** — repeat the text-Read-text pattern. The intervening text breaks the UI's tool-call grouping, so each image renders inline.

**Sound only:**
- Emit `Bash afplay <absolute sound path> &` — the `&` is required for background play. These can mix freely with any other tool calls; they don't render visually.

**Variety rule:** never reuse the same image or sound slug within a single response. Rotate.

**Never** pair `Read <image>` with `Bash afplay <sound>` for the same fire — the hook handles the paired sound automatically. (Bash afplay is for sound-only fires, separate from any image.)

## Critical rendering rule

The Claude Desktop chat UI inlines an image **as long as the `Read` tool call is not visually grouped with other tool calls in the same UI block**. Grouping collapses the image into a "Ran a command, read a file" dropdown.

The reliable way to keep `Read` un-grouped — proven through testing — is to wrap it with one short line of text before AND one short line of text after. Examples of separator text: "Here you go:", "Behold:", "👻", "Skeleton time.". The text breaks the UI's batching logic and the image renders inline.

The skill invocation itself counts as a tool call, so a bare `Read` would batch with it and collapse. **Always use the text-Read-text pattern.**

**Multiple images in one response:** repeat the pattern — `text → Read → text → Read → text`. Each Read is separated by text, so each renders inline independently. Do NOT cluster `Read → Read → Read` without text between them; that batches.

## Detecting the surface

The `UserPromptSubmit` hook auto-detects CLI vs Desktop mode and tells you which image-emit pattern to use in the FIRE reminder. The mode is in the reminder header (`(mode: cli)` or `(mode: desktop)`). Trust it.

**Detection logic (in `remind-fire.sh`):**
1. Manual override via `CLAUDE_BRAINROT_MODE=cli|desktop` env var.
2. Else if `$TERM_PROGRAM` is set → CLI mode (terminal emulator detected).
3. Else default to Desktop mode.

**Mode-specific image emit:**
- **Desktop:** `text → Read <abs_path> → text`. Renders inline.
- **CLI:** `Bash <SKILL_DIR>/scripts/show.sh <abs_image_path>`. The script opens the image briefly (~3s, configurable via `CLAUDE_BRAINROT_SHOW_SECONDS`) then auto-closes via `qlmanage` (macOS) / `feh` (Linux). It backgrounds itself so your response continues immediately.

**The PostToolUse hook listens on BOTH Read and Bash** — so whether you Read an image (Desktop) or invoke `show.sh` with the image path (CLI), the hook extracts the path and fires the paired sound automatically. Never manually pair `afplay` with an image emit.

## How the sound-pairing hook works

The hook script at `<SKILL_DIR>/scripts/play-paired-sound.sh` receives the Read tool input as JSON on stdin and:
1. Bails if the path is not under any `.claude/skills/claude-brainrot/images/`.
2. Resolves the image's slug from the basename, looks it up in `catalogue.json`.
3. Selection priority:
   - `silent: true` → exit, no sound.
   - `lock_sound` → use that sound.
   - `preferred_sounds` → 80% pick from those, 20% tag overlap.
   - else → random pick from non-locked, non-standalone sounds whose tags overlap the image's tags.
4. Plays the chosen sound in the background (detached, cross-platform).

The hook command in this skill's frontmatter resolves to `${CLAUDE_PROJECT_DIR}/.claude/skills/claude-brainrot/scripts/play-paired-sound.sh` — dynamic to whatever project Claude Code is running in, as long as the skill is installed at `<project>/.claude/skills/claude-brainrot/`.
