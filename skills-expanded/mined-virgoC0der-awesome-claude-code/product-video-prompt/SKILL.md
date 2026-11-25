---
name: product-video-prompt
description: >
  从 Shopify 商品链接生成面向海外 TikTok/Reels 的伪 UGC 商品视频 prompt，目标模型为 Seedance
  （字节跳动文生视频）。默认输出伪 UGC 风格——第一人称 POV，像真实用户随手拍的产品分享，
  带对镜头讲述、手持感、生活化场景。可选品牌高级感模式。完整流程：抓取 Shopify 商品数据
  （products.json API 优先）、看图分析、提炼亮点、生成 15 秒 9:16 竖屏英文视频 prompt。
  触发场景：用户给 Shopify 商品链接并想生成 UGC 视频、product video、视频脚本、TikTok 视频、
  Reels 视频、Seedance prompt、带货视频、短视频脚本、达人视频；即使用户只说"帮我给这个商品
  写个视频"也要触发。用户说"品牌视频"、"高级感视频"、"brand video"时走品牌模式；否则默认 UGC。
---

# Product Video Prompt Generator (Pseudo-UGC Default)

把 Shopify 商品链接变成一个**伪 UGC 英文视频 prompt**，目标模型：**Seedance（字节跳动文生视频）**，发布平台：**海外 TikTok / Instagram Reels**。

## 两种输出模式

| 模式 | 何时使用 | 风格特征 |
|------|---------|---------|
| **Pseudo-UGC（默认）** | 用户没特别要求 / 提到 UGC / TikTok / Reels / 达人 / "真实感" | 第一人称 POV，对镜头讲述，手持感，生活化场景，真实质感 |
| **Brand Mode（可选）** | 用户明确说"品牌视频"、"高级感"、"brand"、"commercial"、"广告大片" | 电影感镜头、精致场景、第三人称叙事、品牌调性 |

**默认走 Pseudo-UGC**。只有当用户明确要求品牌感时才切 Brand Mode。

两种模式的前 4 步（数据抓取、看图分析、亮点提炼、参考图选择）完全一样，区别只在 Step 5 生成 prompt 时的模板。

---

## Workflow

### Step 1: 获取商品数据

从用户提供的 Shopify 商品链接获取数据：

1. **提取域名和 handle**：`https://example.com/products/cool-shoe` → `example.com` + `cool-shoe`
2. **优先 products.json**：请求 `https://{domain}/products/{handle}.json`，成功即解析 JSON
3. **Fallback**：web_fetch 商品页 URL，从 HTML 提取

必需字段：title、description、images（所有 URL）、variants、price、tags、product_type、vendor。

**视频资源（重要）**：很多 Shopify 商品页面带有官方产品视频，通常嵌在图片 gallery 里，格式是 `.mp4` 文件。获取视频 URL 的方式：

- `products.json` 不返回视频——必须用 `web_fetch` 拿商品页 HTML
- 在 HTML 里搜索 `cdn/shop/videos/` 或 `.mp4` 关键字
- 典型 URL 模式：`https://{domain}/cdn/shop/videos/c/vp/{hash}/{hash}.HD-1080p-*.mp4`

找到的视频要作为**重要资产**记录下来——它在 Step 5 生成 prompt 时可以作为 `[MOTION REFERENCE]` 提供给 Seedance（图生视频模式，或直接作为动作参考说明）。这对有复杂机械动作的产品（开合、折叠、变形）特别有用——参考视频比任何文字描述都准确。

如果没找到视频，记录为 "No official product video available"，不影响流程继续。

### Step 2: 看图（+ 看视频）分析 — 提取硬信息

看 3-5 张关键图，必须提取：

**硬信息（给全局约束用）**：
- 确切颜色（"哑光黑"而不是"黑色"）
- 材质（仿皮革/网布/橡胶/金属/磨砂塑料等）
- Logo 信息（位置、颜色、内容）
- 结构部件（几条拉链、几个扣子、是否对称）
- 关键图形元素（条纹/人字纹/图案，具体位置）

**叙事信息**：
- 产品品类（鞋类 / 服饰 / 3C / 美妆 / 家居 / 食品 / 运动 / 包袋配饰）
- 可动部件
- 目标人群画像（年龄、性别、生活方式、兴趣）
- 使用场景

**如果有产品视频**，额外提取（用文字描述视频内容，不要求真的能播放视频）：
- 视频里产品如何被操作（动作顺序、节奏、方向）
- 关键变形过程的分解（比如"0-2s 拉链从 A 拉到 B"）
- 手 / 脚 / 产品的相对位置和进入画面的角度
- 操作的快慢节奏（是一气呵成还是分步停顿）

