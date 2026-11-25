---
name: find-influencer
description: |
  Search and evaluate high-potential content creators across platforms (Xiaohongshu, Douyin, Bilibili, etc.).
  Interactive workflow: collect requirements -> search -> filter by data -> deep content analysis -> report.
  Use when: user wants to find creators, bloggers, KOLs, influencers, or evaluate content quality.
  Triggers: find influencer, find creators, find bloggers, search KOL, find influencers, talent scout, creator analysis, find-influencer, 找达人, 搜索博主, 达人检索, 博主分析.
---

# Creator Discovery & Analysis

Multi-platform creator discovery tool for brand collaboration. Finds high-potential creators through multi-layer keyword search (exact product + competitor + broader domain), filters by recent engagement data (not just follower count), and evaluates subjective brand fit (content style, AI/tech experience, competitor history, visual quality, audience match).

ARGUMENTS: User's initial request (platform, content direction, etc.)

## Phase 1: Requirements Gathering

Use AskUserQuestion to collect:

1. **Target Platform(s)**: Xiaohongshu / Douyin / Bilibili / YouTube / TikTok / X(Twitter) / Instagram / multiple
2. **Product/Brand**: What product or brand is this collaboration for? e.g., ChatGPT, Claude, Gemini
3. **Content Direction**: The specific topic AND broader category. e.g., "ProductX (broader: AI agent, AI工具)"
4. **Collaboration Goal**: What kind of content do you want the creator to produce? e.g., 产品测评, 教程, 创意展示
5. **Tone Preference**: What style fits the brand? e.g., 专业但不枯燥, 轻松科普, 极客硬核, 创意炫酷
6. **Follower Range**: default 5,000 - 500,000 (soft reference, not hard cutoff -- great recent data can override low followers)
7. **Recent Data Priority**: default 1 month. Minimum acceptable recent post engagement (likes/saves/views)
8. **Known Competitors**: List competitor products so we can check if creators have collaborated with them. e.g., Coze, Dify, FastGPT
9. **Number of Results**: default 5-10 creators

If ARGUMENTS already contain these details, skip redundant questions.

## Phase 2: Content Search

### Tool Selection

| Platform | Primary Tool | Fallback |
|----------|-------------|----------|
| Xiaohongshu | `opencli xiaohongshu search` | Playwright browser |
| Bilibili | `opencli bilibili search` | Playwright browser |
| Douyin | Playwright browser | - |
| YouTube | `opencli youtube search` | Playwright browser |
| TikTok | `opencli tiktok search` | Playwright browser |
| X (Twitter) | `opencli twitter search` | Playwright browser |
| Instagram | `opencli instagram search` | Playwright browser |

### Search Strategy: Multi-Layer Keyword Expansion

Don't just search the exact product name -- use a 3-layer keyword strategy to find both vertical and adjacent creators:

**Layer 1: Exact product/brand keywords** (find creators already covering your product)
- Direct product name and variations
- Example for ProductX: "ProductX", "productx教程", "productx测评"

**Layer 2: Competitor & category keywords** (find creators in the same space)
- Competitor product names from Phase 1
- Category terms that your product belongs to
- Example: "Coze教程", "AI agent平台", "AI工作流搭建", "Dify教程"

**Layer 3: Broader domain keywords** (find quality AI creators who could pivot to your product)
- Broader topic keywords in the same domain
- Adjacent content areas where your audience overlaps
- Example: "AI工具推荐", "AI效率提升", "AI科技测评", "AI产品体验"

**Execution:**
1. Generate 2-3 keywords per layer (6-9 total), search each with `sort=popularity_descending` when available
2. Extract: title, author name, author ID/URL, likes count, saves count (收藏), post date
3. **Tag each result with its source layer** -- Layer 1 hits are highest relevance, Layer 3 are expansion candidates
4. **IMPORTANT**: The author field from search results often contains a date suffix (e.g., "博主名02-05", "博主名2天前"). Parse this date and use it to pre-filter -- only keep posts from within the recency window (default: 1 month). A high-likes post from 6 months ago is NOT evidence of current quality.
5. Filter to recent posts (within 1 month by default) with 赞藏数 (likes + saves) meeting user's threshold
6. Deduplicate by author -- prefer candidates with MULTIPLE recent high-engagement posts over one-hit wonders
7. When deduplicating, preserve the **highest-relevance layer tag** (if a creator appears in both Layer 1 and Layer 3, tag as Layer 1)

