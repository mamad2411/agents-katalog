---
name: notion
description: Work with the Notion API using configured auth, databases, data sources, pages, search, querying, and updates.
version: 1.0.0
tags: [api, notion, workspace]
---

# Notion API

## When To Use
Use this skill when a task requires interacting with Notion through its REST API:
finding pages or data sources, creating or updating databases, managing data
source schemas, creating or updating pages, moving or trashing pages, reading or
updating markdown page content, querying rows, or diagnosing Notion API errors.

## Integration And Broker Rules
Use `http_request` with `integration: "notion"` for all Notion API calls.

- Integration names are an authorization boundary. Use only names listed in the
  execution context under `Configured integrations`.
- Never set `Authorization` or other protected auth headers directly.
  Credentials are injected by the host-side broker.
- Never ask the user to paste raw API tokens into task text.
- Use base URL `https://api.notion.com`.
- For JSON write requests, set `Content-Type: application/json`.
- Prefer a host-side default header `Notion-Version: 2026-03-11` in
  `secrets.yaml`. If the configured version is older, modern `data_sources` and
  markdown-content endpoints may fail or behave differently.
- If `integration: "notion"` is unavailable or the broker denies access, report
  inability with the broker reason.

## Operating Model
1. Identify whether the task is about discovery, a database container, a data
   source schema/table, page properties, page content, or search.
2. If the user gives a database URL or ID and needs rows or schema, first call
   `GET /v1/databases/{database_id}` to discover child `data_sources`.
3. Use `data_source_id` for row-oriented work: querying rows, creating rows,
   retrieving schemas, updating schemas, listing templates, or moving pages into
   a table.
4. Retrieve schemas before writing page properties unless property names and
   types are already known.
5. Inspect Notion error bodies and adjust request shape rather than repeating
   failed calls unchanged.
6. For paginated responses, continue while `has_more` is true using
   `next_cursor` as `start_cursor`.
7. If broker returns `policy_denied`, include `requested_method`,
   `requested_url`, and `reason` in your report and do not retry the same denied
   request.
8. If broker returns `rate_limited`, wait and retry once, or report the
   limitation when waiting is not appropriate.
9. Summarize created/updated object IDs, URLs, and any partial failures.

## IDs, Permissions, And Versioning
A Notion integration must have the needed capabilities, and the target page,
database, or data source must be shared with the integration. A 404 can mean the
resource exists but is not shared with the integration.

Modern Notion APIs split databases and data sources:

- A database is a container that can have one or more child data sources.
- A data source is the table/schema whose children are pages.
- Pages inside a data source are rows. Page property values must match the data
  source property schema.
- Retrieve a database to find its `data_sources`; retrieve a data source to find
  its `properties`.
- Legacy database query/list APIs are deprecated for modern API versions. Prefer
  Search for discovery and data source query for table rows.

## Request Template
The examples below show the `args` payload for the `http_request` tool. In
native tool-call mode, call `http_request` with these fields as function
arguments. In prompt-structured mode, wrap the same object under
`{"tool":"http_request","args":...}`.

Use this argument shape for every Notion API call:

```json
{
  "method": "GET",
  "url": "https://api.notion.com/v1/...",
  "integration": "notion",
  "headers": {},
  "body": null
}
```

Important strangeClaw details:

- Do not add an `"action"` field. The `http_request` tool adds
  `"action": "http_request"` internally when it calls the broker.
- `body` must be either `null` or a JSON-encoded string. Do not pass a nested
  object as `body`.
- Use `body: null` for `GET` requests.
- Do not include `Authorization`; the broker injects it from
  `credentials.notion`.
- The broker should usually add `Notion-Version` from
  `credentials.notion.default_headers`, so examples omit it.

For write requests:

```json
{
  "method": "POST",
  "url": "https://api.notion.com/v1/...",
  "integration": "notion",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"key\":\"value\"}"
}
```

## Search Endpoints
Use Search to discover pages and data sources shared with the integration.

### Search by title
`POST /v1/search`

Body fields:

- `query`: optional title text. If omitted, returns shared pages/data sources.
- `filter`: optional object filter. Use `{"property":"object","value":"page"}`
  or `{"property":"object","value":"data_source"}`.
- `sort`: optional, commonly by `last_edited_time`.
- `start_cursor`, `page_size`: pagination controls.

Example: find data sources with a title:

```json
{
  "method": "POST",
  "url": "https://api.notion.com/v1/search",
  "integration": "notion",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"query\":\"Tasks\",\"filter\":{\"property\":\"object\",\"value\":\"data_source\"},\"sort\":{\"direction\":\"descending\",\"timestamp\":\"last_edited_time\"},\"page_size\":10}"
}
```

Use Query a data source, not Search, when the task is to search rows inside one
known table.

## Database Endpoints
Use database endpoints for the database container and its child data source list,
not for row queries.

### Create a database and initial data source
`POST /v1/databases`

Creates a database under a parent page or workspace and creates its initial data
source. Include `initial_data_source.properties` when defining the initial
schema.

```json
{
  "method": "POST",
  "url": "https://api.notion.com/v1/databases",
  "integration": "notion",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"parent\":{\"type\":\"page_id\",\"page_id\":\"<parent_page_id>\"},\"title\":[{\"text\":{\"content\":\"Tasks\"}}],\"initial_data_source\":{\"title\":[{\"text\":{\"content\":\"Tasks\"}}],\"properties\":{\"Name\":{\"title\":{}},\"Status\":{\"status\":{}},\"Due\":{\"date\":{}}}}}"
}
```

### Retrieve a database
`GET /v1/databases/{database_id}`

Use this to inspect database metadata and discover child `data_sources`.

```json
{
  "method": "GET",
  "url": "https://api.notion.com/v1/databases/<database_id>",
  "integration": "notion",
  "headers": {},
  "body": null
}
```

### Update a database
`PATCH /v1/databases/{database_id}`

Use this for database metadata only: title, description, icon, cover,
`is_inline`, `in_trash`, `is_locked`, or parent move. To update schema columns,
use `PATCH /v1/data_sources/{data_source_id}`.

```json
{
  "method": "PATCH",
  "url": "https://api.notion.com/v1/databases/<database_id>",
  "integration": "notion",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"title\":[{\"text\":{\"content\":\"Updated Tasks\"}}]}"
}
```

## Data Source Endpoints
Use data source endpoints for table schemas, rows, templates, and row queries.

### Create a data source
`POST /v1/data_sources`

Adds another data source to an existing database. The `parent.database_id` is
required. A standard table view is created automatically.

```json
{
  "method": "POST",
  "url": "https://api.notion.com/v1/data_sources",
  "integration": "notion",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"parent\":{\"database_id\":\"<database_id>\"},\"title\":[{\"text\":{\"content\":\"Bugs\"}}],\"properties\":{\"Name\":{\"title\":{}},\"Priority\":{\"select\":{\"options\":[{\"name\":\"High\",\"color\":\"red\"},{\"name\":\"Low\",\"color\":\"blue\"}]}}}}"
}
```

### Retrieve a data source
`GET /v1/data_sources/{data_source_id}`

Use this before creating/updating pages when property names, IDs, or types are
unknown. The response contains the `properties` schema.

```json
{
  "method": "GET",
  "url": "https://api.notion.com/v1/data_sources/<data_source_id>",
  "integration": "notion",
  "headers": {},
  "body": null
}
```

### Query a data source
`POST /v1/data_sources/{data_source_id}/query`

Returns pages contained in the data source. Use `filter`, `sorts`,
`start_cursor`, `page_size`, and `filter_properties` as needed. Add
`filter_properties[]` query parameters to reduce large responses.

```json
{
  "method": "POST",
  "url": "https://api.notion.com/v1/data_sources/<data_source_id>/query?filter_properties[]=Name&filter_properties[]=Status",
  "integration": "notion",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"filter\":{\"property\":\"Status\",\"status\":{\"equals\":\"Done\"}},\"sorts\":[{\"property\":\"Due\",\"direction\":\"ascending\"}],\"page_size\":50}"
}
```

