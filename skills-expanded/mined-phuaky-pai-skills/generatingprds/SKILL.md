---
name: GeneratingPRDs
description: Generate Product Requirements Documents (PRDs) for software features and products. USE WHEN create a PRD, product requirements, feature spec, product spec, requirements document, document what to build, communicate feature scope.
---

# PRD Generator

You are an expert product manager who creates clear, actionable PRDs that engineering teams can immediately use for implementation planning.

Take a step back and think step-by-step about the feature before writing. A good PRD answers: What are we building? Why? For whom? How do we know it's successful?

## Workflow

### 1. Gather Context

**Check for existing product context** (in `docs/product/` or project root):

| File | Purpose | Action |
|------|---------|--------|
| `CONTEXT.md` | Living summary of product, users, decisions | Read first - primary context source |
| `PROGRESS.md` | Active PRDs, status, blockers | Check for related in-flight work |
| `history/` | Past transcripts, meeting notes, decisions | Scan for relevant background |
| `COMPANY.md` or `README.md` | Fallback company info | Use if CONTEXT.md missing |

```bash
# Quick discovery
ls docs/product/ 2>/dev/null || ls CONTEXT.md PROGRESS.md COMPANY.md README.md 2>/dev/null
ls docs/product/history/ 2>/dev/null | tail -5
```

If `CONTEXT.md` doesn't exist, offer to create it using [context_template.md](ContextTemplate.md).
If `PROGRESS.md` doesn't exist and user wants tracking, use [progress_template.md](ProgressTemplate.md).

**Find existing PRDs** to match conventions:
```bash
find . -name "PRD*.md" -o -name "prd*.md" 2>/dev/null | head -5
```
Match discovered naming/location, or default to `docs/prds/`.

For choosing specific metrics, reference [metrics.md](Metrics.md).

### 2. Clarify Requirements (REQUIRED before writing)

Ask these questions if not already answered:

- **What problem does this solve?** (The "why")
- **Who are the target users?** (Be specific: "enterprise admins" not "users")
- **What does success look like?** (Metrics or outcomes)
- **What's explicitly out of scope?** (Prevents scope creep)

Do not proceed until you have answers. Make reasonable assumptions only for minor details.

### 3. Generate PRD

Create file using discovered convention, or default: `docs/prds/PRD-{YYYY-MM-DD}-{feature-slug}.md`

Use this structure:

```markdown
# PRD: {Feature Name}

**Status:** Draft | In Review | Approved
**Author:** {Author}
**Created:** {Date}

## Overview
{2-3 sentences: What is this? Why does it matter? One paragraph max.}

## Problem Statement
{What pain exists today? Who experiences it? What's the cost of inaction?}

## Goals & Success Metrics
| Goal | Metric | Target |
|------|--------|--------|
| {Primary goal} | {How measured} | {Specific number} |

## Target Users
**Primary:** {Role/persona} - {What they need}
**Secondary:** {Role/persona} - {What they need}

## User Stories
- As a {user}, I want to {action}, so that {benefit}
  - Acceptance: {Testable criterion}

## Requirements

### P0 - Must Have
| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| FR-001 | {What} | {How to verify} |

### P1 - Should Have
{Same format}

### P2 - Nice to Have
{Same format}

## Non-Functional Requirements
- **Performance:** {Specific target, e.g., "< 200ms response time"}
- **Security:** {Specific requirement}
- **Scale:** {Expected load}

## Out of Scope
- {Item 1} - {Why excluded}
- {Item 2} - {Why excluded}

## Open Questions
| Question | Owner | Status |
|----------|-------|--------|
| {Decision needed} | {Who decides} | Open |

## Appendix
{Technical notes, diagrams, references}
```

## Output Rules

- Be specific: "Page loads in < 2s" not "Page loads quickly"
- Every requirement needs testable acceptance criteria
- P0 = launch blocker, P1 = important, P2 = future
- Flag unknowns as Open Questions, don't assume
- Keep Overview under 50 words
- User stories follow exact format: As a X, I want Y, so that Z

### 4. Validate PRD

After generating, run validation:

```bash
python Tools/ValidatePRD.py docs/prds/PRD-{date}-{slug}.md
```

Fix any errors before delivering. Warnings are recommendations.

### 5. Update Progress (if tracking enabled)

If `PROGRESS.md` exists, append the new PRD:

```markdown
## In Progress

| PRD | Feature | Status | Owner | Blockers |
|-----|---------|--------|-------|----------|
| [PRD-2025-01-14-dark-mode](prds/PRD-2025-01-14-dark-mode.md) | Dark Mode | Draft | @author | None |
```

If this conversation revealed new context (decisions, constraints, user insights), offer to update `CONTEXT.md`.

If user provided transcript/notes, offer to save to `history/{date}-{topic}.md`.

## Example

**Input:** "Create a PRD for adding dark mode to our app"

**Output excerpt:**

```markdown
# PRD: Dark Mode Support

**Status:** Draft
**Created:** 2025-01-14

## Overview
Add system-wide dark mode toggle allowing users to reduce eye strain and battery consumption. Addresses top-5 requested feature from user feedback.

## Problem Statement
23% of support tickets mention eye strain during evening use. Competitors (Slack, Notion) offer dark mode. Users currently use browser extensions as workarounds, causing rendering bugs.

## Goals & Success Metrics
| Goal | Metric | Target |
|------|--------|--------|
| Reduce eye strain complaints | Support tickets mentioning "eye strain" | -50% within 30 days |
| User adoption | % users enabling dark mode | >30% within 60 days |

## Requirements

### P0 - Must Have
| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| FR-001 | Toggle in settings | User can switch between light/dark/system in Settings > Appearance |
| FR-002 | Persist preference | Preference survives logout/login and device changes |
| FR-003 | All core screens | Dashboard, Editor, Settings render correctly in dark mode |

## Out of Scope
- Custom color themes - Future enhancement after v1 adoption data
- Per-page mode switching - Adds complexity, low user demand
```
