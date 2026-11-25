---
name: knowledge-management
description: Classify, store, recall, and maintain project knowledge across sessions. Covers memory taxonomy, what to save vs exclude, recall verification, and memory hygiene. Use when saving project knowledge, organizing memories, reviewing stored context, or when the user says "remember this."
user-invocable: true
---

# Knowledge Management

CRITICAL: Memory is for knowledge NOT derivable from the current project state. If you can grep for it or read it from CLAUDE.md, don't save it as memory.

## Memory Taxonomy

Four types of knowledge, each with distinct purpose and storage rules:

<types>
<type>

**user** — Who the user is, their role, expertise, preferences, and how to tailor your work to them.
- Save when: You learn about the user's role, knowledge level, or working style.
- Use when: Tailoring explanations, calibrating technical depth, adjusting communication style.
- Example: "Deep Go expertise, new to React — frame frontend explanations in terms of backend analogues."

</type>

<type>

**feedback** — Guidance on how to approach work. Both corrections ("don't do X") AND confirmations ("yes, keep doing that").
- Save when: The user corrects your approach OR confirms a non-obvious approach worked. Corrections are easy to spot; confirmations are quieter — watch for them.
- Use when: Guiding behavior so the user doesn't repeat the same guidance.
- Structure: Lead with the rule, then **Why:** (reason/incident), then **How to apply:** (when this kicks in).
- Example: "Integration tests must hit a real database. **Why:** mock/prod divergence masked a broken migration. **How to apply:** any test that touches DB queries."

</type>

<type>

**project** — Ongoing work, goals, initiatives, and decisions NOT derivable from code or git history.
- Save when: You learn who is doing what, why, or by when. Convert relative dates to absolute dates ("Thursday" → "2026-04-03").
- Use when: Understanding context behind requests, anticipating coordination issues.
- Structure: Lead with the fact/decision, then **Why:** and **How to apply:**.
- Example: "Merge freeze begins 2026-04-05 for mobile release cut. Flag non-critical PR work after that date."

</type>

<type>

**reference** — Pointers to where information lives in external systems.
- Save when: You learn about resources outside the project directory and their purpose.
- Use when: The user references an external system or asks about external resources.
- Example: "Pipeline bugs tracked in Linear project 'INGEST'."

</type>
</types>

## What NOT to Save

These exclusions apply even when the user explicitly asks. If they ask to save a PR list or activity summary, ask what was *surprising* or *non-obvious* about it — that's the part worth keeping.

- **Code patterns, architecture, file paths, project structure** — derivable by reading the current project state
- **Git history, recent changes, who-changed-what** — `git log` / `git blame` are authoritative
- **Debugging solutions or fix recipes** — the fix is in the code; the commit message has the context
- **Anything already in CLAUDE.md files** — don't duplicate what's already documented
- **Ephemeral task details** — in-progress work, temporary state, current conversation context

## Memory Frontmatter Format

```markdown
---
name: {{descriptive name}}
description: {{one-line description — used to decide relevance in future conversations, so be specific}}
type: {{user, feedback, project, reference}}
---

{{content — for feedback/project types, use rule + Why + How to apply structure}}
```

## When to Access Memories

- When memories seem relevant, or the user references prior-conversation work.
- You MUST access memory when the user explicitly asks you to check, recall, or remember.
- If the user says to *ignore* or *not use* memory: proceed as if the memory store were empty. Do not apply, cite, compare against, or mention memory content.
- Memory records can become stale. Use them as context for what was true at a given point. Before acting on a memory, verify it against current state.

## Before Recommending from Memory

A memory that names a specific function, file, or flag is a claim that it existed *when the memory was written*. It may have been renamed, removed, or never merged.

- If the memory names a file path: check the file exists.
- If the memory names a function or flag: grep for it.
- If the user is about to act on your recommendation: verify first.

"The memory says X exists" is not the same as "X exists now."

A memory that summarizes repo state is frozen in time. If the user asks about *recent* or *current* state, prefer `git log` or reading the code over recalling a snapshot.

## Memory Layer Precedence

Knowledge sources load in this order, with later sources taking higher priority:

1. **Global/managed** — Organization-wide defaults
2. **User** (~/.claude/CLAUDE.md) — Personal instructions across all projects
3. **Project** (CLAUDE.md, .claude/rules/*.md) — Checked into the repo, shared with team
4. **Local** (CLAUDE.local.md) — Private project-specific instructions, not checked in

When sources conflict, trust the higher-priority (later-loaded) source. If a project rule contradicts a global rule, the project rule wins.

## Memory Hygiene

### Propose-Then-Approve
- Present ALL memory change proposals before making any changes.
- Don't modify memory files without explicit user approval.
- Group proposals by action type: promotions, cleanup, ambiguous.

### Classify Before Storing
| Destination | What Belongs |
|---|---|
| CLAUDE.md | Project conventions all contributors should follow |
| CLAUDE.local.md | Personal instructions specific to this user |
| Auto-memory | Working notes, temporary context, uncertain patterns |

### Periodic Cleanup
When reviewing memories, check for:
- **Duplicates**: entries already captured in CLAUDE.md → remove from auto-memory
- **Outdated**: older entries contradicted by newer information → update the older layer
- **Conflicts**: contradictions between layers → resolve, noting which is more recent

CRITICAL REMINDER: Only save what can't be derived from the current project state. Verify memories against current reality before recommending. Propose changes — don't apply them without approval.

## Related Skills

- `context-summarization` produces structured session summaries that inform what should become durable memory.
- `session-handoff` extends memory into cross-session continuity with template-based notes.
- `codebase-exploration` patterns help verify memory claims against current code state.

## Project Customization

If `user-config.md` exists alongside this file, read it and let its contents override or extend the defaults above. Common customizations:
- Team conventions for what belongs in CLAUDE.md vs personal notes
- External knowledge sources and their locations
- Memory retention policies (e.g., auto-expire project memories after N days)
- Additional memory types specific to the team's workflow
