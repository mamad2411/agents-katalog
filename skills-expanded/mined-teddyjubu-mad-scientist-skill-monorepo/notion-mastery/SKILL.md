---

name: notion-mastery
description: Build beautiful, well-organized Notion pages and databases — from a single meeting note to a full team wiki, CRM, OKR tracker, or project hub. Use this skill whenever the user mentions Notion, asks to create or update a Notion page or database, wants to design a workspace, build a template, sync content into Notion, or even hints at workflows like "wiki", "team space", "project tracker", "second brain", "meeting notes hub", "PARA", "Zettelkasten", "company knowledge base", or "personal dashboard" — even if they don't explicitly say "Notion". Also triggers on Notion API questions, block JSON, database schema design, property types, formula syntax, relations, rollups, and on requests to convert markdown or other documents into Notion. Designed to work in agents that consume the agentskills.io SKILL.md format (Anthropic, Hermes Agent, OpenClaw) whether they call the API via MCP, the official SDK, or raw HTTP.
license: MIT
metadata:
  version: 1.0.0
  authored_for: Hermes Agent (NousResearch) and OpenClaw, compatible with any agent runtime that loads agentskills.io SKILL.md format

---
This skill makes you a Notion expert. By "expert" I mean two things at once: technically airtight (you produce valid API payloads on the first try, you know the constraints, you know which version of the API supports what) and aesthetically considered (the pages you build feel restrained, organized, and pleasant — not the typical wall-of-blocks output that most agents produce).

The skill is structured so you can do small jobs without loading everything, and load deep references only when the task needs them.

## What This Skill Does

This skill Build beautiful, well-organized Notion pages and databases — from a single meeting note to a full team wiki, CRM, OKR tracker, or project hub. Use this skill whenever the user mentions Notion, asks to create or update a Notion page or database, wants to design a workspace, build a template, sync content into Notion, or even hints at workflows like "wiki", "team space", "project tracker", "second brain", "meeting notes hub", "PARA", "Zettelkasten", "company knowledge base", or "personal dashboard" — even if they don't explicitly say "Notion". Also triggers on Notion API questions, block JSON, database schema design, property types, formula syntax, relations, rollups, and on requests to convert markdown or other documents into Notion. Designed to work in agents that consume the agentskills.io SKILL.md format (Anthropic, Hermes Agent, OpenClaw) whether they call the API via MCP, the official SDK, or raw HTTP.

## How to use this skill

Almost every Notion task follows the same shape:

1. **Clarify intent.** What is the user actually trying to build? A one-off page, a reusable template, a database, or a whole subsystem? Who else will use it?
2. **Pick the right primitive.** Page or database? Inline or full-page? New workspace or extend existing? See `references/design-patterns.md` §6 (Information Architecture) for the decision rules.
3. **Design before writing.** For anything bigger than a single page, sketch the structure first: parent page, child databases, relations, views. Confirm with the user before generating JSON.
4. **Generate the smallest correct payload.** Don't over-spec. Start with required fields, then add properties, then add content. Notion's API rejects extra fields silently in some cases and loudly in others — minimalism is safer.
5. **Validate against constraints.** See §"Critical constraints" below. Most agent failures are constraint violations, not logic errors.
6. **Make it beautiful.** Before declaring done, run the "Beautiful by Default" checklist (`references/design-patterns.md` §9).

## What's in this skill

