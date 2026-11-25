---
name: ios-design-workflow
description: Orchestrates complete iOS app design workflow from idea to implementation. Use when starting a new iOS feature, planning iOS app architecture, or need end-to-end iOS design process.
version: 1.0.0
---

# iOS Design Workflow

End-to-end orchestrator for iOS app design, from initial idea to GitHub/Gitea issues.

## When to Use

- Starting a new iOS app or feature
- Planning iOS UI/UX from scratch
- Need structured approach to iOS design
- Want to follow Apple HIG throughout the process

## Workflow Phases

### Phase 1: Requirements Gathering
**Invoke:** `superpowers:brainstorming`

Explore the idea through collaborative dialogue:
- Clarify app purpose and target users
- Identify core features and user flows
- Define success criteria
- Understand constraints (iOS versions, devices)

### Phase 2: Research
**Invoke:** `sc:research`

Deep research on:
- Similar iOS apps and patterns
- Apple HIG requirements for the feature type
- SwiftUI/UIKit capabilities needed
- Third-party libraries if applicable

### Phase 3: Business Specification
**Invoke:** `sc:business-panel` then `sc:spec-panel`

Create comprehensive specification:
- User stories with acceptance criteria
- Feature requirements document
- UI/UX flow diagrams
- Success metrics

Save to: `docs/specs/{feature-name}-spec.md`

### Phase 4: Task Decomposition
**Invoke:** `sc:workflow` or `sc:spawn`

Break specification into actionable tasks:
- Identify independent work streams
- Define task dependencies
- Estimate complexity (S/M/L)
- Create parallelization strategy

### Phase 5: Architecture Planning
**Invoke:** `sc:design` + `ios-swiftui-generator`

For each task:
- Design component architecture
- Generate SwiftUI code scaffolding
- Plan data flow and state management
- Document API contracts

Validate with: `ios-design-review`

### Phase 6: Documentation & Issues
**Actions:**
1. Save all specs to `docs/` directory
2. Create issues via Gitea MCP or GitHub CLI
3. Link issues to specification documents
4. Set up project board if needed

## Example Usage

```
User: I want to build an iOS expense tracker app

Claude: [Invokes superpowers:brainstorming]
- What's the primary use case?
- Target audience?
- Key features needed?
...continues through all phases...
```

## Output Artifacts

| Phase | Output |
|-------|--------|
| 1 | `docs/plans/YYYY-MM-DD-{feature}-requirements.md` |
| 2 | Research findings in conversation |
| 3 | `docs/specs/{feature}-spec.md` |
| 4 | Task breakdown with estimates |
| 5 | Architecture docs + code scaffolding |
| 6 | GitHub/Gitea issues created |

## Related Skills

- `ios-swiftui-generator` — Generate SwiftUI components
- `ios-design-review` — Validate HIG compliance
- `ios-hig-reference` — Apple HIG quick reference
