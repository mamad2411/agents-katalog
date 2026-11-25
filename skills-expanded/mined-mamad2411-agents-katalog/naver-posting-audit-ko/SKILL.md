---
name: naver-posting-audit-ko
description: Use this skill when auditing, validating, scoring, or revising Korean Naver Blog posts or drafts against posting guidelines, especially review posts, product reviews, 체험단 reviews, sponsored posts, 내돈내산 posts, title keyword checks, intro checks, body structure checks, image plan checks, reference blogger comparison, ad disclosure checks, omission/search 누락 risk checks, and post-publication verification checklists.
---

# Naver Posting Audit KO

## Core Rule

Audit the post against the user's posting guideline and return a practical fix list. Do not only summarize. Start with the conclusion and separate must-fix issues from optional improvements.

If the draft lacks images, links, sponsorship status, or target keyword, mark those fields as "확인 필요" instead of inventing them.

## Output Format

Use this structure by default:

```markdown
## 결론
## 검증 결과
## 필수 수정
## 권장 수정
## 수정 예시
## 발행 후 확인
```

For `검증 결과`, use a compact table:

```markdown
| 항목 | 상태 | 판단 | 수정 방향 |
|---|---|---|---|
| 제목 | 통과/주의/수정필수/확인필요 | ... | ... |
```

Status meanings:

- `통과`: guideline is satisfied.
- `주의`: not fatal, but CTR/search/review trust may weaken.
- `수정필수`: violates a core guideline or legal/sponsorship safety rule.
- `확인필요`: cannot verify without missing information or live search.

## Required Inputs To Check

Try to infer from the post, but ask or mark missing when needed:

- Target main keyword
- Full title
- Full body text
- Review type: tech, daily, hobby, food, beauty, place, etc.
- Sponsorship status: 내돈내산, 제품 제공, 원고료, 할인, 환급, affiliate, 체험단
- Image count and rough order, if available
- External links count, if available
- Publication state: draft or already published

## Title Audit

Check:

1. The title is not a keyword dump.
2. The title clearly explains what the post is about.
3. The title includes the main keyword naturally.
4. If multiple keywords appear in the title, the body actually covers each one.
5. The blog does not repeat near-identical serial titles such as `일본여행 1일차`, `일본여행 2일차`, `DAILY 20240626`.
6. If targeting a Naver Smart Block/popular topic, the relevant topic keyword appears somewhere in the title.

Flag as `수정필수` when:

- The title is a long list of unrelated keywords.
- The title promises topics that the body does not cover.
- The title lacks the main product/place/service keyword.

Flag as `확인필요` when:

- Title similarity with other bloggers must be checked but no search results or comparison titles were provided.
- Smart Block keyword suitability requires live search.

Suggest a revised title using:

```text
[고지] [핵심키워드/제품명] 후기: [사용상황/차별점] 중심 솔직리뷰
```

## Intro Audit

Check the first 3-6 paragraphs:

1. The first image plan includes a hook image or main product/place image, ideally 1-2 strong images.
2. The intro starts from a reader/user problem, motivation, or real-life trigger.
3. The intro explains why the product/place/service was chosen or reviewed.
4. The target main keyword appears naturally.
5. The post purpose is explicit, such as "주요 기능과 사용 후기를 공유하려고 합니다."
6. Basic context appears early: brand, model, price, location, menu, or product type.
7. The next image plan shows overall appearance/design/size, usually 2-3 images.
8. Filming caveats or reviewer limitations appear only after the hook, usually in usage or BEFORE/AFTER context.

Flag as `수정필수` when:

- The post jumps into praise without context.
- The main keyword is absent from the intro.
- The reader cannot tell what is being reviewed within the first screen.
 - The intro starts with internal production details such as "촬영 당시..." before explaining why the product matters.

## Body Audit

Check whether the body follows the review context.

For product reviews, verify:

- Major features and benefits are explained.
- Components or included items are listed.
- Close-up image plan covers texture, logo, weight, labels, components, ports, buttons, packaging, or material, usually 4-7 images.
- Usage method and major functions are explained.
- Real-use photos or videos are planned, usually 3-5 images or one short video.
- Personal experience is specific, not only promotional.
- Limitations, flaws, or improvement points are included when relevant.
- Price-performance/value judgment is present.

For sponsored campaign product reviews, verify:

- Campaign-required claims are included in the user's own language rather than copied from the guide.
- Required photo/video evidence is placed near the matching body section.
- Usage method is explained from actual photos/video, not only copied from the package.
- BEFORE/AFTER appears with enough context: what was observed, when, and what changed.
- Honest limitations are included when relevant, such as 오일감, 향 호불호, size, stickiness, or fit.
- The draft uses personal-observation wording for sensitive body/beauty claims.

For men's beard oil/essence reviews, specifically check:

- 수염 아래 피부 보습 is connected to 면도 후 건조함, 당김, 각질감, or 가려움.
- 뻣뻣한 수염 케어 is connected to 짧은 수염의 까슬함 or 긴 수염 결 정돈.
- 정돈된 인상 is connected to 턱선, 인중, 수염 자국, or grooming appearance.
- The post avoids growth/medical claims such as 수염이 난다, 치료, 피부 질환 개선.