这些信息在 Step 5 写 `[MOTION REFERENCE]` 块时直接用，避免让模型"凭空想象"动作过程。

### Step 3: 提炼商品亮点

3-5 个核心卖点。每个包含：
- 亮点名称（简短）
- 一句话描述（突出差异化）
- 英文短 tagline（后续可能变叠字或台词碎片，不超过 8 英文字）

优先级：功能性 > 视觉/设计 > 情感/场景。

### Step 4: 选择 UGC 人设（仅 Pseudo-UGC 模式）

真实感的关键是**具体的人**。不要"一个女生"，要"一个名叫 Chloe 的 24 岁大学生"。

根据目标人群画像设计：

- **年龄 + 身份**：24 岁 barista / 32 岁 working mom / 19 岁 college freshman / 38 岁 dad of two
- **外形锚点**：发色+发型、一个让人记住的特征（雀斑/眼镜/特定穿搭风格）
- **说话风格**：casual、enthusiastic、deadpan-funny、thoughtful
- **拍摄场景**：自己的卧室 / 厨房 / 车里 / 办公桌 / 健身房 / 街头走路时

**人设要匹配产品目标人群**，但不等于"直接扮演目标人群"。举个关键区别：
- 卖 adaptive sneaker，人设**不**应该是"虚构的 disabled 角色做自我测评"——这在欧美会被 disability community 批评为 tokenism 或 inspiration porn
- 人设**可以**是"照顾 disabled 长辈的家属"、"在康复科工作的 PT"、"给朋友买礼物的人"——他们接触产品有真实理由，但不把别人的 disability 拿来作为营销噱头

### Step 4.5: 跨文化伦理审视（**重要**）

生成 prompt 前和生成后都要做一次伦理审视，确保脚本不会冒犯目标市场（默认欧美 TikTok/Reels 用户）。这一步不可跳过——**冒犯性内容的商业代价远高于脚本不够亮眼**。

#### 高风险雷区（必须避免）

**1. Disability / 残障相关**
- ❌ 虚构 disabled 人物推销 adaptive 产品（"Maya had a stroke, so..."）→ tokenism
- ❌ 把 disability 当作幽默素材（"my other hand is useless lol"）→ ableism
- ❌ "Inspiration porn"——把 disabled 人物日常行为渲染成"励志奇迹"
- ❌ 用 "overcome / despite / suffering from" 这类框架描述 disability
- ✅ 正确做法：用 allies / caregivers / professionals 视角，或者不指定健康状态让产品卖点自己说话
- ✅ 如果真的需要 disabled representation，说明这应该由 creator/品牌与真实 disabled creator 合作

**2. Race / Ethnicity**
- ❌ 不要在人设里指定特定种族除非是产品本身的叙事需要（比如卖 afro hair care 产品的 Black creator 合理）
- ❌ 不要用刻板印象（"Asian mom who's strict about..."、"Latina who's passionate about..."）
- ❌ 不要让白人 creator 用其他族裔的文化元素（AAVE、religious dress 等）——cultural appropriation
- ✅ 默认不指定种族，用中性描述（"dark brown hair"、"warm smile"）

**3. Body / Appearance**
- ❌ 不要对身材、体重、外貌做正面或负面评价
- ❌ 不要暗示产品让人"显瘦/更好看/更 acceptable"
- ❌ 对时尚产品：不写 "body type" 限制（"这个适合瘦的人穿"）
- ✅ 直接描述产品特性，不贴身体评价

**4. Gender / Sexuality**
- ❌ 不要假设性别规范（"as a woman, I need..."、"real men use..."）
- ❌ 不要用异性恋叙事默认（"my boyfriend said..."）除非产品本身相关
- ✅ 默认用中性叙事或明确多元视角

**5. Socioeconomic**
- ❌ 不要暗示"买了这个你就高人一等"（classism）
- ❌ 不要 "struggling to afford" 叙事来制造情绪（poverty porn）
- ✅ 实用价值 / 情感价值为主

**6. Mental Health**
- ❌ 不要把产品描述成"治愈焦虑/抑郁"的 cure
- ❌ 不要轻描淡写地用 mental health 词汇（"this is my therapy"、"ADHD brain rotted"）
- ✅ 如果产品真的是 wellness 相关，用温和的 "helps me feel calmer" 而不是诊断语言

**7. Religion / Politics**
- ❌ 不要涉及宗教符号或政治立场，除非品牌本身是明确相关的
- ✅ 保持世俗、中性

