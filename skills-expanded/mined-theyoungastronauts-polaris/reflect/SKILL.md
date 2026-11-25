---
name: reflect
description: "Session retrospective — capture learnings into the project context scaffold and per-project session memory."
disable-model-invocation: true
---

# Session Reflection

Capture what you learned this session into persistent memory.

## When to Use

Run `/reflect` at the end of a productive session — especially when:
- You corrected Claude's approach or preferences
- You hit a tricky bug and found the root cause
- You established or discovered project conventions
- You repeated a workflow pattern multiple times

Skip for quick sessions or trivial changes.

## 1. Scan the Session

Review the conversation history. Look for four categories:

**Corrections** (highest signal)
- Times the user redirected your approach
- Suggestions the user rejected and what they wanted instead
- Explicit preferences ("always do X", "never do Y")

**Debugging Insights**
- Root causes that weren't obvious from the error
- Framework gotchas or environment quirks
- Diagnostic sequences that worked

**Patterns**
- Repeated workflows worth codifying
- File organization or naming conventions
- Tool preferences or configurations

**Conventions**
- Architectural patterns found in the codebase
- Implicit project rules not documented elsewhere
- Integration patterns between services

## 2. Filter Ruthlessly

Each candidate must pass ALL four checks:

1. **Stable?** — Will this recur? One-off decisions don't need memory.
2. **Already documented?** — Check CLAUDE.md, existing memory files, project docs. Don't duplicate.
3. **Actionable?** — "The API is complex" is useless. "Always pass X header when calling Y endpoint" is useful.
4. **Project-scoped?** — The memory store is per-project. If a finding applies to all projects (a user preference, a general workflow lesson), still record it here — note the broader scope in the entry so it can be promoted later.

Discard anything that fails any check.

## 3. Bridge to Project Context

After filtering, do a second pass on the surviving findings. Ask: **"Is this finding project-structural?"**

A finding is project-structural if it describes:
- An architectural decision or tradeoff (→ `decisions.md`)
- A naming, file organization, or error handling convention (→ `conventions.md`)
- A reusable structural pattern (→ `patterns/`)

For any project-structural findings, check if `.claude/context/` exists:

**If the scaffold exists:** Propose writing them with the `remember` skill's format — read the installed `remember` skill (`.claude/skills/remember/SKILL.md`, or `skills/remember/SKILL.md` in the repo) for its classify → format → write steps rather than guessing the scaffold format. Present each one:

```
**Context type:** Decision | Convention | Pattern
**Target:** .claude/context/<file>
**Entry:**
> [The formatted entry text]
```

Group these separately from session memory proposals (Step 4). The user approves context writes independently from memory writes.

**If the scaffold doesn't exist:** Skip this step. Mention that `/intel` can generate the scaffold if the user wants to persist project-level findings.

Non-structural findings (personal preferences, debugging tricks, tool configurations) stay in session memory only — continue to Step 4 for those.

## 4. Propose Session Memory Updates

For each surviving finding, present:

```
**Type:** User | Feedback | Project | Reference
**File:** <memory file slug — one fact per file, e.g. git-commit-style.md>
**Action:** Add | Update | Remove

> The exact text to write

**Evidence:** What happened in the session that produced this
```

Pick `Type` using the same taxonomy as Memory Organization below. Group by type, then by file.

## 5. Write Approved Changes

Only write what the user explicitly approves.

**Project context entries** (from Step 3): Follow the installed `remember` skill (`.claude/skills/remember/SKILL.md`, or `skills/remember/SKILL.md` in the repo) — its classify → deduplicate → format → write process is the single source of truth for context-scaffold entries. Don't re-derive the format here.

**Session memory entries** (from Step 4):

1. Write each approved finding to its own file in the memory store, with the `name`/`description`/`metadata` frontmatter from Memory Organization (create the file — don't append into an unrelated one)
2. Add a one-line pointer to it in `MEMORY.md`
3. If a memory file already covers the topic, update or replace it rather than adding a duplicate

## Memory Organization

Session memory lives in the harness's per-project auto-memory store:
`~/.claude/projects/<project-path>/memory/`. The convention is **one fact per
file**, each file carrying frontmatter:

```markdown
---
name: {short-kebab-slug}
description: {one-line summary — this is what future sessions scan to judge relevance}
metadata:
  type: {user | feedback | project | reference}
---

{The memory itself — a few lines. Link related memories with [[other-slug]].}
```

Pick `type` by what the finding is: a fact or preference about the user → `user`;
guidance on how to work, or a correction → `feedback`; state about the current
work → `project`; a pointer to where information lives elsewhere → `reference`.

`MEMORY.md` is the **index, not a store**: one pointer line per memory file
(`- [Title](file.md) — one-line hook`), no frontmatter, kept short (it is always
loaded into context, and lines past ~200 are truncated). Never write memory
content directly into `MEMORY.md`.

Organize by topic, not by date. When a finding supersedes an earlier one, update
or remove that memory file instead of appending a contradiction.

## What NOT to Save

- Session-specific context (current task, temporary state)
- Information already in CLAUDE.md or project docs
- Speculative conclusions from limited evidence
- Generic best practices any developer would know
- Anything that contradicts established project conventions
