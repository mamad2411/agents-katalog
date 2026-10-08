---
name: Spec-Driven Development
description: Interrogates the user to build a complete design specification before writing any code. Prevents "vibe coding" failures.
created: 2026-02-27
auto-invoke: false
model: default
context_trigger: "build app, create feature, new project, spec out, design doc, requirements, let's build, software project"
---

# 📋 Spec-Driven Development

> **Philosophy**: 55 minutes defining the problem, 5 minutes solving it.

## 1. The Problem

Most AI coding failures happen because the agent starts coding before understanding:

- What the user actually wants (vs. what they said)
- Edge cases and constraints
- Integration points and dependencies
- Success criteria

## 2. Execution Workflow

```
PHASE 1: INTERROGATION (No Code Allowed)
  ├─ "What is the ONE thing this must do?"
  ├─ "What does success look like? Be specific."
  ├─ "What are 3 things this must NOT do?"
  ├─ "Who/what does this interact with?"
  └─ "What's the simplest version that would be useful?"

PHASE 2: SPEC DOCUMENT
  └─ Write a design.md with:
     ├─ Goal (1 sentence)
     ├─ Requirements (numbered list)
     ├─ Non-Requirements (explicit exclusions)
     ├─ Architecture (how components connect)
     ├─ Edge Cases (what could go wrong)
     └─ Acceptance Criteria (how to verify)

PHASE 3: USER APPROVAL
  └─ Present spec for review
  └─ DO NOT proceed to code until approved

PHASE 4: IMPLEMENTATION
  └─ Code against the approved spec
  └─ Reference spec line items in commits
```

## 3. The Spec Template

```markdown
# Design Spec: [Feature Name]

## Goal
[One sentence describing what this does]

## Requirements
1. [Must do X]
2. [Must handle Y]
3. [Must integrate with Z]

## Non-Requirements (Out of Scope)
- [Will NOT do A]
- [Will NOT support B]

## Architecture
[How the components connect — diagram or description]

## Edge Cases
- [What if input is empty?]
- [What if API is down?]
- [What if user does X instead of Y?]

## Acceptance Criteria
- [ ] [Testable condition 1]
- [ ] [Testable condition 2]
```

## 4. When to Use

- Any feature that touches >3 files
- Any task that takes >30 minutes
- Any time you catch yourself thinking "I'll figure it out as I go"

---

# skill #engineering #planning #spec