**8. 语言和幽默**
- ❌ 不要用 AAVE（African-American Vernacular English）除非 creator 明确是 Black
- ❌ 不要用可能冒犯的 slang（"ghetto"、"basic" 对特定群体、"tribal" 形容风格等）
- ❌ Self-deprecating humor 要非常小心——特别是关于 identity 方面的
- ✅ 中性的 Gen-Z / Millennial casual English 最安全

#### 伦理审视清单（生成后必做）

写完 prompt 后，逐条审视：

- [ ] 人设的任何 identity 标签（disability / race / gender / sexuality / religion）**是产品叙事真正需要**的吗？不是的话删掉
- [ ] 所有台词读起来像是这个具体人物会真实说出口的吗？有没有把别人的 identity 拿来当营销素材？
- [ ] 任何"幽默"点是否可能伤害到某个群体的感情？
- [ ] 产品卖点的 framing 是否暗示了对某类人的负面判断？（例："easy enough even for clumsy people" → 侮辱性）
- [ ] 如果这个脚本明天就上 TikTok，最 savvy 的评论区会不会立刻 pile on？

**关键原则**：当拿不准时，走保守路线——**不指定** identity 比错误指定安全得多。让产品的功能和美学自己说话，比编造代表性人设更有效。

### Step 5: 生成 Prompt

**先读 `references/prompt-methodology.md`** 理解生成模型的能力边界，再写 prompt。

---

## Pseudo-UGC Mode（默认）

### 核心理念

伪 UGC 的目标是**让观众下意识认为这是真实用户分享**，绕开对广告的本能抵触。做到这点靠三件事：
1. **手持感视觉语言**（非专业运镜、略微抖动、自然光）
2. **第一人称口语化台词**（对镜头讲述，像发 TikTok）
3. **生活化场景细节**（杂乱的背景、真实的家居、不完美的构图）

**Seedance 限制提醒**：Seedance 不生成音频。对白台词写在 prompt 里是**给模型理解场景用的**（让它知道人物在说话、嘴型怎么动、情绪是什么），实际音频需要后期配。写法上用 `[The creator says to camera: "..."]` 这种明确标记，不要写成"她说..."这种容易触发音频审核的中文叙述。

### Prompt 结构（Pseudo-UGC）

```
(1) Title line（英文）
(2) Global constraints（英文，product lock）
(3) Motion reference block（英文，仅当有官方产品视频时）
(4) Creator persona block（英文，人设锁）
(5) UGC style block（英文，视觉风格锁）
(6) Scene-by-scene script（英文，4-5 段）
(7) On-screen text & CTA（英文）
```

### (1) Title Line

`{Product Name} — Pseudo-UGC TikTok/Reels Video (9:16 vertical, 15 seconds)`

### (2) Global Constraints（英文）

```
[GLOBAL CONSTRAINT — Product Appearance]
As shown in Reference Image 1, the {product} appearance must remain consistent 
across all frames: {exact color}, {material}, {logo location and content}, 
{key design elements}. No new structural parts may appear.

[GLOBAL CONSTRAINT — {mechanism name, if applicable}]
{How the mechanism works}. Closed state = Reference Image X. Open state = Reference Image Y.
```

### (3) Motion Reference Block（仅当有官方产品视频时）

如果 Step 1 找到了官方产品视频，加这个块。它特别有用于有复杂机械动作的产品（开合、折叠、穿戴过程）——参考视频能让 Seedance 理解动作节奏和方向，远比文字描述准确。

```
[MOTION REFERENCE]
An official product video is available as a motion reference: {video URL}
Use this video as the reference for: {具体哪些动作}, matching its pacing and 
mechanical motion. Key motion beats from the reference video:
- {0-Xs: 动作 A 的节奏}
- {Xs-Ys: 动作 B 的方向}
- {...}
Do NOT deviate from the mechanical motion shown in the reference video.
```

如果没有官方视频，**跳过这个块**——不要编造一个不存在的视频 URL。

### (4) Creator Persona Block（英文）

```
[CREATOR PERSONA]
- Name/Identity: {e.g., Chloe, 24, barista in Brooklyn}
- Appearance: {hair, a memorable feature, typical outfit style}
- Speaking style: {casual/enthusiastic/deadpan/thoughtful}
- Filming setup: {selfie handheld / phone propped on shelf / mirror}
- Personality note: {one line about vibe}
```

### (5) UGC Style Block（英文，不可缺）

这块是让视频看起来"像 UGC"的关键。必须包含：

```
[UGC STYLE]
- Handheld phone camera look, slight natural shake
- Vertical 9:16 framing, slightly imperfect composition
- Natural lighting only — no studio lights, no flattering key light
- Real apartment/bedroom/kitchen background with everyday clutter visible
- iPhone-quality footage aesthetic (not cinematic)
- No professional camera moves — only natural handheld pan/tilt
- Creator looks directly into camera when talking (selfie POV)
```

