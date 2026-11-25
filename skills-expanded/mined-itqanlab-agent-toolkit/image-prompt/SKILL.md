---
name: image-prompt
description: "Write image prompts in the project's brand, sized for each platform, ready for any image generator. Triggers: 'write an image prompt', 'prompt for an Instagram post image', 'make a prompt for a product photo', 'give me a prompt I can paste into ChatGPT', 'brand prompt for this product', 'what size should this image be', 'image prompt'. Reads the project's own brand file for palette, look, tone and a don't list, and never stores brand values itself. Writes the prompt, a JSON with size, ratio and a suggested model, and on request short paste steps for a web tool. It never generates an image and never spends credits. Needs Node 18 or newer."
license: MIT
compatibility: "Requires Node 18 or newer. Run scripts/setup-deps.sh (or scripts/setup-deps.ps1 on Windows) to check for it and install it if missing. Works offline. Writes only to .prompts/ in the folder it runs from, or to --out."
metadata:
  author: itqanlab
  version: 1.0.1
  category: media
  short: "Brand-aware image prompts, sized for each platform"
  starter: "write a prompt for an Instagram portrait post of this product"
---

# Image Prompt

Writes the prompt for an image: in the project's brand, in the right size for the platform, with a don't list. It writes text only. It never generates an image, so it costs nothing.

The prompt then goes to an image generator. When the `higgsfield-studio` skill is installed, hand it over there: it quotes the price before anything is spent. Otherwise the user pastes it into any web tool.

## Who you are doing this for

Assume the person asking has never opened a terminal. **You run the commands; they never do.** Show them the prompt in plain words and say what happens next. If they are clearly comfortable with a terminal, let them drive.

## Before anything else: check the dependencies

```
sh scripts/setup-deps.sh --check
```

Non-zero exit means Node is missing or older than 18. `sh scripts/setup-deps.sh` (Windows: `.\scripts\setup-deps.ps1`) prints the right install command for the machine and asks before running it; `--yes` skips the question.

## Commands

```
node scripts/prompt.mjs --subject "..." [--type editorial] [--platform instagram_post] [--variant portrait]
     [--size 1080x1350] [--reference] [--people] [--headline "..."] [--scene "..."]
     [--brand FILE] [--brand-mode full|minimal|none] [--paste "Tool name"] [--out DIR] [--force]
node scripts/prompt.mjs sizes        every platform, variant, pixel size and ratio
node scripts/prompt.mjs brand        which brand file is used and what was read from it
```

- `--subject` is what the image shows, in plain words: "a tan leather tote bag".
- `--type` is the direction: `editorial` (default), `clean-studio`, `detail` or `branded-overlay`. See `references/prompt-craft.md`.
- `--platform` and `--variant` set the size from the table below. `--size WxH` sets it directly.
- `--reference` when the user has a photo of the real product to attach. The prompt then tells the model to keep the subject exactly and build a new scene.
- `--people` adds a person styled with the subject. `--headline` sets one short line of text on a `branded-overlay`.
- `--paste "ChatGPT"` also writes `PASTE.md`: short, general steps for pasting the prompt into that web tool.

Each run writes a folder with `prompt.txt` (the prompt alone, ready to copy) and `prompt.json` (the prompt, size, ratio, don't list, the brand file used, and a suggested Higgsfield model with its ratio and any crop needed).

## Platforms

| Platform | Variants | Size |
| :-- | :-- | :-- |
| `product_page` | | 2048x2048 |
| `instagram_post` | `portrait` (default), `square`, `landscape` | 1080x1350, 1080x1080, 1080x566 |
| `instagram_story`, `instagram_reel_cover` | | 1080x1920 |
| `facebook_post` | `square` (default), `landscape` | 1080x1080, 1200x630 |
| `facebook_story` | | 1080x1920 |
| `linkedin_post` | `square` (default), `landscape` | 1200x1200, 1200x627 |
| `x_post` | | 1600x900 |
| `pinterest_pin` | | 1000x1500 |
| `youtube_thumbnail` | | 1280x720 |

## The brand

The brand comes from a Markdown file the project owns: `--brand FILE`, else `BRAND_FILE`, else `brand.md`, `BRAND.md`, `brand/brand.md` or `docs/brand.md` in the folder the command runs from. Its sections (palette, look, studio, motion, tone, don't) are found by their headings. The full contract and an example are in `references/brand-file.md`.

- No brand file is fine: the prompt carries no brand style, and the tool says so. Offer to write one with the user. Ask for their colours, how their photos look, their tone, and what they never want.
- Never invent brand values, and never copy them into this skill. Read the file every time.
- `--brand-mode minimal` keeps only the look and the don't list. `none` ignores the brand.

## Handing it to Higgsfield

`prompt.json` has a `higgsfield` block: the model, the aspect ratio, the size to crop to when the model cannot make the exact ratio, and how to hand it over. With the `higgsfield-studio` skill installed, use its `create` command with `--prompt-file` pointing at `prompt.txt`, that model and ratio, and `--image` for a reference photo. It quotes the price first. Check the model's parameters there before guessing.

## Rules

- **Read the brand file every time.** Never write a brand value from memory.
- **One prompt, then look.** Make one image from it before writing variations. Fix with one change at a time (`references/prompt-craft.md` lists the usual fixes).
- **Respect the log.** Exit code 3 means a similar prompt was already written in this project. Show the user the earlier one. Use `--force` only when they want a new one.
- **Vary the type across a series,** so a feed does not repeat itself.
- **Disclosure.** Generated images count as AI-generated material on most platforms. Tell the user to use each platform's AI label when they publish.

## Updates

This skill is versioned. Its version is `metadata.version` in the header of this file. `CHANGELOG.md` in this folder lists what changed in each version, newest first.

To check for a newer version, open the address on the `Latest:` line of `CHANGELOG.md` and compare its top version with the installed one. If the newer one is ahead, read every entry between the two and tell the user what changed before anything is updated. A `Breaking` section means the user has to do something. To update, reinstall the skill from its source repository, the same way it was installed.
