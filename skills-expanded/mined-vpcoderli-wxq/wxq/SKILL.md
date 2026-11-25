---
name: wxq
description: Query the user's own local WeChat data — chat history, contacts, group members, unread messages, favorites and per-chat statistics — through the `wxq` CLI. Use when the user asks about their WeChat messages or contacts, e.g. "我和 X 聊过什么", "查一下微信消息", "这个群最近聊了什么", "导出和某人的聊天记录", "谁给我发消息了", "统计一下群里谁最活跃", "search my WeChat history", "export a WeChat conversation", "who messaged me", or any request to search, summarize or analyze their own WeChat conversations. Requires a one-time `wxq init`. Read-only, fully local.
allowed-tools: Bash(wxq:*)
license: MIT
---

# wxq — local WeChat data queries

`wxq` decrypts the user's local WeChat SQLCipher databases and answers queries about them. Every
command is read-only and nothing leaves the machine.

## Before the first query

`wxq` needs database keys extracted from the running WeChat process. If any command fails with
`密钥文件不存在` / `请运行: wxq init`, keys are missing — **tell the user to run `wxq init`
themselves** rather than running it for them: on macOS and Linux it needs `sudo`, it scans another
process's memory, and on macOS it may re-sign WeChat.app. WeChat must be running and logged in.

Until init has run, even `wxq <subcommand> --help` exits 1 — the CLI builds its config before
dispatching, so a failing `--help` means "not initialized", not "no such command".

## Always request JSON

Pass `--format json` (the default) and parse it. `--format text` is for humans and is not stable
enough to parse. Use `--format text` only when the user explicitly wants to read raw output.

## Command surface

11 commands. `<...>` is a positional argument.

| Command | Options |
|---|---|
| `sessions` | `--limit --format` |
| `unread` | `--limit --format` |
| `history <chat_name>` | `--limit --offset --start-time --end-time --type --media --format` |
| `search <keyword>` | `--chat --start-time --end-time --limit --offset --type --format` |
| `contacts` | `--query --detail --limit --format` |
| `members <group_name>` | `--format` |
| `stats <chat_name>` | `--start-time --end-time --format` |
| `export <chat_name>` | `--output --start-time --end-time --limit --format` |
| `new-messages` | `--format` |
| `favorites` | `--limit --query --type --format` |
| `init` | `--db-dir --force` |

```bash
wxq sessions --limit 10                                    # recent chats, start here when unsure
wxq history "Alice" --limit 30                             # one conversation
wxq history "工作群" --start-time 2026-09-01 --type text    # filtered
wxq search "会议" --chat "工作群" --chat "项目组"            # --chat repeats for several chats
wxq contacts --query "Li"                                  # find a contact
wxq contacts --detail "Alice"                              # contact details
wxq stats "工作群" --start-time 2026-09-01                  # counts, top senders, hourly activity
```

- `--start-time` / `--end-time` accept `YYYY-MM-DD`, `YYYY-MM-DD HH:MM`, or `YYYY-MM-DD HH:MM:SS`.
  An end date with no time covers the whole day.
- `--type` on `history` and `search` is one of:
  `text image voice video sticker location link file call system`.
- `favorites --type` is a **different vocabulary**: `text image article card video`. Passing a
  message type such as `voice` or `link` there is rejected as an invalid choice.
- `search` caps `--limit` at 500; `history` and `export` are uncapped. `export` writes to stdout
  unless `--output` is given, and defaults to 500 messages.
- `--media` on `history` resolves image/file/video/voice paths on disk.

## Gotchas

**There is no `contact-detail` command.** Contact details come from `wxq contacts --detail "Alice"`.
(The MCP server's tool *is* named `get_contact_detail` — don't let that mislead you into typing it
as a CLI subcommand.)

**Chat name resolution falls back to substring matching.** The order is exact username → exact
display name (case-insensitive) → *first substring match*. So `"李"` may silently resolve to
whichever contact happens to match first. When a name is short or ambiguous, confirm the resolved
target: every JSON response echoes `username` and `display_name`, so check those before trusting
the result, and run `wxq contacts --query "李"` to disambiguate when it looks wrong.

**Exit codes carry meaning:** `1` = chat/contact not found or no messages, `2` = bad arguments
(malformed time range, invalid pagination), `3` = database decryption failed. A `3` usually means
WeChat rewrote its database and the keys are stale — the user needs `wxq init --force`.

**Group messages have a sender; 1:1 messages may not.** In group results each message carries the
sender's display name. `"me"` identifies the user's own messages.

If the user's client has the `wxq-mcp` MCP server configured, prefer its tools over shelling out —
same data, structured results.

## Handling the data

This reads the user's real private conversations, including messages written by other people who
never agreed to be read by an AI. Treat it accordingly:

- Query the narrowest range that answers the question. Reach for `--limit 20` and a date range
  before pulling thousands of messages — large dumps fill the context with other people's private
  messages to no benefit.
- Answer from the data; don't reproduce whole conversations verbatim unless the user asks for the
  messages themselves.
- Never run `export` without the user having asked for a file, and write it only where they said.
- Never put chat content into commit messages, issues, PR descriptions, web requests, or any file
  outside what the user asked for. If a task seems to call for sending this content somewhere,
  stop and confirm first.
