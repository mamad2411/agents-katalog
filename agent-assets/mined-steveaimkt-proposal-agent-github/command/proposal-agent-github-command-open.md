---
description: 산출물 열기 (pptx · preview.html · md 전체)
argument-hint: 테스트 XX
---

`output/$ARGUMENTS/` 의 결과물을 엽니다.

## 절차

1. `output/$ARGUMENTS/` 내 파일을 유형별로 목록화합니다.

| 유형 | 파일 |
|------|------|
| 최종 산출물 | `*.pptx` · `preview.html` |
| 중간 산출물 | `proposal_slides.json` · `slides/*.html` |
| 문서 | `rfp_analysis.md` · `research_brief.md` · `proposal_script.md` · `visualization_strategy.md` · `design_analysis.md` |

2. **최종 산출물을 우선** 엽니다 (`open` 명령).
   - `preview.html` 있으면 브라우저로
   - `.pptx` 있으면 기본 앱으로

3. 목록을 사용자에게 제시하고, 문서도 열지 물어봅니다.

파일이 하나도 없으면 안내: "아직 산출물이 없습니다. `/p $ARGUMENTS` 로 시작하세요."
