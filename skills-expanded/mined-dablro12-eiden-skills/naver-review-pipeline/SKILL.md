---
name: naver-review-pipeline
description: Use this skill when the user says "/naver review pipeline" or asks to run the full Korean Naver Blog review workflow from campaign requirements and product pages through media-folder photo/video matching, review drafting, Notion-copyable HTML generation, and final campaign compliance audit. Trigger when the user provides or is expected to provide a campaign/review-requirements URL, product page URL, media folder path, photos/videos, sponsored review requirements, Naver SmartEditor output, or a request to orchestrate the existing Naver review skills end-to-end.
---

# Naver Review Pipeline

## Purpose

Run the full Naver Blog review workflow as an orchestrator. This skill coordinates these module skills:

1. `naver-unmet-need-item-survey`: campaign requirements, product facts, unmet need, item survey.
2. `naver-photo-review`: media-folder inventory, photo/video selection, role mapping, review-ready filenames.
3. `naver-review-writing-ko`: review structure, Korean draft, Naver Blog paragraph rhythm, Notion/HTML output.
4. `naver-posting-audit-ko`: final compliance and quality audit.

Use this skill to start a new review project cleanly. Do not reuse product-specific claims from prior reviews unless the new campaign actually matches them.

## Required Inputs

Ask for missing blockers before starting. The minimum useful inputs are:

```text
1. 캠페인/리뷰 요구사항 페이지 URL:
2. 상품 상세페이지 URL:
3. 사진/영상 폴더 경로:
4. 최종 결과물 형식: HTML / 원고만 / 사진 구성만
```

Helpful optional inputs:

```text
- 실제 사용 후기 메모:
- 강조하고 싶은 장점:
- 솔직하게 넣을 아쉬운 점:
- 사용 기간:
- 본인 상황/사용 환경:
- 원하는 제목 방향:
- 기존 참고 블로그 URL:
- 사진 목표: 10장/15장/20장 이상
- 영상 목표: 1개/움짤/화면녹화
```

If only one of the campaign URL or product URL is missing, proceed with the available source and flag the gap. If the media folder is missing, complete the survey and then output a required-shot checklist instead of pretending media was inspected.

## Intake Questions

When the user gives an incomplete request, ask at most these concise questions:

```text
1. 캠페인 요구사항 페이지 URL과 상품 페이지 URL을 둘 다 보내주실 수 있나요?
2. 사진/영상이 들어있는 폴더 경로가 있나요?
3. 최종 결과물은 노션 복붙용 HTML까지 만들까요, 아니면 요구사항/사진 구성까지만 할까요?
```

If the user already supplied those, do not ask again. Start the pipeline.

## Pipeline Order

### 1. Project Setup

Create or identify a main project folder. Prefer the media folder as the project folder when the user says to use it.

Expected outputs:

```text
project folder/
├── naver_review_assets/
├── media_inventory.json
├── media_inventory.csv
└── notion_blog_review_template.html
```

Use `naver_review_assets/` for selected and renamed review media. Preserve source files by default.

### 2. Campaign And Product Survey

Use `naver-unmet-need-item-survey`.

Deliver:

- campaign requirement table
- keyword requirement table
- product-detail fact table
- unmet need table
- item survey table
- required photo/video checklist
- risks and missing information

Important:

- Preserve exact campaign keywords, spacing, dates, photo count, video count, link rules, and sponsor-banner instructions.
- Use absolute dates when deadlines matter.
- If campaign text conflicts, follow the stricter condition.
- Cite inspected URLs when web pages were used.

### 3. Media Matching

Use `naver-photo-review` when a folder is supplied.

Deliver:

- folder media count
- selected photo/video list
- mapping to required campaign evidence
- ordered filename plan
- copied assets folder
- excluded files and why
- missing shots to capture

Default for sponsored product reviews:

```text
대표 썸네일
패키지/구성
제품 디테일
사용 방법
제형/화면/기능 증거
사용 장면
BEFORE/AFTER or 결과 비교, only when appropriate for the product
마무리 컷
영상 1개
```

For digital products, replace beauty/product-physical slots with:

```text
대표 화면
다운로드/파일 수령
앱 불러오기
커버/인덱스
템플릿 구성
필기/작성 예시
하이퍼링크 이동
실사용 화면
화면녹화 1개
```

### 4. Review Draft

Use `naver-review-writing-ko`.

Draft in Korean with:

- title candidates
- clear disclosure at the top
- short intro from the reader's problem or motivation
- product first impression
- actual use process
- personal observations
- required campaign claims rewritten naturally
- honest limitation
- recommendation target
- required hashtags
- photo/video placement notes

Do not overfit to old templates. For each product category, rewrite the motivation, evidence, pros/cons, and recommendation logic.

### 5. HTML Output

When the user asks for Notion copy-paste or final upload prep, create:

```text
notion_blog_review_template.html
```

HTML rules:

- Use selected filenames from `naver_review_assets/`.
- Keep paragraphs short.
- Place text near matching images.
- Include video where the campaign asks for it.
- Include store link and sponsor banner placeholder/instruction when required.
- Avoid decorative complexity; the user handles visual design if they say so.

### 6. Final Audit

Use `naver-posting-audit-ko`.

Audit:

- title keyword compliance
- word count requirement
- photo count
- video count
- required keywords and hashtags
- sponsor banner/disclosure
- required product claims
- link placement
- media evidence alignment
- duplicate paragraphs
- caption grammar
- overclaiming or medical/performance exaggeration
- Naver Blog flow and readability

Fix the draft/HTML after audit when issues are concrete and local.

## Standard Start Prompt

When the user wants a one-shot request, this is the preferred prompt:

```text
$naver-review-pipeline 사용해서 네이버 리뷰 전체 작업을 진행해줘.

캠페인 요구사항 페이지:
[URL]

상품 상세페이지:
[URL]

사진/영상 폴더:
[ABSOLUTE_FOLDER_PATH]

최종 결과물:
노션에 복붙 가능한 HTML 파일

추가 메모:
- 실제 사용 후기:
- 강조하고 싶은 점:
- 솔직하게 넣을 아쉬운 점:
- 사용 기간:
```

## Output Summary

At the end, report:

```text
## 결론
## 생성/수정 파일
## 사진/영상 구성
## 캠페인 요구사항 충족 여부
## 남은 사용자 작업
```

Keep the final answer concise. Include exact file paths for generated HTML and selected media folder.