### (6) Scene-by-Scene Script（英文，4-5 段）

每段包含：
- 时间标记：`[0-3s | Scene Title]`
- 场景环境（1-2 句，具体地点+光线）
- Creator 动作（具体到她/他在做什么）
- **对镜头的台词**（用 `[Creator to camera: "..."]` 标记，短句，口语化）
- 产品状态（引用 Reference Image）
- 镜头说明（handheld, POV, close-up 等）

**UGC 台词的写法**：
- 口语化，有语气词（like / okay so / honestly / no joke）
- 制造"我不是在打广告"的 tone（"I wasn't gonna post about this but..."）
- 有真实感反应（停顿、语气上扬、小惊讶）
- 不超过 2 句一段

#### UGC 标准 4 段结构（紧凑型）

```
[0-3s | Hook — Direct-to-camera opener]
场景+人物入镜
[Creator to camera: "{hook line — a question / a claim / a pain point}"]
镜头：selfie handheld

[3-7s | The demo]
展示产品核心功能（用参考图绑定状态）
[Creator to camera: "{the key benefit in one casual sentence}"]
镜头：产品特写 + 她的反应切换

[7-11s | The proof / reaction]
使用后的反应 / 对比 / 细节展示
[Creator to camera: "{genuine reaction or specific detail}"]
镜头：产品细节 + 她的笑脸/惊讶

[11-15s | Soft CTA]
收尾 + 品牌提及（不要硬广告腔）
[Creator to camera: "{casual recommendation, link in bio style}"]
最后一帧：on-screen text "{brand handle} — {tagline}"
```

5 段变体（如果产品复杂需要更多演示时间）：
```
0-2 | Hook
2-6 | Problem/context
6-10 | Demo
10-13 | Reaction/proof
13-15 | Soft CTA
```

### (7) On-Screen Text & CTA（英文）

UGC 风格的叠字要**像用户自己打的**，不是品牌广告感的大字标语：

- ✅ 小字幕，有时带 emoji（like real TikTok captions）
- ✅ 用词随意："wait till you see this" / "not sponsored but" / "this is genius"
- ❌ 不要大字冲击："CHANGE YOUR LIFE" / "BUY NOW"

CTA 形式：
- 最后一帧显示 `@{brand_handle}` 或 `#{brand_hashtag}`
- 配一句 soft CTA："link in bio" / "found on {brand website}" / "saved this to my faves"

### Pseudo-UGC 自查清单

**真实感**：
- [ ] 有具体的人设（名字、年龄、身份），不是"a girl"
- [ ] 有至少 3 句对镜头的口语台词（短、口语化、有语气词）
- [ ] 背景是真实生活场景，有自然杂乱感（不是纯白影棚）
- [ ] 镜头是手持 / 自拍 视角，不是专业运镜
- [ ] 自然光，没有 studio lighting 描述
- [ ] 第一句 hook 有"我真的不是在打广告"的 tone

**产品约束**：
- [ ] Global constraints 写明了颜色、材质、logo、关键结构
- [ ] 关键状态绑定了 Reference Image
- [ ] **如果 Step 1 找到了官方产品视频，prompt 里有 `[MOTION REFERENCE]` 块引用视频 URL**
- [ ] **如果没找到官方视频，prompt 里也没有 `[MOTION REFERENCE]` 块（不编造假 URL）**
- [ ] 没有让模型做它做不到的复杂机械动作
- [ ] 同段内没有手+脚+产品复杂协同
- [ ] 没有任何音乐/音效/BGM 描述

**复杂机械结构加固**（仅产品有特殊机制时适用，方法论文档 Pattern A/B/C/D）：
- [ ] **Pattern A 几何拓扑**：机制描述写清 START / PATH / END + 对称性（非对称机制要显式声明 "NOT symmetric"）
- [ ] **Pattern A 整体性**：可变形的大面板声明为 "ONE single connected piece"，明确不会 "split into halves"
- [ ] **Pattern B 显式禁止**：把模型可能幻想成"可动"但实际不动的部件显式锁死（"X is closed/rigid, CANNOT open"），区分装饰性元素和功能性元素
- [ ] **Pattern C 状态连续性**：开场锁定起始状态（如 "no shoes on yet"），段间动作前重申状态（如 "before this moment, right foot is still bare"）
- [ ] **Pattern D 单次演示**：如果动作需要重复（穿两只鞋/戴两只耳环），只演示一只，另一只保持起始状态或不入镜