### Platform-Specific Search

**Xiaohongshu via opencli:**
```bash
opencli xiaohongshu search "<keyword>" --limit 20 -f json
```
If blocked by login wall, use Playwright:
```
Navigate: https://www.xiaohongshu.com/search_result?keyword=<encoded>&type=1&sort=popularity_descending
Close login modal if present, then extract via browser_evaluate
```

**Bilibili via opencli:**
```bash
opencli bilibili search --keyword "<keyword>" --limit 20 -f json
```

**TikTok via opencli:**
```bash
opencli tiktok search "<keyword>" --limit 20 -f json
# Get profile stats
opencli tiktok profile <username> -f json
# Get recent videos
opencli tiktok user <username> --limit 20 -f json
```

**X (Twitter) via opencli:**
```bash
opencli twitter search "<keyword>" --limit 20 -f json
# Get profile stats (followers, bio)
opencli twitter profile <username> -f json
```

**Instagram via opencli:**
```bash
opencli instagram search "<keyword>" --limit 20 -f json
# Get profile stats
opencli instagram profile <username> -f json
# Get recent posts
opencli instagram user <username> --limit 20 -f json
```

**YouTube via opencli:**
```bash
opencli youtube search --query "<keyword>" --limit 20 -f json
# Get video metadata (views, likes)
opencli youtube video "<url>" -f json
```
For YouTube channel subscriber count, use Playwright to visit `https://www.youtube.com/@<handle>`.

Refer to `guides/platform-selectors.md` for DOM selectors and JS extraction code.

## Phase 3: Creator Filtering (Two-Tier)

Filtering is split into **Tier A (Objective Data)** and **Tier B (Subjective Fit)**. Tier A is applied first to narrow the candidate pool, then Tier B is evaluated during deep analysis.

### Tier A: Objective Data Filtering

#### Priority Order (most important first)

| Priority | Metric | Default Threshold | Description |
|----------|--------|------------------|-------------|
| **P0** | 近期帖子综合质量（1个月内） | 3/5 篇以上"达标"（见下方评估方法） | **最关键指标。** 必须对每篇近期帖子从两个维度独立评估，然后统计达标篇数。不设固定绝对值，而是结合博主自身量级综合判断。 |
| **P1** | Historical hit rate | >= 1 post with 1000+ 赞藏 ever | Proves viral potential exists. Use 赞藏 (likes + saves), not likes alone. |
| **P1** | Comment quality | Comments show genuine interest, not spam/bots | Real engagement vs inflated numbers |
| **P2** | Recent 赞藏 trend | Compare recent posts vs older posts — is 赞藏 growing, stable, or declining? | Declining creators have old viral posts but weak recent numbers. Avoid. |
| **P2** | Total 赞藏/followers ratio | > 3x | Overall engagement health. High ratio from ancient posts is misleading — cross-reference with recent data. |
| **P3** | Follower count | 5,000 - 500,000 (soft reference) | **Soft filter only.** A 3k-follower creator with amazing recent data SHOULD still be recommended. A 50k-follower creator with dead recent data should be REJECTED. |

#### P0 每篇帖子评估方法（两个维度）

对近期每篇帖子，分别从以下两个维度判断是否健康：

**维度1：赞藏率（赞藏数 / 粉丝数）**

不设固定百分比，而是看"赞藏数与粉丝量级是否相称"：
- 赞藏数远高于粉丝数的一定比例 → 说明内容被算法放大推给了非粉丝 → 健康
- 赞藏数极低，与粉丝量完全不匹配 → 说明内容未被算法认可 → 偏弱
- 横向对比该博主其他帖子：该篇是明显高于还是低于自身均值？

**维度2：赞藏评比例（赞藏数 : 评论数）**

每篇帖子都需要检查，不只是整体历史数据：
- 20:1 ～ 80:1 → 健康，真实互动
- 80:1 ～ 150:1 → 偏高，结合内容类型判断（教程类收藏高、评论少属正常）
- 150:1 ～ 200:1 → 明显偏高，需留意，建议人工核查评论质量
- > 200:1 → 较大注水嫌疑，该篇视为不达标

