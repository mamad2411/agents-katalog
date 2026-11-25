---
name: f5-workflow
description: F5 Framework workflow commands for AI-assisted development
category: core
allowed-tools: Read, Write, Glob, Grep, Bash
user-invocable: true
context: inject
---

# F5 Workflow Skill

## Quick Start

| Command | Description |
|---------|-------------|
| `/f5-research "topic"` | Gather context and evidence |
| `/f5-innovate` | Brainstorm ≥3 alternatives |
| `/f5-design --srs` | Create SRS document |
| `/f5-design --basic` | Create architecture design |
| `/f5-design --detail` | Create detail design |
| `/f5-plan` | Create implementation plan |
| `/f5-execute` | Generate code |
| `/f5-validate` | Multi-agent review |
| `/f5-workflow` | Show current status |
| `/f5-gate <name>` | Check quality gate |

## Workflow Phases

See: phases/

### Phase Sequence
Research → Innovate → Design (SRS → Basic → Detail) → Plan → Execute → Validate
↓         ↓           ↓                            ↓        ↓         ↓
D1        D1          D2,D3                        D4       G2        G3,G4

## Quality Gates

See: gates/

| Gate | Checkpoint | Requirements |
|------|------------|--------------|
| D1 | Before Design | Evidence ≥3, Quality ≥80% |
| D2 | SRS → Basic | SRS approved + evidence |
| D3 | Basic → Detail | Basic Design approved + evidence |
| D4 | Design → Plan | All docs approved, Confidence ≥90% |
| G2 | Plan → Execute | Plan exists, Confidence ≥90% |
| G3 | Execute → Validate | Tests pass, Coverage ≥80% |
| G4 | Final | Aggregate ≥90%, 0 critical issues |

## Templates

See: templates/

Document templates for:
- SRS (Software Requirements Specification)
- Basic Design (Architecture)
- Detail Design (Frontend + Backend + API)
- Test Plan

## Scripts

- `scripts/check-gate.py` - Validate gate requirements
- `scripts/update-status.py` - Update workflow status

## Memory System

F5 maintains state in `.claude/f5/memory/`:
- `CONTEXT.md` - Current phase, gates, confidence
- `PLANNING.md` - Architecture decisions
- `TASK.md` - Active tasks
- `KNOWLEDGE.md` - Lessons learned

## Language Rules

- **Content**: Vietnamese
- **Technical terms**: English (API, JWT, DTO, etc.)
- **Prohibited in SRS/Basic Design**: Source code, SQL, pseudocode