| File | When to read it |
|---|---|
| `references/api-reference.md` | Whenever you need exact JSON shapes, endpoint specifics, or version-dependent behavior. This is the canonical technical reference. |
| `references/block-types.md` | When composing page content — quick lookup for any block type's payload shape. |
| `references/database-properties.md` | When designing or modifying a database schema. Every property type with create + update + value payloads. |
| `references/design-patterns.md` | When the user wants something to look good. Visual hierarchy, color discipline, layout patterns, anti-patterns. |
| `references/templates.md` | When building a known archetype (CRM, OKR tracker, sprint board, content calendar, etc.). Pre-designed schemas. |
| `references/ecosystem-resources.md` | When the user asks "where should I learn X" or you need to recommend a library, blog, or community resource. |
| `references/markdown-to-blocks.md` | When converting markdown (or any document) into Notion blocks. Covers the native `markdown` field (recommended) and manual AST translation. |
| `references/troubleshooting.md` | When an API call fails. Symptom → cause → fix lookup. |
| `scripts/md_to_notion_blocks.py` | Markdown → Notion block JSON converter. Use when the runtime doesn't support the native markdown field or when you need fine-grained control. |
| `scripts/chunk_rich_text.py` | Splits long strings to respect the 2000-char-per-rich-text-element limit. |
| `scripts/batch_append.py` | Appends large block lists by chunking into 100-block batches with retry handling. |
| `scripts/validate_payload.py` | Pre-flight check for common payload mistakes before you call the API. |

Don't read all of these. Read what the task needs.

## How agents actually call Notion (three common runtimes)

This skill is runtime-agnostic. The payload shapes are the same; only the transport differs:

1. **Notion MCP server** — if a Notion MCP is connected, prefer it: tools like `notion-create-pages`, `notion-fetch`, `notion-search`, `notion-update-page`, `notion-create-database`. The MCP handles auth, headers, and version negotiation. Use this tier first whenever it's available.
2. **Official SDKs** — `@notionhq/client` (Node), `notion-sdk-py` (Python). Use when writing code the user will run themselves.
3. **Raw HTTPS** — `curl`, `fetch`, `requests`. Base URL `https://api.notion.com/v1`, header `Authorization: Bearer <token>`, header `Notion-Version: 2025-09-03` (current stable; see api-reference.md §0 for version selection).

Whichever transport you use, you're producing the same JSON. The payload shapes in this skill apply universally.

## The five things that go wrong most often

These are the failure modes you should pre-empt before submitting any payload. Memorize them.

1. **Property name mismatch.** Database property names are case-sensitive and must match the schema exactly. "due date" ≠ "Due Date" ≠ "DueDate". When updating a page, fetch the database schema first (or remember it from creation) — never guess.
2. **Wrong parent type.** A page in a database needs `parent: { database_id: "..." }`. A subpage needs `parent: { page_id: "..." }`. Mixing these returns a confusing validation error.
3. **Rich text length.** Each `rich_text` text element maxes at 2000 characters. Long paragraphs must be chunked across multiple text elements (within one rich_text array). Use `scripts/chunk_rich_text.py`.
4. **Block batching.** Maximum 100 children per create-or-append call. Max 2 levels of nesting per call. For larger payloads, use multiple calls (`scripts/batch_append.py` handles this).
5. **Select / multi-select options.** When setting a select value, if the option doesn't exist yet, the API will create it — but only if the integration has schema-write permission and only in the property's existing color palette. Safer to either confirm the option exists or update the schema explicitly first.

For the long-tail of error patterns, see `references/troubleshooting.md`.

## Critical constraints

These are hard limits. The skill assumes a target version of **Notion-Version: 2025-09-03** unless the user has pinned an older version. See `references/api-reference.md` §0.1 for version specifics.

| Limit | Value |
|---|---|
| Rate limit | ~3 requests/sec average per integration (bursts allowed; respect `Retry-After` on 429) |
| Children per create/append call | 100 blocks |
| Nesting depth per create call | 2 levels (build deeper trees with follow-up appends) |
| Characters per rich_text element | 2000 |
| Blocks per page (soft) | ~1000 — past that, Notion's UI gets sluggish |
| Payload size per request | 500 KB |
| Database property count (soft) | ~25 — past that, table views become unusable |
| Page title length | 200 chars (rich_text array) |
| Database/property names | 200 chars |
| Files property URL | 2000 chars |

## The Notion API mental model

Two ideas unlock most of the API:

