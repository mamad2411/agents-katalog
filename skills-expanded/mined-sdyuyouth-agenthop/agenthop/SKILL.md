---
name: agenthop
description: >-
  Let two agents on different machines exchange information. Use it when the user wants to pair, has received a pairing code, wants to talk with a contact by name, or runs /agenthop.
  When the agenthop_create / agenthop_join tools are available, use them; the whole flow lives in the tools.
  Only without those tools, start agenthop on the command line and keep that process running until the conversation ends. The conversation must stay visible to the user.
user-invocable: true
---

# agenthop

## First, check for the agenthop tools

If you can call `agenthop_create`, `agenthop_join` and the other agenthop tools, **use the tools and do not start the command line**. The tools cover the whole flow: nothing to write into any process's standard input, and no log to watch yourself. How to use them is under "Using the tools" below.

Only without these tools, use the way under "Using the command line". To give an agent these tools, see the end of "Install".

## Using the tools

- **Open a room**: `agenthop_create(background)` returns a pairing code. Hand the **whole** code to the user to pass on to the other side.
- **Join**: `agenthop_join(code)` returns the other side's task background. Check whether it matches your context: if it does, confirm with one line via `agenthop_say` and the channel opens; if not, ask the user and do not reply.
- **Wait for the other side**: `agenthop_wait`. It returns only when it is your turn (they said something, sent a file, confirmed, or said goodbye); if nothing came in time, call it again. What it returns includes their progress (`working`).
- **Reply**: when a line arrives, first send a receipt with `agenthop_working` (what you are doing, roughly how long), then start the work; when you have the answer, reply with `agenthop_say`, which may span several lines. `say` tells you right away whether it was delivered.
- **Send a file**: `agenthop_send_file(path)`, at most 512 KiB; its contents and name are encrypted. The other side keeps it on disk only if they passed `accept_files: true` when opening or joining; otherwise only the name is recorded.
- **Finish**: `agenthop_bye`, optionally with a parting line.

When the other side says several things at once, answer all of them, not just the first.

### Contacts: pair once, then find each other by name

- In every conversation the other side shows who it is. The result of `join`, and the `identity` line in `wait`, reads "Their identity: alice (contact, …)" or "not a contact, fingerprint xxxx-xxxx-xxxx-xxxx".
- If the user wants to reach this person directly later, save them with `agenthop_save_contact(name)`, during the conversation or just after it. **Both sides must save each other**, or invitations are not taken.
- After that, `agenthop_invite(name, background)` invites them directly, with no pairing code to pass on. Their agent must have agenthop running at that moment to receive it; if it does not, you are told so, and then you open a room with `agenthop_create` as usual and have the user pass the code on. Once it is delivered, use `agenthop_wait` to wait for them to join and confirm.
- With no conversation going, `agenthop_wait` waits for invitations from contacts. **When one arrives, tell the user first**, and call `agenthop_accept(from)` only once they agree; to turn it down, `agenthop_decline(from, reason)`, and the other side knows right away. If the user said beforehand to accept anyone who calls, you can accept right away. After accepting it works like `join`: read the background, and if it matches, confirm with one line.
- `agenthop_contacts` lists contacts and this machine's fingerprint; `agenthop_forget_contact(name)` deletes one.

Each tool result is the conversation itself, so the user sees it in the transcript. Opening and joining a room also give the path of the log file.

## Using the command line

Start `agenthop` with one tool call and keep that process running until the conversation ends. Read the other side's words from its standard output, and write yours into the same standard input, one line per message.

Every line this process writes is the conversation itself and must appear where the user can see it. Keeping a copy elsewhere is fine, but in the same reply tell the user the file's absolute path and how to view it (`tail -f <path>` on macOS and Linux, `Get-Content -Wait -Tail 30 <path>` in Windows PowerShell). There is one test: can the user see the conversation moving right now.

## Install

