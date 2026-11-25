---
name: asset-dehydration
description: Extract reusable patterns from business code into permanent skill assets. Use when the user asks to extract, dehydrate, distill, or generalize a pattern, solution, or architectural approach into a reusable skill or document.
---

# Asset Dehydration (资产脱水)

## When to Use

- A tricky bug was solved with an elegant pattern worth preserving
- A system design model proved effective (e.g. worker pool, retry strategy)
- A coding pattern keeps recurring across modules
- User explicitly asks to "dehydrate" or "extract" a reusable asset

## Core Principle

Every hard-won insight must be stripped of business coupling and crystallized into a permanent, reusable asset. Don't let it rot in chat history.

## Dehydration Workflow

```
Dehydration Progress:
- [ ] Step 1: Identify the reusable pattern
- [ ] Step 2: Strip business coupling
- [ ] Step 3: Write a clean, generic demo
- [ ] Step 4: Package as a Skill or Pattern doc
- [ ] Step 5: Verify the asset is self-contained
```

### Step 1: Identify the Pattern

Analyze the business code and extract the core mechanism:

- What is the general problem being solved? (Not "how to handle Telegram messages" but "how to build a channel adapter")
- What are the key constraints and trade-offs?
- What makes this solution non-obvious?

### Step 2: Strip Business Coupling

Remove all project-specific references:

- Replace `TelegramChannel` with `SomeChannel`
- Replace `ChatMessage` with `Message` or `Item`
- Remove imports of project-specific packages
- Generalize configuration to use placeholder values

### Step 3: Write a Clean Demo

Create a minimal, self-contained Go example that demonstrates the pattern:

```go
// Example: Worker Pool pattern
// - Configurable concurrency limit
// - Graceful shutdown via context
// - Error collection with errgroup
func ExampleWorkerPool() {
    pool := NewWorkerPool(maxWorkers)
    results, err := pool.Process(ctx, items)
    // ...
}
```

The demo must:
- Compile and run independently
- Include inline comments explaining key decisions
- Cover the happy path and at least one error path

### Step 4: Package as Asset

Choose the storage location based on scope:

**Option A: Cursor Skill** (for coding patterns the AI should apply)

Create in `.cursor/skills/<pattern-name>/`:

```
<pattern-name>/
├── SKILL.md      # When and how to apply this pattern
└── reference.md  # Detailed implementation guide
```

**Option B: Pattern Document** (for design decisions and architecture patterns)

Create in `docs/patterns/`:

```
docs/patterns/<pattern-name>.md
```

### Step 5: Verify Self-Containment

The asset must be usable without reading the original business code:

- [ ] Can a developer understand it without project context?
- [ ] Does the demo compile on its own?
- [ ] Are all trade-offs and constraints documented?
- [ ] Is the "when to use" section specific enough?

## Output Template

```markdown
# Pattern Name

## Problem
[What general problem does this solve?]

## Solution
[Core mechanism in 2-3 sentences]

## Key Constraints
- [Constraint 1]
- [Constraint 2]

## Implementation
[Code with comments]

## When to Use
[Specific scenarios where this pattern applies]

## When NOT to Use
[Anti-patterns or scenarios where this is overkill]
```
