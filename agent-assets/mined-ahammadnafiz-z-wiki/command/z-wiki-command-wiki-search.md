---
description: Grep-first ranked search over the compiled wiki. Prints results; writes nothing.
argument-hint: "<query>"
when_to_use: Use when the user wants to browse the wiki without filing an answer — "search the wiki for X", "what pages mention X", "find pages tagged Y". This is a read-only substrate for /wiki-query; /wiki-query invokes it internally. Unlike /wiki-query, it does not synthesize an answer or consume tokens on page bodies.
allowed-tools: Bash
---

# Wiki Search

Grep-first ranked search over `wiki/.meta/search-index.tsv`. Fast at
any vault size. Zero context cost beyond the results printed.

## The query

$ARGUMENTS

## Dispatch

1. If `wiki/.meta/search-index.tsv` is missing, run
   `python3 scripts/build_meta.py` first.
2. Invoke:

   ```bash
   python3 scripts/wiki_search.py "<query>"
   ```

   Pass through flags if the user's request implies them:
   - `--type sources|concepts|entities|syntheses|outputs` when they
     say "sources about X", "concepts for Y", etc.
   - `--tag <tag>` when they say "tagged X" or "#X".
   - `--limit N` when they ask for "top N" or "more results".

3. Print the raw output. Do not summarise unless the user asks. Do
   not file anything.

## When to reach for `/wiki-query` instead

- User wants a *synthesised answer*, not a list of pages.
- User needs citations compiled into an output file.
- Question requires reading multiple pages to reconcile.

`/wiki-search` is the browse primitive. `/wiki-query` is the answer
primitive.

## Failure modes

- No matches → print `no matches` (already the default from
  `wiki_search.py`). Suggest `/wiki-add <url>` or `/wiki-init` if the
  vault is empty.
- Sidecar missing → rebuild it and retry once. If it still fails,
  tell the user to run `python3 scripts/build_meta.py` manually.
