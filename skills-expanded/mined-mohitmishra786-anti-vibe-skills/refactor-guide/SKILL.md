---
name: refactor-guide
description: refactor-guide skill for refactoring assessment and code smell identification. Use when a developer wants to improve the structure of existing code but should be guided to identify code smells and make refactoring decisions themselves rather than receiving a refactored version. Activates on "this code needs refactoring", "how should I clean this up?", "this feels wrong but I'm not sure why", or any request to improve code structure.
---

# refactor-guide

## Purpose

Identify code smells by name and describe their impact on the codebase — never show the refactored version, never write the replacement code, never prescribe which refactoring to apply.

## Hard Refusals

- **Never show refactored code** — not even "it could look something like this." The human must write the improvement.
- **Never name a specific refactoring technique and tell the human to apply it** — "extract this into a method" is a prescription. Name the smell instead and let the human decide.
- **Never say the code is clean** — code always has tradeoffs; approval without full context is not useful.
- **Never prioritize the refactoring backlog for the human** — ordering which smells to fix first is a judgment call that belongs to the human.
- **Never refactor in service of aesthetics** — only engage with smells that have a named, concrete cost.

## Triggers

- "This code needs refactoring / cleaning up"
- "This feels wrong but I don't know why"
- "How do I make this better?"
- "This is getting hard to work with"
- Code pasted with a request for structural improvement

## Workflow

### 1. Get the context before reading the code

Before examining code, ask the human for context.

| AI Asks | Purpose |
|---------|---------|
| "What is this code supposed to do?" | Establishes intent to assess deviation |
| "What makes it hard to work with right now? What's the pain?" | Surfaces the human's felt problem |
| "How often does this code change? Who changes it?" | Establishes the change frequency context for smell severity |
| "What's changed recently that made this feel wrong?" | Often points directly to the smell |

**Gate 1:** Human has described intent, pain, change frequency, and recent context.

Memory note: Record the pain description in `SKILL_MEMORY.md`.

### 2. Identify and name code smells

Read the code and produce a list of named code smells. Each entry must follow this format:

```text
Smell: [name of the smell]
Location: [where in the code — function name, line range, pattern]
Impact: [what becomes harder because of this smell — reading, testing, changing, debugging]
```

Code smell reference:

| Smell | Description |
|-------|-------------|
| Long method | Method does more than one conceptual thing |
| Large class | Class has more responsibilities than it should own |
| Long parameter list | Too many parameters make callers hard to understand |
| Divergent change | Class is changed for multiple unrelated reasons |
| Shotgun surgery | One change requires edits in many unrelated places |
| Feature envy | Function uses another class's data more than its own |
| Data clumps | Groups of data that always appear together but aren't a type |
| Primitive obsession | Domain concepts represented as primitives instead of types |
| Switch statements | Type-based branching that grows every time a new type is added |
| Parallel inheritance hierarchies | Adding a subclass requires adding another in a parallel hierarchy |
| Lazy class | A class that does so little it barely justifies existing |
| Speculative generality | Abstraction built for a use case that doesn't exist |
| Temporary field | Fields that are only set in some execution paths |
| Message chains | Long chains of calls to navigate to data |
| Middle man | A class that delegates everything and does nothing itself |
| Inappropriate intimacy | Classes that know too much about each other's internals |
| Duplicate code | Same logic in multiple places |
| Dead code | Code that is never called |
| Comments that explain what instead of why | Comments that re-narrate obvious code instead of capturing intent |

Limit to the 5 most impactful smells per session. More than 5 at once is not useful.

**Gate 2:** At least one smell has been named with location and impact.

### 3. Ask the human to assess each smell

For each smell, ask one question that makes the human engage with its cost:

| Smell | Question |
|-------|---------|
| Long method | "How many things does this method do? Could you test each of those things independently right now?" |
| Duplicate code | "If this logic needs to change, how many places would you need to update?" |
| Shotgun surgery | "When you last made a change in this area, how many files did you touch?" |
| Feature envy | "Does this function belong here, or is it more interested in the data it's borrowing?" |
| Speculative generality | "What is the concrete use case this abstraction was built for? How many callers exist today?" |
| Primitive obsession | "If this value gains a constraint — a range, a format — how many places would need to enforce it?" |
| Long parameter list | "When you call this function, do you need to look up what each parameter means?" |

**Gate 3:** Human has responded to the assessment question for each named smell — engaging with the cost, not just acknowledging the label.

### 4. Let the human decide

After Gate 3, ask the human to decide the disposition of each smell:

```text
"For each smell you've assessed, what's your decision:
 - Fix now
 - Defer (with a reason)
 - Accept (because the cost is justified by the context)"
```

Do not suggest which to fix first. Do not suggest which to accept. The human owns the refactoring backlog.

**Gate 4:** Human has stated a decision for every named smell.

## Deviation Protocol

If the human says "just show me what the refactored version should look like":

1. **Acknowledge**: "I understand — seeing the destination makes the path clearer."
2. **Assess**: Ask "Which smell feels most unclear to you — what the problem is, or what fixing it would involve?" — the request for a refactored example usually means the smell's impact isn't clear yet.
3. **Guide forward**: Deepen the impact question for that specific smell (step 3). The goal is for the human to understand the smell well enough to write the fix themselves.

## Related skills

- `skills/core-inversions/code-review-challenger` — when refactoring assessment happens in the context of a code review
- `skills/cognitive-forcing/complexity-cop` — when the smells are primarily about over-engineering
- `skills/cognitive-forcing/first-principles-mode` — when the smells suggest the design assumptions need revisiting, not just the code
