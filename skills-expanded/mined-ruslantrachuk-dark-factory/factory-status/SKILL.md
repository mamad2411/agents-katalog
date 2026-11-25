---
name: factory-status
description: One read-only status of every project on this server — development session, On-call session and its login, production monitor watchdog, subscription quota, ready queue, lag behind the template. Use on "status", "factory status", "how are the projects", "is the monitor alive", "what is in the queue".
---

# Skill `factory-status` — how every project is doing

> Factory operations (control plane). The mechanics are the plugin's `scripts/fleet.py status`;
> the projects are those of this server (`~/.config/dark-factory/projects`, see `/dark-factory:provision-server`).
> Session checks assume a Linux server provisioned with systemd user units; on macOS (attended sessions) the
> development session reads "not provisioned" by design.

Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fleet.py" status` (add `--project <name>` for one project) and answer with its output as one
message, no preamble:

```
Factory status · <time UTC>

● subscription quota — <5h and 7d, reset times>
● Codex — daemon running <version>, CLI <version>                  (only with FLEET_CODEX=on)
● Codex quota — <the plan's windows, reset times>                   (only with FLEET_CODEX=on)
● role broker — <N>/<M> roles held, <W> waiting, <H> handed over not done, <D> dead   (only with FLEET_BROKER=on)
● feed — written <time>, served on <address>               (only with FLEET_FEED_ADDR)

<project>
  ● plugin — installed and enabled
  ● Codex hooks — <N> hooks approved                            (only a project with the agent-codex module on a Codex server)
  ● development session — active — "<name>"
  ● new sessions — active — "<name> · new sessions"
  ● On-call — running
  ● prod monitor — watchdog and channel fine
  ● dev stand — updated to <sha> (origin/main) · <time>        (only with scripts/stand-update.sh)
  ● queue — ready: <N>
  ○ template — template v1, the plugin is at v2 (/dark-factory:upgrade)
  ○ worktrees — <N>; <M> clean and merged (fleet.py gc --project <slug>)
```

● is fine, ○ needs attention; a check that does not apply to the project (no module) is not shown.
Under the block, for each ○ one line with the next action:

| ○ | Next action |
|---|---|
| plugin not installed / not enabled — guard and quota guard off | urgent, tell the owner first: `claude plugin install dark-factory@dark-factory --scope project` in the project's main checkout (or restore the `enabledPlugins` entry), then restart its sessions and On-call |
| development session not provisioned / inactive | `/dark-factory:provision-server`; `journalctl --user -u df-<slug>-session` |
| development session failed (start limit) | fix the cause from the journal, then `systemctl --user reset-failed df-<slug>-session && systemctl --user start df-<slug>-session` |
| development session waiting at a login or folder-trust prompt | `tmux -L df-<slug> attach` and answer it (`/login`, or trust the folder) |
| new sessions not active / failed / at a prompt | the same as the development session, with `df-<slug>-rc` and `tmux -L df-<slug>.rc attach` |
| On-call not running | `scripts/feedback-desk.sh up` in the project (or `systemctl --user restart df-<slug>-desk`) |
| On-call asks to log in | attach to its tmux session and run `/login` (the screen check is a best-effort hint) |
| prod monitor ✗ / watchdog silent | `scripts/ops/prod_monitor/prod-monitor.sh status` in the project |
| dev stand: update failed | `journalctl --user -u df-<slug>-stand` shows the script's run; the fix goes to main as a new commit, which the stand tries next (or, after a fix outside git, `fleet.py stand <checkout> --retry`) |
| dev stand: uncommitted changes / on branch X | someone works in the stand's checkout (a session with `--spawn same-dir`, a hand edit): tell the owner; the updater does not touch it until it is clean and on main or detached |
| dev stand: not provisioned | `/dark-factory:provision-server` |
| feed: not written yet / not written for N min (the status page shows "no data") | `journalctl --user -u df-fleet-feed`; `systemctl --user status df-fleet-serve` |
| quota ≥ 80% | new work is stopped by the quota guard until the reset shown |
| Codex not installed / not logged in / daemon not running | the owner: install Codex CLI or `codex login` on this server; `journalctl --user -u df-fleet-codex` |
| Codex quota ≥ 80% or "no new work" | the quota guard stops new work in Codex sessions until the reset shown; Claude sessions are not affected |
| role broker not answering / dead letters | `journalctl --user -u df-fleet-broker`; `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/broker.py" status` names the roles with waiting, not-done and dead messages: tell the owner, a dead letter is a message nobody handled |
| Codex hooks not approved | urgent, tell the owner first: Codex skips unapproved hooks silently, so the guard is off in that project's Codex sessions; the owner runs the `codex_project.py setup --project <path>` command the line prints |
| template behind | `/dark-factory:upgrade` in the project: Copier on a work branch plus the release notes' "How to upgrade" steps; a project on a canon commit SHA syncs once with `scripts/harness-diff.sh` |
| worktrees: clean and merged | `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fleet.py" gc --project <slug>` (dry run), then `--apply` after the human's yes |
| worktrees: on other rules than main | a session there reads the old rules from its branch (no plugin at all if the branch predates the canon): tell the owner to start a new session instead of continuing that conversation, or merge main into the branch; a clean merged one goes with `gc` |
| worktrees: no commits for N days | ask the human — abandoned work or a long branch; nothing removes those automatically |

Read-only: restart, edit, remove or claim nothing — do not run `gc --apply` or `status --notify` from this skill (the
fleet watch timer runs `--notify` and keeps its own state).
