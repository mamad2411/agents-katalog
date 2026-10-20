---
description: Query the OS for a topic. Say "find the file about [topic]" or "search my OS for [topic]" (or run /founder-os:query <question>). Three modes (index, timeline, full) for progressive disclosure. Read-only.
argument-hint: <question> | --mode timeline --anchor <slug> | --mode full --ids <id1,id2>
allowed-tools: ["Read", "Bash"]
---

# Founder OS query

Run the query skill at `skills/query/SKILL.md` end to end.

## Procedure

1. If `$ARGUMENTS` is empty, reply `What should I query? Re-run as /founder-os:query <question>.` and stop.
2. If `core/identity.md` does not exist, reply `Founder OS not set up here. Say "set up Founder OS" first.` and stop.
3. If `skills/query/SKILL.md` is missing, reply `Query skill not found at skills/query/SKILL.md. Restarting Claude Code fixes this most of the time, because it reloads what is installed. If it happens again after a restart, say "update Founder OS".` and stop.
4. If `scripts/query.py` exists, invoke it via the **Bash** tool using the `env` form below so user input is never interpolated into a shell command line. The user's `$ARGUMENTS` may contain `;`, `|`, backticks, or `$(...)` and the shell would execute them if pasted verbatim.

   **Plain question (no `--` flags in `$ARGUMENTS`):** pass the question as one argument via an env var. Substitute the placeholder `__QUESTION__` literally with the user's argument string (do not escape, do not quote - the env var carries it intact):

   ```bash
   FOUNDER_OS_Q='__QUESTION__' python scripts/query.py "$FOUNDER_OS_Q"
   ```

   **Argument string contains flags (`--mode`, `--ids`, `--anchor`, `--root`):** parse the user's argument string into individual tokens yourself (split on whitespace), then call `python scripts/query.py` with each token as a separate Bash tool argument. Do not concatenate them into a single command-line string. Reject any token whose first character is not in `[A-Za-z0-9_/.-]` or that contains `;`, `|`, `&`, backticks, `$(`, or `>` - reply `Refusing to forward potentially unsafe argument token: <token>` and stop.

   If neither form fits, stop and reply: `Could not parse arguments safely. Re-run as /founder-os:query "<your question>" or with explicit flags.`

The underlying script also accepts `--root <path>` for direct CLI use, for example `python scripts/query.py --root /path/to/archive "outreach stalled"`.

5. Print stdout verbatim. If the script exits non-zero, print stderr and stop.
6. If the script is missing, follow the manual procedure in the skill file.

## Forms

- `/founder-os:query <question>` - default `index` mode. Returns ~10 candidate nodes with IDs.
- `/founder-os:query --mode timeline --anchor <slug-or-id>` - returns entries within 7 days either side of the anchor, ordered chronologically.
- `/founder-os:query --mode full --ids <id1,id2,...>` - returns full bodies for the listed IDs.

Examples:

- `/founder-os:query outreach stalled`
- `/founder-os:query --mode timeline --anchor brain/flags.md`
- `/founder-os:query --mode timeline --anchor log-2026-05-07-001`
- `/founder-os:query --mode full --ids log-2026-05-07-001,log-2026-05-07-002`

## Progressive Flow

Recommended for any non-trivial question:

1. Start with `index` to see candidate nodes.
2. Pick one and run `timeline` anchored on it for surrounding context.
3. Pull specific IDs with `full` to read bodies end to end.

## Rules

- Read-only.
- No external dependencies.
- No em dashes or en dashes.
- No banned words.
