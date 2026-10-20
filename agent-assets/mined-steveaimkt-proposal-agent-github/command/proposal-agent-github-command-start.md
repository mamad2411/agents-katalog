---
description: 유형 + 출력 형식 선택 후 8-Step 파이프라인 전체 실행
argument-hint: 테스트 XX
---

`제안요청서/$ARGUMENTS/` 를 분석해 제안서를 제작합니다.
`generate` 스킬(PM)을 오케스트레이터로 **8-Step 파이프라인**을 실행하세요.

## 진행 방식

모든 단계를 **하나씩 순차적으로** 진행합니다. 각 단계 완료 후
`.claude/rules/step-checklists.md` 의 컨펌 포맷으로 **체크리스트 + 결과 요약 + 확인 사항**을
제시하고, 사용자 컨펌 후 다음 단계로 넘어갑니다. 자동 연속 실행 금지.

---

## Step 0: 킥오프

AskUserQuestion으로 **두 가지를 함께** 질문합니다.

1. **제안서 유형**
   - 입찰 제안서 — RFP(제안요청서) 기반
   - 마케팅 제안서 — 마케팅 플랜/브리핑 기반
   - 캠페인 제안서 — `campaign_brief.md` 기반 (`/brainstorm` 산출물)

2. **출력 형식**
   - HTML→Figma — `preview.html` + 개별 슬라이드 (기본)
   - PPTX — `designer` 스킬로 직접 생성

그다음 **스마트 시작** 판정: `.claude/rules/smart-start.md` 의 감지 순서를 따르고,
결과를 사용자에게 먼저 알립니다.

마지막으로 `제안요청서/$ARGUMENTS/` 내 파일 목록을 제시합니다.

---

## Step 1: 분석 → `analyst` 스킬

- (입찰) `제안요청서/$ARGUMENTS/` 내 PDF 분석 → `output/$ARGUMENTS/rfp_analysis.md`
- (마케팅) PDF 분석 또는 브리핑 수집 → `output/$ARGUMENTS/mkt_analysis.md`
- (캠페인) 건너뜀 — Step 3으로

체크리스트 1-1~1-9 검증 후 컨펌 요청.

---

## Step 2: 리서치 → `research` 스킬

4개 병렬 리서처(시장환경 / 경쟁벤치마킹 / 타겟인사이트 / BP·KPI)를 동시 실행하고
통합 → `output/$ARGUMENTS/research_brief.md`

**모든 데이터에 출처(기관명/URL/연도) 필수** — 체크리스트 2-2.

체크리스트 2-1~2-5 검증 후 컨펌 요청.

---

## Step 3: 콘텐츠 기획 → `script` 스킬 ★

SPARK-6 프레임워크 + Win Theme 3개 + S-E-P + Action Title
→ `output/$ARGUMENTS/proposal_script.md`

**★ 반드시 사용자 승인 필요 ★**
- 목차, Win Theme, 슬라이드 수, Part별 비중, KPI 요약을 제시
- "승인" / "진행해" → Step 4
- 수정 요청 시 반영 후 재확인

체크리스트 3-1~3-13 검증.

---

## Step 4: 디자인 전략 → `design-analyzer` + `visualizer` 스킬

- (4a) `디자인 레퍼런스/` 확인 → `output/$ARGUMENTS/design_analysis.md`
  - 파일 있으면 분석 / 비어있으면 기본 디자인 시스템 적용
- (4b) 도식화 전략 → `output/$ARGUMENTS/visualization_strategy.md`
  - 패턴은 `.claude/skills/visualizer/references/diagram-patterns.md` (40종)에서 선택

체크리스트 4-1~4-8 검증 후 컨펌 요청.

---

## Step 5: 제작

### HTML→Figma 모드
```bash
python3 src/converters/script_to_json.py "output/$ARGUMENTS/proposal_script.md" \
    --viz-strategy "output/$ARGUMENTS/visualization_strategy.md" \
    --design-analysis "output/$ARGUMENTS/design_analysis.md"

python3 src/generators/html_slide_renderer.py "output/$ARGUMENTS/proposal_slides.json" \
    --output-dir "output/$ARGUMENTS/"
```
출력: `proposal_slides.json` · `slides/slide_NN.html` · `preview.html`

### PPTX 모드
`designer` 스킬로 `output/$ARGUMENTS/generate_제안서.py` 생성 후 실행.
규칙은 `.claude/rules/pptx-rules.md` 참조.

결과물을 열고 체크리스트 5-1~5-12 검증 후 컨펌 요청.

---

## Step 6: 검수 → `qc` 스킬

7개 전문 QA(layout / shape / diagram / typography / color / content / interaction)를
**2라운드** 실행하고 CRITICAL·WARNING 건수를 보고합니다.

체크리스트 6-1~6-6 검증 후 수정 여부 컨펌 요청.

---

## Step 7: 수정 & 최종 납품

- CRITICAL 즉시 수정 (0건이 될 때까지)
- WARNING은 사용자 판단 후 수정
- 최종 결과물 열기 + 산출물 전체 목록 제시

체크리스트 7-1~7-4 검증 후 완료 컨펌.
