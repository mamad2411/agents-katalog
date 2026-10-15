---
name: brain-shared-list
description: List all shared skills, agents, and rules in the brain network.
---


The user wants to see all shared artifacts in the brain network.

## Steps

1. Check if brain is initialized:
   ```bash
   source "${CLAUDE_PLUGIN_ROOT}/scripts/common.sh"
   if ! is_initialized; then
     echo "Brain not initialized. Run /brain-init first."
     exit 1
   fi
   ```

2. List shared artifacts:
   ```bash
   BRAIN_REPO="${HOME}/.claude/brain-repo"
   SHARED_DIR="${BRAIN_REPO}/shared"

   if [ ! -d "$SHARED_DIR" ]; then
     echo "No shared artifacts yet. Use /brain-share to share skills, agents, or rules."
     exit 0
   fi

   echo "## Shared Artifacts"
   echo ""
   echo "| Type | Name | Shared By | Date |"
   echo "|------|------|-----------|------|"

   found=false
   for type in skills agents rules; do
     if [ -d "${SHARED_DIR}/${type}" ]; then
       for file in "${SHARED_DIR}/${type}"/*; do
         if [ -f "$file" ]; then
           found=true
           name=$(basename "$file")
           # Get git log info for this file
           info=$(cd "$BRAIN_REPO" && git log --format="%an|%ad" --date=short -1 -- "shared/${type}/${name}" 2>/dev/null || echo "unknown|unknown")
           author=$(echo "$info" | cut -d'|' -f1)
           date=$(echo "$info" | cut -d'|' -f2)
           echo "| ${type%s} | ${name} | ${author} | ${date} |"
         fi
       done
     fi
   done

   if ! $found; then
     echo "| — | No shared artifacts yet | — | — |"
   fi

   echo ""
   echo "Use /brain-share <type> <name> to share more artifacts."
   ```
