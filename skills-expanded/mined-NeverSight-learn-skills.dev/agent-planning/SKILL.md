---
name: agent-planning
description: 'Agent-optimized project planning. Given a problem statement, produces a compact 1-page charter: objective, MVP scope, actors, modules, roadmap, risks, stack. Use when user says "plan project", "project charter", "MVP scope", "define scope", "plan this". No methodology explanations, no ceremonies, no MoSCoW theory.'
requires-devkits: auto-detect
---

# Agent Planning -- Compact Project Charter

Produces a 1-page project charter optimized for agent consumption. Tables only, no prose.

---

## Workflow

### Step 1: Ask Minimum Questions

Ask at most 2 questions in one message:
1. What problem does it solve and for whom? (one sentence)
2. What is the target platform? (web, mobile, both)

Infer stack from project if available. If no project, assume reasonable defaults.

### Step 2: Generate Compact Charter

Output exactly this template. Skip any section not applicable. Maximum 1 page.

```
# Project Charter: [Name]

## Objective
[One sentence. Problem + user.]

## MVP Scope (Must)
- [Feature 1]
- [Feature 2]
- [Feature 3]

## Out of Scope (Won't -- explicit)
- [Exclusion 1]
- [Exclusion 2]

## Actors
| Actor | Device | Access |

## Modules
| Module | Responsibility | Priority | Phase |

## Roadmap
| Phase | Duration | Features | Depends On |

## Top Risks
| Risk | Type | Probability | Impact | Mitigation |

## Stack (inferred/suggested)
| Layer | Tech | Why |

## Key Decisions (ADR candidates)
| Decision | Options Considered | Choice | Rationale |
```

### Step 3: Flag Gaps

After the charter, append a `## Undefined` section listing what's still unknown:
```
## Undefined
- [ ] [Gap that needs decision]
```

---

## Format Rules

- Tables for every section. No paragraph blocks.
- Risk probability: `High | Medium | Low` with concrete trigger conditions, not percentages.
- Roadmap durations in weeks: `5-6 weeks`, `3-4 weeks`.
- Feature IDs use module prefix: `ORD-01`, `MES-01`.
- Priority: `P0 (MVP) | P1 (Phase 2) | P2 (Phase 3)`.
- Stack rows include "Why" column with one-phrase rationale.
- Decisions table: each row is a candidate ADR with choice made.

## Actor device descriptions use concrete specs, not prose:
| Actor | Device | Access |
|-------|--------|--------|
| Mesero | Tablet 10", touch | Own orders, tables, catalog (read-only) |
| Admin | PC Desktop | Full access |

---

## What NOT to do

- No project charter template explanations. Output only the charter.
- No methodology discussions. No "we'll use Scrum with 2-week sprints".
- No role definitions ("Product Owner is responsible for...").
- No MoSCoW theory explanation. Just use Must/Should/Could/Won't as labels.
- No budget sections unless explicitly asked.
- No stakeholder mapping unless explicitly asked (that's a separate skill).
- No architecture diagrams. That belongs to agent-design.
- No user stories. That belongs to agent-spec.
