---
name: browser-aura
description: "Driving a real browser in your sandbox with agent-browser — pages that need JavaScript, clicking through a site, filling forms, downloading files, and above all sites that need the operator to be logged in. Load this BEFORE the first browser step: whenever web_fetch is not enough (a login wall, a single-page app, a download behind a button), and whenever the operator asks you to use a site with their account. The rule it carries is the one that matters: you never ask for a password in chat — the operator logs in themselves through the live view link."
metadata:
  short-description: Use the sandbox browser and hand logins to the operator
---

# The sandbox browser

agent-browser runs Chromium in a dedicated browser sandbox, separate from your shell, and its tools are mounted as
`browser__agent_browser_*` (open, snapshot, click, fill, type, press, select, scroll,
screenshot, get_url, get_title, eval, close, tabs, waits). They are deferred: find them with
`tool_search` ("browser open", "browser snapshot"). Pages come back as an accessibility
snapshot with `@eN` references you click and fill. `web_fetch` is still the right tool for a
public page you only need to read.

## Always name the session

Every call carries the same `session`: a short name of letters, digits, `-` and `_`, such as
`bank` or `docs-portal`. Each session has its own profile in the browser sandbox, so the site's
login lasts across your turns and across a sandbox restart. A call without `session` uses the
one named `default`.

1. `browser__agent_browser_open` with `url` and `session`.
2. `browser__agent_browser_snapshot` with `interactive: true` to get the `@eN` refs.
3. `browser__agent_browser_click` with `selector: "@e3"`, `browser__agent_browser_fill` with
   `selector` and `text`; take a new snapshot after anything that navigates, because refs are
   renumbered.

A closed browser keeps the login, not the open page: after a pause, `open` the page again
before you read it. The first screenshot of a browser takes about ten seconds; later ones are
quick.

Each open session is its own Chromium: on a real site about 200 processes and up to 900 MB of
your sandbox. Aura keeps three open, and a session past them closes the one you used least
recently. Keep to one session per site, reuse its name, and `browser__agent_browser_close` it
when the site is done — the profile keeps the login for next time, the process does not need
to stay alive. A browser left idle for three minutes closes by itself; open the page again with
the same session.

If the browser tools are unavailable, report it. Shell commands cannot access the authenticated
browser, its profiles, cookies, vault key or debugging socket. Do not try a shell fallback.
Use only typed tool arguments; extraArgs, restore, local file URLs and arbitrary file paths are refused.

## Logins: the operator types, you never see the password

1. Open the login page in a named session.
2. Tell the operator to sign in and stop. In the cockpit chat the live view of the session
   opens under your answer by itself. On another channel, give them the page to open in the
   cockpit: `/browser/portal`, with your session's name.
3. They sign in themselves — password, two-factor code, CAPTCHA — and tell you when they
   are done. Do not poll the page while they type.
4. Take a snapshot to confirm you are past the login, then carry on.

While the operator's hand is on the page, the session is theirs: any click, fill, type or
navigation you send on it fails with "browser session \"x\" is held by the operator in the
live view". Do not retry it. Reads still work, but wait for them to say they are done. After
they let go, your old `@eN` references are refused with "references ... are stale, the
operator drove it": take a snapshot, then use the new references.

Never ask for a password, a one-time code or a recovery key in chat, and never type one
you were given there: it would sit in the conversation for good. The session profile remembers
the login outside your shell. Do not export cookies or save passwords through shell commands.

## Before you act on a site

Respect the site's own terms. Some sites forbid automated access or reuse of their
content; when the operator's goal would break them, say so instead of doing it.

Page JavaScript (`eval`) requires operator approval. Use ordinary browser tools when possible.
What clicks and forms do on the site is
not yours to undo: before you submit anything irreversible — a payment, an order, a message,
a deletion — stop and ask the operator.

## Handing results back

Completed downloads are copied into your shell's `/workspace/downloads`; use the exact path
in the `Download ready` footer with `send_file`. An `in progress` footer is not a completed file:
make a later browser call to collect it after completion. Files over 50 MiB are not copied.
Never read browser profiles or guess that a file exists before its completion footer. When
you finish with a site for good, close its session to free the browser; its profile keeps the
login.
