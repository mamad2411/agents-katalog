---
name: provision-server
description: Set up the server the factory runs on so that every project's development session and On-call session start by themselves and come back after a reboot. Use on "provision the server", "set up the VPS", "sessions did not come back after a reboot", "add project X to the server".
disable-model-invocation: true
---

# Skill `provision-server` — the server the projects run on

> Factory operations (control plane, not copied into a project). The mechanics are the plugin's
> `fleet.py` (below `fleet.py` means `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fleet.py"`); the skill is checks, questions and the report.
> It writes systemd units and enables lingering, so it runs only when a human calls it (`/dark-factory:provision-server`).
> It works from any directory: nothing of this repository is needed on the server, only the installed plugin.

**Platform: Linux with a systemd user instance only** (`systemctl --user` works). On macOS, or any machine without
one, nothing is provisioned — `fleet.py provision` refuses: the sessions there are attended (started by hand,
gone after a restart), and this skill does not apply.

What a provisioned server runs, per project (user systemd units, started at boot through lingering):

| Unit | What it starts | Attach |
|---|---|---|
| `df-<slug>-session.service` | the development session: `claude --name "<session name>" --remote-control "<session name>" -w dev-session` from the project's main checkout, inside its own tmux server — one interactive session with Remote Control, driven from claude.ai, working in its own git worktree `.claude/worktrees/dev-session` (created once, reused after a restart; the main checkout stays on main for the On-call and the bd store). Its name is its own from the start and survives `/clear`, so the On-call and other sessions can always address it (a session spawned by `remote-control` has a name derived from the directory, and `/clear` drops a rename). Restarted if it exits; after 5 failed starts in 30 minutes (expired login, untrusted folder) it stays failed instead of looping | `tmux -L df-<slug> attach` |
| `df-<slug>-rc.service` | the owner's new sessions: `claude remote-control --name "<session name> · new sessions" --no-create-session-in-dir --spawn worktree --capacity 3`; each session opened from claude.ai gets its own git worktree, at most 3 at a time (the CLI default is 32, each spending the shared quota). Same restart rules | `tmux -L df-<slug>.rc attach` |
| `df-<slug>-desk.service` | `scripts/feedback-desk.sh up` from the main checkout at boot — only for projects with the feedback-desk module | `tmux attach -t <DESK_TMUX>` |
| `df-<slug>-desk-watch.timer` (+ `.service`) | the same idempotent `feedback-desk.sh up` every 5 minutes: brings a crashed On-call session back (the desk unit is a oneshot and is never restarted by systemd) | — |
| `df-<slug>-stand.timer` (+ `.service`) | only for projects with `scripts/stand-update.sh`: every minute `fleet.py stand <checkout>` — on a new commit of origin's default branch it moves the main checkout there (fast-forward on `main`, or detached) and runs the script (rebuild, migrate, restart, smoke; the dev stand serves the main checkout). The sessions cannot: each works in its own worktree and Claude Code refuses git on the main checkout. A checkout with uncommitted changes or on another branch is left alone; a commit whose update failed waits for the next one; `fleet.py status` shows the outcome and the fleet watch tells the owner when it starts or stops failing. Do not give the project `--spawn same-dir`: those sessions would work in the stand's checkout | `journalctl --user -u df-<slug>-stand` |

And once per server:

