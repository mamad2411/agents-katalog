---
name: memory-flush
description: Prune, consolidate, and verify the CEO's MEMORY.md. Remove stale entries, update outdated facts, consolidate duplicate notes, and verify that referenced files and slugs still exist. Run after major milestones or when MEMORY.md exceeds 200 lines.
---

# Memory Flush

Over time, MEMORY.md accumulates stale entries: articles that were never published, decisions that were reversed, slugs that were renamed. Memory flush cleans this up to keep the CEO's context accurate.

## When to Run

- After 10+ articles published (periodic maintenance)
- After a major architectural change (new Astro version, redesign, etc.)
- When MEMORY.md exceeds 200 lines
- When the CEO notices a decision being made that contradicts a memory entry (suggests stale data)
- Explicitly requested via issue

## What to Check

### 1. Article Slugs

For every slug mentioned in memory:
- Verify `src/content/articles/{slug}/index.mdx` exists in the artstroy repo
- Verify `isDraft` status matches memory's record
- Remove entries for articles that were deleted or renamed

### 2. Agent/Skill References

- Verify each agent slug in memory corresponds to an actual `agents/{slug}/AGENTS.md` in this repo
- Remove references to agents that no longer exist
- Update skill names if they were renamed

### 3. Decision Records

- Cross-reference memory decisions against `docs/project_notes/decisions.md`
- If they contradict each other, `decisions.md` is authoritative — update memory
- Remove duplicates (memory often re-records decisions already in decisions.md)

### 4. Configuration Facts

- Verify environment variable names against `.paperclip.yaml inputs.env`
- Check that server URLs/hostnames in memory still match `key_facts.md`
- Flag any API key references that may have rotated

## Output

After flushing, post a summary:

```markdown
## Memory Flush — {YYYY-MM-DD}

- Entries before: {count}
- Entries after: {count}
- Removed: {count} stale article references, {count} outdated decisions, {count} dead links
- Updated: {count} entries corrected against current state
- Flagged for human review: {count} entries that needed context to verify

_Memory flush complete._
```

## Invariant

Do not delete memory entries you cannot verify are wrong. If uncertain, add `[VERIFY: {date}]` tag rather than deleting. Let humans clean up entries that require domain judgment.
