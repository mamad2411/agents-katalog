---
name: engineering-strategy
category: dx
description: "Engineering Strategy 가이드 — 기술 전략 수립: Tech Radar, Build vs Buy, OKR, 로드맵, 기술 부채 관리 Use when working with dx 도메인의 패턴 / 구현 선택."
effort: low
deprecated: false
---

# Engineering Strategy 가이드

기술 전략 수립: Tech Radar, Build vs Buy, OKR, 로드맵, 기술 부채 관리

## Quick Reference (결정 트리)

```
전략적 의사결정?
    │
    ├─ 새 기술 도입 ──────────> Tech Radar 평가
    │       │
    │       └─ Adopt / Trial / Assess / Hold 판정
    │
    ├─ 만들기 vs 구매 ───────> Build vs Buy 분석
    │       │
    │       └─ 3단계: 초기 평가 → 5년 TCO → 전략 평가
    │
    ├─ 목표 설정 ─────────────> Engineering OKR
    │       │
    │       └─ 배포속도, 품질, 기술부채, DX 카테고리별
    │
    ├─ 분기 계획 ─────────────> Now / Next / Later
    │       │
    │       └─ 실행 중 / 다음 분기 / 미래 백로그
    │
    └─ 기술 부채 관리 ────────> 부채 레지스터 + RICE
            │
            └─ 분류 → 스코어링 → 스프린트 할당
```

---

## Tech Radar

### ThoughtWorks 모델

```
┌─────────────────────────────────────────────────────────────────┐
│                        Tech Radar                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│              4 Quadrants × 4 Rings                               │
│                                                                  │
│  Quadrants:                  Rings:                              │
│  ─────────                   ─────                               │
│  Techniques                  Adopt  ← 프로덕션 사용 권장         │
│  Tools                       Trial  ← 파일럿/PoC 단계           │
│  Platforms                   Assess ← 평가/조사 단계            │
│  Languages & Frameworks      Hold   ← 신규 사용 금지            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Ring 판정 기준

| Ring | 의미 | 판정 기준 | 예시 |
|------|------|----------|------|
| **Adopt** | 적극 채택 | 프로덕션 검증 완료, 팀 역량 확보 | Kubernetes, PostgreSQL |
| **Trial** | 시범 도입 | PoC 성공, 리스크 관리 가능 | NATS JetStream, Dagger |
| **Assess** | 평가 중 | 관심 기술, 조사/학습 단계 | WebAssembly Components |
| **Hold** | 사용 중단 | 대안이 더 우수, 레거시화 | jQuery, XML Config |

### Tech Radar 운영

```markdown
## Tech Radar 업데이트 프로세스

1. 분기별 리뷰 미팅 (Engineering Leads)
2. 각 Quadrant 담당자가 변경 제안
3. Ring 이동 시 ADR 작성 (근거 기록)
4. 전사 공유 (Backstage 또는 정적 사이트)

## 제안 템플릿
- 기술명: ...
- 현재 Ring: Assess → 제안 Ring: Trial
- 근거: PoC 결과, 벤치마크 데이터
- 리스크: 운영 복잡도, 학습 곡선
- 담당팀: ...
```

### 자체 Tech Radar 구축

```yaml
# tech-radar.yaml
quadrants:
  - name: Techniques
    items:
      - name: Trunk-Based Development
        ring: adopt
        description: "메인 브랜치 직접 커밋, 짧은 수명 브랜치"
      - name: Micro Frontends
        ring: trial
        description: "프론트엔드 독립 배포"

  - name: Tools
    items:
      - name: OpenTelemetry
        ring: adopt
        description: "관측성 표준"
      - name: Dagger
        ring: assess
        description: "프로그래머블 CI/CD"

  - name: Platforms
    items:
      - name: Kubernetes
        ring: adopt
      - name: Wasm Edge Runtime
        ring: assess

  - name: "Languages & Frameworks"
    items:
      - name: Go
        ring: adopt
      - name: Rust
        ring: trial
