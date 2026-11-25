---
type: summary
source: 01_Raw/github/anthropics/claude-code/plugins/hookify/skills/writing-rules/SKILL.md
title: "Writing Hookify Rules (hookify plugin skill)"
summarized_at: 2026-05-05
entities_referenced: [Hooks, Skill, Plugin]
concepts_referenced: []
---

Skill that teaches Claude how to author hookify rule files. Hookify is a plugin that lets users define watcher rules in markdown with YAML frontmatter at `.claude/hookify.{rule-name}.local.md`. Rules are read dynamically — changes apply on next tool use; no restart needed.

**Rule schema (frontmatter)**:
- `name` (required): kebab-case, action-oriented (`warn-dangerous-rm`, `block-console-log`).
- `enabled` (required): bool to toggle without deleting.
- `event` (required): `bash` / `file` / `stop` / `prompt` / `all`.
- `action` (optional): `warn` (default — allow + show message) or `block` (PreToolUse stops the call, or Stop event blocks session-stop).
- `pattern` (simple): Python regex matched against `command` (bash event) or `new_text` (file event).

**Advanced multi-condition format** uses `conditions` list — each entry has `field` + `operator` + `pattern`. Fields: bash → `command`; file → `file_path`/`new_text`/`old_text`/`content`; prompt → `user_prompt`. Operators: `regex_match`, `contains`, `equals`, `not_contains`, `starts_with`, `ends_with`. ALL conditions must match.

Example multi-condition rule warning when API_KEY is added to a `.env` file:
```yaml
event: file
conditions:
  - {field: file_path, operator: regex_match, pattern: \.env$}
  - {field: new_text, operator: contains, pattern: API_KEY}
```

**Body**: shown to Claude on trigger. Use formatted markdown — explain detection, why it matters, alternatives.

**Event-specific patterns**:
- bash dangerous: `rm\s+-rf`, `dd\s+if=`, `mkfs`, `sudo\s+`, `chmod\s+777`.
- file: `console\.log\(`, `eval\(`, `innerHTML\s*=`, sensitive paths `\.env$`/`\.pem$`, generated dirs.
- stop: enforce checklist (tests run, build succeeded, docs updated).
- prompt: production deploy reminders.

**Pattern tips**:
- YAML quoted strings need double backslashes (`"\\s"`); unquoted works (`pattern: \s`). **Recommendation: unquoted**.
- Test via `python3 -c "import re; print(re.search(r'pattern','test'))"` or regex101.com (Python flavor).
- Avoid too-broad (`log` → matches "login"/"dialog") and too-specific (`rm -rf /tmp` → exact path).

File location: `.claude/hookify.{descriptive-name}.local.md`. Add `.claude/*.local.md` to `.gitignore`.

Examples folder bundled with the plugin: `dangerous-rm.local.md`, `console-log-warning.local.md`, `sensitive-files-warning.local.md`.
