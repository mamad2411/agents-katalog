---
name: autonomous-setup
description: "Autonomous: Setup. Gets a Mac or Windows machine ready for the autonomous skills and a hands-on workshop from a one-line prompt that names the event and links here: the agent gets the skills, opens a setup checklist canvas in the same chat, installs what's missing, starts the sign-ins, and has the person test each item with a Try-it prompt. Never handles passwords or keys. The full setup covers VS Code Insiders, GitHub CLI, git, Node and Yarn 1, Python, ffmpeg, a browser, the workshop settings, a private copy of the skills with the daily sync and weekly update, Work IQ, Playwright, Computer Use, dictation, and optional Azure, a dev box and research. A prompt naming a workshop folder takes the light AI-First path: portable tools, light skills and a practice repo, only what the person checks, after Confirm. Resumable. Use for 'set me up for <event>', 'set me up on my dev box', 'set up the autonomous skills', 'check my setup', 'continue my setup', or 'am I ready for the workshop'."
---

# Autonomous: Setup

One line takes a person from a fresh machine to ready: the tools, the workshop settings, their own private copy of
the skills, the connections agents use (Work IQ, Playwright, Computer Use), dictation, and the optional extras. Each
item gets installed, then the person tests it for real with a "Try it" prompt. It runs in the Agents window (or
Copilot CLI) on macOS and Windows, and the same line picks up again at any point.

People do this alone, before the workshop, so every message says plainly what's happening and what they need to do.

A prompt that names a workshop folder ("... in ~/ai-first-workshop") takes the light AI-First path instead: a public
setup for designers on their own laptops, with portable tools in that folder and nothing installed until they click
Confirm on the canvas. It's in [`references/ai-first.md`](references/ai-first.md), and it starts below, in "Start here".

## Start here

Do these first, in order, before anything else in this file.

0. **Which path.** When the prompt names a folder ("... in ~/ai-first-workshop. Follow ..."), do "The AI-First path"
   just below instead of steps 1 to 3, then follow [`references/ai-first.md`](references/ai-first.md) and nothing
   else in this file. Without a folder, it's the setup in the rest of this file, steps 1 to 3 first.
1. **Work from the clone.** If you're reading this anywhere other than
   `$HOME/.copilot/autonomous-output-skills/autonomous-setup/SKILL.md` (on GitHub, from a link, in another folder),
   clone the repo there first: `git clone https://github.com/eli-w-king/autonomous-output-skills
   "$HOME/.copilot/autonomous-output-skills"`. When it's already there, pull instead:
   `git -C "$HOME/.copilot/autonomous-output-skills" pull --ff-only` (if that can't fast-forward, keep what's there
   and say so in one line). Then read that copy's `autonomous-setup/SKILL.md` from the top and follow it, not the copy
   you started from. `COPILOT_HOME`, when set, replaces `$HOME/.copilot`; on Windows write `$HOME\.copilot\...`.
2. **Stay in this chat.** Never set, change or move this session's workspace, not even to the clone. Use full paths
   (rule 9).
3. **Save the values from the prompt** (below) with `check-setup.py remember`, before the first check.

### The AI-First path

1. **The folder** is the one the prompt names (`~/ai-first-workshop`; on Windows `$HOME\ai-first-workshop`). Make it
   if it's missing. Install nothing else yet: the person chooses on the canvas first.
2. **Get the skills into `<folder>/autonomous-output-skills`**, never into `~/.copilot/autonomous-output-skills`:
   - **When git works without installing anything,** clone shallow: `git clone --depth 1
     https://github.com/eli-w-king/autonomous-output-skills "<folder>/autonomous-output-skills"`, or pull with
     `git -C "<folder>/autonomous-output-skills" pull --ff-only` when it's there. On a Mac, git works when
     `xcode-select -p` succeeds or a git is in `/opt/homebrew/bin` or `/usr/local/bin`. Never run `/usr/bin/git`
     without Apple's command line tools: it opens a 1.3 GB install dialog.
   - **Otherwise download it.** macOS: `curl -fsSL
     https://github.com/eli-w-king/autonomous-output-skills/archive/refs/heads/main.tar.gz | tar -xz -C "<folder>"`,
     then rename `autonomous-output-skills-main` to `autonomous-output-skills`. Windows (PowerShell, one at a time):
     `curl.exe -fsSL -o "<folder>\skills.zip" https://github.com/eli-w-king/autonomous-output-skills/archive/refs/heads/main.zip`,
     `tar.exe -xf "<folder>\skills.zip" -C "<folder>"`, rename the folder the same way, and delete the zip. When a
     copy is already there, move it aside first.
