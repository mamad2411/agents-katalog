---
name: tossinbox
description: Create disposable email inboxes from the terminal or via MCP, wait for verification (OTP) codes, read messages, and delete the inbox when done. Use when a signup, test, or privacy flow needs a throwaway email address that receives real mail.
---

# TossInbox — disposable email for agents

TossInbox spawns real disposable inboxes on live providers (mail.tm by
default, plus mail.gw, GuerrillaMail, tempmail.lol, temp-mail.io, tempmail.plus
and maildrop.cc as fallbacks), waits for incoming verification mail,
extracts the OTP code, and deletes the inbox when done. It is receive-only:
it never sends email. No accounts, no API keys, no interactive prompts.

## When to use

- A signup or verification flow needs an email address, and reusing a real
  mailbox is not acceptable.
- CI must test a real email pipeline and read the OTP programmatically.
- Do NOT use it for identities that matter (banking, government, personal
  accounts). Treat every disposable inbox as public.

## Install (Node.js 18+)

```bash
npm install -g tossinbox
# or run without installing:
npx tossinbox@latest spawn
# or on macOS/Linux:
brew install mohamed-khairy-5i/tap/tossinbox
```

## CLI flow (every command accepts --json; exit codes 0-4)

```bash
tossinbox providers                    # sanity check: proves install + network
tossinbox spawn                        # fresh disposable address, saved locally
# ... submit the address in the signup form FIRST ...
tossinbox wait --code --from noreply@example.com --timeout 120
tossinbox toss                         # delete server-side + wipe local state
```

Commands: `spawn` (`-p provider`, `-l label`; if the provider is down, another
one is used automatically — `--no-failover` opts out), `list` (`-a address`),
`read <id>` (`--save [dir]` saves every attachment plus the HTML/plain-text
bodies to `<dir>/<message-id>/`, default `./tossinbox-attachments`; `--html`
prints the raw HTML body), `wait` (`-f from`, `-s subject`, `-c` extract code,
`-t` timeout max 600s, `-i` interval), `watch` (stream new messages until
Ctrl-C; `--json` streams one JSON object per line), `inboxes`,
`toss` (`-a`, `--all`), `clear`, `providers`, `mcp`.

Exit codes: 0 success · 1 error (network/provider) · 2 timeout ·
3 not found · 4 usage error. Script against these codes, not against stdout.

## MCP server (preferred by MCP clients)

The same binary runs a stdio MCP server (`tossinbox mcp`, or the
`tossinbox-mcp` binary) exposing four tools:

| Tool            | Returns                                          |
|-----------------|--------------------------------------------------|
| `create_inbox`  | Fresh disposable address + provider name. If the requested provider is down, another one serves the inbox automatically (`no_failover` opts out) |
| `list_messages` | Messages currently in the inbox                  |
| `read_message`  | Full message body incl. any detected code        |
| `wait_for_code` | Blocks until a code arrives, returns it          |

Client config:

```json
{
  "mcpServers": {
    "tossinbox": {
      "command": "npx",
      "args": ["-y", "tossinbox", "mcp"]
    }
  }
}
```

## Typical agent flow (no human in the loop)

1. `create_inbox` -> get the address.
2. Submit the address in the signup form (your tooling).
3. `wait_for_code` -> get the OTP.
4. Finish the signup with the code.
5. `tossinbox toss` from the shell, or leave the inbox to age out.

## State and privacy

- Local state: `~/.tossinbox/state.json` (0600; override with the
  `TOSSINBOX_STATE` environment variable).
- `toss` deletes the provider account when supported; `clear` only wipes
  local state.
- Receive-only by design, no bulk mode. Respect each provider's terms.

Docs: https://tossinbox.pages.dev/ · Source:
https://github.com/mohamed-khairy-5i/tossinbox · License: MIT
