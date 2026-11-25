---
name: reviewer-application-comment-ko
description: Use this skill when drafting, revising, or optimizing Korean 체험단/리뷰어 campaign application messages, especially fields named "신청 한마디", "신청자 한마디", "지원 이유", "리뷰어 신청", "체험단 신청문구", or short comments for Naver Blog, 놀러와체험단, 클라우드리뷰, 레뷰, 강남맛집, 디너의여왕, product review, restaurant/cafe/bar visit, performance/culture, lifestyle, tech, beauty, or local experience campaigns. The skill researches the campaign page and the user's Naver Blog reviewer identity, defaulting to https://blog.naver.com/dablro12, then writes a concise, natural 3-sentence Korean application message that feels like a real reviewer wrote it, identifying the reviewer as the best-fit 생활/여행/IT/뷰티/취미 블로거 type, why the campaign fits, and how the review will be produced.
---

# Reviewer Application Comment KO

## Output Rule

Start with a copy-paste-ready Korean application message. Default to exactly 3 natural Korean sentences unless the user requests variants, a longer form, or a campaign character limit makes 3 sentences impractical. If a campaign has a character limit, stay below it; when unknown, aim for 180-350 Korean characters.

Write as if the reviewer personally typed the message because they actually want the experience, not as if AI summarized campaign facts. Keep the tone warm and specific, vary sentence openings, and avoid stiff template rhythm, exaggerated praise, overly polished marketing copy, and list-like phrasing.

When the user asks "AI가 쓰지 않은 것처럼", "정성스럽게", "자연스럽게", or similar, treat it as a mandatory style override: make the message feel hand-written by a real applicant. Add one concrete personal use scene, one campaign-specific detail, and one sincere review promise; avoid generic phrases that could fit any campaign.

Make sentence 2 flow like a real reason for applying, not a formula. Avoid the awkward pattern "`[제품명]은/는 [설명]인 만큼 ...`"; prefer natural situation-first phrasing such as "`평소 [상황]이 신경 쓰여서 [제품명]을 직접 써보고 싶습니다.`", "`[상황]에서 [핵심 기능]이 얼마나 체감되는지 궁금해 신청합니다.`", or "`[제품명]의 [특징]이 제 사용 루틴과 잘 맞을 것 같아 신청합니다.`"

Before writing, decide the applicant's real-feeling motive in one short phrase: why this campaign would fit their current life, curiosity, routine, taste, problem, schedule, or content style. Let that motive drive the message. Campaign facts should support the motive; they should not become the whole message.

## Core Workflow

1. Inspect the campaign source when a URL or page text is provided.
   - Extract the campaign object: place/product/performance name, location, offer, target keywords, visit constraints, required media, review deadline, and any tone implied by the page.
   - For local places, include the neighborhood and category only when verified.
   - For product/performance campaigns, identify the usage or viewing situation that makes the application feel personal.

2. Refresh the reviewer identity from the user's Naver Blog.
   - Default blog URL: `https://blog.naver.com/dablro12`.
   - Prefer live inspection of `https://m.blog.naver.com/dablro12` and `https://rss.blog.naver.com/dablro12.xml`.
   - Extract only confirmed facts: blog name, nickname, introduction, categories, recent post topics, visible review style, and current metrics if clearly shown.
   - If live access fails, read [references/reviewer-profile.md](references/reviewer-profile.md) and treat it as a fallback snapshot.

3. Choose a personal motive before drafting.
   - Infer a believable reason the applicant would genuinely want this campaign from the campaign type, season, location, offer, blog topics, and recent posts.
   - Use a motive that sounds like a person, such as `퇴근 후 들를 만한 공간`, `서울 근교에서 쉬고 싶은 일정`, `직접 만들어 오래 남기는 체험`, `요즘 피부/건강/생활 루틴 고민`, or `방문 후기 콘텐츠와 잘 맞는 메뉴`.
   - Do not simply restate the offer, price, required photos, keywords, or location as the reason for applying.

4. Write the message using this exact logic:
   - Sentence 1: Show the reviewer identity using the best-fit blogger type.
     - Infer one label from the campaign page, product category, offer, and use context: `생활 블로거`, `여행 블로거`, `IT 블로거`, `뷰티 블로거`, or `취미 블로거`.
     - Example shape: "`Needly Life`에서 일상 속 경험을 직접 해보고 차분히 기록하는 생활 블로거입니다."
   - Sentence 2: Connect the campaign to a concrete interest or situation.
     - Mention the place/product/performance name and why it fits the blog.
     - Do not use "`[product]은/는 [category/feature]인 만큼`" or similar stiff connector patterns.
     - Lead with the applicant's real situation, problem, curiosity, schedule, taste, or use scene whenever possible.
     - Make this sentence answer: "Why do I personally want to try this, beyond receiving a free offer?"
   - Sentence 3: Promise the review method.
     - Mention concrete deliverables such as photos, video, atmosphere, menu, route, use scene, comparison, honest strengths/limits, or required keywords only after the personal motive is clear.
   - Treat the sentence roles as intent, not a rigid template. Adjust the wording so the 3 sentences flow naturally and do not look copied from a reusable AI pattern.

