---
name: video-prompt
description: "Write video prompts in the project's brand, sized and timed for each platform, ready for any video generator. Triggers: 'write a video prompt', 'prompt for a reel', 'make a prompt to animate this photo', 'prompt for a product video', 'give me a prompt I can paste into Kling', 'how long should this reel be', 'video prompt'. Reads the project's own brand file for palette, look, motion, tone and a don't list, and never stores brand values itself. Writes the prompt, a JSON with size, ratio, length and a suggested model, and on request short paste steps for a web tool. It never generates a video and never spends credits. Needs Node 18 or newer."
license: MIT
compatibility: "Requires Node 18 or newer. Run scripts/setup-deps.sh (or scripts/setup-deps.ps1 on Windows) to check for it and install it if missing. Works offline. Writes only to .prompts/ in the folder it runs from, or to --out."
metadata:
  author: itqanlab
  version: 1.0.1
  category: media
  short: "Brand-aware video prompts, sized and timed per platform"
  starter: "write a prompt for a 7 second reel of this product"
---

# Video Prompt

Writes the prompt for a short video: in the project's brand, in the right size and length for the platform, with the motion spelled out and a don't list. It writes text only. It never generates a video, so it costs nothing.

The prompt then goes to a video generator. When the `higgsfield-studio` skill is installed, hand it over there: it quotes the price before anything is spent, and video is where credits go fastest. Otherwise the user pastes it into any web tool.

## Who you are doing this for

Assume the person asking has never opened a terminal. **You run the commands; they never do.** Show them the prompt in plain words and say what happens next. If they are clearly comfortable with a terminal, let them drive.

## Before anything else: check the dependencies

```
sh scripts/setup-deps.sh --check
```

Non-zero exit means Node is missing or older than 18. `sh scripts/setup-deps.sh` (Windows: `.\scripts\setup-deps.ps1`) prints the right install command for the machine and asks before running it; `--yes` skips the question.

## Commands

```
node scripts/prompt.mjs --subject "..." [--type turntable] [--platform instagram_reel] [--variant square]
     [--size 1080x1920] [--seconds 7] [--reference] [--people] [--scene "..."] [--motion "..."]
     [--brand FILE] [--brand-mode full|minimal|none] [--paste "Tool name"] [--out DIR] [--force]
node scripts/prompt.mjs sizes        every platform, variant, size and accepted length
node scripts/prompt.mjs brand        which brand file is used and what was read from it
```

- `--subject` is what the video shows, in plain words.
- `--type` is the shot: `turntable` (default), `hero-reveal`, `editorial`, `detail` or `animate-still`. See `references/prompt-craft.md`.
- `--platform` and `--variant` set size and default length from the table below. `--size WxH` sets the size directly.
- `--seconds` sets the length. A length the platform does not accept is refused.
- `--reference` when there is a photo of the real subject (image to video). `animate-still` always uses one.
- `--motion` replaces the shot's motion line. The brand's own motion rules are still added after it.
- `--paste "Kling"` also writes `PASTE.md`: short, general steps for pasting the prompt into that web tool.

Each run writes a folder with `prompt.txt` (the prompt alone, ready to copy) and `prompt.json` (the prompt, size, ratio, length, don't list, the brand file used, and a suggested Higgsfield model with ratio, clip length, number of clips and a cheaper draft model).

## Platforms

| Platform | Variants | Size | Default length |
| :-- | :-- | :-- | :-- |
| `instagram_reel`, `facebook_reel`, `tiktok`, `youtube_short` | | 1080x1920 | 7 to 10 s |
| `instagram_story`, `facebook_story` | | 1080x1920 | 7 s |
| `instagram_post` | `portrait` (default), `square` | 1080x1350, 1080x1080 | 7 s |
| `facebook_feed`, `linkedin_post` | `square` (default), `landscape` | 1080x1080, 1280x720 or 1920x1080 | 10 s |
| `youtube` | | 1920x1080 | 10 s |
| `product_page` | | 1080x1080 | 5 s |

`node scripts/prompt.mjs sizes` shows the exact length range each one accepts.

## The brand

The brand comes from a Markdown file the project owns: `--brand FILE`, else `BRAND_FILE`, else `brand.md`, `BRAND.md`, `brand/brand.md` or `docs/brand.md` in the folder the command runs from. Its sections (palette, look, studio, motion, tone, don't) are found by their headings. The full contract and an example are in `references/brand-file.md`.

- No brand file is fine: the prompt carries no brand style, and the tool says so. Offer to write one with the user. For video, also ask how things should move: pace, camera, cuts.
- Never invent brand values, and never copy them into this skill. Read the file every time.
- `--brand-mode minimal` keeps only the look and the don't list. `none` ignores the brand.

## Handing it to Higgsfield

`prompt.json` has a `higgsfield` block: the model, a cheaper draft model, the aspect ratio, the length of each clip and how many clips. With the `higgsfield-studio` skill installed, use its `create` command with `--prompt-file` pointing at `prompt.txt`, the model, `--aspect_ratio` and `--duration`, and `--image` for a reference. It quotes the price first. Make the draft, check the motion, then render the final once.

## Rules

- **Read the brand file every time.** Never write a brand value from memory.
- **Short first.** 5 to 10 seconds fails less and costs less. A longer piece is several clips.
- **One prompt, then look.** Fix with one change at a time (`references/prompt-craft.md` lists the usual fixes).
- **Respect the log.** Exit code 3 means a similar prompt was already written in this project. Show the user the earlier one. Use `--force` only when they want a new one.
- **Disclosure.** Generated video counts as AI-generated material on most platforms. Tell the user to use each platform's AI label when they publish.

## Updates

This skill is versioned. Its version is `metadata.version` in the header of this file. `CHANGELOG.md` in this folder lists what changed in each version, newest first.

To check for a newer version, open the address on the `Latest:` line of `CHANGELOG.md` and compare its top version with the installed one. If the newer one is ahead, read every entry between the two and tell the user what changed before anything is updated. A `Breaking` section means the user has to do something. To update, reinstall the skill from its source repository, the same way it was installed.
