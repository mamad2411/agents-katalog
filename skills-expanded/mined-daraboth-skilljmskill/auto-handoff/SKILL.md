---
name: auto-handoff
description: Hand the current session's work to a fresh agent session end to end. Writes a handoff file from what this session knows, starts the successor in a new Orca terminal tab with the same CLI, profile and agent flags, delivers the prompt, checks the successor's first reply, then stops. Works for Claude Code and Codex, for a main session or a looping team agent. Use when the user says "hand off", "handover", "start a fresh session", "pass this to a new agent", "take over", "my context is too big", or when this session's transcript has grown so large that a fresh session would serve the user better and the user agrees.
---

# Auto handoff

A handoff moves ownership. The new session does the work from now on; this session writes the
file, starts the successor, confirms it took over, and then does nothing more. The successor knows
only the file, its memory and its project instructions, so the file carries every fact that lives
only in this conversation.

## 1. Before writing

1. **Save durable lessons to memory first.** A rule the user taught you, a trap you hit, a
   convention: write it to memory now. Memory outlives every session; the handoff file holds only
   the state of the work in flight.
2. **Collect the live state, do not recall it.** For every repo you touched, run
   `git status -sb`, `git log --oneline -5`, `git stash list`, and `git rev-list --left-right --count @{u}...HEAD`.
   Note background jobs, `/loop` loops, cron or wake-up schedules this session started: they stop
   when this session stops, so the successor must restart the ones that still matter.
3. **Find your own launch.** Note the CLI (`claude` or `codex`), and for Claude the
   `--agent <name>` and `--model <model>` you were started with (your first user message, your
   agent definition, or the project's launch convention). The successor gets the same ones.
4. **Find your transcript.** Claude: `<config dir>/projects/<folder-key>/<session-id>.jsonl`.
   Codex: the newest file under `~/.codex/sessions/`. Put its path and size in the file so the
   successor can grep it for detail.

## 2. Write the file

Copy `references/template.md` and fill it. Rules:

- **Path.** Your scratchpad directory if your system prompt lists one, otherwise the OS temp
  folder (`$TMPDIR`, `%TEMP%`). Name: `handoff-<role>-<YYYY-MM-DD>.md`. Never inside a repo.
- **Quote the user's standing rules verbatim**, with the plain-words rule after each. A paraphrase
  loses the force of the original.
- **Reference, do not copy.** Commits by hash, PRs by number, plans and specs by absolute path.
  Do not repeat what memory or the project's CLAUDE.md / AGENTS.md already says.
- **Every claim checkable.** Hash, path, run id or ticket number next to each fact. Mark anything
  you could not verify as "unverified".
- **Separate "waiting on the user" from "open decisions".** The first are the user's actions; the
  second are questions the successor must ask, not decide.
- **No secrets.** No keys, passwords, tokens, `.env` values or personal data. Name where a secret
  lives, never its value.
- **End with one "First thing to do".** Usually: tell the user it has taken over and wait. For a
  loop agent: the exact command that restarts its loop.
- Aim for under 150 lines. A long file means you copied instead of referencing.

## 3. Start the successor

Two ways: with the [Orca](https://github.com/stablyai/orca) terminal app (fully automatic,
below), or by hand in any terminal (see **No Orca**). Orca is optional.

Run the bundled script from Git Bash (Windows) or any POSIX shell. It opens a new Orca tab in the
current worktree, starts the same CLI with the same profile, waits for it to be ready, sends the
prompt, and prints the successor's first reply.

```bash
bash ~/.claude/skills/auto-handoff/scripts/launch-successor.sh \
  --file "<absolute path to handoff file>" \
  --title "<role> handoff" \
  --flags "<same flags you were started with, e.g. --agent api --model sonnet>"
```

- `--cli codex` for a Codex successor. `--worktree <selector>` to open it in another Orca
  worktree. `--prompt "<text>"` to replace the default prompt.
- Claude successors inherit `CLAUDE_CONFIG_DIR` from your shell, so they sign in with your
  profile. A bare `claude` in a new tab may land on a profile that is not signed in.
- The script refuses to send when the new tab shows a login, folder-trust or "command not found"
  screen. It prints the screen; tell the user what to fix, or fix it in that tab, then send the
  prompt by hand with `orca terminal send`.
- Exit codes: 3 no Orca CLI, 4 tab not created, 5 successor not ready, 6 unclear send receipt.
  On 6, never resend blindly: read the tab first (`orca terminal read --terminal <handle>`).

### No Orca

Give the user one command to run in a new terminal in the same folder, with the profile prefix if
one is set:

```bash
CLAUDE_CONFIG_DIR=<your config dir> claude <flags> "Read the handoff file <path> in full, then tell me you have taken over."
```

For Codex: `codex "<same prompt>"`.

## 4. Confirm and stop

1. Read the successor's first reply in the script output. It must say it took over. If it asks
   for something the file should have held, answer it once with `orca terminal send`, and note the
   gap so the next handoff carries it.
2. Tell the user, in two lines: the new tab's title and handle, the handoff file path.
3. Stop. Make no further edits, commits, messages to other agents, or schedule changes. If the
   user writes to this session again, point them to the new tab.
4. Do not close your own tab: closing it kills this process mid-reply. The user closes it.

## Why it is shaped this way

- The prompt goes in through `orca terminal send` after the tab is idle, not as a CLI argument,
  because a fresh Claude tab can stop on a login or trust screen and swallow the prompt.
- Git Bash turns a leading `/` into a Windows path (`/loop` becomes `C:/Program Files/Git/loop`);
  the script exports `MSYS_NO_PATHCONV=1` and `MSYS2_ARG_CONV_EXCL='*'` before sending.
- A send receipt of `accepted: true` proves the keys arrived, not that a turn started. A tab made
  by `orca terminal create` is a plain shell to Orca, so it cannot report `turn_started`; the
  successor's screen, read after it goes idle, is the proof. Never resend on silence, so the
  successor never gets the prompt twice.
- `orca agent launch --agent claude --prompt` is not used because it starts Claude without your
  `CLAUDE_CONFIG_DIR`, which can land on a profile that is not signed in.
- Tested 2026-10-23: a Haiku successor in a new tab read a test handoff file and replied as told.
