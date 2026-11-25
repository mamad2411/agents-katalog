---
name: myicor-lessons-find
description: Find myICOR course lessons by topic using semantic search. Status — shipping in CLI v1.1. Until then, invoke the myicor-learn-search skill for myICOR articles, videos, and podcasts.
---

# myICOR Lesson Finder

This skill will let you (the AI agent) find specific myICOR **course
lessons** by topic — for questions like "which lesson covers the tag
system?" or "where does the course explain a brain dump?".

## Status: shipping in CLI v1.1

The `myicor lessons find` command is **registered but not yet active** in
CLI v1.0.0. Running it prints a notice and exits with code `2`.

**Why:** lesson search is semantic. It ranks lessons by meaning, not
keywords, which requires turning the user's query into a 1024-dimension
`voyage-context-3` embedding before the search runs. The query-embedding
path is being wired for CLI v1.1; v1.0.0 does not yet ship it.

## What to do until v1.1

For myICOR articles, videos, and podcast episodes, use the
**`myicor-learn-search`** skill — it is fully functional today:

```sh
myicor learn search "tag system"
myicor learn search "brain dump" --type video
```

That covers the learning **library**. Course-lesson-level discovery is what
this skill will add in v1.1.

## Command reference (v1.1 — not active yet)

### `myicor lessons find "<query>" [--json]`

Semantic search across myICOR course lessons. Each result will carry an
`is_accessible` flag derived from the user's membership tier — a free-tier
member can discover a lesson exists and see its deep link, but opening it
triggers an upgrade prompt in the app.

Planned `--json` shape:

```json
{
  "query": "tag system",
  "results": [
    {
      "title": "Building a tag system that scales",
      "course_title": "PKM like a Pro",
      "level": "...",
      "duration_seconds": 540,
      "url": "https://app.myicor.com/courses/<course>/<lesson>",
      "is_accessible": true,
      "minimum_access_tier": "monthly"
    }
  ]
}
```

When v1.1 ships, this skill will be updated and the command will return
real results.

## Repository

This skill lives at https://github.com/myicor/skills under
`skills/myicor-lessons-find/`.
