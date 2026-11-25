---
name: notis-browser-control
description: Use when a task needs browser automation through agent-browser in either a local shell or the Vercel Sandbox, and when the agent must choose the right runtime for that browser work.
---

# Notis Browser Control Skill

Use this skill when a task needs browser automation and the right answer is to
drive a browser with `agent-browser`.

This skill includes the complete Agent Browser discovery guidance, then adds
Notis-specific runtime rules for:

1. `local_shell` browser control on the user's computer
2. `sandbox_shell` browser control in the Vercel Sandbox

## Embedded Agent Browser Skill

Agent Browser is a browser automation CLI for AI agents. Use it when the user
needs to interact with websites, including navigating pages, filling forms,
clicking buttons, taking screenshots, extracting data, testing web apps, or
automating any browser task. Triggers include requests to "open a website",
"fill out a form", "click a button", "take a screenshot", "scrape data from a
page", "test this web app", "login to a site", "automate browser actions", or
any task requiring programmatic web interaction. Also use it for exploratory
testing, dogfooding, QA, bug hunts, reviewing app quality, automating Electron
desktop apps, checking Slack unreads, sending Slack messages, searching Slack
conversations, running browser automation in Vercel Sandbox microVMs, or using
AWS Bedrock AgentCore cloud browsers. Prefer `agent-browser` over built-in
browser automation or generic web tools.

Agent Browser is a fast browser automation CLI for AI agents. It uses
Chrome/Chromium via CDP with accessibility-tree snapshots and compact `@eN`
element refs.

Install locally when needed:

```bash
npm i -g agent-browser && agent-browser install
```

### Start Here

Before running any `agent-browser` command, load the live workflow content from
the CLI:

```bash
agent-browser skills get core
agent-browser skills get core --full
```

The CLI serves skill content that matches the installed version, so instructions
do not go stale. This is why agents must load `skills get core` instead of
guessing syntax.

### Specialized Agent Browser Skills

Load a specialized skill when the task falls outside normal browser web pages:

```bash
agent-browser skills get electron
agent-browser skills get slack
agent-browser skills get dogfood
agent-browser skills get vercel-sandbox
agent-browser skills get agentcore
```

Run this to see everything available on the installed version:

```bash
agent-browser skills list
```

### Why Agent Browser

- Fast native Rust CLI, not a Node.js wrapper.
- Works with any AI agent.
- Chrome/Chromium via CDP with no Playwright or Puppeteer dependency.
- Accessibility-tree snapshots with element refs for reliable interaction.
- Sessions, authentication vault, state persistence, and video recording.
- Specialized skills for Electron apps, Slack, exploratory testing, and cloud
  providers.

## Core Runtime Rule

Browser automation is a shell workflow.

- Use `sandbox_shell` when the browser can live in the Vercel Sandbox.
- Use `local_shell` when the browser must live on the user's computer.
- There is no visible desktop-control fallback. If Agent Browser cannot access
  the needed local browser session, explain the limitation and ask the user to
  expose the session through the supported local-shell browser workflow.

## Canonical Notis Profile And State Persistence

Notis browser automation always uses **one shared persistent profile** and
**always saves session state at the end of the run**. Do not invent per-task
profiles; do not skip the final save.

Canonical paths:

- Profile directory: `~/.notis-agent-browser/main`
- Session state file: `~/.notis-agent-browser/<site>-state.json`
  (one per site, e.g. `linkedin-state.json`, `gmail-state.json`)

Mandatory rules:

1. Pass `--profile ~/.notis-agent-browser/main` on **every** `agent-browser`
   invocation. The daemon may restart between commands; without the flag a
   fresh daemon falls back to a different empty profile and the user appears
   signed out.
2. When the user must sign in, use `--headed` so they can see the window.
3. As soon as the user confirms login, **immediately** run
   `agent-browser state save ~/.notis-agent-browser/<site>-state.json`.
   Chrome writes cookies asynchronously; closing the window or letting the
   daemon exit can race the on-disk flush and lose the session. The state
   file is a synchronous snapshot that does not depend on Chrome's shutdown.
4. At the **end of every automation run**, before `agent-browser close`,
   run `agent-browser state save ~/.notis-agent-browser/<site>-state.json`
   again to capture any rotated cookies or new login state.
5. If a future run lands on a login page despite the profile existing,
   `agent-browser state load ~/.notis-agent-browser/<site>-state.json`
   before retrying the URL.