**Ideas → blocks → pages → databases.** A *page* is a tree of *blocks*. The page's "content" is just `children` of the page-as-block. A *database* is a special collection of pages that share a schema. Every database has exactly one `title` property; everything else is up to you. Beyond that, databases and pages are the same animal under the hood.

**The "type" discriminator pattern.** Almost every Notion object is a tagged union: there's a `type` field whose value names a sibling field holding the type-specific payload. A `heading_2` block has `{ "type": "heading_2", "heading_2": { ... } }`. A `select` property value has `{ "type": "select", "select": { "name": "..." } }`. A rich_text element has `{ "type": "text", "text": { ... } }` or `{ "type": "mention", "mention": { ... } }`. Once this clicks, the JSON stops feeling redundant — every object self-describes.

## Building a beautiful page (the workflow)

When the user wants "a page that looks good," follow this loop. Don't skip steps — the cumulative effect is the difference between an obviously-AI page and a thoughtful one.

1. **Cover and icon.** Default to a gradient cover (1500×600). Choose an emoji that reads at 16×16 — single subject, high contrast. If the page is part of a series (e.g., meeting notes), match icons across siblings.
2. **Intro callout.** One sentence stating the purpose, in a callout block with a relevant icon and a soft background (`gray_background` is the safest default). This is the "why this page exists" signal.
3. **Section structure.** H2 for top-level sections, H3 for sub-sections. Avoid H1 in the body — H1 is implicitly the page title. Three H2 sections per page is a sweet spot; more than five and the page should probably split.
4. **Whitespace and dividers.** A divider between major sections, and an empty paragraph block before each H2, provides breathing room. Notion has no margin controls — empty blocks *are* your spacing primitive.
5. **Use columns for dashboards, not for prose.** Two- or three-column layouts work for navigation, quick stats, and side-by-side reference. They don't work for prose.
6. **Don't over-use color.** Pick at most three colored elements above the fold (one callout, two colored text spans, say). More than that, the page reads as cluttered.
7. **End with action.** What should the reader do next? A linked database view, a list of related pages, a CTA toggle.

Full pattern catalog (named layouts like "Hero with Callout Intro", "Three-Column Dashboard", "Hub and Spoke") in `references/design-patterns.md` §2.

## Building a database (the workflow)

1. **Start with the title.** Every database needs exactly one `title` property. Make it descriptive — "Project Name", "Customer Account", "Article Title" — not just "Name". The title is the only property that's always visible in every view.
2. **Choose the smallest schema that solves the problem.** Eight properties is plenty for most use cases. Twenty-five is unusable. If you're tempted to add a property, ask whether it can be a tag instead.
3. **Order matters.** The canonical order in Notion is: `title → status → owner → dates → tags/categories → metadata → notes`. Users scan left-to-right; the most-acted-on property should be near the title.
4. **Use the right property type.** `status` (not `select`) for workflow states — it groups by To-do / In progress / Complete and feeds the board view's columns. `select` for tags that don't have an order. `multi_select` only when items genuinely belong to multiple categories. `relation` to link to other databases; pair with a `rollup` to surface count/sum/latest from the related records.
5. **Default views are not enough.** Set up at least: a table view for power editing, a board view for status, and one filtered "Active" or "Mine" view. Note: views cannot be created via the API in versions below 2026-04-01 — create the database via API, then guide the user to set up views in the UI, or use the Views API on a supported version.
6. **Seed it.** A database with zero rows looks broken. Add 2–3 sample rows when creating, marked clearly as examples the user can delete.

For property-type details and create-payload examples, see `references/database-properties.md`. For ten ready-to-use database designs (CRM, OKR tracker, sprint board, etc.), see `references/templates.md`.

## Searching and fetching (the workflow)

Notion's search is full-text and *eventually* indexed — a page created seconds ago may not show up yet. Plan for that.

