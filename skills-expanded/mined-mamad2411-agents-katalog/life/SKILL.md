---
name: life
description: Use when working with Charlie's life vault, personal notes/documents, agent memory, or the life MCP gateway (brain/agents/ledger/1Password tools).
---

# Life vault

The vault is Charlie's life: his notes, journal, documents, and the agents' shared brain. `/AGENTS.md`
at the vault root is the rulebook — read it first (`brain … read_text_file({ path: "AGENTS.md" })`),
then `agents/memory/MEMORY.md`. This skill only covers how to reach the vault; the rulebook says how
to behave in it, and it wins if the two disagree.

## Paths

One path names one file everywhere: relative to the vault root, no leading `/`.
`agents/devin/log/2026-09-23.md`, `agents/memory/MEMORY.md`, `Journal/2026-09-23.md`. The `agents`
namespace serves only `agents/` and *still* wants the prefix: `devin/log/x.md` and
`agents/agents/devin/log/x.md` are refused with the corrected path in the error — fix the path,
don't retry variations. A note Charlie marked `agent_access: none` does not exist as far as you
can tell; `agent_access: read` refuses writes. Don't work around either; tell him what you needed.

## Tools

Everything goes through the `life` MCP server (the Executor gateway, tailnet-only). Its tools:
`skills({ name: "execute" })` (read it once), `execute({ code })`, which runs TypeScript with a
`tools` object, and `resume({ executionId })`. Namespaces and their tools, so you don't need
`tools.search` / `tools.describe.tool` for the common cases:

- `agents.org.shared.*` — the `agents/` subtree; reads and writes are free, no approval.
  `read_text_file({path})`, `write_file({path, content})`, `append_file({path, content})`,
  `edit_file({path, edits: [{oldText, newText}], dry_run?})`, `list_directory({path})`,
  `directory_tree({path})`, `search_files({query, path?, limit?})`, `get_file_info`,
  `create_directory`, `move_file`, `read_media_file`.
- `brain.org.shared.*` — the whole vault, same tools. Reads are free; every write pauses for
  Charlie's approval: the call returns a paused execution (id + approval URL) instead of a result.
  Give Charlie the URL, then call `resume({ executionId })`, which waits for his decision. Don't
  retry, rewrite, or route the write through `agents` instead.
- `ledger.org.shared.*` — finance, read-only, signed amounts (liabilities negative), ISO dates:
  `accounts()`, `net_worth()`, `transactions({account_id?, since?, until?, search?, limit?})`,
  `spending({since, until})`, `positions({account_id?})`, `investment_transactions({...})`.
- `onepassword.org.shared.*` — `list_vaults()`, `list_items({vault})`, `get_item`, `read_secret({reference})`,
  `create_item`, `edit_item`. Values are secrets: use them, never echo them into the vault or a log.

Every call returns `{ ok: true, data } | { ok: false, error }`; branch on `ok`. `agents`, `brain`
and `onepassword` are proxied MCP servers, so text comes back as
`r.data.structuredContent?.result ?? r.data.content?.[0]?.text`; `ledger` returns plain JSON in
`r.data`. Do one `execute` per step and batch independent calls with `Promise.all` — a balance
check is one call, not nine. Many agents share the vault: `append_file` for logs, `edit_file` for
changes to existing notes, `write_file` only for a file you just created.

Devin cloud VMs join the tailnet lazily, so the gateway isn't reachable until the join has run.
Before your first `life` call, run `devin-tailscale-up` once (a shell command; ~20 s, and the
session's first shell command pays that anyway) — then the MCP works. If a `life` call still
fails with "error sending request", that's the tailnet, not the API key: run it again, it prints
why the join is failing. Never fall back to curl or a script against the gateway. On Macs and the
workstation the machine is already on the tailnet and `devin-tailscale-up` doesn't exist; skip this.

On Charlie's personal Macs the vault is a plain folder (Obsidian + Self-hosted LiveSync),
`~/all/life`, and Claude Code's auto-memory points at `agents/memory/` inside it. The rulebook
applies to direct file edits too: stay inside `agents/` unless Charlie has approved the change.
