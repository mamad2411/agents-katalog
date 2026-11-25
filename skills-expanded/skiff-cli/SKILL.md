---
name: skiff-cli
description: Manage Skiff sessions and coordinate agent tasks with the skiff CLI. Use to list or report sessions, start agents, arrange panes, send tasks, monitor work, collect results, or stop requested sessions. Works from Skiff panes and external shells such as Termius.
---

# Skiff CLI

`skiff` talks to `skiffd`, the daemon that owns every Skiff terminal. The app and the CLI see the same sessions and groups. A change from one shows in the other at once. `skiff COMMAND --help` gives the full flags and exit codes.

`skiff skill path` prints the path of this file. It needs no daemon and no Skipper. Use it after a compaction, or in an agent that has no skills system. This file is plain text: read it as instructions.

## Boot sequence

Do these steps once per task, before the first other command.

1. Run `skiff status`. If the command is not found, stop. Tell the user to run Help › Install skiff command… in Skiff. If skiffd does not run, stop and tell the user to open Skiff. If it prints a warning, tell the user.
2. Check `$SKIFF_SESSION`. If it is set, you run in a Skiff pane. Then `.` is your own session, and `--group .` is the group of your pane. If it is not set, use ids. Do not use `.`.
3. Run `skiff ls --json` and `skiff group ls --json`. Read the JSON, not the tables. `"coordinator": true` marks the Skiff agent's session.

## Names

- A session is a full id, a unique id prefix, or the name the sidebar shows. A group is an id, a prefix or a name.
- An argument that matches more than one session is an error that lists them. Pick the id and run again.
- `skiff new --agent` with no `--name` gives the agent a random call sign, such as `Corsair Cutlass`. `skiff new --type T` names it after the type: `review`, then `review 2`. A shell has no name. The sidebar shows its title or program.
- A Skipper (Admiral, a project or a fleet Skipper) must give `--name` to `skiff new` and `skiff group new`. Without it, both exit 2 and start nothing. A person in a shell pane or outside Skiff is not checked.
- Name a session for one issue `#N feature`, with a short feature name from the issue title: `#136 kanban and calendar`. Name any other session with 2 to 4 words that say the task. Leave out the project name: the sidebar shows it. Name a group after the work it holds.
- Names change and can repeat. Use ids in scripts.

## Session report

For an overview of all sessions, run the bundled script from this skill's folder:

```sh
python3 <skill folder>/scripts/session_report.py --width 100
```

- It needs Python 3 and Rich. It changes nothing. It does not mark output as seen.
- It draws one table for each working directory, with names, states, unread output and titles.
- Always give `--width`. With no terminal on stdout, as from an agent's shell, it falls back to 38 columns.
- For a phone or a mobile chat, use `--mobile`. Do not paste a wide table into a mobile chat.
- `--details` adds paths, ids, programs, groups and empty groups.

Use the report to show the user what is open. Use the JSON to pick a target or make a decision.

## Commands

| Task | Command |
|---|---|
| List sessions, groups, projects | `skiff ls --json`, `skiff g ls --json`, `skiff projects --json` (`kind`: `git` or `folder`) |
| Add a project | `skiff projects add PATH [--name N] [--fleet F] [--json]` |
| Remove a project | `skiff projects remove NAME [--end-sessions]` |
| Start a shell | `skiff new [--name N] [--cwd DIR]` |
| Start an agent | `skiff new --agent ID [--name N] [--cwd DIR]` (`skiff agents --json` lists ids) |
| Start a task type | `skiff new --type T [--model M] [--cwd DIR]` |
| Start an agent with a model | `skiff new --agent ID --model M` |
| Start a command | `skiff new -- npm run dev` |
| Start next to me | `skiff new --agent codex --group .` |
| Type into an idle agent | `skiff send S "text" --enter` |
| Type a command into an idle shell | `skiff send S "make test" --enter --shell` |
| Send a long prompt | `skiff send S - --enter < prompt.md` |
| Read the screen | `skiff peek S [-n 40]` |
| Wait for a stop | `skiff wait S --for idle` |
| Wait for the first of several | `skiff wait S1 S2 --any --for idle` |
| Wait for a turn's end | `skiff wait S --for turn` |
| Follow state changes | `skiff events --json [S...] [--timeout SECS]` |
| Rename, clear the name | `skiff rename S "name"`, `skiff rename S ""` |
| Mark seen | `skiff seen S` |
| Stop | `skiff kill S... [--force]` |
| Groups | `g new [--name N] [--cwd DIR] [--dir row\|col] [S...]`, `g add G S [--split right\|down\|left\|up] [--of S]`, `g rm G S`, `g rename G N`, `g delete G...` |
| Themes | `skiff theme ls`, `theme session\|project\|app set ... ID`, `clear` |
| Open with | `skiff open-with ls`, `set KEY "CMD"`, `clear KEY`. Keys: `diff`, `text`, `markdown`, `html` |