```

---

## Build vs Buy 분석

### 3단계 의사결정

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  1단계       │───>│  2단계       │───>│  3단계       │
│  초기 평가   │    │  TCO 비교    │    │  전략 평가   │
│              │    │  (5년)       │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
      │                   │                   │
      ▼                   ▼                   ▼
 핵심 차별화인가?     총 비용 비교        장기 전략 적합성
 시장에 솔루션       라이선스 + 인건비    벤더 종속 리스크
 있는가?             + 유지보수 + 기회비용  확장성/커스터마이징
```

### 1단계: 초기 평가

| 질문 | Build | Buy |
|------|-------|-----|
| 핵심 비즈니스 차별화 요소인가? | Build | - |
| 시장에 80%+ 요구사항 충족 솔루션이 있는가? | - | Buy |
| 내부 전문 인력이 충분한가? | Build | Buy |
| 빠른 출시가 최우선인가? | - | Buy |
| 장기 커스터마이징이 필수인가? | Build | - |

### 2단계: 5년 TCO 비교

```
Build TCO:
  초기 개발 비용         = 개발자 수 × 단가 × 개발 기간
  + 연간 유지보수        = 초기 비용의 15~20% × 5년
  + 인프라 비용          = 서버 + 모니터링 + 보안
  + 기회 비용            = 다른 프로젝트 못 한 가치
  ────────────────────
  = Build Total

Buy TCO:
  라이선스/구독비        = 연간 비용 × 5년
  + 통합/커스터마이징    = 초기 연동 개발 비용
  + 운영 비용            = 관리자 인건비
  + 벤더 종속 리스크     = 가격 인상, 서비스 중단 리스크
  ────────────────────
  = Buy Total
```

### 3단계: 전략 평가 (Decision Matrix)

| 기준 (가중치) | Build (1-5) | Buy (1-5) |
|-------------|-------------|-----------|
| 핵심 역량 일치 (30%) | ? | ? |
| TCO (25%) | ? | ? |
| 출시 속도 (20%) | ? | ? |
| 커스터마이징 유연성 (15%) | ? | ? |
| 벤더 리스크 (10%) | ? | ? |
| **가중 합계** | **?** | **?** |

```
Score = Σ (기준별 점수 × 가중치)
Build Score > Buy Score → Build 선택
차이 < 0.5 → 추가 PoC 필요
```

---

## Engineering OKR

### 카테고리별 OKR 예시

**배포 속도 (Delivery Speed)**

```
Objective: 배포 파이프라인 속도를 Elite 수준으로 개선한다
  KR1: 배포 빈도를 주 3회에서 일 1회 이상으로 증가
  KR2: Lead Time을 평균 5일에서 1일 이내로 단축
  KR3: 배포 자동화율을 60%에서 95%로 향상
```

**품질 (Quality)**

```
Objective: 프로덕션 안정성을 강화한다
  KR1: Change Failure Rate를 15%에서 5% 이하로 감소
  KR2: MTTR을 평균 4시간에서 1시간 이내로 단축
  KR3: P1 장애 발생 건수를 월 3건에서 1건 이하로 감소
```

**기술 부채 (Tech Debt)**

```
Objective: 핵심 서비스의 기술 부채를 체계적으로 감소시킨다
  KR1: 부채 레지스터 항목 중 High Priority 50% 해소
  KR2: 레거시 API v1 엔드포인트 70% 마이그레이션 완료
  KR3: 테스트 커버리지를 65%에서 80%로 향상
```

**개발자 경험 (DX)**

```
Objective: 개발자 생산성과 만족도를 향상시킨다
  KR1: 로컬 빌드 시간을 5분에서 1분 이내로 단축
  KR2: 신규 개발자 온보딩 기간을 3주에서 1주로 단축
  KR3: DXI(Developer Experience Index)를 60에서 75로 향상
```

### OKR 작성 원칙

| 원칙 | 설명 |
|------|------|
| 측정 가능 | "개선한다" → "X에서 Y로 변경" |
| 도전적 | 70% 달성이 적절한 목표 (Stretch Goal) |
| 시간 제한 | 분기 단위 OKR, 월 단위 체크인 |
| 결과 중심 | "CI 파이프라인 구축" → "배포 빈도 N회 달성" |

---

