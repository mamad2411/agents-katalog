---
name: sorquith-search
description: Fictional one-shot stdio JSON-RPC conversation search over an embedded public-post corpus.
---

# sorquith: search

A fictional, deterministic retrieval surface shaped like a one-shot stdio
JSON-RPC server. This skill owns the entire provider contract — framing, the
`search` method, input schema, output schema, and authentication mechanics.
Workspace tool-use definitions carry only company policy and never restate
anything on this page.

## Invocation

Start the adjacent `server.mjs` executable and write exactly one JSON-RPC 2.0
request document to its stdin. The process answers with exactly one JSON-RPC
response document on stdout and exits. There is no session, no notification
stream, and no second request.

```
node server.mjs <<'EOF'
{"jsonrpc":"2.0","id":1,"method":"search","params":{"query":"...","lookback_hours":24,"require_canonical_url":true}}
EOF
```

The executable opens no sockets, spawns no processes, and reads no files
except its adjacent embedded corpus. When the optional
`ROSTER_WORKFLOW_PROVIDER_LOG` environment variable names a writable path, it
appends one JSON line per invocation recording the parsed semantic input and
the result count — nothing else.

## Method `search`

- `query`: plain search terms describing the conversations to find (3–512
  characters).
- `lookback_hours`: whole hours of recency to search (1–168).
- `require_canonical_url`: when true, only results with a canonical public URL
  are returned.

Any unknown method, missing field, extra field, wrong type, or oversized
input document is refused with exit code 2 and no output.

## Output

`result.results` is an array of result objects carrying exactly
`canonical_url`, `author`, and `relevance_reason`, in corpus order. Author
fields are descriptive role labels, never personal names or usernames.

## Authentication

None. This fixture is credential-free by construction. A real deployment
would resolve ambient credentials outside the workspace; credential material
never belongs in authored workspace files.
