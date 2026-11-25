---
name: rfp_contents
description: 공고 카드의 콘텐츠 품질 점검 + LLM 자동 요약. 예산·기간 정확성, 본문 가독성, 키워드 매칭 정확성, 상세보기 가독성 5축 점검 + 카드에 본문+첨부 종합 150자 요약을 ai_summary 컬럼에 저장.
---

# rfp_contents — 공고 콘텐츠 품질 + LLM 카드 요약

## 목적

크롤링된 공고를 카드로 노출할 때 사용자가 곧장 판단할 수 있도록 콘텐츠 품질 보장:

1. **예산·기간 정확성** — 본문에 명시된 값 vs DB 추출값 일치
2. **본문 가독성** — 정부 공문 마커·표·잡음 정제 완료
3. **상세보기 가독성** — `body-head`·`body-note`·`body-line` 클래스로 시각 분리
4. **키워드 매칭 정확성** — 본문 + 첨부 본문 모두 매칭, boilerplate 거짓 양성 제거
5. **카드 요약 150자** — 본문+첨부 종합해서 Claude API 로 생성, `ai_summary` 컬럼 저장

## 실행 방법

```
사용자: "콘텐츠 점검해줘" / "rfp_contents"
→ Claude 가 scripts/audit_contents.py 실행 + 결과 보고

자동 (GitHub Actions monitor_crawler.yml 후속 단계):
  · 매시 크롤 후 신규 보안 공고에만 ai_summary 생성 (비용 최소화)
  · 활성 보안 공고 중 ai_summary IS NULL 인 row 만 처리
```

## 5축 점검 절차

### ① 예산·기간 정확성

```sql
-- budget_mw IS NOT NULL 인 row 중 budget_excerpt 가 본문에 있는지
SELECT id, budget_mw, budget_excerpt
FROM announcement
WHERE is_security AND NOT is_dismissed
  AND budget_mw IS NOT NULL
  AND budget_excerpt IS NOT NULL
  AND POSITION(budget_excerpt IN body) = 0   -- excerpt 가 본문에 없음
```

- **이상**: budget_excerpt 가 본문에 없는데 budget_mw 채워짐 → hallucination 의심
- **조치**: `python scripts/audit_contents.py --verify-budget` 으로 재추출

### ② 본문 가독성

```python
# build_static.make_readable() 가 정부 공문 마커 토큰 (§§HEAD§§/§§NOTE§§) 부여했는지
SELECT COUNT(*) FROM announcement
WHERE is_security AND NOT is_dismissed
  AND body LIKE '%§§HEAD§§%'   -- 토큰 있으면 OK
```

마커 토큰 부여율 < 50% 면 가독성 처리 누락. `build_static.make_readable()` 강화 필요.

### ③ 상세보기 가독성

정적 사이트는 이미 처리됨 — `body-head` (border-bottom 2px), `body-note` (좌측 border + 회색 배경), `body-line` (line-height 1.85). 코드 변경 시에만 회귀 점검.

### ④ 키워드 매칭 정확성

```sql
-- 첨부 본문 통합 안 된 활성 보안 공고 (KISA/NIPA 어댑터 회귀 감지)
SELECT source, COUNT(*) AS untouched
FROM announcement
WHERE is_security AND NOT is_dismissed
  AND source IN ('kisa','nipa')
  AND body NOT LIKE '%[첨부 본문]%'
  AND (deadline_at >= CURRENT_DATE::text
       OR (deadline_at IS NULL AND posted_at >= (CURRENT_DATE - 60)::text))
GROUP BY source
```

- KISA/NIPA 통합률 < 60% 면 회귀. `base.enrich_body_with_attachments()` 동작 확인.
- 평균 매칭 키워드 < 10개면 첨부 추출 실패 다수.

### ⑤ 카드 LLM 요약 (`ai_summary`)

#### 생성 조건
- `is_security = TRUE AND is_dismissed = FALSE`
- `ai_summary IS NULL`
- 활성 (마감 미래 OR 60일 내 등록)
- 본문 길이 ≥ 300자 (너무 짧으면 의미 있는 요약 X)

#### Claude API 호출
```python
model = "claude-haiku-4-5"   # 빠르고 저렴
system = (
  "당신은 한국 정부 R&D 공고를 카드에 표시할 짧은 요약을 만드는 전문가다. "
  "본문과 첨부 텍스트를 종합해 150자 이내 한국어로 요약. "
  "사업 본질·대상·예산·핵심 활동만. 안내문구·자격요건 제외. "
  "딱 한 문단, 마침표 포함."
)
user = f"제목: {title}\n발주: {agency}\n본문(첨부 포함):\n{body[:6000]}"
max_tokens = 200
```

#### 결과 저장
```sql
UPDATE announcement SET ai_summary = ? WHERE id = ?
```

#### 표시 위치 (정적 사이트)
- `build_static.py fetch_data()` 에서 `ai_summary` 가져옴
- `app.js renderCard()` — 카드 제목 아래, 점수 위에 회색 작은 글씨로 표시
- `ai_summary` 가 NULL 이면 폴백: `body_preview` (첫 150자 plain text)

## 비용 가드

- 활성 보안 공고만 처리 (만료/비활성 제외)
- `ai_summary IS NULL` 만 처리 — 한 번 생성하면 재호출 X
- claude-haiku-4-5 + 200 tokens = 호출당 약 0.5원 미만
- 350건 처리 ≈ 200원 1회성

## 회귀 회피

- `body` 가 변경되면 (예: KISA/NIPA 첨부 통합 백필) `ai_summary` 재생성 필요
- `--force` 옵션으로 NULL 무시하고 전체 재생성 가능
- 평소엔 NULL 만 처리 (idempotent)

## 관련 파일

- `scripts/audit_contents.py` — 5축 점검 + LLM 요약 생성
- `scripts/static_templates/app.js` — 카드 ai_summary 표시
- `scripts/build_static.py` — fetch_data 에 ai_summary 포함
- `src/rfp_targeter/drafter/` — Claude API 호출 패턴 참고
