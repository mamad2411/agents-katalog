---
name: setup-source
description: Build the local source adapter OpenArc needs (openarc_adapter.py) so `openarc patrol` can search and reply. Use when `openarc patrol` reports no source adapter is configured, when the user asks to "set up the source" / "build the adapter" / "connect OpenArc to my source", or when it stopped working and needs re-fitting to the source's current interface.
---

# Build OpenArc's source adapter

OpenArc ships no code for talking to any post source. It
reaches its source through one small seam you implement locally, for the source the
**user** is authorized to use, on the user's own account/session. Your job is to write
`openarc_adapter.py` in the repo root so it satisfies that seam. The user is
responsible for complying with their source's terms of service — surface that, don't
work around it.

## The contract

`openarc_adapter.py` must expose `create_source(config)` returning an object with two
methods (the `PostSource` seam in `src/openarc/source.py`):

```python
def search(self, keyword: str, since: datetime) -> list[Post]: ...
def publish_reply(self, post_id: str, text: str) -> None: ...
```

- `Post` is `openarc.source.Post` — `id`, `author_id`, `author_username`, `text`,
  `permalink`, `posted_at` (ISO-8601 string). `id` and `author_id` must be stable per
  post/author (OpenArc dedupes and rate-limits on them).
- `search` returns posts matching `keyword`, none older than `since`, newest first.
- A successful search with no matches returns `[]`. Authentication failures, rate
  limits, request/schema drift, parser failures, and API-level errors must raise an
  exception so OpenArc never reports them as an empty market result. For GraphQL-style
  APIs, inspect the response body for `errors` even when HTTP status is 200.
- `publish_reply` posts `text` as a reply to `post_id`.
- Read any secrets the source needs (a key, a session token, ...) from the environment
  **inside the adapter** — OpenArc's config knows nothing about them.
- Manage the source's session/auth lazily inside these methods.

Start from `openarc_adapter.example.py` — copy it to `openarc_adapter.py` and fill in
the two methods.

## How to build it

The user has to supply what only they have: which source, and how their client reaches
it. Ask them for it — don't invent endpoints or guess at a private interface.

1. **Get the source's shape from the user.** The reliable way: ask the user to perform
   the action once in their own logged-in browser/app (a search; a reply) and hand you
   the resulting request(s) — e.g. "copy as fetch" from the browser's network panel, or
   an equivalent capture. That request, made from the user's own session, is the ground
   truth for what to reproduce. In DevTools, filter Network requests by
   `graphql` and inspect `operationName`; for this Threads flow, useful search hints are
   `SearchResultsQuery` and `configure_text_only_post`. They are search terms, not a
   promise that the interface will remain unchanged. Save the capture as a local UTF-8
   file instead of pasting it through a PowerShell command line.
2. **Reproduce it in `search` / `publish_reply`** using `httpx`, mapping the response
   into `Post` objects. Replay the complete captured request when the source uses a
   private or versioned web interface; only replace fields known to vary, such as the
   query. Do not guess that apparently redundant request fields are safe to remove.
   Keep credentials out of the code — pull them from the environment.
3. **Verify** with `openarc pending` empty and one real `openarc patrol`: it should
   return posts (or a clean empty result), not raise. Then let the user review drafts in
   `openarc queue` before anything is published.

## Windows/PowerShell encoding

- Do not put Chinese request bodies or reply text directly inside a PowerShell command,
  `echo`, `Out-File` default, or `cmd /c` string. Write a UTF-8 file and pass its path.
- For a draft reply containing non-ASCII text, use:

  ```text
  openarc draft <post_id> --text-file <utf8_reply_file>
  ```

  OpenArc accepts UTF-8 with or without a BOM. Use the harness file writer or an explicit
  UTF-8 writer; a console that displays `??` is not proof that the file is corrupted.
- For diagnostics in Windows PowerShell, set `$OutputEncoding` and
  `[Console]::OutputEncoding` to UTF-8 before printing. `openarc pending` intentionally
  emits escaped JSON so non-ASCII text survives every terminal encoding.

## When it stops working

Source interfaces change. If `patrol` starts returning nothing or erroring, the request
you reproduced has drifted — ask the user for a fresh capture and re-fit `search` /
`publish_reply` to it. Same skill, same steps.

## Keep it narrow

This adapter is the user's personal automation over their own access. Keep it to what the
patrol needs — search and reply — at a human pace. Don't add bulk-scraping, multi-account,
or evasion behavior; if the user asks for those, say no and explain why (it raises both
account and legal risk, and it's outside what this tool is for).
