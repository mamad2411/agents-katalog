---
name: allow-defer
description: Parse a blocked permission prompt and save a suggested allow rule for later review via /suggestions. Non-interrupting capture.
---

# Suggest Allow Rule (Deferred)

**Execute mechanically.** Follow the steps; no need to weigh alternatives or deliberate.

Capture a blocked permission prompt as a **suggestion file** in `~/.claude/suggestions/`. Do NOT edit `settings.json` directly — the user reviews and applies suggestions in bulk later via `/suggestions`. Keep this flow fast and non-interrupting.

For immediate application to `settings.json`, use `/allow-now` instead.

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
5. **Ambiguous scope** — pick the most useful generalization without asking. Err on the side of slightly narrower rules; the user can broaden on review. Only ask if you genuinely cannot produce a sensible pattern.

## Process

1. Extract and generalize the rule.
2. Check for duplicates:
   - Read `~/.claude/settings.json` — if `permissions.allow` already contains the exact rule, tell the user it's already allowed and stop. Do not write a suggestion.
   - Read existing files in `~/.claude/suggestions/` — if a pending suggestion has the same rule, tell the user and stop.
3. Generate a filename: `allow-<slug>-<unix-timestamp>.md` where slug is a short kebab-case summary of the rule (e.g. `allow-bash-pwsh-1745481234.md`). Keep slug under ~30 chars.
4. Write the suggestion file (see format below) to `~/.claude/suggestions/`. Create the directory if it doesn't exist.
5. Report briefly in one line:

   > Suggestion saved: `Bash(...)` — review with `/suggestions`.

   **Do NOT** use `AskUserQuestion` or otherwise interrupt. The whole point is to defer.

## Suggestion file format

````markdown
---
type: allow
created: <ISO 8601 UTC timestamp>
source: /allow-defer
---

# Allow rule: `<rule>`

## Context

User invoked `/allow-defer` with: `<raw $ARGUMENTS>`

## Action on accept

Append to `permissions.allow` in `~/.claude/settings.json`:

```
<rule>
```
````

The frontmatter `type: allow` tells `/suggestions` how to apply the action. The body is human-readable so the user can review it raw if they want.