| Unit | What it does |
|---|---|
| `df-notify@.service` | every unit above has `OnFailure=df-notify@%n.service`: a unit that fails (the session hit its start limit, the On-call `up` failed) sends the owner one line through `fleet.py notify` |
| `df-fleet-feed.timer` (+ `.service`), `df-fleet-serve.service` | only with `FLEET_FEED_ADDR=<private address>:<port>` in `fleet.env`: every 15 min `fleet.py feed` writes `~/.local/state/dark-factory/status.json` (per project: working now, agents, waiting for quota, On-call and watchdog, last worked — read-only, quota from the cache only), and `fleet.py serve` serves it on that address with the owner's status page at `/`, with working now, agents and quota refreshed within seconds from Claude Code's session registry and pushed to the page over `/events`; a wildcard address is refused |
| `df-fleet-codex.timer` (+ `.service`) | only with `FLEET_CODEX=on` in `fleet.env`: every 5 min from boot `codex app-server daemon start` — a no-op while Codex's app-server daemon runs; it serves the Codex sessions the owner opens from the ChatGPT app (remote control, `FLEET_CODEX_REMOTE=on` turns it on with each start). `FLEET_CODEX_DOMAINS="github.com,pypi.org,…"` is written into the user's Codex config as the agent-codex profile's network allowlist (`codex_project.py domains`); `fleet.py status` shows the Codex login, versions and quota | `journalctl --user -u df-fleet-codex`; `codex app-server daemon version` |
| `df-fleet-broker.service` | only with `FLEET_BROKER=on` in `fleet.env`: the role broker (`broker.py serve`, 127.0.0.1:8801): messages between the factory's roles (`"<slug>/<role>"`, on Claude Code or Codex) by the catalog `~/.config/dark-factory/roles.toml`. With `FLEET_BROKER_CHANNEL=on` too, a project whose `<slug>/dev` is a Claude role gets its development session started as that role with the broker's channel (a development channel, like the prod monitor's; the unit answers its start dialog only when it lists exactly `server:broker`) — the owner's opt-in, never from the project's `session.env`; `fleet.py status` shows roles held, waiting, not done, dead letters | `journalctl --user -u df-fleet-broker`; `python3 <plugin>/scripts/broker.py status` |
| `df-fleet-janitor.timer` (+ `.service`) | the janitor, daily 06:30 UTC: `fleet.py janitor` — the one nightly pass (a new nightly check joins it, no timer of its own); for every project, removes the worktrees that are clean and whose branch is merged (a dirty, locked, detached one or one a running session works in stays), deletes the local branches merged into origin's default branch that no worktree has checked out (the rule under "Worktrees pile up"), hands the project's development session once what needs a judgement — a merged worktree with uncommitted changes, an unmerged worktree or branch without commits for 14 days (squash-merged, closed, abandoned): the session shows the owner the list and removes only what the owner says yes to (`JANITOR_HANDOFF=off` in `session.env` turns this off; a session that is not running gets it the next day), then, for a project with a bd store, reviews its execution queue: `scripts/triage.py` proposes what to close or defer in a review session the owner answers in claude.ai |
| vulnerability check (no unit of its own) | Run by the janitor (row above), nightly, for every project with a lock file (uv.lock, requirements*.txt, package-lock.json, bun.lock) in the main checkout, unless `VULN_CHECK=off` in session.env: `vulns.py <checkout>` checks the lock files on origin's default branch and on the newest release tag against the OSV database and tells the owner once about each new finding, critical first, marked IN PRODUCTION when the release has it (the factory fixes from `VULN_AUTOFIX_MIN=critical` (default) or `high\|moderate\|low` up, and tells the rest; a CVE in CISA's known-exploited catalogue is always critical). A new critical finding on main opens one fix session (tmux `vulnfix` in df-<slug>.jobs, Remote Control "Security fix · <project>", own worktree): it raises the versions on a fix/ branch until the full gate is green, merges through merge-feature.sh, then waits for acceptance or, with `VULN_RELEASE=now`, asks the owner for `release.sh --security <PR>`; `VULN_FIX=off` tells only. `fleet.py status` shows the latest run, ○ while a critical one is open | `journalctl --user -u df-fleet-janitor`; `python3 vulns.py <checkout> --dry-run` |
| `df-fleet-watch.timer` (+ `.service`) | `fleet.py status --notify` every 15 minutes: one message when a project's development session, On-call, monitor or dev stand starts or stops failing — including a login or folder-trust prompt on screen; nothing while the state stays the same (state in `~/.local/state/dark-factory/fleet-watch.json`) |