**单篇帖子达标判定（结合两个维度）：**
- 赞藏率合理 + 赞藏评比例 <150:1 → ✅ 达标
- 赞藏率合理 + 赞藏评比例 150~200:1 → ⚠️ 勉强，酌情处理
- 赞藏率极低 或 赞藏评比例 >200:1 → ❌ 不达标

**P0 总评（根据达标篇数）：**
- 5/5 达标 → 优秀
- 4/5 达标 → 良好
- 3/5 达标 → 勉强可用，需在报告中标注
- ≤2/5 → P0 不通过，淘汰

#### Step 1: Profile-Level Quick Screen

For each candidate author, visit their profile page to extract:
- Follower count
- Total likes/favorites
- Bio/description

Use Playwright `browser_run_code` to batch-visit multiple profiles efficiently.
See `guides/platform-selectors.md` for extraction code.

**Soft-reject** candidates far outside follower range (e.g., < 1,000 or > 1,000,000), but keep borderline cases if other signals are strong. Do NOT yet evaluate "recent post quality" from profile-level data.

#### Step 2: Recent Post Data Collection (CRITICAL — Do NOT Skip)

**WARNING: Profile pages do NOT sort notes chronologically.** The notes shown on a profile page are algorithmically ordered and mix old viral posts with recent ones. You CANNOT determine recency from profile page alone.

**最常见的错误：只看到一篇高赞帖就认为达人数据好。必须强制验证多篇近期帖子。**

For each candidate that passes the profile quick-screen, you MUST:

1. **Click into 5-8 individual posts** from their profile to check actual publish dates
2. **Identify all posts published within the recency window** (default: 1 month)
3. **For each verified recent post, record ALL of the following:**
   - 发布日期
   - 点赞数
   - 收藏数
   - 赞藏合计 (likes + saves)
   - 评论数
   - 赞藏评比例 (赞藏 : 评论)
   - 赞藏率 (赞藏数 / 粉丝数，百分比)
4. **对每篇帖子按两个维度独立打标**（参考上方 P0 评估方法）：✅ 达标 / ⚠️ 勉强 / ❌ 不达标
5. **Build a 近期帖子数据表** with at least 3 rows (ideally 5). If a creator has fewer than 3 posts in the last month, they fail P0 automatically.
6. **统计达标篇数**，得出该创作者的 P0 总评。

**The goal is to present a DATA TABLE for each creator with per-post evaluations. A creator with 4/5 posts consistently healthy is far better than one with 1 viral post and 4 near-zero posts.**

#### Step 3: Apply P0-P3 Filters

Apply filters in priority order. Candidates must pass P0 to proceed. P1-P3 contribute to a composite score but a single P3 failure does not eliminate a candidate with strong P0/P1.

### Tier B: Subjective Fit Assessment (evaluated in Phase 4)

These dimensions are assessed during deep content analysis. They cannot be automated by data alone -- require reading/watching actual content.

| Dimension | What to Evaluate | How to Check |
|-----------|-----------------|-------------|
| **Content Style Match** | Does the creator's tone match the brand? (专业/轻松/极客/创意) Are they informative, entertaining, or both? | Watch 1-2 videos or read 2-3 posts. Summarize their style in 2-3 words. |
| **AI/Tech Experience** | Has the creator produced AI or tech content before? How deep is their technical understanding? | Scan post history for AI/tech keywords. Check bio for tech credentials. Rate: no experience / surface / moderate / deep. |
| **Competitor Collaboration** | Has the creator worked with competitor products? Which ones? How recently? | Search their post history for competitor product names (from Phase 1). Note: competitor experience can be POSITIVE (proves they understand the space) or NEGATIVE (exclusive deals, brand conflict). |
| **Visual Quality** | Cover design, editing quality, visual consistency, brand-readiness of their content | Screenshot representative posts. Score 1-10 using the Visual Quality Scoring table. |
| **Audience Fit** | Does the creator's audience overlap with the target user base? | Check comment section: are commenters asking relevant questions? Check follower demographics if available. |
| **Brand Safety** | Any controversial content, inappropriate tone, or risky associations? | Quick scan of recent posts for red flags. |

### Xiaohongshu: Extract Post Date from Detail Page

