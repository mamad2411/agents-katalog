---
name: new-idea
description: Use when the user has a product idea to brainstorm, research, and document — captures ideas in a structured format that ports directly into Ralph sprint planning
---

# /new-idea — Brainstorm, Research & Document Product Ideas

Captures product ideas through structured brainstorming, market research, and codebase analysis. Produces a living document in the ideas directory that can be directly ported into a Ralph sprint via `/new-sprint`.

## Before Starting

Read `RALPH.md` to find:
- `Documents.ideas` — path to the ideas index file (derive the ideas directory from this path)
- `Documents.prd` — path to the PRD

If `RALPH.md` doesn't exist or is missing these paths, tell the user: "RALPH.md is missing or incomplete. Run `/ralph-init` to set up your project."

## Step 1: Explore the Idea

Start a conversation to understand what the user is thinking. Don't jump to solutions — dig into the problem first.

Ask about (naturally, not as a checklist):
- **The problem**: What user pain point does this solve? What's frustrating today?
- **The vision**: What would it look like when it's working? Walk me through the experience.
- **Who benefits**: Which user persona cares most? (See your PRD for user personas)
- **Inspiration**: Did they see this somewhere? What triggered the idea?

Keep going until you have a clear picture. Summarize back to the user: "So the idea is..." and confirm.

## Step 2: Research the Market

Use WebSearch to investigate how others handle this. Research at least 3 angles:

1. **Direct competitors**: Other apps in this space that have this feature — how do they implement it? What's good/bad?
2. **Adjacent apps**: Apps outside this space that solve a similar UX problem — what patterns work?
3. **Technical approaches**: How is this typically built? What libraries, APIs, or services exist?

Present findings as a brief competitive landscape:

```
## Market Research

### How Others Do It
- **[App/Service]**: [How they handle it, what works, what doesn't]
- **[App/Service]**: [...]

### What We Can Do Better
- [Specific differentiator or improvement opportunity]

### Technical Options
- [Approach 1]: [trade-offs]
- [Approach 2]: [trade-offs]
```

Discuss findings with the user — do they want to go a similar direction or differentiate?

## Step 3: Audit the Codebase

Silently check what already exists that's relevant:

1. Read `CLAUDE.md` — current tech stack, project structure (if exists)
2. Read `AGENTS.md` — codebase conventions, key files (if exists)
3. Read `README.md` — project overview (if exists)
4. Read the PRD (from RALPH.md `Documents.prd`) — check if this idea overlaps with planned features
5. Search the codebase for related files, hooks, components, or database tables
6. Read the ideas index (from RALPH.md `Documents.ideas`) — make sure this isn't a duplicate of an existing idea

Present a brief summary:

```
## Codebase Relevance

### Already Exists
- [What we'd build on — existing tables, hooks, components, APIs]

### Would Need
- [New tables, services, screens, or integrations required]

### PRD Overlap
- [Does this overlap with any planned PRD features? Which section?]
```

## Step 4: Assess the Idea

Rate the idea on these dimensions. Be honest — the user wants real assessment, not cheerleading.

```
## Assessment

| Dimension | Rating | Notes |
|-----------|--------|-------|
| **User Value** | High / Medium / Low | How much does this improve the user experience? |
| **Effort** | Trivial / Easy / Medium / Hard / Very Hard | How complex is this to build? |
| **Technical Risk** | High / Medium / Low | Unknown APIs, complex state, performance concerns |
| **Scope Creep Risk** | High / Medium / Low | How likely is this to balloon beyond the original idea? |
| **Market Fit** | Strong / Moderate / Weak | Does this differentiate us or just match competitors? |

**Overall**: [1-2 sentence honest take — is this worth pursuing and when?]
```

### Effort Scale
- **Trivial**: A few hours, minor changes to existing code
- **Easy**: 1 sprint (3-5 stories), no new infrastructure
- **Medium**: 1-2 sprints, may need a new API or service
- **Hard**: 2-3 sprints, new infrastructure or major refactor
- **Very Hard**: 3+ sprints, foundational change or new platform capabilities

### Risk Flags
- Depends on external API with no fallback
- Requires ML/AI model training or fine-tuning
- Changes core data model (migrations across many tables)
- Needs real-time sync or complex state management
- Platform-specific behavior divergence

Discuss the assessment with the user. They may want to adjust scope to reduce effort or risk.

## Step 5: Document the Idea

Derive the ideas directory from the `Documents.ideas` path in RALPH.md (e.g., if ideas is `docs/ideas/_index.md`, the directory is `docs/ideas/`). Write the idea file to `[ideas directory]/[idea-name].md` using the template below. The format is designed to port directly into `/new-sprint` when the time comes.

### File Naming
- Use kebab-case: `smart-search.md`, `bulk-import.md`
- Keep names short and descriptive

### Template

```markdown
# [Idea Title]

> [One-line summary of what this does for the user]

**Status:** idea
**Proposed by:** [user]
**Date:** [YYYY-MM-DD]
**Effort:** [Trivial/Easy/Medium/Hard/Very Hard]
**Value:** [High/Medium/Low]

## Problem

[What user pain point does this solve? Why does it matter?]

## Proposed Solution

[High-level description of the feature. What does the user experience look like?]

## Market Research

### Existing Solutions
- **[App/Service]**: [How they handle it — strengths and weaknesses]

### Our Differentiator
[What would make our version better or different?]

### Technical Options
- [Approach]: [trade-offs]

## Technical Considerations

### Builds On
- [Existing tables, hooks, components, APIs we'd leverage]

### New Infrastructure
- [New tables, services, screens, or integrations needed]

### Risks
- [Technical risks, scope creep risks, dependency risks]

## Open Questions

- [Unresolved questions that need answers before implementation]

## PRD Mapping

[Which PRD section would this fall under? Is it an extension of an existing feature or entirely new? This helps `/new-sprint` know where to slot it.]
```

### Status Values
- `idea` — just captured, not yet committed to
- `researched` — has market research and technical audit
- `planned` — committed to building, ready for `/new-sprint`
- `in-progress` — currently in a sprint
- `shipped` — built and merged to main
- `parked` — intentionally deferred (add reason)

## Step 6: Update the Index

Add or update the entry in the ideas index file (from RALPH.md `Documents.ideas`).

If the index file doesn't exist, create it from the template:

```markdown
# Ideas

Living index of product ideas. Use `/new-idea` to add new entries.

| Idea | Status | Effort | Value | File |
|------|--------|--------|-------|------|
```

The index format:

```markdown
| [Title] | idea | Medium | High | [filename.md](filename.md) |
```

Sort by status: `planned` first, then `researched`, then `idea`, then `parked`. Within each group, sort by value (High first).

## After Documenting

Tell the user the idea has been saved, then ask what they'd like to do next:

Use AskUserQuestion:
- **Promote to backlog now** — "The idea feels fully baked. Let's resolve open questions and add it to the backlog." If selected, invoke `/promote-idea` for this idea (skip Step 1 of that skill since the idea is already identified).
- **Save for later** — "I want to think on it. I'll run `/promote-idea` when I'm ready."
- **Brainstorm another idea** — Loop back to Step 1.

```
Idea documented in [ideas directory]/[filename].md

When you're ready to build it, run /promote-idea to move it
to the backlog, then /new-sprint to generate a sprint.
```
