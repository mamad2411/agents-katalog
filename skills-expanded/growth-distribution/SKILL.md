---
name: growth-distribution
description: Cross-platform content distribution and growth strategy for DYA app across 10+ platforms (Xiaohongshu, Douyin, TikTok, Instagram Reels, X/Twitter, Reddit, Weibo, Bilibili, WeChat Video). Use when planning social media posts, distributing video content, optimizing for platform algorithms, writing platform-specific copy, scheduling content releases, analyzing engagement data, deciding posting strategy, or maximizing organic reach. Also use when creating video ads that need multi-platform distribution, or when discussing growth/marketing/推广/发帖/推流/算法/涨粉 topics.
---

# Growth Distribution Skill

Multi-platform content distribution engine. Combines algorithm research with battle-tested DYA marketing execution.

## ⭐ 第零条铁律：先给价值，再带产品

> **This is the single most important rule. Everything else is secondary.**

小红书规则核心逻辑："禁止低价值硬广，鼓励有价值分享"

| ✅ 正确顺序 | ❌ 错误顺序 |
|-----------|-----------|
| 先讲方法论/干货/真实经历 | 先推产品/功能介绍 |
| 再把 App 作为"实现方法的工具"自然带出 | 再讲"我们App能干嘛" |
| 算法判定：有价值内容 → 推流 | 算法判定：营销导流 → 限流 |

### 成功案例：solopro（438粉/1693赞藏）
- 498赞帖「如何搭建永不混乱的人生系统？」→ 先讲系统方法论，再展示App实现
- 344赞帖「在过一种一目了然的生活」→ 先讲生活理念，再自然引入工具
- 101赞帖「如何"真的"在24h内重启人生？」→ 疑问句标题+场景拆解+App是工具

### DYA 适配示例
- ❌ 「同意吗APP上线了，功能介绍」
- ✅ 「恋爱中最该说清楚的3件事（第3件90%的人都忽略了）」→ 文末自然引出DYA
- ✅ 「一个人做了个App 被苹果拒3次终于上架了」→ 开发者故事（已验证有效：8赞8评251浏览）
- ✅ 「口头承诺为什么总是不靠谱？3个让约定真正生效的方法」→ 方法论+工具

## Core Workflow

1. **Write content using value-first approach** — Method/story first, product second
2. **Identify content type** — Video (60s/15-30s/Reels) or text+image post
3. **Select platforms** — Use platform priority matrix below
4. **Adapt content** — Apply platform-specific rules from `references/platform-playbook.md`
5. **Visual consistency** — Use unified brand style (see Visual Identity section)
6. **Schedule** — Follow phased distribution timeline
7. **Post-publish** — Execute first-hour engagement protocol

## Platform Priority Matrix

| Priority | Platforms | Why |
|:--------:|-----------|-----|
| ⭐⭐⭐ | 小红书 · TikTok · 抖音 | Highest ROI for DYA's content type (争议性+情感+developer story) |
| ⭐⭐ | IG Reels · 微信视频号 | Original content boost + social chain amplification |
| ⭐ | B站 · X · Reddit · 微博 | Niche/long-tail/developer community |

## Universal Rules (All Platforms)

1. **先给价值再带产品** — The #0 rule above. Never lead with product.
2. **Front 3 seconds = life or death** — Hook must grab within 3s or all platforms throttle
3. **No external links in post body** — Bio + comment + self-reply only
4. **Comments >> Likes** — Design content to spark discussion, not just appreciation
5. **Share/Repost = nuclear weapon** — Content should trigger "tag your partner" impulse
6. **First hour is critical** — Coordinate group members to engage within 60 min of posting
7. **3 video versions**: 60s full · 15-30s highlight · with/without URL watermark
8. **No cross-platform watermarks** — IG penalizes TikTok watermarks and vice versa
9. **不虚构互动数据** — 帖子不能写"收到私信""评论区炸了"等可被验证为假的描述

## 小红书内容创作方法论

### 🚀 S040v5 AI 梗图连续生成流水线 (baoyu-integrated)
基于开源项目 `baoyu-xhs-images` 验证过的 10.5K⭐ 方法论，DYA 小红书生图必须遵循以下 **4 大机制**：

#### 1. 视觉锚点死锁 (Reference Image Chain)
- **绝对铁律**：生成多张连环图(Carousel)时，**首图(封面)** 必须先无参考单独生成。
- **锚点绑定**：从第 2 张图开始，强制将第 1 张图作为 `--ref` 或视觉参考输入给大模型。
- **目的**：保证 3-4 张图里的主角脸、衣服、画风、用色 100% 连贯，消除 AI 抽卡崩坏感。