```javascript
() => {
  // Date is in the note detail page, usually near the bottom of the content area
  const dateEl = document.querySelector('[class*="date"], [class*="time"], .bottom-container .date');
  const allText = document.body.innerText;
  // Match patterns like "02-05", "2025-12-24", "3天前", "昨天"
  const dateMatch = allText.match(/(\d{4}-\d{2}-\d{2}|\d{2}-\d{2}|\d+天前|昨天|前天|\d+小时前)/);
  return dateMatch?.[0];
}
```

Alternatively, batch-check by navigating to each post URL and extracting the date element.

### Output

Present a filtered candidate table with **date-verified** recent post data and search layer source:
```
| # | Creator | Layer | Followers | Total Likes | Recent Post (date) | Likes | Best Historical | Profile |
```
Layer column shows: L1 (exact match), L2 (competitor/category), L3 (broader domain)

## Phase 4: Deep Content Analysis + Subjective Fit (Tier B)

For each creator that passes Tier A filtering, perform deep content analysis AND evaluate all Tier B subjective dimensions simultaneously.

### 4a. Video Content Analysis

**Bilibili 特殊处理（视频过长，跳过播放）：**

1. **Navigate** to the video page
2. **Screenshot** the cover image only (do NOT play the video)
3. **Extract** text info via browser_evaluate:
   - Title, description, tags
   - Play count, likes, coins, favorites, shares
   - Publish date
4. **Evaluate** based on cover + text only; skip transcription entirely

**其他平台（小红书等）正常流程：**

1. **Navigate** to the video post
2. **Play** the video (click video element or play button)
3. **Screenshot** 3 frames:
   - Frame 1: ~2s after start (opening/hook)
   - Frame 2: ~middle of video (main content)
   - Frame 3: ~near end (conclusion/CTA)
   - Save to `screenshots/` directory
4. **Read** screenshots to evaluate visual quality
5. **Transcribe** speech if meaningful audio content:
   - First check if the note description already contains a transcript (timestamps like "00:00", "00:24")
   - If no transcript in text, use the transcribe script:
     ```bash
     /Library/Frameworks/Python.framework/Versions/3.12/bin/python3 ${CLAUDE_SKILL_DIR}/scripts/transcribe.py "<video_url>"
     ```
   - Evaluate: clarity, information density, pacing, expertise level

### 4b. Image/Text Content Analysis

1. **Navigate** to the post detail page
2. **Screenshot** the post (cover image + content)
3. **Extract** full text content via browser_evaluate
4. **Evaluate**:
   - Cover design: brand consistency, color scheme, typography
   - Image quality: creativity, clarity, visual impact
   - Text quality: information density, actionability, originality
   - Title: click-worthiness, emotional hooks

### 4c. Tier B Subjective Evaluation (do this FOR EVERY candidate)

While analyzing content in 4a/4b, simultaneously evaluate all Tier B dimensions:

#### Content Style Match
- Summarize the creator's tone in 2-3 words (e.g., "专业科普型", "轻松幽默型", "极客实操型")
- Compare against the user's tone preference from Phase 1
- Rate: Mismatch / Partial Match / Strong Match

#### AI/Tech Experience Check
- Scan post history for AI/tech content keywords
- Check bio for tech credentials (company, degree, role)
- Rate the depth: No experience / Surface-level (转载为主) / Moderate (有自己的理解) / Deep (原创深度内容)

#### Competitor Collaboration Scan
- Search the creator's recent posts for competitor product names (from Phase 1 "Known Competitors")
- Record: which competitors, how recently, what type of content (测评/教程/广告)
- Flag: competitor experience is usually POSITIVE (proves they understand the space and can produce brand content), but note any exclusive deals or direct conflicts

#### Audience Fit
- Read 5-10 comments on the creator's best-performing posts
- Are commenters asking relevant questions? Are they potential target users?
- Note any demographic signals (students, professionals, developers, general audience)

#### Brand Safety
- Quick scan recent 10 posts for red flags: controversial topics, inappropriate tone, political content, negative sentiment
- Rate: Safe / Minor concerns / Red flag

### Visual Quality Scoring (1-10)

| Score | Criteria |
|-------|----------|
| 9-10 | Professional design, strong brand identity, high-res visuals, consistent style |
| 7-8 | Good design sense, clean layout, decent visual impact |
| 5-6 | Acceptable quality, basic design, functional but not distinctive |
| 3-4 | Low effort, screenshots/plain text, no visual identity |
| 1-2 | Poor quality, blurry, cluttered, unprofessional |

## Phase 5: Final Report

