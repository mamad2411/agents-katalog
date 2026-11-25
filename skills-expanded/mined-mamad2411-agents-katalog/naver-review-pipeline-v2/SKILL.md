---
name: naver-review-pipeline-v2
description: Run an evidence-first Korean Naver Blog review workflow optimized for reader usefulness, Naver Search and AI Briefing eligibility, and Homefeed relevance without promising exposure. Use when the user asks for the V2 full pipeline, higher-exposure Naver review writing, AI Briefing or Homefeed-aware drafting, campaign/product/media analysis, channel-topic analysis, search-intent planning, Notion-copyable HTML, or final sponsored-review compliance and quality auditing.
---

# Naver Review Pipeline V2

## Purpose

Run the complete Korean Naver review workflow while improving the factors that
Naver publicly recommends: firsthand experience, topic consistency,
transparency, readable structure, freshness, reader context, process, valid
comparisons, concrete results, and relevant media.

Optimize for usefulness and eligibility, not a guaranteed rank. Never claim
that a table, keyword count, GIF, title formula, comment question, or this skill
will produce a specific exposure increase.

Coordinate these module skills when available:

1. `naver-unmet-need-item-survey`
2. `naver-photo-review`
3. `naver-review-writing-ko`
4. `naver-posting-audit-ko`

When exposure, AI Briefing, Homefeed, SEO, or a third-party diagnosis matters,
read [references/exposure-research.md](references/exposure-research.md) before
drafting.

## Non-Negotiable Rules

- Preserve exact campaign disclosure, keywords, dates, counts, links, and
  sponsor instructions.
- Treat user notes and media as the only source of personal experience.
- Never invent use duration, comparisons, measurements, prices, defects,
  reactions, before/after results, or photos.
- Separate measured facts, observed facts, sourced facts, and hypotheses in the
  working notes.
- Label unsupported exposure advice as a hypothesis; do not present it as a
  Naver rule.
- Keep key information in body text even when it also appears in an image,
  video, GIF, infographic, or table.
- Use relevant terms naturally. Do not force arbitrary keyword density or add
  unrelated trending terms.
- Keep a required campaign repetition count only when explicitly required;
  satisfy the minimum naturally and flag spam risk when the wording becomes
  repetitive.
- Prefer an accurate, specific title over curiosity bait.
- Write the final content in Korean unless the user requests another language.

## Inputs

Use available inputs and continue without blocking when possible:

```text
1. 캠페인/리뷰 요구사항 URL 또는 원문:
2. 상품 상세페이지 URL:
3. 사진/영상 폴더:
4. 블로그 URL:
5. 실제 사용 후기 메모:
6. 사용 기간·환경·비교 대상·측정 방법:
7. 최종 결과물: 원고 / 사진 구성 / 노션 복붙 HTML / 전체
```

If campaign or product information is missing, use only verified sources and
flag the gap. If media is missing, produce a required-shot plan. If experience
evidence is missing, draft with explicit placeholders such as
`[실제 사용 기간 입력]` rather than fabricating it.

Ask at most three concise questions only for facts that would materially change
the draft. Do not ask again for information already provided.

## Pipeline

### 1. Lock Sources And Project Scope

Create an internal source ledger with these classes:

```text
CAMPAIGN  exact obligations from the campaign
PRODUCT   verified specifications from the official product source
USER      firsthand notes, media, measurements, and preferences
OFFICIAL  Naver or other authoritative guidance
THIRD-PARTY  diagnostic or market advice
HYPOTHESIS  an optimization idea not confirmed as a ranking rule
```

Resolve conflicts in this order:

1. Legal and platform transparency requirements
2. Campaign obligations
3. Verified product facts
4. User firsthand evidence
5. Third-party advice

Do not let optimization advice override truthfulness or campaign compliance.

### 2. Survey Campaign And Product

Use `naver-unmet-need-item-survey`.

Extract:

- disclosure and sponsor-banner wording
- title, body, and hashtag requirements
- required links and placement
- minimum text, image, and video counts
- mandatory product claims
- prohibited expressions
- deadline and retention period
- verified product specifications
- missing or conflicting facts

