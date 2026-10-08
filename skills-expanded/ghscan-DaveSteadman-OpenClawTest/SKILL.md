````skill
# Skill: Gen3ReadWebpage

Read a webpage and save the article main body into a local Markdown file (`.md`) in shared datastore folder structure.

## What this skill does

- Downloads HTML from a URL
- Strips scripts/styles/navigation/sidebar-like blocks
- Calls shared Ollama helper from `skills/CommonCode/OllamaPrompt.py`
- Uses local Ollama to keep article main body content
- Writes UTF-8 Markdown to:
  - `data/datastore3/<Area>/<Domain>/YYYY/MM/DD/<webpage-name>.md`

## Files

- `gen3_read_webpage.py` — Python script that performs fetch + extract + write

## Required inputs

- `--url` (webpage URL)
- `--domain` (folder name under area)

Optional:
- `--area` (defaults to `mine`)

## Usage

```powershell
python .\gen3_read_webpage.py --url "https://example.com/news/market-update" --domain "News"
```

Example output path:

`data/datastore3/01-Mine/News/2026/03/02/market-update.md`

## Notes

- Webpage filename uses page title (first 32 characters) when available; otherwise it falls back to URL path segment.
- No third-party packages required.
- LLM is Ollama-only using local API `http://127.0.0.1:11434/api/generate`.
````
