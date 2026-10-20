---
description: proposal_script.md → JSON + HTML 슬라이드 렌더링 (Step 5)
argument-hint: 테스트 XX
---

`output/$ARGUMENTS/proposal_script.md` 를 JSON v2.0으로 변환하고 HTML을 렌더링합니다.
`convert` 스킬을 사용하세요.

## 1. 전제 확인

- `output/$ARGUMENTS/proposal_script.md` — 없으면 중단:
  "먼저 `/script $ARGUMENTS` 로 스크립트를 작성해주세요."
- `output/$ARGUMENTS/visualization_strategy.md` — 없으면 경고 후 진행
  (도식화 전략 없이 변환하면 layout_hint가 비어 품질이 떨어집니다.
   `/design $ARGUMENTS` 를 먼저 권합니다.)

## 2. JSON 변환

```bash
python3 src/converters/script_to_json.py "output/$ARGUMENTS/proposal_script.md" \
    --viz-strategy "output/$ARGUMENTS/visualization_strategy.md" \
    --design-analysis "output/$ARGUMENTS/design_analysis.md"
```

## 3. 변환 검증

체크리스트 5-1~5-7 로 확인:
- 슬라이드 수 = 스크립트 슬라이드 수 (5-1)
- Win Theme 3개 파싱 (5-2)
- S-E-P 분리: story / evidence[] / promise (5-3)
- Evidence 출처 분리: text + source (5-4)
- design_intent 채움률 80%+ (5-5)
- layout_hint가 도식화 전략과 매칭 (5-6)

불일치가 있으면 수정 후 재변환.

## 4. HTML 렌더링

```bash
python3 src/generators/html_slide_renderer.py "output/$ARGUMENTS/proposal_slides.json" \
    --output-dir "output/$ARGUMENTS/"
```

출력: `slides/slide_01.html` ~ `slide_NN.html` + `preview.html`

체크리스트 5-8~5-12 확인 (슬라이드 수 일치, 텍스트 보존, 16:9, 폰트).

## 5. 결과 안내

`preview.html` 을 열고 생성 파일 목록을 제시합니다.
다음 단계로 `/r $ARGUMENTS` (QC 검수)를 안내하세요.
