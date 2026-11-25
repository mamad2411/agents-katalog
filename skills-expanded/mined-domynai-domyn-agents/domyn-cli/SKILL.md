---
name: domyn-cli
version: 2.0.0
description: >-
  How to act on the user's own domyn setup: where its files live, how to change the
  config or add a skill safely, when a change takes effect, and fixing common
  problems. For how a command, option or feature works, use domyn-docs.
tags: [domyn, cli, configuration, skills, help]
---

# Working on the user's domyn setup

You are running inside the domyn CLI, so questions about "the CLI", "this tool",
"my config" or "my skills" are about the environment you are running in. This skill
says where everything lives, how to change it, and **when a change takes effect**.
Most changes reach the next message; a few need a restart. Getting that wrong leaves
the user thinking a change failed when it was simply never loaded.

What a command, slash command, option or setting does, and how to build agents, is in
the documentation: the `domyn-docs` skill. Read the page there rather than answering
from memory.

## First: are your tools running in a Docker container?

Run `echo "$DOMYN_BACKEND"` once, before anything else. **`docker` means every tool you
have (`run_command`, the file tools and the browser) runs in a Docker container on the
user's machine, not on the machine itself.** Empty means they run on the user's machine
and nothing in this section applies. The container exists so that a dangerous command
breaks it and not the user's computer, and that has a price you must not forget:

| | on the user's machine | in the Docker container |
|---|---|---|
| `config.yaml` | you may edit it; it reloads at the next message | **read only. Do not try to edit it and do not look for a way around.** Give the user the exact change and ask them to make it, or to run `domyn setup` or `/model`. The config names code the user's machine runs and which backend to use, which is why a container may not write it |
| credentials, approvals, history | on disk (never print credentials) | **not there**: you cannot read them |
| files outside the project (`~/Downloads`, `~/.ssh`, another repository) | reachable by `run_command` | **do not exist**, unless the workspace is the user's home folder, which then is all there (only `~/.domyn` is hidden). Otherwise only the workspace, the skill folders and the session's state are the user's files. When the user names a file elsewhere, ask them to copy it into the workspace |
| paths the user writes (`~/project/a.md`, `/Users/them/project/a.md`) | mean what they mean on the machine | **the same, for `run_command` and the file tools**: `~` is the user's home path and the workspace is at its real path, so use the path as the user gave it, if it is under the workspace. Not under it: not found, as above. Do not rewrite it to `/tmp/...` or ask for another spelling |
| `.git/hooks`, `.git/config` | writable | **read only**: a hook runs on the user's machine at their next `git commit` |
| `domyn ...` commands | on `PATH`, they change the user's setup | on `PATH` (the same release), but **they change nothing of the user's**: `$DOMYN_PROJECT_DIR` there is an empty scratch folder of this conversation, with the real `config.yaml` read-only over it. A `domyn run` keeps a history of its own and sees no credentials, so it needs a key from a `.env` in the workspace or from `allowed_env`; `domyn setup` and the like are not what the user asked for. For a change to the user's setup, tell the user which command to type |
| programs and servers on the user's machine (a dev server on `localhost`, installed tools) | reachable | **not reachable**: `localhost` is the container, and private addresses are refused |
| your skills, `SOUL.md` / `AGENTS.md`, `.agents`, `.domyn` in the project | writable | writable (they are mounted, as on the user's machine) |
| file tools | confined to the workspace and the skill folders | reach the whole container, `/tmp` included; the user's files are only what is mounted |
| installing packages | a virtualenv per conversation | `pip` and `npm install -g` work and come back after a restart; no root, so no `apt` |
| background commands | outlive the session | stop with the session |
| network | whatever the machine has | `allowed_network`: public HTTPS sites by default, or a list, or none |
| environment variables | a fixed safe set plus `allowed_env` | the same |

When something fails in the container and works on the user's machine, this table is
the first place to look. Say which difference you hit instead of retrying.

Ground rules:

- **You cannot run slash commands.** `/config`, `/model`, `/clear` and the rest are
  typed by the user at the prompt. When one of them is the answer, tell the user
  which one to type.
- **Check before you answer.** When a shell is available, `domyn --help` and
  `domyn <command> --help` describe the installed version.
- **Never show a secret.** Do not print `~/.domyn/credentials` or `.env`, and do not
  write an API key into `config.yaml`. See *Reading and changing the config*.

## Where things live

Everything is under `~/.domyn/` (the *home* directory), unless the session runs a
**project** (`domyn run --project <name|path>`): then the project's folder takes the
place of `~/.domyn/` entirely — see *Which configuration this session runs* below. A
`./.domyn/` in the directory the CLI is started from can hold skills and instructions
(autodiscovery, when setup turned it on), but a `config.yaml` there is never read.

| path | what it is |
|---|---|
| `~/.domyn/config.yaml` | provider, model, default agent, tools, compaction. A `./.domyn/config.yaml` in the directory the CLI was started from is **not** read: a folder's own configuration is a project (`--project`) or a file passed to `domyn run` |
| `~/.domyn/credentials` | API keys as `NAME=value`, permissions 0600. Written by `domyn setup` |
| `~/.domyn/builtin-skills/` | the built-in skills chosen in `domyn setup`, copied from the package. **`domyn setup` deletes and rewrites this directory every time**, so nothing of the user's own belongs here. It is not scanned: `config.yaml` lists each skill in it by absolute path |
| `SOUL.md`, `AGENTS.md` (or `AGENT.md`) | standing instructions: identity, tone and preferences (`SOUL.md`, follows the user), what the agent is working on (`AGENTS.md`, follows the task). Read from the paths under `standing_instructions.source.paths` in `config.yaml`: the files `domyn setup` was pointed at, plus `./.domyn` and `./.agents` (subfolders included) when the user turned that on. **`~/.domyn/SOUL.md` and `~/.domyn/AGENTS.md` are not read** unless setup was given their path, and neither are the ones at a project's top. `/config` lists the files in use |
| `~/.domyn/approvals.yaml` | tool approvals the user granted with "always" |
| `~/.domyn/state.yaml` | settings remembered between sessions (`verbose`, `auto_approve`), written by `/verbose`, `/auto`, Shift+Tab and `-v`. A project has its own in its folder. Never exported. Do not edit it to turn auto-approve on for the user: tell them to use `/auto` |
| `~/.domyn/projects/<folder>-<hash>/approvals.yaml` | approvals for this project only, one file per directory the CLI starts in. `./.domyn/approvals.yaml` is not read. Not used when the CLI is started from the home directory itself |
| `conversations.db` (next to the config) | saved conversations, used by `--resume` and `/resume` |
| `conversations/<id>/` (next to `conversations.db`) | per-conversation virtualenv (`venv/`, when `isolate_environment` is on) and `output/`, in the project's folder or `~/.domyn`, never in the working directory. Beside it, `processes/<id>/` holds the logs of background commands and `browser/` the browser's saved pages. None of the three is exported or imported. `domyn clean --older-than <days>` (or `--all`, `--dry-run`, `--project`) deletes old conversations with their `conversations/<id>/` folders; it leaves `processes/` and `browser/` alone. `--memory` (alone, or with `--conversations`) removes entries of that folder's own `memory.md` by the date each was written, with the same `--older-than`/`--all`: `--memory --older-than 90` leaves the conversations alone |
| the `memory_manager`'s `file_path` and `read_only_sources` in the config | the long-term memory, when on: `file_path` is the file the agent learns into, `read_only_sources` the files it only reads and never changes. The global memory is `~/.domyn/memory.md`, shared by every configuration that uses it; a project's own is `memory.md` in the project's folder. A project can read one or both, and learns into one. Markdown, one bullet per fact; `/memory` lists and changes the file learned into, and marks the entries only read `(read only)` |
| `.env` (working directory or a parent) | loaded at startup. Variables already set in the shell take precedence |
| `~/.domyn/projects/<name>/` (or any folder given by path) | a project: its own `config.yaml`, `skills/`, `credentials` (a key it does not set is read from `~/.domyn/credentials`), approvals and `conversations.db`, laid out like `~/.domyn/`, and the instruction files its config lists. Created by `domyn setup --project <name>` or `domyn export` |

### Which configuration this session runs

**Find this out before reading or changing anything** — the config, a skill, an
instruction file — and before running any `domyn` command. Each project has its own
files, and changing the wrong ones looks like it worked while the session never sees
it.

1. Run `echo "$DOMYN_PROJECT_DIR"` in the shell. It names the folder this session
   uses as its home: its config is `$DOMYN_PROJECT_DIR/config.yaml`, its skills folder
   `$DOMYN_PROJECT_DIR/skills/`, its instructions the files that config lists, whatever
   folder the CLI was started in (a `./.domyn/config.yaml` there is not read).
   - **`~/.domyn`** (the home folder's `.domyn`): no project, the global configuration.
   - **Any other folder**: the session runs the project in that folder. **Nothing in
     `~/.domyn/` is used**: do not read or edit the files there for this session.
   - **Empty**: the session was not started by the `domyn` CLI; ask the user which
     configuration it runs.
2. A session can also run a config file named on the command line
   (`domyn run my.yaml`), which only `/config` shows. When unsure, or when there is no
   shell, ask the user to type `/config`: it prints the file in use and a summary
   with secrets removed.
3. **Every `domyn` command you run in the shell takes
   `--project "$DOMYN_PROJECT_DIR"`** (`domyn skill remove`, `domyn skills`,
   `domyn export`, …). Without it the command reads and changes `~/.domyn/`, which in a
   project is not this session's configuration, and reports success. With
   `~/.domyn` it is the global configuration, as without the option.

**What your file tools can reach.** The built-in file tools only work inside the
workspace (by default the directory the CLI was started in) plus the skill
directories known when the session started (only when the agent comes from a YAML
config, the default one included; a `.py` agent gets no skill directories). `~/.domyn/config.yaml`,
the user's own `SOUL.md` / `AGENTS.md` (the paths saved by `domyn setup`) and the
session's state beside the config (background commands' logs, a conversation's
`output/`) are normally **outside** it, so `read_file` and `write_file` will refuse
them; read a log with `check_command`, or `tail`/`grep` through `run_command`. The ones in
`./.domyn` and `./.agents` are inside it. To work on them, use `run_command`
(`cat ~/.domyn/config.yaml`, a small Python edit, …). It asks the user for approval
first. If no shell tool is available, give the user the exact change to make by
hand.

## When changes take effect

| what changed | takes effect | how |
|---|---|---|
| `config.yaml` edited (by hand, by you **when your tools run on the user's machine**, or by `domyn setup` in another shell) | **next message** | the file is compared with what the agent was built from before every message, and the agent is rebuilt when it changed: model, tools, skills, instructions, MCP servers, anything. The session prints "Reloaded …". A file that no longer loads keeps the previous configuration, and the session says why once |
| provider / model / key, through `/model` | immediately | `/model` rewrites the file and reloads the agent |
| a skill file **edited** in a folder the config already lists | **next message** | listed skills are read again on every turn. Suggest `/clear` if the old version was already read into this conversation |
| a **new** skill added to `./.domyn/skills` or `./.agents/skills` | **next message** with autodiscovery on (`.domyn/skills` and `.agents/skills` in the paths); otherwise once it is listed in `config.yaml` | see *Adding a skill* |
| a new `skills.source.paths` entry | **next message** | it is part of `config.yaml` |
| `SOUL.md` / `AGENTS.md` edited, created or deleted in a directory the session reads them from | **next message** | they are read again on every turn, nothing to reload. `/config` shows what is loaded right now |
| `standing_instructions.source.paths` in `config.yaml` | **next message** | it is part of `config.yaml` |
| `credentials`, `.env`, exported env vars | **next start only** | read once, at startup (`/model` is the exception: a key typed there is used right away) |
| approvals | right away | managed with `/approvals` |
| `state.yaml` edited by hand | **next start only** | read once, at startup; `/verbose` and `/auto` write it |

When you tell the user a change is done, also say when it takes effect, e.g.
"Saved. It is used from your next message."
`/clear` only starts a new conversation with the same agent. Suggest it when the
model and config are fine but the conversation history is out of date. It is not
needed to pick up an edited skill, `SOUL.md` or `AGENTS.md`: those already reach the
next message.

## Adding a skill

A skill is a markdown file with YAML frontmatter. **A skill is loaded only when
something names it**: the agent's `skills.source.paths` in `config.yaml`. **Both are
read again before every message**: `config.yaml` itself
(when it changed, the agent is rebuilt from it, so a path added during a session is
in use from the next message, no restart), and the skill files inside the listed
paths (so a new or edited skill in a listed folder is too). `/skills` and `/skill`
read them the same way when used.

Two entries are special: **`.domyn/skills`** and **`.agents/skills`** in the paths are
*autodiscovery*, turned on by `domyn setup` — "load `./.domyn/skills` (domyn's folder)
and `./.agents/skills` (the folder other agent tools share) of the folder `domyn run`
is started in". Being listed folders, a skill created in either loads from the next
turn, with no change to the config. If both hold a skill with the same name,
`./.domyn/skills` wins. The user can turn both on or off inside a session with
`/skills-autodiscover on|off` (bare `/skills-autodiscover` shows the current state), which writes
the same entries setup does and applies from the next message.

```
<folder>/<name>/SKILL.md          # preferred: room for scripts and references beside it
<folder>/<group>/<name>/SKILL.md  # a group folder: every skill under it is loaded
<folder>/<name>.md                # flat form, also accepted
```

Neither autodiscovery folder, nor a folder on the way to it, may be a symbolic link:
a link is not followed, and `domyn run` names it at startup.

Steps:

1. **Check what exists, and where new skills go.** Ask the user to type `/skills`
   to see the current skills and their paths (`domyn skills` in a shell shows the
   same), and `/config`: its `config` row is the configuration file of this session,
   its `skills` row the listed paths. Reusing a name **overrides** or is overridden
   by the existing skill (see precedence below); do it on purpose or not at all.
   Then decide where the new skill goes:

   - **Autodiscovery is on** (the `skills` row lists `.domyn/skills` and
     `.agents/skills`): create it in **`./.domyn/skills/<name>/`**, relative to the
     folder the CLI was started in. Nothing else to do: it is loaded from the next
     message.
   - **Autodiscovery is off**: create it in the **`skills/` folder of the
     configuration's own folder** (see *Which configuration this session runs*):
     `$DOMYN_PROJECT_DIR/skills/<name>/` (`~/.domyn/skills/<name>/` without a
     project) — **and add it to the config** (step 4).
     Nothing scans that folder: a skill created there and not listed in
     `config.yaml` is **never loaded**. Writing the file is half the job. If the user
     would rather keep their skills in `./.domyn/skills`, suggest `/skills-autodiscover on`
     instead: then the first case applies.
2. **Write the file**, with `name` and a `description` that says **when** the skill
   applies, not just what it is: the description is all the model sees when choosing
   a skill. The format (front matter, sections, `requires`, `enforcement`) is in the
   Skills page of `domyn-docs`.
   Files the skill needs besides its `SKILL.md` (a script folder, a helper) go in an
   optional `external_files` list, relative to the `SKILL.md`. For the user's own
   skills nothing is copied: each listed file must already exist, or the skill is
   marked unavailable.
   **`external_files` must list every file the skill uses** besides its `SKILL.md`:
   `domyn export` copies a skill as its `SKILL.md` plus exactly those files, so a
   file left off the list stays behind and the exported skill breaks.
3. **Create it with the right tool.** `write_file` can create the file in both
   places (the user is asked to approve): `./.domyn/skills` is inside the workspace,
   and the configuration's `skills/` folder is reachable while it holds an installed
   built-in skill. If `write_file` refuses the path (no built-in installed there),
   create it with a shell command instead.
4. **With autodiscovery off, add the skill to the config.** Append the new skill's
   folder to the `paths` list under the root agent's `skills: source:` in the file
   `/config` names. In a project, write it as
   `${DOMYN_PROJECT_DIR}/skills/<name>`, the way the installed skills are written
   there, so the project still works moved or exported; without a project, write the
   absolute path. Put it before the built-in skills if it should win a name clash.
   The file tools cannot open the configuration folder's `config.yaml`, so this is a
   shell command the user approves; keep the YAML valid, and change nothing else.
5. **Check, then tell the user it is loaded from their next message.** With
   autodiscovery off, read the config back (`grep` the new path in it) before saying
   the skill is ready; if the entry is missing, step 4 is not done. In both cases the
   config and the skill files are read again before every message. `/skill <name>`
   shows it now. If it does not appear, the path written in the config is wrong, or
   the edited file no longer loads — the session then says "changed but cannot be
   loaded" and keeps the previous configuration until the file is fixed.
   - A skill created in the configuration's `skills/` folder sits where `domyn setup`
     installs the built-in skills, and every `domyn setup` rewrites that folder: the
     next setup names it as "not a built-in skill" and asks before deleting it, and
     if the user keeps it, setup leaves the built-ins as they were. Tell the user,
     so the question does not come as a surprise.

**Where skills come from, in precedence order** (if two have the same name, the
first one found wins): the paths in the agent's `skills.source.paths` in
`config.yaml`, in the order listed. `domyn setup` writes `.domyn/skills` and
`.agents/skills` (autodiscovery) first, then the user's own skills it was pointed at,
then the built-in ones it installed, so a skill of the user's beats a built-in of the
same name.

Nothing else is searched. The skills inside the package are not a fallback: they are
only the source `domyn setup` copies from, so a configuration with no `skills` entry
has none of the built-in ones.

**A relative path is read from the folder `domyn run` is started in**, which is what
makes `.domyn/skills` mean `./.domyn/skills` wherever it starts. A project's own files
are written `${DOMYN_PROJECT_DIR}/...` instead, which the CLI sets to the project's
folder. A listed path that does not exist (deleted, moved, or relative to another
folder) is named at startup as "Skill not found: ..." — except `.domyn/skills` and
`.agents/skills`: most folders have neither, and that is normal. The list in the global
`~/.domyn/config.yaml` is shared by every folder; a configuration of its own is a
project (`domyn setup --project <name>`, then `domyn run --project <name>`).

**The built-in skills** are chosen in `domyn setup`, which copies each chosen one
(and the files it shares with others) into `~/.domyn/builtin-skills/` and lists it in
`config.yaml`. The project's own skills are listed where they are: nothing is
copied. To change either choice, the user re-runs `domyn setup`, which pre-ticks the
current ones. For the built-ins it rewrites the directory from scratch: a skill left
unticked disappears, and one that changed in the package arrives in its new version.
An edit to an installed built-in skill is lost the next time. To customise one,
untick it in `domyn setup` and keep a copy under `./.domyn/skills`.

A listed skill whose `external_files` are missing is reported at startup as "Skill
'<name>' needs files that are missing: ...", and is unavailable until they are there
(`/skills` shows why). Create the files (a path is relative to the skill file), or fix
the `external_files` list; it counts from the next message, nothing to re-run. The reverse is
silent at run time: a file the skill uses but does not list works here, and is only
noticed when `domyn export` leaves it behind. So when writing or reviewing a skill,
check that every file its instructions or scripts refer to is listed.

Editing a skill of the user's own means editing its file, at the path `/skills`
shows. To stop loading a skill, run `domyn skill remove <name>` (with
`--project "$DOMYN_PROJECT_DIR"` in a project, see *Which configuration this session
runs*): it removes the entry naming that skill (its folder or its `.md` file) from the
config and leaves the files where they are. Without `--project` it edits
`~/.domyn/config.yaml`. A skill loaded through
`./.domyn/skills` or `./.agents/skills` autodiscovery, or through a listed folder
holding several skills, is not listed on its own, so the command changes nothing and says so: turn autodiscovery off
(`/skills-autodiscover off`), or delete or move the skill's file. The session picks
the change up from the next message; `/skills` shows it right away.

## Writing SOUL.md or AGENTS.md

Both are plain markdown, no frontmatter. Pick the file by what it holds:
**`SOUL.md`** for identity, tone and standing preferences (it follows the user);
**`AGENTS.md`** for what the agent is working on (it follows the task or project).

Steps:

1. **Check what exists.** Ask the user to type `/config`: it lists the instruction
   files loaded right now, with their paths. Edit the one already there rather than
   creating a second: every `SOUL.md` and `AGENTS.md` found is loaded, so a second
   file adds to the first instead of replacing it.
2. **Decide where it goes**, by the same rule as a new skill. Read the config file
   of this session (see *Which configuration this session runs*) and look at the
   root agent's `standing_instructions: source: paths`:
   - **Autodiscovery is on** (the paths list `.domyn` or `.agents`): write
     **`./.domyn/SOUL.md`** or **`./.domyn/AGENTS.md`**, relative to the folder the
     CLI was started in (`./.agents/` is the folder other agent tools share; use it
     only when the user wants them to read the file too). Nothing else to do.
   - **Autodiscovery is off**: write it in the **configuration's own folder**,
     `$DOMYN_PROJECT_DIR/SOUL.md` in a project, `~/.domyn/SOUL.md` without one (the
     same for `AGENTS.md`), **and add it to the config**: append its path to
     `standing_instructions: source: paths`, as `${DOMYN_PROJECT_DIR}/SOUL.md` in a
     project. No folder is read without being listed, so a file there that the
     config does not list is **never loaded**; read the config back to check the
     entry.
3. **Create it with the right tool.** `./.domyn/` is inside the workspace, so
   `write_file` can create the file there (the user is asked to approve). The
   configuration's folder is outside it: use a shell command.
4. **Tell the user it is used from their next message**: the files are read again
   before every message. `/config` shows it loaded.

## Reading and changing the config

`config.yaml` is a standard domyn YAML application file, the same format that can be
passed to `domyn run <file.yaml>`. What `domyn setup` writes, and the settings most
worth changing, are in the "Configuring the CLI" page of `domyn-docs`; every key is in
its YAML reference.

**The context window.** Write it as `context_window` in the provider block. The
wizard also accepts `max_model_len`, but the running provider does not: a hand-written
`max_model_len` is ignored. A provider block without `context_window` is "auto": the session asks the
provider for its window at start and assumes 150000 when it cannot answer. `/config` shows it
as `auto`, and `/context` shows the window the session got. `domyn setup` and `/model` write
the key only when the user types a number (`auto` or an empty answer leaves it out).

**Reading it.** Ask the user to type `/config` for a summary with secrets removed, or
run `domyn setup --show`. To read the raw file, use `cat` on the path `/config`
prints. Do not repeat a literal key if you find one: just tell the user that one is
there and should be moved (below).

**Changing it**, depending on what changes:

- **Provider, model, URL, API key, context window, max tokens** → the user types
  `/model` (applies right away) or runs `domyn setup` in a shell (applies from the
  next message of a running session, since it rewrites `config.yaml`).
  Both are interactive, so you cannot fill them in for the user.
- **Anything else** → edit the YAML. Edit the file `/config` names: it is
  `$DOMYN_PROJECT_DIR/config.yaml` in a project, the file given to `domyn run` when
  there was one, `~/.domyn/config.yaml` otherwise.
  Below, `CONFIG` stands for that path. Before editing:
  1. Back it up: `cp CONFIG CONFIG.bak`.
  2. Make the smallest edit that does the job, keeping the existing structure and
     indentation.
  3. Check it still parses:
     `python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" CONFIG`.
  4. Tell the user it is used from their next message. If the session then prints
     "changed but cannot be loaded", the edit broke the file: restore the backup or
     fix it; the session keeps the previous configuration until it loads again.

**Secrets.** API keys belong in `~/.domyn/credentials` (written by `domyn setup` /
`/model`), in `.env`, or in an exported variable. In the YAML, refer to them by name
as `${VAR_NAME}`. If that variable is not set, the file fails to load and the CLI
says which variable is missing.

**Two things that can surprise the user, so mention them when relevant:**

- `domyn setup` and `/model` **rewrite the whole file** from the fields they know
  about: the provider's type, model, url, `max_tokens` and `context_window`; the
  agent's name, description, instruction, stream, skills and
  `standing_instructions`; the tool bundle's bundles, workspace, backend (and its `docker` options), isolation,
  `allowed_env` and `browser` options; and the compaction settings. Anything else is
  dropped, e.g. `mcp_servers`, `hooks`, `tools`, extra agents, other
  `generation_params` (temperature, …) and provider `headers`. A custom `${MY_VAR}`
  key reference is replaced by the provider's usual variable name. If the file has
  been edited by hand, suggest backing it up first, or edit the provider block by
  hand instead.
- `/model` starts from the file **as it is now** (it reloads it first), so hand
  edits are kept, subject to the rewrite above.

To start over: `domyn setup` (it pre-fills the current values; Enter keeps them).

## Troubleshooting

| symptom | likely cause and fix |
|---|---|
| "No configuration yet" / setup opens on every run | config missing or incomplete (no model; no `url` for vllm/custom). Run `domyn setup` |
| fails at startup naming an environment variable | a `${VAR}` in the YAML is not set. Set it in `.env`, `credentials` or the shell, or re-run `domyn setup` |
| auth errors when calling the model | key missing or wrong. `/model` asks for it again and saves it to `credentials` |
| a `config.yaml` edit "did nothing" | not reloaded. Restart (`/exit`, `domyn run`) |
| a SOUL.md / AGENTS.md edit "did nothing" | it applies from the next message, so check that the edited file is the one being read: `/config` lists the paths in use. A sub-agent reads only the `standing_instructions` its own YAML entry declares |
| a new skill does not appear | it must be in `./.domyn/skills` or `./.agents/skills` with autodiscovery on, or listed in `config.yaml`; either way it is loaded from the next message (the config's skill paths and the skill files are read before every message). Otherwise a skill earlier in the precedence list has the same name, the listed path is wrong (`/config` shows the paths), or a "Skill not found" line at startup says so |
| "Tool-call arguments still malformed after 3 retries" | the answer hit `max_tokens`. Raise it through `/model` |
| the conversation hits the model's limit and is never compacted | no `context_window` in the provider block (or it is spelled `max_model_len`). Add `context_window`; it applies from the next message |
| `/model` says it only applies to the default configuration | the session was started from a file. Edit that file; it applies from the next message |
| a file outside the project is refused | workspace containment. Start the CLI in that directory or set `workspace` |
| tools do not run in the Docker container | `backend` in the tool bundle (the `tool_bundles` entry that lists `shell`) is `local`, or it is `auto` and Docker was not running, or its image could not be pulled, when the session started (it warns and the line under the banner says `tools: this machine`). Check the value, start Docker and restart; the check from inside is `test -f /.dockerenv && echo container \|\| echo host`. `backend: docker` refuses to start without Docker instead |
| a command fails with `[docker] blocked connection(s) to <host>` | the container's `docker.allowed_network` is a list that does not have the host. Add it to the list in the tool bundle (applies from the next message), or set `allowed_network: public` (any public site over HTTPS, the default). Plain `http://`, other ports and private addresses are refused in every mode |
| "The container was lost; starting a new one" | Docker restarted or the container was removed during the session. The next command made a new one: workspace files and installed packages come back, anything else written inside the container is gone. If it keeps happening, check that Docker Desktop is not stopping or running out of memory |