3. **Then read `<folder>/autonomous-output-skills/autonomous-setup/references/ai-first.md` and follow it.** Stay in
   this chat, as everywhere in this skill. Its first step copies the canvas into this chat; until then, don't call
   `list_canvas_capabilities` or `open_canvas`, and never guess a canvas id. Part 2 below isn't for this path.

### Values from the prompt

The prompt names the event and its hosts and links here, like `Set me up for "<Series>: <Title>", hosted by <Host> +
<Host>, including research and a dev box. Follow <link to this file>`. Take the values from the prompt, never from
this file:
- **The quoted name.** With a colon ("Series: Title"): `subtitle` is the part before the first colon, `title` the
  part after it, and `checkInChat` (the meeting chat for the Work IQ check-in) the whole name. Without a colon, the
  whole name is both `title` and `checkInChat`.
- **"hosted by ..."** is the `presenter`, exactly as written (both names, with the plus).
- Save them now: `check-setup.py remember --set "title=<title>" --set "subtitle=<subtitle>" --set
  "presenter=<presenter>" --set "checkInChat=<whole name>"`, and pass them to the canvas when you open it.
- **"including research and a dev box"** means they asked for both: `--set research_requested=yes --set
  devbox_requested=yes` in the same command. Turn both on when the canvas opens, and take it as their okay to create
  one dev box in the top pool that stays on, after you've shown the plan. Without it, both stay optional: offer them,
  never push.
- **"on my dev box"**: this is their dev box. Add `--set setup_mode=devbox` and see "Dev box mode". The prompt decides
  the mode (`os.devbox_hint` may confirm it, never override it); a request for "a dev box" there is ignored.
- Never write the event's own names into this skill or its files: they're published, and the publish check refuses
  private names.

## The rules

1. **Detect first, then show the plan.** Run the check, show what is missing and what the standard setup will
   change, then continue. Do not add a separate "reply go" stop for work the setup request already authorizes.
2. **Stay within the requested setup, and do the terminal steps yourself.** The standard tools, private skills copy,
   daily sync, weekly update and connection plugins are the setup, and so is what the prompt asked for (research, one
   dev box). New paid or cloud resources beyond that, destructive changes, study launches and sending messages still
   need explicit approval. Never send the person to a terminal: you run the commands, start the sign-ins and open the
   installers. Never run `sudo` or anything that asks for a password in your shell. What needs their password asks
   for it in its own window (the macOS Installer for Homebrew), and sign-ins finish in their browser. The one
   exception is Homebrew on an Intel Mac, whose install script they run in Terminal.
3. **Never handle secrets.** No passwords, tokens or API keys in the chat, in commands, or in files you write.
   Sign-ins finish in the person's own browser (you start them; they approve), and keys go into a file they edit
   themselves. Never print or read back a secret file.
4. **Install, then test.** An item is installed when a real check passes (a version prints, a setting reads back, a
   server is configured). It's tested when the person's own Try-it prompt works; record that with
   `check-setup.py tested <item>`. Record steps with `check-setup.py mark`, which the readiness checklist uses.
5. **Never send, post, publish or launch** anything unless the person typed the Try-it prompt that asks for it, or
   approved the exact text. The Work IQ check-in goes out once and is read back afterwards.