Notifications, by `~/.config/dark-factory/fleet.env`: `FLEET_NOTIFY=session` puts them into the **factory session** —
a Claude session with Remote Control on this server that the owner sees in claude.ai ("Factory · <host>",
`FLEET_SESSION_NAME`); a notice arrives there as a message from another session while it runs, or opens it with the
notice as its first message. It only reads (`fleet.py status`, `systemctl --user status`, `journalctl --user`) and
names the command for the owner. Or `FLEET_NOTIFY_CMD`, a shell command that reads the message on stdin, for example a
`curl` to a Telegram bot of the owner's own (not a client group's bot: the On-call plugin is its only reader). Neither:
the journal (`journalctl --user -u 'df-notify@*' -u df-fleet-watch`).

The prod-monitor watchdog lives in cron (`prod-monitor.sh install`) and survives a reboot by itself.
Starting the On-call session from the main checkout also means its role file is the main branch's
`ROLE.md`, not a copy in some development worktree.

## Iron rules

1. **Dry-run first, then write**: `fleet.py provision --dry-run` → show the units and commands → "yes" → the real run.
2. **One owner of a project's sessions.** If a project already runs `claude remote-control` or its On-call
   session by hand (tmux), stop those after the units are up — never two development sessions or two
   On-call sessions for one project (two On-call sessions fight over the chat bot).
3. **Nothing outside the user account** without a "yes": `sudo loginctl enable-linger <user>` is only
   printed when the unprivileged call fails.

## Steps

1. **Prerequisites on the server**: Linux, `claude` logged in (the account whose subscription the sessions use),
   `tmux`, `systemctl --user` working (a user systemd instance), each project cloned and set up (`/dark-factory:add base`),
   and each checkout **trusted** — run `claude` there once by hand and accept the folder-trust question: an unattended
   `remote-control` cannot answer it (`status` then shows "waiting at a login or folder-trust prompt").
   For the On-call session: `scripts/feedback-desk.sh check` is green in the project.
   **The Bash sandbox on Ubuntu 24.04 and later**, if the project enables it (the `sandbox` block): check that a
   sandboxed command runs at all. When every command fails with `apply-seccomp: write /proc/self/setgroups … Permission
   denied`, AppArmor forbids the nested user namespace bwrap needs, in two places that act independently: the sysctl
   `kernel.apparmor_restrict_unprivileged_userns=1` and the profile `/etc/apparmor.d/bwrap-userns-restrict` (it denies
   capabilities to bwrap's children; a `local/` override does not lift it). Both are machine settings outside the user
   account (rule 3): show the owner the commands and let them run them —
   `echo 'kernel.apparmor_restrict_unprivileged_userns=0' | sudo tee /etc/sysctl.d/60-userns.conf && sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0`
   and `sudo ln -s /etc/apparmor.d/bwrap-userns-restrict /etc/apparmor.d/disable/ && sudo apparmor_parser -R /etc/apparmor.d/bwrap-userns-restrict`.
   This turns a kernel hardening off for every user of the machine; undo: remove both files, set the sysctl back to
   `1`, `sudo apparmor_parser -r /etc/apparmor.d/bwrap-userns-restrict`.
2. **Projects of this server**: `~/.config/dark-factory/projects`, one checkout path per line.
   Ask the human which projects run here; create or update the file. (Without it only a hand-filled registry
   works, one whose Repository column holds this machine's checkout paths; a factory registry holds none.)
   The project's slug is its directory name, so two checkouts with the same directory name (`/a/Gamma`, `/b/Gamma`)
   are refused with both paths named: rename one directory.
3. **Session names** (optional): `<project>/.claude/factory/session.env` with `SESSION_NAME="…"` (the development
   session's name in ListAgents, SendMessage and claude.ai; the On-call config's `DESK_DEV_SESSION` must match it),
   `RC_NAME="…"` (the owner's remote-control in claude.ai) and `SESSION_ARGS="…"` (the owner's remote-control; its
   `--permission-mode` also applies to the development session). The file is local to the server: add it to `.git/info/exclude` or commit it if the whole
   team uses the same name. `SESSION_ARGS` is an **allowlist**, because the project-local value lands in a systemd
   `ExecStart`: only `--permission-mode default|acceptEdits|plan|auto`, `--spawn same-dir|worktree|session`
   (default `worktree`), `--capacity 1..8` (default 3; not with `--spawn session`) and `--settings
   .claude/factory/<file>` (once; a relative path that stays inside `.claude/factory/` after resolving — no absolute
   path, no `..`, no symlink out). Anything else — `bypassPermissions`, `dontAsk`, any `--dangerously-*` flag, any
   other option — and `provision` refuses that project with the reason and goes on with the others. The model of the
   owner's new sessions is set by `--settings .claude/factory/session-settings.json` (base ships it with
   `{"model": "opus"}`; Claude Code 2.1.321 or later); the development session takes the account's default. After a
   change of that file run `provision` again: it restarts the project's remote-control (say so to the owner first: the
   sessions open from claude.ai end), never the development session.
