---
name: add-pagination
description: Adds pagination to a list endpoint in the style your project already uses, with a stable order and updated tests.
disable-model-invocation: true
---

Add pagination to: $ARGUMENTS

1. Read the endpoint and the query behind it. Search other list endpoints for an existing convention (page and limit, offset, or cursor) and follow it. If there is none, prefer cursor paging for large or changing tables and page numbers for small admin lists, and say which you chose.
2. Add a default and a hard maximum page size, and validate both inputs.
3. Make the order deterministic: add a unique tiebreaker such as id after the sort column.
4. Return the project's envelope with items plus total or next cursor, whichever fits the chosen style. Avoid an expensive COUNT on huge tables unless the convention requires it.
5. Check that an index supports the sort and filter; if not, name the index to add but do not create it.
6. Update tests: first page, middle page, last page, empty result, limit above the maximum, invalid cursor.
7. Run the tests.

Report the new request and response shape, and the index suggestion if any.
