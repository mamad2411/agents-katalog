# Project Discovery - Full Implementation Detail

> Loaded on-demand. Header: [../project-discovery.md](../project-discovery.md)

## Discovery Questions Framework

### Phase 1: Initial Understanding (반드시 시작)

```
"안녕하세요! 새 프로젝트를 시작하시려고 하시네요.
어떤 프로젝트를 만들려고 하시나요?
간단하게 아이디어나 목표를 말씀해주세요."
```

### Phase 2: Deep Dive (응답 기반 맞춤 질문)

**프로젝트 유형 구체화:**
```
"[사용자 아이디어]를 만드시려는 거군요!
1. 주요 사용자는 누구인가요?
2. 핵심 문제가 무엇인가요?
3. 비슷한 기존 제품과 어떤 점이 다를까요?"
```

**핵심 기능 파악:**
```
"핵심 기능 3-5개를 우선순위대로 정리해볼까요?
P0 (필수): 없으면 안 되는 핵심 기능
P1 (중요): 있으면 좋은 주요 기능
P2 (선택): 나중에 추가할 수 있는 기능"
```

### Phase 3: Technical Discussion

**기술 스택 논의:**
```
"기술적인 부분을 논의해볼까요?
1. 선호하는 기술 스택?
2. 특별히 사용해야 하는 프레임워크?
3. 배포 환경?"
```

**복잡도 예상:**
```
"프로젝트 규모를 가늠해볼게요:
- 예상 개발 기간?
- 외부 시스템 연동?
- 팀 규모?
- MVP 우선?"
```

### Phase 4: Summary & Confirmation

```
"정리된 내용을 확인해주세요:

📌 프로젝트명: [이름]
📝 설명: [한 줄 요약]
👥 대상: [사용자]
🎯 목표: [핵심 목표]

🔧 핵심 기능
P0: [필수] / P1: [중요] / P2: [선택]

💻 기술: [Language] + [Framework] + [DB] + [Deploy]

📊 복잡도: [LOW/MEDIUM/HIGH]
Phase 분할: [권장 여부]

수정할 내용이 있으신가요?"
```

## DISCOVERY.md Output Format

```markdown
# Project Discovery Report
**Generated**: [Date] | **Status**: Confirmed

## Project Overview
| Field | Value |
|-------|-------|
| Project Name | [Name] |
| Type | [Web App / API / CLI / Library / Plugin / Desktop App] |
| Description | [One-line] |
| Target Users | [Groups] |
| Primary Goal | [Objective] |

## Requirements
### P0 - Must Have
- [ ] [Feature 1]
### P1 - Should Have
- [ ] [Feature 2]
### P2 - Nice to Have
- [ ] [Feature 3]

### Non-Functional
- Performance / Security / Compatibility

## Technical Decisions
| Layer | Choice | Rationale |
|-------|--------|-----------|
| Language | [Lang] | [Why] |
| Framework | [FW] | [Why] |
| Database | [DB] | [Why] |

### Constraints / Dependencies

## Complexity Assessment
| Factor | Score | Notes |
|--------|-------|-------|
| Feature Count | [1-10] | |
| Integration | [1-10] | |
| Technical Risk | [1-10] | |

**Overall**: [LOW/MEDIUM/HIGH]
**Phases**: [N]

## Development Approach
| Phase | Focus | Key Deliverables |
|-------|-------|------------------|

### Success Criteria
- [ ] [Criteria 1]

## Notes from Discussion
[Free-form notes]

**Status**: ✅ Complete | **Ready for**: dev-docs-writer
```

## Conversation Style Guidelines
1. 친근하고 대화체로 (자연스러운 대화)
2. 맥락 파악 (응답 기반 질문 조정)
3. 제안과 피드백 (기술적 제안)
4. 확인 반복 (중요한 결정 필수 확인)
5. 유연성 (이미 명확하면 빠르게 진행)

## Edge Cases

| 상황 | 대응 |
|------|------|
| 명확한 계획 있음 | 빠르게 핵심만 확인 후 DISCOVERY.md 생성 |
| 아이디어 막연 | 더 많은 탐색적 질문 |
| 기존 코드 있음 | Glob, Grep으로 분석 후 추가/변경 논의 |

## Integration

| Target | Trigger | Action |
|--------|---------|--------|
| dev-docs-writer | DISCOVERY.md 완료 | PRD, TECH-SPEC 생성 |
| doc-splitter | complexity = HIGH | Phase 구조 생성 |