Without an `agenthop` command, download the file for this system from https://github.com/sdyuyouth/agenthop/releases/latest and install it once. `--skill-dir` is the directory where this agent keeps `SKILL.md`, and may be repeated.

macOS on Apple silicon:

```bash
chmod +x agenthop-macos-arm64
./agenthop-macos-arm64 install --skill-dir <skill directory>
```

On an Intel Mac the file is `agenthop-macos-x64`. Linux x64 uses `agenthop-linux-x64` and Linux ARM64 `agenthop-linux-arm64`, installed the same way as on macOS. On these four systems the command goes to `~/.local/bin/agenthop`; open a new terminal and run `agenthop`.

On 64-bit Windows, run this in PowerShell, without `chmod`. There is no Windows ARM build.

```powershell
.\agenthop-windows-x64.exe install --skill-dir <skill directory>
```

On Windows the command goes to `%LOCALAPPDATA%\agenthop\agenthop.exe`; open a new terminal and run `agenthop`.

`--skill-dir` is remembered. From then on `agenthop update` updates the program and SKILL.md together: it replaces the program, then writes the new SKILL.md back to every recorded directory, and prints which files it wrote.

Once installed, run `agenthop update` (`--check` only checks, `--force` reinstalls even at the same version). If it prints `SKILL.md was not updated with it`, the skill text was not written (this happens when coming from a version before v0.2.0); run the install command it gives once more.

`agenthop --version` shows the version, `agenthop help` the full usage.

Installing also prints how to plug agenthop in as MCP tools: one ready-made command for each agent it finds. `agenthop install --mcp <claude|grok|codex|cursor|gemini>` writes it into that agent's configuration for you. Once plugged in, the agent has the `agenthop_*` tools.

### Language

agenthop speaks English by default. `agenthop install --lang zh` switches the program, and this skill, to Chinese; `--lang en` switches back. `AGENTHOP_LANG=zh` does it for a single process. The state words and the log's layout are the same in both languages, and two sides need not use the same one.

## The conversation

Open a room. The text after it is this side's task background, sent to the other side as the hello:

```bash
agenthop "<background>"
```

The `waiting` line on standard output holds the pairing code; hand **that whole string** to the other side. They join in their own session:

```bash
agenthop <pairing code>
```

The pairing code ignores case and may be separated by spaces or hyphens, but must not be cut short: its last part is this conversation's key, and without it the other side cannot get in or read anything.

When `peer hello` appears on the joining side's standard output, the agent in that session checks whether the background matches its own context. If it does, it writes one line of confirmation into standard input, and the creating side then prints `peer confirm` and `local ready`. If not, ask the user in that session and write nothing to standard input.

After `ready`, every time the other side says something the same process writes another `peer say` line. Read it and write your reply into standard input. Once sent, a `local say` line follows: the record of what you just said.

Every line on standard input is the text to send, with no state word and no JSON. To send a file, write a line `/file <path>` (at most 512 KiB; its contents and name are encrypted).

### When it is your turn

Only these lines mean it is your turn: `peer hello`, `peer confirm`, `peer say`, `peer files`, `peer bye`.

`peer working` is the other side's progress while it works. **Do not take a turn for it**: it exists so you know you can wait. `peer identity` is who the other side is (a contact's name, or a fingerprint) and needs no answer either. Lines starting with `local` are your own record and need no answer.

The program has no switch to filter its output: standard output is always the whole record, because the process must stay visible to the user. To wake only on your turn, wait from the log's current end:

```bash
tail -n 0 -f <log path> | grep -m1 -E ' peer (say|bye|hello|confirm|files)( |$)'
```

`-n 0` starts at the end, without replaying lines already seen. The `( |$)` at the end matters: `peer bye` has no text after it, and without it you would never see the other side's goodbye.

After waking, read the log through once: the `peer working` progress lines are in it, and they help when deciding whether to ask a follow-up.

### Send a receipt first

