---
name: prompt-sharing
description: "Hands a prompt to a coworker (or to yourself) formatted for paste-and-go into their own Claude Code session, through a transport you choose: clipboard by default, a secret GitHub gist, your own shell command such as a chat webhook, or LibreWhatsApp /push. Use when the user wants to share, send, or pass a prompt to someone, or save one to paste elsewhere."
user-invocable: false
---

# Share a prompt, paste-ready

> One command, and the recipient gets a code-fenced prompt they can copy straight into their own session.

Designed for the live handoff: a coworker is stuck, you have the prompt that unblocks them. For prompts worth keeping, promote them instead: a reusable workflow becomes a skill, an always-needed rule goes into CLAUDE.md.

## Trigger

```
/share-prompt @<handle> <prompt body>
```

The first whitespace-separated token that starts with `@` is the recipient handle. Everything after it is the prompt body, verbatim.

```
/share-prompt @me summarize the open TODO.md items and propose which to close
/share-prompt @teammate reproduce the flaky login test with --repeat 20 and report the failing seed
/share-prompt @gist:reviewers review auth/session.ts for token-refresh races
```

## Settings

Read the settings file if it exists: `cat "${SESSIONFLOW_CONFIG:-$HOME/.claude/sessionflow.json}" 2>/dev/null`, section `share_prompt`:

```json
"share_prompt": {
  "default_transport": "clipboard",
  "recipients": {
    "me": { "transport": "clipboard" },
    "teammate": { "transport": "push", "target": "wa teammate" },
    "reviewers": { "transport": "gist" },
    "team-channel": { "transport": "command", "command": "<shell command that reads stdin>" }
  }
}
```

No settings: every handle falls back to the clipboard transport, so the skill works with no setup.

## Step 1: parse

Split into handle and body. If either is missing, print the trigger syntax and stop. Refuse an empty body.

## Step 2: resolve the handle

In order:

1. **`@<transport>:<address>`**: explicit transport, for example `@gist:reviewers`, `@push:wa teammate`, `@clipboard:me`. Use that transport directly.
2. **`@<name>` found in `share_prompt.recipients`**: use that recipient's transport and target.
3. **`@me` with no entry**: clipboard.
4. **Unknown `@<name>`**: say `no recipient named @<name>`, list the configured names, and ask which one (or offer the clipboard). Never guess a recipient. Sending the wrong person a message costs more than asking.

## Step 3: check the body

Scan for credentials: `(?i)(api[_-]?key|secret|password|token|bearer)\s*[:=]\s*\S+` and private-key headers (`-----BEGIN .* PRIVATE KEY-----`). On a match, stop and ask the user to remove the secret or confirm explicitly. A prompt that needs a secret should name where the secret lives, not contain it.

## Step 4: format

```
Prompt to paste into your Claude Code session:

```
<prompt body, verbatim>
```
```

- If the body itself contains triple backticks, fence the wrapper with `~~~` instead.
- For chat transports (`push`, `command`), split a body longer than 3500 characters at paragraph boundaries into parts labeled `[1/N]`, `[2/N]`, each fenced on its own, and say in the first part that the prompt comes in N parts. Never split inside a code block.

## Step 5: deliver

Write the formatted message to a temp file first (`mktemp`), so quotes and backticks survive the shell.

### clipboard (default)

Pick the first tool that exists: `wl-copy` (Wayland), `xclip -selection clipboard` or `xsel --clipboard --input` (X11), `pbcopy` (macOS), `clip.exe` (WSL). Pipe the file into it, then read the clipboard back (`wl-paste`, `xclip -o -selection clipboard`, `xsel --clipboard --output`, `pbpaste`) and confirm it starts with `Prompt to paste`. Only then report it as copied. If no clipboard tool works (for example over ssh with no display), print the formatted message in a fenced block and say so.

### gist

```bash
gh gist create --desc "Prompt for <handle>" --filename prompt.md - < <tmpfile>
```

(`-` makes `gh` read the content from stdin; `--filename` names the file inside the gist.)

`gh` creates a secret gist unless `--public` is passed; keep it secret unless the user asks otherwise. Anyone with the link can still open a secret gist, so the secret scan in Step 3 matters here too. Report the URL and copy it to the clipboard.

### command

Show the formatted message and the command it goes to, then run the recipient's `command` with the message on stdin: `<command> < <tmpfile>`. Report the exit status in one line.

### push (LibreWhatsApp)

Requires the LibreWhatsApp `/push` command. Hand the formatted message to `/push <target> "<message>"`. Push shows its own preview and waits for confirmation; do not skip it. Without LibreWhatsApp installed, say so and fall back to the clipboard.

## Step 6: report

One line: `Shared with @<handle> via <transport>: <copied | gist url | exit 0 | queued>`. Do not dump raw API responses.

## Don'ts

- Don't share secrets. Message and gist histories outlive the moment.
- Don't auto-resolve an ambiguous or unknown handle.
- Don't send to a chat transport without the user seeing the message first (command) or the push preview (push).
