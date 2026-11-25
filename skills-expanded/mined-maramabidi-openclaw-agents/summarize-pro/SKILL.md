---
name: summarize-pro
description: Summarize long content into clear, concise outputs in the user's preferred format and language. Use for articles, documents, meetings, emails, transcripts, reports, conversations, and other long text.
metadata: {"clawdbot":{"emoji":"📝","requires":{"tools":["read","write"]}}}
---

# Summarize Pro

Produce concise, accurate summaries that never invent missing facts.

## Use Cases

- articles and blog posts
- reports and business documents
- meeting notes and transcripts
- emails and message threads
- book chapters and long excerpts
- research notes and product docs
- comparisons between two texts
- action-item extraction from long text
- summaries in another language
- very short TL;DR responses

## What The User Can Say

Trigger the skill when the user says any of these:

- `summarize this`
- `summarize`
- `summary`
- `tldr`
- `tl;dr`
- `bullet points`
- `summarize in bullets`
- `key takeaways`
- `main points`
- `action items`
- `what do I need to do`
- `executive summary`
- `exec summary`
- `meeting summary`
- `meeting notes`
- `email summary`
- `summarize this email`
- `thread summary`
- `conversation summary`
- `chapter summary`
- `compare`
- `summarize in French`
- `summarize in Arabic`
- `summarize in [language]`
- `summarize in 50 words`
- `summarize in 3 sentences`
- `make it shorter`
- `make it longer`
- `save summary`
- `show saved summaries`
- `summary history`
- `summary stats`
- `my stats`

## Core Rules

- Preserve names, numbers, dates, and decisions exactly.
- Keep the tone aligned with the source text.
- Do not add facts that are not in the original.
- If the source text is short, say so instead of padding the result.

## Local Data

Store settings, history, saved summaries, and templates under:

- `~/.openclaw/summarize-pro/settings.json`
- `~/.openclaw/summarize-pro/history.json`
- `~/.openclaw/summarize-pro/saved.json`
- `~/.openclaw/summarize-pro/templates.json`

## First Run

If the data directory does not exist, create it before reading or writing files.

```bash
mkdir -p ~/.openclaw/summarize-pro
```

## Behavior

- Always count words when summarizing.
- Auto-detect the best format when the user does not specify one.
- Log summaries to history and keep the most recent 100 entries.
- Update usage stats after each summary.
- If the user gives no text, ask them to paste the content first.
- If the text is short, say it is already short instead of padding it.
- If the text is unclear, give the best interpretation and say it is uncertain.

## Output Formats

- TL;DR: 1-2 sentences, direct and compact
- Bullets: 3-7 bullets, each focused and concrete
- ELI5: simple language and analogies
- Key takeaways: ranked list of the most important points
- Action items: tasks, owners, deadlines, if present
- Executive summary: formal business summary
- Meeting summary: topic, participants, decisions, actions
- Email summary: purpose, key points, action required
- Comparison: side-by-side differences and similarities
- Custom length: follow the requested word or sentence count as closely as possible

## Examples

- `Summarize this article in 5 bullets`
- `TL;DR this report`
- `What are the action items from this meeting?`
- `Compare these two summaries`
- `Summarize this in French`
- `Give me an executive summary`
- `Save this summary`
- `Show summary history`