The first thing to do on reading `peer say` is write one line of receipt, then start the work:

```
/working Got it, tracing how these three files call each other, about two or three minutes
```

On the other side it appears as `peer working Got it, tracing…`, not `peer say`, so it does not use up their turn.

- **Receipt first, then think.** A receipt held back and sent with the reply is no receipt: they arrive together.
- Say in the receipt what you understood the task to be. If you got it wrong, one line from the other side corrects it now; finding out after the work is a redo.
- On long work, write another `/working still running` in between, so the other side can tell thinking from gone.
- If you can answer right away, just answer; the reply is the receipt.
- The joining side's confirmation is the receipt for the `hello`; no separate receipt is needed before it.

When the other side says several things at once, **answer all of them together**, not just the first. The rest will not come up again, and the two sides drift apart.

## Finishing

Write a line `/bye` to end the conversation, optionally with a parting line: `/bye Thanks, that's all for today`. When the other side reads it, it says bye back; each side's record has a `local bye` and a `peer bye`, and then both processes exit.

On `peer bye` there is nothing to do, and nothing more to write to standard input: the program says bye back by itself and exits.

## What it says when something goes wrong

- `local reconnecting` / `local reconnected`: the connection dropped and the room is being brought back with the same pairing code; once it is back the conversation goes on, with no pairing again.
- `local undelivered <text>`: this line **did not reach the other side**. Do not treat it as answered. A line over 64 KiB is stopped before it goes and written here with its size; split it into several.
- `local throttled`: the relay takes only a few dozen lines a minute for one room, and this side is writing too fast. **Do not resend**: the queued lines go out by themselves in their original order, each showing `local say` as usual.
- `peer gone`: the other side is no longer there (its process exited, the network dropped, or the room sat idle for over ten minutes).
- `local expired`: nobody joined with this pairing code and the room has expired. Run `agenthop "<background>"` again for a new code.
- `peer refused`: this line did not enter the conversation and did not reach the disk. The reason is on the same line: the sender lacked the key from the pairing code, the same line arrived twice, or this session reached its limits (8 MiB in all, 2000 messages, 64 KiB per message).
- `peer files`: the other side sent a file. **By default only the name is recorded, not the file**; to keep files, add `--accept-files` to the starting command (`accept_files: true` with the tools), and then this line is the file's path.
- `peer other`: the other side sent a form this version does not know, most likely because the two versions differ. The text is recorded as it came, cut short; no answer needed.
- `local input-closed`: standard input was closed, so this side can only listen.

Ctrl-C also sends the bye before exiting.

## The log

**The first line after starting is the log's absolute path** (`local log <path>`); tell the user that path, with no need to work it out yourself.

A log is named by room and by end: the creating side's is `<room address>.create.log`, the joining side's `<room address>.join.log` (the room address is the pairing code without its key: the first four parts). Both are in `~/.agenthop/sessions/` (`%USERPROFILE%\.agenthop\sessions\` on Windows). Two ends on the same machine never write into the same file.

It holds the same as standard output, one line each:

```text
<time> <local|peer> <state> <text>
```

The states are `log`, `waiting`, `connected`, `identity`, `hello`, `confirm`, `ready`, `say`, `working`, `bye`, and from the section above `reconnecting`, `reconnected`, `undelivered`, `throttled`, `gone`, `expired`, `refused`, `files`, `other`, `input-closed`. `local` is this side and `peer` the other. The time is local time, with its UTC offset.

## Relay

The default is `https://agenthop.imatrix.tech`. To use another relay, pass `--relay URL` or set `AGENTHOP_RELAY`. If your own relay has a password, add `--pass <password>` on both sides, or set `AGENTHOP_PASS` (command-line arguments show up in `ps`; environment variables do not).

A room disappears after ten minutes without a message, so a pairing code must be used within ten minutes. If the connection drops midway, leave it: the program brings the room back with the same pairing code by itself.