For food/place reviews, verify:

- Menu/price/location or purchase channel is clear.
- Taste, texture, portion, freshness, atmosphere, service, and revisit intent are covered.
- Photos cover exterior/sign, menu, table, main dish, detail cut, and receipt or price if appropriate.

For tech reviews, verify:

- Setup, compatibility, workflow fit, performance, battery/stability, privacy/security when relevant, and alternatives are addressed.

For hobby reviews, verify:

- Entry reason, required cost/time, difficulty, enjoyment, repeatability, beginner suitability, and recommendation fit are addressed.

## Ad Disclosure Audit

If the post has any economic relationship, enforce a conservative rule:

- Disclosure must appear in the title or at the very top of the body before the review starts.
- The wording must say who provided what: product, service, 원고료, 할인, 숙박, 환급, affiliate commission, or 체험단 participation.
- The text must be visible as normal body text or clearer.
- Disclosure only at the bottom is insufficient.
- Disclosure only inside an image is insufficient.
- Naver's built-in "제품/서비스 제공" checkbox alone should not be treated as enough for this audit; recommend direct body disclosure as well.

Good examples:

```text
이 포스팅은 [업체명]으로부터 제품을 무상으로 제공받아 작성했습니다.
```

```text
본 리뷰는 [플랫폼명] 체험단으로 참여해 작성한 솔직한 후기입니다.
```

```text
[업체명]의 협찬을 받아 작성된 글입니다.
```

Bad examples:

- Only `(협찬)` at the bottom.
- "광고가 포함되어 있습니다" without who/what.
- Tiny text hidden in an image.
- Only checking the Naver built-in disclosure box.

Legal note: Do not present this audit as legal advice. If the user asks for current legal compliance, verify the latest official Fair Trade Commission or law.go.kr materials before answering.

## Omission/Search Risk Audit

This is a heuristic risk check, not a guarantee of Naver exposure.

Flag risks:

- Body is under 1,000 Korean characters: high information-depth risk.
- Body is under 2,000 Korean characters for 체험단/commercial review: improvement recommended.
- Repeated extreme ad phrases such as "최고", "강추", "꼭 가세요", "무조건" without evidence.
- Main keyword is repeated mechanically. Use the user's guideline threshold: exact forced repetition over 3 times is a warning unless natural and necessary.
- External links exceed 2, or there are 3+ promotional links.
- Images are reused from other posts or not newly created.
- Title and body content do not match.
- Similar serial titles are used across multiple posts.

Post-publication checks:

```text
1. After 6-12 hours, search the exact title on Naver.
2. Search the main keyword and check the first 1-2 result pages.
3. Search `site:blog.naver.com/[blog_id]` if indexing seems abnormal.
4. For 체험단, verify exposure before submitting the campaign link.
```

## Reference Blogger Comparison

Use this when the user provides another blogger's post, competitor post, or says "비슷한 흐름으로", "참고 블로그와 비교", or "다른 블로거처럼".

Compare structure, not wording. Never copy distinctive phrases.

Check these:

| 비교 항목 | 좋은 기준 | 자주 보이는 보완점 |
|---|---|---|
| 도입 | reader problem or purchase/review motivation first | starts with campaign/filming caveat too early |
| 첫 화면 | disclosure, title keyword, strong product image | product identity appears too late |
| 흐름 | problem -> product -> usage -> evidence -> verdict | photos are dumped before/after one text block |
| 사진 캡션 | short, neutral, useful | harsh wording, typo, or inside joke |
| 중복 | no repeated paragraph | package/first impression repeated twice |
| 링크 카드 | optional and not disruptive | product link card breaks the story too early |
| 실사용 | specific time/situation | vague "좋았다" without context |
| 결론 | recommended user is clear | everyone-targeted generic praise |

When auditing a published post against a reference blogger flow, always inspect:

1. Whether the introduction motivates the review before discussing shooting conditions.
2. Whether repeated paragraphs appear after image carousels or link cards.
3. Whether captions have visible grammar issues.
4. Whether "혐오주의", excessive self-deprecation, or overly casual wording weakens trust.
5. Whether media count includes only intended review photos/videos, not ad widgets and OG thumbnails.
6. Whether the final recommendation names the exact user fit.

Return concrete edits such as:

```text
삭제: duplicated paragraph beginning with ...
수정: "순서이" -> "순서가"
수정: "혐오주의" -> "면도 후 턱 주변 변화"
수정: "사용 후 직전" -> "사용 직후"
```

## Fix Style

When issues are found, provide:

- A revised title.
- A revised first 3-5 intro lines.
- A missing-section insert block.
- A disclosure sentence if needed.
- A post-publication checklist.

Do not rewrite the entire post unless the user asks. Prefer targeted patches.

## Final Checklist

Before finalizing the audit, confirm:

- Title is clear and not keyword-stuffed.
- Main keyword appears naturally in title and intro.
- Intro contains reason, discovery path, purpose, and basic information.
- Body covers features, use method, personal experience, limits, and price-value.
- Image order is sufficient or missing image evidence is called out.
- Ad disclosure is correct when there is any economic relationship.
- Search omission risks are listed as risks, not certainties.
- The answer ends with concrete next actions.
