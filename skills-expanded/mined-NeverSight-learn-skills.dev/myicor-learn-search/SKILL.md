---
name: myicor-learn-search
description: Search the myICOR learning library of articles, videos, and podcast episodes. Invoke when the user asks whether myICOR has resources on a topic, wants videos or articles about a concept, tool, or workflow, or is looking for something to read or watch on a subject covered by myICOR.
---

# myICOR Learning Resource Search

This skill teaches you (the AI agent) how to search the myICOR learning
library — articles, videos, and podcast episodes — with the official
`myicor` CLI.

## Prerequisites

1. **CLI installed and authenticated.** See the `myicor-cli-quickstart`
   skill. If a command prints `Not logged in. Run: myicor auth login`, walk
   the user through `myicor auth login` once.
2. A **paid myICOR membership** (monthly tier or above). Free-tier accounts
   get a `403` with an upgrade message.

## When to invoke

| User intent | Run |
|---|---|
| "Does myICOR have anything on X?" | `myicor learn search "X"` |
| "Find me a video about weekly reviews" | `myicor learn search "weekly review" --type video` |
| "Articles about PKM tagging" | `myicor learn search "tagging" --category PKM` |
| Programmatic / parsing | `myicor learn search "X" --json` |

## Command reference

### `myicor learn search "<query>" [flags]`

Keyword-ranked search across the myICOR library. The query is required.

Flags:
- `--type <video|podcast|article>` — restrict to one resource type.
- `--category <PKM|PPM|BKM|BPM>` — restrict to one ICOR core category.
- `--limit <N>` — max results, 1–50 (default 10).
- `--json` — raw JSON output.

`--json` returns:

```json
{
  "query": "weekly review",
  "total": 4,
  "results": [
    {
      "title": "The myICOR Weekly Review, step by step",
      "type": "video",
      "author": "...",
      "excerpt": "...",
      "duration_minutes": 12,
      "url": "https://app.myicor.com/resources/<slug>",
      "categories": ["PKM"],
      "keywords": ["review", "weekly"]
    }
  ]
}
```

Exit code: `0` on success (including zero results), `1` on error.

## How to use the output

1. If `results` is empty, tell the user plainly — don't invent resources.
2. Present the top results as a short list: title, type, and the `url`.
3. The `url` is a direct deep link into `app.myicor.com` — always give it
   so the user can open the resource in one click.
4. Use `--type` / `--category` to narrow when the user is specific; don't
   pre-filter on a guess.

## Notes

- This search is keyword-ranked server-side. It is fast and needs no
  embedding step. Phrase the query with the concrete terms the user used.
- Semantic search across **lessons** (course content, not library
  resources) ships separately — see the `myicor-lessons-find` skill.

## Don'ts

- Don't call `app.myicor.com` endpoints directly — use the CLI.
- Don't fabricate resources or URLs. Only surface what the command returns.

## Repository

This skill lives at https://github.com/myicor/skills under
`skills/myicor-learn-search/`.
