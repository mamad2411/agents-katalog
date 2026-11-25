---
name: remember
description: "[OMCP] Review reusable project knowledge and decide what belongs in project memory, rules, notepad, wiki, shared memory, or durable docs"
---

# Remember

Use this skill when the user wants to preserve or organize useful knowledge discovered during a session, including project memory, rules, wiki pages, notepad entries, and durable instructions.

## Goal
Promote durable, reusable knowledge into the right memory surface instead of leaving it buried in chat history.

## Memory surfaces
- **Project memory** — durable team/project knowledge
- **Rules** — long-lived behavioral constraints that should apply to future file work
- **Notepad priority** — short high-signal context for the next turns
- **Notepad working** — temporary active-session notes
- **Wiki** — reviewable architecture, debugging, convention, and decision knowledge
- **Shared memory** — cross-agent coordination findings/questions
- **Docs / AGENTS / instruction files** — durable instructions and conventions when they truly belong there

## OMCP tools
- Read pending matched rules before deciding whether a rule already exists:
  `mcp__omcp__rules_pending_read({ limit: 10 })` for a redacted overview, or
  include `session_id` for full pending rule text from the current session.
- Inspect the rules/memory ownership model:
  `mcp__omcp__rules_policy_report({})`
- Store durable facts with `mcp__omcp__project_memory_write` or
  `mcp__omcp__project_memory_add_note`.
- Store durable behavior preferences with `mcp__omcp__project_memory_add_directive`
  unless they should become a repository rule file.
- Store active short-lived context with `mcp__omcp__notepad_write_priority` or
  `mcp__omcp__notepad_write_working`.
- Store reviewable compound knowledge with `mcp__omcp__wiki_add` or
  `mcp__omcp__wiki_ingest`.

## Workflow
1. Gather the relevant session findings.
2. Classify each item:
   - durable project fact
   - durable rule/policy
   - temporary working note
   - wiki-worthy reusable explanation
   - agent coordination message
   - operator preference or instruction
   - duplicate / stale / conflicting information
3. Propose the best destination for each item.
4. Write or update only the appropriate memory surface.
5. Call out duplicates or conflicts that should be cleaned up.

## Rules
- Do not dump everything into one store.
- Prefer project memory for durable team knowledge.
- Prefer rule files for constraints that should apply whenever matching files are touched.
- Prefer notepad for short-lived working context.
- Prefer wiki pages for reusable explanations that need markdown structure and search.
- Prefer shared memory only for coordination between active agents.
- Keep entries concise and actionable.
- If something is uncertain, mark it as uncertain rather than storing it as fact.

## Output
- What was stored
- Where it was stored
- Any duplicates/conflicts found
