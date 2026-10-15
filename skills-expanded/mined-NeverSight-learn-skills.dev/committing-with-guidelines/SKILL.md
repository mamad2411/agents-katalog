---
name: committing-with-guidelines
description: Create git commits with atomic scope and product-focused messages. Use whenever preparing, writing, or reorganizing commits.
---

# Story-first commits

Build a reviewable sequence of atomic commits. Each commit should record one product or architectural outcome and enough reasoning for a future reader to understand it.

## Workflow

### 1. Inventory the worktree

Inspect, at minimum:

```bash
git status --short
git diff
git diff --cached
```

Check recent commit subjects when repository conventions may be stricter than this skill. Identify generated files, unrelated edits, and changes that should remain uncommitted.

**Complete when:** every changed path belongs to a proposed commit or is explicitly excluded.

### 2. Plan the story

Order commits by dependency and by how a reviewer would learn the change. Keep each commit to one logical outcome, while including its related tests and documentation. Split unrelated outcomes even when they touch the same file.

For more than one commit, state the proposed sequence before staging.

**Complete when:** each changed hunk has one destination and every commit can stand on its own.

### 3. Stage one unit

Stage exact paths or use patch mode:

```bash
git add path/to/file
git add -p
```

Then inspect the staged result:

```bash
git diff --cached --stat
git diff --cached
```

Use broad staging only after inventorying the whole worktree.

**Complete when:** the index contains exactly one logical outcome, including the tests and docs needed to support it.

### 4. Validate the staged change

Run the repository's relevant tests, linters, or checks. Choose the narrowest checks that cover the commit, and add broader checks when project instructions require them.

**Complete when:** required checks pass, or the user knows which check failed and why the commit should or should not proceed.

### 5. Write and create the commit

Use this structure:

```text
<Action> <product-focused outcome>

- <decision, rationale, user impact, or trade-off>
- <additional context only when it helps a future reader>
```

#### Subject

- Start with `Add`, `Update`, `Remove`, or `Delete`.
- Use present tense and name the concrete outcome.
- Prefer a subject under 72 characters.
- Describe the product or architecture rather than the files or classes.
- Keep ticket numbers in the branch name unless the repository requires them in commits.

Examples:

```text
Add team filtering to the progress dashboard
Update notification delivery to support multiple channels
Remove deprecated user-preference endpoints
```

#### Body

Add a body when the reason, impact, or trade-off is not obvious from the diff. Use bullets for distinct decisions. Explain:

- why the change took this shape;
- product or user impact;
- architectural implications;
- material trade-offs.

Leave out implementation inventories, routine test additions, and AI attribution or co-authorship. The diff records implementation; the commit message records intent.

Before committing, read the staged diff once more and derive the message from that exact content.

**Complete when:** the message accurately describes the staged outcome and its non-obvious reasoning.

### 6. Verify and continue

After each commit, inspect `git status --short` and the new commit. Repeat the workflow for the next planned unit.

**Complete when:** the intended sequence exists, each commit is independently understandable, and remaining changes are accounted for.

## History safety

Treat published history as immutable. Reorder, squash, amend, or force-push only when the user requests history editing and confirms the commits are safe to rewrite. Prefer `--force-with-lease` over `--force`.

For worked examples of splitting a mixed worktree, improving messages, or arranging unpublished commits, read [EXAMPLES.md](EXAMPLES.md).