## 기술 전략 문서 (Strategy Doc)

### Will Larson 접근법

> "Design Doc 5개에서 공통점을 추출하면 전략이 된다"

```
┌─────────────────────────────────────────────────────────────┐
│                  Strategy Document 구조                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Diagnosis (진단)                                         │
│     현재 상황과 핵심 문제를 명확히 기술                        │
│     "우리 팀의 배포 속도는 업계 평균의 1/3이다"               │
│                                                              │
│  2. Guiding Policies (방침)                                  │
│     문제 해결을 위한 방향성과 원칙                             │
│     "모든 서비스는 독립 배포 가능해야 한다"                    │
│     "플랫폼 팀이 Golden Path를 제공한다"                      │
│                                                              │
│  3. Coherent Actions (실행 계획)                              │
│     방침을 구체화한 실행 항목                                  │
│     "Q1: CI/CD 파이프라인 표준화"                             │
│     "Q2: 서비스 메시 도입"                                    │
│     "Q3: 자동 카나리 배포 구축"                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 전략 문서 템플릿

```markdown
# Engineering Strategy: {영역}

## Diagnosis (현재 상황 진단)
- 핵심 문제: ...
- 근거 데이터: 메트릭, 설문 결과, 인시던트 데이터
- 영향: 비즈니스/팀에 미치는 영향

## Guiding Policies (방침)
1. [원칙 1]: 설명 및 근거
2. [원칙 2]: 설명 및 근거
3. [원칙 3]: 설명 및 근거

## Coherent Actions (실행 계획)
| 분기 | 액션 | 담당팀 | 성공 기준 |
|------|------|--------|----------|
| Q1 | ... | ... | ... |
| Q2 | ... | ... | ... |

## Success Metrics
- 6개월 후 목표: ...
- 12개월 후 목표: ...
```

---

## Now / Next / Later 로드맵

```
┌─────────────────┬─────────────────┬─────────────────┐
│      NOW        │      NEXT       │     LATER       │
│   (이번 분기)    │   (다음 분기)    │   (6개월+)      │
├─────────────────┼─────────────────┼─────────────────┤
│ 확정, 실행 중   │ 계획됨, 우선순위 │ 아이디어, 조사  │
│                 │ 결정됨          │ 필요            │
├─────────────────┼─────────────────┼─────────────────┤
│ - CI/CD 표준화  │ - 서비스 메시   │ - ML 파이프라인 │
│ - 모니터링 구축  │ - 자동 카나리   │ - Edge 배포    │
│ - API Gateway   │ - Chaos Eng     │ - WebAssembly  │
│   마이그레이션   │ - 부하 테스트   │   런타임       │
└─────────────────┴─────────────────┴─────────────────┘
```

| 시점 | 확실성 | 상세도 | 변경 빈도 |
|------|--------|--------|----------|
| Now | 높음 (90%+) | 에픽/스토리 수준 | 주간 |
| Next | 중간 (60~80%) | 에픽 수준 | 월간 |
| Later | 낮음 (< 50%) | 테마/이니셔티브 수준 | 분기별 |

---

## 기술 부채 관리

### 부채 분류

| 유형 | 정의 | 예시 |
|------|------|------|
| **의도적 (Strategic)** | 속도를 위해 의식적으로 선택 | "일단 모놀리스로, 나중에 분리" |
| **비의도적 (Accidental)** | 지식 부족이나 실수로 발생 | 잘못된 DB 스키마, 중복 코드 |
| **환경적 (Environmental)** | 외부 변화로 발생 | 프레임워크 EOL, 보안 패치 |

### 부채 레지스터

```markdown
# Tech Debt Register

| ID | 항목 | 유형 | 영향 서비스 | RICE | 상태 |
|----|------|------|-----------|------|------|
| TD-001 | 레거시 인증 모듈 교체 | Strategic | auth, user | 84 | In Progress |
| TD-002 | API v1 deprecation | Environmental | gateway | 72 | Planned |
| TD-003 | 중복 유틸리티 통합 | Accidental | 전체 | 36 | Backlog |
| TD-004 | Node 16 → 20 업그레이드 | Environmental | frontend | 65 | Planned |
```

### RICE 스코어링

```
RICE Score = (Reach × Impact × Confidence) ÷ Effort

