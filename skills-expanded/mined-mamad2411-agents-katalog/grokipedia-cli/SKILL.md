---
name: grokipedia-cli
description: Query Grokipedia knowledge base using the grokipedia CLI. Use when working with knowledge articles, documentation search, wiki content, or when the user mentions Grokipedia, knowledge base, wiki search, or grokipedia.
---

# Grokipedia CLI

Query Grokipedia knowledge base using the `grokipedia` command-line tool.

## Prerequisites

```bash
grokipedia --version
export GROKIPEDIA_API_KEY='your-api-key'
grokipedia auth status
```

## Authentication

- API key from Grokipedia
- Environment variable: `GROKIPEDIA_API_KEY`

## Articles & Content

### Search

```bash
grokipedia search --query "machine learning" --limit 20
grokipedia search --category "Technology" --tag "AI"
grokipedia articles list --recent --limit 50
```

### Get Articles

```bash
grokipedia articles get ARTICLE_ID
grokipedia articles get ARTICLE_ID --format markdown
grokipedia articles get ARTICLE_ID --include-references
```

### Categories & Tags

```bash
grokipedia categories list
grokipedia categories get CATEGORY_ID --articles
grokipedia tags list --popular
grokipedia tags get TAG_ID --articles
```

## Knowledge Management

```bash
grokipedia knowledge graph --topic "Artificial Intelligence"
grokipedia related --article ARTICLE_ID --limit 10
grokipedia path --from "Neural Networks" --to "Deep Learning"
```

## Content Export

```bash
grokipedia export --category "Science" --format json
grokipedia export --query "quantum computing" --format markdown --output ./articles/
grokipedia backup --all --output grokipedia-backup.zip
```

## Agent Best Practices

1. **Full-text search**: Use natural language queries
2. **Categories**: Use for browsing vs searching
3. **Formats**: JSON (default), Markdown, or HTML
4. **References**: Use `--include-references` for research tasks
