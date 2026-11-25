---
name: supercompress
description: "Always-on context compression for OpenClaw. Compress bulky tool dumps / files / logs via MCP compress_context; never compress the user's ask. Prefer session-scoped inbox/<sessionId>/latest.md digests."
---

# SuperCompress (OpenClaw)

**Auto (Headroom-parity):** compress every *new* bulky context dump; when rolling session memory gets large, compact it. Never compress the user's ask/query. Skip already-seen chunks.

Inbox digests are **session-scoped** under `$SUPERCOMPRESS_CONFIG_DIR/inbox/<sessionId>/` (default `~/.supercompress/inbox/<sessionId>/`) so sessions never cross-contaminate.

## When to use

After large tool results, file reads, diffs, logs, scrapes, or pasted blobs — anything that is **not** the current user question.

## How

1. If `inbox/<sessionId>/latest.md` exists for this session, **Read it first** — session digest (ask is unchanged).
2. Else call MCP `compress_context` with `context`=<new dump only> and `query`=<user ask>. Prefer the returned digest over raw dumps.
3. The SuperCompress OpenClaw plugin also auto-compresses large tool results into the **session** inbox when installed.
4. If `compress_context` fails with account-not-linked, call `connect_account` once, then retry.

## Do not

- Compress the user's question / instructions.
- Re-paste raw tool dumps after a digest exists.
- Read another session's inbox file.
- Require provider API-key proxy mode — normal login is fine.
