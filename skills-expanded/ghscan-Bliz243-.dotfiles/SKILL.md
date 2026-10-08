---
name: review-agent-instructions
description: Review recent Claude Code and Codex sessions for the current project and propose improvements to the global and project AGENTS.md files, plus cleanup of Claude's auto memory. Use when asked to review, audit, or improve agent instructions, AGENTS.md or CLAUDE.md files, or agent memory.
---

# Review agent instructions from session history

Find where recent sessions went wrong or needed repeated correction, and turn that into precise edits to the instruction files.

## Files in scope
- Global: `~/.dotfiles/agents/AGENTS.md`, shared by Claude Code and Codex. It lives in a public repo: no secrets, machine-specific values, or project-specific details.
- Project: `./AGENTS.md` is canonical. `CLAUDE.md` files are import shims; never add rules to them.
- Claude auto memory for the project: `~/.claude/projects/<project path with / and . replaced by ->/memory/`.

## Step 1: Extract sessions
From the project root, run the bundled script. It writes plain-text transcripts of the most recent Claude Code and Codex sessions for this project, without injected instructions or tool output:

```bash
node ~/.agents/skills/review-agent-instructions/scripts/extract-sessions.js "$PWD" "/tmp/agent-review-$(date +%s)" 15
```

## Step 2: Analyze
Compare each transcript against the global and project files. Batch large transcripts separately, and use parallel subagents if available. List:
1. Rules that exist but were violated: sharpen the wording, or enforce the rule with a hook, lint, or test if it must never break.
2. Corrections the user repeated that aren't written down: project-specific ones go in the project `AGENTS.md`; ones true for every project go in the global file.
3. Rules that are outdated, contradict another rule, or never mattered in practice.

Propose a rule only when a transcript shows it would have prevented a real mistake, and cite that transcript.

## Step 3: Review memory
Read the project's auto memory and flag:
- Rules or facts both tools need: move them to the project `AGENTS.md`.
- Completed-work logs, task status, and anything the code or git history already records: delete.
- Entries contradicted by the current code or instructions: fix or delete.

## Step 4: Report, then apply
Summarize as violated rules, additions (project and global), removals, and memory moves and deletions. Keep the global file tool-agnostic and under about 60 lines. Ask before editing, then edit the `AGENTS.md` files, never the `CLAUDE.md` shims.