**语言**：
- [ ] Prompt 整体英文
- [ ] 对白用 `[Creator to camera: "..."]` 格式标记
- [ ] 台词是 Gen-Z / millennial casual English，不是 brand copy

**跨文化伦理（Step 4.5 必做）**：
- [ ] 人设没有虚构 disabled / 特定种族 / 特定宗教身份作为营销素材
- [ ] 没有把 disability / race / gender / body / mental health 当作幽默素材
- [ ] 没有 inspiration porn / tokenism / poverty porn 的 framing
- [ ] 所有 identity 标签都是产品叙事真正需要的，不是"装饰性多元"
- [ ] 台词和叠字文案想象在 TikTok 评论区会不会被 pile on

---

## Brand Mode（可选）

### 何时使用
用户明确说"品牌视频"、"高级感"、"brand video"、"commercial"、"广告大片"。

### Prompt 结构（Brand Mode）

```
(1) Title line（英文）
(2) Global constraints（英文）
(3) Scene-by-scene narrative（英文，4-6 段）
(4) On-screen text & CTA（英文）
```

**区别**：
- 没有 Creator Persona block（用第三人称叙事）
- 没有 UGC Style block（改为 Cinematic Style block）
- 场景更精致、光线更戏剧化
- 叠字是 brand tagline 风格（大字、简洁、英文）
- 人物是"代言人/用户"而非"creator"

### Cinematic Style Block

```
[CINEMATIC STYLE]
- Professional camera work, smooth gimbal movements
- Studio-quality lighting with key/fill/rim
- 9:16 vertical, carefully composed frames
- Color-graded cinematic look
- Clean, styled sets (not cluttered real-life spaces)
```

### Brand Mode 叙事结构（5 段标准）

```
[0-2s | Scene setup + hook]
[2-5s | Core benefit demo]
[5-8s | Usage process]
[8-11s | Style/detail showcase]
[11-15s | CTA with brand logo]
```

---

## Step 6: 组装最终输出

```markdown
# {Product Name} — Video Prompt Report

## 📦 Product Info
- Name / Category / Price / Link / Brand / Material / Variants

## 🔍 Highlights
1. **[highlight]**: [description] — Tagline: "[English]"
2. ...

## 🎬 Mode: {Pseudo-UGC | Brand}
Reason: ...

## 👤 Creator Persona (if Pseudo-UGC)
- Name/Identity / Appearance / Speaking style / Filming setup

## 📸 Reference Assets
| # | Asset | Type | Content | Used in |
|---|-------|------|---------|---------|
| Ref 1 | [image URL] | Image | 闭合侧面 | Global constraint, [0-3s] |
| Ref 2 | [image URL] | Image | 展开俯视 | Global constraint, [3-7s] |
| Ref Video | [video URL] | Video | 官方动作参考（如果有） | Motion reference |

*Video 行仅当 Shopify 页面有官方产品视频时出现*

## 🎯 Seedance Prompt
(Complete English prompt, copy-paste ready)
```

---

## ⚠️ 严禁写入 prompt 的内容

Seedance 是**文生视频**，不生成音频。以下内容无效且会触发 `output audio may contain sensitive information` 审核失败：

- ❌ 音乐描述（"indie music"、"upbeat soundtrack"、"BGM"）
- ❌ 音效描述（"click sound"、"footsteps"、"door closing"）
- ❌ 声音相关词汇（"voiceover"、"narration"、"soundscape"）

**UGC 对白的特殊处理**：
- 用 `[Creator to camera: "text"]` 标记——这是**场景指示**，不是音频生成指令
- 模型会理解"此时人物在对镜头说话、有嘴型动作、情绪对应"
- 实际音频后期录制

如果要表达"轻快氛围"，用画面语言：明亮光线、跳跃镜头节奏、人物轻盈动作。

---

## Important Notes

- **默认走 Pseudo-UGC 模式**，用户明确要求品牌感才切 Brand Mode
- Prompt **整体英文**（目标平台是海外 TikTok/Reels）
- 必读方法论：`references/prompt-methodology.md`
- 人设具体化——有名字、有年龄、有身份、有外形锚点
- UGC 台词口语化，Gen-Z / Millennial tone，不是 brand copy
- 对白用 `[Creator to camera: "..."]` 格式，不写成 "she says" 或中文叙述
- 3-5 张参考图够用，不贪多
- **Step 1 务必尝试提取官方产品视频 URL**（在 HTML 里搜 `cdn/shop/videos/` 或 `.mp4`），找到就加 `[MOTION REFERENCE]` 块——对复杂机械动作产品特别关键
- 遇机械结构复杂的产品，动作保守——文字锁状态，参考图/视频讲形态