Output a ranked creator report with:

### Per-Creator Card

```markdown
### [Rank]. Creator Name -- Rating: X/5 stars

| Metric | Value |
|--------|-------|
| Platform | Xiaohongshu |
| Search Layer | L1 精准匹配 / L2 竞品赛道 / L3 泛AI领域 |
| Followers | X |
| 总赞藏 (历史累计) | X |
| 历史最高帖 | "title" (赞藏 X) |
| 近期赞藏趋势 | 上升 / 稳定 / 下降 |
| 近期数据稳定性 | 稳定 / 不稳定（最高/最低比 > 5x） |
| Profile | [link](url) |

**近期3-5篇帖子数据（1个月内，必须逐一列出）**

| # | 标题 | 日期 | 赞 | 收藏 | 赞藏 | 评论 | 赞藏评比例 |
|---|------|------|----|------|------|------|-----------|
| 1 | "帖子标题" | MM-DD | X | X | X | X | X:1 |
| 2 | "帖子标题" | MM-DD | X | X | X | X | X:1 |
| 3 | "帖子标题" | MM-DD | X | X | X | X | X:1 |
| 4 | "帖子标题" | MM-DD | X | X | X | X | X:1 |
| 5 | "帖子标题" | MM-DD | X | X | X | X | X:1 |

近期均值：赞藏 X，评论 X，赞藏评比例 X:1

**Tier A 数据评分**
- 近期赞藏一致性 (P0): X/10 — [描述：如"5篇均超2000赞藏，最高/最低比仅1.3x，极稳定"]
- 历史爆款 (P1): X/10
- 赞藏评比例 (P1): X/10 — 赞藏:评论 = X:1（正常范围 20-80:1，>100:1 有注水风险）
- 赞藏趋势 (P2): X/10

**Tier B 调性评分**
- 内容风格: [2-3词描述] — [匹配度: Strong/Partial/Mismatch]
- AI/科技经验: [No/Surface/Moderate/Deep] — [具体说明]
- 竞品合作: [有/无] — [具体产品及时间]
- 视觉质量: X/10
- 受众匹配: [描述目标受众重合度]
- 品牌安全: [Safe/Minor concerns/Red flag]

**综合评价**: [2-3 sentence summary covering: why this creator fits, what kind of content they could produce for the brand, any risks or considerations]

**Representative Screenshots**: [reference saved screenshot files]
```

### Summary Table

```
| Rank | Creator | Layer | Followers | 近期均赞藏 | 历史最高赞藏 | Style | AI Exp | Competitor | Visual | Overall |
```

### Ranking Logic

Final ranking considers both Tier A and Tier B, weighted as follows:
- **50%** Tier A (objective data): recent engagement is dominant factor
- **30%** Tier B relevance: content style match + AI experience + competitor knowledge
- **20%** Tier B quality: visual quality + audience fit + brand safety

A creator with average data but perfect brand fit may rank higher than one with great data but poor style match. Flag any cases where Tier A and Tier B scores diverge significantly -- let the user make the final call.

## Dependencies

### Required (check on first run)

```bash
# Check and prompt if missing:
which ffmpeg || echo "MISSING: Run 'brew install ffmpeg'"
python3 -c "import whisper" 2>/dev/null || echo "MISSING: Run 'pip install openai-whisper'"
which opencli || echo "MISSING: opencli not installed (use Playwright fallback)"
```

### Screenshots Directory

Create `screenshots/` in the current working directory for storing captured frames.

## High-Potential Small Creator Profile (Reference Model)

When evaluating small-but-promising creators, look for these traits. Based on real case: 浙大猫学长 (1.2万粉, 9.1万获赞, 18篇帖子, 多篇近期1000+赞).

### Key Indicators