#### 2. 滑动漏斗流设计 (Swipe Flow Architecture)
小红书单图必死，必须拆成 3-4 张首尾相连的图：
- **图1 (Cover)**: `Sparse` (极简排版)。最高视觉冲击 + 数字/痛点钩子。
- **图2 (Setup)**: `Balanced` (平衡排版)。建立痛点共鸣，用自身经历代入。
- **图3 (Core)**: `Dense/List` (密集排版)。核心干货输出、对比表格（Before/After）。
- **图4 (Ending)**: `Sparse` (极简排版)。总结金句 + CTA 互动诱导。

#### 3. 二维审美矩阵解耦 (Style × Layout Matrix)
生图指令不要模糊，必须精确组合「画风」与「排版布局」：
- **Style (画风)**：`cute`(甜美), `warm`(治愈分享), `bold`(大字报强调), `minimal`(极简职场), `notion`(黑白知识卡), `screen-print`(波普艺术海报)。
- **Layout (布局)**：`sparse`(留白聚焦), `balanced`(均衡信息), `dense`(信息密卡), `comparison`(左右对比), `quadrant`(四象限分类)。
- *指令示例*："用 Screen-print 风格 + Comparison 布局画一张产品对比图。"

#### 4. 强制滑动钩子 (Swipe Hooks)
除了尾图，前面每一张图的右下角或文末，必须加微型诱导短语：
- "第一个就很强大👇" / "猜猜下一个是什么？👇" / "最重要的来了👇"

#### 5. 🔴 视觉迭代铁律：先锁文字，再做视觉 (MEMORIES.md 3/24 battle-tested)
> **PUA帖 10 轮迭代 (V2→V10) 验证**: V2 文字内容最强但视觉差 → V3-V5 视觉升级却丢失文字深度 → V9 赛博朋克风「太丑太low」→ V10 回到品牌色才通过。

