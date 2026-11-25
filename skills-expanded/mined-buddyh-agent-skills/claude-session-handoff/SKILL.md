---
name: claude-session-handoff
description: Recover working context from a prior Claude Code session by reading its JSONL conversation log and turning it into a clean handoff for Codex or another agent. Use when the user wants Codex to continue where Claude left off in the same repo, asks you to get up to speed on previous work, wants to resume a Claude thread after an interruption or outage, or needs help finding and summarizing the relevant file in ~/.claude/projects/.
---

# Claude Session Handoff

Recover the state of a prior Claude Code session, then confirm what actually exists in the current workspace before continuing.

## Workflow

### 1. Find the right session

Default to the current project path unless the user gives a specific JSONL file.

For the common handoff case, do not search every Claude transcript first. Bias toward the current repo, the most recent top-level session, and recent activity.

Run the helper script:

```bash
python3 scripts/claude_session_handoff.py --project-path "$PWD"
```

Useful variants:

```bash
python3 scripts/claude_session_handoff.py --project-path "$PWD" --list
python3 scripts/claude_session_handoff.py --project-path "$PWD" --date YYYY-MM-DD
python3 scripts/claude_session_handoff.py --session /path/to/session.jsonl
python3 scripts/claude_session_handoff.py --recent 10
python3 scripts/claude_session_handoff.py --project-path "$PWD" --date YYYY-MM-DD --contains "anchor phrase" --from-match
```

Use these defaults:

- Start with the current repo and the newest top-level session.
- If the user implies "today", resolve that to the exact local date and pass `--date YYYY-MM-DD`.
- Read the last meaningful turns first. Do not read the entire transcript by default.
- Use `--list` when multiple Claude sessions exist for the same project and you want the candidate set before choosing one.
- Use `--recent` when the repo moved and the stored `cwd` no longer matches the current path.

### 2. Read only the meaningful turns

The helper script already filters the noisy parts, but keep these rules in mind:

- Ignore `subagents/` files unless the user explicitly wants delegated-session context.
- Ignore local-command pseudo-messages such as `<local-command-caveat>`, `<command-name>`, and `<local-command-stdout>`.
- Ignore assistant messages that are only `[thinking]` or other non-user-visible placeholders.
- Treat images as context markers, not text that needs verbatim transcription.

Default to the most recent meaningful turns only. Large transcripts should be narrowed before you read deeply.

If the session is large and the user wants a specific earlier point, ask for one anchor only:

- a distinctive phrase
- a short quoted line
- an approximate time

Prefer phrase matching over line numbers. Use `--contains "anchor phrase" --from-match` to jump to the relevant point without reading the full transcript.

### 3. Reconstruct the handoff

Summarize the session in this order:

1. The user's original goal
2. The options, decisions, or constraints already discussed
3. What actually happened in the session
4. What did not happen yet
5. The exact next step

Call out failures explicitly. If the session ended on an API error, tool error, overload, or interrupted command, say so instead of implying the work completed.

### 4. Verify the workspace separately

A Claude session log tells you conversation state, not code state. Confirm the actual workspace before continuing:

- Check whether the repo exists and whether it is a git repository
- Inspect the file tree with `ls` or `rg --files`
- Run `git status --short` when git is present
- Read the touched files or run targeted verification when the session claims code was written

If the workspace is empty or unchanged, say that explicitly. Do not infer implementation from discussion alone.

For interrupted-session recovery, assume the last discussed change may not have landed until you verify it in the workspace.

### 5. Report back concisely

Your handoff should usually include:

- The selected session file
- Whether the prior session was exploratory or implementation-focused
- Whether any code or files exist in the current workspace
- The unresolved next step

If you used an anchor phrase, also include the matched timestamp and make clear that the summary starts from that point rather than from the beginning of the session.

## Resources

### scripts/

- `claude_session_handoff.py`: Find relevant Claude Code session files, filter meaningful user and assistant turns, and print a compact handoff-oriented summary