6. **Keep moving.** When a step is blocked (a license, an admin, an account limit, a person's sign-in), mark it
   `blocked` or `pending` with what to do next and go on. Offer the optional steps; never push them.
7. **Talk like a person.** Many attendees are designers. Say what each step is for in one sentence, what they'll see,
   and what you need from them. Short messages, no jargon, no walls of output.
8. **Shared machine manners.** Start nothing visible they didn't ask for, stop every process you started, and leave
   their other apps, windows and settings alone.
9. **Stay in this chat.** The setup runs in a session with no workspace (Chat). Never set, change or move the
   session's workspace (no `set_workspace`), even when a step names a folder: use full paths instead
   (`$HOME/.copilot/...`). In Autopilot the host confirms a workspace change for the person, so they'd never see it.

## Autopilot and Allow all: where it still stops

The person sets the picker to **Autopilot** and **Allow all** before pasting the prompt, so commands run without an
approval click each time. Some things still need them, and Autopilot changes how you ask:
- **Questions:** in Autopilot the host answers `ask_user` for the person ("The user is not available to answer your
  question..."), so never use `ask_user` for a decision. Write the question in chat (and on the canvas), then end
  your turn (call `task_complete` with the question if Autopilot keeps going). Their reply continues the setup.
- **Passwords:** a command in your shell that asks for a password or secret is cancelled ("Auto-approve / autopilot
  mode cannot safely supply secrets"), so never run one, and never `sudo`. On an Apple Silicon Mac, Homebrew comes
  from its signed installer package: you download it and `open` it, and the macOS Installer asks for their password
  in its own window. On an Intel Mac, Homebrew's install script is theirs to run in Terminal.
- **Sign-ins:** you start them and they approve in the browser. GitHub CLI: `gh auth login` in an async shell prints a
  one-time code; you show the code, open the page and wait ("Machine"). `az login` opens their browser and returns
  once they're signed in. Work IQ asks as soon as the next chat starts: VS Code shows "MCP authentication required"
  for workiq with **Authenticate**; they click it and sign in with their work account in the browser (and consent if
  asked). The chat keeps working meanwhile. On a dev box, the Windows and VS Code sign-ins are theirs, on the box.
- **Computer Use:** in Autopilot the agent can't turn it on (the host reports it as unattended) and the app approval
  prompt is cancelled. They type `/computer on` themselves, allow the two macOS permissions in System Settings, and
  switch the picker to Interactive for the Computer Use Try-it (then back to Autopilot).
- **The restart** VS Code asks for after a settings change (for Computer Use), and the **microphone** permission the
  first time they dictate.
- **New tools need a new chat:** Work IQ's plugins and the Playwright MCP server load when a chat starts, so you start
  that chat yourself ("The next chat").
- [check] Work IQ: if its server asks for a confirmation in chat, Autopilot cancels it; switch to Interactive for
  the check-in then.

## The next chat

When the setup needs a chat that starts after something was installed (Work IQ and Playwright, or canvases that
were off when this chat started), start it yourself with `create_session`: a `title` like "Workshop setup
(continued)" and a `prompt` like "Continue my workshop setup: follow
$HOME/.copilot/autonomous-output-skills/autonomous-setup/SKILL.md, Resuming." Pass no `model` and nothing else. Without
`model`, the new chat keeps this chat's GPT-6 Astra, Max, 1M, Autopilot and Allow all; with `model` set (even
to the same model) its effort dropped to Medium. Then tell the person in one line that the setup continues in that
chat (it's under this one in the session list), say it on the canvas (`setStep`), and end your turn so only one chat
works at a time. Never ask them to start a chat or paste the prompt again.

## Where things are

- `<skill>` is this skill's folder: `~/.copilot/autonomous-output-skills/autonomous-setup` when the setup starts from
  the clone, `~/.copilot/skills/autonomous-setup` once the skills are installed. `COPILOT_HOME`, when set, replaces
  `~/.copilot` everywhere.
- Run the scripts with `python3` on macOS and `python` (or `py -3`) on Windows; `<py>` below means that one. On
  Windows, `python3` is the Microsoft Store stub, so never use it there. The scripts use only the standard library and
  never prompt.
- Windows shell habits: PowerShell 5.1 has no `&&` (run commands one at a time), use `curl.exe` (plain `curl` is an
  alias), write paths as `$HOME\.copilot\...` (it passes `~` to programs as is), and call `npm.cmd`, `npx.cmd` and
  `yarn.cmd`, which work under any PowerShell execution policy.

| Script (`<skill>/scripts/`) | What it does |
|-----------------------------|--------------|
| `check-setup.py` | the check (JSON, or `--format text`); `mark`; `tested`; `remember`; `readiness`; `state` |
| `canvas-extension.py` | `status`, `install`, `remove` the setup canvas in Copilot's user extensions folder |
| `workshop-settings.py` | `diff`, `apply` (backs up first), `restore` for the workshop's VS Code settings |
| `mcp-servers.py` | `status`, `add playwright`, `add devbox`, `remove` in Copilot's MCP config |
| `devbox.py` | a dev box that stays on: `status`, `pools`, `create`, `wait`, `link`, `delete` and the admin message |
| `practice-repo.py`, `screenshot.mjs` | the practice repo, for the workshop itself (not used during setup) |
| `ai-first.mjs` | the AI-First path, with no Python: `check`, `canvas`, `install <item>`, `env`, `automation`, `record`, `uninstall` ([`references/ai-first.md`](references/ai-first.md)) |

- Workshop values are in [`references/workshop.json`](references/workshop.json), the settings in
  [`references/workshop-settings.jsonc`](references/workshop-settings.jsonc).
- Progress lives in `~/.copilot/workshop-setup/state.json` (steps, answers and tests, never secrets), backups and
  logs next to it.
- Per-OS install commands and traps: [`references/machine.md`](references/machine.md). Work IQ, Playwright and
  Computer Use: [`references/connections.md`](references/connections.md). Azure, dev box and research:
  [`references/optional.md`](references/optional.md).
- Every item in the check's JSON has `group` (basics, workshop, connections, yours, optional, later), `try_it` (the
  prompt the person copies to test it, or null) and `tested`. `summary` has `done` and `total` (required items, not
  counting `later`), `tested` and `later`.

## Before the prompt (what the person already did)

The workshop page has people do these first, in this order, so canvases are already on when the prompt arrives:
1. **Install or update VS Code Insiders.**
2. **Sign in to GitHub** with the account that has Copilot. Agents run on that account.
3. **Open the Agents window.**
4. **Paste the workshop settings into User settings (JSON)** (the snippet in `references/workshop-settings.jsonc`)
   and restart when VS Code asks (only Computer Use needs it). The snippet turns the agent sandbox off (with it on, the
   setup can't write outside its folder, so it can't clone the skills into `~/.copilot` or install tools, and a chat
   without a workspace can't start), turns on canvases (the setup checklist) and cloud dictation, starts new chats on
   GPT-6 Astra (`chat.defaultModel`; the effort still starts at Medium, so Max stays a step), and turns on what
   later modules use. In the editor window, the settings that exist only in the Agents window show greyed out; that's
   expected.
5. **Turn on Dev Tunnels:** the radio tower icon at the top right of the Agents window (its tooltip says "Remote
   Connections: Off"), then **Dev Tunnels**, so a dev box can reach this computer later. It's shared only while
   Insiders is open.
6. **Start a new chat, set up exactly like this.** No project or folder is needed:
   - Workspace: **Chat**.
   - Model: **GPT-6 Astra**.
   - Reasoning effort: **Max**.
   - Context: **1M**.
   - Mode: **Autopilot**.
   - Permissions: **Allow all** (click **Enable** when asked).
   - Sandboxing for terminal: **Off**.
7. **Paste the one-line prompt.**

## Dev box mode

When the prompt says "on my dev box", this machine is their dev box: read
[`references/devbox-mode.md`](references/devbox-mode.md) before Part 1. The same setup, with Google Chrome required,
`--weekly none`, a Work IQ Try-it that reads, and four items skipped.

## Part 1: a quick check, in chat

1. On Windows, if `python` doesn't run (or is the Microsoft Store alias), say so and install Python first
   ([machine](references/machine.md), "Python and Pillow"), since every script needs it.
2. The values are saved ("Start here"). Run `check-setup.py --quick` (JSON) and read `items.settings` (`matching`,
   `missing` and `different` against every key in the snippet, `total` of them) and `items.dictation`.
3. **A setting missing or different:** list them in one short message and add them: `workshop-settings.py diff`, then
   `apply --json` (it backs up first and keeps everything else). The prompt is the okay. When the result says
   `restart_needed`, VS Code asks "A setting has changed that requires a restart to take effect.": they click
   **Restart**, reopen this chat from the session list and say "continue my setup". Mark `settings ok` once the check
   shows all of them.
4. **This chat's picker:** check it's on **GPT-6 Astra**, **Max** and **1M**. If the host doesn't expose these,
   ask them to check the picker rather than claiming you verified it. Autopilot: if `ask_user` comes back with the
   host's automatic reply ("The user is not available..."), it's on. Allow all can't be read from here: ask them to
   check the picker says **Allow all** (and **Sandboxing for terminal** is off), and to tell you if an approval prompt
   ever shows up.
5. Then open the canvas, in this chat (part 2). If canvases were off when this chat started (`chat.canvases.enabled`
   was missing), this chat has no canvas tools: add the setting, then continue in "The next chat".

## Part 2: the setup canvas

### Open the canvas, in this same chat

<!-- CANVAS: the setup canvas (plugins/workshop-setup/extensions/setup-checklist), canvas id autonomous-setup-checklist. -->
On the AI-First path, skip this section: `references/ai-first.md` copies and opens the canvas.

1. `list_canvas_capabilities` with canvasId `autonomous-setup-checklist`. When it's listed (a machine with the
   workshop-setup plugin, or a copy from an earlier run), use it: go to step 4 and don't copy anything.
2. Not listed: `<py> <skill>/scripts/canvas-extension.py install --json`. It copies the canvas from the clone
   (`plugins/workshop-setup/extensions/setup-checklist`) into Copilot's user extensions folder
   (`~/.copilot/extensions/setup-checklist`), and copies nothing when the workshop-setup plugin is installed. Then
   `extensions_reload` (find it with tool search) and `list_canvas_capabilities` again (a plugin installed now would
   only load in later chats). Use one or the other, never both: with both, every chat sees the canvas twice.
3. "Multiple canvases match" (an older machine with the plugin and the copy): open it with `extensionId`
   `plugin:workshop-setup:setup-checklist`, then `canvas-extension.py remove`, so later chats see it once.
   `skipped: "plugin"` from step 2 (the plugin is installed but not in this chat): the canvas comes up in "The next
   chat". Still not listed after the reload (canvases off for this chat): "The next chat" too.
4. `open_canvas` with canvasId `autonomous-setup-checklist`, instanceId `workshop-setup`, and input
   `{title, subtitle, presenter, checkInChat, skillsDir}` from the remembered values (`skillsDir` is the clone,
   `~/.copilot/autonomous-output-skills`; on a dev box, `checkInChat` is `""`). Every field is optional; pass `{}`
   when there's nothing. Reopening the same instanceId keeps its state, so resuming is `open_canvas` again, then
   `getState`.
5. When the prompt asked for research and a dev box (`research_requested`, `devbox_requested`): `setItem {id:
   "research", status: "todo", note: "You asked for this in your prompt."}` and the same for `devbox`, which turns
   both on. In dev box mode, see its reference for the canvas.
- The canvas runs `check-setup.py` itself. `getState` returns `progress {done, total}`, `step`, the person's
  `choices` for the optional items (`azure`, `devbox`, `research`: true, false or null), and `items` with each status.
- On each item: `setStep {id}`, then `setItem {id, status: "working"}`. When they have to act:
  `setItem {id, status: "needs-you", note, commands}` (plain steps, one per line, and copyable commands). After an
  install the check proves: `refresh` (or `setItem installed`), and the page shows its Try it prompt. After their Try
  it works: `check-setup.py mark <step> ok`, `check-setup.py tested <item>`, then `setItem {id, status: "tested"}`.
  Failures: `setItem failed` with the exact error line. Statuses: todo, working, needs-you, installed, tested,
  skipped, failed. Ids are the check's item ids plus `weekly`, `dictation`, `voice`, `taste`.
- `check-setup.py mark <step> ok` counts as tested on the canvas, so mark a step `ok` only after its Try it worked
  (items without a test, like the tools and the settings, are done when the check shows them).
- No canvas tools at all (an older host, or canvases off by policy): keep going in chat. Show
  `check-setup.py --format text` in a few lines at the start and after each item, and the Try-it prompts (`try_it` in
  the check) as a list.
<!-- /CANVAS -->

### Show the plan

Build the plan from the check: every missing tool with its install command, the private copy of the skills and
everything that step changes (`gh auth setup-git`, the skills installed into `~/.copilot/skills` with backups, the
daily sync job and its macOS "Background Items Added" notice, the weekly automation), the Work IQ plugins, the
Playwright MCP server, and the optional items they turned on (`getState` `choices`) or asked for in the prompt: for a
dev box, the box `devbox.py` would create (project, pool, size, region; it stays on), and for research, the Outset
key and the two sign-ins. Post a short explanation, then proceed with the requested standard setup. Pause only for a
real choice, a sign-in, a password in an installer window, secret entry or a separately authorized change, not a
second blanket confirmation. Plan on about 45 minutes for the whole setup on a laptop that already has Homebrew, Node
and git, up to 75 on a brand-new Mac [check].

### Then, without stopping

Work through the items in this order. After each one: prove it, mark it, and point at its Try-it prompt. A dev box
the prompt asked for takes 30 to 90 minutes to provision, so start it right after the plan and keep going. Batch the
items that need a new chat: install Work IQ and Playwright, then start "The next chat", where they test both, sign in
to User Interviews, and the setup goes on.

#### Machine

Why: the tools every module uses.
- They're signed in to GitHub with Copilot (they're chatting with Copilot): `check-setup.py remember --set
  copilot_signed_in=yes`. When the check lists more than one GitHub CLI account, the plan names the one it will use
  (say which are Microsoft-managed). Missing tools are in the plan with their commands.
- **GitHub CLI sign-in, done by you:** run `gh auth login --hostname github.com --web --git-protocol https` in an async
  shell. With no terminal attached it prints a one-time code ("First copy your one-time code: XXXX-XXXX") and
  https://github.com/login/device, then waits. Show the code in chat and on the canvas (`setItem {id: "gh", status:
  "needs-you", note: "Enter this code on the GitHub page that just opened, then approve.", commands: ["<code>"]}`),
  open the page (`open https://github.com/login/device`; on Windows `Start-Process https://github.com/login/device`),
  and wait for the command to exit. Then `gh auth setup-git`, so git uses that sign-in.
- **Homebrew missing on a Mac.** Apple Silicon: download the newest release's `Homebrew-<version>.pkg` from
  https://github.com/Homebrew/brew/releases (signed with a Developer ID and notarized; `pkgutil --check-signature`
  shows it) and `open` it: the macOS Installer asks for their password in its own window. Then add
  `eval "$(/opt/homebrew/bin/brew shellenv)"` to `~/.zprofile` (once) and run it in your shell. Intel: the install
  script, which they run in Terminal. Details: [machine](references/machine.md).
