---
description: Context Summarization - Guidelines for creating focused summaries when context becomes too large for efficient processing
alwaysApply: false
---

# Context Summarization

## Purpose

When context becomes too large for efficient processing, create focused summaries to:
- Reduce token usage
- Improve comprehension
- Enable faster retrieval
- Maintain accessible knowledge base

**Industry Standard:** ✅ Yes - Summarization is widely used in AI systems (GitHub Copilot, Cursor AI, RAG systems)

---

## When to Summarize

**Trigger Conditions:**
- Context exceeds practical token budget (>50K tokens)
- Same context referenced multiple times across sessions
- Large codebase analysis (100+ files analyzed)
- Complex multi-file implementations (10+ related files)
- User explicitly requests summary

**Decision Flow:**
```
Is context > 50K tokens? → Summarize
Is same context used 3+ times? → Summarize
Is analysis spanning 100+ files? → Summarize
Otherwise → Use full context
```

---

## How to Summarize

### Step 1: Identify Logical Chunks

**Don't create one giant summary.** Break into topic-focused chunks:

**Examples:**
- `validation-logic.md` (validation logic)
- `processor-integration.md` (processor integration)
- `aggregation-logic.md` (aggregation logic)
- `status-flow.md` (status management)

**Principle:** One logical area = one summary file

---

### Step 2: Create Topic-Focused Summaries

**File Location:**
```
docs/context/summaries/{YYYY-MM-DD}_{HH-MM}_{topic-name}.md
```

**File Naming:**
- Format: `{YYYY-MM-DD}_{HH-MM}_{topic-name}.md`
- Use kebab-case for topic names
- Include timestamp for versioning
- Be descriptive but concise

**Examples:**
- ✅ `2025-10-30_11-00_validation-logic.md`
- ✅ `2025-10-30_11-00_feature-implementation.md`
- ❌ `summary.md` (too generic)
- ❌ `context.md` (not descriptive)

---

### Step 3: Use Summary Template

**Standard Template:**
```markdown
# {Topic Name} - Context Summary

**Date:** {YYYY-MM-DD HH:MM}
**Source:** {What was summarized - e.g., "Analysis of ComponentA.php and related files"}
**Detail Level:** {Overview | Detailed | Comprehensive}
**Related Files:** {Links to related summaries or source files}

## Summary
{2-3 sentence high-level summary}

## Key Components
- **Component 1:** {description}
- **Component 2:** {description}
- **Component 3:** {description}

## Important Details
{Important technical details that shouldn't be lost in summary}

## File Relationships
- `File1.php` → `File2.php` (relationship description)
- `File3.php` → `File4.php` (relationship description)

## Code Patterns
{Key code patterns or conventions identified}

## Related Context
- [Related Summary 1](./2025-10-30_11-00_related-topic.md)
- [Related Summary 2](./2025-10-30_11-00_another-topic.md)

## Notes
{Any important notes or warnings}
```

---

### Step 4: Update Master Index

**File:** `docs/context/summaries/index.md`

**Index Format:**
```markdown
# Context Summaries Index

**Last Updated:** {YYYY-MM-DD HH:MM}

## {Topic Category} ({Date})
- **{Topic Name}:** [`{filename}.md`](./{filename}.md) - {Brief 1-line description}
- **{Topic Name}:** [`{filename}.md`](./{filename}.md) - {Brief 1-line description}

## {Another Category} ({Date})
- **{Topic Name}:** [`{filename}.md`](./{filename}.md) - {Brief 1-line description}
```

**Index Maintenance:**
- Add entry immediately after creating summary
- Group by topic category
- Sort by date (newest first)
- Include brief description for quick scanning

---

### Step 5: Reference Summaries

**In Future Sessions:**
- Reference summary file instead of full context
- Link to summary: `See context summary: [Topic Name](./docs/context/summaries/2025-10-30_11-00_topic-name.md)`
- Use summary for context, retrieve full files only if needed

---

## Best Practices

### ✅ DO:
- **Chunk by topic** - One logical area per file
- **Include metadata** - Date, source, detail level
- **Link related summaries** - Cross-reference related topics
- **Update index** - Always add to index.md
- **Be descriptive** - Include enough detail to be useful
- **Use timestamps** - Enables versioning and chronological order

### ❌ DON'T:
- **Don't create one giant summary** - Too hard to navigate
- **Don't skip the index** - Makes summaries hard to find
- **Don't forget metadata** - Context about context is important
- **Don't duplicate** - Check if summary already exists
- **Don't make it too brief** - Include important technical details

---

## Hierarchical Summarization (Optional Enhancement)

**For Complex Topics:** Create multiple detail levels

**Structure:**
```
docs/context/summaries/
├── 2025-10-30_11-00_feature-overview.md (high-level, 1 page)
├── 2025-10-30_11-00_feature-detailed.md (detailed, 3-5 pages)
└── 2025-10-30_11-00_feature-comprehensive.md (full detail, 10+ pages)
```

**Use Cases:**
- Overview: Quick understanding, initial context
- Detailed: Working with the code, implementing features
- Comprehensive: Deep debugging, architectural decisions

---

## Incremental Updates

**When Context Changes:**
- Don't recreate entire summary
- Add "Changes Since Last Update" section
- Update "Last Updated" timestamp
- Keep previous summary intact (for history)

**Example:**
```markdown
## Changes Since Last Update (2025-10-30 15:00)

### Added:
- Feature X validation (commit abc123)
- Integration logic (commit def456)

### Updated:
- Status flow documentation (commit ghi789)

### Removed:
- Legacy logic (commit jkl012)
```

---

## Verification Checklist

Before considering context summarized:
- [ ] Summary file created with proper naming
- [ ] Summary follows template structure
- [ ] Metadata included (date, source, detail level)
- [ ] Index.md updated with entry
- [ ] Related summaries linked
- [ ] Important technical details preserved
- [ ] File location: `docs/context/summaries/`

---

## Remember

✅ **Chunk by Topic**: One logical area per summary file  
✅ **Metadata Matters**: Include date, source, detail level  
✅ **Update Index**: Always add to index.md for discoverability  
✅ **Link Related**: Cross-reference related summaries  
✅ **Preserve Details**: Include important technical details  
✅ **Use Timestamps**: Enables versioning and chronological order  
✅ **Don't Duplicate**: Check if summary already exists
