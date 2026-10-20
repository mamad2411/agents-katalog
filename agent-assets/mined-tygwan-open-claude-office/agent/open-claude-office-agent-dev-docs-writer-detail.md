# Dev Docs Writer - Full Implementation Detail

> Loaded on-demand. Header: [../dev-docs-writer.md](../dev-docs-writer.md)

## Document Templates

### 1. PRD.md
```markdown
# [Project Name] PRD

## Overview
- Project name, purpose, scope
- Target users and use cases

## Requirements
### Functional Requirements
- Core features with priority (P0, P1, P2)
- User stories

### Non-Functional Requirements
- Performance, Security, Compatibility

## Success Metrics
- KPIs and measurable outcomes
```

### 2. TECH-SPEC.md
```markdown
# [Project Name] Technical Specification

## Architecture
- System overview, Component diagram, Data flow

## Technology Stack
- Languages, frameworks, libraries, tools

## API Design
- Key interfaces, Data models

## Implementation Notes
- Critical algorithms, Performance, Security
```

### 3. PROGRESS.md
```markdown
# [Project Name] Development Progress

## Current Status
- Phase: [Name] | Progress: [X%] | Updated: [Date]

## Milestones
| Phase | Description | Status | Target |
|-------|-------------|--------|--------|

## In Progress / Blockers
```

### 4. CONTEXT.md
```markdown
# [Project Name] Context Summary

## Quick Reference
- One-paragraph summary, Key files, Dependencies

## Architecture Snapshot
- Main components, Entry points

## Current Focus
- Active area, Recent changes

## Token Optimization
- Essential files, Excludable paths
```

## Integration with context-optimizer
1. CONTEXT.md structured for context-optimizer consumption
2. Clear headers for easy parsing
3. "Quick Reference" for rapid loading
4. PROGRESS.md as living document for session continuity

## Integration with doc-splitter

For HIGH complexity → Phase structure:
```
docs/phases/phase-N/ → SPEC.md, TASKS.md, CHECKLIST.md
```

## Template Integration

Phase templates at `.claude/templates/phase/`:
```
SPEC.md, TASKS.md, CHECKLIST.md
```

Placeholder substitution:
```
{{PHASE_NUMBER}} → 1
{{PHASE_NAME}} → "기초 인프라 구축"
{{START_DATE}} → "2025-01-15"
```

## Quality Standards

### PRD.md
- [ ] 프로젝트 목적 한 문장으로 명확
- [ ] 핵심 기능 3-5개, 우선순위(P0-P2) 명시
- [ ] 성공 지표 측정 가능

### TECH-SPEC.md
- [ ] 아키텍처 다이어그램, 기술 스택 명시
- [ ] 주요 API 인터페이스, 데이터 모델

### PROGRESS.md
- [ ] 현재 Phase, 진행률 %, 마일스톤 테이블

### CONTEXT.md
- [ ] 100단어 이내 요약, 핵심 파일 5개 이내

### Validation Rules
```yaml
min_sections: 3
required_headers:
  PRD: ["Overview", "Requirements", "Success Metrics"]
  TECH_SPEC: ["Architecture", "Technology Stack"]
  PROGRESS: ["Current Status", "Milestones"]
  CONTEXT: ["Quick Reference", "Current Focus"]
max_file_size: 50KB
language: "ko"
```

## Using DISCOVERY.md Content

### Mapping
```yaml
Project Overview     → PRD Overview + CONTEXT Quick Reference
Requirements (P0-P2) → PRD Requirements
Technical Decisions  → TECH-SPEC Technology Stack
Complexity Assessment→ PROGRESS Phase Overview
Success Criteria     → PRD Success Metrics
```

### Verification Checklist
- [ ] PRD features match DISCOVERY.md exactly
- [ ] Tech stack matches discovery decisions
- [ ] Phase count matches complexity
- [ ] No assumptions added beyond discovered requirements

## Best Practices
1. DISCOVERY.md is source of truth: Never invent requirements
2. Concise over verbose: Clarity and brevity
3. Actionable content: Guides development
4. Living documents: Easy to update
5. Context-aware: Structured for AI optimization
6. Phase-aware: Consider doc-splitter for complex projects
