---
name: qbt-kit
description: >
  Drive qBittorrent from the command line or over MCP with qbt-kit. Use this
  whenever a task involves qBittorrent at all — listing or adding torrents,
  moving data, categories, tags, preferences, search plugins, or working out why
  a download is not finishing — even when the user does not name qBittorrent and
  only says things like "is that download done", "why is this stuck", "move
  those files" or "clean up the queue". Also use it before answering any
  question about whether a torrent has finished, because the obvious ways of
  checking are wrong.
---

# qbt-kit

A complete client for the qBittorrent WebUI API: `qbt` covers all 123 endpoints
one-to-one, `qbt-mcp` exposes 15 tools: 13 task-shaped, plus `qbt_call` and
`list_endpoints`.

## Start here

```sh
qbt doctor       # version, auth mode, which endpoints this server supports
qbt health       # can each torrent actually finish?
qbt ready        # what is complete and settled enough to move
```

`--json` works on everything, and goes **before** the subcommand:
`qbt --json ready`.

## The one thing worth internalising

**A stalled download is usually not slow — it is mathematically stuck.**

`availability` is how many complete copies of a torrent exist across the peers
you can reach. When it does not meaningfully exceed `progress`, the pieces you
are missing are missing from the swarm too, and no amount of waiting will finish
it. 99.9% and 20% are equally dead when that gap is zero.

```sh
qbt health
```

But there is a trap inside the trap: a **queued** torrent reports availability
`0.0` simply because it is not connected yet, which looks identical to a dead
swarm. Judging those as dead is how you delete healthy downloads. `qbt health`
reports them separately as "not yet connected"; never apply the rule to a
torrent in `queuedDL`, `metaDL`, `checkingResumeData` or `moving`.

When something is genuinely stuck, the fix is a different release, not patience.
Season packs survive far longer than single-episode torrents, because more
people keep them.

## Judging completeness

Use `qbt ready`. Do **not** judge by:

- **Size on disk** — qBittorrent preallocates to full length when configured to.
- **A torrent's overall percentage** — deselected files never complete, so a
  season pack with most episodes skipped reads 10% while the wanted ones are done.
- **The `.fastresume` files** — resume data is flushed only every
  `save_resume_data_interval` minutes (60 by default), so anything finished in
  the last hour looks unfinished there.

Per-file progress from the API is the live, correct answer.

## Moving data

```sh
qbt torrents set-location --hashes <h> --location /new/path
```

This makes qBittorrent perform the move and the torrent stays valid, unlike a
manual `mv`, which orphans it. Two caveats: the call returns **before** the move
finishes, so poll `save_path` and check the bytes arrived; and a `recheck`
afterwards rehashes everything, which is expensive on large media — only do it
when you need proof.

Categories carry save paths. With automatic management on, **setting a category
moves the data**, which is useful deliberately and surprising accidentally.

## Things that will waste your time otherwise

- **A bare 401 is often not bad credentials.** Host-header validation is on by
  default and rejects any request whose `Host` port differs from the port
  qBittorrent listens on — which is what happens behind mapped container ports,
  SSH tunnels and reverse proxies. `qbt doctor` tells the two apart.
- **Force-start overrides share limits.** A force-started torrent ignores
  stop-on-complete entirely, so it keeps seeding no matter the configuration.
  If something will not stop, check `force_start` first.
- **`delete` with `--delete-files` is permanent** — not the Trash. The CLI
  requires `--confirm`, and MCP requires `confirm=true`.
- **Per-torrent limits of `-2` mean "use the global setting".** A global rule
  reaches a torrent only when its own limit is `-2`.

## MCP

```jsonc
{ "mcpServers": { "qbittorrent": {
    "command": "uvx", "args": ["qbt-mcp", "--url", "http://127.0.0.1:8080"] } } }
```

Add `--read-only` to refuse everything that changes state. Credentials come from
flags, then the environment, then the macOS Keychain (`qbittorrent` service,
accounts `webui` for the password and `api-key` for an API key). Prefer the
Keychain: MCP client config files are plaintext and often committed.

Refused calls return a structured cause and a remedy rather than an opaque
error, so read the response and correct the call instead of retrying blindly.

Use `list_endpoints` to discover what `qbt_call` can reach when no curated tool
fits.
