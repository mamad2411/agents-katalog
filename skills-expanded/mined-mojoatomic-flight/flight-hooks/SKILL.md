---
name: flight-hooks
description: "Patterns for writing and modifying Flight calibration hooks (.claude/hooks/*.sh). Use when editing, creating, or reviewing hook infrastructure — stdin handling, exit codes, JSON parsing, and anti-patterns like heredocs in sourced functions."
user-invocable: false
---

# Flight Hooks Bash Skill

Load this skill before editing any hook infrastructure.

## NEVER

1. **Heredocs in sourced functions** — Do not use `cat <<EOF` or `<<EOF` in functions that may be sourced by scripts that consume stdin. The parent script's `INPUT=$(cat)` consumes stdin; heredocs in sourced functions will hang waiting for input that never comes.

   ```bash
   # BAD — will hang
   flight_banner() {
     cat >&2 <<EOF
   Banner text here
   EOF
   }

   # GOOD — use echo statements
   flight_banner() {
     echo "Banner text here" >&2
   }
   ```

2. **Assume stdin is available in sourced functions** — If a function is defined in a sourced file (like `lib/banner.sh`), it cannot read from stdin. The parent script already consumed it.

3. **Output to stdout for user messages** — CC captures stderr, not stdout. User-facing messages must go to stderr or they disappear.

4. **Unquoted variables in conditionals** — Always quote: `[[ -n "$VAR" ]]` not `[[ -n $VAR ]]`.

---

## MUST

1. **Consume stdin exactly once at script start**
   ```bash
   INPUT=$(cat)
   ```
   All subsequent parsing uses `$INPUT`. Never read stdin again.

2. **Parse JSON with jq, handle missing fields**
   ```bash
   FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty')
   ```
   The `// empty` prevents null from appearing in output.

3. **Output to stderr for CC visibility**
   ```bash
   echo "Message for Claude Code" >&2
   ```
   CC displays stderr from hooks. Stdout is captured but not shown.

4. **Use correct exit codes**
   - `exit 0` — allow the operation
   - `exit 2` — block with feedback (CC shows stderr)
   - Other codes — treated as hook errors

5. **Degrade ANSI colors gracefully**
   ```bash
   if [[ -t 2 ]] && [[ "${TERM:-}" != "dumb" ]]; then
     RED='\033[0;31m'
     BOLD='\033[1m'
     DIM='\033[2m'
     RESET='\033[0m'
   else
     RED=''
     BOLD=''
     DIM=''
     RESET=''
   fi
   ```

6. **Use $CLAUDE_PROJECT_DIR for project root**
   ```bash
   PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
   ```
   Defaults to current directory if unset.

7. **Start with strict mode**
   ```bash
   set -euo pipefail
   ```
   Exit on error, undefined variables, and pipe failures.

---

## SHOULD

1. **Source lib/banner.sh for consistent visuals**
   ```bash
   SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
   source "$SCRIPT_DIR/lib/banner.sh"
   ```

2. **Log significant events to signal.log**
   ```bash
   printf '[%s] EVENT %s detail:%s\n' \
       "$(date '+%Y-%m-%d %H:%M:%S')" "$FILE_PATH" "$DETAIL" \
       >> "$PROJECT_DIR/.claude/signal.log"
   ```

3. **Include structured questions for AI self-correction**
   ```
   PERCEPTION: What did you think this value/pattern was?
   REALITY:    What is it actually? (Read the source)
   PATTERN:    What pattern in this codebase would have told you?
   ```

4. **Filter by file type early**
   ```bash
   if ! echo "$FILE_PATH" | grep -qE '\.(ts|tsx|js|jsx)$'; then
     exit 0  # Not our concern
   fi
   ```

---

## Hook Types

| Hook | Fires | Purpose |
|------|-------|---------|
| PreToolUse | Before Edit/Write | Verify content before it reaches disk |
| PostToolUse | After Edit/Write | Log success, capture patterns |
| PostToolUseFailure | After rejection | Prompt learning from the correction |
| UserPromptSubmit | On each prompt | Inject context, detect complexity |

---

## Testing Hooks

Always test with timeout to catch hangs:
```bash
echo '{"tool_input":{"file_path":"test.ts","content":"..."}}' | \
  timeout 5 bash .claude/hooks/your-hook.sh 2>&1
echo "Exit: $?"
```

If it hangs, check for:
- Heredocs in sourced functions
- Additional stdin reads after `INPUT=$(cat)`
- Infinite loops in while-read constructs

---

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| `cat <<EOF` in function | Hangs if stdin consumed | Use `echo` statements |
| `while read line` on stdin | Stdin already consumed | Use `<<< "$VARIABLE"` |
| `echo $ERRORS` unquoted | Word splitting breaks output | `echo "$ERRORS"` |
| `exit 1` for blocks | CC may not display feedback | `exit 2` for blocks |
| Colors without fallback | Breaks in non-TTY contexts | Check `[[ -t 2 ]]` |
