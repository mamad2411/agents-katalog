---
description: QC 검수 — 7개 전문 QA × 2라운드 (Step 6)
argument-hint: 테스트 XX
---

`output/$ARGUMENTS/` 산출물을 QC 검수합니다. `qc` 스킬을 사용하세요.

## 0. 모드 판정 (먼저 수행)

`output/$ARGUMENTS/` 를 확인해 검수 대상을 결정합니다.

| 감지 파일 | 모드 | 검수 대상 |
|----------|------|----------|
| `preview.html` / `slides/` | **HTML→Figma** | JSON + HTML 슬라이드 |
| `generate_제안서.py` | **PPTX** | 파이썬 스크립트 + PPTX |
| 둘 다 | 사용자에게 질문 | — |
| 둘 다 없음 | 중단 | "먼저 `/convert $ARGUMENTS` 또는 `/run $ARGUMENTS`을 실행해주세요" |

---

## 1. 자동 검증

### HTML→Figma 모드
```bash
python3 tools/validate_script.py "output/$ARGUMENTS/proposal_script.md"
```
- 슬라이드 수 일치, S-E-P 필드, Evidence 출처, Action Title 길이

### PPTX 모드
```bash
python3 tools/validate_script.py "output/$ARGUMENTS/generate_제안서.py"
python3 tools/visual_check.py "output/$ARGUMENTS/generate_제안서.py"
```
- Y좌표 넘침, Part별 분량, 레이아웃 다양성

CRITICAL은 즉시 수정 후 재검증. WARNING은 리포트에 기재.

---

## 2. 7개 전문 QA (2라운드)

각 QA를 **독립적으로** 수행하고, 1라운드 수정 후 2라운드로 재검증합니다.

| QA | 검수 항목 |
|----|----------|
| **layout** | 겹침·넘침·여백, 16:9(1920×1080) 준수 |
| **shape** | 도형 정렬·크기 일관성·간격 |
| **diagram** | 도식 유형이 콘텐츠 논리에 맞는가, `diagram-patterns.md` 40종 준수 |
| **typography** | 위계(Display/H1/H2/H3/Body), Pretendard, 자간·행간 |
| **color** | 팔레트 준수, 명도 계단 의미 일관성, 대비비 |
| **content** | SPARK-6 구조, S-E-P, Win Theme 3개 태깅, Action Title 15~35자, Evidence 출처 |
| **interaction** | 슬라이드 전환, 네비게이션, preview.html 동작 |

---

## 3. 결과 리포트

`.claude/rules/step-checklists.md` 의 Step 6 체크리스트(6-1~6-6)로 판정합니다.

```
═══ QC 검수 결과 ═══
🔴 CRITICAL: N건
🟡 WARNING : N건

[QA별 상세]
layout      — CRITICAL n / WARNING n
shape       — ...
...

판정: PASS / WARNING / FAIL
```

- **PASS**: CRITICAL 0건 + MUST 전부 달성
- **FAIL**: CRITICAL 1건 이상 → 수정 후 재검증

수정 여부를 사용자에게 컨펌 요청하세요.