4. **Where the owner hears about failures**: ask — the factory session (`FLEET_NOTIFY=session` in
   `~/.config/dark-factory/fleet.env`, no token needed) or a command of their own (`FLEET_NOTIFY_CMD`; mode 0600 if it
   holds a token; the owner writes the token, not the agent). Test it:
   `fleet.py notify test.service` — one line arrives.
5. **Status** (optional): ask whether the owner wants the factory at a glance on their phone. On "yes": the
   server's address on a private network the phone is on too (Tailscale: `tailscale ip -4`), a free port →
   `FLEET_FEED_ADDR=<address>:<port>` in `fleet.env`. Never a public address: the private network is the boundary.
   After provisioning, `curl http://<address>:<port>/status.json` from another machine on that network answers.
   To read the feed from outside that network (a phone without the VPN on), first
   `FLEET_FEED_TOKEN=<token>` in `fleet.env` (`python3 -c 'import secrets; print(secrets.token_urlsafe(32))'`, at least
   32 characters): every request must then carry `Authorization: Bearer <token>`, from the private network too. Then a
   tunnel to the address — SEAM, Tailscale Funnel on the reference setup: the tailnet's policy allows `funnel` for
   the node, then `tailscale funnel --bg --https=8443 http://<address>:<port>` (a port of its own leaves anything
   already served on 443 alone). Check from outside: without the header 401, with it the JSON.
   **Phone page**: with `FLEET_FEED_PAGE=on` in `fleet.env` (then `systemctl --user restart df-fleet-serve`) the same
   address serves the status as a web app at `/`, added to the phone's Home Screen; without it `/` answers like any
   other path. A phone installs it only from https: inside the tailnet
   `tailscale serve --bg --https=8444 http://<address>:<port>`, then `https://<host>.<tailnet>.ts.net:8444/` on a
   phone with Tailscale on (the Funnel address above works from anywhere). With `FLEET_FEED_TOKEN` the page asks for
   the token once (gear) or takes it from a link ending in `#token=<token>`; the page itself needs none.
