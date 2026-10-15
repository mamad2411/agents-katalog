---
name: proto-delete
description: Permanently delete a ProtoPeek prototype — the link, every uploaded version, and all reviewer feedback. Use when the user wants a shared prototype gone for good (not just deactivated), or wants uploaded content removed from protopeek.dev.
---

Permanently delete a ProtoPeek prototype. This kills the link immediately and removes the
stored HTML (every version), all reviewer annotations, comment threads, and screenshots.
It cannot be undone.

Arguments: a share URL, a bare UUID, or a natural reference ("the old signup card").

## Step 1 — Config

```bash
CFG="${XDG_CONFIG_HOME:-$HOME/.config}/protopeek"
[ -n "$PROTOPEEK_TOKEN" ] || . "$CFG/config" 2>/dev/null
```

If there's no token, this machine hasn't been set up — there is nothing to delete from here.

## Step 2 — Resolve the reference → UUID

A URL/UUID is used directly; otherwise match `$CFG/prototypes.json` by name / filename /
path / project / recency.

## Step 3 — Confirm (always, even for an explicit URL/UUID)

Show the resolved target (name, share URL, version, live/expired) and make sure the user
wants it *gone*, not just switched off:

- If they only want the link dead but the feedback kept (reversible), offer deactivation
  instead:
  ```bash
  curl -s -X PATCH "$PROTOPEEK_BASE_URL/api/prototypes/<uuid>" \
    -H "Authorization: Bearer $PROTOPEEK_TOKEN" -H "Content-Type: application/json" \
    -d '{"is_active": false}'
  ```
  (Re-open later with `{"is_active": true}`.)
- Only proceed to delete on an explicit yes.

## Step 4 — Delete

```bash
curl -s -o /dev/null -w "%{http_code}" -X DELETE \
  "$PROTOPEEK_BASE_URL/api/prototypes/<uuid>" \
  -H "Authorization: Bearer $PROTOPEEK_TOKEN"
```

`204` means deleted. Anything else: show the status (`404` = not found, or not owned by
this token) and the response `detail` if present.

## Step 5 — Update the log

Remove the record from `$CFG/prototypes.json` (atomic write — temp file + rename), then
confirm to the user: the link is dead and the prototype, its versions, and all feedback
are permanently removed. (Expired prototypes are purged automatically 14 days after
expiry — deleting is only needed sooner than that.)
