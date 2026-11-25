---
name: form-to-reddit-pipeline
description: >-
  Orchestrates the complete workflow: reads Discord form responses via discord-form-reader,
  researches optimal subreddits via reddit-readonly, and delivers recommendations.
  Use when you want end-to-end automation from form submission to Reddit strategy.
metadata: {"clawdbot":{"emoji":"🔄","requires":{"bins":["node"]}}}
---

# Form to Reddit Pipeline

Connects discord-form-reader → reddit-readonly → Final Response

## What this pipeline does

1. Detects new messages in #filled-answers
2. Extracts business data using discord-form-reader
3. Searches Reddit for relevant subreddits using reddit-readonly
4. Analyzes top subreddits for engagement and rules
5. Generates tailored Reddit post
6. Delivers complete strategy back to Discord

## Hard rules

- **Never post automatically** - only generate recommendations and post drafts
- **Always include permalinks** from reddit-readonly results
- **Validate form data** before proceeding to Reddit search
- **Respect rate limits** - add delays between Reddit requests
- **Preserve original message** in pipeline logs for auditing

## Output format

All commands print JSON to stdout.

- Success: `{ "ok": true, "data": { ... }, "pipeline": "complete" }`
- Failure: `{ "ok": false, "error": { "message": "...", "step": "parsing|reddit|generation" } }`

## Commands

### 1) Run complete pipeline on latest message

```bash
node {baseDir}/scripts/form-to-reddit-pipeline.mjs