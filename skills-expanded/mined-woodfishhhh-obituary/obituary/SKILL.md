---
name: obituary
description: Delete restorably and give scratch files a lifespan with Obituary (obit). Use before deleting any file or directory; when creating scratch space, debug scripts, logs, screenshots or test output that should not outlive the task; when a deletion command was denied by Obituary's delete guard; and when a file you expected is missing.
---

# Obituary (讣告) — the trash bin for AI agents

Obituary gives files and directories a lifespan. When it runs out they are buried in a graveyard, where they stay restorable for 7 days by default before they are purged. Anything you bury or delete through `obit` can be put back exactly where it was. The CLI is `obit`; it is on PATH.

## Quick rules

| You are about to… | Do this |
|---|---|
| delete a file or directory | `obit bury <path>...`, or `obit rm -rf <path>` with the usual `rm` arguments. Not plain `rm -rf`, `del`, `Remove-Item` or `git clean`. |
| create scratch space | `dir=$(obit mktemp 1d)` in bash, `$dir = obit mktemp 1d` in PowerShell |
| leave a debug script, log, screenshot or test output | `obit mark <path> 2d` (any lifespan: `30m`, `2h`, `3d`, `1w`, `1d12h`) |
| back up a file before editing it (`*.bak` and the like) | `obit mark <backup> 1w` |
| recreate something that is missing | first `obit graveyard --here`; if it is there, `obit resurrect <id>` |
| undo the deletion you just made | `obit resurrect --last` |
| are asked, when you stop, to sort files you created this session | `obit mark <path> 2d` for scratch, `obit bury <path>` for what is done with; deliverables stay |
| act on a proposal, a `.obitrules` file or a purge | describe it to the user; approving, trusting and purging are theirs |

If tools named `obit_*` are available (Obituary's MCP server), they do the same with absolute paths: `obit_mark`, `obit_mktemp`, `obit_bury`, `obit_resurrect`, `obit_extend`, `obit_spare`, `obit_list`, `obit_graveyard`, `obit_proposals`, `obit_stats`.

## Lifespans

- `obit mktemp <lifespan>` returns a new directory that is buried when the lifespan ends. Inside a Git project it lives in `.obit/tmp/`, which Git ignores.
- `obit mark <path> <lifespan>` gives an existing file or directory a lifespan; it stays where it is until then.
- `obit list` shows what has a lifespan and how long is left. `obit extend <id> <lifespan>` gives more time; `obit spare <id>` stops tracking and keeps the file.
- State and result commands (`list`, `graveyard`, `proposals`, `stats`, `mark`, `bury`, `resurrect` and similar) accept `--json`.
- Once per session, when you are about to stop, Obituary may list the files you created in this session that still have no lifespan and that Git does not track. Scratch among them (debug scripts, logs, screenshots, temporary output) gets `obit mark <path> <lifespan>` or `obit bury <path>`; deliverables stay. Only the listed files are in question.
- If a command reports `commit unconfirmed`, its change may already have taken effect: check `obit list` or `obit graveyard` before running it again, since each `obit extend` adds more time.

## Deleting

- `obit bury <path>...` moves things into the graveyard right away.
- `obit rm`, `obit rmdir` and `obit git-clean` take the common non-interactive arguments of `rm`, `rmdir` and `git clean` (`-r`, `-f`, `-d`, `-x` and the like) and bury what those commands would delete. `obit remove-item` takes one literal path, like `Remove-Item -LiteralPath`. Interactive or unusual options (`rm -i`, `rmdir -p`) are reported as errors, so rephrase with the plain arguments.
- When the delete guard is on, a deletion command is denied and the reason names the equivalent `obit` command. Run that command: it does the same deletion, restorably. Commands the guard does not need to handle run as usual.
- A Docker container you start for a task can get a lifespan too: `obit docker add <name-or-id> <lifespan>`. At expiry it is stopped (its writable layer stays), `obit resurrect <id>` starts it again, and it is removed only after the retention period. Volumes and images are left alone. Containers started with `--rm` remove themselves, so they are not registered.

## Bringing things back

- `obit graveyard` lists buried items with their numbers and how long each stays restorable; `obit graveyard --here` lists only those whose original path is in the current directory.
- When a tool call touches a buried path, Obituary adds a grave notice with the item's number. A notice for a path inside a buried directory refers to the whole directory.
- `obit resurrect <id>` puts an item back where it was. It never overwrites: if the original path is taken, the item comes back under a suffixed name, and the output says where.
- `obit resurrect --last` brings back everything the latest `obit bury` or `obit rm` buried, together. Inside an agent session it picks that session's latest deletion (Claude Code sessions are recognised automatically; `OBIT_SESSION_ID` names one explicitly), otherwise the latest deletion in the current Git project that recorded no session. From a plain terminal it picks the latest deletion in the current Git project. When nothing matches it says so, and `obit graveyard` shows the numbers.
- In `obit resurrect` and `obit purge`, a bare number (`5` or `#5`) is an ID; a file whose name is a number is written `./5` or as an absolute path.

## Decisions that belong to the user

- Nothing goes into Obituary by itself unless the user turns automatic registration on: what goes in is what you register (`obit mark`, `obit mktemp`, `obit bury`) and what the user registers from the Explorer context menu on Windows or with folder policies.
- Automatic registration is the user's setting (`[proposals] mode` in `config.toml`, or the window's Decisions page): `off` (the default), `tiered` (what an agent created in its session, the hook having seen the write, and the containers it starts for the project get a lifespan at once and are reported afterwards; the rest is proposed), `auto` (everything automatic goes in and is reported afterwards) or `ask` (everything is proposed first). `obit spare <id>` undoes a registration made without asking and `obit extend <id> <lifespan>` keeps it longer.
- Proposals: a proposal lists only what is safe to approve (uncommitted work never appears), and approved items stay restorable after burial. `obit proposals` lists pending proposals and what went in without asking. The user answers with `obit approve <id>` or `obit reject <id>`; describe the proposal, recommend approving it, and let them decide. An explicit `obit mark` or `obit mktemp` takes effect at once and is not a proposal.
- Project rules: a repository's `.obitrules` takes effect after the user reviews it and runs `obit trust`.
- Purging: `obit purge` deletes graveyard items permanently and is the user's call. `obit purge <id>` also lets the user abandon an interrupted resurrection that can no longer be verified.

## Facts worth knowing

- Files tracked by Git, and dependencies, build output and caches (`node_modules`, `dist`, `__pycache__` and the like), are never given a lifespan automatically, and an automatic lifespan is checked against Git again before burial.
- Burying a directory takes everything inside it. A directory that contains a `.git` repository needs `obit bury --force`; `obit rm -rf` buries it the way `rm -rf` would delete it.
- With `mode = "recycle"` in Obituary's configuration, buried and expired items go to the system Recycle Bin and are restored from there. `obit config` shows the mode in effect.
- `obit stats` shows how much has been buried, purged and resurrected; `obit doctor` checks the installation.