- **铁律**: 先锚定最佳文字版本（信息深度），再以此为不可变基准做视觉升级
- **严禁**: 为视觉好看而简化/删减文字内容
- **品牌色 > 潮流风格**: 品牌色(charcoal #0d1117 + gold #C9A84C) 稳定可信，赛博朋克/霓虹 = 廉价感
- **流程**: ① 定稿文字 → ② 用户确认文字 → ③ 视觉化（锁定文字不动） → ④ 视觉迭代只调排版/配色/字体

### 标题写法
- **疑问句/痛点句** >> 陈述句（点击率高 2-3x）
- 示例：「如何"真的"在24h内重启人生？」「恋爱中最该说清楚的3件事」
- 标题 ≤ 20 字
- 标签全中文（英文标签零搜索量）

### 正文结构
- **❶❷❸ 编号拆解**：每段一个使用场景/方法，降低阅读门槛
- **嵌入FAQ**：正文直接回答用户高频问题（消除购买壁垒）
- **尾句提问**：「你觉得呢？」「你会用这种方式吗？」→ 邀请评论
- **语态**：共情式、朋友式（"我知道这听起来有点奇怪，但..."），不要官方说教

### 评论区运营
- **🚨 S040v4 铁律: 评论区置顶禁止自推广** — 高互动帖零个作者在评论区提项目名/搜索词/下载链接/"看我主页"
- ❌ 评论区不得出现: 项目名/App名/GitHub搜索词/App Store搜索/下载链接/"看我主页"/"搜XXX"/功能清单
- ✅ **评论区置顶应该做**: 补充故事细节("补个后续：第4次终于过了") / 回应投票 / 抛新问题引互动
- ❌ 不直接在评论区写兑换码/链接/微信号
- 每条评论都详细回复（也算评论数，增加CES）

### 内容矩阵（多角度覆盖不同搜索意图）
- **开发者故事**：被苹果拒3次、36天极限开发（已验证最有效）
- **亲密关系方法论**：恋爱中的沟通技巧、信任建立方法
- **产品使用场景**：租房协议、朋友间的约定、亲密前的确认
- **FAQ科普**：电子签名法律效力、隐私保护

### 制造稀缺感
- 「前100名公测用户免费Pro」「限量名额」「绝版福利」

### 预告机制
- 提前预告即将发布的视频/功能更新，锁定关注

## Visual Identity（视觉统一性）

> solopro 爆款秘诀之一：所有帖子统一暗色+紫色渐变+iPhone mockup = 品牌辨识度

### DYA 品牌视觉规范
- **配色**：黑色底 + 荧光绿/粉色（DYA 品牌色）
- **封面图**：暗色渐变背景 + iPhone mockup 展示 App 界面
- **字体**：大字标题叠加在暗色底上（高对比度）
- **一致性**：所有帖子保持相同色调和构图风格

## 微信群发布规范 (MEMORIES.md 3/19 battle-tested)

> **龙虾塘事件验证**: 长版功能更新被用户直接否决——"太长了，这样直接刷微信群的手机屏幕了"

### Half-Screen Rule (半屏铁律)
- **内容长度**: 控制在手机半屏以内（约 8-10 行），绝不刷屏
- **禁止**: 功能清单、版本号堆叠、技术术语罗列
- **推荐格式**: 痛点投票 > 功能列表
  - ❌ "v2.30.0: Memory Gap Prevention + Sync Up Enforcement + ..."
  - ✅ "用AI写代码最崩溃的瞬间是？1️⃣换个对话就失忆 2️⃣干着干着跑偏 3️⃣修bug上下文爆了 4️⃣多项目乱串 5️⃣以上全中"
- **技巧**: 每个痛点选项暗扣产品功能，用户投票即产生共鸣，自然引出产品
- **语气**: 群友聊天式，非官方公告式
- **适用**: 微信群、Discord、Telegram 等即时通讯群组

## Video Distribution Timeline

### Phase 1: Day 0 (国内平台)
```
12:00  抖音     60s full + ¥50 Dou+ test
12:30  小红书   60s + developer story caption + SEO keywords
13:00  视频号   60s → share to 朋友圈 + 微信群
14:00  B站      60s or extended BTS version
14:30  微博     60s + doyouagree.app link (微博 OK with links)
```

### Phase 2: Day 1 (海外平台)
```
09:00 EST  TikTok     60s native upload (no watermark)
10:00 EST  IG Reels   60s separate export (no watermark)
11:00 EST  X          Text-first post (video in self-reply next day)
```

### Phase 3: Day 2-3 (深度互动)
- Reply to every comment on all platforms
- X: upload native video (not link)
- Reddit: builder-angle post if unblocked (no links in body)

## Content Adaptation Rules

| Rule | Applies To |
|------|-----------|
| Value-first, product-second | ALL platforms (most important) |
| Title ≤ 20 chars | 小红书 |
| No hashtags | X (post-2025 algorithm change) |
| No external links in body | TikTok, IG, 小红书, X (50-90% reach penalty) |
| Links OK in body | 微博, Reddit (with karma) |
| Developer story angle | 小红书 ✅ verified, 微博 ✅, X ✅ |
| Emotional/controversy angle | 抖音, TikTok, IG Reels |
| Simplified Chinese only tags | 小红书 (English tags = 0 search volume) |
| Loop design for completion rate | TikTok, IG Reels, 抖音 |
| 编号拆解+疑问句标题 | 小红书 (solopro验证有效) |
| 评论区置顶故事型追评(禁自推广) | 小红书, 抖音, B站 (S040v4) |

## Account Positioning（账号气质）

> **博主化，而非官方化**

- 名字「同意吗APP」本身没问题，问题在内容的营销感浓度和账号整体气质
- 弱化「官方号」冰冷感 → 强化「独立开发者/亲密关系探索者」人设
- 人设包装：Solo developer + 生活方式分享 + 亲密关系探索
- 语态：朋友分享经验，不是官方说教

## Platform-Specific Details

For detailed algorithm mechanics, CES scoring formulas, engagement weight multipliers, and platform-specific strategies, read `references/platform-playbook.md`.

Key sections:
- **小红书 CES评分公式** — `grep "CES" references/platform-playbook.md`
- **TikTok Follower-First Testing** — `grep "Follower-First" references/platform-playbook.md`
- **X权重乘数表** — `grep "权重倍数" references/platform-playbook.md`
- **抖音三级火箭** — `grep "三级火箭" references/platform-playbook.md`

### X/Twitter 算法情报 (2025-2026 全网验证)

> 来源: Sprout Social, hashmeta.com, posteverywhere.ai, GPTZero, Reddit 社区, Grok AI 系统更新

**🔴 铁律: 正文外链砍 30%-90% 曝光**
- 含外部链接的帖子被算法严重降权（导流出站 = 平台不喜欢）
- **正确做法**: 链接放第一条 self-reply，或用 X 原生 Article 功能
- 实测: 配额帖 4.1% 互动率但仅 146 views，推算无外链可达 300-400 views

**📊 互动权重乘数 (影响推荐分)**
| 行为 | 权重 (vs 赞) | 策略 |
|------|:----:|------|
| 回复 (有作者回复) | **150x** | 引导评论 + 积极回复每条 |
| 转推/Repost | **20x** | 写值得转发的观点 |
| 收藏/Bookmark | **10x** | 提供实用/可收藏的内容 |
| 赞/Like | **1x** | 基线 |

**📐 Thread vs 单条**
- **Thread (3-5条)** — 算法偏爱: dwell time 更长 + "thread completion rate" 是新排名因子 + 每条推文独立曝光入口
- **单条长推+配图** — 适合争议/观点/情绪帖。钩子够强时单条也能爆
- **Thread 6+ 条** — 风险: completion rate 下降，反而不如单条
- **原则**: 知识帖/教程 → Thread (3-5条)。争议/观点/吐槽 → 单条+配图

**💎 X Premium**
- 2-4x 曝光加权。回复被算法优先展示
- 考虑开通（成本低/回报高）

**📹 内容类型偏好**
- 原生视频 > 图片 > 纯文本
- 竖版 9:16 视频优先

### Hacker News 平台规则

**格式**: 纯文本，不支持图片/视频/Markdown。代码用缩进 2 空格
**Ask HN**: 标题 "Ask HN: ..." + 正文。无法编辑/删除，一击必中
**Show HN**: 标题 "Show HN: Name – Description" + 正文 + URL
**最佳发帖时间**: 周二/三 8-11 AM UTC (北京 16:00-19:00)
**养号**: karma ≥ 20 + 2 周活跃 + 10 条有价值评论。不求赞（反作弊算法惩罚）
**评论**: 具体经验 > 空泛赞美。2-4 句有信息量。坦诚 tradeoff 是美德
**外链**: HN 帖正文可以放链接（HN 不惩罚外链，跟 X 不同）

## DYA Red Lines (合规红线)

- 🚨 小红书: 私信绝不导流外部（微信/QQ/绿泡泡/V/➕）
- 🚨 小红书: 评论区不提兑换码/福利细节（只说"戳我私信了解～"）
- 🚨 小红书: 评论区不写技术术语（链上/SHA-256/区块链），用"加密存证"替代
- 🚨 全平台: 不用绝对化用语（最好/第一/唯一）
- 🚨 全平台: 广告帖必带 #广告 标签
- 🚨 全平台: 不虚构互动数据（"收到私信""评论区炸了"）
- 🚨 X: 外链放 self-reply，不放正文
- 🚨 IG: 不带其他平台水印
- 🚨 Reddit: 9:1规则（9条真实贡献:1条推广）
- 🚨 小红书: 评论区置顶禁止自推广 (S040v4 铁律 — 项目名/搜索词/下载链接/"看我主页" = 限流)

## Reddit 增长方法论 (OpenPhone 验证·6年103帖)

> 来源: OpenPhone CMO Daryna Kulya，用 Reddit 获得前 1000 客户

### 核心原则
1. **Create more value than you capture** — 带故事/数据/独特洞见，缺任何一个就别发
2. **Don't sound like a marketer** — 直接、透明、有用。❌ 抛光文案 ❌ 通用表述 ❌ 精修配图
3. **Comments > Posts** — 单条高价值评论可获 46 upvotes，超过多数帖子
4. **Engage off-platform** — 有人 DM/回复立刻跟进，主动公开邮箱
5. **Own your subreddit** — 建自己的 r/[品牌]，最终目标是用户互助社区

### 帖子成功公式 (OpenPhone 最佳帖解构)
- ✅ **Unique data**: 分享每个阶段具体做了什么
- ✅ **Personal story**: 有叙事弧而不是功能介绍
- ✅ **Content/subreddit fit**: 帖子主题匹配目标 subreddit 核心兴趣

### 帖子失败公式
- ❌ 不给受众任何价值（只要信息不给故事）
- ❌ 无叙事（错失人格连接机会）
- ❌ 不够具体/和 subreddit 主题无关（通用帖可发在任何地方）

### 评论区黄金规则
- ✅ 在竞品对比帖中提供有用视角 + 坦诚偏见（"I'm from X, bias disclosed"）→ 高 upvote
- ❌ 纯产品推广 + 两个链接 → downvote 灾难

### DYA/MUSE/Prometheus Reddit 适配
- 🎯 DYA: r/relationships · r/datingadvice · r/consent (故事型·不推产品)
- 🎯 MUSE: r/ClaudeAI · r/ChatGPTCoding · r/vibecoding (技术分享·开源贡献)
- 🎯 Prometheus: r/LocalLLaMA · r/artificial · r/singularity (SDK展示·开发者故事)

## Social Listening 工具

### F5Bot (免费·推荐)
- **功能**: 实时监控 Reddit + Hacker News + Lobsters 关键词提及
- **通知**: 分钟级邮件 / Slack / Discord webhook
- **免费层**: 基础关键词追踪（足够早期使用）
- **付费层**: AI 语义搜索 + REST API + 千级关键词
- **注册**: https://f5bot.com
- **建议关键词**: "do you agree app" / "consent app" / "muse agent" / "claude code memory" / "prometheus avatar" / "AI avatar SDK" / "myths labs"

## First-Hour Engagement Protocol

1. Post content
2. Immediately self-comment with **story-type follow-up** (禁自推广，S040v4)
3. Share to 微信公测群 (request genuine engagement)
4. Reply to first 3 comments within 10 minutes
5. Monitor for 1 hour, reply to every comment (详细回复，增加CES)
6. 小红书: Aim for ≥8-char comments (3x CES weight)
