---
name: commit-conventions
description: 'Write commit messages and split large changes into small, ordered, atomic commits. Use when the user asks to commit changes, write a commit message, split a change into commits, or asks "how should I commit this". Enforces the `type(component): message` title format and the `git commit -s -m` signed-off command.'
---

# Commit Conventions

Writes commit messages in a consistent format and decomposes large changes into small, dependency-ordered, atomic commits. Every commit is created with a sign-off using `git commit -s -m`.

## Commit Title Format

```
type(component): message
```

- **type** — one of the five allowed types below.
- **component** — the affected module, package, or directory (e.g. `auth`, `api`, `parser`). Prefer the package or directory name. Omit only for changes that touch nothing specific.
- **message** — lowercase, imperative mood ("add", not "added"/"adds"), under ~60 characters, no trailing period.

| Type | When to use | Example |
|------|-------------|---------|
| `feat` | A new feature or capability | `feat(auth): add OAuth login flow` |
| `fix` | A bug fix | `fix(parser): handle empty input` |
| `docs` | Documentation only | `docs(readme): document setup steps` |
| `chore` | Maintenance, deps, tooling, no product change | `chore(deps): bump axios to 1.7` |
| `refactor` | Code restructuring with no behavior change | `refactor(api): extract request builder` |

## The Commit Command

Always commit with sign-off:

```bash
git commit -s -m "type(component): message"
```

- `-s` appends a `Signed-off-by: Your Name <you@example.com>` trailer, taken from `git config user.name` and `git config user.email`.
- Before committing, verify both are set so the sign-off is correct:

```bash
git config user.name && git config user.email
```

If either is empty, set them before committing.

## Thinking Process

When activated, follow this structured approach.

### Step 1: Survey the Change

**Goal:** Understand the full scope before committing anything.

**Actions:**
1. Run `git status` to see staged, unstaged, and untracked files.
2. Run `git diff` (and `git diff --staged`) to read what actually changed.
3. Group the changes mentally by intent, not by file.

**Decision Point:** Proceed only when you can name each distinct logical change in one sentence. If you can only say "lots of stuff changed", keep reading the diff.

### Step 2: Decompose Into Atomic Commits

**Goal:** Turn one large change into several small commits, each a single self-contained idea.

**Thinking Framework:**
- "One commit = one reviewable unit that does exactly one thing."
- "Could this commit be reverted on its own without breaking unrelated work?"
- "If a reviewer read only this commit's diff, would it make sense?"

**Heuristics for a good boundary:**
- A new interface/contract is its own commit, separate from its implementation.
- A refactor that enables a feature is its own commit, landing before the feature.
- Tests can ship with the code they cover, or as their own commit if added later.
- Unrelated fixes never ride along inside a feature commit.

**Anti-patterns to avoid:**
- A single giant "implement everything" commit.
- Mixing a refactor and a behavior change in one commit (impossible to review).
- "WIP", "fixes", "update" titles with no type or component.

### Step 3: Order Commits by Dependency

**Goal:** Sequence commits bottom-up so each one builds and passes on its own.

**Thinking Framework:**
- "What must exist before the next layer can compile or run?"
- Land foundational and contract layers first, then their consumers.

A reliable ordering for a non-trivial feature:

1. **Design / scaffolding** — types, data models, config, migrations. The shapes everything else depends on.
2. **Interface / contract** — public function signatures, API definitions, abstract interfaces. What callers will rely on.
3. **Implementation** — the concrete logic that fulfills the interface.
4. **Integration / wiring** — connect the implementation into the app, routes, DI.
5. **Tests & docs** — if not already shipped alongside each step.

This is a guideline, not a rule. Small changes may collapse to a single commit. Adapt the layers to the change at hand, but keep the principle: dependencies come before dependents.

### Step 4: Write Each Title and Commit

**Goal:** Produce a correct title and commit it with sign-off.

**Actions:**
1. Pick the right `type` for the commit's intent (the change, not the file kind).
2. Pick the `component` from the package or directory most affected.
3. Write the message: lowercase, imperative, concise.
4. Stage only the files for this commit (`git add <paths>`), then:

```bash
git commit -s -m "type(component): message"
```

Stage selectively so each commit stays atomic. Avoid `git add -A` when multiple logical changes are pending.

### Step 5: Self-Check

Before finishing, verify each commit:

- [ ] Atomic — does exactly one thing.
- [ ] Builds/passes on its own (dependencies committed earlier).
- [ ] Correct `type` and a meaningful `component`.
- [ ] Message is lowercase, imperative, under ~60 chars, no trailing period.
- [ ] Created with `-s` (signed off).
- [ ] Commits ordered so dependencies land before dependents.

## Worked Example

A large change adds rate limiting to an API. Instead of one commit, split and order it:

```bash
git commit -s -m "feat(config): add rate limit settings model"
git commit -s -m "feat(ratelimit): define Limiter interface"
git commit -s -m "feat(ratelimit): implement token bucket limiter"
git commit -s -m "feat(api): apply rate limiter to request handler"
git commit -s -m "docs(ratelimit): document configuration options"
```

The config model and interface (design + contract) land first, the implementation follows, then it is wired into the API, and docs close it out. Each commit builds on the previous and is reviewable alone.

## Rules Summary

| Rule | Detail |
|------|--------|
| Title format | `type(component): message` |
| Allowed types | `feat`, `fix`, `docs`, `chore`, `refactor` |
| Message style | lowercase, imperative, under ~60 chars, no trailing period |
| Commit command | `git commit -s -m "type(component): message"` |
| Sign-off | `-s` required; verify `git config user.name`/`user.email` first |
| Atomicity | one commit = one self-contained, reviewable change |
| Ordering | dependencies before dependents (design → interface → implementation) |
| Staging | stage selectively; avoid `git add -A` with mixed changes |

## Anti-Patterns

```bash
# BAD: one commit, many concerns, no format
git commit -m "added rate limiting and fixed login bug and cleanup"

# BAD: vague, no type or component, not signed off
git commit -m "wip"

# GOOD: atomic, formatted, signed off
git commit -s -m "fix(auth): reset session on failed login"
git commit -s -m "feat(ratelimit): implement token bucket limiter"
```
