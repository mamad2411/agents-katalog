---
name: managing-notion
description: Notion workspace management - pages, databases, blocks, and content. Use when searching, creating, updating, or organizing Notion content.
connection_type: notion
preload: false
---

# Managing Notion

Tools for Notion workspace management including pages, databases (data sources), blocks, and comments.

**Important:** All tools require a parameter object. Pass `{}` for tools with no required parameters.

## Tools (21 total)

### Users

| Tool | Description |
|------|-------------|
| `APIGetSelf({})` | Get current bot user |
| `APIGetUser({ user_id })` | Get a user by ID |
| `APIGetUsers({})` | List all users (optional: `start_cursor`, `page_size`) |

### Search

| Tool | Description |
|------|-------------|
| `APIPostSearch({})` | Search pages/databases by title (optional: `query`, `filter`, `sort`, `start_cursor`, `page_size`) |

### Pages

| Tool | Description |
|------|-------------|
| `APIRetrieveAPage({ page_id })` | Get page metadata (optional: `filter_properties`) |
| `APIPostPage({ parent, properties })` | Create new page (optional: `children`, `icon`, `cover`) |
| `APIPatchPage({ page_id })` | Update page (optional: `properties`, `archived`, `in_trash`, `icon`, `cover`) |
| `APIMovePage({ page_id, parent })` | Move page to new parent |
| `APIRetrieveAPageProperty({ page_id, property_id })` | Get specific property value |

### Blocks

| Tool | Description |
|------|-------------|
| `APIRetrieveABlock({ block_id })` | Get block metadata |
| `APIGetBlockChildren({ block_id })` | List child blocks (optional: `start_cursor`, `page_size`) |
| `APIPatchBlockChildren({ block_id, children })` | Append blocks (optional: `after`) |
| `APIUpdateABlock({ block_id })` | Update block (optional: `type`, `archived`) |
| `APIDeleteABlock({ block_id })` | Delete/trash a block |

### Data Sources (Databases)

| Tool | Description |
|------|-------------|
| `APIQueryDataSource({ data_source_id })` | Query with filters (optional: `filter`, `sorts`, `start_cursor`, `page_size`) |
| `APIRetrieveADataSource({ data_source_id })` | Get database schema |
| `APICreateADataSource({ parent, properties })` | Create database (optional: `title`) |
| `APIUpdateADataSource({ data_source_id })` | Update schema (optional: `title`, `description`, `properties`) |
| `APIListDataSourceTemplates({ data_source_id })` | List templates in database |

### Comments

| Tool | Description |
|------|-------------|
| `APIRetrieveAComment({ block_id })` | Get comments (optional: `start_cursor`, `page_size`) |
| `APICreateAComment({ parent, rich_text })` | Add comment |

## Examples

### Search and Retrieve

```typescript
import { APIPostSearch, APIRetrieveAPage, APIGetBlockChildren } from '@connections/notion';

// Search (pass empty object if no query)
const results = await APIPostSearch({
  query: 'meeting notes',
  filter: { property: 'object', value: 'page' }
});

// Get page
const page = await APIRetrieveAPage({ page_id: 'page-id-here' });

// Get blocks
const blocks = await APIGetBlockChildren({ block_id: page.id });
```

### Create Page

```typescript
import { APIPostPage } from '@connections/notion';

const page = await APIPostPage({
  parent: { page_id: 'parent-page-id' },
  properties: {
    title: [{ text: { content: 'New Page' } }]
  },
  children: [
    {
      object: 'block',
      type: 'paragraph',
      paragraph: { rich_text: [{ text: { content: 'Hello' } }] }
    }
  ]
});
```

### Query Database

```typescript
import { APIQueryDataSource } from '@connections/notion';

const results = await APIQueryDataSource({
  data_source_id: 'database-id',
  filter: {
    property: 'Status',
    status: { equals: 'In Progress' }
  },
  sorts: [{ property: 'Due Date', direction: 'ascending' }]
});
```

## Property Types

| Type | Format |
|------|--------|
| Title | `{ title: [{ text: { content: 'value' } }] }` |
| Rich Text | `{ rich_text: [{ text: { content: 'value' } }] }` |
| Number | `{ number: 42 }` |
| Select | `{ select: { name: 'Option' } }` |
| Multi-select | `{ multi_select: [{ name: 'Tag' }] }` |
| Status | `{ status: { name: 'Done' } }` |
| Date | `{ date: { start: '2024-01-01' } }` |
| Checkbox | `{ checkbox: true }` |

## Block Types

`paragraph`, `heading_1`, `heading_2`, `heading_3`, `bulleted_list_item`, `numbered_list_item`, `to_do`, `toggle`, `code`, `quote`, `callout`, `divider`, `table`, `image`, `video`, `file`

## Common Errors

| Error | Solution |
|-------|----------|
| "object not found" | Verify ID is correct and accessible |
| "validation_error" | Check property names match schema |
| "unauthorized" | Ensure integration has access |
| 422 | Pass `{}` for tools with no required params |

## Output Format

Present results as a structured report:
```
Managing Notion Report
══════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

