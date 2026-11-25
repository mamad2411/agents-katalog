---
name: skill-rebuild
disableModelInvocation: true
description: 기존 스킬을 개선/재구성할 때 skill-creator의 전체 파이프라인(evals 생성, 벤치마크, description 최적화)을 강제하는 래퍼 스킬. "스킬 재구성", "스킬 개선", "스킬 리빌드", "skill rebuild", "스킬 다시 만들어", "스킬 업그레이드" 요청 시 반드시 이 스킬을 사용하라. 단순 SKILL.md 수정이 아닌 체계적인 파이프라인을 통해 스킬 품질을 보장한다.
---

# Skill Rebuild

기존 스킬을 개선/재구성할 때 **전체 파이프라인을 강제**하는 스킬.

skill-creator가 제공하는 eval → benchmark → description 최적화 프로세스를 생략 없이 실행한다.
각 단계는 체크포인트로 관리되며, 단계를 건너뛸 수 없다.

## 왜 이 스킬이 필요한가

스킬 재구성 요청 시 흔히 발생하는 문제:
- SKILL.md만 수정하고 evals를 생략
- 벤치마크 없이 "개선됐다"고 판단
- description 최적화를 빠뜨려 트리거 정확도가 떨어짐

이 스킬은 **모든 단계를 체크리스트로 강제**하여 이런 문제를 원천 차단한다.

---

## 파이프라인 (8단계, 건너뛸 수 없음)

### Step 1: 기존 스킬 분석

대상 스킬을 찾아 현재 상태를 파악한다.

1. 스킬 경로 탐지 (아래 순서로 검색):
   - 글로벌: `~/.claude/skills/{스킬명}/SKILL.md`
   - 프로젝트: `.claude/skills/{스킬명}/SKILL.md`
   - 플러그인 캐시: `~/.claude/plugins/cache/*/{스킬명}/*/skills/{스킬명}/SKILL.md`
2. SKILL.md 전문 읽기
3. 기존 evals, workspace 존재 여부 확인
4. 문제점/개선 방향 정리 → 사용자에게 공유

**체크포인트**: 사용자가 분석 결과와 개선 방향에 동의해야 다음 단계로 진행.

### Step 2: 기존 스킬 스냅샷

baseline 비교를 위해 현재 버전을 보존한다.

```bash
cp -r <skill-path> <workspace>/skill-snapshot/
```

이 스냅샷은 Step 4에서 `old_skill` baseline으로 사용된다.

**체크포인트**: 스냅샷 생성 확인.

### Step 3: skill-creator로 SKILL.md 개선

`skill-creator` 스킬을 호출하여 개선된 SKILL.md를 작성한다.

skill-creator의 "Improving the skill" 섹션 원칙을 따른다:
- 피드백을 일반화하여 과적합 방지
- 프롬프트를 간결하게 유지
- why를 설명하여 이해 기반 지시
- 반복 작업은 스크립트로 번들링

**체크포인트**: 개선된 SKILL.md 내용을 사용자에게 공유하고 승인 받기.

### Step 4: evals 생성 (필수)

테스트 케이스를 반드시 2-3개 이상 작성한다. 이 단계는 **절대 생략할 수 없다**.

1. `evals/evals.json` 작성 (스킬에 맞는 현실적인 프롬프트)
2. 사용자에게 테스트 케이스 공유 및 확인
3. 각 테스트 케이스에 대해 **두 개의 서브에이전트** 동시 실행:
   - `with_skill`: 개선된 스킬로 실행 → `iteration-N/eval-{ID}/with_skill/outputs/`
   - `old_skill`: 스냅샷(기존 스킬)으로 실행 → `iteration-N/eval-{ID}/old_skill/outputs/`

```
<workspace>/
├── skill-snapshot/          # Step 2에서 생성
├── evals/evals.json         # 테스트 케이스
└── iteration-1/
    ├── eval-{name}/
    │   ├── eval_metadata.json
    │   ├── with_skill/
    │   │   ├── outputs/
    │   │   └── timing.json
    │   └── old_skill/
    │       ├── outputs/
    │       └── timing.json
    ├── benchmark.json
    └── benchmark.md
```

