---
name: naver-unmet-need-item-survey
description: Use this skill when the user asks to start a Naver Blog review workflow by organizing campaign requirements and extracting product-detail information before drafting. Trigger on phrases such as "/naver unmet need &item Survey", "캠페인 요구사항 먼저 정리", "상세페이지 제품 정보 추출", "네이버 리뷰 시작 전 조사", "체험단 미션 정리", product review planning, sponsored review requirements, SmartStore product page analysis, or any task that needs a reusable pre-writing survey for Korean Naver Blog posts.
---

# Naver Unmet Need & Item Survey

## Purpose

Prepare the pre-writing survey before a Korean Naver Blog review. Do not draft the final review yet unless the user asks. First separate the campaign obligations from the product story, then turn them into a writing-ready brief.

Use this skill before `naver-review-writing-ko` and `naver-posting-audit-ko`.

## Workflow

1. Open and inspect the campaign page.
2. Open and inspect the product page or attached 상세페이지 images.
3. Extract campaign requirements exactly.
4. Extract product information and selling points.
5. Identify the reader's unmet need.
6. Convert findings into a blog-review planning brief.
7. Flag missing information, conflicts, and compliance risks.

When the page content may have changed or requires login, state what was verified from accessible text and what still needs manual confirmation from screenshots, attachments, or the logged-in page.

## Campaign Requirement Survey

Create this table first.

```text
| 항목 | 내용 |
|---|---|
| 캠페인명 | |
| 리뷰 채널 | |
| 캠페인 유형 | 방문형/배송형/기자단/구매평/숏폼 |
| 제공 내역 | |
| 제공가/가격 | |
| 모집 인원 | |
| 모집 기간 | |
| 리뷰어 발표 | |
| 리뷰 등록 기간 | |
| 캠페인 마감 | |
| 원고 분량 | |
| 사진 수 | |
| 영상/움짤 | |
| 제목 필수 조건 | |
| 본문 필수 조건 | |
| 링크 삽입 | |
| 공정위/스폰서배너 | |
| 유지 기간 | |
| 패널티/주의사항 | |
```

Then summarize the requirements as a checklist:

```text
## 반드시 지킬 것
- [ ] 제목에 [필수 키워드/업체명] 포함
- [ ] 본문에 [필수 키워드] 자연스럽게 반복
- [ ] 사진 [n]장 이상
- [ ] 영상/움짤 [n]개
- [ ] 링크 삽입
- [ ] 스폰서배너/대가성 문구 삽입
- [ ] 등록기간 준수
```

If requirements conflict, prefer the stricter condition. Example: mission card says 10 images but detail text says 15 images, plan for 15 images.

## Keyword Survey

Separate keyword obligations from optional tags.

```text
| 구분 | 키워드 |
|---|---|
| 제목 필수 키워드 | |
| 메인키워드 | |
| 서브키워드 | |
| 본문 반복 필요 키워드 | |
| 해시태그 필수 | |
| 업체명/브랜드명 | |
```

Add usage guidance:

- Put the strongest main keyword at the front of the title when required.
- Use exact spacing from the campaign page.
- Insert at least 3 required keywords into natural sentences 2-3 times only when the campaign asks for repetition.
- Do not keyword-stuff; keep the first three lines readable.

## Product Detail Survey

Extract product information from the official product page, 상세페이지 images, campaign text, and user-supplied photos.

```text
| 항목 | 내용 |
|---|---|
| 제품명 | |
| 브랜드/업체명 | |
| 제품군 | |
| 가격/제공가 | |
| 구매처 | |
| 구성/파일/옵션 | |
| 사용 대상 | |
| 사용 환경 | |
| 핵심 기능 | |
| 디자인 포인트 | |
| 소재/성분/스펙 | |
| 사용 방법 | |
| 차별점 | |
| 주의사항 | |
```

For digital goods such as GoodNotes templates, include:

- supported apps: GoodNotes, Noteshelf, Notability, PDF annotation apps when verified.
- supported devices: iPad, Galaxy Tab, tablet, PDF-compatible devices when verified.
- file delivery method and download period if the campaign states it.
- page count, hyperlink/index structure, stickers, covers, color options, planner/note templates when visible.
- realistic use cases: study planner, university notes, exam prep, 임고/고시, daily planning, diary, lecture notes.

## Unmet Need Survey

Before writing, identify the reader problem that makes the product worth reviewing.

```text
| 독자 고민 | 리뷰에서 연결할 제품 포인트 |
|---|---|
| 기존 노트/플래너가 흩어져 관리가 어려움 | 올인원 구성, 인덱스/하이퍼링크 |
| 굿노트속지를 매번 따로 찾기 번거로움 | 한 파일 안에서 여러 템플릿 사용 |
| 공부 계획과 필기를 같이 정리하고 싶음 | 스터디 플래너 + 필기 노트 구성 |
| 예쁜 디자인도 중요함 | 파스텔컬러, 20-30대 선호 디자인 |
| 아이패드/갤럭시탭 활용도를 높이고 싶음 | 디지털노트, PDF 기반 활용 |
```

Use this to plan the opening motivation. Start from the reader's situation, not from "제품을 제공받았다" or "사진을 찍었다".

## Item Survey

Turn product facts into review angles.

```text
| 리뷰 각도 | 쓸 내용 |
|---|---|
| 첫인상 | 컬러, 화면 구성, 파일 정돈감 |
| 설치/적용 | 다운로드, 굿노트/노트쉘프 불러오기 |
| 사용성 | 인덱스 이동, 페이지 넘김, 필기 공간 |
| 디자인 | 파스텔톤, 20-30대 여성 취향, 깔끔함 |
| 실사용 장면 | 공부 계획, 강의 필기, 데일리 플래너 |
| 장점 | 반복 사용성, 구성 다양성, 정리 편의 |
| 아쉬움 | 처음 불러오기/앱별 차이/디지털 필기 적응 |
| 추천 대상 | 대학생, 고시생, 임고생, 갓생 루틴러 |
```

## Output Format

Use this exact order unless the user asks otherwise:

```text
## 결론
## 캠페인 요구사항 정리
## 키워드 요구사항
## 상세페이지 제품 정보 추출
## Unmet Need 정리
## Item Survey 정리
## 리뷰 작성 시 반드시 넣을 포인트
## 사진/영상 구성 초안
## 주의할 점
## 다음 단계
```

Keep this stage concise but complete. The result should be ready to hand off into a review draft.

## Review Planning Rules

- Preserve exact campaign terms, dates, counts, and keywords.
- Use absolute dates when the current date affects deadline interpretation.
- If a campaign has already ended or the review period is near, explicitly flag it.
- Distinguish confirmed facts from inferred recommendations.
- Cite source links used at the end when web pages were inspected.
- Avoid copying 상세페이지 marketing copy verbatim into the future review.
- Do not invent specs such as page count, app compatibility, or price unless the source confirms them.
- For sensitive claims, convert claims into personal-use phrasing during the later review-writing step.

## Handoff To Drafting

After this survey, ask for or inspect the review photos/videos. Then use `naver-review-writing-ko` to draft the post and `naver-posting-audit-ko` to validate it.
