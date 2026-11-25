---
name: playwright-personas
description: Account-aware browser automation. Use when Claude needs to navigate a site, fill a form, screenshot a page, scrape data, log into an account, or drive any web app on the user's behalf. Persistent per-account profiles via the `pw` wrapper keep every login alive across sessions. Includes the Google login bypass, token-discipline rules, and site-specific gotchas (YouTube Studio, Instagram).
allowed-tools: Bash(playwright-cli:*), Bash(pw:*), Bash(pw-login:*)
---

# Browser Automation

> **Check for a non-browser path first.** Driving a browser is the slowest, most
> fragile option. If an MCP or API covers the job, use that instead. Use this
> skill only when there is no cleaner programmatic path.

## Start here — pick the entry point

1. **Does the user have an account to use?** (Gmail, GitHub, Stripe, anything)
   -> Use the `pw` wrapper, not bare `playwright-cli`. Bare `playwright-cli open`
   starts a logged-out browser. `pw <account> open <url>` is already signed in.
   First-time setup is `pw-login <account> <url>` (see below).
2. **Is the target a known site with documented quirks?**
   -> Read the matching file in `references/` first. Each gotcha costs a wasted
   retry if you skip it.
3. **Will you repeat the same flow many times?** -> Write a Python script with
   `pw_helpers.py`, don't loop CLI calls. See Scripting repeated flows below.
4. **Anything else** -> plain `playwright-cli` commands below.

## The `pw` wrapper — multi-account, persistent login

Each account is its own on-disk Chrome profile at
`$PW_PROFILE_ROOT/<account>/` (default `~/.playwright-profiles/<account>/`),
so logins persist forever. `pw` and `pw-login` are shell functions that wrap
`playwright-cli`.

```bash
pw-login <account> <url>     # FIRST-TIME login only — opens real Chrome,
                             # user logs in by hand, closes the window.
pw <account> open <url>      # daily use — runs playwright-cli already logged in
pw <account> <cmd> [args]    # any playwright-cli subcommand for that account
pw accounts                  # list configured accounts
pw list                      # list running sessions
pw close-all                 # close all sessions
```

**Why two browsers?** `pw-login` deliberately opens vanilla Chrome (not a
Playwright-controlled browser) because Google's anti-abuse system blocks sign-in
inside any CDP-controlled browser ("this browser may not be secure"). After
the user logs in once, the saved profile carries the cookies, and `pw <account>`
reuses them via CDP. See `references/google-login-bypass.md` for the full story.

**Run `pw` through the Bash tool, not PowerShell.** `pw` is defined in
`~/.bashrc` (or `~/.zshrc`) AND in the PowerShell profile. The Bash tool loads
your shell rc, so `pw` resolves there. The PowerShell tool starts with no
profile, so `pw` is undefined in it. If you must use PowerShell — or want a
shell-agnostic call — run the raw equivalent that `pw open` expands to:

```bash
# pw <account> open <url>   ==
playwright-cli -s=<account> open <url> --profile=$HOME/.playwright-profiles/<account> --browser=chrome
# every command after that only needs the session — the profile stays attached:
playwright-cli -s=<account> <cmd> [args]
```

If a profile is signed out, ask the user to run `pw-login` — don't try to
automate past the Google block.

## Profile hygiene

- DO kill stale automation processes when sessions hang: `playwright-cli close-all`,
  or `playwright-cli kill-all` for zombies.
- NEVER run `delete-data` (or `pw <account> delete-data`) on a `pw` persistent
  profile. That erases the saved login and forces a redo of `pw-login`.

## Token discipline

Browser automation is a top token sink. Every command writes a page snapshot
and prints a link to it; reading those snapshot files is the cost. See
[references/token-discipline.md](references/token-discipline.md) for the rules.
Short version:

- **Selector-first.** Use a stable CSS / text=/role= selector instead of an
  `eNN` snapshot ref whenever possible. `click`, `fill`, `hover`, `snapshot`,
  `eval` all accept selectors directly — no discovery snapshot needed.
- **Partial snapshots.** `snapshot <target>` or `snapshot --depth=N` instead of
  the full tree. A full snapshot of an app like YouTube Studio is huge.
- **Grep, don't Read.** When a snapshot lands in a file, `Grep` it for the
  role/name/text you need — that returns the ref in one line — instead of
  `Read`-ing thousands of lines of YAML.
- **Batch multi-step flows into one `run-code` call** instead of N commands
  that each pay for a snapshot.

## Core commands

