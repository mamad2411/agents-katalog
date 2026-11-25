---
name: luxury-editorial-site-builder
description: >-
  Complete workflow for a high-end editorial brand homepage (furniture, interior design, fashion, luxury goods, atelier) — large whitespace, restrained motion, light neutral palette, 100dvh full-bleed hero image or video. Also covers static brand sites needing Hailuo/Veo/Kling AI video, Topaz upscale, multi-video crossfade or Vercel deploy. Triggers: "editorial-luxury / 杂志感 / 高端品牌官网 / editorial website / 高端家具网站 / luxury hero video website", or any request that smells like a high-end campaign-style brand homepage with a hero video.
---

# Luxury Editorial Site Builder

This skill captures a battle-tested 9-phase workflow for building a single-page editorial brand site, refined on a real project (U2 Living, a Hong Kong furniture brand). The next site should take ~1-2 weeks instead of starting from zero.

**Tech profile**: pure static HTML/CSS/JS, deployed to Vercel. No build step, no framework. Variable serif (Fraunces) + sans (Geist). Hero video crossfade. Pretext-based per-line text reveal.

**Aesthetic profile**: ESTUDIO ANÓNIMO / editorial luxury / 杂志感 / 大量留白 / 克制动效 / 浅色中性色.

---

## Workflow at a glance

```
Phase 0  Alignment        ← invoke taste skill + interview user
Phase 1  Skeleton         ← build with placeholder brand
[USER REVIEW REQUIRED — sign-off on aesthetic before proceeding]
Phase 2  Real content     ← fill-in md template, batch replace
Phase 3  AI images        ← user generates ChatGPT images that match style
Phase 4  Insert images    ← sips compress, replace placeholders
Phase 5  AI videos        ← image-to-video on fal.ai (Hailuo 02 Pro)
Phase 6  Insert videos    ← crossfade integration, 4K upscale
Phase 7  Design system    ← terminal convergence pass
Phase 8  Deploy           ← Vercel CLI + API hidden ops
```

Three things drive this ordering:
1. **Aesthetic gets locked first** — every later phase compounds aesthetic mistakes
2. **Images precede videos** — fal.ai's `image-to-video` models use the image as source, so the image must exist + match the site's visual language first
3. **Design system convergence is terminal** — token churn during build is fine, ship-time inconsistency is fatal

---

## Phase 0 — Alignment (do this BEFORE any code)

**This phase produces nothing visible — it produces context. Don't skip it.**

### Step 1: Load aesthetic baseline (taste-skill MODE A — Editorial Monochrome)

Invoke `Skill(taste-skill)` and select §11 MODE A (Editorial Monochrome — Notion / Linear / warm-monochrome) as the editorial-luxury baseline. This is the canonical replacement for the removed `high-end-visual-design` / `design-taste-frontend` / `gpt-taste` / `stitch-design-taste` skills (deleted 2026-06-02). The taste preset prompts (palette / type / motion / restraint) load into context — build against them directly.

> NEVER fall back to `ls ~/.claude/skills | grep taste` discovery — that path is dead (the 4 skills above were deleted 2026-06-02). The aesthetic baseline is **taste-skill MODE A, hard-named**. If `taste-skill` is missing, STOP and warn the user — do NOT generate against model priors.

### Step 2: Interview the user

Ask exactly these 7 questions, in one message. Wait for the user's answers before doing anything else.

```
我准备开始搭建。在动手之前对齐 7 个问题：

1. 品牌中英文全称？是否有正式 wordmark（比如 U2 LIVING 全大写带空格）？
2. 行业 / 品类？（家具 / 服装 / 室内设计 / 工作室 / 其他）
3. 创立年份 + 创始人 / 城市？（决定 hero eyebrow 和 footer 法律行）
4. 参考品牌（任何让你"就要这种感觉"的网站）？
5. 主要城市 / 工作室地址？（决定 footer 列结构）
6. 网站核心场景：纯展示 / 邀约预约 / 批发渠道 / 设计师对接？
7. 有没有任何不能用的元素或必须有的元素？（PROJECT.md 风格 anti-CTA 规则、宗教 / 文化禁忌、必须出现的产品名等）
```

