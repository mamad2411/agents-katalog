---
name: snow-kb
description: Use when searching, reading, writing, or publishing ServiceNow knowledge-base articles — answering questions from the KB, or turning a resolved issue into a KB article.
---

# ServiceNow knowledge base

Orient first (see `using-snow`). Read-only deployments can search and read
but not author.

## Find & read

- `search_knowledge(query="vpn timeout")` — full-text like the portal search
  box, permission-filtered, relevance-ranked. Falls back to a table search
  automatically if the KB API is off (the `source` field says which
  answered). Structured filters (category, date, author) → `query_records`
  on `kb_knowledge` instead.
- `get_article(sys_id)` — the full body (HTML). Note: like the portal, this
  increments the article's view count.

## Author & publish

1. `create_article(knowledge_base="IT", short_description=..., text=...)` —
   KB by display name; body is HTML (plain text renders as-is). Articles
   start as **drafts**, invisible to readers.
2. Review the draft content with the user before publishing.
3. `publish_article(sys_id)` — then **check the returned state**: KBs with
   an approval workflow route to `review` instead of `published`; tell the
   user which happened.

Contributor/publish rights are per-KB; a 403 means the user lacks them on
that knowledge base (not a tool failure). Good article hygiene: title states
the problem, body leads with the fix, then symptoms/cause.