Use the stricter condition when campaign text conflicts. Cite inspected URLs.

### 3. Analyze Channel Topic With A Valid Time Window

When a blog URL is available:

1. Inspect the latest active 90 days or latest 20 active posts.
2. Report older history separately when a long posting gap exists.
3. Count posts by topic and category, but do not treat old and recent posts as
   equally representative after a hiatus.
4. Identify one primary content pillar and up to three supporting clusters.
5. State the sample size and window.

Do not recommend changing a registered topic from raw all-time counts alone.
Treat a third-party topic label as that tool's taxonomy unless Naver confirms
the same field. If the active sample has fewer than 10 posts, mark confidence
as low.

### 4. Build The Reader And Search-Intent Brief

Define before drafting:

```text
Primary reader:
TPO (who / when / where / why):
Decision or problem:
Primary query:
Supporting queries:
Campaign keywords:
One-sentence answer:
Opening hook angle:
Unique firsthand angle:
Closest relevant alternatives:
Evidence still missing:
```

Choose one primary query that accurately describes the article. Use two to four
supporting queries only when they are semantically relevant and supported by
the content. Distinguish campaign-mandated keywords from independently
researched search terms.

Do not infer search demand from intuition alone. When live search-volume,
autocomplete, related-question, or AI Briefing evidence is available, record
the source and observation date. Otherwise label the term selection as a
content-fit hypothesis.

For `Opening hook angle`, define the reader desire, tension, or avoided pain
that the introduction should speak to. Use one evidence-grounded angle such as
comfort, saving time, avoiding regret, cleaner daily routine, better gift-giving,
small-space relief, family care, confidence, or a simpler decision. The hook
must be connected to the user's real notes, product facts, or visible media.
Do not use manipulative fear, shame, exaggerated scarcity, fake consensus, or a
promise the review cannot substantiate.

### 5. Plan Firsthand Evidence Before Writing

Collect evidence in four blocks:

1. **Process**: actual order, setup, time, mistakes, and corrections.
2. **Comparison**: alternatives genuinely considered or used and the decision
   reason.
3. **Result**: what changed, what did not, and the observation period.
4. **Limitation**: downside, exception, unsuitable reader, or unresolved point.

For every number, record:

```text
metric / value / unit / baseline / time window / environment / method / source
```

Use exact numbers only when measured or documented. Convert unmeasured
impressions into honest language or a clearly defined subjective scale. Never
turn “덜한 느낌” into an invented percentage.

Use comparison tables only when the compared attributes are known. If only one
product was used, compare it with the prior routine or selection criteria
instead of pretending to have tested competitors.

### 6. Match Media To Evidence

Use `naver-photo-review` when a folder is supplied.

Map each selected asset to a claim or reader question:

```text
대표 결과
구성품·크기·마감
설치·준비 과정
실제 사용 순서
측정·관찰 근거
비교 또는 전후 맥락
한계·주의사항
추천 대상
영상 또는 GIF
```

Preserve source files. Copy only selected assets into
`naver_review_assets/`. Exclude duplicates, irrelevant media, and assets that
cannot support a nearby statement.

Do not assert that a GIF itself improves ranking. Use motion only when it
demonstrates a process or result more clearly than a still image.

### 7. Draft The Review

Use `naver-review-writing-ko`.

#### Title

Generate three accurate title candidates and score each from 0–2 on:

- primary-query clarity
- reader/TPO specificity
- firsthand differentiator
- campaign compliance
- non-clickbait accuracy

Select the highest-scoring title. Use the primary topic once when natural.
Avoid duplicated keyword blocks, unrelated popular terms, unsupported
superlatives, and a question whose answer is absent from the article.

#### Opening Hook

Before the main body, write a short hook that makes the reader feel the review
is about a desire or problem they already have. The hook should usually appear
within the first 2-4 paragraphs after the disclosure.

Use this sequence unless the campaign requires another opening order:

