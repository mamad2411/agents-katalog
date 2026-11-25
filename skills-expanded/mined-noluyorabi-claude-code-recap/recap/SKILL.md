---
name: recap
description: Show recent Claude Code sessions across all projects, so the user can re-enter work after a reboot or context switch. Lists per session the absolute project path, a short summary, where the session stopped, last activity, turn count, git branch, model, and a ready-to-paste resume command; can search sessions by what was said in them, flag projects with uncommitted or unpushed work, and re-open every session at once in new terminal tabs. Use when the user asks "what was I working on", "which projects did I touch recently", "where did I leave off", "list my recent sessions", "how do I get back into that session", "open all my sessions again", "which session did I fix X in", "where do I still have uncommitted work", or invokes /recap. Reads only local files; the default run is instant and offline.
license: MIT
metadata:
  version: "1.3.0"
  author: noluyorAbi
  source: https://github.com/noluyorAbi/claude-code-recap
---

# recap: re-entry radar for Claude Code sessions

One command, full overview of recent sessions across every project on this machine. Built for the post-reboot moment: which projects, what was each session about, and the exact command to jump back in.

## How to run it

Personal or project install (the skill directory is on disk next to this file):

```bash
python3 ~/.claude/skills/recap/recap.py [flags]
```

Plugin install (Claude Code exports the plugin root):

```bash
python3 "$CLAUDE_PLUGIN_ROOT/skills/recap/recap.py" [flags]
```

Nothing to install beyond Python 3 (stdlib only, no third-party packages).

| Flag | Meaning |
|------|---------|
| (none) | last 15 sessions, newest first, instant, no network |
| `--since 7d` | only sessions active in the window (`30m`, `24h`, `7d`, `2w`) |
| `--project foo` | filter by substring of the absolute project path; separators are interchangeable (`my_app`, `my-app`, `work/my_app`) |
| `--grep PATTERN` | only sessions whose conversation matches PATTERN (regex, case-insensitive); the matching excerpt replaces the `↳` line |
| `--dirty` | annotate each row with its project's uncommitted and unpushed counts (read-only git calls) |
| `--limit N` | max rows (default 15) |
| `--json` | machine-readable output with full session ids and resume commands |
| `--no-tail` | hide the `↳` line that says where each session stopped |
| `--smart` | real one-sentence summaries via ONE `claude -p` haiku call (network, ~10s) |
| `--pick` | choose a row interactively, then `cd` + `claude -r` into it directly |
| `--open` | open EVERY listed session in its own new terminal tab and resume it there |
| `--claude-flags "..."` | extra flags for each resumed `claude` (e.g. `"--chrome --dangerously-skip-permissions"`); also shown in the printed resume lines and `--json` |
| `--terminal NAME` | which terminal `--open` drives: `iTerm2`, `Terminal`, `tmux`, `wezterm`, `kitty`, `gnome-terminal`, `konsole` (default: auto-detected) |
| `--yes` / `-y` | skip the `--open` confirmation prompt (required when stdin is not a TTY) |
| `--dry-run` | with `--open`: print the tabs and commands, open nothing |
| `--color` | force ANSI colors when output is piped (e.g. inside Claude Code) |
| `--plain` | no ANSI at all (also honors NO_COLOR / FORCE_COLOR env) |

## Usage examples

```bash
# after a reboot: what was I doing?
python3 ~/.claude/skills/recap/recap.py

# everything in one repo this week
python3 ~/.claude/skills/recap/recap.py --since 7d --project my-repo

# which session did I solve this in?
python3 ~/.claude/skills/recap/recap.py --grep "connection pool" --limit 5

# where did I leave work uncommitted?
python3 ~/.claude/skills/recap/recap.py --dirty --since 7d

# jump straight back into a session
python3 ~/.claude/skills/recap/recap.py --pick

# re-open yesterday's whole working set in terminal tabs, browser enabled, no permission prompts
python3 ~/.claude/skills/recap/recap.py --since 24h --limit 12 \
  --open --yes --claude-flags "--chrome --dangerously-skip-permissions"

# preview first, open nothing
python3 ~/.claude/skills/recap/recap.py --open --dry-run

# feed into other tooling
python3 ~/.claude/skills/recap/recap.py --json --limit 50
```

## The `--open` flag

Restores a whole working set at once. It opens one new tab per listed session and types the resume command into it. Rules:

