---
description: 진행 상황 확인 — 산출물 점검 후 다음 Step 안내
argument-hint: 테스트 XX
---

`output/$ARGUMENTS/` 의 진행 상황을 점검합니다. **읽기 전용 — 아무것도 생성하지 않습니다.**

## 1. 입력 확인

`제안요청서/$ARGUMENTS/` 파일 목록과 총 용량을 확인합니다.

## 2. 산출물 점검

각 파일의 존재 여부·크기·수정시각을 확인합니다. **0바이트는 없는 것으로 취급**합니다.

| Step | 산출물 | 상태 |
|------|--------|------|
| 1 | `rfp_analysis.md` / `mkt_analysis.md` | ✅ / ⬜ |
| 2 | `research_brief.md` | ✅ / ⬜ |
| 3 | `proposal_script.md` | ✅ / ⬜ |
| 3' | `campaign_brief.md` (캠페인 모드) | ✅ / ⬜ |
| 4 | `design_analysis.md` · `visualization_strategy.md` | ✅ / ⬜ |
| 5 | `proposal_slides.json` · `preview.html` / `*.pptx` | ✅ / ⬜ |

## 3. 판정 및 안내

`.claude/rules/smart-start.md` 의 감지 순서로 **다음 Step**을 판정하고,
실행할 커맨드를 제시합니다.

```
═══ $ARGUMENTS 진행 상황 ═══

입력 : 제안요청서/$ARGUMENTS/ — N개 파일
모드 : HTML→Figma / PPTX / 미정

[진행률] ███████░░░ Step 4 / 7 완료

✅ Step 1 분석      rfp_analysis.md        (12KB, 08-05 14:22)
✅ Step 2 리서치    research_brief.md      (28KB, 08-05 15:10)
✅ Step 3 기획      proposal_script.md     (64KB, 08-05 16:44)
⬜ Step 4 디자인    visualization_strategy.md 없음
⬜ Step 5 제작
⬜ Step 6 검수

→ 다음: /design $ARGUMENTS
```

## 4. 이상 징후 보고

아래에 해당하면 함께 알립니다.

- **순서 역전** — 하위 산출물이 상위보다 최신 (예: script보다 json이 오래됨 → 재변환 필요)
- **0바이트 파일**
- **고아 파일** — `slides/` 는 있는데 `proposal_slides.json` 이 없음