Reach:      영향받는 개발자/서비스 수 (분기 기준)
Impact:     3(massive) / 2(high) / 1(medium) / 0.5(low) / 0.25(minimal)
Confidence: 100% / 80% / 50%
Effort:     person-weeks
```

**예시 계산:**

```
TD-001: 레거시 인증 모듈 교체
  Reach = 30 (전체 개발자)
  Impact = 3 (massive - 보안 + DX)
  Confidence = 80%
  Effort = 8.5 person-weeks
  RICE = (30 × 3 × 0.8) / 8.5 = 8.47 → 정규화 84
```

### 스프린트 할당 비율

```
┌─────────────────────────────────────────────┐
│              Sprint Capacity                 │
├─────────────────────────────────────────────┤
│                                              │
│  ██████████████  70% 기능 개발               │
│  ████           20% 기술 부채                │
│  ██             10% 실험/학습                │
│                                              │
└─────────────────────────────────────────────┘
```

| 상황 | 기능 | 부채 | 실험 |
|------|------|------|------|
| 기본 (건강한 코드베이스) | 70% | 20% | 10% |
| 부채 과다 (High Priority 많음) | 50% | 40% | 10% |
| 출시 압박 (런칭 임박) | 85% | 10% | 5% |
| 혁신 스프린트 | 50% | 10% | 40% |

---

## 연간/분기별 계획 프레임워크

```
┌───────────────────────────────────────────────────────────────┐
│                    Annual Planning Cycle                        │
├───────────────────────────────────────────────────────────────┤
│                                                                │
│  12월: 연간 Tech Strategy 수립                                 │
│    └─ Diagnosis → Policies → Actions 작성                      │
│    └─ Tech Radar 연간 리뷰                                     │
│                                                                │
│  분기 시작 (1월, 4월, 7월, 10월):                                │
│    └─ OKR 설정                                                 │
│    └─ Now/Next/Later 업데이트                                   │
│    └─ 부채 레지스터 리뷰 + RICE 재평가                          │
│                                                                │
│  분기 중간:                                                     │
│    └─ OKR 체크인 (진행률 리뷰)                                   │
│    └─ 로드맵 조정                                               │
│                                                                │
│  분기 종료:                                                     │
│    └─ OKR 회고 (달성률 + 학습)                                   │
│    └─ 메트릭 리뷰 (DORA, DXI)                                   │
│    └─ 다음 분기 계획 시작                                        │
│                                                                │
└───────────────────────────────────────────────────────────────┘
```

---

## Anti-Patterns

| 안티패턴 | 문제 | 해결 |
|----------|------|------|
| Tech Radar 없이 기술 도입 | 일관성 없는 기술 스택, 유지보수 비용 증가 | Ring 평가 후 도입 |
| Build vs Buy 감으로 결정 | TCO 과소평가, 숨은 비용 발생 | 3단계 분석 필수 |
| OKR에 Output만 기재 | "CI 구축" vs "배포 빈도 N회" | Outcome 중심 KR |
| 기술 부채 무시 | 개발 속도 저하, 장애 증가 | 20% 스프린트 할당 |
| 로드맵이 날짜+기능 목록 | 변경 불가, 압박만 증가 | Now/Next/Later 형식 |
| 전략 문서 1회 작성 후 방치 | 현실과 괴리 | 분기별 리뷰 + 업데이트 |

---

## Sources

- ThoughtWorks Technology Radar: https://www.thoughtworks.com/radar
- Will Larson, "An Elegant Puzzle: Systems of Engineering Management" (2019)
- Will Larson, "Staff Engineer" (2021) — Strategy chapter
- Google re:Work OKR Guide: https://rework.withgoogle.com/guides/set-goals-with-okrs/
- Martin Fowler, "Technical Debt Quadrant" (2009)
- Intercom, "RICE Scoring" framework
- Shape Up (Basecamp): https://basecamp.com/shapeup

**관련 skill**: `/rfc-adr`, `/dx-metrics`, `/team-topologies`, `/product-thinking`
