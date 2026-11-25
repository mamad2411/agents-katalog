---
name: refactoring-principles
category: dx
description: "Refactoring Principles — 리팩토링 기본 원칙, 코드 스멜 식별, 점진적 개선 전략. Use when working with dx 도메인의 패턴 / 구현 선택."
effort: low
deprecated: false
---

# Refactoring Principles

리팩토링 기본 원칙, 코드 스멜 식별, 점진적 개선 전략.

## Quick Reference

```
리팩토링 결정 트리
    │
    ├─ 코드 스멜 발견 ─────> 코드 스멜 카탈로그 참조
    │
    ├─ 구조 개선 필요 ─────> SOLID 원칙 적용
    │
    ├─ 대규모 변경 ────────> 점진적 전략 (Strangler Fig)
    │
    └─ 안전한 리팩토링 ────> 테스트 먼저, 작은 커밋
```

---

## CRITICAL: 리팩토링 황금률

| 원칙 | 설명 |
|------|------|
| **테스트 먼저** | 리팩토링 전 테스트 커버리지 확보 |
| **작은 단위 커밋** | 하나의 리팩토링 = 하나의 커밋 |
| **동작 변경 금지** | 리팩토링은 동작을 유지하면서 구조만 개선 |
| **롤백 가능** | 언제든 이전 상태로 복귀 가능해야 함 |

---

## 리팩토링 타이밍 가이드

### 언제 리팩토링 해야 하는가?

| 타이밍 | 설명 | 적용 |
|--------|------|------|
| **Rule of Three** | 3번째 반복할 때 시작 | 중복 코드 발견 시 |
| **Boy Scout Rule** | 코드 만질 때마다 조금씩 개선 | 모든 커밋에 |
| **기능 추가 전** | 새 기능 전에 기존 코드 정리 | 기술 부채 방지 |
| **코드 리뷰 중** | 피어 리뷰에서 발견한 개선점 | PR 리뷰 |
| **버그율 낮을 때** | 디버깅과 분리하여 진행 | 안정기 |

### Sprint 할당 전략

```
┌─────────────────────────────────────────────┐
│            Sprint 시간 배분                 │
├─────────────────────────────────────────────┤
│  ████████████████████  60% 새 기능 개발    │
│  ██████              20% 버그 수정          │
│  ██████              20% 리팩토링/기술부채   │
└─────────────────────────────────────────────┘
```

### TDD Red-Green-Refactor 사이클

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│   RED    │────▶│  GREEN   │────▶│ REFACTOR │
│ 실패하는 │     │ 통과하는 │     │ 정리하는 │
│ 테스트   │     │ 코드     │     │ 코드     │
└──────────┘     └──────────┘     └─────┬────┘
     ▲                                  │
     └──────────────────────────────────┘
```

### 리팩토링 하지 말아야 할 때

| 상황 | 이유 |
|------|------|
| 마감 직전 | 새 버그 유입 위험 |
| 버그 수정과 동시에 | 원인 파악 어려움 |
| 전면 재작성이 나을 때 | 시간 낭비 |
| 테스트 없는 코드 | 회귀 검증 불가 |

---

## 코드 스멜 카탈로그

### Bloaters (비대해진 코드)

| 코드 스멜 | 증상 | 해결 방법 |
|----------|------|----------|
| **Long Method** | 20줄 이상 | Extract Method |
| **Large Class** | 300줄 이상 | Extract Class |
| **Long Parameter List** | 4개+ 파라미터 | Parameter Object |
| **Primitive Obsession** | int/String으로 도메인 표현 | Value Object |
| **Data Clumps** | 같은 필드 그룹 반복 | Extract Class |

### Object-Orientation Abusers

| 코드 스멜 | 증상 | 해결 방법 |
|----------|------|----------|
| **Switch Statements** | 타입별 분기 반복 | Polymorphism |
| **Refused Bequest** | 상속받고 사용 안함 | Replace with Delegation |
| **Alternative Classes** | 같은 기능 다른 인터페이스 | Unify Interface |

### Change Preventers

| 코드 스멜 | 증상 | 해결 방법 |
|----------|------|----------|
| **Divergent Change** | 한 클래스가 여러 이유로 변경 | Extract Class |
| **Shotgun Surgery** | 한 변경이 여러 클래스 수정 필요 | Move Method |
| **Parallel Inheritance** | 클래스 추가 시 다른 계층도 추가 | Collapse Hierarchy |

### Dispensables (불필요한 것들)

| 코드 스멜 | 증상 | 해결 방법 |
|----------|------|----------|
| **Duplicate Code** | 동일 코드 2곳+ | Extract Method/Class |
| **Dead Code** | 사용되지 않는 코드 | Remove |
| **Lazy Class** | 하는 일이 너무 적음 | Inline Class |
| **Speculative Generality** | "나중에 필요할" 코드 | Remove |

### Couplers

| 코드 스멜 | 증상 | 해결 방법 |
|----------|------|----------|
| **Feature Envy** | 다른 클래스 데이터 과다 사용 | Move Method |
| **Inappropriate Intimacy** | 클래스 간 과도한 결합 | Extract Class |
| **Message Chains** | a.b().c().d() 체인 | Hide Delegate |
| **Middle Man** | 위임만 하는 클래스 | Remove Middle Man |

---

## SOLID 원칙 적용

### S: Single Responsibility (단일 책임)

```
신호: 클래스 설명에 "그리고"가 들어감