- `skiff new` prints the new id. `--json` prints the full session.
- `--cwd` is relative to your current folder. With `--group` and no `--cwd`, the session starts in the group's folder.
- Without `--split`, the group takes its next template shape: 2 side by side, 1 left and 2 right, then 2 by 2. `--split` halves one pane, so repeated splits shrink the newest pane. `--split` needs `--group`. A full group refuses before anything starts.
- A group holds 4 panes at most. A session is in one group at most. `g add` takes it out of its old group.

States: `working`, `waiting`, `idle`, `done`.

- `waiting` is an approval prompt or a bell. Only a person answers it.
- `idle` means no output for a while. It does not prove that the agent is done.
- An agent that exits leaves a shell in its pane. `done` means the shell exited too.

## Task types

`skiff agents --json` prints `{"agents": [...], "tasks": [...]}`. Each task row has `type`, `agent`, `model` (null: the agent's default), `file`, `instructions`, `command` and `error`. The person sets the table in Settings › Task types.

1. Pick the type yourself. Skiff reads no task text.
2. Do not use a row whose `error` is not null.
3. If a task fits a type, start it with `skiff new --type T --cwd DIR`.
4. If the person names a model, add `--model M`. `skiff new --agent ID --model M` adds the same model flag. A custom agent (`"custom": true`), opencode and hermes take their model in the command and refuse `--model`: exit 1, nothing starts. `--model` with `-- CMD` is an error.
5. If no type fits, start the project's agent with `--agent`.

`--type` with no row exits 1 and starts nothing. `--type` with `--agent` or `-- CMD` is an error.

`file` is the type's instruction file, `types/<type>.md` in the agent folder. `instructions` is its size in bytes, or null when it is missing, empty or only its `# <type>` line. With a file, `--type` gives it to the agent at start, on top of the project's `AGENTS.md` or `CLAUDE.md`. Do not repeat the file in the task text. Do not write the file: the person owns it. gemini, hermes and custom agents cannot take a file: the row has an `error`, and `--type` exits 1.

## Send a task

1. Find the pane in the JSON. Use its id. Confirm its working directory.
2. Run `skiff peek S -n 40`. Check the current result and the input box. If the task already runs or is complete, report that. Do not send it again. A known agent can show a prompt suggestion in gray in an empty input box. `peek` does not print that gray text, so text in the box was typed. Do not report a draft from `peek` alone. Send: only exit 9 tells you that the box holds a real draft.
3. Write a clear task: the result, the scope, the context, the permitted actions, and what to report. An investigation request permits an investigation only. Pass on a permission to fix or deploy only when the user gave it.
4. For a long prompt, write a file and send it with `skiff send S - --enter < file`. Keep shell syntax and user text apart.

`send` types the text as a paste. Newlines stay in the text. `--enter` presses Enter once, after the text.

Skiff has no message queue. A refused send types nothing. Do not wait and retry. Do not interrupt the pane to make room. Report that the task was not delivered.

### Send exit codes

`send` checks the session before it types. The checks run in this order:

| Exit | Condition | What to do |
|---|---|---|
| 7 | The session is your own (`$SKIFF_SESSION`), by any name | Send to another session. |
| 3 | The session is `waiting` | Tell the user which pane needs them. End the turn. |
| 4 | The session is `working` | Do not wait and do not retry. |
| 6 | The session is `done` | Its program exited. Start a new session. |
| 5 | A shell or an unknown program is in front | Add `--shell` only to type a shell command. A `skiff new -- CMD` session or a custom agent shows its launch shell, so it needs `--shell`. |
| 9 | A known agent shows a draft or its busy line, or the session took input after the check | For a draft, tell the user which pane holds it. For the busy line, do as for exit 4. A gray Claude Code prompt suggestion is not a draft. `send` exits 0 for it. |
| 0 | Sent | |
| 1 | Error, for example no match or more than one | |

`--shell` relaxes only exit 5. After the text goes in, one more check applies:

| Exit | Condition | What to do |
|---|---|---|
| 8 | `--enter` went to a known agent (Claude Code, Codex, Gemini, Grok, opencode, Hermes), but no turn started in 5 seconds | Run `skiff peek S`. If the text is in the input box, tell the user which pane, with its name and id. |

- `send` never presses Enter a second time. A second send while the text is in the box gets exit 9.
- There is no exit 8 without `--enter`, with `--raw`, or when the program in front is not a known agent.
- A turn that starts and ends in under 5 seconds with no output can also give exit 8.

## Monitor and collect the result

Keep monitoring after a send when the user wants the result. A request only to deliver a message ends when the send exits 0.

- Run one `skiff wait S --for idle` at a time. Finish an open shell call before you start another wait.
- In a Skiff pane, or with no terminal on stdout, `wait` stops after 45 seconds. A `--timeout` above 60 becomes 60. On a timeout, read the screen and wait again while the task runs.
- For several children, use `skiff wait S1 S2 S3 --any --for idle`. It prints the id, name and state of the first one. Read that screen, then wait on the rest.
- To keep your turn free, run `skiff events --json [S...]` as a background job. It has no time limit. In the foreground, give `--timeout`. With no names, it follows every session, new ones too.
- After each `wait` exit 0 and each event, run `peek`. `idle` means quiet, not done.
- An agent that reports its state (OSC 7501: Claude Code, Codex, Grok, Antigravity) says more. In `ls --json`, `program_status.state` is `working`, `blocked` (with `kind`: `permission`, `question` or `auth`, and `msg`), `idle`, `done` or `error`. `done` and `error` end a turn. `skiff wait S --for turn` waits for that end, and exits 4 when it was an error. Still read the screen: the report says the turn ended, not what it did.
- Collect the result, the checks and any blocker. Do not report a task as done from the state alone.
- For a deployment, get the agent's deployment result before you call it live. Keep local checks apart from production checks.
- A child leaves its result on screen. For a long result, give the child a file path.

`wait` exit codes:

| Exit | Meaning |
|---|---|
| 0 | Every session reached the state. With `--any`: one did. |
| 1 | Timeout. |
| 2 | A session closed or exited first. With `--any`: every session did. |
| 3 | A session is `waiting`. With `--for idle`, `done`, `any-not-working` or `turn`, this stops the wait at once. |
| 4 | With `--for turn`: a turn ended in an error the program reported. |

With `--for idle`, a known agent that shows its busy line ("esc to interrupt") is not idle yet.

`events --json` lines:

```
{"event":"state","session":ID,"name":N,"state":"idle"}
{"event":"exit","session":ID,"name":N,"code":0}
{"event":"removed","session":ID,"name":N}
{"event":"status","session":ID,"name":N,"program_status":{"state":"blocked","kind":"permission","msg":"..."}}
{"event":"turn","session":ID,"name":N}
```

A `status` line comes when what a program reports changes its state, what it waits for or its message; `program_status` is `null` once it reports nothing. A `turn` line comes when a turn ends.

`events` exits 0 when `--timeout` ends or every named session is gone, 1 on an error, and 2 when a name matches no session.

For several agents, give each a different task and folder. If they share a repository, say which files each one can change. Collect each result before work that depends on it. Start agents only in the requested scope. A named existing pane can do a single task.

## The Skiff agent and its ledger

The Skiff agent is the main Skipper and the normal coordinator. Its default name is Admiral; a stored name `Skipper` also shows as Admiral. It is one agent session in its own folder, `~/skiff-agent` by default. The app makes that folder at start, with the agent on or off, and turning the agent on adds its files there. Its `AGENTS.md` is the user's standing permission to send tasks to sessions in Skiff projects. A person opens it from its row in the app, or with `skiff skipper` in any terminal. `skiff skipper --no-attach` prints its id.

The ledger is `ledger.db` in that folder. Use only `skiff ledger` to read or change it. Never open or edit the file.

- Each row has an owner: Admiral, the main Skipper (`grand`), a project Skipper (its project's name), or a fleet Skipper (`fleet:<fleet>`). `ls` shows an OWNER column when a project or fleet Skipper owns a row.
- A coordinator changes only its own rows: `add`, `send`, `update`, `report`, `close`, `reopen`, `prune`, `rm`. The CLI knows the caller from its session. `skiff skipper` records Admiral's session. A project or fleet Skipper may also report the hand-off it was given: `ledger update UID --state done [--outcome O] --result PATH`, and no other change. Another agent pane gets a refusal. A shell pane is a person and may change any row. A shell outside Skiff is refused, unless a person passes `--person`.
- `ls`, `show` and `stale` work from anywhere.
- Each row has an id and an 8-character uid. Neither is used again. Every ID argument takes both. Use the uid when you name a task.

Task states are `pending`, `sent`, `blocked` and `done`. A done task also has an outcome: `succeeded`, `failed`, `interrupted` or `unobserved`. A task whose pane is gone is `unobserved`, never `succeeded`. `ls` shows an OUTCOME column when a row has one. `ls` and `show` also print:

- `interrupted`: the pane restarted after the send. A restore runs a new shell under the old id, so the task does not run.
- `gone`: the session closed. Skiff sets the task `done`, `unobserved`, on the next `ledger ls`, `ledger show` or watcher step, whatever its state was, and its work closes when nothing else holds it. An `interrupted` or `elsewhere` task, or an unanswered session list, closes nothing. A skiffd that had a failed load closes nothing either, and does not write its workspace file, until someone clears the fault and restarts skiffd. A failed load is a file that cannot be read or parsed, or a file with saved sessions of which none started. If at least one started, a saved session that cannot start is closed: its task closes, and its entry leaves the file at the next save. Each ledger read says so on stderr, and each watcher says so in one `[watch]` line. Tell the person. An interrupted task whose session closes later takes this path. The files stay until a flush. `--json` shows `state` `done` and a `gone_at` stamp.
- `elsewhere` in LIVE: the task went out on another daemon. Its socket shows. It is not gone. Leave it to that daemon's Skiff agent.

A plan shows `done` when every task in it is done, else `sent`.

Work is a plan with its tasks, or a task with no plan. It is `working` while an agent is on one of its tasks (the task is `sent`, and its pane works or ended its turn), `open` otherwise, and `finished` once closed. Done is not closed. Work closes by itself when every task in it is closed. A task is closed when it is done and reported, done and flushed by the person, or when its session closed. A session closed means it no longer exists, or its program and shell exited (state `done`). An idle session is not closed, so a blocked or finished task in an idle session stays open. A hand-off with tasks stays open until its Skipper reports it or its Skipper's session closes. Then it follows its tasks. A hand-off with no tasks follows its Skipper's session. This has the same effect as `ledger close`. A plan with no task stays open. After `ledger reopen`, work stays open until a task in it changes state.

### Project Skippers

A project can have its own Skipper: one agent session in the project's folder, at most one per project. No Skipper starts by itself: the person starts it from the project menu, or a hand-off starts it. Its folder is always `projects/<project>/` in the Skipper folder (`~/skiff-agent/projects/<project>/` by default): its instructions are `SKIPPER.md` there, and its results go to `results/` there. `SKIPPER.md` holds the project section only. `AGENTS.md` in the Skipper folder is the base of every Skipper. Skiff never writes over the person's edit. Skiff writes nothing into the project. A restore brings its pane back as a plain shell. Its session is named `<project> Skipper`, such as `gesher Skipper` (a name set in Settings takes the place of `Skipper`), so `skiff send "gesher Skipper" ...` reaches it and never Admiral; the sidebar shows it as "Skipper" inside its project block.

- `skiff skipper --project P` finds or starts it, and attaches. `--no-attach` prints its id. A new one gets one first message: read this skill's `SKILL.md` by its full path before any `skiff` command, read `AGENTS.md` in the Skipper folder, then `SKIPPER.md`, which wins where the two differ, then do the First steps. The message is plain instructions, so an agent with no skills system can do it. Skiff links the skill only into the Skipper folder, and a project Skipper starts in the project, so this message is how it finds the skill.
- Admiral hands work to it with `skiff ledger handoff P "TASK" --title "..." [--parent UID]`. This adds a hand-off row that Admiral owns, with the project Skipper as its pane. It starts the project Skipper if none runs, and sends it the task. It exits with `send`'s code. A busy project Skipper keeps the row `pending`.
- The project Skipper adds its tasks with `--parent UID` of the hand-off. Those rows are its own. When they are done, it reports the hand-off: `skiff ledger update UID --state done --result PATH`.
- Admiral can cancel a hand-off: it is Admiral's row. It cannot change the project Skipper's tasks, or add tasks under a hand-off.
- For a follow-up, Admiral gives `--parent UID` of the earlier hand-off, or names its uid in the task. With `--parent`, the new hand-off joins that hand-off's plan, or a new plan of Admiral's wraps both. A hand-off never goes under a hand-off.
- Brief: `handoff` writes `brief.md` in the hand-off's folder. It lists the rows that the hand-off joins with `--parent` or cites by uid, one step further, with the tasks under them: each with its state, outcome, pane, result path and the first 300 bytes of its task. Then it lists the scope's open work. It is at most 8 KiB, and a "Left out" line counts what did not fit. It has no decisions and no result bodies: the task text carries the decisions. The message names it when it differs from the last brief that this Skipper session got, and always for a new Skipper. `--no-brief` writes none. `skiff ledger brief UID` prints it as of now.
- `ledger close` on Admiral's plan also needs the hand-off's tasks done.
- `ledger report` on the hand-off also stamps the done tasks under it, though the project Skipper owns them, and names each that did not succeed on stderr.

### Fleet Skippers

A fleet can have one Skipper for all its projects. It is a project Skipper with a wider scope. Its folder is `fleets/<fleet>/` in the Skipper folder, with `SKIPPER.md` and `results/`, and it starts there. Its `SKIPPER.md` names no project: it runs `skiff projects --json` at the start of each turn. Its first message names this skill's `SKILL.md` too: the fleet folder has no link to the skill. Its rows have the owner `fleet:<fleet>`. Its session is named `<fleet> Skipper`, such as `Harbor Skipper`. The sidebar shows it as "Skipper", the first row under its fleet head.

- `skiff skipper --fleet F` finds or starts it, and attaches. `--no-attach` prints its id. When project Skippers run in the fleet, it names them and asks y/N; `--yes` does not ask. With no terminal and no `--yes`, it refuses.
- Admiral hands work to it with `skiff ledger handoff F "TASK" ...`. A name that is both a project and a fleet is refused: use `fleet:F` or `project:F`.
- It sends tasks only into the projects of its fleet, as `skiff projects --json` shows them now. `ledger add --pane` and `ledger update --pane` refuse a pane in another project.
- It does not hand off. One Skipper per project: while it runs, a project of its fleet has no project Skipper. `handoff PROJECT` and `skipper --project` for such a project are refused and name the fleet. `handoff F` while project Skippers run in the fleet and no fleet Skipper does is refused.
- Takeover: a project with a project Skipper that joins a fleet whose Skipper runs, or a fleet Skipper that starts over project Skippers, takes the project Skippers over on the person's confirm. Every row they own moves to `fleet:<fleet>`. Each open hand-off to the project gets the fleet Skipper as its pane; `pending` and `blocked` become `pending`. The project Skipper loses its mark and ends when idle. Its ledger writes are refused. The fleet Skipper gets one `[watch]` line that names the project, the open tasks and the hand-offs.
- When a project joins or leaves the fleet, the fleet Skipper gets `[watch] F changed: P joined. Read SKIPPER.md again.` Open tasks in a project that left stay its own.

### Instruction files

`AGENTS.md` and each `SKIPPER.md` start as a template. At each Skipper start, Skiff rewrites a file that it wrote itself when the template changed. It never overwrites a file that a person edited.

- `skiff status` prints one warning for each file that is edited and whose template changed, with the command to run. It writes nothing. `--json` gives the same files in `templates`.
- A new project or fleet Skipper gets one more sentence in its first message when its own files have this state.
- `skiff skipper template ls` lists each file with its scope and status: `none`, `template`, `edited` or `edited-template-changed`.
- `skiff skipper template diff SCOPE` shows the change. `-` lines are the file, `+` lines the template. SCOPE is `agents`, `project:NAME` or `fleet:NAME`.
- `skiff skipper template apply SCOPE` replaces the file with its template, and the old file goes to `<name>.bak`. Run it only when the person asks.

### Ledger commands

| Command | Use |
|---|---|
| `ledger add --pane S --task "..." --title "..." --send --enter [--parent UID] [--type T] [--ref TEXT]` | Add a task and send it. |
| `ledger add --plan --task "..." --title "..." [--ref TEXT]` | Add a plan for work with more than one task. |
| `ledger handoff SCOPE "TASK" --title "..." [--parent UID] [--no-brief]` | Hand a task to a project's or a fleet's Skipper. SCOPE: `NAME`, `project:NAME` or `fleet:NAME`. Admiral only. TASK `-` reads stdin, as `add --task -` does. `--parent` may name an earlier hand-off. |
| `ledger brief UID [--json]` | Print a hand-off's brief as of now. It writes nothing. Exit 1: the row is not a hand-off. |
| `ledger send UID --enter` | Send a `pending` or `interrupted` task. |
| `ledger update UID [--state S] [--pane S] [--title T] [--result PATH] [--parent UID] ...` | Change only the given fields. |
| `ledger update UID --outcome O [--commit REF]` | Set how a task ended: `succeeded`, `failed`, `interrupted` or `unobserved`. It sets the task `done`. `--state done` alone gives `succeeded`, or `unobserved` when the evidence the task expects (`add --expect result\|commit`) is missing. |
| `ledger ls [--state S] [--all \| --closed \| --unreported] [--json]` | Show the work that is not closed: working, then open. |
| `ledger show UID [--json]` | Show one row, with its delivery attempts: the session, the payload's bytes and SHA-256, and the evidence (`turn started`, `text accepted`, `no turn`, `refused` or `uncertain`). |
| `ledger report UID... \| --all` | Mark done tasks as told to the person. |
| `ledger close UID...` | Close work on the person's word, before each task is reported. |
| `ledger stale [--older-than 7d] [--json]` | List each row that holds open work with no change for that age, with its session's name and why. Close an idle session to close its task. It closes nothing and writes nothing. A work item with a working session is left out. A hand-off with tasks is listed until its Skipper reports it; its session is the Skipper, so it does not leave the work out. |
| `ledger reopen UID...` | Open closed work again, or keep open work open. Use it for work that waits on the person. |
| `ledger prune [--older-than 7d] [--yes [--flush]]` | Remove closed work. Without `--yes` it only prints it. |
| `ledger rm UID [--flush]` | Remove one row now. |
| `ledger dir UID` | Print the row's work folder. |

- `add` makes the row's work folder and prints the id, the uid, the folder and the result path. It makes no file in the folder. A task needs `--pane`. A plan has none.
- `--send` and `ledger send` add " Put everything for this task in FOLDER: the result, screenshots, scratch copies and worktrees. Write your result to PATH." to the task text. Do not put the folder or the path in `--task`.
- Both run every `send` check and exit with its code. Exit 0 sets `sent`. Exit 8 sets `blocked`. A refusal leaves the task `pending`.
- `ledger send` exits 1 and types nothing for a task that is `sent`, `blocked` or `done`, for a plan, for a gone pane, or for a task on another daemon.
- Give every task and plan a `--title` of 3 to 6 words, such as `--title "Fix found-set count"`. Without one, the Ledger panel uses the first sentence of the task.
- `--type T` records the task type. `--ref TEXT` stores a URL or a ticket key. Skiff stores both and does not act on them.
- `--parent UID` joins a task to its work: a plan or any task in it, or a task with no plan. A task with no plan goes into a new plan with its title, project, ref and type, and `add` prints the plan's uid. A plan cannot be under a plan. A task added or moved under closed work opens it again.
- `ls` groups rows by work in its WORK column: `working`, then `open`. `--closed` shows closed work, `--all` every row. `--json` adds `bucket` and `closed_at`.
- `ls --state` takes `sent`, `pending`, `blocked`, `done`, `interrupted` or `gone`. `ls --unreported` lists the done tasks to report. A flushed task is not in it.
- Run `ledger report` in the same turn as you tell the person. A plan's uid reports its done tasks. A hand-off's uid also reports the done tasks under it. A task that is not done is refused. A state change away from `done` clears the report and flush marks and opens the work again.
- `ledger close` takes a plan, or a task with no plan. It refuses work with a task that is not done, and a task in a plan. It reports the done tasks of the work.
- After each `ledger` command that writes, after each sweep and after the person's flush, Skiff closes the work whose tasks are all closed. A command prints one line for each to stderr. A task that closes unreported and did not succeed (failed, interrupted, unobserved, or open when its session closed) gives Admiral one `[watch]` line, wherever the close ran. Auto flush takes a row's files only when its work is closed, and closes nothing. Work that `ledger reopen` named is not closed until a task in it changes state, is added, or moves into it.
- `prune` removes only closed work, with its tasks. `rm` and `prune` keep the work folders and result files. With `--flush` they also flush each work folder that Settings › Disk use would flush: the work is done, its pane is not working, nothing in it changed in the last 15 minutes, and no git checkout in it has changes or unpushed commits. A folder in use stays, and the output says why.

Work folders: `add` and `handoff` make one folder for each row, in `results/` in the agent folder, in `projects/<project>/results/` for a project Skipper's rows and a hand-off to it, or in `fleets/<fleet>/results/` for a fleet Skipper's. The name is `<uid>-<slug>`, from the title. It never changes.

- A plan, or a task with no plan: `results/<uid>-<slug>/`. A plan's notes go in `plan.md` there. A task's result goes in `result.md` there.
- A task in a plan: `<uid>-<slug>/` in the plan's folder, with `result.md`.
- A hand-off: `<uid>-<slug>/` in the project's or fleet's `results/`, with `result.md`. The tasks under it get their folders in it.
- Put everything for a task in its folder: the result, screenshots, scratch copies and worktrees. `ledger dir UID` prints it. Settings › Disk use flushes a done task's folder as one unit.
- A row from before work folders keeps its old result path and has no folder.

### The watcher

`skiff watch` runs while a Skipper runs: the Skiff agent, or a project or fleet Skipper. Each `[watch]` line goes to the coordinator that owns the task. A project Skipper hears of its own tasks; Admiral hears of its own, and once of each hand-off a project Skipper reports. It types one `[watch]` line into the coordinator when a ledger pane ends a turn, exits, restarts or is gone, or is idle with a pending task. It types only while the agent is idle and its input box is empty. A `waiting` pane gives the person a desktop notification and gives the agent nothing. The app sends that notification itself and starts the watcher with `--no-notify`.

A plan holds the turn ends of its tasks. While a task in the plan still runs, a pane that ends its turn on a `sent` task of the plan gives no line. When every task in the plan has ended, the watcher types one line for the plan: `[watch] plan UID: 3 of 3 tasks ended: pane NAME ID, ...`. A task has ended when it is `done` or `blocked`, or `sent` and its pane is idle, exited, restarted or gone. A `pending` task, a pane that works or waits, and a hand-off that is not done still run. A pane that exits, restarts or is gone, or is idle with a pending task, still gives its own line at once. A task with no plan works as before.

1. Read each pane that a `[watch]` line names with `skiff peek`.
2. Then run `skiff seen S`. An unread pane is named again on the next run.
3. A gone pane cannot be marked seen. The `[watch]` line names the tasks that skiff set `done` with it. Tell the person, then run `skiff ledger report UID...`. To run a task again, reassign it with `skiff ledger update UID --pane S --state pending`.
4. On `[watch] N done tasks not reported`, run `skiff ledger ls --unreported` and report them.
5. On `[watch] the P Skipper reported hand-off UID`, read the hand-off's result, tell the person, then run `skiff ledger report UID`. That also stamps the tasks under it.
6. On `[watch] Closed KIND UID with no report`, tell the person what it names. It comes once. A hand-off in it that a Skipper reports later gives its normal line.
7. On `[watch] plan UID: N of M tasks ended`, read each pane it names and mark it seen. Set each task `done` with its result, tell the person in one report, then run `skiff ledger report UID`.
8. On `[watch] the P Skipper exited: hand-off UID is open` (or `restarted`), tell the person. Do not start the Skipper yourself. `skiff skipper --project P --no-attach` (`--fleet F` for a fleet) starts a new agent in its shell, or a new session, and sets its open hand-offs `pending`; resend each with `skiff ledger send UID --enter`. A Skipper's turn ends and idle time give no line.

### The Ledger panel

The app shows the ledger in a panel at the right of the Skiff agent's pane, and of each project or fleet Skipper's pane. The panel is read-only. Its filter shows all projects, a fleet, or one project: Admiral's panel opens on all, a fleet Skipper's on its fleet, a project Skipper's on its project. A fleet shows its Skipper's rows, the hand-offs to it and its projects' rows. A hand-off shows its project's letters, or the fleet's letters with no color, and nests under its plan, with its tasks one step under it. It shows three sections: Working, Open and Finished. Open lists the rows that need the person first, then done tasks, then the rest. Finished shows the last 20 closed work items. A row that needs the person is amber. Closed work moves to Finished. Each row shows in the section of its work's bucket, as `ledger ls` gives it. The panel shows `--title`.

## Recipe

Hand a task to a new agent and collect the result:

```sh
id=$(skiff new --agent claude --name reviewer --cwd /path/to/repo)
skiff wait "$id" --for idle                # let it boot
skiff peek "$id" -n 40                     # check the agent and its input box
skiff send "$id" "Review the diff on this branch. List bugs only." --enter
skiff wait "$id" --for idle                # on exit 1, peek and wait again
skiff peek "$id" -n 80
```

## Rules

- Never signal skiffd (`kill`, `pkill`, `killall`). skiffd ignores SIGTERM and SIGINT from its own panes and logs the sender.
- Run `skiff daemon stop` or `skiff daemon reload` only when the user asks. `stop` ends every session.
- Do not `kill` a session, or take it out of its group, unless the user named it or you started it in this task.
- `kill` refuses a session with an open ledger task (pending, sent, blocked or interrupted), from any Skipper. It names each session with the task uid and title, kills none of the given sessions, and exits 10. Close the task first. Use `--force` only when the user asks.
- Do not `send` to a session you did not start unless the user asked. A request in this conversation counts. A standing permission in the instructions file of your own folder also counts, such as the Skiff agent's `AGENTS.md`.
- A standing permission covers `send` only. It does not cover `kill`, removal from a group, approvals or theme changes. Every `send` and `wait` refusal still applies.
- Only a person answers an approval. On exit 3 from `send` or `wait`, tell the user the pane's name and id. End the turn. Do not answer the prompt. Do not retry until the user says so.
- Never wait for the session that started you. A send to a busy parent gets exit 4. Then leave the result on screen or in a file and end your turn.
- If a child's report names another pane that needs a person, pass the report to the user and stop.
- `skiff projects add PATH` adds the git repository that holds PATH, or the folder itself when it is in no repository, with the app's defaults: the folder's name, a free color, a theme of its own. A folder in a linked worktree adds the main worktree. A folder that is already a project exits 1: `Already added as the project NAME.` A closed project opens again with its own settings: `Opened the closed project NAME again.` `--json` prints the project as one item of `skiff projects --json`. `--fleet F` puts a new project in fleet F. After a clone, add the repository, so that its sessions can take tasks.
- `skiff projects remove NAME` forgets the project and its settings. The folder and its worktrees stay. While sessions run in the project, it exits 1 and names them. `--end-sessions` ends them first; use it only when the user asks. The app shows an add or a remove within a second or two.
- Change a project or app theme, or an Open with command, only when the user asks. They change `projects.toml` and apply to every pane.
