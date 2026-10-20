---
name: review-implementing
description: (1) Process and implement PR/code review feedback systematically. (2) Evaluate an implementation plan or draft code against a specification before coding proceeds. Use for review comments, pasted feedback, or when aligning a plan with acceptance criteria and design docs.
---
# Review feedback and spec alignment

**Portability:** This skill applies to any coding agent (OpenCode, Claude Code, Gemini, Cursor, Pi, etc.). Use your environment’s normal **task list**, **search**, and **edit** capabilities; names differ by product. Follow the **project’s** convention files (`AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, or team docs).

## Workflow A — Code review feedback

Systematically process and implement changes based on code review feedback.

### When to Use

- Provides reviewer comments or feedback
- Pastes PR review notes
- Mentions implementing review suggestions
- Says "address these comments" or "implement feedback"
- Shares list of changes requested by reviewers

### Systematic Workflow

#### 1. Parse Reviewer Notes

Identify individual feedback items:
- Split numbered lists (1., 2., etc.)
- Handle bullet points or unnumbered feedback
- Extract distinct change requests
- Clarify ambiguous items before starting

#### 2. Create Todo List

Track work with whatever your agent supports (native todo/plan feature, or a checklist in a project note file):
- Each feedback item becomes one or more tasks
- Break down complex feedback into smaller tasks
- Make tasks specific and measurable
- Keep exactly one task actively in progress at a time

Example:
```
- Add type hints to extract function
- Fix duplicate tag detection logic
- Update docstring in chain.py
- Add unit test for edge case
```

#### 3. Implement Changes Systematically

For each todo item:

**Locate relevant code:**
- Search the codebase for functions/classes (ripgrep, IDE search, or your agent’s search tool)
- Find files by name/path patterns as needed
- Read the current implementation

**Make changes:**
- Apply minimal, focused edits (patch/diff style or your agent’s edit workflow)
- Follow project conventions (`AGENTS.md`, `CLAUDE.md`, style guides, or team docs)
- Preserve existing functionality unless changing behavior

**Verify changes:**
- Check syntax correctness
- Run relevant tests if applicable
- Ensure changes address reviewer's intent

**Update status:**
- Mark each task complete as soon as it is done
- Move to the next task (one active task at a time)

#### 4. Handle Different Feedback Types

**Code changes:**
- Edit existing files in place
- Follow type hint conventions (PEP 604/585) when the project uses Python
- Maintain consistent style

**New features:**
- Add new files when needed
- Add corresponding tests
- Update documentation

**Documentation:**
- Update docstrings following project style
- Modify markdown files as needed
- Keep explanations concise

**Tests:**
- Match the project’s test style (e.g. pytest functions, Jest/Vitest, Go tables)
- Use descriptive names

**Refactoring:**
- Preserve functionality
- Improve code structure
- Run tests to verify no regressions

#### 5. Validation

After implementing changes:
- Run affected tests
- Run the project linter if one exists (e.g. `ruff`, `eslint`, `golangci-lint`, or CI’s lint job)
- Verify changes don't break existing functionality

#### 6. Communication

Keep user informed:
- Update the task list in real time
- Ask for clarification on ambiguous feedback
- Report blockers or challenges
- Summarize changes at completion

### Edge Cases

**Conflicting feedback:**
- Ask user for guidance
- Explain conflict clearly

**Breaking changes required:**
- Notify user before implementing
- Discuss impact and alternatives

**Tests fail after changes:**
- Fix tests before marking todo complete
- Ensure all related tests pass

**Referenced code doesn't exist:**
- Ask user for clarification
- Verify understanding before proceeding

### Important Guidelines

- **Always track tasks** (agent todo list or a written checklist)
- **Mark tasks completed immediately** after each item
- **Only one task in progress** at any time
- **Don't batch completions** — update status as you go
- **Ask questions** for unclear feedback
- **Run tests** if changes affect tested code
- **Follow the repo’s convention docs** for code style and architecture
- **Use conventional commits** if creating commits afterward

---

## Workflow B — Plan vs specification (pre-implementation)

Use when the user shares an **implementation plan**, **design doc**, **ticket**, or **draft code** and wants alignment **before** heavy coding.

### Steps

1. **Ingest spec:** List acceptance criteria, non-goals, APIs, data model, security or performance constraints.
2. **Map plan to criteria:** Table each criterion → planned work (or mark gap / risk).
3. **Flag mismatches:** Order of delivery, missing tests, unclear error handling, scope creep, deployment or rollback gaps.
4. **Propose adjustments:** Reorder tasks, add spikes, split PRs, or narrow MVP — do not start implementation until the user confirms.
5. **Optional:** Cross-check with `planning-with-files` or project roadmap docs if present.

This complements Workflow A (post-review changes); use B early, A after review.