1. Name the relatable situation or hidden friction.
2. Connect it to the reader's desire, avoided pain, or ideal daily scene.
3. Introduce the product as the specific option tested.
4. Give the short answer or review promise without overclaiming.

Good hooks are concrete and human:

- `작은 주방이라 정수기 놓을 자리가 없는데, 얼음물은 매일 마시고 싶은 상황`
- `선물은 하고 싶은데 너무 부담스럽지도, 성의 없어 보이지도 않게 고르고 싶은 상황`
- `매번 손이 가는 생활 불편을 줄이고 싶은 상황`
- `가족이 어렵지 않게 쓸 수 있는 제품을 찾는 상황`

#### Body Order

Use this default order, adapting it to the product and campaign:

1. Exact disclosure at the top
2. Reader situation and short answer
3. Optional decision summary
4. Why this option was chosen and alternatives considered
5. Actual process in chronological order
6. Concrete result and evidence
7. Unexpected finding, only if genuinely observed
8. Limitation and purchase/use cautions
9. Situation-specific recommendation
10. Required link, disclosure reminder, and hashtags

Insert a compact summary table near the top only when at least three verified
decision facts exist. Place it after the required disclosure and opening
context. A table is optional structure, not an exposure guarantee.

Use short paragraphs, meaningful subheadings, and explicit text captions.
Avoid generic manufacturer-copy sections that could be reused unchanged for a
different product.

### 8. Produce HTML When Requested

Create `notion_blog_review_template.html`.

- Use selected filenames from `naver_review_assets/`.
- Keep disclosure first.
- Use a real HTML table only when verified rows exist.
- Repeat each image-only key fact in nearby body text.
- Place text next to matching media.
- Include required store links, sponsor instructions, video notes, and
  placeholders.
- Keep the markup simple enough for Notion copy-paste.

### 9. Run Two Audits And Fix Local Issues

Use `naver-posting-audit-ko`.

#### Campaign Audit

- title and body keywords
- minimum text length
- image and video counts
- disclosure and sponsor banner
- required claims and links
- retention and deadline notes

#### Exposure-Quality Audit

Score each item 0, 1, or 2:

```text
A. 독자·상황·목적
B. 직접 경험의 순서·팁·시행착오
C. 실제 대안·비교·선택 이유
D. 결과 근거와 수치의 검증 가능성
E. 소제목·문단·표·미디어의 가독성
F. 핵심 정보의 텍스트 제공
G. 제목의 정확성·고유성·비낚시성
H. 채널 주제 적합성과 정보 최신성
I. 협찬·출처의 투명성
J. 서론 훅의 욕망·문제 연결성과 근거성
```

Do not publish silently with any of these red flags:

- invented or source-less percentage
- unverified before/after claim
- fake competitor comparison
- unrelated keyword insertion
- repetitive keyword stuffing
- curiosity bait unsupported by the body
- generic praise without user evidence
- critical information present only inside media
- third-party exposure advice stated as a Naver guarantee

Fix concrete issues. Leave explicit placeholders for missing user evidence.

### 10. Create A Post-Publish Learning Loop

When the user wants ongoing improvement, record the publishing date, title,
primary query, topic pillar, content change tested, and available outcome
metrics at 7 and 28 days.

Compare at least three reasonably similar posts before claiming a pattern.
Change one major variable at a time when practical. Treat before/after
differences as observational unless a valid experiment supports causality.
Never promise future rank or AI Briefing citation.

## Standard Deliverables

Create only the files the task needs:

```text
project folder/
├── campaign_requirements_and_search_brief.md
├── evidence_ledger.md
├── media_inventory.json
├── media_inventory.csv
├── naver_review_assets/
├── notion_blog_review_template.html
├── posting_audit.md
└── post_publish_measurement_log.csv
```

## Final Response

Lead with the usable outcome and keep the handoff concise:

```text
## 결론
## 생성/수정 파일
## 노출 품질 보강 내용
## 캠페인 요구사항 충족 여부
## 검증된 근거와 가설
## 남은 사용자 작업
```

Include exact absolute paths for created files. State missing evidence and
remaining placeholders explicitly.
