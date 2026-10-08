---
name: deep-analyze
description: "Deep-dive analysis of an initial proposal — research code implementation, produce an actionable roadmap and alternatives"
allowed-tools: Read, Grep, Glob, Bash(git:*), Bash(node:*), Write, Agent
---

# Deep Analyze

## Trigger

- Keywords: deep analyze, deep analysis, deep dive, roadmap, deep-analyze

## When NOT to Use

- Architecture advice only (use `/codex-architect`)
- Tech spec writing (use `/tech-spec`)
- Feasibility analysis (use `/feasibility-study`)

## Agent Dispatch

```
Agent({
  description: "Deep-dive analysis with actionable roadmap and alternatives",
  subagent_type: "solution-architect",
  prompt: `Perform a deep analysis of the following initial proposal.
Follow the analysis framework and output format defined in this skill.`
})
```

## Task

### Input

```
$ARGUMENTS
```

### Analysis Flow

#### Phase 1: Understand & Validate

1. Extract the core objectives of the initial proposal
2. Identify key assumptions (which may be wrong)
3. List technical points that need verification

#### Phase 2: Code Deep Dive

Research the existing codebase thoroughly. **Must verify**:
- Naming conventions
- DI injection patterns
- Error handling patterns
- Implementation patterns of similar features

#### Phase 3: Roadmap Output

Based on the research, produce:
1. Implementation steps (immediately actionable)
2. Key pseudocode (only core 1-3 lines, omit if not necessary)
3. Alternative comparison

## Output

```markdown
# [Proposal Name] Implementation Roadmap

## Proposal Validation
| Assumption | Verification Result | Impact |

## Code Research Summary
| Module | Existing Implementation | Reusable |

## Implementation Roadmap
### Step 1: [Title]
**Objective**: One sentence
**Files**: `src/xxx.ts` (modify/create)

## Alternatives
| Dimension | Option A (Recommended) | Option B |

## Risks & Mitigations
| Risk | Probability | Mitigation |

## Immediate Actions
1. [ ] First task
2. [ ] Second task
```

## Examples

```bash
/deep-analyze "Use Redis to cache token prices with TTL 5 minutes"
/deep-analyze docs/features/xxx/tech-spec.md
```
