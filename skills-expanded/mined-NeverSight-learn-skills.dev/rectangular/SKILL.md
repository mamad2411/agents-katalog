---
name: rectangular
description: >-
  Use this skill whenever you are asked to work on a Rectangular ticket, or told
  "use skill rectangular" / "use the rect skill" together with a ticket number
  (e.g. T-0003), or when the user mentions the `rect` CLI, the task board, or
  wants you to check/comment/close a ticket. This is how you read the board and
  reply as a worker. Load it before touching any `rect` command.
---

# Rectangular — worker quickstart

Rectangular is a chat-first task board. A ticket IS a conversation between the
user and workers. Your job as a worker: read the ticket, do the work, reply on
the ticket. Do NOT flip state unless explicitly told to.

## The commands (the whole toolbox)

```bash
rect list                        # see active tickets, newest first, review-needing on top
rect list --done                 # see closed tickets
rect list --json                 # same, machine-readable
rect status                      # counts + quick peek
rect read T-0001                 # full chat thread of one ticket
rect add "Fix the thing"         # create a new ticket (you usually won't need this)
rect comment T-0001 "my reply" --as assistant --name "your-name"
                                 # reply on a ticket. Default role is 'system' (the machine).
                                 # Use --as assistant to speak as a worker.
rect comment T-0001 "text" --status "in progress"
                                 # reply AND set the free-text status in one shot
rect close T-0001                # state → done. USER-ONLY unless full-access on
rect reopen T-0001               # state → active. USER-ONLY unless full-access on
rect full-access on|off          # enables agents to close/reopen/delete
rect search "fuzzy term"         # full-text search across titles + comments
                                 # (active AND done). Fuzzy: 'quic' finds 'quick'.
                                 # Include a ticket ref (T-XXXX) if you know it.
rect updates                     # what changed since the LAST call (first call = everything so far).
                                 # Stores a cursor in .rect/updates.json; each call only shows newer
                                 # activity, then advances. Great for polling while you work.
                                 # --no-mark peeks without advancing; --since ISO overrides; --json.
rect claim T-0001 --as assistant --name "your-name"
                                 # SOFT LOCK: you're working on it. Others see 🔒.
                                 # Only one claimant at a time.
rect unclaim T-0001 --as assistant --name "your-name"
                                 # Release the claim. Claimant or the user can.
                                 # Closing a ticket auto-releases.
```

## The one rule that matters

- **Messages (comment) are always allowed.** Reply freely.
- **State flips (close/reopen) and destructive ops (delete) are user-only**
  unless Full Access Mode is on (`rect full-access on`). If you need to move a
  ticket and you lack permission, say so instead of failing silently.
- **Claims are a soft lock.** If you start working a ticket, claim it
  (`rect claim T-XXXX --as assistant --name "<you>"`) so other workers see 🔒.
  Release with `rect unclaim` when done — or just let the user close it, which
  auto-releases. Claiming is etiquette, not a wall: nobody is blocked from
  commenting, but don't be rude and grab a claimed ticket.

## Typical worker loop

1. `rect list` — find your ticket(s). If given a number like T-0003, use it.
2. `rect read T-0003` — read the full thread. Context is everything.
3. Do the work.
4. `rect comment T-0003 "done — here's what I did" --as assistant --name "<you>"`
   This flags the ticket as needing the user's review.

That's it. Keep it simple, keep it on the board.
