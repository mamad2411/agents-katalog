---
name: swarm-eject
description: Disconnect a project from SwarmVault and choose what happens to its knowledge — keep it, export it into the repo, or delete it. Use when the user wants to stop using SwarmVault here, remove the vault wiring, uninstall the framework from a project, offboard or archive a project, or delete a project's vault data.
---

# swarm-eject — leaving cleanly

Ejecting is not `rm -rf`. A project is wired in six places, and a partial removal leaves the
user worse off than never installing: a marker with no registry entry, instruction files
still pointing agents at a vault that no longer has the project, hooks firing into nothing.

The `eject` command does the work; this skill runs the conversation.

## 1. Ask which exit they want

Lead with the recommendation. Most people asking this want **unwire**, not deletion.

| mode | what happens to the knowledge | reversible |
|---|---|---|
| **unwire** *(default, recommend first)* | stays in the vault; the project just stops being wired | yes — `register` brings it back |
| **export** | copied into the repo at `docs/swarmvault-archive/`, then removed from the vault | via those files |
| **purge** | deleted | only from the backup |

If they say something like "remove SwarmVault from this project," that is **unwire** unless
they explicitly say delete. Ask before assuming otherwise.

## 2. Show the inventory before doing anything

The command's default is a dry run, so run it plainly and read the output back:

```bash
swarmvault.py eject --project <P> --mode unwire|export|purge
```

It prints what leaves and what stays: note counts per vault folder, total size, the exact
instruction files and hooks to be unwired, and — for export and purge — every inbound
`[[wikilink]]` from other projects that would go dead. Surface the orphan warning to the
user; it is the one consequence they cannot see coming.

## 3. Apply

```bash
swarmvault.py eject --project <P> --mode <mode> --apply [--backup PATH]
```

- **purge** asks for the project name typed back. Don't work around that prompt; if the
  session is non-interactive, tell the user and let *them* pass `--confirm-name <P>`.
- A backup tarball is written outside the vault before any deletion. `--no-backup` exists;
  don't reach for it, and never pass it on the user's behalf.
- Report the printed log back rather than summarising it as "done."

## Rules

- **Live work blocks the eject.** Open ticket claims or a running supervisor cause a refusal
  listing what's holding it. Release the claims or `supervisor stop` first, and say why —
  never present the refusal as a bug.
- **The repo is not vault property.** `docs/SRS.md`, `docs/specs/`, source, and git history
  are never touched at any level. If the user actually wants their SRS deleted, that's a
  normal file operation they ask for separately.
- **Global instruction files stay.** They are shared with every other project; only this
  project's own files get unwired.
- Idempotent — a half-finished eject completes on a re-run, and `doctor` names the state.
- After unwire, `swarm-flow` and the phase skills no longer apply here. Say so, in one line.

## Undo

Unwire is reversible while the vault content is intact:

```bash
swarmvault.py register --name <P> --path <path>   # then: wire --platforms <list>
```

Export and purge are only reversible from the backup tarball. Say that out loud before
applying either.

---
*The reverse of swarm-init and FR-06's `wire`; the safety protocol follows the vault's
own destructive-action stance (FR-25).*