**체크포인트**: evals.json이 존재하고 최소 2개 테스트 케이스가 포함되어 있어야 함.

### Step 5: 벤치마크 & 뷰어 (필수)

정량적 비교를 수행한다. 이 단계도 **절대 생략할 수 없다**.

1. **Grading** — 각 실행 결과에 대해 assertions 평가, `grading.json` 생성
2. **Aggregate** — 벤치마크 집계:
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```
3. **Analyst pass** — 벤치마크 데이터 분석 (non-discriminating assertions, 고분산 evals 등)
4. **Viewer 실행** — 사용자가 결과를 직접 확인:
   ```bash
   nohup python <skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "<skill-name>" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   ```

**체크포인트**: benchmark.json 생성 완료, 뷰어 실행 완료.

### Step 6: 사용자 리뷰 & 반복 개선

1. 사용자에게 뷰어 안내: "Outputs 탭에서 테스트 케이스별 결과를 확인하고, Benchmark 탭에서 정량 비교를 확인하세요."
2. `feedback.json` 읽기
3. 피드백 기반으로 SKILL.md 개선
4. **Step 4-5를 반복** (새 iteration 디렉토리에 결과 저장)

종료 조건:
- 사용자가 만족
- 피드백이 모두 비어있음 (모든 결과 양호)
- 의미 있는 개선이 더 이상 없음

**체크포인트**: 사용자가 최종 결과에 만족한다고 명시적으로 확인.

### Step 7: description 최적화 (필수)

트리거 정확도를 최적화한다. 이 단계도 **절대 생략할 수 없다**.

1. 트리거 eval 쿼리 20개 생성 (should-trigger 10개 + should-not-trigger 10개)
2. `assets/eval_review.html` 템플릿으로 사용자 리뷰
3. 최적화 루프 실행:
   ```bash
   python -m scripts.run_loop \
     --eval-set <trigger-eval.json> \
     --skill-path <skill-path> \
     --model <current-model-id> \
     --max-iterations 5 \
     --verbose
   ```
4. `best_description`을 SKILL.md frontmatter에 적용
5. 사용자에게 before/after 및 점수 보고

**체크포인트**: description이 최적화 결과로 업데이트됨.

### Step 8: 완료 체크리스트

모든 단계가 완료되었는지 최종 확인한다.

```
[ ] Step 1: 기존 스킬 분석 완료
[ ] Step 2: 기존 스킬 스냅샷 생성
[ ] Step 3: SKILL.md 개선 완료 (사용자 승인)
[ ] Step 4: evals.json 생성 (최소 2개 테스트 케이스)
[ ] Step 5: 벤치마크 실행 & 뷰어로 결과 확인
[ ] Step 6: 사용자 리뷰 피드백 반영
[ ] Step 7: description 최적화 (run_loop.py)
[ ] Step 8: 체크리스트 전체 통과
```

모든 항목이 체크되어야 스킬 재구성 완료로 간주한다.
하나라도 빠지면 해당 단계로 돌아가서 완료한다.

---

## 스킬 경로 자동 탐지

스킬명만 주어졌을 때 아래 순서로 검색한다:

1. `~/.claude/skills/{스킬명}/SKILL.md` (글로벌 사용자 스킬)
2. `.claude/skills/{스킬명}/SKILL.md` (프로젝트 로컬 스킬)
3. `~/.claude/plugins/cache/**/{스킬명}/*/skills/{스킬명}/SKILL.md` (플러그인 캐시)

찾지 못하면 사용자에게 경로를 직접 입력받는다.

## workspace 위치

`<skill-name>-workspace/` 디렉토리를 스킬 디렉토리의 sibling으로 생성한다.

예: `~/.claude/skills/my-skill/` → `~/.claude/skills/my-skill-workspace/`

---

## 주의사항

- skill-creator 스킬의 스크립트(`scripts/`, `eval-viewer/`, `agents/`, `assets/`)는 플러그인 캐시 경로에서 실행한다
- 스크립트 경로: `~/.claude/plugins/cache/claude-plugins-official/skill-creator/*/skills/skill-creator/`
- 실행 전 최신 캐시 버전을 사용하고 있는지 확인
