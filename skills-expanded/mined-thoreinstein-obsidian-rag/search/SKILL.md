---
name: search
description: >-
  Use when the user wants to find notes by keyword or filename, or says
  "search", "find notes", or "look for".
---

# Search Vault

Search for notes by keyword or filename match.

## Workflow

1. Call `obsidian_search_notes` with the user's query
2. Present matching files in a clear list
3. Ask if the user would like to read any of the results

## Arguments

The search query follows the skill invocation. Example: `/search cooking recipes`

## Tips

- This is a simple text match (keyword in filename or content)
- For semantic/meaning-based search, suggest `/research` instead
- Results are capped at 20 matches
