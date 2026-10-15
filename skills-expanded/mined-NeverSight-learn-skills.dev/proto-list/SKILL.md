---
name: proto-list
description: List every prototype uploaded to ProtoPeek with this machine's token — status, versions, new-feedback hints, and share links. Use when the user asks what prototypes they have shared or wants to find an old link.
---

List all prototypes owned by this machine's ProtoPeek token.

## Step 1 — Config

```bash
CFG="${XDG_CONFIG_HOME:-$HOME/.config}/protopeek"
[ -n "$PROTOPEEK_TOKEN" ] || . "$CFG/config" 2>/dev/null
```

If there's no token, this machine hasn't been set up — point the user at `/proto-up`.

## Step 2 — Fetch

```bash
curl -s "$PROTOPEEK_BASE_URL/api/prototypes" -H "Authorization: Bearer $PROTOPEEK_TOKEN"
```

## Step 3 — Report and reconcile

Print a compact table: name · version · live/expired · feedback (`total_comments`, with a
**new** marker when `has_new` is true) · share URL. A live prototype whose `rules` is
empty is **locked** — nobody can view it — so mark it "locked", not "live".
For any row marked new, suggest
`/proto-status <url>` (exact new-item count, watermark-safe) or `/proto-feedback <url>`
(pull + synthesize). `/proto-delete <url>` removes one for good.

Then reconcile the local log: add any returned prototypes missing from
`$CFG/prototypes.json` (the server is the source of truth — this recovers the list on a
new machine or after a lost log), and drop local records the server no longer has
(deleted or purged). Local-only fields like `source_path` stay blank for records the
server supplied.

The user can also browse everything in a browser: sign in with the token at
`$PROTOPEEK_BASE_URL/token` (no password).
