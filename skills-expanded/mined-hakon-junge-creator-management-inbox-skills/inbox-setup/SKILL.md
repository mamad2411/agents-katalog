---
name: inbox-setup
description: >
  Guided setup for Creator Management Inbox, for people new to the terminal: the demo
  first, then Gmail, profile, voice, rates and a first real run. Use for "set up my
  inbox", "get started", "connect my Gmail", "switch to the e-commerce demo", "help me
  install Python", "is everything set up?", or when an inbox command reports something
  missing.
---

# Inbox setup

The user may be non-technical. Your job is to do the work, explain each step in
one plain sentence, and never leave them staring at an error. Run commands for
them; only hand over what genuinely needs their hands (clicking in Google Cloud,
approving the browser consent).

`inbox` is on PATH once the plugin is installed. If a shell says
`command not found`, use `"${CLAUDE_PLUGIN_ROOT}/bin/inbox"` instead, and suggest
`/reload-plugins`.

Start every setup conversation with `inbox doctor` and pick up from the first
`TODO`. Tell them where they are: "You're at stage 2 of 5."

## Stage 1 - Try the demo (about 10 minutes)

The goal is the "oh, that's good" moment before any account work.

1. `inbox setup` - creates the private folder `~/.claude/inbox/` (only their user
   account can read it), copies the profile templates, installs the Gmail libraries
   into a private Python environment. Settings start at `provider: demo`.
   - Python missing or too old -> see "Installing Python" below.
2. Ask what they sell. An app: "I'll answer six fictional emails as Sam at Fernwell, a
   made-up app. Nothing is sent." Physical products: set `demo_profile: ecommerce` in
   settings.md, then say eight emails, as Imogen at Quillmoss, a made-up skincare brand.
3. Run the `inbox-auto-draft-workflow` skill in full.
4. Open `~/.claude/inbox/demo-output/index.html` for them (`open <path>` on a Mac).
   Point out three things: the rate counter used real math and never revealed the
   walk-away; the script feedback flagged the risky claim; the suspicious email was
   refused and flagged, not obeyed.

## Stage 2 - Connect Gmail (about 15 minutes)

Walk them through `references/connect-gmail.md` one step at a time. Show one
step, wait for "done", then the next. Offer to open each URL in their browser.

- Ask first: work Gmail (Google Workspace) or personal @gmail.com? It changes step 3.
- After step 4: `inbox import-client ~/Downloads/client_secret_*.json` (if there are
  several matches, use the newest). Then remind them to delete the Downloads copy.
- `inbox auth`, then `inbox whoami`. Show them the connected address.
- Personal Gmail: explain the weekly-logout fix and offer to walk them through
  publishing the app.
