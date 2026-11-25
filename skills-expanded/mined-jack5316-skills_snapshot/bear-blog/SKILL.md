---
name: bear_blog
description: Publish an Obsidian note to BearBlog. Use when user asks to publish to BearBlog or /bear_blog.
---

# BearBlog Publish Skill

Publishes an Obsidian note to BearBlog, mapping frontmatter fields to BearBlog's header format.

## Usage

```bash
python3 _scripts/bearblog_publish.py NOTE_PATH [options]
```

- `NOTE_PATH` — path to note (relative to vault or absolute)
- `--draft` — save as draft instead of publishing
- `--title TITLE` — override post title
- `--link SLUG` — custom URL slug (e.g. `my-cool-post`)
- `--tags "AI, books"` — comma-separated tags
- `--discoverable` / `--no-discoverable` — show/hide on BearBlog feed
- `--lang LANG` — post language (e.g. `en`, `zh`)

## BearBlog Header Fields

All these fields can be set in the note's YAML frontmatter and will be passed through:

```yaml
---
title: I like Bears
link: i-like-bears
alias: 2012/01/02/cool-post.html
canonical_url: https://example.com/bears
published_date: 2022-12-30 08:30
is_page: false
meta_description: Look for the bear necessities.
meta_image: https://example.com/image.jpeg
lang: en
tags: AI, books, productivity
make_discoverable: true
---
```

CLI flags override frontmatter values when both are present.

## Output

Prints the URL of the created post on BearBlog.
