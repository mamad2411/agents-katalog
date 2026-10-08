---
name: spec-exploration
description:
  Sub-skill of /spec-session. Phase 0.75 mandatory codebase exploration. Ensures
  agents verify actual code with Read/Grep/Glob tools before any analysis rounds
  begin.
---

# Spec Exploration Skill

Ensures agents explore actual code before analysis. Prevents specs built on
assumptions rather than reality.

**Called by**: `/spec-session` Phase 0.75 (mandatory, before analysis rounds)
**Can also run standalone**: Yes — to re-run exploration if initial session was
invalid

## Why This Phase Exists

Previous spec sessions had agents receiving context summaries but never
verifying them by reading actual files. This led to:

- Analysis based on assumptions, not reality
- Missing implementation details
- Incorrect understanding of existing code
- Proposals that ignored existing patterns

## Exploration Requirements

Each agent MUST:

1. **Use Read tool** to examine key files (at least 2-3 files)
2. **Use Grep tool** to search for patterns mentioned in context
3. **Use Glob tool** to discover related files
4. **Cite specific files and line numbers** in their analysis

## Spawning Note

Exploration agents need tools (Read, Grep, Glob), not inter-agent chat. **Always
use subagents** regardless of agent mode — use `subagent_type: 'Explore'`.

## Verification Checklist

Before moving to ANALYSIS round, verify:

- [ ] Each agent has called Read tool at least 2 times
- [ ] Agents cited specific file paths in their responses
- [ ] Agents referenced line numbers for key code
- [ ] Any discrepancies between summary and actual code noted

**See references/exploration-process.md** for spawn code, prompt templates,
valid/invalid indicators, and recovery steps.

## Related Commands

- `/spec-session` — Parent command that calls this sub-skill
- `/spec-consensus` — Runs after exploration and analysis rounds complete
