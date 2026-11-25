---
name: brainstorming
description: Socratic design dialogue - explores user intent, requirements and design before implementation. Use before any creative work - creating features, building components, adding functionality, or modifying behavior.
category: engineering
exposure: standard
---

# Brainstorming Ideas Into Designs

## Overview

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design and get user approval.

## The Iron Law

```
NO IMPLEMENTATION WITHOUT APPROVED DESIGN FIRST
```

Do NOT write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it.

## Anti-Pattern: "This Is Too Simple To Need A Design"

Every project goes through this process. A todo list, a single-function utility, a config change — all of them. "Simple" projects are where unexamined assumptions cause the most wasted work. The design can be short (a few sentences for truly simple projects), but you MUST present it and get approval.

## Checklist

Complete these steps in order:

1. **Explore project context** — check files, docs, recent commits
2. **Ask clarifying questions** — one at a time, understand purpose/constraints/success criteria
3. **Propose 2-3 approaches** — with trade-offs and your recommendation
4. **Present design** — in sections scaled to their complexity, get user approval after each section
5. **Write design doc** — save to changes/ directory
6. **Transition to implementation** — invoke plan-protocol skill

## The Process

### Understanding the Idea

- Check out the current project state first (files, docs, recent commits)
- Before asking detailed questions, assess scope: if the request describes multiple independent subsystems, flag this immediately
- If the project is too large for a single spec, help the user decompose into sub-projects
- Ask questions one at a time to refine the idea
- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message - if a topic needs more exploration, break it into multiple questions
- Focus on understanding: purpose, constraints, success criteria

### Exploring Approaches

- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why

### Presenting the Design

- Once you believe you understand what you're building, present the design
- Scale each section to its complexity: a few sentences if straightforward, up to 200-300 words if nuanced
- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense

### Design for Isolation and Clarity

- Break the system into smaller units that each have one clear purpose
- Communicate through well-defined interfaces
- Can someone understand what a unit does without reading its internals?
- Can you change the internals without breaking consumers?
- Smaller, well-bounded units are easier to work with

## Design Document Template

```markdown
# [Feature Name] Design

## Problem Statement
[What problem are we solving?]

## Proposed Solution
[How will we solve it?]

## Architecture
[System components and their interactions]

## Data Flow
[How data moves through the system]

## Error Handling
[What happens when things go wrong]

## Testing Strategy
[How we verify it works]

## Open Questions
[Unresolved issues or alternatives considered]
```

## Quick Reference

```
1. Explore context
2. Ask questions (one at a time)
3. Propose approaches (2-3)
4. Present design (section by section)
5. Write design doc
6. Transition to planning
```

## Integration with Our Workflow

- **Before any feature:** Invoke this skill
- **Design approved:** Save to changes/ directory
- **Next step:** Use `plan-protocol` to create implementation plan
- **During implementation:** Use `test-driven-development`