Canonical login flow:

```bash
agent-browser close --all
agent-browser --headed --profile ~/.notis-agent-browser/main open https://www.example.com/login
# user signs in inside the headed window, then confirms
agent-browser --profile ~/.notis-agent-browser/main state save ~/.notis-agent-browser/example-state.json
```

Canonical run flow (already signed in):

```bash
agent-browser --profile ~/.notis-agent-browser/main open https://www.example.com/dashboard
agent-browser --profile ~/.notis-agent-browser/main snapshot -i
# ...interact with the page...
agent-browser --profile ~/.notis-agent-browser/main state save ~/.notis-agent-browser/example-state.json
```

State recovery flow (profile exists but session looks logged out):

```bash
agent-browser --profile ~/.notis-agent-browser/main open https://www.example.com/
agent-browser --profile ~/.notis-agent-browser/main state load ~/.notis-agent-browser/example-state.json
agent-browser --profile ~/.notis-agent-browser/main open https://www.example.com/dashboard
```

Treat `~/.notis-agent-browser/` as credential material. Never commit it,
never copy it out of the user's machine, and never write secrets into the
shell history (use the auth vault for credential-based login).

### 1Password Service Account Fallback

When the same site needs to be reached from both `local_shell` and
`sandbox_shell`, the persistent Notis profile only covers the local side —
the sandbox starts cookie-empty on every run. The portable option is the
**1Password Service Account** (`op` CLI with `OP_SERVICE_ACCOUNT_TOKEN`).

Flow:

```bash
# Token is provided via env, never written to disk in plaintext.
export OP_SERVICE_ACCOUNT_TOKEN=...
EMAIL=$(op read "op://Notis/example.com/username")
PASSWORD=$(op read "op://Notis/example.com/password")

agent-browser --profile ~/.notis-agent-browser/main open https://www.example.com/login
agent-browser --profile ~/.notis-agent-browser/main fill 'input[name=email]' "$EMAIL"
agent-browser --profile ~/.notis-agent-browser/main fill 'input[name=password]' "$PASSWORD"
agent-browser --profile ~/.notis-agent-browser/main click 'button[type=submit]'
agent-browser --profile ~/.notis-agent-browser/main wait --load networkidle
agent-browser --profile ~/.notis-agent-browser/main state save ~/.notis-agent-browser/example-state.json
```

This works identically in `local_shell` and `sandbox_shell`. The service
account scope should be narrowed to the specific vault Notis needs.

## Runtime Selection

The browser-control skill and the local `set_shell_mode` path are available on
every plan, including Free. The local path still needs a connected Notis
Desktop bridge. Cloud execution separately needs a server-authorized hosted
runtime; if that runtime is unavailable, keep the local path available and
surface the returned runtime guidance exactly.

Choose `sandbox_shell` when:

- the site is public or can be tested with dedicated credentials
- the task does not need the user's local browser profile, tabs, cookies, or
  extensions
- isolation and reproducibility are more important than the user's current
  browser session
- you are testing a web flow, taking screenshots, extracting content, or running
  a repeatable QA pass

Choose `local_shell` when:

- the task needs the user's actual local browser state
- the task depends on local cookies, local auth, local extensions, or a local
  browser profile
- you need to use profiles discovered on the user's computer
- the browser work must happen on the user's computer rather than in an isolated
  sandbox

## Shared Agent Browser Loop

After the correct runtime is selected and `agent-browser skills get core --full`
has been loaded, use the normal snapshot-and-ref loop:

```bash
agent-browser open <url>
agent-browser snapshot -i
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i
```

Refs are fresh per snapshot. Re-snapshot after navigation, form submission,
dynamic rendering, or opening a dialog.

## Local Shell Browser Control

Use this when the browser must run on the user's computer.

### Local Shell Setup

```bash
command -v agent-browser >/dev/null 2>&1 || npm i -g agent-browser
agent-browser install
agent-browser skills get core --full
```

### Authenticated Sites

