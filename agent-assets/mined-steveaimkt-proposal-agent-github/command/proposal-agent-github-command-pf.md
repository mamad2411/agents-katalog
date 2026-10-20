---
description: HTML→Figma 모드로 8-Step 실행 (preview.html + 개별 슬라이드)
argument-hint: 테스트 XX
---

`제안요청서/$ARGUMENTS/` 를 분석한 후 HTML+Figma 제안서를 제작합니다.
`generate` 스킬로 **8-Step 파이프라인**을 **HTML→Figma 모드 고정**으로 실행하세요.

## 스마트 시작

`.claude/rules/smart-start.md` 의 감지 순서를 따릅니다.
판정 결과를 먼저 알린 뒤 해당 Step부터 시작하세요.

## Step 1~4

분석 → 리서치 → 기획(★승인) → 디자인 전략.
상세 절차는 `/start` 커맨드 정의를 따릅니다.

## Step 5: 제작

```bash
python3 src/converters/script_to_json.py "output/$ARGUMENTS/proposal_script.md" \
    --viz-strategy "output/$ARGUMENTS/visualization_strategy.md" \
    --design-analysis "output/$ARGUMENTS/design_analysis.md"

python3 src/generators/html_slide_renderer.py "output/$ARGUMENTS/proposal_slides.json" \
    --output-dir "output/$ARGUMENTS/"
```

출력:
- `output/$ARGUMENTS/proposal_slides.json`
- `output/$ARGUMENTS/slides/slide_01.html` ~ `slide_NN.html`
- `output/$ARGUMENTS/preview.html`

## Step 6: 검수

`qc` 스킬 — 7개 전문 QA × 2라운드.

## Step 7: 수정 & Figma 변환

1. CRITICAL 수정 (0건까지)
2. Figma 변환 안내 — `html.to.design` 플러그인으로 `preview.html` 임포트
3. Figma에서 미세 조정 (텍스트·색상·레이아웃)
4. 필요 시 Figma → PNG 추출 → PPTX 조립

상세는 `.claude/rules/html-figma-mode.md` 참조.
