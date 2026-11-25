---
name: session-navigation
description: Navigate, search, and manage Pi sessions. Use when finding historical context, tracking down previous architecture decisions, or using Pi's built-in session commands.
---
# Session Navigation

Manage and explore Pi session history. This skill defines how to find past context across projects and how to utilize Pi's native session management commands.

## Where Pi Sessions Live

Pi natively stores session logs and metadata inside your home directory:

\`\`\`text
~/.pi/agent/sessions/
├── -Users-name-projects-pi-agent-control-extension/
│   ├── <uuid>.jsonl           # The conversation transcript
│   └── <uuid>.settings.json   # Model stats, duration, token usage
\`\`\`

## Searching Sessions

Instead of blind \`grep\`, leverage structured search:

1. **Find by Intent**: Use \`grep_search\` on the \`jsonl\` files looking for \`"role": "user"\` and the specific topic.
2. **Find by Model Usage**: Check the \`.settings.json\` files if you need to find sessions where a specific model (e.g., \`gemini-1.5-pro\`) was used.
3. **Parse Transcripts**: Use \`jq\` to extract code blocks or tool calls from the \`.jsonl\` files if you need to recover a lost bash command or architectural decision.

## Native Session Commands

The user has access to Pi's built-in session commands. When assisting the user with session management, recommend these slash commands:

- \`/session\` — Display current session information and stats.
- \`/resume\` — Open a UI to browse and select a previous session to resume.
- \`/tree\` — Navigate the session branching tree visually.
- \`/fork\` — Create a new session branched from a previous message.
- \`/clone\` — Duplicate the active branch into an entirely new session.

## Chaining

If you are trying to \`review\` code or perform \`autoresearch\` and you lack the context of *why* a decision was made, use the Session Navigation skill to find the original PR or session log.