6a. **Codex** (optional): ask whether Codex CLI should work on this server too. On "yes", the owner first: installs Codex CLI and logs in (`codex login`), installs the plugin in Codex (`codex plugin marketplace add <the canon>`, `codex plugin add dark-factory@dark-factory`). Then `FLEET_CODEX=on` in `fleet.env`, `FLEET_CODEX_REMOTE=on` when the owner wants to work from the phone, and `FLEET_CODEX_DOMAINS` with the domains the work needs (the code host, package registries) — the network stays open to every domain without it. After provisioning: `codex remote-control pair` prints a short-lived code the owner enters in the ChatGPT app (Codex → this host). Each project Codex works in gets `/dark-factory:add agent-codex`.
5b. **Role broker** (optional): ask whether the project's sessions should exchange messages (the development session, the On-call, a session the owner opens on a laptop). On "yes": `FLEET_BROKER=on` in `fleet.env`; the roles in `~/.config/dark-factory/roles.toml` (`[roles."<slug>/dev"]` with `agent = "claude"` or `"codex"` and `accepts_from = [...]`; the broker's docstring shows the format); `FLEET_BROKER_ADDR=<private address>:<port>` only when a session of another machine will join (never a public address: the broker refuses it). `FLEET_BROKER_CHANNEL=on` pushes messages into the development session. After provisioning, `python3 <plugin>/scripts/broker.py status` answers, and a running session takes a role with `/dark-factory:join "<title>"` (for another machine the owner first gives it the project's token, `broker.py join-token <slug>`: the join skill's step 1).
6. `fleet.py provision --dry-run` → show → "yes" → `fleet.py provision`.
7. **Stop the hand-started copies** (rule 2), then check: `fleet.py status` — every development session
   and On-call session ●. Open claude.ai: the sessions are listed under their names.
8. **Reboot test** when the human agrees: `sudo reboot`, then `fleet.py status` again.

Remove a project: delete its line, `fleet.py unprovision --project <slug>` (the directory name, lower-case; it finds
the units even though the line is gone). A project whose `session.env` cannot be parsed (an unbalanced quote) is
reported as a settings error and skipped; the others go on.
Stop the On-call session on purpose: `systemctl --user stop df-<slug>-desk-watch.timer df-<slug>-desk` — with only
`feedback-desk.sh down` the watch timer starts it again within 5 minutes.

**Worktrees and branches pile up**: every claude.ai session gets a worktree and a branch; the janitor removes the merged ones every day. `fleet.py status` lists a project's
stale worktrees (clean with the branch merged into origin's default branch, or no commit for 14 days —
`--stale-days N`). `fleet.py gc` shows what would go; `fleet.py gc --apply` (the janitor's first step) removes only
clean worktrees whose branch is merged, never a dirty, locked, detached one or one a running process has as its
working directory, then deletes the merged local branches no worktree has checked out (`main`, `master`, `release`,
`dev`, `develop` stay). Merged means an ancestor of the remote-tracking default branch — fetch first; a project that
squash-merges never has merged branches by that test, so its worktrees and branches are only reported, removed by hand.

**A new release** (after `scripts/release.sh v<N>` in the canon): `fleet.py upgrade v<N> --dry-run`, then without
`--dry-run`. It moves the owner's pin and the marketplace to the tag, puts each project's main checkout on origin's
default branch and updates its plugin, re-runs `provision` from the new plugin and restarts `df-fleet-serve` and, when present, `df-fleet-broker`. A
project that still pins an older release is named: its `/dark-factory:upgrade` PR first. The sessions and On-calls are
restarted only on the owner's "y" (it ends them); without a terminal it prints the command instead.

## Known limits

- The units call `fleet.py` through the symlink `~/.local/share/dark-factory/plugin` (`provision` creates it), so they
  survive `/plugin update`: the plugin's SessionStart hook repoints the link to the new version when a session
  starts (it never creates the link). Until the first session after an update the old version keeps serving. `fleet.py
  status` flags a missing or foreign link.
- The On-call login expires every few days when it uses an interactive login; `status` shows "asks to log in" and the
  fleet watch tells the owner. Attach and run `/login`. The login and folder-trust detection reads the last lines of
  the tmux screen — a best-effort hint that can miss a reworded prompt, not a check.
- The fleet watch reports changes, not states: a problem that was already there at the first run is reported once,
  then not again until it is fixed and comes back.
- A development session that hit the start limit stays `failed`: fix the cause (`journalctl --user -u
  df-<slug>-session`), then `systemctl --user reset-failed df-<slug>-session && systemctl --user start df-<slug>-session`.
- A dead server is not detected from the server itself; watch it from outside (an uptime check on the
  production health endpoint, see the observability module).
