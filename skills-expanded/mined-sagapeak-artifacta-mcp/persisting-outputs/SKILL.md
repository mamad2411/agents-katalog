---
name: persisting-outputs
description: Use when a run produces outputs worth keeping beyond the current session — reports, datasets, generated files, analysis results, build outputs — or when the user asks to save, share, or hand off work products, or wants something back from a previous run. Persists files to Artifacta with session and agent metadata, retrieves earlier artifacts, and shares them via expiring download links or public pages.
---

# Persisting outputs with Artifacta

Artifacta is an artifact store built for AI agents: a hosted MCP server plus a
Python CLI/SDK, backed by tenant-scoped storage with sessions, TTLs, and
shareable links. This skill covers storing a run's outputs, finding them
again later, and handing them off to a human or another system.

## Check the connection first

Before a batch of work that will produce outputs, call `whoami` once. It
takes no arguments and returns the tenant name, plan tier, current usage
(`usage_requests_month`, `usage_storage_bytes`), the plan's limits
(`plan_requests_limit_month`, `plan_storage_limit_bytes`), active link counts,
and rate limits. Use it to confirm the connection works and to size what you
are about to do against quota — don't discover a storage cap mid-run.

If `whoami` or the other Artifacta tools are not available in this session
(no MCP connection), skip to **CLI fallback** below.

## When to persist — and when not to

Persist:
- End-of-run deliverables: reports, generated files, datasets, build
  artifacts, anything the user would want back after the session ends.
- Intermediates that are expensive to regenerate (long computations, large
  fetches) even if not a final deliverable.
- Anything the user explicitly asks you to save, share, or hand off.

Don't persist:
- Throwaway scratch files with no value once the current step finishes.
- Secrets, credentials, or other sensitive material the user hasn't asked
  you to store.
- Anything you're unsure about — ask the user rather than guessing either
  way.

## Storing artifacts

`store_artifact` uploads a file in one call. It requires `filename`, plus
exactly one of `content` or `path` — and which one is safe depends on where
the MCP server runs:

**Hosted MCP or the Claude Code plugin (`mcp.artifacta.io`): never use
`path`.** The server runs remotely, so a `path` argument resolves on the
server's own container filesystem — not the machine your files are on — and
fails or reads the wrong file. Always send `content` (base64-encoded bytes,
up to 10 MB decoded); for anything larger, use the large-file flow below.

**Local stdio server only** (launched on this machine via npx/pipx with an
`ak_live_` key): `path` — an absolute local path inside the server's
`--allow-path` allow-list — streams the file server-side and handles up to
500 MB. If you aren't certain the server is local, use `content`.

Files larger than 500 MB always need the large-file flow below.

Attribution and organization, all optional:
- `session_id` — groups this artifact with others from the same run.
- `agent_id` — defaults to the connected MCP client's name (or `"mcp"`) if
  you omit it, so provenance is never blank.
- `model` — **always pass this**, using the exact model ID from your system
  prompt (e.g. `"claude-fable-5"`); it is stored as `metadata.model` unless
  you've already set that key yourself. If a subagent produced this artifact
  end-to-end, pass its model, not yours. This is a declared producer claim —
  never describe it as a verified model.
- `metadata` — an object of string values. Keys must match
  `^[a-zA-Z][a-zA-Z0-9_-]{0,63}$` (no dots, no leading digit), values capped
  at 1024 characters.
- `ttl` — a duration like `"7d"` / `"30d"`, or `"never"` (Pro only).
  Defaults to the plan default if omitted.
- `content_type` — guessed from the filename if omitted.
- `transcript` — set `true` when storing a conversation/session log: it
  tags the artifact `metadata.type=transcript` and defaults the content
  type to `application/x-ndjson` (explicit values win). To capture the
  *current supported agent session's* transcript, use the `capture-transcript`
  skill instead — it handles locating and verifying the live file.

For crash-safe retries pass your own `idempotency_key` (≤256 chars); a
replay within 24h returns the original artifact instead of creating a
duplicate. Re-storing bytes that are already stored is also free at the
content-hash level — don't hesitate to store the same file again if you're
unsure whether it was saved before.

The response is the full artifact record, including the new `artifact_id`
(format `art_` + 16 alphanumeric characters) and `content_hash`.

## Organizing runs with sessions