| Trait | Why It Matters | Example |
|-------|---------------|---------|
| **Low post count, high hit rate** | Quality > quantity. A creator with 20 posts and 7 viral hits (35%+ hit rate) is better than one with 200 posts and 3 hits. | 18 posts, 7 posts with 1000+ likes = 39% hit rate |
| **Extreme engagement ratio** | Best post likes / follower count > 50% signals strong content-market fit and algorithmic recommendation. | 9126 / 12000 = 76% |
| **Real professional credentials** | Domain expertise in bio (specific company, degree, role) that matches content topic. Not vague "AI enthusiast". | "浙大数学硕士 \| 腾讯AI算法工程师" |
| **Niche pioneer** | Creating or defining a new category rather than following trends. First-mover content gets disproportionate algorithmic boost. | Coined "Vibe Animation" / "Vibe Motion" as new categories |
| **Consistent recent high performance** | Multiple 1000+ posts in last 6 weeks, not just one lucky viral hit. | 4 posts with 1000+ likes in 6 weeks |
| **Video-first with technical depth** | Video content with real demos/tutorials, not just talking heads or text overlays. Shows actual technical ability. | Live coding demos, animation tutorials |
| **Getting ratio > 5x** | Total likes-and-saves / followers > 5x means content reaches far beyond existing audience. | 9.1万 / 1.2万 = 7.6x |

### Red Flags (Anti-Patterns)

| Red Flag | What It Signals |
|----------|----------------|
| High followers but low recent likes | Declining creator, bought followers, or topic fatigue |
| Viral posts are all 3+ months old | One-hit wonder or abandoned account |
| Many posts with < 50 likes mixed with rare 1000+ | Inconsistent quality, likely gaming the algorithm |
| Bio says "AI博主" but content is generic reposts | No original perspective, low defensibility |
| Post titles are clickbait but content is thin | Short-term tactic, audience will churn |
| Very high posting frequency (daily) with low avg likes | Volume strategy without quality, unlikely to produce breakthroughs |

## Common Pitfalls (Lessons Learned)

### 1. Profile page notes are NOT chronologically sorted

The notes displayed on a Xiaohongshu profile page are algorithmically ranked, NOT by date. A profile might show a 6-month-old viral post (9000 likes) next to a 2-day-old post (30 likes). **Never assume profile-visible posts are "recent".**

### 2. Must click into posts to verify dates

The profile page extraction only gives you titles and like counts -- no dates. You MUST navigate into individual post detail pages to see the actual publish date. Without this step, you will mistake old viral posts for current performance.

### 3. High historical likes != current quality

A creator with a 10,000-like post from 6 months ago might now only get 50-200 likes per post. This indicates declining engagement. Always compare **date-verified recent performance** against the user's threshold, not historical peaks.

### 4. Search result date hints

In Xiaohongshu search results, the `author` field extracted via JS often includes a date suffix (e.g., "博主名02-05", "博主名2天前"). Parse these as a preliminary recency signal before investing time in profile visits.

### 5. Batch profile visits save time, but don't skip date verification

It's efficient to batch-visit profiles for follower counts (quick-reject on follower threshold). But after the follower screen, you MUST do a second pass clicking into actual posts. Don't skip this step to save time -- it leads to recommending declining creators.

### 6. Total likes/followers ratio can be misleading

A very high ratio (e.g., 26x) might come from a few ancient viral posts rather than consistent recent performance. Always cross-reference with date-verified recent post data.

### 7. Detail page like counts extraction is unreliable

The JS selectors for extracting likes from a post detail page often grab wrong elements (comment counts, "赞" button text, numbers from titles). **Use the profile-level likes data** (which is more reliable) for actual like counts, and use detail page visits ONLY for date verification. Cross-reference: profile gives you (title, likes), detail page gives you (title, date) -- match them by title.

## Notes

- Always use opencli first; fall back to Playwright only if opencli fails or doesn't support the platform
- When using Playwright, close login modals before extracting data
- Video transcription is optional -- skip if the note text already contains a transcript
- Keep screenshot count reasonable (3 per video, 1-2 per image post) to save context
- Present results in Chinese (the user's preferred language)
- Rate creators relative to each other, not on absolute scales

## Exporting to Feishu Spreadsheet

When user asks to export results to a Feishu spreadsheet, follow `guides/feishu-export.md`.

**Key rule**: Always use `lark_api` PUT directly — never use `lark_sheet` write action.
`lark_sheet` write silently fails (returns `{"data": {}}` with no error) and data won't appear in the sheet.

Quick template:
```
1. create_spreadsheet(title="...") → get spreadsheet_token
2. get_spreadsheet_sheets(token)   → get sheetId
3. lark_api PUT /open-apis/sheets/v2/spreadsheets/{token}/values
   body: { "valueRange": { "range": "{sheetId}!A1:H{n}", "values": [[...], ...] } }
4. Verify response has updatedRows == expected count
```