5. Self-check the final message before answering.
   - Check whether sentence 2 clearly shows a human motive: curiosity, preference, current need, planned visit/use scene, or why the campaign fits the blog now.
   - Check whether the message would still make sense if the campaign name were replaced with another similar campaign. If yes, it is too generic; rewrite it.
   - Check whether the message reads like information delivery, such as `제공내역`, `요구사항`, `사진/영상`, or `키워드` listed without desire. If yes, rewrite it with the applicant's motive first and requirements second.
   - Check whether the rhythm is stiff or template-like. If it starts with a repeated pattern used in recent outputs, rewrite with a different sentence opening.
   - Check whether it sounds like the applicant wants to review the campaign because it genuinely matches their life or blog. If not, rewrite before final output.
   - Do not expose this checklist or revision process unless the user asks.

## Reviewer Identity Rules

- Use "Needly Life" plus a campaign-fit blogger type; do not use "Eiden" in the application message.
- Choose the blogger type by inference from the link/page:
  - `생활 블로거`: household goods, daily items, cleaning, food products, restaurants, cafes, local daily experiences, practical services.
  - `여행 블로거`: lodging, camping/glamping, travel spots, regional experiences, outdoor itineraries, transport or trip-related products.
  - `IT 블로거`: digital devices, apps, software, learning platforms, tech accessories, productivity tools.
  - `뷰티 블로거`: skincare, cosmetics, hair/body care, grooming, fragrance, beauty shops.
  - `취미 블로거`: books, movies, music, performances, exhibitions, sports, leisure, hobby supplies, lifestyle activities not better covered by travel.
- Present the blog as a daily-life review blog that records reading, experiences, thoughts, books, tech, travel, food, films, music, and useful discoveries.
- For restaurant/cafe/bar campaigns, emphasize actual visit experience, atmosphere, menu choice, photos, route, reservation/seat details, and who the place fits.
- For product campaigns, emphasize practical daily use, first impression, photos, details, before/after or comparison when relevant.
- For culture/performance campaigns, emphasize the reviewer's reflective writing style and the ability to connect the performance to everyday recovery, emotion, or cultural life.
- For tech/education campaigns, emphasize the reviewer's previous tech and learning-content posts.

## Do Not

- Do not invent monthly visitors, 운영 기간, awards, neighbor count, or review history.
- Do not claim "맛집 전문 블로거" unless the blog evidence supports that exact claim. Prefer "일상과 경험을 리뷰하는 블로거" or "방문 경험 중심으로 기록하는 블로거".
- Do not overpromise perfect praise. Promise "솔직하고 꼼꼼한 후기" instead.
- Do not include hashtags unless the application field explicitly asks for them.
- Do not mention that the page was crawled, searched, or analyzed.
- Do not write formulaic second sentences like "`[제품명]은/는 ...인 만큼 ...`"; make the reason sound situational and personal.
- Do not make the application sound like a campaign requirement summary. Avoid centering the message on `제공내역`, `사진 N장`, `텍스트 N자`, or `키워드` unless sentence 2 already shows a genuine reason for applying.

## Useful Templates

### General Visit Campaign

```text
Needly Life에서 일상 속 경험과 공간을 직접 다녀와 기록하는 [생활/여행/취미] 블로거입니다. 요즘 [상황/관심사]에 맞는 곳을 찾고 있어 [지역/장소명]의 [핵심 매력]을 실제로 경험해보고 싶습니다. 공간 분위기, 방문 동선, 이용 장면, 사진과 영상까지 자연스럽게 담아 솔직한 후기로 작성하겠습니다.
```

### Food, Cafe, Bar

```text
Needly Life에서 음식과 공간을 실제 방문 경험 중심으로 기록하는 생활 블로거입니다. [상황: 퇴근 후/주말 약속/데이트/혼밥]에 들르기 좋은 곳을 찾다가 [장소명]의 [메뉴/분위기]가 궁금해 신청합니다. 메뉴 선택 이유, 좌석 분위기, 방문 동선, 사진과 영상, 지도 정보까지 자연스럽게 담아 성실한 후기로 작성하겠습니다.
```

### Product Campaign

```text
Needly Life에서 일상에 필요한 제품과 경험을 직접 써보고 기록하는 [생활/IT/뷰티/취미] 블로거입니다. 요즘 [구체적 고민/루틴/사용 상황]이 있어 [제품명]을 제 생활 속에서 직접 써보고 싶습니다. 첫인상, 디테일, 실제 사용 장면, 느낀 장단점까지 사진과 함께 꼼꼼히 담겠습니다.
```

### Culture or Performance

```text
Needly Life에서 책, 영화, 음악, 공연처럼 일상에 오래 남는 경험을 차분히 기록하는 취미 블로거입니다. 최근 [감정/관심사/문화생활 상황]이 있어 [공연/전시명]을 직접 보고 느낀 점을 남겨보고 싶습니다. 관람 전 기대감, 현장 분위기, 관람 후 여운까지 솔직하고 읽기 좋은 후기로 작성하겠습니다.
```