- Install one tool at a time, re-run the check after each, and refresh PATH on Windows. Details and traps:
  [machine](references/machine.md).
- Yarn 1 comes from `npm install -g yarn`, never Corepack. A global install ignores a project's `.npmrc`, and
  public npm is blocked or unreliable on Microsoft-managed devices, so when the check's `npm.uses_feed` is false, ask,
  then point npm at Microsoft's package feed first (no sign-in; managed Macs already have it):
  `npm config set registry https://packagefeedproxy.microsoft.io/npm/`. Say what it changes when you ask: npm uses
  the feed for all their projects from then on, and the feed holds brand-new package versions back for 7 days. On
  Windows use `npm.cmd` for both.
- Windows: when the check's `powershell.policy` is Restricted (the client default), `npm` and `yarn` typed in
  PowerShell fail with "running scripts is disabled on this system". Offer
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, since the modules have them type `yarn` themselves.
- Commit identity missing: ask for the name to use and suggest the GitHub noreply email.
- Prove: the check shows every machine item ok. Mark:
  `check-setup.py mark machine ok --set copilot_signed_in=yes --set github_account=<login>`.

#### Skills and the weekly update

Why: their own private copy of the skills, so the skills learn from their corrections every week and they review
each change as a pull request; Eli's updates come in the same way.
- Skip this step when the check's `skills.mode` is `maintainer` (the machine already runs the two-repo sync).
- The plan offers: a private copy `<login>/autonomous-output-skills` (recommended), one they already have, or just the
  skills without a copy for now.
