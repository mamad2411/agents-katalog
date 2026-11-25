# service-io

Mechanical filesystem, shell, web search, and HTTP fetch. Does not call LLMs or other Quark services.

## Filesystem

- `io_Read` — read text; optional `start_line` / `end_line` (1-based inclusive)
- `io_List` — list directory; `recursive`, `include_hash`
- `io_Stat` — metadata; set `include_hash` for sha256 on regular files
- `io_ReadMedia` — read bounded image/document bytes; runtime exposes only an opaque media reference to the agent
- `io_Write`, `io_Append`, `io_Replace` — atomic file mutations; require `approved: true` after explicit user approval
- `io_Remove` — admin-risk file or directory removal; requires `approved: true` after explicit user approval

## Shell

- `io_Execute` — runs a non-empty `bash -c` command; requires `approved: true`

## Network

- `io_SearchWeb` — `query`, `max_results`; needs `BRAVE_API_KEY` or `SERPAPI_KEY` on the service process
- `io_Fetch` — GET/HEAD only; `url`, optional `max_bytes`, `timeout_seconds`, `max_redirects`; private and link-local network targets are blocked

## Indexing

For directory discovery use `io_List` / `io_Stat`. When a source is being indexed, its content evidence belongs to document service functions rather than `io_Read`.
