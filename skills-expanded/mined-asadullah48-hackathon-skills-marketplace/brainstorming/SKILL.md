---
name: brainstorming
description: Use when the user presents an idea, feature request, or problem that needs exploration before implementation - facilitates collaborative ideation through structured questioning and approach evaluation
---

# Brainstorming Ideas Into Designs

## Overview

Transform ideas into comprehensive designs through structured dialogue.

**Core principle:** Progressive refinement through targeted questions, then present approaches with trade-offs.

**Announce at start:** "I'm using the brainstorming skill to explore this idea."

## The Process

### Phase 1: Understanding the Idea

1. **Assess current state** - What exists today?
2. **Ask clarifying questions** - One at a time, prefer multiple choice
3. **Refine progressively** - Each answer narrows scope

**Question patterns:**
- "What problem does this solve?"
- "Who is the primary user?"
- "What are the constraints?"
- "What does success look like?"

### Phase 2: Exploring Approaches

Present 2-3 approaches with trade-offs:
- Lead with recommended option
- Explain rationale clearly
- Show contrast between options

### Phase 3: Presenting Design

Break into sections of 200-300 words:
- Architecture
- Components
- Data flow
- Error handling
- Testing approach

Validate after each section.

## After the Design

**Documentation:**
- Write to `docs/plans/YYYY-MM-DD-<feature-name>.md`
- Commit to git

**Implementation:**
- Confirm readiness
- Use appropriate skills for execution

## Key Principles

- One question at a time (avoid overwhelm)
- Prefer multiple choice options
- YAGNI: ruthlessly remove unnecessary features
- Validate incrementally

## Red Flags - STOP

- Skipping questioning phase
- Presenting single approach only
- Assuming requirements without validation
- Over-engineering features not needed