```bash
# Lifecycle
playwright-cli open                       # new in-memory browser
playwright-cli open https://example.com   # open + navigate
playwright-cli goto https://example.com
playwright-cli reload / go-back / go-forward
playwright-cli close

# Interact — <target> is an eNN snapshot ref OR a unique selector (CSS / text=)
playwright-cli click e3
playwright-cli click "#submit-btn"             # CSS selector — no snapshot needed
playwright-cli click "text=Sign in"            # text selector
playwright-cli type "search query"             # real keystrokes
playwright-cli fill e5 "user@example.com"      # fast set — fails on Polymer/React-custom fields
playwright-cli press Enter
playwright-cli select e9 "option-value"
playwright-cli check e12 / uncheck e12
playwright-cli hover e4 / drag e2 e8
playwright-cli upload ./document.pdf
playwright-cli dialog-accept / dialog-dismiss

# Inspect
playwright-cli snapshot                        # full accessibility tree
playwright-cli snapshot "#content" --depth=6   # partial + depth-capped (cheaper)
playwright-cli eval "document.title"
playwright-cli eval "el => el.textContent" e5
playwright-cli screenshot --filename=page.png
playwright-cli console / requests

# Advanced
playwright-cli run-code "async page => { ... }"   # arbitrary Playwright; batch flows here
playwright-cli route "**/*.jpg" --status=404      # request mocking
playwright-cli state-save auth.json / state-load auth.json
playwright-cli tab-new / tab-list / tab-select 0
```

Run `playwright-cli --help` for the full command list.

### Open parameters

```bash
playwright-cli open --browser=chrome|firefox|webkit|msedge
playwright-cli open --persistent
playwright-cli open --profile=/path/to/profile
playwright-cli open --headed                      # visible window
```

The `pw` wrapper already passes `--profile` and `--browser=chrome` for you.

## Snapshots

After each command playwright-cli writes a snapshot of browser state to a file
and prints a link:

```
### Snapshot
[Snapshot](.playwright-cli/page-2026-02-14T19-22-42-679Z.yml)
```

A snapshot is an accessibility tree of the page; each element is tagged with a
ref like `e1`, `e3`, `e15`. Those `eNN` refs are what `click` / `fill` / etc.
accept as a target — but they regenerate on every snapshot and only stay valid
until the page changes. Stable selectors are preferred (see Token discipline).

## Recovery from a failed action

When a `click` / `fill` / etc. fails (stale ref, element not found, element
not visible):

1. Take one fresh `snapshot` — the page likely changed and the old ref is gone.
2. Re-resolve the target (prefer a stable selector over the new ref) and retry once.
3. If it still fails, stop and report — don't loop. Check `references/` for a
   known cause (an interstitial, a Polymer-invalid field, a signed-out profile).

Two failures of the same step means something structural is wrong; a third
retry wastes tokens.

## Scripting repeated flows

Past ~3 repetitions of the same browser flow, stop issuing CLI calls and write
a Python script — it's deterministic, loops without per-step snapshot token
cost, and is reusable.

`pw_helpers.py` (under `~/.playwright-personas/python/`) factors the
boilerplate (the `pwcli` subprocess wrapper, `snapshot`, `find_ref`, `eval_js`,
and `click/fill/type/press` wrappers) into one importable module:

```python
import sys, pathlib
sys.path.insert(0, str(pathlib.Path.home() / ".playwright-personas" / "python"))
import pw_helpers as pw

pw.open_account("mygmail", "https://mail.google.com")
title = pw.eval_js("() => document.title", session="mygmail")
pw.close("mygmail")
```

## Browser sessions

```bash
playwright-cli -s=mysession open example.com --persistent
playwright-cli -s=mysession click e6
playwright-cli -s=mysession close
playwright-cli list
playwright-cli close-all
playwright-cli kill-all                  # force-kill stale/zombie daemons
```

Each session has isolated cookies, storage, tabs, and history. The `pw`
wrapper uses the account name as the session name.

## Local installation

If the global `playwright-cli` binary fails, fall back to `npx playwright-cli`.

## Reference docs

- [references/google-login-bypass.md](references/google-login-bypass.md) — why
  Google blocks Playwright/CDP browsers, what `pw-login` does, how the profile
  persists.
- [references/token-discipline.md](references/token-discipline.md) — full
  rules and patterns for keeping browser automation cheap.
- [references/youtube-studio.md](references/youtube-studio.md) — interstitial,
  Polymer inputs, the Publish-button trap.
- [references/instagram.md](references/instagram.md) — DOM-obfuscation
  workarounds via accessibility-tree locators.
