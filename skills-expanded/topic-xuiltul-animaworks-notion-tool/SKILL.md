---
name: notion-tool
description: >-
  A Notion integration tool. It performs page and database search, retrieval, creation, and updates via the API.
  Use when: Use when: you need to edit Notion pages, add database rows, or search and retrieve workspace content.
tags: [productivity, notion, external]
---


# Notion Tool

An external tool that performs page and database search, retrieval, creation, and updates via the Notion API.

## How to Invoke

**Bash**: Run with `animaworks-tool notion <サブコマンド> [引数]`

## List of Actions

### search — Workspace Search
```bash
animaworks-tool notion search [検索ワード] -j
```

### get_page — Retrieve Page Metadata
```bash
animaworks-tool notion get-page PAGE_ID -j
```

### get_page_content — Retrieve Page Content
```bash
animaworks-tool notion get-page-content PAGE_ID -j
```

### get_database — Retrieve Database Metadata
```bash
animaworks-tool notion get-database DATABASE_ID -j
```

### query — Database Query
```bash
animaworks-tool notion query DATABASE_ID [--filter JSON] [--sorts JSON] [-n 10] -j
```
- `filter`: Notion API filter JSON (optional)
- `sorts`: Array of sort conditions (optional)

### create_page — Create Page
```bash
animaworks-tool notion create-page --parent-page-id ID --properties JSON -j
```
- Either `parent_page_id` or `parent_database_id` is required
- `children`: Array of page content blocks (optional)

### update_page — Update Page
```bash
animaworks-tool notion update-page PAGE_ID --properties JSON -j
```

### create_database — Create Database
```bash
animaworks-tool notion create-database --parent-page-id ID --title "名前" --properties JSON -j
```

## CLI Usage

```bash
animaworks-tool notion search [検索ワード] -j
animaworks-tool notion get-page PAGE_ID -j
animaworks-tool notion get-page-content PAGE_ID -j
animaworks-tool notion get-database DATABASE_ID -j
animaworks-tool notion query DATABASE_ID [--filter JSON] [--sorts JSON] [-n 10] -j
animaworks-tool notion create-page --parent-page-id ID --properties JSON -j
animaworks-tool notion update-page PAGE_ID --properties JSON -j
animaworks-tool notion create-database --parent-page-id ID --title "名前" --properties JSON -j
```

## Notes

- The Notion API Token must be pre-configured in credentials
- Page/database IDs can be with or without hyphens
- The structure of properties follows the Notion API schema
