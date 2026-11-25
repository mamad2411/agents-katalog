---
name: nyxid-business-setup-worker
description: CMA worker procedure for nyxid-business-starter. Use when a task block starts with TASK notion-hub or TASK faq-research. Builds a small business's Notion hub (FAQ page, Bot rules page, Queue and Reservations databases) under a parent page with the bundled notion_hub.py script, or researches the business from official sources, the menu and its Google listing and appends a sourced FAQ. Ends with a SETUP_RESULT JSON line. Never contacts customers.
version: "1.5"
metadata:
  category: mixed
  output-type: text
  runtime:
    - python3
  tool-list:
    - nyx__call_tool
    - nyx__search_tools
  tag:
    - cma
    - notion
    - small-business
    - faq
---

# Setup worker

You receive one task block per input. Do exactly that task, then finish with a
single line `SETUP_RESULT: {json}`.

## Access

Use only NyxID's published operations, through the bundled
`scripts/notion_hub.py` (copy it into the workspace and run it with python3):

- `hub`, `verify`, `append` build and check the Notion hub with the owner's
  Notion connection (`{NOTION_SERVICE}__notion_create_database`,
  `__notion_create_page`, `__notion_append_block_children`,
  `__notion_list_block_children`, `__notion_retrieve_database`).
- `call TOOL --args JSON|@file` runs any other published operation, for example
  `api-firecrawl__scrape` or `tools-firecrawl__search`, and prints its result.

The script uses `nyxid mcp call` when available and otherwise NyxID's MCP
endpoint with the sandbox's NyxID credential. When NyxID's MCP endpoint refuses
that credential (CMA sandboxes reach NyxID through a local broker), the script
runs the same published operations, exactly as NyxID's MCP config lists them,
through `nyxid proxy request`; this is expected, not an error. Never write your
own proxy requests, use other credentials or other connections, and never touch
pages outside PARENT_PAGE_ID. The script is idempotent (reuses pages and
databases with the same title, never deletes) and prints one JSON line; on
failure it prints the error. Include that error text in SETUP_RESULT
`problems`; never discard an error. If an operation is refused or missing,
stop and report it.

## TASK notion-hub

1. Write RULES from the task block to `rules.json` (keys listed in the script
   docstring; add `business` and `timezone`).
2. Run `python3 notion_hub.py hub --service {NOTION_SERVICE} --parent
   {PARENT_PAGE_ID} --modules {MODULES} --rules rules.json`.
3. If it fails on a transient network error, run it again (it is safe to repeat).
   If it fails on a Notion or NyxID error, stop and report it. A reused
   database with missing properties is reported in `problems`, not altered.
4. Run `python3 notion_hub.py verify ...` and include its schema problems.
5. Result: `{"task":"notion-hub","faq_page_id":...,"rules_page_id":...,
   "queue_db_id":...,"reservations_db_id":...,"reused":[...],"problems":[...]}`.

## TASK faq-research

Follow references/faq-research.md (Firecrawl for every web read). Write the
finished customer-facing FAQ as markdown (only `## `, `- ` and plain lines) to
`faq.md`, then run `python3 notion_hub.py append --service {NOTION_SERVICE}
--page {FAQ_PAGE_ID} --markdown faq.md`. Result: `{"task":"faq-research","sections_written":[...],
"open_questions":n,"sources":n,"unreadable_sources":[...],"problems":[...]}`.
Also include the "Open questions for owner" list in your final message so the
owner can answer them.