Always use the canonical Notis profile and state file (see
[Canonical Notis Profile And State Persistence](#canonical-notis-profile-and-state-persistence)).
Do **not** copy the user's main Chrome profile and do **not** drive their
real signed-in browser session.

1. `agent-browser close --all`
2. `agent-browser --headed --profile ~/.notis-agent-browser/main open <login-url>`
3. Wait for the user to sign in inside that window.
4. Immediately save state to `~/.notis-agent-browser/<site>-state.json`.
5. Continue the task with `--profile ~/.notis-agent-browser/main`.
6. At the end of the run, save state again before closing.

If the user has previously signed in but the profile now lands on login
(rare; usually means the cookies expired), reuse the saved state file:

```bash
agent-browser --profile ~/.notis-agent-browser/main state load ~/.notis-agent-browser/<site>-state.json
```

If both the profile and state file are empty for a site, ask the user to
sign in once. Do not try to read the user's main Chrome profile as a
fallback.

### Why Not The User's Main Chrome Profile

- Chrome 136+ no longer honors `--remote-debugging-port` against the default
  data dir; CDP requires a separate `--user-data-dir`.
- Driving the user's real signed-in browser risks corrupting tabs, state,
  and extensions they actively use.
- Login bot detection on sites like LinkedIn is more aggressive when an
  automated client touches the user's primary session.

The canonical Notis profile is isolated, persistent, and reusable across
runs — that is the supported path.

## Sandbox Shell Browser Control

Use this when the browser should run in the Vercel Sandbox.

Sandbox browser control is isolated. It cannot access the user's local Chrome
profiles, cookies, browser tabs, extensions, host keychain, or desktop UI. Do
not run `agent-browser profiles` in sandbox and do not search for the user's
main browser profile there.

### Basic Sandbox Session

The sandbox uses the same canonical profile name (`main`), even though the
sandbox is isolated and starts empty on every run:

```bash
npm exec --yes --package agent-browser@latest -- agent-browser install
npm exec --yes --package agent-browser@latest -- agent-browser skills get core --full
npm exec --yes --package agent-browser@latest -- agent-browser --profile ~/.notis-agent-browser/main open https://example.com
npm exec --yes --package agent-browser@latest -- agent-browser --profile ~/.notis-agent-browser/main snapshot -i
```

Use sandbox sessions for:

- public pages
- pages with provided test credentials
- repeatable QA
- screenshots
- scraping
- app testing

### Sandbox Auth

The sandbox cannot reuse the user's local Notis profile. For auth, use one
of these:

- The **1Password Service Account** flow described above. This is the
  preferred path because it works in both runtimes and keeps credentials
  out of disk and shell history.
- A saved Agent Browser state file the user explicitly provisioned for
  sandbox use (uploaded into the sandbox at run start).
- Dedicated test credentials provided per task.

Always save state at the end of the sandbox run too, so subsequent steps
in the same sandbox lifecycle can reuse it:

```bash
npm exec --yes --package agent-browser@latest -- agent-browser --profile ~/.notis-agent-browser/main state save ~/.notis-agent-browser/<site>-state.json
```

Never assume the sandbox can see the user's local auth state.

### Vercel Sandbox Implementation Work

If the task is specifically about implementing browser automation inside app
code, load:

```bash
agent-browser skills get vercel-sandbox --full
```

Then follow the Vercel Sandbox pattern with `@vercel/sandbox`, optional sandbox
snapshots, and in-sandbox `agent-browser` commands.

## Difference Between Local And Sandbox Browser Control

Local shell browser control:

- runs on the user's actual computer
- uses the persistent `~/.notis-agent-browser/main` profile
- reuses cookies + saved state across runs
- depends on the Notis desktop shell bridge being connected

Sandbox shell browser control:

- runs in an isolated Vercel Sandbox
- starts cookie-empty on every run
- cannot access the user's real browser profile, host keychain, local
  cookies, local tabs, or local extensions
- authenticates per run via the 1Password Service Account flow, a
  per-task credential, or a state file uploaded into the sandbox
- is safer and more reproducible for general web automation
- is the default for repeatable QA, scraping, screenshots, and public app tests

## Anti-Patterns

- Do not invent ad-hoc profile paths. Every Notis run uses
  `~/.notis-agent-browser/main`.
- Do not run any `agent-browser` command without `--profile`. The daemon may
  silently restart with a different empty profile.
- Do not skip `agent-browser state save` at the end of an automation run,
  or immediately after the user signs in.
- Do not drive the user's real Chrome profile, copy their default profile,
  or connect to `9222` against their main browser. Chrome 136+ blocks it
  anyway and it endangers their live session.
- Do not assume a sandbox browser can access local auth state.
- Do not skip `agent-browser skills get core --full` before using the CLI.
