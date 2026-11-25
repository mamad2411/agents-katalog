---
name: optimize-assets
description: Optimize (shrink) image assets in a directory — resize oversized PNG/JPG and re-encode them IN PLACE (same filenames, so zero <img> reference changes), idempotently, via sharp. Opt-in `--audio`/`--video` does the same for MP3/MP4 via ffmpeg. Use when the user says "optimize/compress the assets", "procesa/optimiza los assets", "reduce image weight", "las imágenes pesan mucho", "shrink public/assets", "optimiza los vídeos/audios", "el mp4 pesa mucho", or asks to cut the size of an image, audio or video folder. Project-AGNOSTIC and portable — the whole skill folder can be copied to any project or agent; the only dependency is `sharp` (plus `ffmpeg` on PATH for audio/video). This skill is the TOOL only; wiring it into a build/deploy pipeline is a separate task.
---

# optimize-assets

Idempotent, project-agnostic image optimizer. It **resizes** oversized raster
images and **re-encodes** them **in place** (same filename → the `/assets/...`
URLs and every `<img src>` stay identical; only the bytes shrink). A per-file
content-hash manifest makes it a **no-op on re-run** and processes only NEW or
CHANGED files. It **never enlarges** a file (writes only when the result is
smaller).

The tool is `optimize-assets.mjs`, bundled in this folder. Run it with `node`.
When installed as a plugin, the script lives at
`${CLAUDE_PLUGIN_ROOT}/skills/optimize-assets/optimize-assets.mjs` — the
`SCRIPT` shorthand below stands for that path (or wherever you copied the folder,
e.g. `.claude/skills/optimize-assets/optimize-assets.mjs`).

## When to use

- The user asks to optimize / compress / shrink a folder of images.
- A folder of vendored/design PNG-JPG is heavy and served as-is (no `next/image`).
- The user asks the same for MP3/MP4 — add `--audio` / `--video` (needs `ffmpeg`).

Do NOT use it to convert formats app-wide or rewire `<img>` to `next/image` —
this keeps the same files, just lighter.

## How to run

```bash
# 1. ensure the one dependency exists (once per project)
npm i -D sharp            # or: pnpm add -D sharp

# 2. preview first — writes nothing, prints projected savings
node "$CLAUDE_PLUGIN_ROOT/skills/optimize-assets/optimize-assets.mjs" <dir> --dry-run

# 3. optimize in place (conservative defaults: cap 1600px, quality 82)
node "$CLAUDE_PLUGIN_ROOT/skills/optimize-assets/optimize-assets.mjs" <dir>
```

Always show the `--dry-run` projection and confirm before the real pass — these
are usually a designer's assets and fidelity matters.

Every run ends with a **before → after total** line for the optimized assets,
e.g. `shrank 12 asset(s): 24.8MB → 9.1MB (−63%, saved 15.7MB)`. Relay that line
to the user verbatim so they see the weight cut. If nothing changed it prints
`nothing to optimize — N file(s) already minimal or skipped`.

### If it errors out

The tool fails loudly with an actionable message (never a stack trace); surface
it to the user as-is:

- **Missing dependency** (exit 1): `'sharp' is not installed. Run: npm i -D sharp` → run that, then retry.
- **Missing ffmpeg** (exit 1, only with `--audio`/`--video`): `'ffmpeg' is not installed or not on PATH` → tell the user to install it (`winget install Gyan.FFmpeg` · `brew install ffmpeg` · `apt install ffmpeg`); do NOT try to work around it.
- **Bad usage** (exit 2): unknown flag, a value-flag with no value, more than one directory, or an out-of-range number (`--quality` must be 1–100, `--max`/`--min-kb` ≥ 0) print the offending option plus the help text.
- **Not a directory** (exit 2): the given path isn't a folder.

### Options

| flag | default | meaning |
|---|---|---|
| `<dir>` | cwd | target directory (recursive) |
| `--max <px>` | 1600 | cap the longest side, keep aspect (`0` = no resize) |
| `--quality <n>` | 82 | encode quality 1–100 |
| `--ext <csv>` | `png,jpg,jpeg` | extensions to process |
| `--ignore <csv>` | — | extra directory names to skip (added to the built-in ignore list) |
| `--min-kb <n>` | 8 | skip files smaller than this |
| `--no-palette` | off | PNG: skip palette quantization (bigger, max fidelity — use if you see banding) |
| `--webp` | off | ALSO write a sibling `<name>.webp` (does not replace the source) |
| `--audio` | off | also process `.mp3` (needs `ffmpeg`) — LAME VBR, drops cover art; already-lean files are remuxed, never re-encoded |
| `--video` | off | also process `.mp4` (needs `ffmpeg`) — H.264, keeps resolution + audio track |
| `--manifest <path>` | `<dir>/../.optimize-assets.json` | idempotence ledger |
| `--concurrency <n>` | 8 | parallel workers |
| `--force` | off | reprocess everything (ignore the manifest) |
| `--dry-run` | off | report only |
| `--self-test` | — | run the built-in correctness check and exit |

## Audio & video

Opt-in only — never add `--audio`/`--video` unless the user asked for audio or
video. Requires `ffmpeg` on PATH. MP3 is re-encoded to LAME VBR with embedded
cover art dropped (ID3 tags kept); MP4 is re-encoded to H.264 with the audio
track copied untouched and `+faststart` applied. `--max` does NOT apply to
media — videos keep their resolution on purpose.

Say this plainly when the user asks about quality: an MP3 re-encode is
lossy → lossy. That is why the tool reads the source bitrate first (`ffprobe`)
and, when a file is already at or below the target, remuxes it with `-c:a copy`
instead of encoding — cover art still dropped, audio bit-identical. Only
genuinely bloated files (320 kb/s and up) are re-encoded.

`--video` has NO such guard — H.264 has no readable "already optimized" number,
so every MP4 is re-encoded and the only safety net is write-only-if-smaller.
Always show the `--dry-run` first for video, and warn against running it
repeatedly with different `--quality` values on footage the user cares about.

## Fidelity

Defaults are conservative but **not lossless** (resize + re-encode). On the
FIRST bulk pass, spot-check a few of the heaviest outputs. If a gradient/neon
render shows banding, re-run that folder with `--no-palette` or a higher
`--quality`. The manifest lets you re-run safely — only files whose bytes
changed get reprocessed.

## Safe to run anywhere

`walk` never descends into dot-directories (`.git`, `.next`, …) or the built-in
ignore list (`node_modules`, `dist`, `build`, `out`, `coverage`, `vendor`,
`tmp`, `target`). So pointing it at a project root — or running it with no dir —
won't churn through dependency or build-output images. Add project-specific
skips with `--ignore <csv>`. Still, prefer pointing it at the actual assets
folder (`public/assets`) for speed and intent.

## Idempotence & manifest

Each processed file is recorded by content hash in `--manifest`. Re-runs skip
unchanged files. A designer replacing an asset (new bytes) is reprocessed
automatically. Keep the manifest OUT of any folder that gets deployed/synced
(the default puts it one level above the target dir).

## Verify the tool itself

```bash
node "$CLAUDE_PLUGIN_ROOT/skills/optimize-assets/optimize-assets.mjs" --self-test
```
Generates a synthetic 3000px PNG, optimizes it, and asserts it shrank, was
resized, and that a second run does not rewrite it.

## Portability

Self-contained: copy this folder into another repo (or hand it to another AI
agent). The only runtime requirement is `sharp`. No repo paths or framework
assumptions are baked in — everything is a CLI flag.

## Author

Pedro Plasencia — https://programacion-es.dev
