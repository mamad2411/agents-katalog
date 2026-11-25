---
name: create-skill-devops
description: >
  Scaffold a project-scoped /devops skill in the current project — a
  command-based toolbox for setting up and verifying that project's build
  environments. Use when the user says "/create-skill-devops", "give this
  project a devops skill", or wants to add environment-setup commands (e.g.
  iphone-setup, docker-setup, node-setup) to a project. Generic: interviews
  for what the project needs, then generates .claude/skills/devops/ from the
  templates, following the audit → plan → install → verify discipline.
---

# create-skill-devops

Creates a **project** skill at `<project>/.claude/skills/devops/` that gives
the project a `/devops` command toolbox for build-environment setup. This
meta-skill encodes the intent and discipline; the templates make it concrete.

Invoke with an optional command name — e.g. `iphone-setup`, `docker-setup`,
`node-setup` — naming the environment to scaffold. Omit it and the skill
interviews for what the project needs.

## The intent

Every project has environment prerequisites (SDKs, toolchains, runtimes,
services) that are easy to forget between machines and months. A project
devops skill makes them:

- **Discoverable** — `/devops` lists commands; the `argument-hint` shows the
  typeable options right in the slash-command autocomplete menu.
- **Reproducible** — the setup procedure lives in the repo, travels with git,
  and works on a fresh machine.
- **Safe** — nothing installs before an audit and a plan are shown; every
  step is idempotent; interactive steps (sudo, account logins) are handed to
  the user as `!`-prefixed commands, never scripted around.
- **Provable** — setup ends with a real verification (a build, a boot, a
  version check chain), not an assumption.
- **Observable** — a built-in `status` command reports the current state of
  everything the skill manages, any time, without changing anything.

## The discipline every generated command follows

1. **Audit first** — a read-only check script prints `KEY | STATUS | DETAIL`
   rows and always exits 0. Running it changes nothing, any time.
2. **Plan** — list only what the audit flagged, in dependency order, with
   download sizes, disk needs, and which steps are interactive. Get
   confirmation before large downloads.
3. **Install** — run non-interactive steps directly (long ones in the
   background). Interactive steps (sudo password, Apple ID, cloud logins) are
   given to the user as `! <command>` to run in-session. Idempotent: re-running
   on a healthy environment reports "already set up" and changes nothing.
4. **Verify** — re-run the audit, then prove the environment end-to-end with
   the most real check available (build the actual project if one exists).
   Report plainly what was proven and what wasn't.

## The optional lifecycle command set (build / up / down / remove)

Projects with multiple runnable units often want four standard actions per
unit rather than one bespoke command per service. This is backend-agnostic:
the unit can be a **Docker Compose service** (image + container) just as
easily as a **native background process** (a built binary/venv + a running
PID, managed by something like `scripts/dev.sh start|stop|status` with
PID-file bookkeeping instead of a container runtime) — same four verbs,
same audit/plan/execute/verify shape, different underlying commands. Offer
this set whenever the project has more than one buildable/runnable
"solution", regardless of backend (e.g. a `docker-compose.yml` with 2+
services, or 2+ native processes started/stopped via PID files):

- **`build <solution|all>`** — produce the build artifact (image, or a
  compiled binary / venv), start nothing.
- **`up <solution|all>`** — build if needed, start, then prove it's actually
  serving (curl/log/PID check), not just that a container or process
  technically exists.
- **`down <solution|all>`** — stop the running unit (container, or kill the
  PID), keep the build artifact. Cheaply reversible — `up` again should be
  fast.