If the user gives partial answers, ask the missing items in a follow-up. Don't proceed to Phase 1 until 7/7 are answered. Pre-fill answers from anything they mentioned earlier in the conversation.

### Step 3: Confirm understanding before building

Once you have answers, send back a 6-line confirmation:

```
确认理解：
- 品牌：[name]，[industry]，[city]，[year]
- 风格锚：[reference brands] → editorial / 杂志感 / 浅色中性
- 主场景：[scenario]
- 必有 / 禁忌：[constraints]
- Hero 形式：100dvh full-bleed [video / image]，oversized serif headline + italic accent
- 我会先用占位品牌跑通骨架，搭好后给你 desktop+mobile 截图过审

如果以上有偏差告诉我，否则我开干。
```

User confirms or corrects → proceed to Phase 1.

For taste skill briefing template + canonical design tokens, see `references/01-taste-skeleton.md`.

---

## Phase 1 — Skeleton build with placeholder brand

**Goal**: a working HTML/CSS/JS skeleton that lives or dies on aesthetic alone, using a fictitious placeholder brand.

### What you build

- 7 sections: Hero / 001 Manifesto / 002 Index of products / 003 Featured Object / 004 Workshop / 005 Notes / Footer
- Top marquee ribbon
- Floating pill nav with glass-pill scroll state
- Reveal animations (translate + opacity, no filter:blur)
- Pretext-based per-line text reveal for paragraphs
- Reduced-motion fallback

### Performance rules baked in from day 1

- **Never `filter: blur`** on reveals or images — GPU slow path
- **Never `mix-blend-mode`** for noise — same problem
- **Ken Burns is one-shot** (`forwards`, 4.5s), never infinite
- **Hero video mask = sibling overlay div with `radial-gradient(...)` background**, NEVER `mask-image: radial-gradient` directly on `<video>` (alpha-mask is GPU slow path)
- **`will-change` only while pending**, drop after animation completes
- **`scroll` listener must be rAF-throttled**

### Use placeholder data freely

Make up a brand name, products, locations, year, copy. The aesthetic gets locked here. Real data flows in Phase 2. Paste tokens from `references/01-taste-skeleton.md` into `:root`.

### Deliverable

A page that renders cleanly at desktop (1440×900) and mobile (390×844). Take screenshots of both before declaring Phase 1 done.

---

## [USER REVIEW REQUIRED — Phase 1 sign-off]

Before proceeding to Phase 2, send the user:

```
骨架搭好了。截图：
- desktop: [path]
- mobile: [path]

请 review 三件事：
1. Hero 的字体 + 留白 + 标题排版是不是你想要的"杂志感"？
2. 各 section 的节奏（manifesto 编辑感 / index 错位卡片 / object 编辑式分屏 / workshop 三框 / notes 双栏）方向对不对？
3. 整体浅色中性调 + 米褐意大利体强调 OK 吗？

要改就告诉我哪一块；OK 的话我去做下一步（生成填空 md 让你填真实信息）。
```

Iterate on aesthetic until user verbally signs off. Do NOT proceed past Phase 1 without explicit "OK / 可以 / 继续" type confirmation.

---

## Phase 2 — Real content migration

**Goal**: replace all placeholder copy with real brand data via async batch.

### Step 1: Generate fill-in markdown template

Create `~/Downloads/<brand-slug>-content.md`. Each block has 4 parts: where it appears, current placeholder, writing guide, 2-3 sample variations the user can pick or remix. Aim for ~500 lines covering all sections + footer + ribbon.

For canonical template structure, see `references/02-content-template.md`.

### Step 2: Send to user, wait for fill-back

```
内容收集表已生成：~/Downloads/<brand-slug>-content.md (~500 行)

每个 block 我给了 2-3 个示例方向，你选 / 改 / 重写都行。填完发我路径即可，~30 分钟的事。
```

### Step 3: Batch replace

When they return the path:
1. Read the file
2. `Edit` per block with `replace_all: false`
3. Repeated placeholders (e.g. brand name appearing 30+ times) use `replace_all: true`
4. Fix line breaks where titles broke awkwardly (`&nbsp;` between glued pairs)

### Step 4: Apply brand-specific design tweaks

