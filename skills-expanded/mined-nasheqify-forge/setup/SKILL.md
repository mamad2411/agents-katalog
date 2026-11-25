---
name: setup
description: >
  Set Forge up after its plugin is installed: switch Buddy on for one
  project or for every session, change that scope, name or create the
  personal-context folder, or remove Forge's settings. Use when the user
  asks to set up, switch on, switch off or remove Forge or Buddy, or
  accepts Forge's setup offer.
status: active
invocation:
  primary: user-facing
  trigger_patterns:
    - "set up Forge"
    - "switch Buddy on"
    - "remove Forge"
disable-model-invocation: false
cc_wrapper: false
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: setup

The user answers questions; you run the commands. Never ask the user to write or edit a file: every file this setup
touches is written by `forge_setup.py`. The framework root `<root>` is the directory that holds `.claude-plugin/`, two
levels above this skill's folder; take the absolute folder from the skill listing the host shows, or the one
`INSTALL.md` located. On OpenCode, the `forge:boot` skill this setup writes names `<root>` as its framework root;
when `<root>` is Claude Code's versioned plugin folder, it names Codex's stable plugin folder if Codex has the plugin,
else `<root>`, and the script then notes that the setup must be run again after a plugin update.
`S` below stands for `python3 <root>/scripts/forge_setup.py`.

## 1. Facts

Run `S status --project <project folder>` as its own call (the project folder is the session's working folder unless
the user named another). It prints JSON: the hosts found and their plugin roots (OpenCode: its CLI, the framework
root its boot skill points at, and whether that skill is in place), whether the project carries the activation line,
whether the user switch is on per host, the personal-context folder the machine setting names, the allow rules
and Forge's deny rules present. Decide from it; do not read or parse the host files yourself.

## 2. The choice

Unless the request already says it, ask one question: Buddy **in this project only** (one line in the project's
`AGENTS.md`, which teammates get when it is committed) or **in every session** (a setting in the user's home; Buddy
then also starts in folders without the line). Say what each means in one sentence. The question ends your turn:
make no setup write in it; §3 runs on the user's answer. Do not pick the scope for the user, also not the one that
changes less in their home: the choice is theirs.

For every session, also settle where personal context lives (who the user is, how they work, open topics, carried
across projects). If the status names a folder, offer to keep it. Otherwise propose `~/forge-context` and ask whether
to use an existing folder instead. A folder that does not hold `context/user/` yet is created or completed only on
the user's yes (`--create-user-repo`); the scaffold has headings only.

## 3. The writes

Run the one command that matches, as its own call; add `--dry-run` first when the user wants to see the changes:

| Request | Command |
|---|---|
| Buddy in this project | `S project --project <folder>` |
| Buddy in every session | `S every-session --user-repo <folder> [--create-user-repo]` |
| Back to this project only | `S every-session --off`, then `S project --project <folder>` if the project lacks the line |
| Buddy off in this project | `S project --project <folder> --off` |
| Remove Forge | `S remove --project <folder>` (each project the user names), then the host's uninstall commands in `<root>/INSTALL.md` §Remove (OpenCode has none: `S remove` takes its skill and line out) |

The script writes for every host whose plugin it found, and for OpenCode when `opencode` is on `PATH`: its boot skill
`forge:boot` (`${XDG_CONFIG_HOME:-~/.config}/opencode/skills/forge-boot/SKILL.md`) with `project` and
`every-session`, and for every session the activation line in `${XDG_CONFIG_HOME:-~/.config}/opencode/AGENTS.md`.
`every-session --off` takes that line out and keeps the skill (projects may still carry their line). On OpenCode
that global line is what starts Buddy in every session; the switch in the machine setting alone does not. So check
`S status` for a mismatch between `setting.switch` and `hosts.opencode.line` (for example after a run limited with
`--host`) and tell the user; `S every-session` or `S every-session --off` brings them in line. It prints what
it wrote, what was already in place and what it skipped. It is idempotent: running the same command again changes
nothing. A refusal (exit 2) names the file it would not overwrite (for example a settings file that is not valid
JSON, or an edited `forge-boot` skill); report it and ask the user how to proceed, without editing that file
yourself.

After `project`, the activation line is a change in the project's `AGENTS.md`: tell the user, and offer to commit it.

For a plugin migration, read `wrapper_migration` in the project setup result
or `project.wrapper_migration` in status. Report the listed project-relative
paths and whether each old target is reachable or missing. A reachable
wrapper can still take precedence over the plugin skill. Offer to remove
the listed files only. After the user expressly approves the paths, run
`S remove-migration-wrappers --project <folder> --wrapper <path>=<target_state>:<sha256>`
with one `--wrapper` per approved row, its values copied from that row, then run project status again; the
command refuses a file that changed since it was listed. Report the wrapper check as clear only on `clear`. On
`pending`, report the conflicts that remain. On `unavailable`, report its reason (the plugin skill list or a
wrapper location could not be checked) and that the migration status remains unresolved.

Forge uninstall uses `S remove` and the host's uninstall commands. Outside
uninstall and the approved wrapper cleanup, every file stays as it is, also one that
mentions Forge (host caches, older lines in an `AGENTS.md`, Forge checkouts, other settings): name such files to the
user if you came across them, and delete or edit one only when the user asks for that file.

## 4. The check

A setting takes effect in a fresh session; this session does not change. Check one:

- Claude Code: `claude -p "hi"` run in the project folder (every session: in a folder without the line).
- Codex: `codex exec "hi"` in the same folder (add `--skip-git-repo-check` outside a Git repository).
- OpenCode: `opencode run "hi"` in the same folder.

Pass: the reply opens with Buddy's orientation line (machine, time, folder). If the host cannot run a fresh session
from here (no login, a permission prompt), ask the user to open one and say whether the first reply opens with that
line. Report what you checked and what you could not.