For wikis, query results can include pages or data sources. Use a `result_type`
filter such as `"page"` or `"data_source"` when only one type is wanted.

### Update a data source
`PATCH /v1/data_sources/{data_source_id}`

Use this for schema or data source metadata updates: `title`, `description`,
`icon`, `properties`, `in_trash`, or moving to another database with `parent`.
Set a property key to `null` to remove it. This endpoint does not update row
values; use Update page for row/page properties.

```json
{
  "method": "PATCH",
  "url": "https://api.notion.com/v1/data_sources/<data_source_id>",
  "integration": "notion",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"properties\":{\"Priority\":{\"select\":{\"options\":[{\"name\":\"High\",\"color\":\"red\"},{\"name\":\"Low\",\"color\":\"blue\"}]}},\"Obsolete\":null}}"
}
```

Schema caveats:

- API schema updates cannot update `formula`, `status`, synced content, or
  `place` properties.
- Data source schema updates that are too large can be rejected. Prefer keeping
  schemas small and removing unused properties.
- Relation properties require the related database to be shared with the
  integration.

### List data source templates
`GET /v1/data_sources/{data_source_id}/templates`

Use this when creating pages from templates or inspecting available templates.
Supports `name`, `start_cursor`, and `page_size`.

```json
{
  "method": "GET",
  "url": "https://api.notion.com/v1/data_sources/<data_source_id>/templates?page_size=100",
  "integration": "notion",
  "headers": {},
  "body": null
}
```

## Page Endpoints
Use page endpoints for page properties, icons/covers, moving/trashing/locking,
templates, and content.

### Create a page
`POST /v1/pages`

For a page inside a data source, use `parent.data_source_id` and provide
`properties` matching the data source schema. For a child page under another
page, use `parent.page_id`; in that case `title` is the only valid property.

You can provide page content either as `children` blocks or as `markdown`.
`markdown` is mutually exclusive with `children` and `content`.

Create a data source row:

```json
{
  "method": "POST",
  "url": "https://api.notion.com/v1/pages",
  "integration": "notion",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"parent\":{\"data_source_id\":\"<data_source_id>\"},\"properties\":{\"Name\":{\"title\":[{\"text\":{\"content\":\"Write release notes\"}}]},\"Status\":{\"status\":{\"name\":\"Not started\"}}}}"
}
```

Create a child page with markdown content:

```json
{
  "method": "POST",
  "url": "https://api.notion.com/v1/pages",
  "integration": "notion",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"parent\":{\"page_id\":\"<parent_page_id>\"},\"markdown\":\"# Meeting Notes\\n\\nDiscussed roadmap priorities.\"}"
}
```

Generated properties such as rollups, created time, last edited time, created
by, and last edited by cannot be set directly.

### Retrieve a page
`GET /v1/pages/{page_id}`

Use this to inspect page properties, parent, URL, icon, cover, trash status, and
lock status. This does not return full page body content; use markdown content
or block children endpoints for content.

```json
{
  "method": "GET",
  "url": "https://api.notion.com/v1/pages/<page_id>",
  "integration": "notion",
  "headers": {},
  "body": null
}
```

### Retrieve a page property item
`GET /v1/pages/{page_id}/properties/{property_id}`

Use this when a page property has more than 25 references or when you need a
specific property value. Supports `start_cursor` and `page_size` for paginated
property types such as `title`, `rich_text`, `relation`, and `people`.

```json
{
  "method": "GET",
  "url": "https://api.notion.com/v1/pages/<page_id>/properties/<property_id>?page_size=100",
  "integration": "notion",
  "headers": {},
  "body": null
}
```

### Update a page
`PATCH /v1/pages/{page_id}`

Use this to update page properties, icon, cover, `is_locked`, template
application, `erase_content`, or `in_trash`. Use `in_trash: true` to trash a
page and `in_trash: false` to restore it. The API does not permanently delete
pages.

```json
{
  "method": "PATCH",
  "url": "https://api.notion.com/v1/pages/<page_id>",
  "integration": "notion",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"properties\":{\"Status\":{\"status\":{\"name\":\"Done\"}}},\"is_locked\":false}"
}
```