If the user's content reveals constraints (anti-CTA rule, language preference, must-include legal text), apply them. Examples:
- Anti-CTA → delete sign-up section, footer Correspondence column carries equivalent
- All-English copy → lock language switcher to en
- Roman numeral copyright year for editorial brands (`MCMXCVII—MMXXVI`)

---

## Phase 3 — User generates AI images

**Goal**: user produces a batch of images that match the site's editorial visual language, ready to drop in.

### Why the user generates these (not you)

- ChatGPT / DALL·E 3 produces better results when the user iterates on prompts directly with their own brand context
- Image generation is hands-on creative work; the user wants control over which exact 4-5 product shots make the cut
- Saves your context budget — image gen is iterative and noisy

### Hand them this brief

```
现在轮到你出图。我们需要 4-6 张产品 / 场景图，全部要"高端家具杂志摄影"质感（也就是和你这个网站调性贴合的）。

【需要的图片】
1. Hero 视频源图（16:9 横，主产品居中）— 用于生成 hero 视频
2. Index 卡片 1（主推产品 5:6 portrait）
3. Index 卡片 2（4:5 portrait）
4. Index 卡片 3（4:5 portrait）
5. Index 卡片 4（5:7 tall portrait — forthcoming / 抽象材质特写也行）
6. Object section 编辑式特写（4:5 portrait，可以复用 hero 那张产品但不同景别）

【ChatGPT 提示词模板】
Generate a [aspect ratio] [horizontal/portrait] hero image for a high-end [furniture/your category] website.

Subject: [specific product description with materials, e.g., "gray fabric sectional sofa with chaise lounge, white topstitching, adjustable headrests"]

Setting: pure white seamless background OR warm-cream minimalist room with [optional context: window view / herringbone floor].

Lighting: studio product lighting — soft key light from upper left, gentle fill, subtle rim light catching [material name] texture, soft shadows.

Style: photorealistic, premium [furniture/your category] catalog aesthetic, magazine quality. No text, no watermarks, no logos.

【关键】
- 必须严格控制比例（DALL·E 3 默认会跑偏，prompt 里反复强调）
- 文件名一律 ASCII 小写连字符（sofa.png, table.png）— 中文名 + 空格会让后面 fal.ai 上传崩溃
- 出来不满意就重 prompt，每张图先迭代到自己满意再批量发我

出完一批告诉我，我会做压缩 + 替换 + 接下来生成视频。
```

For aspect ratio map + ChatGPT prompt examples, see `references/05-image-asset-pipeline.md`.

---

## Phase 4 — Insert images into site

**Goal**: compress + place every image, swap placeholder.svg references.

### Step 1: sips compression

```bash
cd <project>/img
sips -s format jpeg -s formatOptions 85 -Z 1600 \
  "<source>.png" --out <name>.jpg
```

`-Z 1600` resizes longest edge to 1600px preserving aspect. Quality 85 is editorial sweet spot. Typical 2.5MB PNG → 500KB JPEG.

### Step 2: Map images to slots

| Slot | Aspect | File |
|---|---|---|
| Hero video source | 16:9 | hero-source.jpg (kept aside for Phase 5) |
| Index `--feature` card | 5:6 | mari-table.jpg |
| Index `--offset` card | 4:5 | gianni-sofabed.jpg |
| Index 3rd-child | 4:5 | kori-table.jpg |
| Index `--quiet` card | 5:7 | u26-material.jpg |
| Object section media | 4:5 | reuse mari-table.jpg (browser caches) |
| Atelier 3 frames | 3:4 / 4:5 / 3:4 | placeholder.svg (workshop shots are hard to source authentically; placeholder is editorial) |

### Step 3: Update HTML

```html
<img
  src="./img/<name>.jpg"
  alt="[descriptive alt with material + context]"
  loading="lazy"
  decoding="async"
  onerror="this.onerror=null;this.src='./img/placeholder.svg';"
/>
```

`onerror` fallback is critical — if the JPG ever 404s, page degrades gracefully to placeholder.

For `placeholder.svg` source + image filter recipes, see `references/05-image-asset-pipeline.md`.

---

## Phase 5 — Generate hero video(s) from images

**Goal**: produce 1-2 hero videos via image-to-video AI, using the Phase 3 images as source.

