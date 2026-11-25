---
name: data-extraction
description: "Extract structured data from authenticated pages: tables, lists, paginated content, and multi-page scraping via the user's real browser session."
---

# Data Extraction

Extract structured data from authenticated pages that automated scrapers
cannot reach. Uses the user's real browser session, so cookies, CSRF tokens,
and login state are already handled.

## When to Use

- Scraping data from pages behind login (dashboards, admin panels, private
  boards, intranets)
- Extracting structured data from pages with CAPTCHAs or bot detection that
  block headless browsers
- Collecting visible page content when API access is unavailable
- Monitoring pages that require authentication on a schedule

## Workflow

### 1. Verify Connection

Call `list_browsers`. If no browsers are connected, ask the user to connect.

### 2. Navigate (If Needed)

Brijio does **not** navigate. The user must have the target page
open in their browser before extraction begins. If the user is on the wrong
page, ask them to navigate to the correct URL and confirm when ready.

### 3. Read the Page

Call `read_current_page` with appropriate parameters:

- `includeContent: true` — includes readable text content chunks
- `maxContentChunks: N` — limit chunks for large pages (default: 1, increase
  for pages with more content)

The response contains:

- `page.title` — page title
- `page.url` — current URL
- `links` — navigation links with IDs, text, and hrefs
- `actions` — buttons and interactive elements
- `forms` — form structures with controls and current values
- `editables` — contenteditable areas with their text
- `content` (when `includeContent: true`) — readable text chunks

### 4. Extract Structured Data

Parse the page context into structured data based on the extraction target:

#### Tables

Look for content chunks that contain tabular data. Extract rows and columns
into a structured array of objects:

```
[
  { "name": "John", "role": "Admin", "status": "Active" },
  { "name": "Jane", "role": "Editor", "status": "Inactive" }
]
```

#### Lists and Cards

Many pages render data as card lists or `<ul>/<ol>` structures. Extract each
item with its attributes.

#### Form Values (Data from Inputs)

If the target data is inside form fields (e.g., a profile edit form), extract
from `forms[].controls[].value` — each control has a `label`, `type`, and
`value`.

#### Mixed Content

For pages with mixed content (text + tables + forms), use the content
chunks alongside the structured form/link data to build a complete picture.

### 5. Handle Pagination

For multi-page data sets:

1. Read the current page and extract all data.
2. Look for "Next" or pagination links in the `links` array.
3. Ask the user to click "Next" (Brijio can click pagination links,
   but the user should confirm for authenticated pages).
4. After the page updates, call `read_current_page` again.
5. Accumulate data from all pages.
6. Continue until no more "Next" links appear.

### 6. Output Format

Return extracted data in the format the user requested:

- **JSON** — structured objects, best for programmatic use
- **CSV** — tabular data, best for spreadsheets
- **Markdown table** — human-readable, best for reports
- **Summary** — key findings and statistics, best for quick overviews

## Pitfalls

### Content Chunk Limits

`maxContentChunks` defaults to 1. For pages with significant text content
(articles, documentation, long lists), increase this to 5–20 to capture
all content. Each chunk is typically 500–2000 characters.

### Dynamic Content (SPAs)

Single-page applications may not show all data in the initial page load.
Content that loads via JavaScript after the page renders may not appear in
the first read. Ask the user to scroll or wait for content to load, then
re-read the page.

### Infinite Scroll

Pages with infinite scroll only show a limited number of items. For complete
extraction, the user must scroll down to load all items. Coordinate with the
user to scroll incrementally, re-reading the page after each scroll.

### Short-Lived IDs

Element IDs expire on page navigation. When extracting across multiple
pages, always re-read after any navigation.

### Auth-Dependent Content

The extracted content reflects what the **user's browser** sees. If the user
has different roles or permissions, the data will differ. Confirm with the
user that their account has the visibility needed for the extraction.

### Rate Limiting

Brijio requests go through the user's real browser. Rapid repeated
calls may trigger rate limiting or anti-bot protections on the target site.
Add small delays between reads if extracting from multiple pages.

## Example: Extract Team Members from a Dashboard

```
1. list_browsers → Confirm browser connected
2. read_current_page(includeContent: true, maxContentChunks: 5)
3. Parse content for team member entries:
   - Each member has: name, role, email, status
4. For pagination:
   - Check links for "Next" button
   - Click "Next" → re-read → extract → accumulate
5. Return structured JSON:
   {
     "members": [
       { "name": "Alice Johnson", "role": "Admin", "email": "alice@co.com", "status": "Active" },
       { "name": "Bob Smith", "role": "Developer", "email": "bob@co.com", "status": "Active" }
     ],
     "total": 47,
     "extracted": 47,
     "pages": 5
   }
```