- **`remove <solution|all>`** — delete the build artifact too (image, or the
  venv/downloaded binary). **Destructive.** Always show what will be
  deleted and its re-acquire cost (fast local rebuild vs. a real
  re-download) and get explicit confirmation before running — same rule as
  any hard-to-reverse action. **If any solution persists real data outside
  the build artifact** (a Docker bind-mounted data volume, or — for a
  native process — a data directory / DB file on disk that a plain
  `down`+`remove` wouldn't touch), `remove` must **ask explicitly, every
  run**, whether to also delete that data, and wait for a yes/no before
  touching it — never delete it silently, and never assume removing the
  build artifact reset it (that data survives a plain `remove` and comes
  back untouched on the next `up`/`build`). Offer a `--purge-data`-style
  flag to skip the ask and go straight to "yes" for scripting/directness,
  but the flag is an opt-in shortcut to the same confirmed action, not a
  way to avoid the plan/confirm step.

A **"solution"** is whatever unit the project defines as independently
buildable/runnable — one row per Compose service, or one row per
native process the dev script manages — though units that are always
operated together (e.g. a tunnel pair bound by `depends_on`, or a bridge
process + app process always started/stopped as a pair) can be grouped
into one named solution.

These four commands share state, so they share ONE audit script
(`scripts/<name>-check.sh`, e.g. `compose-check.sh` for a Docker backend or
`native-check.sh` for a PID-file backend) rather than one each — it reports
build+running status per solution and is Phase 1 for all four. `status`'s
discovery still globs `scripts/*-check.sh`; when several routing-table
commands point at the same script, group them under one section in the
status report instead of repeating the same table four times.

Scaffold from `templates/lifecycle.template.md` (one reference doc covering
all four actions) and `templates/lifecycle-check.template.sh` (the shared
audit — has commented pattern blocks for both a Docker Compose backend and
a native PID-file backend; use whichever matches the project, or both if it
has solutions of both kinds). Still follows audit → plan → execute →
verify, just lighter than environment setup: audit = current build/run
state, plan = what will happen, execute = the actual compose command or
`dev.sh`-style invocation, verify = re-audit plus a real traffic/log check
for `up`.

If the project already has its own lifecycle script (a `scripts/dev.sh` or
equivalent that starts/stops native processes), don't duplicate its logic —
the `/devops` commands should thinly wrap it (call `scripts/dev.sh build`,
`up`, `down`, etc.) and add only what it's missing, most often `remove`
(deleting build artifacts is rarely a verb an app's own dev script needs,
so this is usually genuinely new, implemented directly in the reference doc
as `rm -rf`/`rm -f` steps against the same paths `build` created).

## The standard `status` command

Every generated devops skill includes a `status` command, created at scaffold
time alongside the first real command. It is what makes the toolbox
observable, and it is generic by construction:

- **Discovers** every audit script in the skill's `scripts/` directory
  (`scripts/*-check.sh` → one entry per command), so commands added later are
  reported automatically with zero changes to `status`.
- **Runs** each audit (all read-only, all exit 0) and reports per command: a
  verdict — **ready** (all build-relevant rows `ok`), **partial**, or **not
  set up** — the non-`ok` rows, and the exact `/devops <command>` to fix it.
- **Adds live extras** where cheap and read-only (running services, booted
  simulators/containers, in-flight background downloads).
- **Never installs, fixes, or changes anything.**
- Bare `/devops` routes to `status`, and `status` appears in the
  `argument-hint`.

Scaffold it from `templates/status.template.md`.

## Procedure

### 1. Check for an existing skill

If `<project>/.claude/skills/devops/` already exists, switch to **add-command
mode**: add the new command to the existing skill (routing-table row, section
in SKILL.md, `references/<command>.md`, optional `scripts/<command>-check.sh`,
and update the `argument-hint`). Never overwrite existing commands.

### 2. Interview (only what's not obvious)

Determine, from the argument, the project contents, and if needed 1-2 short
questions:

- What environment(s) does this project need? (e.g. iOS/Xcode, Docker,
  Node/pnpm, Python/uv, a database)
- What is the command name and its aliases? (kebab-case, e.g. `iphone-setup`
  with aliases `ios`, `iphone`)
- What does "verified working" mean for this project? (the smoke test)
- Does the project have 2+ runnable units — whether Docker Compose services
  or native background processes managed by a dev script (PID files,
  `nohup`, etc.)? If so, offer the `build`/`up`/`down`/`remove` lifecycle
  set (see above) — name the actual solutions and confirm the grouping
  (e.g. does a bridge process + app process always started together count
  as one solution or two) before scaffolding. If a native dev script
  already exists, plan to wrap it rather than reimplement its start/stop
  logic.
- If offering the lifecycle set: does any solution persist real data outside
  its build artifact — a Docker bind-mounted data volume (check the compose
  file's `volumes:` for a host-path source, `./something:/container/path`,
  not a bare named volume), or, for a native process, a data directory/DB
  file on disk the build artifact doesn't include? If yes, record the
  path(s) per solution — `remove`'s template needs them to ask about
  deleting that data, every run.

### 3. Scaffold from templates

Copy and fill the templates in this skill's `templates/` directory:

| Template | Becomes | Fill in |
|---|---|---|
| `SKILL.template.md` | `.claude/skills/devops/SKILL.md` | project name, command rows, argument-hint |
| `reference.template.md` | `.claude/skills/devops/references/<command>.md` | audit keys, plan table, install steps, smoke test |
| `check.template.sh` | `.claude/skills/devops/scripts/<command>-check.sh` | one check block per prerequisite |
| `status.template.md` | `.claude/skills/devops/references/status.md` | usually verbatim — it is fully generic |
| `lifecycle.template.md` | `.claude/skills/devops/references/lifecycle.md` (one file covering all four `build`/`up`/`down`/`remove` actions) | naming the project's actual solutions/services and backend (Docker Compose, native PID-file processes, or mixed) |
| `lifecycle-check.template.sh` | `.claude/skills/devops/scripts/<name>-check.sh` (e.g. `compose-check.sh` or `native-check.sh`) | one built+running check block per solution, using whichever commented pattern (Docker or native) matches — only when the project has 2+ runnable units |

Rules that must survive templating:

- `argument-hint` lists every command word and alias, pipe-separated in
  square brackets — and is updated every time a command is added.
- Scripts are referenced relative to the skill's base directory (announced at
  invocation), never by absolute path — project skills must survive cloning.
- The check script starts with `setopt null_glob` (zsh) and always exits 0.
- Research real download sizes / disk requirements for the plan table —
  don't invent numbers; mark unknown ones "verify at install time".

### 4. Test and hand off

- Run the generated check script; fix any script errors now.
- Show the user the audit output and the generated file tree.
- Remind them: `/reload-skills` to pick it up, and if the project isn't a git
  repo yet, the skill won't travel until it is.
