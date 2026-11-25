---
description: Connect Gmail to Claude via mailwarden — walk the user through the one-time Google Cloud OAuth setup, `npx mailwarden@0.32.1 --auth`, and verify with `npx mailwarden@0.32.1 --check`. Use when the user wants to set up or repair mailwarden, when a mailwarden tool fails with "Not authorized yet", "Cannot read OAuth credentials", "invalid_grant" or "missing a Gmail scope", or when they ask how to connect a second Gmail account.
---

# Set up mailwarden

mailwarden runs locally and talks to Gmail with the user's OWN Google OAuth client — there is no
hosted service and no shared credential. Setup is a one-time dance with the Google Cloud console
and one terminal command. The authoritative, step-by-step guide ships with this plugin:

    ${CLAUDE_PLUGIN_ROOT}/docs/SETUP.md

Read it before you start (it is short) and follow it rather than improvising — in particular the
part about setting the OAuth consent screen to **Production**, which is what keeps the token from
expiring after seven days.

## How to run this

1. **Diagnose first.** Run `npx -y mailwarden@0.32.1 --check` and read its report. It tells you exactly
   which step is missing (no `credentials.json`, no token, wrong scopes, encrypted token without
   passphrase, …) and what to do. If it passes, setup is already done — say so and stop.
2. **Walk the user through the console steps** from `docs/SETUP.md` §1–§4 (Cloud project → Gmail
   API → consent screen in *Production* → Desktop-app OAuth client → download `credentials.json`
   into `~/.mailwarden/`). These happen in the user's browser; you cannot do them for them. Give one
   step at a time and wait.
3. **Authorize** (§5): the user runs `npx -y mailwarden@0.32.1 --auth` in their own terminal — it opens a
   browser for Google consent and stores the refresh token in `~/.mailwarden/token.json`. Do not run
   this from a tool call yourself; it needs an interactive browser session. The "unverified app"
   warning is expected for a personal OAuth client (§5, "The unverified app warning is normal").
4. **Verify** with `npx -y mailwarden@0.32.1 --check` again, then call the `get_profile` tool to confirm
   which mailbox is connected.

## Options worth mentioning

- **Least privilege:** `MAILWARDEN_TOOLS=read` (or `MAILWARDEN_READONLY=1`) registers only the read
  tools and requests only `gmail.readonly` at `--auth`. The plugin's default server entry runs
  the default tiers (read, manage, filters; the opt-in drafts tier stays off); a user who wants a narrower tier should add the server themselves with
  `claude mcp add mailwarden -e MAILWARDEN_TOOLS=read -- npx -y mailwarden@0.32.1` and disable this
  plugin's server. Widening the tiers needs a fresh `--auth`; narrowing does not.
- **Second account:** `npx -y mailwarden@0.32.1 --auth --account work`, then a second server entry with
  `MAILWARDEN_ACCOUNT=work` (README → "Multiple accounts"). One server = one mailbox, by design.
- **Troubleshooting:** every known error message has an entry in `docs/SETUP.md` → Troubleshooting.
  Quote the matching entry instead of guessing.

What mailwarden will never do, so don't look for it: send, reply, forward, or permanently delete.
