---
name: allow-now
description: Parse a blocked permission prompt and immediately append it to ~/.claude/settings.json permissions.allow. Use when you want the rule applied right now, not deferred.
---

# Apply Allow Rule (Immediate)

**Execute mechanically.** Follow the steps; no need to weigh alternatives or deliberate.

Append a permission rule to `permissions.allow` in `~/.claude/settings.json` **right now**. This is the interrupting counterpart to `/allow-defer` — use when you've decided the rule and want it active immediately.

For deferred, batch-reviewed capture, use `/allow-defer` instead.

Input: `$ARGUMENTS` — whatever the user pastes. Could be any of these formats:

- Full prompt text: `Do you want to make this edit to settings.json?`
- Tool call format: `Bash(wt new-tab --tabColor "#1e3a5f" ...)`
- Raw command: `wt new-tab --tabColor "#1e3a5f" -d ...`
- Tool + path: `Write(.vscode/settings.json)`
- Description text: `Yes, allow reading from .claude/ during this session`

If empty, prompt the user to paste the blocked action via `AskUserQuestion` (free-text). Then continue.

## Extracting the rule

Parse `$ARGUMENTS` to identify the **tool type** and **pattern**:

1. **Already in rule format** (e.g., `Bash(wt *)`, `Write(*/.vscode/*)`) — use as-is.
2. **Tool call format** (e.g., `Bash(wt new-tab --tabColor ...)`) — extract the tool and command, generalize.
3. **Mentions a tool action** (e.g., "edit to settings.json", "reading from .claude/") — map to the correct tool:
   - "edit" → `Edit(<path-pattern>)`
   - "read/reading" → `Read(<path-pattern>)`
   - "write/writing" → `Write(<path-pattern>)`
   - Generalize paths with `*` wildcards (e.g., `.claude/` → `*/.claude/**`).
4. **Raw shell command** — wrap in `Bash(...)`:
   - Simple: `Bash(<cmd> *)`.
   - With pipes: `Bash(<cmd> * | *)`.
   - With chaining: `Bash(<cmd> * && *)`.
5. **Ambiguous scope** — pick the most useful generalization without asking. Err on the side of slightly narrower rules; the user can broaden later. Only ask if you genuinely cannot produce a sensible pattern.

## Process

1. Extract and generalize the rule.
2. Read `~/.claude/settings.json`.
3. **Duplicate check**: if `permissions.allow` already contains the exact rule string, tell the user it's already allowed and stop. Do not edit.
4. **Apply**: use `Edit` to append the rule to the `permissions.allow` array. Match the file's existing indentation and quoting style exactly (the JSON in `~/.claude/settings.json` uses an unusual indentation — preserve it).
5. Report in one line:

   > Added to `~/.claude/settings.json`: `<rule>`

6. **Promote any matching pending suggestion**: if a file in `~/.claude/suggestions/` has the same rule under `type: allow`, delete it (the rule is now applied — no need to review it later). Mention briefly: "Cleared matching pending suggestion."

## Notes

- Do NOT prompt the user to confirm. They invoked `/allow-now` precisely because they've already decided. The duplicate check is the only stop condition.
- If `Edit` fails (e.g. JSON shape changed), report the failure and leave the file untouched. Do not retry blindly.
