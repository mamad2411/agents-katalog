---
name: uniparser-paper-markdown
description: Parse scientific papers, PDFs, document images, and public PDF URLs with UniParser into a Markdown paper file plus an images folder. Use when the user wants UniParser output where figures, charts, and extracted image assets are stored locally and linked from Markdown.
---

# UniParser Paper Markdown Skill

Parse local PDFs, document images, and public PDF URLs via UniParser, then write a paper Markdown file and a sibling `images/` folder. Agents should run the bundled CLI scripts rather than writing ad hoc SDK code.

## Installation

Install UniParser-Tools once into the same Python environment used to run the scripts:

```bash
pip install "git+https://github.com/dptech-corp/UniParser-Tools.git"
```

Manual verify:

```bash
python -c "import uniparser_tools; print('ok')"
```

## Configuration

API key lookup order:

1. Environment variable `UNIPARSER_API_KEY`
2. This skill's local `.env` file

Prefer the environment variable. Use `.env` only when the environment is unavailable in the current session.

Windows PowerShell:

```powershell
$env:UNIPARSER_API_KEY="your-api-key"
```

Local fallback:

```dotenv
UNIPARSER_API_KEY=your-api-key
```

## Usage

Run commands from this skill root directory, the folder containing `SKILL.md`.

Input flags, use one per run:

- Local PDF: `--file-path`
- Local image: `--image-path`
- Public PDF URL: `--pdf-url`

```bash
python scripts/parse_paper.py --file-path "/path/to/paper.pdf"
python scripts/parse_paper.py --image-path "/path/to/page.png"
python scripts/parse_paper.py --pdf-url "https://example.com/paper.pdf"
```

Optional flags:

```bash
python scripts/parse_paper.py --file-path "./paper.pdf" --output-dir "./results"
python scripts/parse_paper.py --file-path "./paper.pdf" --async
python scripts/parse_paper.py --file-path "./paper.pdf" --overwrite
```

Recovery for an existing server job:

```bash
python scripts/fetch_by_token.py --file-path "/path/to/paper.pdf"
python scripts/fetch_by_token.py --pdf-url "https://example.com/paper.pdf"
python scripts/fetch_by_token.py --token "existing-token"
```

## Output Contract

Default output directory: `~/Uni-Parser-Paper-Markdown/<source_stem>/`

Files written on success:

- `{stem}.md` - full paper Markdown text
- `images/` - all extracted base64 figure/chart/image assets materialized as files
- `pages_tree.json` - structured layout tree
- `formatted_meta.json` - metadata without full Markdown content

Markdown image references are relative links such as:

```markdown
![figure](images/figure_0001_ab12cd34ef56.png)
```

The linked image is written at the corresponding position where UniParser emitted the image in the Markdown content.

## Parse Options

The scripts keep the original scientific paper defaults:

- `textual`, `equation`, `table`: `OCRHighQuality`
- `chart`, `figure`, `expression`: `DumpBase64`
- `molecule`: `OCRFast`
- `sync=true` by default; `--async` only changes submit mode, then the script still polls and fetches results

## Common Issues

On failure, read stderr JSON `error.message`.

| Problem | Cause | Solution |
|---------|-------|----------|
| `CONFIG_ERROR` | Missing API key or missing package | Set `UNIPARSER_API_KEY`, or fill local `.env`; install UniParser-Tools |
| `DIR_EXISTS` | Output directory already exists | Re-run with `--overwrite` after user confirmation |
| `Token is duplicated` | Same API key and input were already submitted | Use `scripts/fetch_by_token.py` with the same input flag or token |
| Long wait / interrupted CLI | Server job may still be running | Re-run `fetch_by_token.py`; do not submit the same input again |

