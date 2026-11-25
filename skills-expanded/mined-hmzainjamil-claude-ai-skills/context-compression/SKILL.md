---
name: context-compression
description: "Compress conversation history when context fills up. Use anchored iterative summarization to preserve file changes, decisions, and session intent without losing critical details."
risk: safe
source: community
---

# context-compression

When context window is filling up, compress history:

**Method (anchored iterative summarization):**
1. Summarize only the NEW portion that's being truncated
2. Merge with existing summary — don't regenerate from scratch
3. Preserve these sections explicitly:
   - Session Intent (what user is trying to accomplish)
   - Files Modified (path + what changed)
   - Decisions Made (key choices and why)
   - Current State (test status, errors, blockers)
   - Next Steps (what remains)

**Key rule:** Structure forces preservation. Use explicit sections as checklists.

**Trigger when:** conversation > 50k tokens, or `/compact` requested, or context warning appears.

Full docs: ~/.claude/skills-docs/context-compression-FULL.md
