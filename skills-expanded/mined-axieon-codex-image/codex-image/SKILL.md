---
name: codex-image
description: Generate or edit raster images (sprites, icons, illustrations, textures, backgrounds, mockups, photos) by delegating to the OpenAI Codex CLI and its built-in $imagegen tool (gpt-image-2), on the user's ChatGPT plan with no API key. Use whenever the user asks for an image file, or asks to change an existing PNG/JPG. Not for SVG, diagrams, or UI that is better built in code.
---

# Image generation through Codex

The Codex CLI, signed in with a ChatGPT plan (`codex login`), has a built-in image tool that needs
no API key. Each image takes about 1 minute and counts against the user's Codex limits (a 5-hour
and a weekly window), so generate only what was asked for. Making images through Codex costs
Claude's own limits almost nothing.

## Generate: always through the script

The script in `scripts/` next to this file (this skill's base directory) reads the Codex limits,
runs Codex, checks the file landed, reads the limits again and records what the image cost. It
always tries, however high the limits read: a window at 95% may still hold one more image.

On Windows, the PowerShell script (from the Bash tool too):

```
powershell -NoProfile -ExecutionPolicy Bypass -File '<skill dir>/scripts/codex-image.ps1' -Prompt '<prompt>' -OutDir '<folder>' -Name '<name>.png'
```

On macOS and Linux, the bash script (needs `jq` 1.6 or newer):

```bash
bash '<skill dir>/scripts/codex-image.sh' --prompt '<prompt>' --out-dir '<folder>' --name '<name>.png'
```

Both take the same options and print the same JSON:

- `-PromptFile` / `--prompt-file <path>` instead of the prompt for long prompts or ones with quotes
  (write the prompt to a UTF-8 file first).
- `-Edit` / `--edit <image>` attaches an image to change: the prompt says what to change and what
  must stay.
- Use a tool timeout of at least 300000 ms. It prints one JSON line; exit 0 done, 1 failed.
- It never overwrites a file: pick a versioned name (`hero-v2.png`) when one exists.
- One image per call. For several different assets, run separate calls, one after another: runs
  that overlap can't tell their costs apart (`overlapped: true`, no `cost`).

### The limits: report them, never stop on them

`-Check` / `--check` costs nothing and answers `status` (`ok`, `high` from 80%, `spent` from 95%),
each window's `used` and `resetsInMinutes`, the average `perImage` cost and `imagesLeft`. Run it
before a batch (2+ images) so you can say up front how it stands ("Codex 5-hour at 85%, resets in
1h 10m, about 6 images fit"), then go ahead: a high or spent reading is information, not a reason
to stop.

- **An image fails** (exit 1): tell the user why (`error`, and `log` for detail) and when to try
  again from `nextReset` ("Codex's 5-hour limit is used up (96%); it resets in 1h, at 04:02").
  `limitHit: true` means Codex said a limit stopped it; then stop the rest of the batch too, and
  offer to finish it after the reset. Other failures: retry once, then report.
- **After each image**, report what it cost when the JSON has `cost` ("1% of the 5-hour window,
  about 78 more fit"). The average needs a few images before `imagesLeft` appears.
- `known: false` means the limits could not be read (Codex is signed out, or too old to report
  them): generation still works, with no numbers; say so once.
- `recovered: true` means Codex kept the image only in its own folder and the script copied this
  run's image from there (the newest one, when it could not tell the run's session): check closely
  that it is the image you asked for.

### When the setup is missing

These need the user; tell them the command rather than working around it.

- `codex not found`: install the Codex CLI (`npm i -g @openai/codex` or `brew install codex`),
  then `codex login` with a ChatGPT account.
- Codex says it is not signed in: `codex login`.
- `jq not found` or `jq 1.6 or newer needed` (macOS/Linux): `brew install jq` or `sudo apt install jq`.

## Write a good prompt

Spell out: subject, style/medium, aspect ratio (square, 3:2, 16:9), composition, color palette,
background (say "transparent background" when the asset needs alpha), exact text in quotes if any,
and what to avoid ("no text, no watermark"). For game assets, name the use (e.g. "inventory icon
for a survival game").

Ask for a shape, not exact pixels: the tool picks its own size (about 1672x941 for 16:9), and if
you name exact pixels Codex just resizes the file, which adds no detail. Name pixels only when the
project needs that exact size. When a project has its own prompts (e.g. a design doc), copy them
word for word rather than paraphrasing.

## After every call

1. Open the image with the Read tool and look at it: subject, style, text, background.
2. If it is off, re-run once with a single targeted change to the prompt. After 3 failed attempts,
   show the user the best result and ask how to proceed.
3. Tell the user the saved path (and the cost, above).

## Without the script

The raw call, if the script itself fails. Pipe the prompt in so quotes survive the shell; in
Windows PowerShell set `$OutputEncoding = [Text.UTF8Encoding]::new($false)` first.

```bash
printf '%s' '$imagegen <prompt>. Save the final image into the current working directory as <name>.png. Reply with only the saved file path.' |
  codex exec --skip-git-repo-check --enable image_generation -s workspace-write -C '<folder>' -
```

On Windows, if `codex` is not found, try `"$env:LOCALAPPDATA\Programs\OpenAI\Codex\bin\codex.exe"`.
A missing file's original is under `~/.codex/generated_images/<session>/` (the newest PNG).