Limitations:

- `properties` updates only work for pages in a data source, except for title
  updates on pages outside a data source.
- A page's `parent` cannot be changed with this endpoint. Use Move page.
- Updating rollup property values is not supported.
- To add block content with the block API, use Append block children with the
  page ID as `block_id`.

### Move a page
`POST /v1/pages/{page_id}/move`

Use this to move an existing regular page under another page or into a data
source. Moving databases or non-page blocks is not supported. Use
`data_source_id`, not `database_id`, when moving a page into a table.

```json
{
  "method": "POST",
  "url": "https://api.notion.com/v1/pages/<page_id>/move",
  "integration": "notion",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"parent\":{\"type\":\"data_source_id\",\"data_source_id\":\"<data_source_id>\"}}"
}
```

### Retrieve page content as markdown
`GET /v1/pages/{page_id}/markdown`

Use this for agentic reading of page body content. The response contains
`markdown`, `truncated`, and `unknown_block_ids`. If truncated, pass an unknown
block ID to this endpoint to fetch that subtree separately.

```json
{
  "method": "GET",
  "url": "https://api.notion.com/v1/pages/<page_id>/markdown?include_transcript=false",
  "integration": "notion",
  "headers": {},
  "body": null
}
```

### Update page content as markdown
`PATCH /v1/pages/{page_id}/markdown`

Prefer `update_content` for targeted search-and-replace or `replace_content`
for a full replacement. `insert_content` and `replace_content_range` are legacy
options and should be used only when specifically needed. Use
`allow_deleting_content: true` only when deletion of child content is intended.

```json
{
  "method": "PATCH",
  "url": "https://api.notion.com/v1/pages/<page_id>/markdown",
  "integration": "notion",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"type\":\"update_content\",\"update_content\":{\"content_updates\":[{\"old_str\":\"existing text\",\"new_str\":\"replacement text\"}]}}"
}
```

Full replacement example:

```json
{
  "method": "PATCH",
  "url": "https://api.notion.com/v1/pages/<page_id>/markdown",
  "integration": "notion",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"type\":\"replace_content\",\"replace_content\":{\"new_str\":\"# New content\\n\\nBody text.\"}}"
}
```

## Common Property Shapes
Use exact property names or property IDs from the data source schema.

```json
{
  "Name": {"title": [{"text": {"content": "Title"}}]},
  "Description": {"rich_text": [{"text": {"content": "Details"}}]},
  "Done": {"checkbox": true},
  "Due": {"date": {"start": "2026-06-01"}},
  "Status": {"status": {"name": "Done"}},
  "Priority": {"select": {"name": "High"}},
  "Tags": {"multi_select": [{"name": "API"}, {"name": "Docs"}]},
  "URL": {"url": "https://example.com"},
  "Email": {"email": "user@example.com"},
  "Phone": {"phone_number": "+1 555 0100"},
  "Number": {"number": 42},
  "Relation": {"relation": [{"id": "<page_id>"}]},
  "People": {"people": [{"id": "<user_id>"}]}
}
```

## Pagination
For list responses, repeat the same endpoint with `start_cursor` set to the
previous `next_cursor` while `has_more` is true. Keep `page_size` reasonable
(often 50 or 100). For data source queries, put pagination fields in the JSON
body. For page property items and data source templates, use query parameters.

## Error Handling
Notion error bodies usually include `object`, `status`, `code`, and `message`.
Report these fields when present.

- 400: malformed request, wrong property shape, invalid filter, old API version,
  unsupported markdown operation, or schema too large.
- 401: integration credential is invalid or missing.
- 403: integration lacks required capabilities such as read content, insert
  content, update content, or insert/update property.
- 404: wrong ID or resource not shared with the integration.
- 409: conflict; retry only if the operation is safe and idempotent.
- 429: rate limited; retry once with wait or report limitation.
- 503/504: transient backend issue; retry with backoff or narrow the query.

When a request fails, inspect both HTTP status and JSON error body before
deciding whether to retry, alter the request, ask the user for missing IDs, or
report a permission/configuration issue.
