---
name: install-iva
description: >
  Install, check or repair Iva (the self-hosted Telegram assistant, github.com/smixs/iva-agent) on a person's VPS or on
  their own Mac, from the person's own computer over SSH, safely and repeatably. Use when someone says "install Iva",
  "установи Иву", "поставь Иву на сервер", pastes a hosting provider's "your server is ready" email, asks to check or fix
  their Iva, says the Iva bot stopped answering, or wants Iva updated — even if they don't explicitly say "install".
  Do NOT use for changing how Iva talks or what she remembers (that is done in the Iva chat or /menu), for developing
  Iva's code, or for servers that are not meant to run Iva.
---

# Install Iva

## Overview

Take a person from "I have a server" (or "use this Mac") to "my Iva bot answers me", doing every technical step yourself.
The person is usually not technical. Every run is repeatable: check the state first, do only what is missing, and leave
a server that only the person's key can enter.

Talk to the person in their language, in plain words, one short message per step. Show them what you found before you
change anything.

## The ladder

Walk these steps in order on every run. Each step: check → do only what is missing → check again. A step that is already
done costs one check, not a redo.

| Step | What it settles | Read before doing it |
|---|---|---|
| 0. Pre-flight | the person's computer can reach and manage a server; the server is fit for Iva | `references/preflight.md` |
| 1. Target | which machine: a server (address from env, `~/.ssh/config`, mail, or the hosting email) or this Mac | `references/target.md` |
| 2. Access | a key-only SSH login as user `iva`, saved as `ssh iva` on the person's computer | `references/access.md` |
| 3. Server security | non-root user, key-only SSH, root login closed, firewall, fail2ban, security updates | `references/server-security.md` |
| 4. Iva | install, repair, update or leave alone — decided by what is already there | `references/iva-state.md` |
| 5. Keys | model, bot token, the person's Telegram ID — only what is missing | `references/keys.md` |
| 6. Finish | the bot answers the person; they know the one command to reach the server | `references/finish.md` |

A Mac target skips steps 2 and 3 and installs locally (same installer; it sets up launchd itself).

## Rules that protect the person

- **Secrets never become text.** A password, bot token or API key goes from a file to the server through a pipe or a
  file with mode 600 — never inside a command line (it shows in `ps` on both machines), never echoed back, never in your
  final message. Why: the session transcript, shell history and process list all outlive the install. Details and safe
  patterns → `references/secrets.md`.
- **Never lock the person out.** Prove the new key login works before closing password or root login, and keep the
  current session open until then. Why: a VPS with closed password login and a broken key is only recoverable through
  the hosting provider's rescue console, which a beginner cannot use.
- **Use the official installer.** `bootstrap.sh` prepares the server, `install.sh` installs Iva. Do not hand-write
  `.env` beyond the minimal file in `references/keys.md`, do not write systemd units or sudoers files yourself. Why:
  hand-made setups break on the next `iva update`, and the person cannot get help for a setup nobody else has.
- **Change only what is Iva's.** On the person's computer touch only `~/.ssh/iva_ed25519*` and the `Host iva` block in
  `~/.ssh/config`. On a server that already runs other services, ask before installing next to them.
- **A question you cannot ask is a stop, not a guess.** If you run without a way to ask (non-interactive mode) and a
  required answer was not given, stop with that one question.

## Common mistakes

| Mistake | Fix |
|---|---|
| Reading Iva's source to reverse-engineer the setup | The ladder and references are the procedure; the installer does the rest |
| `echo "$PASS" \| sudo -S` inside `ssh host "…"` | The password lands in the remote command line; see `references/secrets.md` |
| Saving new passwords to a plain file "for the person" | The server needs no password after step 3; do not create one to store |
| `Host` block written to a temp config and deleted | The person loses the short login; write it to `~/.ssh/config` |
| Declaring success because the installer printed "ready" | Done means the bot answered the person (step 6) |
| Trying every key in `~/.ssh` against the server | fail2ban bans the person's address for an hour after 5 failures; at most 3 attempts, `IdentitiesOnly=yes` (`references/access.md`) |
| Passing `IVA_DISABLE_PASSWORD_AUTH=false` or leaving it out | Password login stays open on hosts whose image enables it; always `=1` once the key works |