Pass the same `session_id` to every `store_artifact` call in one run to
group its outputs. `list_sessions` lists session IDs synthesized from your
artifacts (they're not first-class — a session exists only as long as
artifacts reference it), each with `artifact_count`, `is_sealed`, and
first/last activity timestamps.

When a run is truly finished, `seal_session` locks the session
permanently — **irreversible, no `unseal`**. Existing artifacts stay
readable, but any further `store_artifact` call against that `session_id`
is refused with `session_sealed`. Only seal a session once you're certain
nothing more will be added to it.

## Retrieving

- `list_artifacts` — filter by `session_id`, `agent_id`, `filename` (exact
  match), `content_type`, `created_after` / `created_before` (ISO 8601), or
  `metadata.<key>=<value>` (multiple metadata filters require Pro), or
  `transcript: true` to list only transcript-tagged artifacts. Results
  are newest-first with a `next_cursor` for pagination. Use this to discover
  what a session or agent produced when you don't have the artifact ID.
- `get_artifact` — metadata only (filename, content type, size, hash,
  session/agent, custom metadata, expiry, created_at) for one `artifact_id`.
  Does not return bytes.
- `get_artifact_download_url` — a presigned URL (1 hour expiry) for the
  agent itself to fetch the bytes.

## Sharing

- `create_download_link` mints a stable `https://dl.artifacta.io/lnk_…`
  URL for handing bytes to a human or a system that can't send bearer
  headers. Default expiry is 7 days; max is plan-dependent (30d Free, 90d
  Pro). This call always requires confirmation, since its side effect is a
  publicly reachable URL.
- `publish_artifact` turns an artifact into a polished public page at
  `https://artifacta.io/a/{slug}`, viewable without an Artifacta account.
  Defaults to `visibility: "unlisted"`; pass `visibility: "public"` to make
  it gallery-eligible. Idempotent — republishing the same `artifact_id`
  updates the same page and URL. `unpublish_artifact` takes the page down
  (the artifact itself is untouched) and is also idempotent.

Use a download link for a quick, time-boxed handoff; use publish when the
output is meant to be browsed as a page rather than downloaded as a file.

## Large files

For files over 500 MB (up to 5 GB) — or anything over the 10 MB `content`
cap on a hosted/plugin connection, where `path` is unavailable —
`store_artifact` isn't an option. Use `request_upload_url` (Pro only) to
reserve a presigned R2 PUT URL, PUT the bytes there yourself, then call
`complete_upload` with the returned `artifact_id` to finalize it. This flow does not support idempotency keys:
if a call fails with a server or network error, don't blindly retry — call
`list_artifacts` with the same `session_id`/`agent_id` first to check
whether a pending artifact was already created.

## CLI fallback (no MCP connection)

`pip install artifacta`, then set `ARTIFACTA_API_KEY` (or run
`artifacta auth login --key ak_live_...`). Useful commands:

```
artifacta push report.pdf --session ses_abc --meta stage=final
artifacta ls --session ses_abc --json
artifacta pull art_abc123def456 -o /tmp/report.pdf
artifacta inspect art_abc123def456 --json
artifacta whoami --json
```

`push` also accepts `--agent`, `--ttl`, `--new-session`, and `--name` /
`--content-type` when piping from stdin (`artifacta push -`). `ARTIFACTA_SESSION_ID`
and `ARTIFACTA_AGENT_ID` are read as defaults for `push` when the matching
flag is omitted.

Exit codes: `0` success, `1` client error, `2` server error, `3` network
error. Output is auto-JSON when stdout is not a TTY; human-readable status
goes to stderr, data to stdout — safe to pipe into `jq` either way.

## Behavior notes

- Artifact IDs are `art_` + 16 alphanumeric characters.
- Deletes are soft: `delete_artifact` makes the artifact disappear from
  listings and download URLs return `410 Gone` immediately, but the R2 blob
  is hard-deleted by a background job 30 days later — there's no undo via
  the API. Ask the user to confirm the exact `artifact_id` first, then call
  with `confirm: true`. Never set `confirm: true` unless they approved the
  delete in this conversation; the tool rejects the call without it.
- `ttl` on an artifact governs when it expires (`artifact_expired` on
  access past that point); it's independent of a download link's own
  `expires_in`.
