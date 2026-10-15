---
name: proto-status
description: Cheap "is there new feedback?" poll for a ProtoPeek prototype — read-only, safe to repeat, does not consume the new-since watermark. Use when the user asks whether reviewers have commented yet.
---

Check activity on a ProtoPeek prototype WITHOUT advancing its "new since last pull"
watermark — safe to run repeatedly.

Arguments: a share URL, a bare UUID, or a natural reference ("yesterday's dashboard").

## Step 1 — Config

```bash
CFG="${XDG_CONFIG_HOME:-$HOME/.config}/protopeek"
[ -n "$PROTOPEEK_TOKEN" ] || . "$CFG/config" 2>/dev/null
```

If there's no token, this machine hasn't been set up — point the user at `/proto-up`,
which walks through the one-call, no-signup token mint (with consent) on first use.

## Step 2 — Resolve the reference → UUID

A URL or UUID is used directly. Otherwise match `$CFG/prototypes.json` by name /
filename / path / project / recency. If more than one candidate, list them and ask —
resolution here is safe (this endpoint is read-only).

## Step 3 — Fetch and report

```bash
curl -s "$PROTOPEEK_BASE_URL/api/prototypes/<uuid>/status" \
  -H "Authorization: Bearer $PROTOPEEK_TOKEN"
```

Report concisely: prototype name + version, whether it's live/expired, and the status
counts — `distinct_reviewers`, `total_comments`, **`new_since_last_pull`** (the
load-bearing "worth re-pulling?" signal), and `last_activity`. If
`new_since_last_pull > 0`, suggest running `/proto-feedback <url>`.

This endpoint is read-only and does not change the watermark; only `/proto-feedback` does.