### Tool selection

**Default: Hailuo 02 Pro on fal.ai** (`fal.ai/models/fal-ai/minimax/hailuo-02/pro/image-to-video`).

Why Hailuo over Veo / Kling / Seedance:
- Form is dead simple (Image + Prompt + Optimizer toggle, that's it). Veo cuts scenes by default; Kling 3.0 Pro's form has 10+ booby-trap fields that randomly break uploads
- $0.48/6s, 768p output (Topaz upscale handles 4K need in next step)
- Image upload reliable for ASCII filenames
- Hailuo respects "no cuts" prompts more reliably than Veo (Veo cuts scenes by default unless prompt explicitly forbids; Hailuo's default is single take)

### Hand the user this brief

```
图片我已经放进去了，现在生成 hero 视频。

打开 fal.ai/models/fal-ai/minimax/hailuo-02/pro/image-to-video，登入后：
1. 上传 [hero-source.jpg]（你 Phase 3 给我的 16:9 横图）
2. Prompt 用这个：
   [我会按你的产品调整给你具体 prompt]
3. Prompt Optimizer 关掉
4. 点 Run，~30-60s 出片，扣 $0.48
5. 跑完发我视频路径，我做 4K 升级 + 接到网站

如果一段视频不够（你想要切换镜头那种），我们生成 2 段（不同景别 / 不同产品），后面我做交叉淡入循环。
```

### Per-product Hailuo prompt template

```
Slow smooth cinematic [push-in / 90-degree orbit / dolly pull-back / static medium shot] toward
the [product description with 2-3 specific material words from the image], single continuous shot,
no cuts. [Lighting description, 1 sentence]. Photorealistic, premium [category] catalog aesthetic,
luxury brand hero video.
```

### Topaz 4K upscale (after each video)

URL: `fal.ai/models/fal-ai/topaz/upscale/video`

| Field | Value | Why |
|---|---|---|
| Model | **Gaia HQ** | Designed for AI-generated content (NOT Artemis — that's for real footage) |
| Upscale Factor | **2.0** for 1080p, **3.0** for 720p source | H.264 caps at 4096×4096; 1080p×2 = 4K UHD safely |
| Recover Detail | 0.3 | gentle, don't go above 0.5 |
| H264 Output | ON | essential for web playback |

Cost: $0.48/6s.

For full prompt examples + model comparison + all settings, see `references/03-hero-video-pipeline.md`.

---

## Phase 6 — Insert videos into site (crossfade integration)

**Goal**: 1 or 2 videos play seamlessly with smooth A→B→A loop.

### Compress for web (multi-format fallback)

```bash
# H.265 main (Safari/Chrome/Edge — ~45% smaller than H.264)
ffmpeg -y -i <topaz-output>.mp4 \
  -c:v libx265 -crf 24 -preset medium -tag:v hvc1 \
  -vf "scale=2560:-2,fps=60" \
  -an -movflags +faststart \
  hero-a.h265.mp4

# H.264 fallback (Firefox / Chromium)
ffmpeg -y -i <topaz-output>.mp4 \
  -c:v libx264 -profile:v high -preset slow -crf 21 \
  -vf "scale=2560:-2,fps=60" \
  -an -movflags +faststart \
  hero-a.h264.mp4
```

Repeat for video B if there's one.

### Drop in the crossfade HTML/CSS/JS

Two `<video>` elements stack in `.hero__media`:

```html
<video class="hero__video is-active" data-hero-video autoplay muted playsinline preload="auto" aria-hidden="true">
  <source src="./video/hero-a.h265.mp4" type='video/mp4; codecs="hvc1"' />
  <source src="./video/hero-a.h264.mp4" type="video/mp4" />
</video>
<video class="hero__video" data-hero-video muted playsinline preload="auto" aria-hidden="true">
  <source src="./video/hero-b.h265.mp4" type='video/mp4; codecs="hvc1"' />
  <source src="./video/hero-b.h264.mp4" type="video/mp4" />
</video>
```

JS scheduler:
- `timeupdate` event → when active clip is within `FADE_LEAD = 0.8s` of end, call `advance()`
- `advance()` flips `.is-active` class; CSS opacity transitions 800ms
- B's first frame primed at init (`play().then(pause + currentTime=0)`) so first crossfade has zero decode latency
- IntersectionObserver suspends both videos + ribbon when hero off-screen
- Page Visibility API as tab-backgrounded fallback

`PLAYBACK_RATE = 0.75` for editorial slow-down (0.7-0.8 sweet spot).

For complete HTML/CSS/JS template ready to paste, see `references/04-multi-video-crossfade.md`.

---

## Phase 7 — Design system convergence (terminal pass)

**Goal**: 30-min audit + token consolidation right before deploy. Don't do it earlier (mid-build churn is fine), don't skip it (ship-time inconsistency is the #1 reason work "looks AI-made").

### Audit

```bash
grep -oE '[0-9]+ms' styles.css | sort -u | wc -l           # transition durations
grep -oE 'cubic-bezier\([^)]+\)' styles.css | sort -u      # easing curves
grep -oE 'wght" [0-9]+' styles.css | sort -u                # font weights
grep -oE 'letter-spacing: [0-9.]+em' styles.css | sort -u   # tracking
```

If you see 8+ durations / 4+ easings / 5+ weights, you're in convergence territory.

### Target ladder (always converge to these)

```
Durations:  --dur-fast 320ms / --dur-base 620ms / --dur-slow 1100ms
Easings:    --ease (crisp UI) / --ease-soft (reveals + image scale)
Weights:    --w-display 340 (h1/h2) / --w-card 380 (h3) / --w-italic 320 / --w-body 400
Tracking:   --tr-pill 0.22em / --tr-ghost 0.24em / --tr-meta 0.28em / --tr-mono 0.18em
Buttons:    pill (.cta + .nav__cta same spec) / ghost-link (.hero__cue + .ghost-link same spec)
```

Search-replace mode `replace_all: true` makes this fast.

For full token set + button base styles + reduced-motion + checklist, see `references/06-design-system-convergence.md`.

---

## Phase 8 — Deploy

```bash
cd <project>
vercel deploy --prod --yes
```

Build is ~13s for the canonical 30-40MB static project. CLI handles auth, project creation, alias.

### Hidden ops via Vercel REST API

Token at `~/Library/Application Support/com.vercel.cli/auth.json`. Two operations the CLI doesn't expose:

```bash
VTOKEN=$(jq -r '.token' "$HOME/Library/Application Support/com.vercel.cli/auth.json")
TEAM=$(jq -r '.orgId' .vercel/project.json)
PROJ=$(jq -r '.projectId' .vercel/project.json)

# Rename project (preserves deploy history; alternative is delete+recreate which doesn't)
curl -sS -X PATCH "https://api.vercel.com/v9/projects/${PROJ}?teamId=${TEAM}" \
  -H "Authorization: Bearer ${VTOKEN}" -H "Content-Type: application/json" \
  -d '{"name":"newname"}'

# Disable SSO Protection (Vercel default blocks new aliases with 401)
curl -sS -X PATCH "https://api.vercel.com/v9/projects/${PROJ}?teamId=${TEAM}" \
  -H "Authorization: Bearer ${VTOKEN}" -H "Content-Type: application/json" \
  -d '{"ssoProtection":null}'
```

Manually bind new short alias after rename (Vercel doesn't auto-create on rename):

```bash
# Get the latest deployment URL first
DEPLOY_URL=$(vercel ls --json 2>/dev/null | jq -r '.[0].url' | head -1)
# Or grab it from the most recent `vercel deploy --prod` output

vercel alias set $DEPLOY_URL <newname>.vercel.app
```

The `<full-deployment-url>` looks like `<project>-<hash>-<user>-projects.vercel.app` and is shown in the JSON response of every `vercel deploy --prod` call (under `deployment.url`).

Optional cleanup of old alias:

```bash
vercel alias rm <oldname>.vercel.app --yes
```

For full deploy + custom domain + troubleshooting, see `references/07-vercel-deploy.md`.

---

## Pitfalls Library (read this BEFORE you hit them)

20 pitfalls catalogued, each with **symptom → diagnosis → fix**. See `references/08-pitfalls.md`.

Top 5 to keep in active memory:

1. **Hero scroll jank** — `filter: blur` or `mix-blend-mode` somewhere. Grep both. Delete.
2. **Mask over video kills 60fps** — `mask-image: radial-gradient` is GPU slow path. Use `.hero__veil` with normal `radial-gradient(...)` background overlay instead.
3. **fal.ai upload "Error initiating upload"** — file name has Chinese / spaces / emoji. Rename to ASCII before upload.
4. **Topaz upscale H.264 error** — Upscale Factor too high. For 1080p source, max factor is 2 (1080×2=4K). For 720p source, max 3.
5. **`*.vercel.app` returns 401 after rename** — Vercel default `ssoProtection: "all_except_custom_domains"`. PATCH `ssoProtection: null` via API.

---

## User Preferences (read this BEFORE replying)

The original developer has these preferences (observed from the U2 Living build, 2026-05). Treat as default starting assumption; adjust if the actual user signals otherwise:

- **Concise Chinese, action-oriented**. Short replies preferred. "继续 / 好的 / 下一步 / 再调慢一点" → match with single concrete next action.
- **Delegator mode**: when they say "下一步是什么" or "你来解决", they want a specific recommendation, not a planning menu.
- **Real data only**: no lorem ipsum, no stock photos. Generate placeholders that look intentional ("image awaiting production" SVG > random stock).
- **Performance + quality dual sensitivity**: will proactively ask "can we make this smoother / sharper". Flag potential pitfalls before they ask.
- **Accept system rewrites**: when performance debt accumulates, willing to do token-system rewrite rather than patches.
- **Screenshot-driven feedback**: they'll send a screenshot pointing at a 4-pixel gap or a marquee that overlaps a button. Take that level of attention seriously.
- **"看真实站点 not 脑补"**: when they mention a real library or website, look at its actual code/source. Don't guess.

For full preferences notes (communication, decision style, what NOT to do), see `references/09-user-preferences.md`.

---

## Master checklist (use this at session start)

```
[ ] Phase 0: Invoke taste skill, ask 7-question alignment, await answers
[ ] Phase 0: Confirm understanding back to user before building
[ ] Phase 1: Build skeleton with placeholder brand, perf rules baked in
[ ] Phase 1: USER REVIEW — desktop + mobile screenshots, await sign-off
[ ] Phase 2: Generate ~/Downloads/<brand>-content.md, await fill-back
[ ] Phase 2: Batch replace via Edit tool
[ ] Phase 3: Hand image-generation brief to user, await batch
[ ] Phase 4: sips compression, ASCII naming, slot mapping, HTML swap
[ ] Phase 5: User generates videos via Hailuo 02 Pro on fal.ai, sends back
[ ] Phase 5: Topaz Gaia HQ × 2.0, H.264 ON
[ ] Phase 6: ffmpeg compress to H.265 + H.264 fallback, integrate crossfade HTML/CSS/JS
[ ] Phase 7: Design system convergence (3 durations / 2 easings / 4 weights / 2 buttons)
[ ] Phase 8: vercel deploy --prod --yes
[ ] Phase 8: API rename + SSO disable + alias bind if needed
```

Total time on a focused build: 1-2 weeks for a new domain (if user is responsive on Phase 0/2/3/5 inputs), 3-4 days for a re-skin where assets exist.

---

## Reference Files Index

When you enter a phase, read the matching reference. Don't preload all of them — fetch on demand.

- `references/01-taste-skeleton.md` — Phase 0/1: taste skill briefing template + canonical design tokens
- `references/02-content-template.md` — Phase 2: fill-in markdown template structure
- `references/03-hero-video-pipeline.md` — Phase 5: Hailuo / Topaz / Veo / Kling / Seedance comparison + full prompt examples
- `references/04-multi-video-crossfade.md` — Phase 6: complete HTML/CSS/JS template
- `references/05-image-asset-pipeline.md` — Phase 3/4: ChatGPT prompts + sips commands + placeholder.svg + aspect ratios
- `references/06-design-system-convergence.md` — Phase 7: full token set + button system + audit script
- `references/07-vercel-deploy.md` — Phase 8: CLI + REST API + alias management
- `references/08-pitfalls.md` — all phases: 20 pitfalls catalogued
- `references/09-user-preferences.md` — all phases: communication / decision / aesthetic notes