1. **For broad search**, use `POST /v1/search` with a `query` string. Filter by `object_type` (`page` or `database`) and sort by `last_edited_time`. Default to descending so users see fresh content first.
2. **For database queries**, use `POST /v1/databases/{id}/query` with a filter object. Filters are per-property-type — see `references/api-reference.md` §5 for the filter grammar. Compound filters use `and` / `or`. Always cap with `page_size` and respect `next_cursor` for pagination.
3. **For exact ID lookups**, prefer `GET /v1/pages/{id}` or `GET /v1/databases/{id}` — they're faster and immune to indexing lag.
4. **Don't fetch what you don't need.** Page properties come back with the page; block children are a separate call. If you only need the title and one property, you're already done after the page fetch.
5. **Cache the database schema.** When operating on the same database multiple times in a session, fetch the schema once and remember it. This avoids the case-sensitivity property-name mistake.

## Updating existing content

Two distinct endpoints, easy to confuse:

- `PATCH /v1/pages/{id}` — updates page **properties** (database row fields), the icon, the cover, or archives/restores the page. Does NOT touch the page's body content.
- `PATCH /v1/blocks/{id}` — updates a single **block** (paragraph, heading, etc.). Use this for page body content.
- `PATCH /v1/blocks/{id}/children` — **appends** new children to a block. Cannot insert in the middle.
- `DELETE /v1/blocks/{id}` — archives a block. (Notion has no true delete; archived ≈ deleted for practical purposes.)

To "edit a paragraph": fetch the block, replace `paragraph.rich_text`, PATCH the block. To "add a section to a page": PATCH children of the page block. To "insert in the middle": you have to delete subsequent blocks and re-append (Notion has no `insertAt` primitive).

## When to ask the user, not guess

Notion is opinionated, and a confidently-wrong design is more painful than a question. Ask the user before doing any of these things without explicit instruction:

- Deleting or archiving any existing content
- Changing a database's property types (especially `select`/`status` — changing these can lose data)
- Renaming properties (breaks formulas, rollups, and views that depend on the old name)
- Adding properties to a database that already has > 10 properties
- Creating new top-level pages in a shared workspace
- Anything that touches more than ~20 pages in one operation

For everything else (composing content, designing new structure, choosing colors and icons), make a confident choice and proceed — the user can always ask you to change it.

## Notion-Version note

Each request requires a `Notion-Version` header. As of May 2026 the practical choices are:

- `2022-06-28` — most stable, widely supported, but no data sources, no markdown POST field, no Views API.
- `2025-09-03` — adds the `data_source` model (databases became containers for data sources) and the `markdown` field on `POST /v1/pages`. **Recommended baseline** for new work.
- `2026-04-01` — adds the Views API (create/update database views programmatically), `heading_4`, and new rate-limit response headers.

If the user is updating an existing integration on `2022-06-28`, don't silently upgrade — preserve their version unless they explicitly opt in. Behavior of `databases` endpoints changed meaningfully between `2022-06-28` and `2025-09-03`; see `references/api-reference.md` §0.1 for the migration notes.

## External resources to recommend

When the user asks where to learn more or wants a template they can buy, here are the trusted sources. (Full annotated list in `references/ecosystem-resources.md`.)

- **Official docs**: developers.notion.com (API reference), notion.com/help (user-level help), notion.com/templates (marketplace)
- **Best independent reference**: Notion VIP / William Nutt (notion.vip)
- **Best free API tutorials**: Red Gregory (redgregory.com)
- **Deepest paid course**: Notion Mastery by Marie Poulin (notionmastery.com)
- **Most popular templates**: Easlo (easlo.co/templates), Thomas Frank (thomasjfrank.com)
- **Top community**: r/Notion on Reddit
- **Methodology**: August Bradley's PPV (Pillars/Pipelines/Vaults) at yearzero.io/notion

## A note on style

Be concise. Don't pad pages with explanations the user can read in the page itself. Don't add "Generated by..." footers unless asked. Don't number things just to number them. The best Notion pages feel like they were carefully edited, not generated; the goal of this skill is to make that distinction invisible.