- The session recap itself runs in is skipped automatically (matched on `CLAUDE_CODE_SESSION_ID`), so it never re-opens itself.
- Sessions whose project directory no longer exists are skipped and reported, never opened.
- Scope comes from the normal filters, so `--limit` / `--since` / `--project` decide exactly which tabs appear. Check with `--dry-run` before committing.
- Without `--yes` it asks for confirmation; with piped stdin (Claude Code's Bash tool) it refuses to open unless `--yes` is passed.
- `--claude-flags` is passed through verbatim to every tab. `--dangerously-skip-permissions` disables all permission checks in each opened session; the script prints a warning before doing it.
- The terminal is auto-detected: tmux when running inside it (even on macOS), else iTerm2/Terminal on macOS via `osascript`, else wezterm, kitty, gnome-terminal or konsole. `--terminal NAME` forces one. Where none can be driven, `--open` says so and opens nothing; `--open --dry-run` needs no terminal and still prints the commands.
- Every opened tab outlives `claude`: quitting a resumed session leaves a shell in that project instead of closing the restored window.

## When Claude runs this skill

Run the script with Bash, ALWAYS with `--color` (tool output is piped, auto-detection would strip the colors; Claude Code renders ANSI). Add `--since`/`--project` if the user narrowed the question, then relay the table. Quote the resume command (`cd <path> && claude -r <id>`) for any session the user wants to re-enter. Only add `--smart` if the user explicitly asks for better summaries; it makes a network call.

Reach for `--grep` when the user is looking for a session by what happened in it ("where did I fix the connection pool"), not by when it ran. Reach for `--dirty` when the question is about unfinished work ("what did I leave half-done", "where do I still have uncommitted changes"); it runs read-only git commands, so it is safe but not instant.

Use `--open` only when the user explicitly asks to re-open or resume the sessions. Because the Bash tool pipes stdin, `--open` needs `--yes`; treat the user's request as the confirmation, and set the scope with `--limit`/`--since` so no unwanted session gets a tab. Pass `--claude-flags` only with flags the user named; state the permission-bypass warning in your reply whenever `--dangerously-skip-permissions` is among them.

## Data sources and guarantees

- `~/.claude/history.jsonl` is the fast index (prompt text, timestamp, project path, session id). `CLAUDE_CONFIG_DIR` is honored when set.
- `~/.claude/projects/<encoded>/<session>.jsonl` transcripts are parsed only for the displayed rows (title, branch, model, turn count). Project paths always come from the `cwd`/`project` fields, never decoded from folder names (that encoding is lossy). Because `claude -r` only finds a session from the directory it started in, recap resolves the path to the first recorded `cwd` whose encoding matches the transcript's folder, so a mid-session `cd` never produces an unresumable command; a session with no `cwd` at all borrows one from a sibling transcript.
- Summary preference: Claude Code's own `ai-title` line, else the first real user prompt, else the first slash command the session ran, else `(no prompt)`. A transcript's user role also holds what Claude Code injects into it, and none of it counts as a prompt: command blocks, local command output, the body of an invoked skill, hook text, task notifications, `!` bash runs and interrupt markers.
- The `↳` line is where the session stopped: Claude's last reply when the run finished, the unanswered prompt when it was interrupted, whichever came last. `--json` always carries it as `lastMessage` / `lastSpeaker`, so `--no-tail` only quiets the table.
- `--grep` searches the conversation. A transcript is rejected by a raw byte scan before it is parsed, using a word every match must contain, derived from the pattern only when that is provably safe (never across an alternation, a quantifier or whitespace).
- `--dirty` runs `git status --porcelain` and one `rev-list` per project directory, cached and only for the rows actually shown. Not-a-repository, no upstream and no git installed all yield the same non-answer: no counts on the row.
- `--smart` privacy: the only path that leaves the machine. It shells out to the local `claude` CLI once and sends, for the listed sessions only, each session's 8-character id prefix, its title (first 150 characters), and its first user prompt (first 300 characters). No file bodies, no transcript contents, no other sessions. If `claude` is not on PATH, `--smart` is skipped with a warning and the offline summaries are used.
- Turn count groups assistant streaming chunks by message id and is labeled approximate.
- Broken or partial JSONL lines are skipped, never fatal. Times shown in the local timezone.
- Display: day-grouped timeline (Today green, Yesterday amber), 14-day activity sparkline in the header, per-project colored dot (stable hash), four-level gray hierarchy with one accent color, per-session resume line indented with spaces only (safe to copy), and a small footer with a GitHub-star CTA and author link (clickable OSC 8 hyperlinks on supporting terminals). Falls back to plain text when piped or when NO_COLOR is set.
- Read-only: the tool never writes or deletes anything. It sees only sessions still on disk (Claude Code prunes old ones). `--open`, `--pick` and `--dirty` are the only side-effecting paths: `--open` drives a terminal, `--pick` `exec`s `claude -r` in the chosen directory, `--dirty` runs read-only git commands in the project directories. None of them writes or touches session data.

## Optional shell alias

```bash
alias recap='python3 ~/.claude/skills/recap/recap.py'
```
