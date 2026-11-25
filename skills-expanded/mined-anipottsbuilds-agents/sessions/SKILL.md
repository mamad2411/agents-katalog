---
name: sessions
description: |
  See active Claude Code sessions on this machine and coordinate across them
  via direct messages, status announcements, and file-overlap awareness.
  Triggers when the user asks "who else is running?", "any other claude open?",
  "what other sessions are active?", "tell <name> to ...", "ping <peer>",
  "let peers know I'm doing X", "broadcast <status>", "check the cc digest",
  or any cross-session / multi-agent coordination on this machine.
model: haiku
---
<!-- tested with: claude code v2.1.133 -->

# cc — session mesh

## Routing decision (always check this first)

**If `mcp__cc__cc` is in your tool list, ALWAYS use it for every verb.**
This is the standard path: typed args, exfil guard, structured response
including `digest_delta` and `subscription_matches`. It's the right
default in every restarted terminal — the cc MCP server is registered
on session start, so any session that came up after `/plugin install`
has the tool.

**Only when the MCP tool ISN'T registered** (the install-trigger session
that ran `/plugin install` and `/reload-plugins` — Claude Code doesn't
re-poll `tools/list` mid-session, so that one terminal won't see the
tool until restart) — use the bash fast path below. Don't tell the user
you're "falling back"; just route correctly and move on. After they
restart that one terminal, the MCP path takes over.

## MCP path (default, when tool is registered)

```
cc({ action: "sessions" })                            # who's running
cc({ action: "send", to: "abcd1234", message: "...", urgency: "normal", subject: "..." })
cc({ action: "announce", summary: "refactoring auth.ts" })
cc({ action: "check", since_s: 3600 })                # rich digest with delta
cc({ action: "subscribe", files: "src/auth/**", urgency_min: "question" })
cc({ action: "unsubscribe", id: "<sub-id>" })
```

Every call also returns `digest_delta` (when peer-visible state changed)
and `subscription_matches` (when the caller has subs and any matched).
Don't call `check` to discover deltas — they ride every cc call.

## Bash path (only when MCP tool isn't in your tool list)

cc state lives in `~/.claude/channels/cc/`:
- `sessions.db` — peer roster, recent_files, announcements, subscriptions
- `inbox/<sid>/*.msg` — direct messages (any new file triggers recipient's
  push notification via their cc-server's FSWatcher, regardless of who
  wrote it)

`bin/cc-quick` is a bash helper that handles atomic .msg writes + sqlite
INSERTs without MCP. Works in the install-trigger session too.

```bash
bash $CLAUDE_PLUGIN_ROOT/bin/cc-quick roster
bash $CLAUDE_PLUGIN_ROOT/bin/cc-quick send <short-id> "message" "subject"
bash $CLAUDE_PLUGIN_ROOT/bin/cc-quick announce "summary text"
bash $CLAUDE_PLUGIN_ROOT/bin/cc-quick check 1800
```

For `subscribe` / `unsubscribe` (typed args, schema validation), the user
must restart their terminal so the MCP tool registers. There's no bash
equivalent.

## Action picker

| Intent | Action |
|---|---|
| "who else is running?" | `sessions` |
| "tell <peer> X", "ping <peer>" | `send` |
| "let peers know I'm doing X" | `announce` |
| "what's new", "check the digest" | `check` |
| "watch src/auth/**" | `subscribe` (MCP only) |
| "stop watching id=X" | `unsubscribe` (MCP only) |

## Targeting peers (`send`)

The `to` field accepts:
- **short id** (8 hex chars from roster) — preferred
- **full session id** — UUID4
- **cwd basename** — convenient but ambiguous across worktrees

For urgency, use `'question'` only when you actually need a reply; default
`'normal'`. `'urgent'` is for blocking coordination ("about to push to your
branch").

## Awareness loop

- **The recipient's cc-server FSWatcher pushes channel notifications** the
  moment a `.msg` file lands in their inbox. Senders don't worry about it.
- **File-overlap alerts** in the digest are advisory. Send a message before
  continuing edits on a flagged file.
- **`digest_delta` rides every cc call** (v3.3+). When using the MCP path,
  responses include a `digest_delta` block with new announcements + edits +
  peer joins/leaves since this session's last cc call. The bash path
  doesn't compute deltas — that's MCP-only.

## Why two paths?

Same sqlite + filesystem state behind both. The MCP tool exists for typed
validation (zod), an exfil guard (rejects paths under cc state dir), and
the `digest_delta` cursor advancement. The bash path exists because the
install-trigger session can't reach the MCP tool until restart. Routing
is automatic — pick by tool availability, not user preference.
