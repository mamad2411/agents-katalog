---
name: hn-extract
description: Extract a HackerNews post (article + comments) into single clean Markdown for quick reading or LLM input.
metadata:  {"openclaw":{"always":false,"emoji":"🦞","homepage":"https://github.com/guoqiao/skills/blob/main/hn-extract/hn-extract/SKILL.md","os":["darwin","linux","win32"],"tags":["hn","hackernews","comments","extract","markdown","python","uv","scraper","rss","reader","summarize"],"requires":{"bins":["uv"]}}}
---

# HackerNews Extract

Extract a HackerNews post (article + comments) into single clean Markdown for quick reading or LLM input.

see [Examples](https://github.com/guoqiao/skills/blob/main/hn-extract/examples)

Use this skill when the user types `/hn-extract` or asks to extract/summarize a HackerNews Post.

**Triggers:**
- "Extract HN Post ..."
- "/hn-extract <hn_id_or_url>"
- "Summarize this HN post ..."

## What it does
- Accepts an HackerNews id or url
- Download the linked article HTML, extracts text, cleans and formats it.
- Fetches the Hacknews post metadata and comments.
- Outputs a readable combined markdown file with original article, threaded comments, and key metadata.

## Requirements

- `uv` installed and in PATH.

## Install

No install beyond having `uv`.
Dependencies will be installed automatically by `uv` into to a dedicated venv when run this script.

## Usage Workflow (Mandatory for Agents)

When an agent is asked to extract a HackerNews post:
1.  **Run the script** with an output path: `uv run --script ${baseDir}/hn_extract.py <input> -o /tmp/hn-<id>.md`.
2.  **Send ONE combined message:** Upload the file and ask the question in the *same* tool call. Use the `message` tool (`action=send`, `filePath="/tmp/hn-<id>.md"`, `message="Extraction complete. Do you want me to summarize it?"`).
3.  **Do not** output the full text or a summary directly in the chat unless specifically requested.

## Usage

```bash
# run as uv script
uv run --script ${baseDir}/hn_extract.py <hn-id|hn-url> [-o path/to/output.md]

# Examples
uv run --script ${baseDir}/hn_extract.py 46861313 -o /tmp/output.md
uv run --script ${baseDir}/hn_extract.py "https://news.ycombinator.com/item?id=46861313"
```

- Omit `-o` to print to stdout.
- Directories for `-o` are created automatically.

## Notes
- Retries are enabled for HTTP fetches.
- Comments are indented by thread depth.
- Sites requires authentication or blocks scraping may still fail.