- With a copy, from the clone (`~/.copilot/autonomous-output-skills`):
  `<py> tools/sync-skills.py setup-attendee --private-repo <owner>/<name> --create --dry-run --json` and check its
  `steps` against the shown setup plan: the private copy on GitHub, `gh auth setup-git` (git uses their GitHub
  CLI sign-in from then on), the skills installed into `~/.copilot/skills` (any old copies backed up), and a daily
  sync job (launchd or Task Scheduler). On a Mac, registering the job shows a "Background Items Added" notification;
  tell them it's expected. Then run it without `--dry-run`. It points `origin` at their copy and a fetch-only
  `public` at the shared repo, keeps the clone on the review branch, installs the skills with backups, and schedules
  the daily sync. On
  `ok: false`, each entry in `problems` has a `fix`; exit code 2 means it refused (a maintainer setup, a public repo).
- The weekly update: with the `configureAutomation` tool, call it with exactly
  `schedule.weekly.automation.configureAutomation` from that JSON (autopilot, full auto-approve, the top model at max
  effort), run it once with `runAutomation`, and check that run with the command in `schedule.weekly.automation.check`
  (`automations/run-weekly-skill-miner.py --check-run --json`; it passes when the run had max effort, the long context
  and no approval left waiting). Without the tool, walk them through `schedule.weekly.automation.steps` in the Agents
  window's Automations view, or import the blueprint `automations/weekly-skill-update.automation.md`. Then follow
  `next`, and `automations/ATTENDEES.md` in the clone for anything else. GitHub CLI must be signed in (the machine
  step) before this runs.
