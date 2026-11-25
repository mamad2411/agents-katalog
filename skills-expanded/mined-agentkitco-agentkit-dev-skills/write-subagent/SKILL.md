---
name: write-subagent
description: Draft a Claude Code subagent file in .claude/agents/ for one repeatable job, with a trigger-ready description, minimal tools and a fitting model. Use to create, fix or tune a subagent.
license: MIT
metadata:
  author: AgentKit Co
  version: "1.1"
---

# Write a Claude Code subagent

Goal: one Markdown file with YAML frontmatter that Claude Code loads, delegates to at the right moments, and that can only touch what its job needs.

## 1. Pin down the job (ask if unclear)

- One job per subagent: "run tests and report failures", not "help with code".
- When should Claude hand off to it? Name the trigger in plain words.
- Does it only read, or must it edit, run commands or browse?
- Scope: this project (`.claude/agents/`, commit it for the team) or every project for this user (`~/.claude/agents/`)? Project wins on a name clash.

Check `.claude/agents/` and `~/.claude/agents/` first (both are scanned recursively). If a subagent with the same `name` exists, edit it instead of adding a second.

## 2. Write the frontmatter

```markdown
---
name: test-runner
description: Runs the test suite and reports only failing tests with the relevant error lines. Use proactively whenever tests need to be run. Do not use for writing or fixing tests, or for lint and type checks.
tools: Bash, Read, Grep
model: haiku
---
```

Rules:

- **`name`**: lowercase with hyphens, unique. Identity comes from this field, not the filename. Never start it with `-` or put `:` in it.
- **`description`** (required): say *what* it does and *when* to use it. Add "Use proactively" only if Claude should delegate without being asked. End with a short "Do not use for ..." line naming the nearby jobs it should leave alone (often the work of a neighbouring subagent); it is the cheapest fix for a subagent that keeps grabbing the wrong tasks.
- **Tools, smallest set**: `tools` is an allowlist. Read-only jobs get `Read, Grep, Glob`. Add `Bash` only for commands, `Edit`/`Write` only for jobs that change files, `WebSearch, WebFetch` only for lookups. To keep everything except a few tools, use `disallowedTools` instead. Omitting both means it inherits all tools, so do that only on purpose.
- **`model`**: `haiku` for fast, mechanical work (search, test runs, summaries), `sonnet` for review and debugging, `opus` for deep audits, or `inherit` to match the main session. Leave it out to use the default.
- Field names are camelCase (`disallowedTools`, `maxTurns`). A misspelled field is ignored silently, so copy names exactly.

## 3. Write the body (the subagent's system prompt)

Keep it under about 40 lines:

1. One sentence on its role.
2. Numbered steps it follows every time.
3. What to return: a short, structured report (for example "failing test, file:line, one-line cause"), not a transcript. The main session only sees this report.
4. Limits: what it must not do (edit files, push, delete, install packages) and when to stop and report instead of guessing.

The subagent does not see your conversation. Put any context it always needs in the body or in `CLAUDE.md`.

## 4. Check it loads

1. Confirm the opening `---` is the very first line and the YAML parses.
2. If `claude plugin validate` is available, run it on the agents folder to catch parse errors; otherwise run `claude --debug` and look for the subagent in the log.
3. In a new session, ask "which subagents are available?" and confirm it is listed. (On current Claude Code versions `/agents` only prints a reminder to edit the files; it no longer lists them.)
4. Test it with an explicit ask ("use the test-runner subagent to ...") and then with a natural request that should trigger it. If it is never picked, make the `description` more specific about *when*. If it is picked for the wrong jobs, add or sharpen the "Do not use for ..." line.

Show the user the file and the test result. Do not commit unless asked.
