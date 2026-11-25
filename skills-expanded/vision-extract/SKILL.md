---
namespace: aiwg
platforms: [all]
name: vision-extract
description: Transcribe scanned page images into per-page + combined Markdown source text for induction, via a provider-neutral vision adapter (codex CLI or a generic command template for Claude/any vision tool). Resumable, with retry + `# Page N` validation + extraction-status markers; optionally rasterizes a PDF to page PNGs first. Runs via `aiwg corpus vision-extract`.
commandHint:
  argumentHint: "--slug SLUG [--rasterize PDF [--dpi N]] [--provider codex|command] [--command TMPL] [--start N --end N] [--model M] [--retries N] [--force]"
  allowedTools: Read, Bash, Write
  model: haiku
  category: research-acquisition
  modelRole: efficiency
  modelTier: economy
---

# Scanned-Page Vision Extraction

Transcribe a directory of scanned page PNGs into Markdown source text — the
acquisition step for inducting scanned books / pages. Provider-neutral: the
vision call is a pluggable adapter, not hardcoded to one CLI.

## How to run

```bash
# Pages already exist at .aiwg/research/sources/images/<slug>/pages/
aiwg corpus vision-extract --slug tufte-1983-visual-display --provider codex

# Rasterize a PDF to page PNGs first (poppler pdftoppm), then transcribe
aiwg corpus vision-extract --slug my-book --rasterize sources/pdfs/my-book.pdf --dpi 200 --provider codex

# Provider-neutral: any vision CLI via a wrapper script (see below)
chmod +x ./vision.sh
aiwg corpus vision-extract --slug my-book \
  --provider command \
  --command './vision.sh {image} {prompt_file} {out}'

# Resume (skips pages already marked complete); --force re-does them
aiwg corpus vision-extract --slug my-book --start 20 --end 40
aiwg corpus vision-extract --slug my-book --force
```

Save this wrapper as `vision.sh`; it receives the image, prompt file, and output
paths as separate arguments:

```sh
#!/bin/sh
claude -p "$(cat "$2")" --image "$1" > "$3"
```

Outputs to `.aiwg/research/sources/text/<slug>-vision/`: per-page
`pages/page-NNN.md`, combined `<slug>-vision.vision.md` + stripped `.txt`, `run.log`.

## Adapters (provider-neutral)

| `--provider` | Vision call |
|---|---|
| `codex` (default) | `codex exec --sandbox read-only --image … --output-last-message` (set `AIWG_CODEX_BIN`/`--model` as needed) |
| `command` | a shell template (`--command` or `AIWG_VISION_COMMAND`) with `{image}` / `{prompt_file}` / `{out}` placeholders — wire any vision CLI (Claude, a custom script). The command writes the transcription to `{out}` (or stdout). |

Both require a vision-capable model to be reachable; `needs-infrastructure`.

Command templates must use unquoted, unescaped placeholders: `{image}` → `"$1"`,
`{prompt_file}` → `"$2"`, `{out}` → `"$3"`. Paths are passed as separate shell
arguments; `AIWG_VISION_IMAGE`, `AIWG_VISION_PROMPT_FILE`, and `AIWG_VISION_OUT`
are also exported. For example: `vision-cli --image {image} --prompt-file {prompt_file} > {out}`.
Templates may expand only `$1`, `$2`, `$3`, `$AIWG_VISION_IMAGE`,
`$AIWG_VISION_PROMPT_FILE`, and `$AIWG_VISION_OUT`, also in braced form
(`${1}`, `${AIWG_VISION_OUT}`, etc.). All other `$` parameter/variable expansions are rejected,
including shell names (`$SHELL`), `$IFS`, special parameters, arithmetic, and braced
operators such as `${1:-fallback}`. A `$` inside single quotes is literal text and allowed.
Keep the provided references quoted when using them as data arguments.
Command substitution (`$(`), backticks, `eval`, nested shell invocations with `-c`
(including redirections and `env … sh -c`), here-documents and here-strings (`<<`),
`#` outside single quotes, and backslash-newline line continuations (anywhere, regardless of quoting) are rejected. Put complex logic in a wrapper script
that receives the paths as data arguments. Templates are trusted executable code
and must not re-parse path values as shell source. Validation is defense in depth;
keep path arguments quoted in the wrapper, as in the example above.

## Contract preserved from the source script

- **Strict transcription prompt**: reading order, `[?]` / `[unreadable]` markers, figure/chart text markers, no summarizing; must start exactly `# Page N`.
- **Validation**: output is accepted only if it starts with `# Page N`; otherwise retried (`--retries`) then written with an `<!-- extraction-status: failed -->` marker.
- **Resumable**: pages with `<!-- extraction-status: complete -->` are skipped unless `--force`.
- **Combine**: all per-page files concatenated into the combined Markdown + a comment-stripped `.txt`.

## PDF → page images

`--rasterize <pdf>` renders the PDF to `page-NNN.png` via poppler `pdftoppm`
(macOS: `brew install poppler`; Debian/Ubuntu: `apt install poppler-utils`) at
`--dpi` (default 200), into the slug's images dir. Omit it when page PNGs already
exist (the script's original input contract).

## Triggers

- "transcribe scanned pages / book"
- "vision OCR a PDF"
- "extract text from page images"

## Notes

- TS-native: `src/artifacts/corpus-tools/vision-extract.ts` — port of section9
  `codex_vision_extract_pages.sh`, generalized off the hardcoded `codex` CLI.
- Sits alongside `research-acquire` / `research-acquisition-agent` (PDF/metadata)
  and the media-transcript tooling (audio/video) as the scanned-page acquisition path.