Before: UserService가 인증, 프로필, 알림 모두 처리
After:  AuthService, ProfileService, NotificationService 분리
```

### O: Open/Closed (개방/폐쇄)

```
신호: 새 기능 추가 시 기존 코드 수정 필요

Before: switch문으로 결제 타입 분기
After:  PaymentProcessor 인터페이스 + 구현체 추가
```

### L: Liskov Substitution (리스코프 치환)

```
신호: 하위 타입이 상위 타입 계약 위반

Before: Rectangle.setWidth() 호출 시 Square가 예상치 못한 동작
After:  별도 Shape 인터페이스로 분리
```

### I: Interface Segregation (인터페이스 분리)

```
신호: 인터페이스 구현 시 빈 메서드 존재

Before: Worker 인터페이스에 eat(), work(), sleep() 모두 포함
After:  Workable, Eatable 인터페이스 분리
```

### D: Dependency Inversion (의존성 역전)

```
신호: 상위 모듈이 하위 모듈에 직접 의존

Before: OrderService가 MySQLRepository 직접 생성
After:  OrderService가 OrderRepository 인터페이스에 의존
```

---

## 점진적 리팩토링 전략

### Strangler Fig Pattern

레거시를 점진적으로 새 시스템으로 교체:

```
┌─────────────────────────────────────────────┐
│  Phase 1: 레거시 앞에 Facade 배치           │
│  ┌─────────┐    ┌─────────┐                │
│  │ Facade  │───▶│ Legacy  │                │
│  └─────────┘    └─────────┘                │
├─────────────────────────────────────────────┤
│  Phase 2: 일부 기능을 새 시스템으로         │
│  ┌─────────┐    ┌─────────┐                │
│  │ Facade  │───▶│ Legacy  │                │
│  └────┬────┘    └─────────┘                │
│       └────────▶┌─────────┐                │
│                 │   New   │                │
│                 └─────────┘                │
├─────────────────────────────────────────────┤
│  Phase 3: 레거시 제거                       │
│  ┌─────────┐    ┌─────────┐                │
│  │ Facade  │───▶│   New   │                │
│  └─────────┘    └─────────┘                │
└─────────────────────────────────────────────┘
```

### Branch by Abstraction

1. 추상화 레이어 도입
2. 기존 구현을 추상화 뒤로 이동
3. 새 구현 병렬 개발
4. 점진적으로 새 구현으로 전환
5. 기존 구현 제거

---

## 테스트 주도 리팩토링

### 특성 테스트 (Characterization Test)

레거시 코드의 현재 동작을 기록:

```java
@Test
void characterizeCurrentBehavior() {
    // 레거시 코드의 실제 출력을 테스트로 기록
    LegacyCalculator calc = new LegacyCalculator();

    // 현재 동작 확인 (예상이 아닌 실제 값)
    assertEquals(42, calc.compute(10, 5));  // 이게 맞든 틀리든 현재 동작
}
```

### Golden Master

출력 전체를 스냅샷으로 저장:

```java
@Test
void goldenMasterTest() {
    String output = legacyReport.generate(testData);

    // 첫 실행: 결과를 golden-master.txt에 저장
    // 이후: 저장된 결과와 비교
    assertMatchesGoldenMaster("golden-master.txt", output);
}
```

---

## 리팩토링 우선순위

### 우선순위 공식

```
우선순위 = 변경빈도 × 복잡도 × 버그빈도
```

| 요소 | 측정 방법 |
|------|----------|
| 변경빈도 | `git log --oneline <file> \| wc -l` |
| 복잡도 | Cyclomatic Complexity 도구 |
| 버그빈도 | 이슈 트래커 연결 |

### Hot Spot 분석

```bash
# 가장 많이 변경된 파일
git log --name-only --format='' | sort | uniq -c | sort -rn | head -20

# 특정 기간 내 변경 빈도
git log --since="6 months ago" --name-only --format='' | sort | uniq -c | sort -rn
```

---

## Anti-Patterns

| Anti-Pattern | 문제 | 해결 |
|--------------|------|------|
| Big Bang 리팩토링 | 한 번에 너무 많은 변경 | 작은 단위로 분할 |
| 테스트 없는 리팩토링 | 회귀 버그 발생 | 테스트 먼저 작성 |
| 리팩토링 + 기능 추가 | 문제 원인 파악 어려움 | 분리하여 커밋 |
| 완벽주의 | 끝나지 않는 리팩토링 | 충분히 좋으면 중단 |
| 문서화 없는 리팩토링 | 변경 의도 불명확 | 커밋 메시지에 기록 |

---

## 체크리스트

### 리팩토링 전

- [ ] 테스트 커버리지 충분한가?
- [ ] 현재 코드가 동작하는가?
- [ ] 변경 범위가 명확한가?
- [ ] 롤백 계획이 있는가?

### 리팩토링 중

- [ ] 하나의 리팩토링만 진행 중인가?
- [ ] 기능 변경 없이 구조만 바꾸는가?
- [ ] 테스트가 계속 통과하는가?

### 리팩토링 후

- [ ] 모든 테스트 통과하는가?
- [ ] 커밋 메시지에 리팩토링 유형 기록했는가?
- [ ] 코드 리뷰 요청했는가?

---

**관련 skill**: `/refactoring-go`, `/refactoring-spring`
