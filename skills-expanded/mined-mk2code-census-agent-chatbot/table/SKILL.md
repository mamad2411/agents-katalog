---
name: table
description: >-
  Build a markdown table comparing census numbers across districts/regions. Use when the user asks for a "table", "list", or "data dump" of metrics.
---

# Table recipe

1. GET THE DATA from tools, never from memory:
   - one metric across districts → `query_tables` on the relevant statement CSV;
   - a few values from prose → `search_census` and record each chunk_id.
2. Render a markdown table in your response AND save a CSV version to the artifacts directory using `execute_python`.
   - Rules for CSV: save it with a descriptive name ending in `.csv` into `OUTPUT_PATH` (provided by the sandbox environment).
3. Reply with `kind="artifact"` if saving a CSV: `artifacts=[filename]` (name only, without directory path), `answer_md` = the markdown table and a brief takeaway, and a claim citing every page/chunk the numbers came from.

## Gotchas
- Sex ratio = females per 1000 males. NEVER convert it to a percentage.
- Growth rates in the docs are already percentages — do not recompute from absolutes unless necessary due to district boundary changes.
