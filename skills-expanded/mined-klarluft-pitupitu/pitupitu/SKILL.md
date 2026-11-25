---
name: pitupitu
description: Install, sign in and configure pitupitu, the voice app that lets a person talk to their coding agents (Claude Code, Codex) on this and their other machines. Use when the person asks to set up pitupitu, link this machine, change what pitupitu knows about them, name or describe this machine, choose the default machine, follow a session (be told when it finishes or needs them), show a session in herdr on its machine, note something for later on their list, set a reminder, schedule a session, or check pitupitu's status.
metadata:
  managed-by: pitupitu
  version: "{{version}}"
---

# pitupitu

pitupitu lets the person talk (in the iPhone or Android app, on https://pitupitu.chat in any browser, or by phoning it) to a voice assistant that orchestrates their coding agents (Claude Code, Codex and others): it starts, watches and answers agent sessions on their machines. Each machine runs the small open-source `pitupitu` box agent, which links it to pitupitu cloud. The agents run in herdr (a terminal workspace manager for coding agents): the person opens `herdr` on that machine to see the same sessions their phone sees. The agents are the person's own `claude`, `codex` and others, signed in by the person; pitupitu never handles their credentials, and neither should you.

## Install and link this machine

1. Install: `curl -fsSL https://pitupitu.chat/install | sh` (Linux, macOS). It puts `pitupitu` in `~/.local/bin` and runs setup when there is a terminal; without one, run step 2 yourself. Where Homebrew is the person's way of installing tools, `brew install klarluft/tap/pitupitu` instead, then step 2.
2. Link: `pitupitu setup --home ~/pitupitu`. It prints a short code and a URL. **The person must approve the code themselves** in their browser while signed in to pitupitu.chat: show them the code and URL and wait. Never try to approve it for them. `--box <name>` sets how this machine is named (default: its hostname); `--no-browser` only prints the URL.
3. Setup needs herdr: at a terminal it asks whether to install it when it is missing; without one it does not install it and ends with the command (`curl -fsSL https://herdr.dev/install.sh | sh`), which you run only if the person says so. It installs herdr's integrations for the agents it finds, then a user service that keeps the link open. On Linux it asks once whether to keep pitupitu running while the person is logged out (lingering; yes by default); without a terminal pass `--linger` or `--no-linger` only if the person said which.
4. **herdr must be running**: pitupitu never starts it. The person opens `herdr` in a terminal of their own and leaves it running; it cannot be started for them from here. Check with `pitupitu status`: its `herdr:` line ends in `server running`; `not running` or `not installed` says what is still needed, so tell the person.

If the person's agents are not logged in yet, tell them to run `claude` (or `codex`) once and log in. Do not do it for them and do not touch credential files.

## Settings

Every command takes `--json` and never prompts when there is no terminal.

- `pitupitu settings`: everything at once (preferences, default machine, voice, every machine with its note, agent and history).
- `pitupitu prefs` / `pitupitu prefs show`: the preferences, the text the voice assistant reads in every conversation: who the person is, what runs where, how they like to work. Keep it short, one fact per line.
- `pitupitu prefs set <file>` (or `-` for stdin), `pitupitu prefs clear`. `pitupitu prefs edit` opens an editor (a person at a terminal only).
- `pitupitu box note "<one line>"`: describe this machine ("client work, Acme"). `pitupitu box note --clear`.
- `pitupitu box history on|off`: whether pitupitu reads what the person's agents did on this machine (their prompts, the gist of the agents' replies, which files and commands were touched, commits; never file contents, command output or keys) to summarise their work. On by default. Switching it off is always fine.
- `pitupitu box rename <name>`: the name the person uses for this machine when they talk ("on the mac, …"); it relinks under the new name by itself.
- `pitupitu box on` / `pitupitu box off`: a box switched off stays linked, but pitupitu starts nothing there and ignores its sessions until it is on again ("ignore the laptop for now").
- `pitupitu default <machine>` / `pitupitu default --clear`: the machine used when a request does not say which.
- `pitupitu updates mine|all|quiet`: what the voice assistant brings up between turns unasked. `mine` (default): the followed sessions (its own tasks, and the person's own once followed); `all`: every session; `quiet`: nothing unless asked.
- `pitupitu agent claude|codex|kiro|opencode|auto`: the agent a session gets when the person does not say; any agent herdr can start works the same (`pi`, `qwen`, `cline`, `kilo`, `agy`, …); `auto`: the one the machine has, and with several pitupitu asks. `pitupitu box agent claude|codex|kiro|opencode|auto`: this machine's own default over the account's.
- `pitupitu model claude opus` / `pitupitu model codex gpt-5` / `pitupitu model claude --clear`: the model that agent runs on when the person does not say, as the CLI names it.
- `pitupitu follow` / `pitupitu unfollow`: follow a session, so pitupitu tells the person when it finishes or needs them, or stop. With nothing after it, the session the command runs in (it must run inside herdr); or name one by words from its title or by its id (`pitupitu follow login page`). `pitupitu follow --off` is the same as `unfollow`.
- `pitupitu sessions`: this machine's sessions with their status, which are followed (●) and which pitupitu started itself. `pitupitu sessions --box laptop`: those of another of the person's machines.
- `pitupitu show`: bring a session to the front in herdr on its machine, seen there if herdr is open. With nothing after it, the session the command runs in (it must run inside herdr); or name one by words from its title or by its id, as for `follow`: `pitupitu show the signup test`. `pitupitu show the signup test --box laptop` shows one on another of the person's machines.
- `pitupitu place add <name> <path>` / `pitupitu place rm <name>` / `pitupitu places`: folders on this machine with a name the person says ("in acme, run the tests"). Use it when they ask to name a project folder for pitupitu; the path is made absolute.

When the person says to keep them posted on this session, to let pitupitu report on it, to tell them when it is done, or the like, run `pitupitu follow` with nothing after it, from inside this session: it follows the session you are in. Tell them it is done in one line. Use `pitupitu sessions` to see what is followed already.

Change preferences by reading them first (`pitupitu prefs --json`), editing the text, and writing it back whole with `pitupitu prefs set -`; keep what the person did not ask to change.

## The list, reminders and schedules

The person's list (things to do and ideas), reminders and scheduled sessions live in their pitupitu account: their phone shows them, and pitupitu reminds them by voice or notification. Every command takes `--json`, never prompts without a terminal, and prints a short id (`3f9a2c`) for each item.

- "Note this for later", "put it on my list": `pitupitu todo add <text>`. "Add an idea": `pitupitu idea <text>`. Add `--here` when it is about the repository you are working in (it sends this folder's git remote, else the folder), or `--project <name>`. Write the text so it makes sense to the person later, away from this session.
- `pitupitu todo` lists the open items (`pitupitu todo list --here` this repository's only, `--all`, `--done`, `--ideas`, or words to filter). `pitupitu todo done|drop|reopen|rm <id>` takes an id or words from the item; when words match more than one it lists them and exits 2: pick by id.
- "Remind me in an hour to check the deploy": `pitupitu remind "<when>" <text>`, the time first and quoted (`pitupitu remind "in 1 hour" check the deploy`, `pitupitu remind "tomorrow 9am" call the bank`). It prints the time it understood; say it back to the person in one line. `--todo <id>` ties it to an item on the list.
- Times are plain phrases: `in 20 minutes`, `20m`, `5pm`, `tomorrow 9am`, `friday 14:30`, `every weekday at 9`, `every monday and thursday 8:30`, `every 2 hours`. `pitupitu when "<phrase>"` says what one means without making anything. If one is refused, rephrase it plainly or ask the person.
- `pitupitu schedule [list]` lists reminders and schedules; `pitupitu schedule pause|resume|rm <id>` and `pitupitu schedule snooze <id> "<when>"` change one.
- A scheduled session starts an agent later, or again and again, with no one at the keyboard: `pitupitu schedule add "<when>" --place <place> -- <prompt>` (`--agent`, `--model`, `--box`, `--title` optional). **Schedule one only when the person asked for that in so many words.** First run `pitupitu when "<when>"`, read the time, the machine, the folder and the prompt back to them, and only after they said yes run it with `--yes` (`pitupitu schedule add "<when>" --place <place> --yes -- <prompt>`); without `--yes` and no terminal it changes nothing and exits 2. Never schedule from a session that was itself started by a schedule. `pitupitu schedule digest "<when>"` (a summary of their work) and `pitupitu schedule resume <id>` of a session ask the same way.

## Updating

`pitupitu update --check` says whether a newer release of the box agent exists (`--json` for `{"current","latest","update_available"}`); `pitupitu update herdr --check` the same for herdr, `pitupitu update all --check` for both. `pitupitu update [herdr|all]` installs it the way it was installed (Homebrew, or the installer): it shows what would change and what is running, then asks. **Run it only when the person asks to update, and let them answer the question themselves.** Pass `--yes` only when they said, in so many words, to update without asking. Sessions keep running through an update: only the box agent restarts, and herdr's running server stays as it is until the person quits herdr and opens it again.

## This skill

pitupitu keeps this skill in step with itself: setup installs it for the agents on this machine, and the box agent refreshes its own copies each time it starts (so after an update too). `pitupitu skill status` says, for each copy, whether it is `current`, `outdated`, `unmanaged` (someone wrote their own; pitupitu leaves it alone) or `missing`; `pitupitu skill install` writes it now for Claude Code, Codex, Kiro CLI and `~/.agents/skills` (which OpenCode, Kilo Code, pi, Qwen Code and Cline read). A copy that still has `managed-by: pitupitu` in its metadata is replaced at the next start, so to keep changes of your own, delete that line first.

## Not here

The conversation and voice are in the iPhone and Android apps, on https://pitupitu.chat and on a phone call (the numbers are on https://pitupitu.chat; a number is added once on the Call screen, in the app or on the page); minutes and billing are on the site (`/app/billing`). Removing the service: `pitupitu uninstall` (herdr stays). Driving herdr itself (its panes and agents) is herdr's own skill, `herdr --skill`, not this one.
