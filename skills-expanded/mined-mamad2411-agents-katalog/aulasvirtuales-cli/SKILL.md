---
name: aulasvirtuales-cli
description: Use when the user explicitly wants to run CLI commands for UTN FRBA Moodle virtual classrooms - downloading resources with conversion/OCR, managing authentication, or configuring the tool. Prefer the /aulasvirtuales MCP skill for general queries; use this CLI skill when the user needs file conversion (--to, --ocr), bulk downloads, or CLI-specific features.
allowed-tools: Bash Read Grep
license: MIT
---

# aulasvirtuales CLI

A CLI tool to interact with UTN FRBA's Moodle platform. Installed as `aulasvirtuales` command.

**Always run commands directly** (e.g. `aulasvirtuales courses`), never with `uv run`.

## Core Agent Behaviors

When interacting with this CLI on behalf of the user, you MUST follow these conversational rules:
1. **Default to Native Conversion; Offer OCR Only When It Fits**: When you're asked to download and convert a document to Markdown, default to native parsing (`--to md`, powered by `pdf-inspector` for PDFs and `mammoth` for DOCX — fast, local, no LLM). Only suggest `--ocr` if the user explicitly mentions it, if the file is an image, or if there's reason to believe the PDF is scanned. The CLI runs a smart classifier gate: if you pass `--ocr` on a text-based PDF it will refuse and tell the user to use `--to md` or add `--force-ocr`. Do **not** add `--force-ocr` just to silence that error; only use it when the user has explicitly asked to OCR anyway.
2. **Offer to Clean Up**: Once your main task is fully completed and all demanded output has been delivered to the user, politely ask the user if they would like you to clear trailing temporary downloads by running `aulasvirtuales clear-downloads -y` so their disk doesn't fill up.

## Authentication

- `aulasvirtuales login` — prompts for username/password, stores session in OS keychain
- `aulasvirtuales logout` — removes credentials from keychain
- `aulasvirtuales status` — shows if logged in and session active
- Session auto-renews using stored credentials if expired

## Commands

### `aulasvirtuales courses`

Lists enrolled courses. Output: ID, Name.

### `aulasvirtuales resources <course_id>`

Lists sections and resources in a course. Output: ID, Type, Name.

Resource types: File, Folder, Forum, Assignment, Quiz, Link, Text, Page. Only File and Folder are downloadable.

### `aulasvirtuales download <course_id> <resource_id> [OPTIONS]`

Downloads a resource (File or Folder).

```bash
aulasvirtuales download 3641 106231
aulasvirtuales download 3641 106231 --to pdf
aulasvirtuales download 3641 106231 --to md
aulasvirtuales download 3641 106231 -o ~/notes
aulasvirtuales download 3641 106231 -o ~/notes/resumen.pdf
```

Options:

- `--to FORMAT` — Convert after download. Supported: `.docx` -> `pdf`, `.pdf` -> `md`, `.docx` -> `md` (chains docx->pdf->md), `.pptx` -> `pdf`, `.pptx` -> `md` (chains pptx->pdf->md). `.pptx` conversions require LibreOffice installed. No conversion if already in target format.
- `-o, --output PATH` — Destination directory or file path (default: `~/aulasvirtuales` or configured dir). File extension = full file path; no extension = directory.
- `--ocr` — Use a vision LLM to extract text via OCR instead of the default converter. Supports `.pdf`, `.docx`, `.pptx`, and images (`.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.tiff`, `.webp`). Requires `uv sync --extra full`. When `--ocr` is used, `--to` defaults to `md`. Valid OCR output formats: `md`, `txt`. On PDFs, `--ocr` passes through a classifier gate: text-based PDFs are rejected with a suggestion to drop `--ocr`, mixed PDFs transparently use a hybrid pipeline (native text + vision OCR on scanned pages only).
- `--force-ocr` — Bypass the classifier gate and run vision OCR even on text-based PDFs. Only use when the user has explicitly asked to OCR a text-based PDF despite the warning. Ignored when `--ocr` is not set.
- `--ocr-provider PROVIDER` — Override the configured OCR provider for this command (`ollama` or `openrouter`).
- `--ocr-model MODEL` — Override the configured OCR model for this command.

```bash
# OCR examples
aulasvirtuales download 3641 106231 --ocr                          # OCR to markdown (gate may refuse text-based PDFs)
aulasvirtuales download 3641 106231 --ocr --to txt                  # OCR to plain text
aulasvirtuales download 3641 106231 --ocr --force-ocr               # bypass the gate (user explicitly asked)
aulasvirtuales download 3641 106231 --ocr --ocr-provider ollama --ocr-model llava  # one-off override
```

