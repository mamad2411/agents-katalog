---
name: web-architect
description: >
  Orchestrate premium web development across all project types. Conducts 4 subagents
  (Designer, Architect, Builder, Reviewer) with Constrained Generation for unique
  design systems. Use for: new pages, redesigns, design systems, project setup.
---

# Web Architect — Lean Orchestrator

Single skill that conducts 4 specialized subagents through a full design-to-code pipeline. Each subagent runs in fresh context. Inter-agent data flows via files on disk.

## Commands

| Command | Purpose | Entry Point |
|---------|---------|-------------|
| `/wa:design [desc]` | Full pipeline: design → architecture → build → review | Step 1 |
| `/wa:build [desc]` | Build with existing design system (skips design phase) | Step 5 |
| `/wa:review` | Review existing code against quality standards | Step 7 only |
| `/wa:profile [type]` | Set/view project type | Config |

## Pipeline Flow

```
1. Profile Check → 2. Load Context → 3. Designer → 4. DESIGN GATE (user approval)
→ 5. Architect → 6. Builder → 7. Reviewer → 8. QUALITY GATE (score >= 80?)
→ 9. Fix Loop (max 2) → 10. Self-Improvement → 11. Summary
```

**Design Gate** (Step 4): Pauses to show user the palette, fonts, concept, motion plan. User approves, modifies, or rejects. Modifications are the strongest learning signal.

**Quality Gate** (Step 8): Score < 80 triggers Builder fix loop (max 2 iterations). Score < 60 requires manual intervention.

## Subagent Dispatch

| Agent | File | Tools | Inputs | Output |
|-------|------|-------|--------|--------|
| wa-designer | `~/.claude/agents/wa-designer.md` | Read, Write, Bash, Glob, Grep | CLAUDE.md, constrained-generation.md, profile, learnings | `design-system/MASTER.md` |
| wa-architect | `~/.claude/agents/wa-architect.md` | Read, Write, Bash, Glob, Grep | CLAUDE.md, MASTER.md, profile | `web-architect-plan.md` |
| wa-builder | `~/.claude/agents/wa-builder.md` | Read, Write, Edit, Bash, Glob, Grep | CLAUDE.md, MASTER.md, plan | Code files + `web-architect-build-report.md` |
| wa-reviewer | `~/.claude/agents/wa-reviewer.md` | Read, Bash, Glob, Grep | All artifacts + quality-standards.md | `web-architect-review.md` |

## Skill Integration

Subagents reference existing skills — they don't replace them:

| Agent | Reads From | Purpose |
|-------|-----------|---------|
| Designer | `ui-ux-pro-max/SKILL.md` | Baseline design recommendations |
| Designer | `frontend-design` SKILL.md | Anti-AI-slop rules |
| Architect | `software-architecture/SKILL.md` | Clean architecture principles |
| Architect | `vercel-composition-patterns` SKILL.md | React composition patterns |
| Builder | `vercel-react-best-practices` SKILL.md | Performance patterns |
| Reviewer | `ui-ux-pro-max/SKILL.md` | Quality checklist |

## Context Rules

- Orchestrator stays under 5% main context
- Each subagent gets 100% fresh context
- Hard cap: 50% total main context window
- **Data transfer = files only**: MASTER.md, plan.md, build-report.md, review.md
- Orchestrator reads only metadata (score, file count) from subagent outputs — never full file contents

## Self-Improvement Loop

After every pipeline execution:
1. Reviewer writes `## Self-Improvement` in review.md (worked/failed/change)
2. Orchestrator extracts learnings
3. Appends to project memory `wa-learnings.md` with date + project type
4. User overrides at design gate get highest priority in learnings
5. Next invocation: loads learnings into Designer + Reviewer context

## Constrained Generation (Summary)

4-layer system ensuring unique output:

| Layer | Constraint | Enforcement |
|-------|-----------|-------------|
| Concept | Metaphor must differ from last 3 same-type projects | Checked via `wa-learnings.md` |
| Color | HSL harmony algorithm + WCAG 4.5:1 | Validated per-pair |
| Typography | Proven font pairing categories, Google Fonts only, banned list | Grep check |
| Motion | Timing ranges + `prefers-reduced-motion` required | Range validation |

Full rules: `references/constrained-generation.md`

## Project Types

8 profiles with type-specific layout, component, performance, and SEO specs:

landing · saas · dashboard · ecommerce · crm · portfolio · blog · desktop

Full profiles: `references/project-profiles.md`

## Quality Gate

5-dimension scoring (0-100 weighted):
- Design Fidelity (30%) — token usage, no hardcoded values
- Accessibility (25%) — WCAG, focus, ARIA, keyboard, reduced-motion
- Performance (20%) — server components, code splitting, image optimization
- Code Quality (15%) — TypeScript, component size, states, no duplication
- Architecture (10%) — plan compliance, RTL, i18n

Pass >= 80 | Fix 60-79 (max 2 loops) | Fail < 60

Full rubric: `references/quality-standards.md`
