---
name: ducter-operate
description: Work with a running Ducter (the user's self-hosted personal AI) from a terminal or as an agent - see its tasks and decisions, talk to the partner, start or follow a task, answer a decision, merge or undo results, connect a device. Use when the user asks you to check on Ducter, hand it work, follow a task, or act on what it reports.
---

# Operate Ducter

Ducter has one **partner** the user talks to; its work runs as **tasks** on AI agents (Claude
Code, Codex…). **On hand** is every task at a glance; **Needs you** are decisions waiting for the
user. The `ducter` CLI talks to the Ducter the user uses: the one on this machine
(`127.0.0.1:7777`), or a Ducter on a server when the Mac app (or `ducter connect`) connected the
command line to it. Check first: `ducter status --json` → `home` (`{kind: "local"}` or
`{kind: "remote", address, name}`); in human mode the first line says `→ <where>`. `--local`
forces this machine, `--home <address>` another Ducter once; `--port <n>` means a Ducter on this
machine on that port. `up`, `doctor`, `domain`, `service`, `worker` always act on this machine.
Prefer `--json`; exit code 0 means it worked.

If it says the command line isn't connected to the server yet, or the server no longer accepts
it, the fix is one line it prints: `ducter connect <address> --code <code>` with a code from
`ducter pair` on that server (ask the user for the code; never guess one).

## Look

```sh
ducter status --json        # On hand: tasks (title, state, place), open decisions with their ids
ducter devices --json       # connected devices and workers ("awake")
ducter tail                 # follow the conversation (Ctrl-C stops); ducter tail <part of a title> follows one task
ducter tail --json          # the same, one JSON event per line
```

`ducter status` exits non-zero with "Ducter isn't running on port 7777" when it's down: see
the ducter-troubleshoot skill.

## Talk and hand off work

```sh
ducter say "What's left on the release?" --json            # waits for the partner's reply (default 300 s; --timeout)
ducter task "Fix the flaky compaction test" --json         # a task with these exact words as its brief, in the repo you're in
ducter task "…" --repo ~/dev/app --agent codex --base main # elsewhere; who does it; what it starts from
ducter open <part of a title>                              # show that task in the Mac app
```

`say` returns `{replies, decisions, settled}`; a decision in `decisions` waits for the user.
`task` returns the new task's card (`taskId`); follow it with `ducter tail <taskId>`.

## Act on results

```sh
ducter answer <decision id or part of its question> go    # go | hold | "your words"
ducter merge <part of a task's title>                     # merge a finished task's branch into its base
ducter undo <part of a task's title>                      # a folder task: put the folder back as it was
```

## Connect a device

`ducter pair --json` → `{code, address, link, command}`: a code for one device, once, for 10
minutes; run it again for each next device (in the Mac app: Devices › Add a device › To talk with Ducter
/ 设备 › 加一台设备 › 用它和 Ducter 说话). The user
opens `link` on a phone or pastes it into the Mac app; another computer runs `command` to do
tasks for this Ducter. `reachable: false` means no address from outside yet: `tailnet` names
the machine when it is in a Tailscale network (then `ducter tailscale`), and `steps` lists the
ways in order; see the ducter-deploy skill. With a `.ts.net` address the phone or computer needs
the Tailscale app on, in the same tailnet. `ducter reach --json` lists every address the home
has. Following a server, `pair --json` also carries `connect`:
the line another computer's command line runs. `ducter devices disconnect` works only on the
machine Ducter runs on.

A task started with `ducter task` while following a server has no folder unless `--repo` names
one, and that folder must be on a computer that does tasks for it.

## Keep it up to date

`ducter update --check --json` says each device's version, the latest, and `available`. When
the user wants it updated: `ducter update --yes` (this machine) or `ducter update --all --yes`
(everything behind: the home, then the computers doing tasks for it, then their AI agents, each
agent once no task uses it; the home keeps the plan through its own restart). Ducter restarts
once; tasks pause and carry on. Exit code 1 with `reason` (and `rolledBack: true`) means it stayed on, or went back to, the
version it had. Don't update on your own initiative while tasks are mid-merge or the user is
in the middle of something.

The AI agents themselves (Codex, Claude Code, pi, DeepSeek Harness) have their own versions:
`ducter update --agents --check --json` gives `{agents:[{device, harness, version, how, latest,
available, standing, latestVerified}]}`. `how` is how that copy was installed (`npm`, `brew`,
`installer`, `app`, `ducter`, `unknown`); only `npm`, `brew` and `installer` can be updated from
Ducter. `standing` other than `verified` means Ducter hasn't checked that version yet: say so
plainly, it is not an error. `ducter update --agents --yes` updates the ones behind (`--all`
for every computer), each once nothing is running on it; it never touches an app's copy. Exit
code 1 with `reason` (and `rolledBack: true`) means it stayed on, or went back to, its old version.

## Browsing on a server

```sh
ducter ability add browser        # Ducter installs its own headless Chrome; tasks can browse
ducter browser check --json       # start it, open example.com, quit: {ok, browser: {device, name, version, profile}, ms}
ducter browser sites --json       # the sites the user signed into in Ducter's browser
ducter browser signout <site>     # forget one; `ducter browser clear` forgets all (ask first)
```

A task that needs a sign-in asks with a card "Sign in to <site>". Only the user answers it, by
signing in themselves in the app's live view and tapping Done. Never answer it with `ducter
answer … go`: the task would carry on not signed in.

## Safe defaults

- **Never answer Go for the user** on anything irreversible or outward (merge to main, push,
  send mail, delete, pay, publish). Show the question, its default and what Go does; let the
  user decide. Hold or a reply that asks a question is fine when unsure.
- `merge` and `undo` change the user's repo or folder: run them only when the user asked.
- Don't start tasks the user didn't ask for. Don't paste pair codes, tokens or keys anywhere
  but to the user.
- Words to the partner are the user's voice: say clearly when a message is from you, the agent.
