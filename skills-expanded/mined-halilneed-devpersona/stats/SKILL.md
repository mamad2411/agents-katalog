---
name: stats
description: Show quick numeric statistics about local coding-agent usage — sessions, prompts, tool calls, error counts, languages, top commands, and active hours per project, across Claude Code, Codex CLI and Gemini CLI. Use when the user asks how much they have used Claude Code or another coding agent, asks for usage stats or numbers, says "show my stats", "istatistiklerimi göster", "ne kadar kullanmışım", or runs /devpersona:stats. Numbers only, no interpretation — for the character profile use devpersona:analyze.
---

# Quick stats

Show the numbers, nothing else. All local.

**Language rule: respond in the language the user is speaking with you.**

1. Run:
   ```
   node "${CLAUDE_PLUGIN_ROOT}/scripts/scan.mjs" --md
   ```
   Add `--lang tr` when the user is speaking Turkish.
2. Present the report as-is (it is already Markdown). You may bold one or two
   genuinely notable numbers, but do not editorialize beyond that.
3. If `node` is missing, tell the user Node.js 18+ is required.
4. Close with one line: `/devpersona:analyze` builds the full character profile
   from these numbers.