- Without a copy: `node tools/install-devbox.mjs` installs the published skills (with backups) and nothing else.
  Mark it with `--set skills_private_copy=no`, so the checklist doesn't list the copy as missing.
- Prove: `<py> tools/sync-skills.py status --json` shows `mode` attendee, their copy as `origin`, and the daily sync
  registered: `setItem {id: "skills", status: "installed"}`. After the proof run's `--check-run` passes: `mark weekly
  ok`, `tested weekly`, `setItem weekly tested`.
- Try it (skills), in the next chat: "List the skills from my copy." When that works: `mark skills ok
  --note "<owner>/<name>"`, `tested skills`, `setItem skills tested`.

#### Work IQ

Why: agents can read their mail, meetings and Teams (only what they can see) and post what they ask for.
- Install the two official plugins yourself, never through the person's terminal
  ([connections](references/connections.md), "Work IQ"): `copilot plugin marketplace add microsoft/work-iq`,
  `copilot plugin install workiq@work-iq`, `copilot plugin install workiq-productivity@work-iq`. When the check's
  `items.workiq.copilot_cli` is null or `copilot_cli_is_vscode_shim` is true (VS Code's `copilot` command can only
  install Copilot CLI from an interactive terminal), install Copilot CLI first: `npm install -g @github/copilot`
  (`npm.cmd` on Windows). Mark `workiq pending --note "installed; test it in the next chat"`.
- When you start the next chat, tell them it will show "MCP authentication required" for workiq: Authenticate, then
  sign in with their work account in the browser.
- Try it, in the next chat: the canvas shows the check-in prompt from `items.workiq.try_it`. With a `checkInChat` it
  posts "Work IQ is set up" in that meeting chat (typing it is their okay), then reads the chat back and confirms
  exactly one copy is there; a timeout or unclear result is never a reason to post again. Without one, it reads their
  next meeting's subject. Sign-in, consent and license problems: mark `blocked` with the next step and who to ask.
- When it works: `mark workiq ok` and `tested workiq`.

#### Playwright

Why: agents open pages, click, fill forms and take screenshots in a real browser.
- `mcp-servers.py add playwright --dry-run --json`, then without `--dry-run`. It adds the Playwright MCP server
  (`@playwright/mcp`, pinned to the newest release, since a registry's "latest" can be an old build) on their
  installed Chrome or Edge, so no browser downloads. It's already there if `items.playwright.ok` is true. Its browser
  keeps its own profile, so a site they sign in to there stays signed in for later chats.
- Then start "The next chat" (Work IQ and Playwright both load there).
- Try it, in the next chat: "Use Playwright to open https://code.visualstudio.com, take a screenshot and show it to
  me." Show them the screenshot. Then `mark playwright ok` and `tested playwright`.

#### Computer Use

Why: agents can work in desktop apps in the background, like writing a line in Notes, with their approval per app.
- The setting is part of the snippet, and the restart turned it on. They type `/computer on` and click **Turn On**
  (Autopilot can't do this for them), then on a Mac allow Screen Recording and Accessibility in the Set Up Computer
  Use dialog until it says "Computer Use is ready." ([connections](references/connections.md)).
- Try it with the picker on **Interactive** (the app approval prompt can't show in Autopilot): "Use Computer Use to
  write "Computer Use works" in a new note in Notes." (on Windows: "...open Notepad and type "Computer Use works".
  Don't save it."). Then back to Autopilot, `mark computer-use ok` and `tested computer_use`.

#### Dictation

Why: talking to the agent is often faster than typing, and the cloud model needs no download.
- `items.dictation.ok` is true once the snippet's `"dictation.model": "mai"` is set (the same Microsoft AI voice
  service Voice Mode uses).
- Try it: "Click the mic in the chat input, say "Dictation works", and send it." The first time, macOS asks to allow
  the microphone. When their dictated message arrives: `mark dictation ok` and `tested dictation`.

#### Your voice and taste

<!-- VOICE-TASTE: the person's own voice and taste ships in a later version. Its step text goes here, with the
canvas items voice and taste and their check-setup.py items. Until then, skip it: nothing to do, nothing on the canvas. -->

#### Optional: Azure, a dev box, research

What they turned on on the canvas or asked for in the prompt. Follow [optional](references/optional.md) and mark the
rest `skipped`.
- **Azure:** you run `az login`; it opens their browser and returns once they're signed in (never
  `--use-device-code`).
- **A dev box:** `devbox.py status --json` first (green when they already have a box that stays on). Otherwise, with
  the prompt's okay (or theirs), create one box in the top pool that stays on: `devbox.py create ... --dry-run --json`,
  show it, then without `--dry-run`. Keep going while it provisions, then give them the link and their part on the
  box: open it, install or update VS Code Insiders, sign in with the same account, paste the same workshop settings,
  turn on Dev Tunnels (and keep Insiders open there), then check the laptop is listed under Dev Tunnels in **Manage
  Remote Environments...** ([optional](references/optional.md), "A dev box").
- **Research:** three things, none of them a key in the chat. The Outset API key, which they get from whoever runs
  Outset for their team and paste into `~/.copilot/research.env` themselves (you make the file from the template and
  open it for them). The Outset sign-in: you run `outset-auth.mjs` and they approve in the browser. And User
  Interviews, signed in once in the Playwright browser: in the next chat, open https://www.userinterviews.com with
  Playwright, they sign in there (password and 2FA are theirs), you confirm read only that they're in, close the page,
  and `check-setup.py remember --set userinterviews_signed_in=yes`. A User Interviews API key is optional. Missing
  access stays pending, never silently skipped or marked tested.

#### Readiness

1. `check-setup.py readiness`: it writes `Workshop readiness.md` on their Desktop (ready and tested, still to do,
   skipped, and what comes at the workshop) and prints the path. Summarize it in a few lines.
2. Tell them they can paste the same prompt again any time: it checks everything, skips what's done, and picks up new
   items.

## The practice repo

The workshop's example repo isn't part of setup: people choose at the workshop between their own work and the
example, and getting the example is a download then. `check-setup.py` reports it as `later` and leaves it out of the
done count. `practice-repo.py` and `screenshot.mjs` stay for that day.

## Resuming

"Continue my setup", a restart, the next chat, or the same prompt again: pull the clone ("Start here"), run the
check, read `steps`, `tests` and `answers` (the saved values), say in one line where you're picking up, and continue at
the first item that isn't installed or tested. Open the canvas the same way as the first time, with the saved values;
when it came from the copy, `canvas-extension.py install --json` first refreshes it if the clone changed (then
`extensions_reload`). Until the skills step installs the skills, a new chat doesn't have this skill: the next chat's
prompt names the clone's SKILL.md, and a pasted prompt clones or pulls first. A step that was `blocked` gets one retry
before you move on. Nothing done earlier is redone unless the check shows it's broken now.

## Testing this skill

- `check-setup.py` is read-only and safe on any machine (`--quick` skips the slow and network checks, including the
  dev box).
- Simulate a fresh machine with a scratch `HOME` and `COPILOT_HOME` (on Windows also `USERPROFILE`, `APPDATA` and
  `LOCALAPPDATA`, plus `WORKSHOP_SETUP_DESKTOP` for the readiness file). Remove scheduled jobs, repos and the canvas
  copy (`canvas-extension.py remove`) you create, and never test against someone's real settings, skills or
  schedules.
- On macOS, GitHub CLI keeps its token in the login keychain, which it can't find under a scratch `HOME` (it reports
  401 "Bad credentials"). Give the test `GH_TOKEN` from `gh auth token` run with the real `HOME`, inline, never
  printed.
- `devbox.py create` and `delete` make and remove real dev boxes: test them with `--dry-run`.

## Maintaining this skill

Fix wrong steps in place, keep per-OS detail in `references/machine.md` and connection detail in
`references/connections.md`, and update `references/workshop.json` and `references/workshop-settings.jsonc` when the
workshop's settings change (the check and the canvas count whatever the snippet lists). Keep the description under
1024 characters, keep the workshop's own names out of this skill (the prompt passes them in), and never use em or en
dashes.
