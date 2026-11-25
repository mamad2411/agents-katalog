---
name: memory-management
description: >
  Save, recall, update, or delete persistent memory across sessions.
  TRIGGER when: user says "remember this", "save context", "forget", "what do you know about me",
  "recall", or asks to persist any information for future conversations.
argument-hint: "[save|recall|list|remove] [topic]"
user-invocable: true
---

# Memory Management

Manage the user's persistent memory system — a structured knowledge base that survives across sessions.

## First-Run Setup

Before any operation, verify the memory directory exists:

1. Check if `~/.claude/memory/` exists — if not, create it with `mkdir -p ~/.claude/memory/`
2. Check if `~/.claude/memory/MEMORY.md` exists — if not, create it with:

```markdown
# Memory Index

<!-- Each entry: - [Title](filename.md) — one-line description (under 150 chars) -->
```

## Memory Types

| Type | Purpose | Example |
|---|---|---|
| `user` | Who the user is — role, expertise, preferences | "Senior backend engineer, prefers Go, new to React" |
| `feedback` | How to work with this user — corrections and confirmations | "Don't add trailing summaries after code changes" |
| `project` | Ongoing work context — goals, deadlines, decisions | "Auth rewrite driven by legal compliance, not tech debt" |
| `reference` | Pointers to external systems and resources | "Pipeline bugs tracked in Linear project INGEST" |

## Operations

### Save — `$ARGUMENTS` contains "save" or user asks to remember something

1. **Classify**: Determine the memory type from context. If ambiguous, ask the user.
2. **Deduplicate**: Read `MEMORY.md` index. Search for existing memories on the same topic using Grep. If a match exists, update it instead of creating a new one.
3. **Normalize dates**: Convert all relative dates ("next Thursday", "yesterday") to absolute ISO dates (e.g., `2026-04-10`).
4. **Validate content**: Reject and explain if the user asks to save:
   - Code patterns, architecture, or file paths (derivable from codebase)
   - Git history or recent changes (use `git log`)
   - Debugging solutions (the fix is in the code)
   - Anything already in `CLAUDE.md`
   - Secrets, tokens, passwords, or credentials
5. **Generate filename**: Use kebab-case derived from topic: `{type}_{topic}.md` (e.g., `project_auth-rewrite.md`)
6. **Write the memory file**:

```yaml
---
name: descriptive-kebab-name
description: >
  One-line description optimized for relevance matching in future conversations.
  Be specific — "user prefers Go for backend services" not "user preferences".
type: user | feedback | project | reference
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

Lead with the core fact or rule.

**Why:** The reason or context behind this (a past incident, strong preference, constraint).

**How to apply:** When and where this memory should influence behavior.
```

7. **Update index**: Add a single line to `MEMORY.md`: `- [Title](filename.md) — one-line hook`
8. **Confirm**: Tell the user what was saved, the type, and filename.

### Recall — `$ARGUMENTS` contains "recall" or user asks what you remember

1. Read `MEMORY.md` to get the full index.
2. If the user specified a topic, use Grep to search memory files for relevant content.
3. Read matching memory files.
4. Present memories grouped by type, with a note on when each was last updated.
5. Flag any memories that may be stale (updated > 30 days ago).

### List — `$ARGUMENTS` contains "list" or user asks to see all memories

1. Read `MEMORY.md` and present the full index.
2. Show count by type: `user: 3, feedback: 5, project: 2, reference: 1`
3. Highlight stale entries (updated > 30 days ago) for review.

### Remove — `$ARGUMENTS` contains "remove", "forget", or "delete"

1. Search for the memory by topic keyword in `MEMORY.md` and memory files.
2. If multiple matches, present them and ask the user to confirm which one.
3. **Never delete without explicit confirmation.**
4. Remove the memory file.
5. Remove the corresponding line from `MEMORY.md`.
6. Confirm what was removed.

## Quality Standards

- **Index hygiene**: `MEMORY.md` must stay under 200 lines. If approaching the limit, prompt the user to triage old entries.
- **Atomic files**: One memory per file. Never combine unrelated facts.
- **Specificity**: Descriptions must be specific enough to match correctly. "user role" is bad. "user is a senior Go engineer at fintech startup" is good.
- **Staleness**: Always include `updated` date in frontmatter. Update it on every edit.
- **No orphans**: Every memory file must have a corresponding `MEMORY.md` entry and vice versa. If you find orphans during any operation, fix them.

## Error Recovery

- If `MEMORY.md` is corrupted or missing entries, rebuild it by scanning `~/.claude/memory/*.md` files.
- If a memory file referenced in `MEMORY.md` doesn't exist, remove the dangling reference.
- If duplicate entries exist for the same topic, merge them and remove the redundant file.

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners

## Edge Cases

- If input data is incomplete, state assumptions explicitly and flag gaps
- For time-sensitive situations, prioritize speed over comprehensiveness
- If multiple stakeholders have conflicting needs, document the tradeoffs
- For first-time use, start with a simplified version and iterate
- Adapt the depth and detail to the audience's expertise level