### `aulasvirtuales download-all <course_id> [OPTIONS]`

Downloads every File and Folder from a course. Same options as `download` (including `--ocr`, `--force-ocr`, `--ocr-provider`, `--ocr-model`). The classifier gate runs per file, so a mixed batch of text-based and scanned PDFs is handled correctly without manual intervention.

```bash
aulasvirtuales download-all 3641
aulasvirtuales download-all 3641 --to pdf -o ~/study/math
```

### `aulasvirtuales clear-downloads [OPTIONS]`

Clears all downloaded files from the configured default download directory.

Options:

- `--force, -y` — Skipt the explicit confirmation prompt.

```bash
aulasvirtuales clear-downloads
aulasvirtuales clear-downloads -y
```

### `aulasvirtuales events [course_id]`

Shows upcoming events and deadlines. Omit course_id for all courses.

```bash
aulasvirtuales events
aulasvirtuales events 29595
```

### `aulasvirtuales grades <course_id> [OPTIONS]`

Shows the grading table and feedback for a course (like assignments, quizzes, and course totals).

Options:

- `--with-status` — Fetches the submission status for each assignment by scraping individual assignment pages. Shows whether each task was submitted (e.g., "Enviado para calificar", "Todavía no se han realizado envíos"). Slower due to additional HTTP requests per assignment.
- `--with-comments` — Iterates through assignments to extract specific text grades (e.g., "Entrega Muy bien") and fetches internal dynamic submission comments left by professors. Slower runtime due to additional HTTP requests.

```bash
aulasvirtuales grades 3641
aulasvirtuales grades 3641 --with-status
aulasvirtuales grades 3641 --with-comments
```

### `aulasvirtuales forums <course_id>`

Lists forums in a course. Output: ID, Name.

### `aulasvirtuales discussions <forum_id> [-n LIMIT]`

Lists discussion threads in a forum. Default limit: 10.

### `aulasvirtuales posts <discussion_id>`

Shows all messages in a discussion thread.

### `aulasvirtuales config [OPTIONS]`

View or update CLI configuration.

- `-d, --download-dir PATH` — Set default download directory.
- `--ocr-provider PROVIDER` — Set OCR provider (`ollama` or `openrouter`).
- `--ocr-model MODEL` — Set OCR model name.
- `--openrouter-api-key KEY` — Set OpenRouter API key (stored in provider config).
- `--ollama-base-url URL` — Set Ollama base URL (default: `http://localhost:11434`).

```bash
aulasvirtuales config --ocr-provider ollama --ocr-model llava
aulasvirtuales config --ocr-provider openrouter --ocr-model google/gemini-flash-1.5 --openrouter-api-key sk-...
aulasvirtuales config   # show current config
```

## Typical Workflows

### Download and convert a file

```bash
aulasvirtuales courses                          # find course ID
aulasvirtuales resources 3641                   # find resource ID
aulasvirtuales download 3641 106231 --to pdf -o ~/notes
```

### Check what's due soon

```bash
aulasvirtuales events
```

### Read announcements

```bash
aulasvirtuales forums 3641                      # find forum ID
aulasvirtuales discussions 23491 -n 5           # find discussion ID
aulasvirtuales posts 406838                     # read the thread
```

### Download with OCR

```bash
aulasvirtuales config --ocr-provider ollama --ocr-model llava   # configure once
aulasvirtuales download 3641 106231 --ocr                       # OCR to markdown (gate may refuse text-based PDFs)
aulasvirtuales download 3641 106231 --ocr --force-ocr           # user explicitly wants OCR despite the gate warning
aulasvirtuales download-all 3641 --ocr --to txt                 # OCR all files to plain text (gate runs per file)
```

## Important Notes

- All IDs are integers from previous command outputs.
- Downloaded files default to `~/aulasvirtuales` or the directory set via `aulasvirtuales config -d`.
- If a `--to` conversion fails, the CLI shows which extra to install.
- OCR (and native document conversion) require `uv sync --extra full`. For `.pptx` OCR, also needs LibreOffice installed on the system.
- The OCR classifier gate uses `pdf-inspector` (shipped in the `full` extra). If the gate is ever skipped because the extra isn't installed, the CLI falls back to the plain vision pipeline and prints a note.
- Symmetric warning: running `--to md` on a scanned PDF prints a warning and suggests `--ocr` instead of producing an empty file.
- OCR provider config is stored in `~/.config/aulasvirtuales/config.json` under `ocr.<provider>` as kwargs passed directly to the LangChain class (`ChatOllama`, `ChatOpenRouter`).
- Session tokens persist in the OS keychain. Auth is automatic.
