---
name: remember
description: Review reusable project knowledge and decide what belongs in project memory, notepad, or durable docs
---

# Remember

Use this skill when the user wants to preserve or organize useful knowledge discovered during a session.

## Goal
Promote durable, reusable knowledge into the right memory surface instead of leaving it buried in chat history.

## Memory surfaces
- **Project memory** — durable team/project knowledge
- **Notepad priority** — short high-signal context for the next turns
- **Notepad working** — temporary active-session notes
- **Docs / AGENTS / CLAUDE files** — durable instructions and conventions when they truly belong there

## Workflow
1. Gather the relevant session findings.
2. Classify each item:
   - durable project fact
   - temporary working note
   - operator preference or instruction
   - duplicate / stale / conflicting information
3. Propose the best destination for each item.
4. Write or update only the appropriate memory surface.
5. Call out duplicates or conflicts that should be cleaned up.

## Rules
- Do not dump everything into one store.
- Prefer project memory for durable team knowledge.
- Prefer notepad for short-lived working context.
- Keep entries concise and actionable.
- If something is uncertain, mark it as uncertain rather than storing it as fact.

## Output
- What was stored
- Where it was stored
- Any duplicates/conflicts found

## When NOT to use
- Information is only useful for the current turn.
- Secrets or credentials.

## Edge cases and failure handling
- Item is both temporary and durable -> store durable part only.
- Duplicate of existing memory -> update, do not add.

## Validation
- Each item is classified and stored once in the right surface; nothing sensitive stored.

## Example
```text
"We use pnpm and Node 20" -> project memory; "debugging login now" -> notepad working.
```

## Related skills
memory-status, wiki

## Inputs
Session findings.
