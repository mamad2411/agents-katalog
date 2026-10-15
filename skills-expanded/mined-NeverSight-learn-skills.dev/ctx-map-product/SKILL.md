---
name: ctx-map-product
description: Build the product.md for a feature by exploring the codebase and talking to the developer to define use cases, business rules, and scope. Use when mapping an existing feature's product definition.
metadata:
  author: nicolasse
  version: "2.0.0"
---

# Map Feature Product

Your job is to generate a `product.md` for a feature — a short, human-readable product definition.

## Tone & Length

**This is critical.** The output must read like a person wrote it from memory, not like it was extracted from code. Think "quick notes on a whiteboard", not "generated documentation".

- The entire file should be **under 40 lines**
- Overview: 1-2 sentences max
- Use cases: one line each — name and what it does, that's it
- Business rules: plain language, one line each
- Out of scope: plain language, one line each
- **No code snippets.** No schemas. No types. That's what `engineering.md` is for.
- **No verbose descriptions.** If you need a paragraph to explain a use case, you're overcomplicating it.

## Input

The user provides a **feature name**.

### Feature Resolution

1. List all directories under `context/`
2. Match the user's request semantically
3. **If confident:** confirm and proceed
4. **If ambiguous or no match:** list available features and ask

If the feature directory doesn't exist yet, ask the user if they want to create it (with all three template files from `_template/`) before proceeding.

### Overwrite Check

If `context/{feature}/product.md` already exists and has content beyond the template:
- Show the user what's currently there
- Ask explicitly: overwrite, merge with new findings, or cancel
- Do NOT overwrite without confirmation

## Process

### Phase 1: Discover from code

List directories at the workspace root (skip `context/`). **Use an agent to explore the repos** — spawn a single agent to search across all repos for feature-related code:

- Triggers → how does a user (or system) initiate this feature? (UI action, cron, event, API call)
- UI components and pages → user-facing behavior
- API endpoints → capabilities
- Event handlers → reactive behavior
- Tests → expected behavior and edge cases

### Phase 2: Validate with the developer

Present a **short summary** of what you found and ask:

1. "Is this complete? Anything missing or wrong?"
2. "What's out of scope?"
3. "Any business rules not obvious from the code?"

Iterate until the developer confirms.

### Phase 3: Write product.md

Follow the template at `context/_template/product.md`. Keep it minimal.

### Phase 4: Review

Show the developer the file before writing. If `engineering.md` or `implementation.md` exist, flag any obvious gaps but don't bloat the product file to cover them.

## Output

1. Short summary of what you found
2. The generated `product.md` (should be short enough to read in 30 seconds)
3. Ask for feedback before writing
