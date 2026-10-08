---
name: brain-share
description: Share a skill, agent, or rule with the team by copying it to the shared namespace
---


Share an artifact with the team by copying it to the shared namespace.

Usage: /brain-share <type> <name>
- type: 'skill', 'agent', or 'rule'
- name: the filename (e.g., 'my-skill.md' or 'important-rule.md')
- Use `/brain-share --list` to see what's currently shared

Arguments: $ARGUMENTS

## Steps

1. Parse arguments:
   ```bash
   ARGS=($ARGUMENTS)
   TYPE="${ARGS[0]:-}"
   NAME="${ARGS[1]:-}"

   # Handle --list flag
   if [ "$TYPE" = "--list" ] || [ "$TYPE" = "list" ]; then
     echo "Delegating to /brain-shared-list..."
     # The agent should invoke /brain-shared-list skill instead
     exit 0
   fi

   if [ -z "$TYPE" ] || [ -z "$NAME" ]; then
     echo "Usage: /brain-share <type> <name>"
     echo "       /brain-share --list"
     echo "Types: skill, agent, rule"
     echo "Example: /brain-share skill my-useful-tool.md"
     exit 1
   fi

   # Validate type
   case "$TYPE" in
     skill|agent|rule) ;;
     *) echo "ERROR: Type must be 'skill', 'agent', or 'rule'"; exit 1 ;;
   esac
   ```

2. Check if the artifact exists locally:
   ```bash
   source "${CLAUDE_PLUGIN_ROOT}/scripts/common.sh"
   
   case "$TYPE" in
     skill) SOURCE_FILE="${CLAUDE_DIR}/skills/${NAME}" ;;
     agent) SOURCE_FILE="${CLAUDE_DIR}/agents/${NAME}" ;;
     rule) SOURCE_FILE="${CLAUDE_DIR}/rules/${NAME}" ;;
   esac

   if [ ! -f "$SOURCE_FILE" ]; then
     echo "ERROR: $TYPE '$NAME' not found at: $SOURCE_FILE"
     echo ""
     echo "Available ${TYPE}s:"
     case "$TYPE" in
       skill) ls "${CLAUDE_DIR}/skills/" 2>/dev/null || echo "  (none)" ;;
       agent) ls "${CLAUDE_DIR}/agents/" 2>/dev/null || echo "  (none)" ;;
       rule) ls "${CLAUDE_DIR}/rules/" 2>/dev/null || echo "  (none)" ;;
     esac
     exit 1
   fi
   ```

3. **Ask the user for confirmation** before sharing:
   "Share $TYPE '$NAME' with all machines in the brain network? This will be visible to all machines that sync with this brain."
   Wait for user to confirm before proceeding.

4. Copy to shared namespace:
   ```bash
   # Create shared directory structure
   mkdir -p "${BRAIN_REPO}/shared/skills" "${BRAIN_REPO}/shared/agents" "${BRAIN_REPO}/shared/rules"

   case "$TYPE" in
     skill) TARGET_FILE="${BRAIN_REPO}/shared/skills/${NAME}" ;;
     agent) TARGET_FILE="${BRAIN_REPO}/shared/agents/${NAME}" ;;
     rule) TARGET_FILE="${BRAIN_REPO}/shared/rules/${NAME}" ;;
   esac

   # Copy the file
   cp "$SOURCE_FILE" "$TARGET_FILE"
   log_info "Copied $TYPE '$NAME' to shared namespace"

   # Show the content preview
   echo ""
   echo "Shared $TYPE content preview:"
   echo "---"
   head -20 "$TARGET_FILE"
   if [ $(wc -l < "$TARGET_FILE") -gt 20 ]; then
     echo "... (truncated, total $(wc -l < "$TARGET_FILE") lines)"
   fi
   echo "---"
   ```

5. Commit and push:
   ```bash
   cd "${BRAIN_REPO}"
   git add shared/
   if git diff --cached --quiet 2>/dev/null; then
     echo "No changes to commit (file may already be shared)."
   else
     git commit -m "Share $TYPE: $NAME (from $(hostname))"
     
     # Try to push
     if git push origin main 2>/dev/null; then
       echo ""
       echo "✓ $TYPE '$NAME' has been shared with the team!"
       echo "  Team members will receive it on their next brain sync."
     else
       echo ""
       echo "⚠ $TYPE shared locally, but failed to push to remote."
       echo "  Run /brain-sync to retry pushing to the team."
     fi
   fi
   ```

6. Show sharing info:
   ```bash
   echo ""
   echo "Shared artifact location: shared/$TYPE/$NAME"
   echo "Team members will see this $TYPE after their next sync."
   ```
