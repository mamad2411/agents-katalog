# /harness:sync

> 코드↔Spec 양방향 동기화 + 엔트로피 스윕 + prototype→standard 승격.

## 사용법

```
/harness:sync                      # 전체 drift 탐지
/harness:sync --from code          # 코드 변경 → Spec 반영
/harness:sync --from spec          # Spec 변경 → 코드 반영 필요 안내
/harness:sync --promote            # prototype→standard 승격
```

## 오케스트레이션

### drift 탐지 (기본)

1. `scripts/detect-drift.mjs`
   - .harness/specs/ 의 AC 목록 vs 실제 코드/테스트 상태 비교
   - drift 유형: spec_without_impl, impl_without_spec, test_without_spec
   - JSON 리포트 출력

### 엔트로피 스윕

2. `scripts/entropy-sweep.mjs`
   - bypass 사용 현황 집계 (audit에서 bypass 이벤트 추적)
   - 오래된 TODO/FIXME 탐색
   - coverage 하락 추세 경고
   - 결과: 정리 필요 항목 리스트

### prototype→standard 승격 (`--promote`)

3. `scripts/promote.mjs`
   - prototype 모드 feature 목록 확인
   - 각 feature에 필수 산출물(spec, plan, test) 존재 여부 확인
   - 승격 가능 여부 판정

## 제약

- .harness/ 초기화 필요
- sync는 경고/안내만 — 자동 수정하지 않음 (User Sovereignty)