- Switch the provider: edit `provider: demo` -> `provider: gmail` inside the
  ```settings block of `~/.claude/inbox/profile/settings.md`.

Never read, print or copy `token.json` or `client_secret.json`. The guard hook
blocks it anyway; use `inbox` commands only. To disconnect: `inbox disconnect`.

## Stage 3 - The profile (10-20 minutes)

Profile files live in `~/.claude/inbox/profile/`. Fill them WITH the user:

0. **`program.md` first ("set up my program")** - it shapes every money email. Ask in
   plain words, one at a time, options as choices; several answers -> a comma list, most
   common first. **First, what they sell:** "physical products online, software or an app
   people sign up for, or something other businesses buy?" (`ecommerce` / `saas` / `b2b`;
   none fits -> leave `TODO`, drafts stay neutral). Then:
   - "All year round, in campaigns with start and end dates, or around seasonal moments?"
   - "A set budget per month or per campaign, each creator priced on their own, or no
     cash at all (product or commission only)?"
   - "The ONE number you judge a creator by: sales, signups, reach, the content itself,
     or demos and qualified leads?"
   - "How do you arrive at a fee: their views, a range per format, their quote,
     commission first, or product only?"
   - "A small test then grow, a one-off, or a multi-month ambassador deal?"
   - "Influencers, UGC creators, affiliates, creators through an agency, podcasters,
     newsletters?"
   Then the two-sentence pitch, in their words, unpolished (`{{PROGRAM_PITCH}}`). Campaign
   programs: current campaign, calendar, budget pot (internal only). Run `inbox program`:
   every answer recognised; tell them in one line the pack and modules it chose.
1. **`company.md`** - ask for their website, read it (and their pricing page) and
   draft every field you can. Then ask only about what the site can't tell you:
   the creator offer, what they gift creators, niches they avoid. Show the result
   and ask them to correct anything.
2. **`me.md`** - name, title, who they escalate to, the tools they use. Offer
   `none` as an answer everywhere; most solo operators have no CRM and that's fine.
3. **`deals.md`** - payment method and timing, tax (gross or net), usage rights,
   what a win is, the deal process. These move money: ask, never assume.
4. **`affiliate.md`** - "Do creators earn commission on sales?" No -> write `none` on
   the Program line and move on.
5. **`settings.md`** - add their own domains to `link_domains` (website, tracking
   links, link shortener) and teammates to `team_addresses`.

Ask in small batches (3-4 questions), with example answers. Fill what they tell
you; leave `TODO` for what they don't know yet and say drafts will stay silent on
those points until filled.

Optional: **creator notes**. "Do you already work with some creators? Paste a list
or a spreadsheet export and I'll create a note for each." One file per creator in
`~/.claude/inbox/creators/`, following `_example-template.md`.

## Stage 4 - Their voice (about 10 minutes)

Hand over to the `voice-builder` skill. This is the biggest single upgrade in draft
quality.

## Stage 5 - Their rates (about 10 minutes, for anyone who negotiates fees)

Hand over to the `rate-engine` skill ("set up my rates"). Skip it for `pricing:
commission` or `gifting` programs. `pricing: rate-card` sets fee bands (`unit=fee`)
instead of CPMs. Without rates, money
emails still get drafted, but they ask the creator for stats instead of naming a fee.

## Stage 6 - First real run

1. Recommend the permission setup below.
2. "Run my inbox, but only the 5 most recent unread emails" - the workflow respects
   a limit the user gives.
3. Walk them to Gmail's **Drafts** folder: each draft is threaded under the email it
   answers, and the originals are still unread.
4. Tell them how it gets better: "Send the ones you like, edit the ones you don't.
   Next run, I compare what you sent with what I drafted and learn from the edits."

## Safer permissions (recommend, and do it with their OK)

- **Don't run inbox sessions in "bypass permissions" mode.** Emails are written by
  strangers; normal permission prompts are a real safety layer.
- To avoid a prompt on every `inbox` call, add an allow rule to
  `~/.claude/settings.json` -> `"permissions": {"allow": ["Bash(inbox:*)"]}`.
  Show them the change before saving it.
- A mail connector enabled in Claude (Gmail, Outlook): find its send, reply, forward and
  trash tools in your own tool list by what they do - in the Claude app the server part
  is often an id (`mcp__1a2b3c4d__send_message`), which the guard can't tell is mail
  outside a run. Propose `"deny"` rules for those exact names in the same file.

## Installing Python

Macs: run `python3 --version`. If macOS offers to install developer tools, accept
and wait. If the version is below 3.9, install the latest from
<https://www.python.org/downloads/> (the macOS installer, next-next-finish), then
re-run `inbox setup`. Windows: install from python.org with **Add python.exe to
PATH** ticked; run commands in Git Bash or WSL.

## When something fails

Read the error, say what it means in one sentence, fix it, re-run. Common ones:

| Error | Meaning / fix |
|---|---|
| `Gmail is not connected yet` | Stage 2 |
| `expired or revoked` | `inbox auth` (and the weekly-logout fix for personal Gmail) |
| `Gmail libraries are not installed` | `inbox setup` |
| `no rates.md` / rates `TODO` | Stage 5, or carry on - money drafts stay in "ask for stats" mode |
| a draft refused with `errors` | the safety checks caught something; fix the draft text, not the check |
