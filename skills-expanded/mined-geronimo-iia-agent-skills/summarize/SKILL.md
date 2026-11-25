---
name: summarize
description: >-
  Summarize URLs, local files (PDFs, documents, audio), and YouTube links.
  Composable pipeline using llm + markitdown + Jina Reader. Supports local
  models via Ollama. Use when you need a quick one-shot summary without
  ingesting into the knowledge base.
metadata:
  version: "1.1.0"
---

# Summarize

Composable pipeline for summarizing web pages, documents, audio, and video.
Mix and match tools based on input type and model preference.

## Install

`llm` needs a persistent install so plugins survive between calls:
```bash
uv tool install llm
llm install llm-ollama            # optional: local models via Ollama
brew install steipete/tap/summarize  # optional: all-in-one CLI alternative
```

`markitdown` and `fabric` work as one-shot `uvx` calls — no permanent install needed.

## Quick start by input type

### URL → summary

```bash
# Jina Reader: zero-install, returns clean markdown
curl -s "https://r.jina.ai/https://example.com" | llm "summarize this"

# With a specific model
curl -s "https://r.jina.ai/https://example.com" | llm -m claude-opus-5 "summarize"
```

### PDF / Word / PPTX / HTML → summary

```bash
uvx markitdown file.pdf | llm "summarize"
uvx markitdown file.docx | llm "summarize"
```

### YouTube / audio → summary

```bash
# Via summarize CLI (handles transcription)
summarize "https://youtu.be/<id>" --youtube auto

# Local: yt-dlp + whisper pipeline
yt-dlp -x --audio-format mp3 -o /tmp/audio.mp3 "https://youtu.be/<id>"
uvx openai-whisper /tmp/audio.mp3 --output_format txt
llm "summarize" < /tmp/audio.txt
```

### Stdin / arbitrary text

```bash
cat notes.txt | llm "summarize"
echo "long text..." | llm -m ollama/llama3.2 "summarize in 3 bullets"
```

## llm — model selection

```bash
llm models                        # list available models
llm -m claude-opus-5 "..."        # Anthropic (needs ANTHROPIC_API_KEY)
llm -m gpt-4o "..."               # OpenAI (needs OPENAI_API_KEY)
llm -m ollama/llama3.2 "..."      # local via Ollama (no key needed)
llm -m gemini-1.5-flash "..."     # Google (needs GEMINI_API_KEY)
```

Set default model once:
```bash
llm models default claude-sonnet-5
```

## fabric — opinionated extraction patterns

Useful when you want structured extraction, not just a summary:

```bash
uvx fabric --pattern summarize < input.txt
curl -s "https://r.jina.ai/https://example.com" | uvx fabric --pattern extract_wisdom
curl -s "https://r.jina.ai/https://example.com" | uvx fabric --pattern extract_ideas
uvx fabric --list   # see all available patterns
```

## summarize CLI (steipete) — when to prefer it

Use over the composable pipeline when:
- You need audio diarization (`--diarize`)
- YouTube via Apify fallback (`--youtube auto`)
- Multi-provider routing from one tool (`--model cli/claude`, OpenRouter, GitHub Copilot)
- You want `--length` control without writing a prompt

```bash
summarize "https://example.com" --model anthropic/claude-sonnet-5 --length long
summarize "file.pdf" --model google/gemini-3-flash-preview
summarize "https://youtu.be/<id>" --youtube auto
summarize "https://example.com" --cli claude   # uses claude CLI, no API key
```

## When NOT to use

Use `ctx_fetch_and_index` instead when you need the content indexed and
searchable later in the same session. These tools are one-shot — output is
not stored in the context-mode knowledge base.
