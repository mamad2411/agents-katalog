---
name: web-aeo
canonical_id: discoverability.web-aeo
aliases: [web-aeo, answer-engine-optimization, generative-engine-optimization]
version: 1.1.0
status: stable
created_date: 2026-05-25
parent: discoverability-orchestrator
layer: L12
sibling-skills: [web-seo, web-local-seo, app-aso]
children: []
upstream: [discoverability-orchestrator]
downstream: [security-app-llm]
allowed-tools: Read, Write, Bash, Grep, Glob
forbidden-tools: []
disable-model-invocation: false
description: >-
  AI Discoverability / AEO - Answer Engine Optimization for AI search and generative answer engines (ChatGPT Search / Claude / Perplexity / Google AI Overviews / Gemini / Bing Copilot): makes public content AI-crawlable, extractable as self-contained passages, citable, and machine-readable via llms.txt. This is where "GEO = Generative Engine Optimization" routes; Local SEO belongs to `web-local-seo` and standard search to `web-seo`.
---

# SKILL: web-aeo

> L12 Discoverability 子层 — narrow skill。
> 上游编排：`discoverability-orchestrator`。
> 同级邻居（边界互斥）：`web-seo`（standard search）/ `web-local-seo`（Local SEO / Google Business Profile / NAP / Google Maps）/ `app-aso`（App Store）。
> 下游 escalation：`security-app-llm`（AI bot 实际访问控制 / UA 校验 / rate limit）。

---

## 1. 概述与适用场景

让**公开**内容能被 **AI 答案引擎**抓取、抽取、引用、归属：

- ChatGPT Search（OpenAI）
- Claude Search（Anthropic）
- Perplexity
- Google AI Overviews / AI Mode（Gemini）
- Bing Copilot（Microsoft）
- 其他生成式搜索 / RAG-style 引用

围绕四件事：

1. **AI crawler policy** — robots / meta / 服务端 user-agent 策略，区分 search / training / user-initiated bot
2. **Citability** — passage 写法，让 AI 能抽取并自包含引用
3. **Machine-readable docs** — llms.txt / llms-full.txt / markdown routes / API quickstart
4. **Brand entity signals** — Wikipedia / Reddit / YouTube / 行业目录等实体痕迹（弱启发式）

> **AEO 是 core SEO 的增量，不是平行新渠道**：Google 官方明确其 AI 搜索功能根植于核心 Search ranking 与质量系统——"AEO" / "GEO" 本质仍是 SEO。**核心 SEO（[`web-seo`](../web-seo/SKILL.md)）没做好，先做那个**；本 skill 的 AI-specific 优化是叠加在扎实 on-page SEO 之上的增量，不替代它。别把这里的工具量误读成"AI search 是一条要单独重投入的新渠道"。

### 不在本 skill 范围

| 邻居 skill | 处理内容 |
|---|---|
| `web-seo` | Google/Bing/Baidu standard search、title/meta、Schema.org 通用部分、Core Web Vitals、sitemap、robots（standard search 视角） |
| `web-local-seo` | **Local SEO**（地理位置 / Google Business Profile / Google Maps / NAP / local pack） |
| `app-aso` | iOS App Store / Google Play 商店优化 |
| `appsec-security-orchestrator` | 任何 security / AppSec / threat model / pentest |
| `security-app-llm` | AI bot UA 校验 / rate-limit / auth wall 等真正硬控制 |
| `qa-a11y-compliance` | 可访问性合规（AEO 引用语义化 HTML，但合规审查归 QA） |

本 skill **绝不**做 security 决策。AI crawler policy 在这里是 **discoverability 决策**，不是 authorization。

---

## 2. 命名澄清（关键 callout — GEO 显式归属）

业界文献里的 **GEO** 100% 指 **Generative Engine Optimization**（语义同 AEO），不是 Geographic。Wikipedia 的 "Generative engine optimization" 条目无 Geographic 消歧条目。本配置里：

| 名称 | 含义 | 归属 |
|---|---|---|
| **web-aeo**（本 skill） | Answer Engine Optimization = AI search / generative answer engines 引用优化 | L12 Discoverability |
| **GEO** / Generative Engine Optimization | 同义于 AEO，业界 SEO 圈惯用此称 | **本 skill**（不是 web-local-seo） |
| **web-local-seo**（邻居 skill） | **Geographic / Local SEO** = Google Business Profile / 地图 / 本地 pack / NAP | L12 Discoverability |
| 外部 `geo-seo-claude` 项目里说的 "GEO" | = Generative Engine Optimization（语义同 AEO） | **接入到 web-aeo**，不接入 web-local-seo |

**铁律**：

- 任何"让 AI 引用 / 出现在 ChatGPT Search / Perplexity 结果里"的能力 → **web-aeo**
- 业界 GEO 同义于 AEO，自动 routing 进 **web-aeo**，不再反问
- 任何"出现在 Google Maps / 本地商家 pack / 周边搜索 / NAP 一致性"的能力 → **web-local-seo**
- 用户明确说 "Local" / "Maps" / "Google Business Profile" / "周边" / "实体店" → **web-local-seo**

> Source: https://en.wikipedia.org/wiki/Generative_engine_optimization
> Source: https://searchengineland.com/what-is-generative-engine-optimization-geo-444418

---

## 3. 目标链路（end-to-end）

```
AI crawler 可访问
   ↓ (robots / meta / user-agent policy 明确允许)
AI answer engine 可抽取
   ↓ (HTML 是 server-rendered，关键内容不靠 JS 才出现)
passage 自包含
   ↓ (answer block 单独读也成立，不依赖前文代词)
实体可信
   ↓ (brand / author / 来源能在 Wikipedia / 行业目录 / 长期内容里找到)
docs 机器可读
   ↓ (llms.txt / llms-full.txt / markdown route / API quickstart)
引用路径清晰
   (canonical URL / open graph / 标题清晰 / 内容时间戳)
```

任何一个环节断了，AI 引用率就会下降。本 skill 沿这条链路给 actionable checks。

---

## 4. 执行宪法（继承 L12）

L12 全层共享 **Script-first** 原则：

1. **先跑脚本**，再让 AI 解释 — 不让 AI 直接读网页去"猜 AEO 是否合规"
2. 归一化后的 channel evidence 必须落 `evidence/discoverability/<tag>/ai-search.json`（canonical channel key 是 `ai-search`，**不是** `aeo`；config 端 `channels.aeo` 仅是历史别名，见 §19）；raw 脚本产物落同一 tag 下的 `raw/` 工作目录，经 `discoverability-sdk evidence.append <tag> ai-search <file>` 归并
3. AI 的角色：解读 JSON、route 到修复、决定 blocker vs warn
4. **不重复造轮子**：`zubair-trabzada/geo-seo-claude` 已有 fetch / citability / llms / brand 工具，vendor 进来固定 commit 用
5. Runner 输出 normalize 后再交给 AI，不让 AI 直接拼接 Python script

### 4.1 L12 5 级 priority ladder（本 skill 适用）

按 L12 父层约定，evidence 来源按以下优先级排序，越靠前自动化程度越高、confidence 越高：

| Level | 类型 | web-aeo 中的体现 | auto/manual |
|---|---|---|---|
| 1 | Deterministic script / API / CLI | `geo-seo-claude` vendor 脚本（`fetch_page.py` / `citability_scorer.py` / `llmstxt_generator.py` / `brand_scanner.py`）、curl 抓 robots.txt | 全自动 |
| 2 | Framework adapter | Next.js Metadata API / Nuxt SEO 等的 AI-ready 配置、SSR 检测 | 全自动 |
| 3 | Structured evidence parser | 把 vendor 输出 normalize 成本 skill 定义的 JSON schema | 全自动 |
| 4 | AI synthesis from evidence | AI 读 normalized JSON，分类 blocker vs warn，输出修复优先级 | 全自动 |
| 5 | Manual AI scan only when no script / adapter | 真实查 AI 引擎效果（answer-engine-tests，需要 API key 且部分依赖人工 prompt）、brand entity 弱信号的人工 sanity check | **lower confidence**，evidence 必须标 `source: manual_ai_scan` |

本 skill 中 Level 1-4 覆盖绝大多数 check（crawler policy / citability / llms.txt / 站内信号）；Level 5 仅在 answer-engine simulation 和 brand entity 启发式补充时使用，且 evidence 中必须显式降权（不能与 Level 1-3 同权）。

---

## 5. AI Crawler Policy（核心章节 — 必须分清 bot 用途）

不同 bot 用途完全不同，**业务决策也完全不同**。把"允许 AI 出现在搜索结果"和"允许被训练抓取"混为一谈是最常见错误。

### 5.1 主流 AI bot 速查表（17 行）

| Bot | Operator | 用途 | 业务决策建议 |
|---|---|---|---|
| `OAI-SearchBot` | OpenAI | ChatGPT search 索引可见性 | 通常 **allow**（想出现在 ChatGPT 搜索结果） |
| `GPTBot` | OpenAI | 训练数据抓取 | **policy decision**（允不允许被训练，独立于上一条） |
| `ChatGPT-User` | OpenAI | 用户在 ChatGPT 提问时**当下**触发抓取 | user-initiated；robots 规则可能不适用，需要服务端策略 |
| `ClaudeBot` | Anthropic | 训练 / 通用抓取 | **policy decision** |
| `Claude-SearchBot` | Anthropic | Claude search 索引可见性 | 通常 **allow** |
| `Claude-User` | Anthropic | 用户在 Claude 中提问时触发抓取 | user-initiated |
| `anthropic-ai` | Anthropic | 旧版 Anthropic 抓取标识（legacy / 部分服务仍发送） | **policy decision**（与 ClaudeBot 同步对齐） |
| `PerplexityBot` | Perplexity | search 抓取 | **verify before gate** — 曾有 user-agent 伪造争议，需服务端确认合法性 |
| `Google-Extended` | Google | 控制是否被 Bard/Gemini **训练**（不影响 search index） | **policy decision** |
| `Googlebot` | Google | standard search 索引（同时驱动 AI Overviews 的内容来源） | **allow**（决策归 web-seo，但与 AEO 强相关） |
| `GoogleOther` | Google | Google 内部研发 / 实验性抓取（非搜索 / 非训练直接归属） | **policy decision**（多数项目可 allow） |
| `Bingbot` | Microsoft | Bing 索引（驱动 Copilot 内容来源之一） | allow（决策归 web-seo） |
| `Applebot` / `Applebot-Extended` | Apple | Siri / Spotlight search vs Apple AI training | 分别独立决策 |
| `CCBot` | Common Crawl | 公开 web crawl，下游被多家 AI 训练集采用 | **policy decision**（block 等于间接减少训练曝光） |
| `Bytespider` | ByteDance | 字节系（豆包 / Doubao）训练 / 抓取 | **policy decision** |
| `FacebookBot` / `Meta-ExternalAgent` | Meta | Meta AI 训练 / 抓取 | **policy decision** |
| `Amazonbot` | Amazon | Alexa / Amazon AI 抓取 | **policy decision** |

> Source: https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/5d8c0afe3b44bf9123f6849e97541f85eefabaca/scripts/fetch_page.py

### 5.2 三种业务决策必须分开

```
决策 1: 允许 AI 引用我的公开内容？
  → 影响：OAI-SearchBot / Claude-SearchBot / PerplexityBot / Googlebot / Bingbot

决策 2: 允许 AI 训练我的公开内容？
  → 影响：GPTBot / ClaudeBot / anthropic-ai / Google-Extended /
          Applebot-Extended / CCBot / Bytespider / FacebookBot /
          Meta-ExternalAgent / Amazonbot

决策 3: 允许用户在 AI 客户端"当下"抓取？
  → 影响：ChatGPT-User / Claude-User
  → 这些是 user-initiated bot；robots.txt 行为与 batch crawler 不同
```

**铁律**：

- "允许 AI 搜索收录" ≠ "允许训练抓取" — 两个决策必须独立
- **AI crawler policy 不是 access control**：本 skill 只产 robots/meta 这类 discoverability signal；任何真正的硬控制（user-agent 校验、rate limit、IP 范围、auth wall）→ escalate to `appsec-security-orchestrator` / `security-app-llm`
- **ChatGPT-User / Claude-User 是 user-initiated**，robots 行为与 batch crawler 不同，决策时要明确这一类
- 业务政策（隐私政策 / ToS）声明的"允许 AI 引用"与 robots.txt 实际规则**必须一致**，不一致是 release blocker

### 5.3 robots.txt 模式示例

下面是**模式示例**，不是模板复制就用 —— 每个项目要根据三种决策的实际答案组合。

```
# 示例 A：允许 AI search 收录 + 不允许训练
User-agent: OAI-SearchBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: anthropic-ai
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: CCBot
Disallow: /
```

```
# 示例 B：全部允许（默认开放路线）
# 不需要为 AI bot 单独写条目；默认 robots 规则适用
```

```
# 示例 C：全部拒绝 AI（极端封闭路线）
User-agent: OAI-SearchBot
User-agent: GPTBot
User-agent: ChatGPT-User
User-agent: ClaudeBot
User-agent: anthropic-ai
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Google-Extended
User-agent: CCBot
User-agent: Bytespider
User-agent: FacebookBot
User-agent: Amazonbot
Disallow: /
```

> **注意**：这只是 crawler policy signal。对 `ChatGPT-User` / `Claude-User` 这类 **user-initiated** bot，robots.txt 规则可能不适用 — 仍需服务端 UA / rate-limit / auth 策略来真正拒绝。具体实施走 `appsec-security-orchestrator` / `security-app-llm`。

### 5.4 robots.txt 7 种 classification status

`fetch_page.py` 对每个 AI bot 在 robots.txt 中的状态给出确定的分类，不允许"暧昧"。Audit evidence 中必须使用以下 7 个 status 之一：

| Status | 含义 | 决策动作 |
|---|---|---|
| `BLOCKED` | 该 bot 显式 `Disallow: /` 全站拒绝 | 明确决策；与业务政策一致即 pass |
| `PARTIALLY_BLOCKED` | 该 bot 显式 disallow 了**部分** path（如 `/admin/` `/private/`），其余允许 | 检查 disallow 列表是否漏了敏感 path |
| `ALLOWED` | 该 bot 显式 `Allow: /` 或对应 group 没有 disallow rule | 明确允许 |
| `BLOCKED_BY_WILDCARD` | 没有针对该 bot 的显式 group，但 `User-agent: *` 拒绝了它 | **隐式拒绝** — 业务上若想"允许 AI 搜索"，需为搜索 bot 写显式 allow group |
| `ALLOWED_BY_DEFAULT` | 没有针对该 bot 的显式 group，且 `User-agent: *` 也未拒绝 | 默认允许 — 提醒用户考虑是否需显式策略 |
| `NOT_MENTIONED` | robots.txt 存在但完全未提到该 bot 名 | 显示为"未表态"，提醒补全 policy |
| `NO_ROBOTS_TXT` | 站点根本没有 robots.txt | 全部 bot 默认 allowed；建议至少写一个 baseline robots.txt |

> Source: https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/5d8c0afe3b44bf9123f6849e97541f85eefabaca/skills/geo-crawlers/SKILL.md

### 5.5 Google-Extended ≠ Googlebot（关键 callout）

> **Blocking Google-Extended does NOT block Googlebot. Google-Extended only controls AI training data usage (Bard / Gemini), not search indexing.**

业务含义：

- 想出现在 Google 搜索结果（含 AI Overviews 引用） → `Googlebot: Allow`
- 不想被 Gemini 训练 → `Google-Extended: Disallow`
- 两者完全独立，**互不影响**

类似关系还有：

- `Applebot` 驱动 Spotlight / Siri search → 通常 allow
- `Applebot-Extended` 控制 Apple Intelligence 训练 → 独立决策

> Source: https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/5d8c0afe3b44bf9123f6849e97541f85eefabaca/skills/geo-technical/SKILL.md

### 5.6 AI crawler audit 6 步骤

每次 audit 必须按下面顺序跑完，缺一项 evidence 不完整：

1. **robots.txt** —— 抓 `/robots.txt`，对每个 bot 给 §5.4 的 7 种 status 之一
2. **meta robots** —— 检查关键页 `<meta name="robots">` 是否 `noindex` / `nofollow`，以及是否针对特定 AI bot（如 `<meta name="GPTBot" content="noindex">`）
3. **HTTP headers** —— 抓 `X-Robots-Tag` 响应头；header 比 meta 优先级高，常被忽略
4. **AI files** —— 检查 `/llms.txt` / `/llms-full.txt` / `/.well-known/ai-plugin.json`（如适用），统计是否存在 + 格式合规
5. **JS rendering** —— 抓页面，比较 SSR HTML 与 hydrate 后差异；**关键**：AI crawlers do NOT execute JavaScript，CSR-only 关键内容 = AI 看到空 HTML
6. **Content-Signal directives** —— 检查 `<meta name="ai-content-declaration">` 或 robots.txt 中的 `Content-Signal:` 行（Cloudflare 等新提案），声明内容是否允许被 AI 用于训练 / 推理 / 引用

> Source: https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/5d8c0afe3b44bf9123f6849e97541f85eefabaca/skills/geo-crawlers/SKILL.md

---

## 6. llms.txt 分级使用规则

### 6.1 背景

`llms.txt` 是 **社区 proposal**（llmstxt.org），不是 W3C / IETF 标准。

- 已采用 / 推广的有：Mintlify、Vercel、Nuxt SEO、Anthropic docs 等
- 但 **Google 官方明确说**：出现在 AI Overviews **不需要**任何 AI 专用文件 —— 标准 SEO + 高质量内容已经足够
- 所以 llms.txt 不是**所有**项目的强制要求

### 6.2 分级

| 项目类型 | llms.txt | llms-full.txt | 是 release blocker？ |
|---|---|---|---|
| **docs-heavy / API-heavy** 项目 | **required** | **required** | ✅ 是（missing → blocker） |
| developer tools / SDK / CLI **with public docs/API surface** | required | recommended | ✅ |
| SaaS app（有 public docs） | recommended | optional | warn-only |
| **landing page / marketing site** | optional | optional | ❌ warn-only |
| 内部工具 / 私有产品 | n/a | n/a | n/a |

判断标准：内容**是否需要**被 AI 完整抽取并用作回答 docs 类问题的来源？是 → required；否 → warn-only。

### 6.3 llms.txt 最小模板

```
# Product Name

> One-sentence positioning. What the product is, who it's for, the main outcome.

## Docs

- [Quickstart](https://example.com/docs/quickstart): Get started in 5 minutes.
- [Authentication](https://example.com/docs/auth): API key + OAuth flow.
- [API Reference](https://example.com/docs/api): All endpoints, params, errors.
- [Rate Limits](https://example.com/docs/limits): Per-key and per-IP limits.

## Guides

- [Common patterns](https://example.com/guides/patterns): Real-world examples.
- [Migration guide](https://example.com/guides/migrate): Upgrade between versions.

## Examples

- [Code samples](https://github.com/org/repo/tree/main/examples): Runnable examples.

## Optional

- [Changelog](https://example.com/changelog)
- [Status page](https://example.com/status)
```

`llms-full.txt` 是同一组 URL 的 **完整纯文本内容**拼接（用 `---` 分隔），不是 link list。

### 6.4 llms.txt 完整性 check

- 所有链接必须 **公开可访问**（200 OK，不是 401/403/private）
- 不能链接到 staging / preview / 内部环境
- 不能包含密钥 / 内部 path / 私有 endpoint
- 与 sitemap.xml 中的公开 URL 一致性 ≥ 80%（差异 > 20% 警告）

### 6.5 llms.txt auto-categorization 规则

`llmstxt_generator.py` 用 path keyword 把 sitemap URL 自动归到 5 个 section。除非用户提供自定义映射，否则按下表执行：

| Section | Path keyword（substring 匹配） |
|---|---|
| **Products & Services** | `/pricing` / `/feature` / `/product` / `/solution` / `/demo` |
| **Resources & Blog** | `/blog` / `/article` / `/resource` / `/guide` / `/learn` / `/docs` / `/documentation` |
| **Company** | `/about` / `/team` / `/career` / `/contact` / `/press` / `/partner` |
| **Support** | `/help` / `/support` / `/faq` / `/status` |
| **Main Pages** | 其它未匹配到任何关键词的 URL（含 `/` `/home`） |

规则细节：

- **大小写不敏感**；匹配 path 的任意 substring
- 同一 URL 命中多个 keyword 时按表中**从上到下**优先级（Products → Resources → Company → Support → Main）
- 项目可在 config 里 override 关键词或追加自定义 section
- Section 顺序：Main Pages（顶部）→ Products & Services → Resources & Blog → Company → Support（底部）

> Source: https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/5d8c0afe3b44bf9123f6849e97541f85eefabaca/scripts/llmstxt_generator.py

---

## 7. Citability — AI 引用友好度（passage 写法规则）

AI 答案引擎抽取内容时，倾向选择**自包含、可直接复用、信号清晰**的 passage。

### 7.1 答案块（Answer Block）规则

| 规则 | 说明 |
|---|---|
| 页面开头 1-2 句**直接回答**核心问题 | 不要先讲背景；先回答，再展开 |
| H2/H3 用**问题式或任务式**标题 | "如何 X" / "什么是 X" / "X vs Y" 比 "Overview" 容易被抽取 |
| 每个 answer block **自包含** | 不依赖前文代词（不说 "this"、"上面提到的" 等指代） |
| 关键事实给数字 / 限制 / 适用对象 | "支持 X 平台 / 每月 100 次 / 免费版包含 Y" 这种 fact-dense 段落容易被引用 |
| 用**真实** `<table>`，不用纯视觉 div | AI 抽 table 远比抽 styled div 准 |
| 图片有**描述性** `alt`，不是 "image1.png" | 影响 AI 在多模态场景下的引用 |
| 代码块声明语言（` ```python `、` ```typescript `） | 提高代码 passage 的归属精度 |
| FAQ 只在**真的有 Q&A**时使用 | 假 FAQ（为 SEO 凑的）会拉低质量信号 |

### 7.2 Docs / API 页面专项

| 要求 | 说明 |
|---|---|
| markdown 版本可直接访问 | `/docs/foo.md` 或 `?format=md` 或 `/llms/foo.txt` |
| API docs 包含 quickstart / auth / error / rate limit / examples 5 块 | 缺一项就是 warn |
| 错误码有**完整列表**和**触发条件** | AI 回答"为什么报错 X" 时需要 |
| 每个 endpoint 有可复制的 curl / SDK 示例 | 提高代码块被引用率 |

### 7.3 内部启发式评分（5 维 + 权重 + grade band）

`citability_scorer.py` 内部按 5 维打分（**internal heuristic, not official ranking factor** — 不是任何 AI 引擎的官方排名因子）。完整 Python 实现在 `tools/vendor/geo-seo-claude/scripts/citability_scorer.py`；本节给权重 + 评分要素 + grade band，让 audit evidence 可解读。

| 维度 | 权重 | 评分要素（正则 / 启发式） |
|---|---|---|
| **Answer Block Quality** | 30 | 页面开头 1-2 句是否直接回答 H1/H2 暗示的问题；H2/H3 是否用问题式 / 任务式表达；每段长度是否落在 **134-167 words** 最佳被引区间 |
| **Self-Containment** | 25 | 段落是否不依赖前文代词（`this` / `上面提到的` / `it` / `该产品` 等指代词触发扣分）；专有名词在段内是否首次出现给定义 |
| **Structural Readability** | 20 | 句长方差、Flesch Reading Ease（目标 60-70，8-9 年级）、术语密度、`<table>` 比例、有序列表使用 |
| **Statistical Density** | 15 | 段内**数字 / 限制 / 版本 / 价格 / 时间戳** 出现频率（正则匹配 `\d+(\.\d+)?%?` / 货币符 / 日期 / 版本号） |
| **Uniqueness Signals** | 10 | 与同类 docs 的差异度（防 boilerplate）、专有名词数量、原创数据 / 案例 |

**总分 0-100**。Grade band：

| Grade | 区间 | 含义 |
|---|---|---|
| **A** | 80+ | 优秀，引用友好 |
| **B** | 65+ | 良好，达成内部 OK 阈值 |
| **C** | 50+ | 一般，触发 warn |
| **D** | 35+ | 较差，需重写关键段落 |
| **F** | < 35 | 不合格，blocker 候选（仍仅 warn-only 输出，**不是** release blocker） |

**关键阈值**：研究（Princeton / Georgia Tech / IIT Delhi 2024）显示，AI 答案引擎对 **134-167 words** 长度的段落引用率最高；过短信息不足，过长抽取困难。

**严重提醒（重复 3 次保留）**：

> 这是 **internal heuristic, not official ranking factor**。
> 这是 **internal heuristic, not official ranking factor**。
> 不能向用户/客户展示为"AI 引用官方分数"或包装成 AEO 官方 ranking。

> Source: https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/5d8c0afe3b44bf9123f6849e97541f85eefabaca/scripts/citability_scorer.py
> Source: https://arxiv.org/abs/2311.09735

### 7.4 Schema.org markup for AI citability

Schema.org JSON-LD 是 AI 实体识别 + 引用归属的关键信号。本 skill 关注的是**与 AI citability 相关**的 schema 用法；标准 Schema.org（Product / Article / FAQPage 基础字段）归 `web-seo`。

**JSON-LD 模板路径**（vendor 已固化 6 个模板）：

```
tools/vendor/geo-seo-claude/schema/
  ├── organization.json          # Organization + sameAs ladder
  ├── article-author.json        # Article + Person author + Person.knowsAbout
  ├── local-business.json        # LocalBusiness（注意：标准 Local SEO 归 web-local-seo；
  │                              #   这里只用作 AI 实体信号，sameAs / hasPart 等字段）
  ├── product-ecommerce.json     # Product + sameAs + Brand
  ├── software-saas.json         # SoftwareApplication + Organization
  └── website-searchaction.json  # WebSite + potentialAction (SearchAction)
```

**sameAs priority ladder**（按强度从高到低）：

1. **Wikipedia** —— 最强实体信号，AI 引擎广泛使用
2. **Wikidata** —— 结构化实体，Google Knowledge Graph 等使用
3. **LinkedIn** —— 公司 / 个人权威页
4. **YouTube** —— 频道页（与 brand authority 强相关，详 §8）
5. **Twitter / X** —— 官方账号
6. **Facebook** —— 公司主页
7. **Crunchbase** —— 公司实体（B2B / startup 尤其重要）
8. **GitHub** —— 项目 / 开源组织
9. **Google Scholar** —— 学术 author
10. **ORCID** —— 学术 author 全球唯一标识

**speakable property** —— 让 AI 语音助手知道哪些片段适合朗读：

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": ["h1", ".article-summary", ".answer-block"]
  }
}
```

**警告（必须保留）**：

> **JSON-LD must be server-rendered (not JS-injected).** AI crawlers do NOT execute JavaScript（详 §5.6 第 5 步），客户端注入的 JSON-LD 等同于不存在。

**边界**：

- **标准 Schema.org**（Product / Article 基础字段 / FAQPage / BreadcrumbList / Recipe / Event）→ `web-seo`
- **AI-specific Schema.org**（`sameAs` to Wikipedia / Wikidata、`speakable` property、`Person.knowsAbout`、`Organization.knowsAbout`、`mentions` 引用网络）→ **web-aeo**
- **LocalBusiness 字段中的 NAP / openingHours / address** → `web-local-seo`
- 同一页可能多个 schema → 各 skill 各审各的字段，不互相覆盖

> Source: https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/5d8c0afe3b44bf9123f6849e97541f85eefabaca/skills/geo-schema/SKILL.md

### 7.5 复合 GEO Score（optional, diagnostic only）

Vendor 还提供一个 0-100 的复合 GEO Score，把 6 个 category 加权聚合。仅作 **diagnostic 整体感知**，**不**作 release gate：

| Category | 权重 | 来源章节 |
|---|---|---|
| AI Citability | 25 | §7.3 citability 5 维评分 |
| Brand Authority | 20 | §8.3 Brand Authority Score |
| Content Quality | 20 | §7.6 E-E-A-T 4 维 |
| Technical AI-Readiness | 15 | §5 crawler policy + §5.6 6-step audit + SSR check |
| Schema.org Coverage | 10 | §7.4 AI-specific schema fields |
| Platform-Specific | 10 | §7.7 5 platform tactics |

**总分 0-100**。5 band：

| Band | 区间 | 含义 |
|---|---|---|
| **Excellent** | 90+ | 全维度优秀 |
| **Good** | 75-89 | 综合良好，少量项目可补强 |
| **Fair** | 60-74 | 中等水平，多个维度需要工作 |
| **Poor** | 40-59 | 大量缺口 |
| **Critical** | 0-39 | 几乎不可被 AI 引用 |

**callout（必须保留）**：

> 这个公式 **opinionated, unvalidated by controlled study**。
> 它是 **diagnostic tool, NOT release blocker**。
> Release blockers 只能走 §10 ID-based 列表（policy/robots 不一致、docs-heavy 缺 machine-readable docs、关键页 CSR-only、llms.txt 含 private/404 URL、llms.txt 含 secret）。
> 不允许把 "GEO Score < N → 阻断 release" 写进 CI gate。

> Source: https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/5d8c0afe3b44bf9123f6849e97541f85eefabaca/docs/scoring-methodology.md

### 7.6 E-E-A-T 4 维（4 × 25 pts）

Google 在 quality rater guidelines 中定义的 E-E-A-T 维度被 AI 引擎广泛参考。Vendor 把它实现为 4 维各 25 分共 100 分的内部评分：

| 维度 | 权重 | 评分要素 |
|---|---|---|
| **Experience** | 25 | 第一手案例 / 真实数据 / 截图 / 时间戳 / "I used X for 6 months..." 类一手叙述 |
| **Expertise** | 25 | author 资历 / `Person.knowsAbout` / 学术或行业背景 / 引用权威来源 |
| **Authoritativeness** | 25 | sameAs to Wikipedia / Wikidata / LinkedIn / Crunchbase；外部权威引用本站 |
| **Trustworthiness** | 25 | HTTPS / privacy policy / about page / contact / 透明的修订时间戳 / 第三方验证 |

**内容标准（一手数据）**：

| 页面类型 | 建议词数 |
|---|---|
| Homepage | ~500 words |
| Blog post | 1500+ words |
| Pillar / cornerstone | 2500+ words |
| 段落（最佳被引区间） | 2-4 sentences |
| Flesch Reading Ease | **60-70**（8-9 年级，平衡可读性与专业度） |

**E-E-A-T 仍是 internal heuristic, not official ranking factor** —— 即便 Google 公开提及 E-E-A-T，本 skill 给的 0-100 分仍是启发式合成，**不是** Google 评分。

> Source: https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/5d8c0afe3b44bf9123f6849e97541f85eefabaca/skills/geo-content/SKILL.md

### 7.7 Platform-specific tactics（5 引擎）

不同 AI 引擎抽取 / 引用机制不同，"一次优化全平台搞定"是幻想。Vendor 把 5 个主流引擎的核心 tactic 总结如下：

| Platform | 核心 tactic |
|---|---|
| **Google AI Overviews** | top-10 organic 排名 + 清晰 heading + question-based heading + `<table>` + heading 后立即直接答案 |
| **ChatGPT Web Search** | Bing index 优先（与 Google 不同）+ Wikipedia / Wikidata 实体强信号 + sameAs ladder |
| **Perplexity** | Reddit / forum 社区验证（**远超**传统 SEO authority）+ 学术引用 + 多源交叉验证 |
| **Gemini** | YouTube 内容权重高（vlog / tutorial）+ Google Business Profile + Google Knowledge Graph 实体 |
| **Bing Copilot** | IndexNow protocol（实时通知 Bing 索引）+ LinkedIn company page + meta description（Bing 比 Google 更依赖 meta desc） |

**callout（必须保留）**：

> Research shows **only ~11% of domains are cited by BOTH ChatGPT and Google AI Overviews for identical queries** — platform-specific optimization is essential. 不能假设"在 Google 上能拿到 AI Overviews 引用，ChatGPT 也会引用"，反之亦然。

实操：

- 每个 platform 单独跑一次 answer-engine simulation（详 §12 步骤 8），统计被引用率
- 不要把所有 tactic 都做 —— 按业务优先级选 2-3 个 platform 重点优化
- Evidence 中分平台报告，不合并为单一"AI 引用率"

> Source: https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/5d8c0afe3b44bf9123f6849e97541f85eefabaca/skills/geo-platform-optimizer/SKILL.md

---

## 8. Brand Entity Signals（实体可信度 — 弱启发式）

AI 引用同一个主题时，多个来源会被加权。实体在大数据集里**存在**的概率会被启发式利用。

### 8.1 信号清单 + correlation 数字

| 信号 | 强度 | 检查方式 | correlation（如有公开数据） |
|---|---|---|---|
| Wikipedia 词条 | 强 | API 搜索品牌名 | — |
| Wikidata 实体 | 强 | wikidata.org/wiki/Special:Search | — |
| YouTube 官方频道 / 教程 | 中-强 | YouTube Data API | **0.737**（与 AI 引用频次相关性） |
| Reddit 提及（subreddit / 帖子 / 评论） | 中 | reddit API / 站内搜索 | — |
| Hacker News 提及 | 中 | hn.algolia.com 搜索 | — |
| LinkedIn company page | 中 | linkedin.com/company/<slug> | — |
| 行业目录 / G2 / Capterra / Product Hunt | 中 | 各平台搜索 | — |
| Domain Rating（Ahrefs） | 弱 | Ahrefs API | **0.266**（弱相关，比 YouTube 低很多） |
| 第三方对比文 ("X vs Y") | 弱-中 | Google search | — |
| GitHub stars / forks / 长尾 issue | 弱 | GitHub API | — |

> Source: Ahrefs Dec 2025 brand-mention study (75K brands)
> **Caveat（必须保留）**：single study, not peer-reviewed；correlation ≠ causation；不能反向得出"刷 YouTube 就能提升 AI 引用"。

### 8.2 警告

- 这些是**启发式**信号，**internal heuristic, not official ranking factor** —— 不是任何 AI 引擎的官方 ranking factor
- 不要包装成"AEO 分数"或"AI 引用分数"
- 输出**作为 evidence**，**不作为 release blocker**
- 不允许"刷"这些信号（购买 Reddit 评论、批量创建 Wikipedia 词条等不在本 skill 推荐范围）

### 8.3 Brand Authority Score 公式 + Wikipedia/Wikidata API auto-check

Vendor `brand_scanner.py` 把 §8.1 信号合成一个 0-100 的 Brand Authority Score：

**公式**：

```
Brand Authority Score =
  (YouTube  × 0.25) +
  (Reddit   × 0.25) +
  (Wikipedia × 0.20) +
  (LinkedIn × 0.15) +
  (Other    × 0.15)
```

每个子项是 0-100 的子分数（如 Wikipedia 子分数 = 词条存在 + 内容完整度 + 引用数；YouTube 子分数 = 官方频道 + 订阅数 + 视频更新频率）。

**5 band**：

| Band | 区间 | 含义 |
|---|---|---|
| **Dominant** | 85-100 | 在 AI 引擎中实体识别度极高 |
| **Strong** | 70-84 | 主流引擎稳定识别 |
| **Moderate** | 50-69 | 部分引擎识别，多源验证不足 |
| **Weak** | 30-49 | 实体痕迹少 |
| **Minimal** | 0-29 | 几乎无 brand entity 信号 |

**Wikipedia / Wikidata API auto-check**：

```bash
# Wikipedia API
curl "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={brand}&format=json"

# Wikidata API
curl "https://www.wikidata.org/w/api.php?action=wbsearchentities&search={brand}&language=en&format=json"
```

Runner 自动跑这两个 API，把结果写入 `brand-entity-signals.json`，不需要 API key。

**铁律（必须保留）**：

> **不允许刷信号，只输出 evidence**。
> Brand Authority Score 是 **internal heuristic, not official ranking factor**，不向客户展示为官方 AI ranking。
> 不允许把 "Brand Authority Score < N" 写进 release gate。

> Source: https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/5d8c0afe3b44bf9123f6849e97541f85eefabaca/scripts/brand_scanner.py

---

## 9. geo-seo-claude vendor adapter（接入外部 repo）

> **Vendor pinned commit**: `5d8c0afe3b44bf9123f6849e97541f85eefabaca` (as of 2026-05-25)
> 本 SKILL.md 所有 `> Source: https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/<sha>/...` 引用此 commit；
> 升级 vendor 时按 §9.1 流程：固定新 commit → 全文替换 `<sha>` → 重跑 evidence → ADR review → promote。
> 永远不要用 `main` 分支 raw URL（上游变更会无声影响本 skill 的 evidence schema 和评分公式引用）。

### 9.1 引入方式

`zubair-trabzada/geo-seo-claude` 作为 **vendored submodule**，**固定 commit**：

```bash
# 仅在项目初始化时执行一次
mkdir -p tools/vendor
git submodule add https://github.com/zubair-trabzada/geo-seo-claude.git tools/vendor/geo-seo-claude
git -C tools/vendor/geo-seo-claude rev-parse HEAD
# 记录 commit hash 到项目 ADR
git -C tools/vendor/geo-seo-claude checkout <PINNED_COMMIT>
git add .gitmodules tools/vendor/geo-seo-claude
git commit -m "chore(vendor): pin geo-seo-claude at <PINNED_COMMIT> for AEO tooling"
```

固定 commit 的理由：

- 上游变更不会无声影响本 skill 的 evidence schema
- 评分公式 / 检查项变化必须经过 review 再升级
- 离线 / 受限网络环境也能跑

### 9.2 Vendor 结构与脚本（reference map）

```
vendor: tools/vendor/geo-seo-claude/   (MIT © 2026 Zubair Trabzada, commit-pinned)
  ├── scripts/
  │   ├── citability_scorer.py         # §7.3 算法（5 维加权 + grade band）
  │   ├── fetch_page.py                # §5 AI crawler 解析 + 7 status classification + 14+ bot 速查表
  │   ├── brand_scanner.py             # §8.3 Brand Authority 公式 + Wikipedia/Wikidata API
  │   ├── llmstxt_generator.py         # §6.5 path categorization 规则 + validate
  │   └── generate_pdf_report.py       # §13.1 PDF report 8-section 结构
  ├── schema/                          # §7.4 6 个 JSON-LD 模板
  │   ├── organization.json
  │   ├── article-author.json
  │   ├── local-business.json
  │   ├── product-ecommerce.json
  │   ├── software-saas.json
  │   └── website-searchaction.json
  └── LICENSE                          # MIT — 保留 copyright notice 即合规
```

### 9.3 提供的脚本（adapter 包装表）

| 脚本 | 用途 | 包装策略 |
|---|---|---|
| `fetch_page.py` | 抓页面，提取 text / headers / meta / structured data；给 §5.4 7 种 robots status | runner 限定 URL allowlist + 超时 + UA |
| `citability_scorer.py` | §7.3 passage 5 维评分（加权 + grade band A-F） | normalize JSON schema，不让 AI 直接读 raw score |
| `llmstxt_generator.py` | validate + generate llms.txt / llms-full.txt，含 §6.5 path categorization | validate 模式 read-only；generate 模式写 build artifact 不写源码 |
| `brand_scanner.py` | 扫 YouTube / Reddit / Wikipedia / Wikidata / LinkedIn 等信号；§8.3 Brand Authority Score | 输出 evidence-only，不阻断 release |
| `generate_pdf_report.py` | JSON → PDF 报告；§13.1 8-section 标准结构 | 输出到 `evidence/discoverability/<tag>/raw/report.pdf` |

### 9.4 安全包装（必须）

- **不让 AI 自由调用** vendor 脚本 —— 所有调用走 `pnpm discoverability:audit:aeo` runner
- evidence 输出统一 normalize 成本 skill 定义的 JSON schema
- 内部启发式分数明确标记 `"source": "internal_heuristic"` / `"not_official_ranking": true`
- 外部 API 调用（YouTube / Reddit）需要的 API key 必须从环境变量取，**不**写入仓库
- vendor 升级需要走 ADR + 重跑全套 evidence 才能 promote
- MIT license 合规：保留 vendor 原 LICENSE 文件 + 在项目 NOTICE / README 标注 "includes geo-seo-claude © 2026 Zubair Trabzada (MIT)"

---

## 10. Blocker（必须阻断 release）

| ID | 描述 |
|---|---|
| `ai_crawler_policy_conflicts_with_business_policy` | 商业政策 / 隐私政策声明"允许 AI 引用"但 robots 阻断 OAI-SearchBot / Claude-SearchBot；或反之 |
| `docs_heavy_project_has_no_machine_readable_docs_path` | API / docs 项目缺 markdown route 且缺 llms.txt |
| `critical_answer_pages_have_no_extractable_text` | 关键回答页 CSR-only，主要内容必须 JS 渲染后才出现（AI crawlers do NOT execute JavaScript） |
| `generated_llms_txt_links_to_nonexistent_or_private_pages` | llms.txt 含 404 / 401 / staging / internal URL |
| `llms_txt_contains_secrets_or_internal_endpoints` | 生成的 llms-full.txt 含 API key / 内部 path（同时 escalate 到 `security-app-llm`） |

---

## 11. Warn-only（不阻断 release，但必须列入 evidence）

| ID | 描述 |
|---|---|
| `llms_txt_missing_for_non_docs_site` | landing page / marketing 站缺 llms.txt（推荐但非必须） |
| `citability_score_below_target` | 内部启发式总分 < 65（grade C 以下；internal heuristic, not official ranking） |
| `answer_blocks_not_self_contained` | 答案块依赖前文代词 |
| `brand_entity_signals_weak` | Brand Authority Score < 50（Moderate 以下；internal heuristic） |
| `reddit_wikipedia_youtube_presence_not_found` | 上述渠道完全无痕迹 |
| `perplexity_or_other_ai_bot_policy_not_officially_verified` | 服务端无法 100% 确认 user-agent 合法性（业内曾有伪造争议） |
| `faq_present_without_genuine_qa_content` | 假 FAQ（为 SEO 凑的） |
| `images_missing_descriptive_alt` | 图片 alt 缺失或非描述性 |
| `code_blocks_missing_language_tag` | 代码块未声明语言 |
| `user_initiated_ai_bot_policy_relies_only_on_robots_txt` | 声明 disallow ChatGPT-User / Claude-User 但服务端无 UA 校验时，仅 robots.txt 不能阻止；推荐加服务端 UA 检查（具体实施 → `appsec-security-orchestrator` / `security-app-llm`） |
| `ai_specific_schema_jsonld_client_rendered_only` | AI-specific Schema.org（sameAs / speakable / Person.knowsAbout）只在 JS hydrate 后出现，AI crawler 看不到 |
| `single_platform_tactic_only` | 只针对 1 个 AI 引擎优化，未覆盖业务关键的其他平台（参考 §7.7 5 引擎差异） |

---

## 12. CLI 命令示例

主入口由 orchestrator 统一暴露。

> **路径约定（v1.2 harness）**：下列 raw 脚本产物写到 **tag-scoped** 的 raw 工作目录 `evidence/discoverability/<tag>/raw/`，最终经 `discoverability-sdk evidence.append <tag> ai-search <file>` 归一化进 canonical channel evidence `evidence/discoverability/<tag>/ai-search.json`。**禁止**写 flat `evidence/discoverability/aeo/`（无 `<tag>` 维度 + `aeo` 是 forbidden evidence 文件名；canonical channel = `ai-search`）。下例用 shell 变量 `TAG` 占位。

```bash
# 主命令
pnpm discoverability:audit:aeo --url https://example.com --out "evidence/discoverability/$TAG/raw"
```

内部组合调用：

```bash
# 1. 抓页面
python tools/vendor/geo-seo-claude/scripts/fetch_page.py https://example.com \
  --out "evidence/discoverability/$TAG/raw/page-snapshot.json"

# 2. citability 评分
python tools/vendor/geo-seo-claude/scripts/citability_scorer.py https://example.com \
  --out "evidence/discoverability/$TAG/raw/citability.json"

# 3. llms.txt validate
python tools/vendor/geo-seo-claude/scripts/llmstxt_generator.py https://example.com validate \
  --out "evidence/discoverability/$TAG/raw/llms.validate.json"

# 4. llms.txt generate（建议输出到 build artifact，不直接落到源码）
python tools/vendor/geo-seo-claude/scripts/llmstxt_generator.py https://example.com generate \
  --out "evidence/discoverability/$TAG/raw/llms.generated.json"

# 5. brand entity scan
python tools/vendor/geo-seo-claude/scripts/brand_scanner.py "Example Inc" example.com \
  --out "evidence/discoverability/$TAG/raw/brand-entity-signals.json"

# 6. AI crawler policy 一致性 check（自建 runner，不在 vendor 里）
node tools/runners/aeo/check-crawler-policy.mjs \
  --robots https://example.com/robots.txt \
  --policy ./docs/ai-content-policy.md \
  --out "evidence/discoverability/$TAG/raw/ai-crawler-policy.json"

# 7. answer block 覆盖度 check（自建）
node tools/runners/aeo/check-answer-blocks.mjs \
  --sitemap https://example.com/sitemap.xml \
  --out "evidence/discoverability/$TAG/raw/answer-block-coverage.json"

# 8. answer engine simulation tests（可选 — 真实查 AI 引擎效果，需要 API key；按 platform 分别跑）
node tools/runners/aeo/run-answer-engine-tests.mjs \
  --queries ./tests/aeo/queries.json \
  --platforms chatgpt,perplexity,google-ai-overviews,gemini,bing-copilot \
  --out "evidence/discoverability/$TAG/raw/answer-engine-tests.json"

# 9. PDF 综合报告（§13.1 8-section 标准结构）
python tools/vendor/geo-seo-claude/scripts/generate_pdf_report.py \
  --in "evidence/discoverability/$TAG/raw" \
  --out "evidence/discoverability/$TAG/raw/report.pdf"

# 10. 归一化进 canonical channel evidence（聚合所有 raw finding）
python scripts/discoverability-sdk.py evidence.append "$TAG" ai-search "evidence/discoverability/$TAG/raw/citability.json"
```

---

## 12.1 quality_gates 字段映射

`discoverability.config.yaml` 的 `quality_gates.aeo.*` 字段与本 SKILL 章节的对应关系。runner 拿 config 字段决定 audit 严格度时用此表反查具体 check 的所在节。

| Config 字段 | 对应 SKILL 章节 | Blocker / Warn |
|---|---|---|
| `require_llms_txt_for_docs_heavy_projects` | §6.2 llms.txt 分级（docs-heavy / API-heavy 行）| warn-only（template 默认；channels.aeo=required 时升 blocker） |
| `require_llms_txt_for_marketing_sites` | §6.2 llms.txt 分级（landing / marketing 行）| warn-only |
| `require_ai_crawler_policy_review` | §5 AI Crawler Policy + §10 `ai_crawler_policy_conflicts_with_business_policy` | warn-only（template 默认；channels.aeo=required 时升 blocker） |
| `require_no_private_pages_in_llms_txt` | §10 `generated_llms_txt_links_to_nonexistent_or_private_pages` + `llms_txt_contains_secrets_or_internal_endpoints` | **blocker**（含 secret 或 internal endpoint → escalate AppSec / `security-app-llm`） |
| `require_answer_blocks_self_contained` | §7.1 答案块规则 + §11 `answer_blocks_not_self_contained` | warn-only |
| `require_machine_readable_docs_path` | §6 llms.txt + §7.2 docs / API 页面专项（markdown route OR llms.txt OR llms-full.txt 三选一） | warn-only |

字段名在 `quality_gates.aeo.*` 下显式 false 时，对应 check 降级为 info 或跳过；显式 true 或缺省按上表 severity 强制。

注：template 中 `min_average_citability_score` 已显式 commented out（"internal heuristic, never an official ranking factor"），本 SKILL 保持一致 — **不**把该字段列为已生效 mapping。如果项目主动 uncomment 启用，runner 必须将其 severity 强制为 warn_only。

---

## 13. Evidence 输出（落盘文件）

归一化后的 channel evidence 落 `evidence/discoverability/<tag>/ai-search.json`（canonical key `ai-search`，schema 由 orchestrator / harness contract §4 定义）；下表的 raw 脚本产物落同一 tag 的 `raw/` 工作目录，被 `ai-search.json` 的 `findings[].evidence_path` 反查引用。**禁止** flat `evidence/discoverability/aeo/`、`aeo.json` 文件名、自产 `gate-result.json`（gate 产物只由 `discoverability-sdk gate.check` 写 `<tag>/gate-result.yaml`）。

| 文件 | 内容 |
|---|---|
| `ai-crawler-policy.json` | 实际 robots 规则 vs 业务政策声明的一致性、每个 bot 类型的 allow/disallow 决策（§5.4 7 种 status）、是否区分 search/training/user-initiated |
| `citability.json` | 关键页 5 维 score（§7.3 grade band）+ 段落级 finding |
| `llms.validate.json` | 现有 llms.txt 合规性、链接可达性、与 sitemap 的一致度 |
| `llms.generated.json` | 生成版 llms.txt 候选（§6.5 path categorization；不直接覆盖源码，需 PR review） |
| `brand-entity-signals.json` | Wikipedia / Wikidata / Reddit / YouTube / LinkedIn 等信号扫描结果 + §8.3 Brand Authority Score |
| `answer-block-coverage.json` | 答案块是否自包含、H2/H3 是否问题式、关键页是否有 1-2 句开头答案 |
| `answer-engine-tests.json` | （可选）真实查询 AI 引擎结果，分平台统计是否被引用 / 被准确归属（§7.7 5 platform） |
| `page-snapshot.json` | 原始抓取产物（中间产物，可被 GC） |
| `report.pdf` | 综合可读报告（§13.1 8-section 结构） |
| `_meta.json` | runner 版本、vendor commit、时间戳、CLI 参数 |

### 13.1 PDF report 标准结构

`generate_pdf_report.py` 输出固定 8 个 section，便于客户 / 内部 review 一致解读：

1. **Cover** —— 项目名 / canonical URL / 报告时间 / vendor commit / 总分（GEO Score band）
2. **Executive Summary** —— 1 页摘要：整体 band + top 3 blocker + top 5 warn + 主要修复方向
3. **Score Breakdown** —— §7.5 6 category 雷达图 + 每项得分 + 简短解读
4. **AI Platform Readiness** —— §7.7 5 引擎分平台 readiness 评估
5. **AI Crawler Access** —— §5 全 bot 速查表（17 行）+ §5.4 每 bot 的 7 种 status
6. **Key Findings** —— 详细 finding 列表，按 severity 排序（Blocker → Warn → Info）
7. **Prioritized Action Plan** —— 修复任务列表，按 effort × impact 排序
8. **Appendix** —— 原始 evidence JSON 摘录 + vendor commit hash + 引用文献链接

**视觉规范**：

| 元素 | 值 |
|---|---|
| Primary color | `#1a1a2e` |
| Success color | `#00b894`（score ≥ 80） |
| Warning color | `#fdcb6e`（score 40-79） |
| Danger color | `#d63031`（score < 40） |

**Score gauge color band**：

- **Green** 80+
- **Blue** 60-79
- **Yellow** 40-59
- **Red** < 40

**Format**：US Letter（8.5 × 11 in）、page numbers、headers、watermarks（vendor commit + 生成时间）。

> Source: https://raw.githubusercontent.com/zubair-trabzada/geo-seo-claude/5d8c0afe3b44bf9123f6849e97541f85eefabaca/scripts/generate_pdf_report.py

---

## 14. 决策流程（route map）

```
触发关键词命中 web-aeo
  ↓
读项目类型 → docs-heavy / saas / landing / internal
  ↓
读业务政策（隐私政策 / ToS / AI 内容声明）
  ↓
跑 audit:aeo runner（步骤 1-7）
  ↓
解析 evidence JSON
  ↓
分类 finding:
  - Blocker (§10)   → 阻断 release，路由到修复
  - Warn (§11)      → 进入 evidence，不阻断
  ↓
输出修复建议（按优先级 + 文件路径）
  ↓
（可选）跑 answer-engine-tests 跟踪改动效果（§7.7 按 platform 分别跑）
  ↓
归档 evidence，向上汇报到 discoverability-orchestrator
```

---

## 15. 常见误区 / 反模式

| ❌ 反模式 | ✅ 正确做法 |
|---|---|
| 把 "GEO（业界 Generative Engine Optimization）" 和 "Local SEO" 混用 | GEO 100% 指 AEO，归 web-aeo；Local / Maps / Google Business Profile 归 web-local-seo |
| 把内部 citability score 包装成"AEO 官方分数" | 明确标 internal heuristic, not official ranking factor，不向客户展示为官方 ranking |
| 把 llms.txt 当所有项目的 release blocker | 按 §6.2 分级，仅 docs/API-heavy 项目是 blocker |
| 把 robots.txt 当 access control | robots 是礼貌规约，本 skill 不做 access control；真正硬控制 → escalate `appsec-security-orchestrator` / `security-app-llm` |
| 不区分 search bot / training bot / user-initiated bot | 三种决策完全独立，必须分开列 |
| 让 AI 直接读网页"猜 AEO 优化" | 必须先跑 geo-seo-claude 脚本，AI 只解读 evidence |
| 用 FAQ 模板凑 SEO（没真问答内容） | 只在有真问答时使用；假 FAQ 拉低质量信号 |
| 复制示例 robots.txt 不改 | robots 必须按三种业务决策的组合定制 |
| vendor submodule 跟踪 main 分支 | 固定 commit，升级走 ADR |
| 把 brand entity 弱信号当作 release blocker | 弱信号只进 evidence；不阻断 |
| 用 visual `<div>` 模拟 table | 用真实 `<table>`，AI 抽取更准 |
| answer block 用 "this"、"该产品"指代 | 自包含写法，每个答案块单独读也成立 |
| JSON-LD 用 JS 注入 / 客户端 hydrate 后才出现 | server-rendered；AI crawler do NOT execute JavaScript |
| 把 vendor 0-100 GEO Score 当 release blocker 阈值 | GEO Score 是 diagnostic tool，不是 gate；blocker 走 §10 ID-based 列表，CI 不允许写 "GEO Score < N → 阻断" |
| 假设"在 Google AI Overviews 被引用 = ChatGPT 也会引用" | 研究显示只有 ~11% 域名被两边同时引用；按 §7.7 平台差异分别优化 |
| 把 Google-Extended 当作 Googlebot 的同义控制 | 两者完全独立；blocking Google-Extended ≠ blocking Googlebot |

---

## 16. 权威来源

**最关键 3 条**：

1. **OpenAI bots overview** — `https://platform.openai.com/docs/bots`
   区分 OAI-SearchBot / GPTBot / ChatGPT-User 的官方说明，是 §5 表格的基础。

2. **Anthropic crawler docs** — `https://support.anthropic.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler`
   区分 ClaudeBot / Claude-SearchBot / Claude-User / anthropic-ai 的官方说明。

3. **llmstxt.org** — llms.txt / llms-full.txt 社区 proposal 原始 spec，是 §6 的基础。

**学术 / 行业研究**：

- **Princeton GEO 论文** — `https://arxiv.org/abs/2311.09735`
  最早系统提出 Generative Engine Optimization 的学术论文，包含 134-167 words 段落长度等关键阈值依据。
- **Search Engine Land GEO 定义** — `https://searchengineland.com/what-is-generative-engine-optimization-geo-444418`
  业界对 GEO = Generative Engine Optimization 的官方定义引用源。
- **Wikipedia Generative Engine Optimization** — `https://en.wikipedia.org/wiki/Generative_engine_optimization`
  实体级澄清：GEO 业界 100% 指 Generative Engine Optimization，无 Geographic 消歧条目。
- **Ahrefs Dec 2025 brand-mention study** — 75K brands 样本，YouTube 0.737 / Domain Rating 0.266 correlation。
  Caveat: **single study, not peer-reviewed**；correlation ≠ causation。

**补充参考**：

- Google AI features doc — 关于 AI Overviews / AI Mode 不需要专用文件的说明
- RFC 9309 — robots.txt 标准（但**不是** access control）
- `zubair-trabzada/geo-seo-claude` README — vendor 脚本的接口约定
- Mintlify llms.txt docs — docs 平台采用 llms.txt 的实际案例

---

## 17. 与上下游 skill 的 handoff

### 上游 → 本 skill

- `discoverability-orchestrator` 路由进来，传入 project type / business policy / target URL list

### 本 skill → 邻居

| 场景 | 路由到 |
|---|---|
| 用户要的是 Google/Bing 标准 search | `web-seo` |
| 用户要的是 Google Business Profile / 本地商家 / Maps / NAP | `web-local-seo` |
| 用户要的是 App Store / Google Play | `app-aso` |
| 用户在问 robots / sitemap 的 standard search 部分 | `web-seo`（与本 skill 协调，避免重复） |
| 用户问 docs 的可访问性 / a11y 合规 | `qa-a11y-compliance` |
| 用户问 security / 任何 bot 的 auth 控制 | `appsec-security-orchestrator` |
| 用户问 LLM 应用的 prompt injection / agentic 安全 | `security-app-llm` |

### 本 skill → 下游

- evidence 归档到 `evidence/discoverability/<tag>/ai-search.json`（canonical channel key `ai-search`）
- 向上汇报到 `discoverability-orchestrator` 的 release readiness aggregator
- Blocker 触发时通知 `gsd-ship` / `gsd-verify-work` gate
- AI bot 实际硬控制（UA 校验 / rate-limit / auth wall）需求 → escalate `security-app-llm`

---

## 18. Skill 状态边界

- **可自动触发**：触发关键词命中（见 frontmatter description 中的完整 trigger 列表）
- **不会自动触发**：用户只说"做 SEO"且无 AI search 语境 → 路由到 web-seo，不抢
- **不抢工**：用户明确说 "Local" / "Maps" / "Google Business Profile" / "周边" / "实体店" → 路由 web-local-seo
- **GEO 自动归属**：业界 GEO 100% 指 Generative Engine Optimization → 本 skill 直接处理，不反问
- **不冒充**：本 skill **不**做任何 security 决策；遇到 auth / pentest / threat model 等关键词 → 立即路由 `appsec-security-orchestrator` / `security-app-llm`

---

## 19. L12 Harness Integration (v1.2+)

L12 harness v1.0 模式下，web-aeo 作为 **`ai-search` channel**（canonical key）的 auditor — **不是** `aeo`。Evidence 经 `python scripts/discoverability-sdk.py evidence.append <tag> ai-search <file>` 归一化。

**Channel key canonicalization**（harness §3.5.3）:
- Config 端：`channels.aeo`（历史兼容保留）
- Evidence / SDK / hook / dispatch：**`ai-search`**（canonical，**绝不**写 `aeo` 到 evidence path）
- Narrow skill 名：`web-aeo`（frozen，orchestrator §15.1）
- Evidence path：`evidence/discoverability/<tag>/ai-search.json`

**Script-first 强制 + AI ranking 永不官方化**：先跑 deterministic source（llms.txt parser / robots crawler-policy parser §5.4 / Schema.org FAQ-HowTo validator / 真实 AI engine query test via API §12 step 8）；全 `manual_ai_scan` → harness BLOCKED；反模式：让 AI 写"看起来合理的"citability / aeo / geo / brand_authority score（§7.3/§7.5/§8.3 均 internal_heuristic）。

**Blocker（仅 5 类强制阻断，与 §10 对齐）**:
1. `ai_crawler_policy_conflicts_with_business_policy`
2. `critical_answer_pages_have_no_extractable_text`
3. `generated_llms_txt_links_to_nonexistent_or_private_pages`
4. `llms_txt_contains_secrets_or_internal_endpoints` → **escalate AppSec / security-app-llm**
5. **`llms_txt_missing`**：仅 `project_type == api_with_public_docs` 时 blocker；其他 project_type 一律 warn_only（harness §4.2 强制，validator 自动 downgrade 违反者）

**永不 blocker**（harness §4.2 红线）：任何 `*_score` 启发式（citability / aeo / geo / brand_authority）— 仅 warn / info。

**Frozen names + 依赖**: 受保护 — skill `web-aeo`, channel `ai-search`, evidence path `evidence/discoverability/<tag>/ai-search.*`（详 orchestrator §15.1）。Contract 源：`~/.claude/templates/discoverability/harness-contract.md` §1 §3.5.3 §4.2。

---

## 20. Post-launch AI citation tracking（上线后 AI 引用追踪 — measurement-only）

> **加入 2026-06-15（CAPABILITY-UPGRADE L3）。** 这是 web-aeo 的 **post-launch measurement** 能力，与本 skill §5-§13 的 **pre-launch citability optimization** 严格区分（区别表见 §20.1）。citation 追踪回答的是"上线后 AI 答案引擎**实际上**有没有引用我"，不是"我的内容**形状**是否便于被引用"。

### 20.0 一句话定位

- **§5-§13（已有）= pre-launch**：审站点形状（crawler policy / 自包含 passage / llms.txt / schema），产 `ai-search.json` channel evidence，进 audit gate（§19 blocker/warn）。
- **§20（本节）= post-launch**：实查 AI 引擎，统计真实"品牌提及率 / 域名引用率 / 被谁挤掉"，产 `measurement.json`（measurement-only），**绝不进 gate**。

两条流并行、互不污染。**citability score（§7.3）≠ 实际 citation rate（§20）**：前者是站点写法的内部启发式，后者是真实查询 AI 引擎得到的观测值。绝不把两者混为一谈或互相代入。

### 20.1 pre-launch citability vs post-launch citation tracking（关键区别表）

| 维度 | §5-§13 pre-launch citability | §20 post-launch citation tracking |
|---|---|---|
| 问题 | 我的内容**形状**便于被 AI 引用吗？ | AI **实际上**引用我了吗？ |
| 输入 | 站点 HTML / robots / llms.txt / schema | 客户会问的真实 query + BYO AI provider key |
| 工具 | `geo-seo-claude` vendor 脚本（§9） | `geo citations` / `geo track`（geo-optimizer-skill，§20.3） |
| 数据来源 | 抓本站，deterministic parse | 查 AI 答案引擎，统计返回 source URLs |
| 产物 | `ai-search.json`（channel evidence） | `measurement.json`（measurement-only artifact） |
| 进 gate？ | ✅ 是（§19 blocker/warn，但 `*_score` 永不 blocker） | ❌ 否（与 L1 measurement 同流，`gate.check` 完全忽略） |
| 何时跑 | release 前（audit 阶段） | 上线后（持续监测 / 优化前后对比） |
| confidence | Level 1-4（脚本 deterministic） | 真实观测，但**依赖 BYO key + UI/API 稳定性**，且只有 Perplexity Sonar 回真实 source URL |

> **铁律**：本节产物是 **measurement-only**，与 L1 post-launch measurement（`measure.pull` / `measure.compare`，harness-contract §2.4）同属上线后只读数据流。它**不**触发 `state.json.gate_status`、**不**进 `gate-result.yaml`、**不**作为 release verdict。AI search 官方 ranking factor 从未公开 —— citation rate 是观测值，不是"AEO 官方分数"。

### 20.2 Script-first 红线（AI 永不编造引用数）

继承 L12 执行宪法（§4）+ harness §8.2：

1. **每个 citation 数字必须来自一次真实的 AI provider API 调用**，由 `geo citations` / `geo track` 发起。AI（本模型）**绝不**凭印象写"你大概被引用了 X%"。
2. **无 API key → `status: skipped`**，绝不编造。这与 L1 puller 的 `disc-measurement-puller` 行为一致（无凭证记 skipped，详 agent 定义）。
3. **provider 能力分级必须标注**（§20.4）：只有 **Perplexity Sonar** 把答案 ground 在 live web search 并返回**真实 source URL** → 能判定"域名被引用"。OpenAI / Anthropic / Groq 是 **parametric**，只反映"模型是否知道这个品牌"（参数化知识），**不能**证明 citation。evidence 里两类必须分开，不可混算成单一"AI 引用率"。
4. **BYO key 从环境变量取**（`PERPLEXITY_API_KEY` / `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` / `GROQ_API_KEY`），**绝不**写进仓库 / `.env` 提交 / chat / report。
5. AI 的角色只在**最后一步**：解读 `measurement.json` 里的真实 verdict（strong/cited/mentioned_only/invisible），关联到 §7 哪些 pre-launch 改动可能起效，给修复优先级 —— 不产生任何 citation 数字本身。

### 20.3 工具：geo-optimizer-skill（`geo citations` / `geo track`，BYO key）

> **参考 / 可吸收**：`Auriti-Labs/geo-optimizer-skill`（MIT）。本节文档化其 citation 追踪能力的**接入契约**；与 §9 的 `geo-seo-claude`（pre-launch citability scorer）是**两个不同 vendor、不同用途**，不要混淆。
> Staged：`CAPABILITY-UPGRADE-2026-06/staging/cloned-repos/geo-optimizer-skill/`。实施时按 §9.1 同样的 commit-pin + ADR 流程 vendor 进 `tools/vendor/`。

| 命令 | 用途 | 关键行为 |
|---|---|---|
| `geo citations --brand <B> --domain <D> [--topic <T>] [--query <Q>]...` | **one-shot** 引用检查：问 AI 引擎客户会问的问题，统计品牌是否被提及 + 域名是否在 source 里 | `--provider perplexity`（默认，若 `PERPLEXITY_API_KEY` 已设）→ 真实 source URL；parametric provider 只验品牌知识 |
| `geo track --url <U> [--history] [--report]` | **持续监测**：对 URL 跑完整 audit 并存本地时序快照，出 trend 报告 | 本地 history store（趋势对比）；`--history` 看历史，`--report` 出 HTML 趋势报告 |

**deterministic verdict**（`geo citations` 输出，4 档，基于真实 `domain_citation_rate` / `brand_mention_rate`，非 AI 主观）：

| Verdict | 触发条件 | 含义 |
|---|---|---|
| `strong` | `domain_citation_rate >= 0.5` | AI 在多数答案里把你的域名当 source 引用 |
| `cited` | `domain_citation_rate > 0`（但 < 0.5） | 出现在 source 里，但不稳定 |
| `mentioned_only` | `brand_mention_rate > 0` 且 `domain_citation_rate == 0` | AI 知道品牌（多半从第三方学的），但从不引用你的页面当 source |
| `invisible` | 两者皆 0 | 既不提品牌也不引用域名 |

> `mentioned_only` 的 actionable 解读：AI 是从第三方了解你的 —— 对应 §7 把**你自己的页面**做成可引用 source（statistics / quotable passage / llms.txt 深度）。`invisible` → 回 §5 crawler policy + §7.1 答案块基础先补齐。

### 20.4 provider 能力分级（evidence 必须标注，不可混算）

| Provider | env key | 能判定 citation（真实 source URL）？ | evidence 里的角色 |
|---|---|---|---|
| **Perplexity Sonar** | `PERPLEXITY_API_KEY` | ✅ 是（grounded in live web search） | **首选** — `domain_citation_rate` 来源 |
| OpenAI | `OPENAI_API_KEY` | ❌ 否（parametric） | 仅 `brand_mention_rate`（品牌知识）|
| Anthropic | `ANTHROPIC_API_KEY` | ❌ 否（parametric） | 仅 `brand_mention_rate` |
| Groq | `GROQ_API_KEY` | ❌ 否（parametric） | 仅 `brand_mention_rate` |

**铁律**：在 `measurement.json` 里，Perplexity 的 `domain_citation_rate` 与 parametric provider 的 `brand_mention_rate` **分字段存**，**不合并**成单一"AI 引用率"。报告里也分开陈述（"Perplexity 真实引用率 X%；OpenAI/Anthropic 品牌知晓 Y%（非 citation 证据）"）。

### 20.5 CLI 流程（写进 measurement 流，不进 channel evidence）

```bash
# 1. one-shot 真实 citation 检查（Perplexity = 真实 source URL；JSON 出到 raw/）
#    BYO key 从环境变量取，绝不写进仓库
geo citations --brand "Example Inc" --domain example.com \
  --topic "AEO audit tools" \
  --provider perplexity \
  --format json --output "evidence/discoverability/$TAG/raw/ai-citations.json"

# 2. （可选）持续监测 + 趋势（本地 history store）
geo track --url https://example.com --report \
  --output "evidence/discoverability/$TAG/raw/ai-citation-trend.html"

# 3. 归并进 measurement.json —— measurement-only，绝不进 gate
#    复用 L1 的 measure.pull（provider=aeo 路由到 ai-search channel 的 ai_citations 指标）
#    （aeo provider 已在 SDK：MEASUREMENT_PROVIDERS 含 aeo，PROVIDER_CHANNEL["aeo"]="ai-search"，见 §20.6）
python ~/.claude/skills/discoverability-orchestrator/scripts/discoverability-sdk.py \
  --project-root . measure.pull "$TAG" --provider aeo \
  "evidence/discoverability/$TAG/raw/ai-citations.json"

# 4. 优化前后对比（真实引用率 delta，纯算术，无 AI 解读）
python ~/.claude/skills/discoverability-orchestrator/scripts/discoverability-sdk.py \
  --project-root . measure.compare "$TAG" --baseline-tag "$BASELINE_TAG"
```

> **路径**：raw 产物落 `evidence/discoverability/<tag>/raw/`，归并进同 tag 的 `measurement.json`（harness-contract §2.4），**不**写 `ai-search.json`（那是 pre-launch channel evidence）。两个文件同住一个 `<tag>/` 目录但语义完全分开。

### 20.6 SDK 依赖说明（已落地 —— 2026-06-27 sync）

L1 已落地 `measure.pull` / `measure.compare`（harness-contract §2.4），且 schema 已含 `ai_citations` / `ai_referral_sessions` 指标键（见 SDK `MEASURE_METRICS`）。**`aeo` provider 现已在 SDK 中**（2026-06-27 补齐）：
- `MEASUREMENT_PROVIDERS` 含 `"aeo"`
- `PROVIDER_CHANNEL["aeo"] = "ai-search"`
- 因此 `measure.pull --provider aeo <raw/ai-citations.json>` 直接归一化进 `measurement.json` 的 ai-search channel（measurement-only，绝不进 gate）

归一化时把 `geo citations` 的 JSON（`domain_citation_rate` / `brand_mention_rate` / `verdict` / `top_cited_domains`）映射到 measurement schema 的 `ai_citations`；按 §20.4 provider 能力分级，parametric provider（OpenAI/Anthropic）的 mention rate **不**计入 citation。

**SDK 无关的独立运行**仍成立：`geo citations --format json` 直接产出 `raw/ai-citations.json` 供 AI 解读；SDK 只负责时序归并 + before/after delta。citation 追踪的**核心价值（真实 verdict + 真实 source URL）不依赖 SDK**。

### 20.7 measurement-only 边界（与 §19 audit gate 不重叠）

| 流 | 产物 | 进 gate？ | owner |
|---|---|---|---|
| pre-launch citability audit（§5-§13） | `ai-search.json` channel evidence | ✅ §19 blocker/warn（`*_score` 永不 blocker） | web-aeo（本 skill）|
| post-launch citation tracking（§20） | `measurement.json`（`measurement_only: true`） | ❌ 完全忽略 | web-aeo（本 skill）+ L1 measure.pull |

**反模式**：
- ❌ 把 `domain_citation_rate < N` 写进 release gate（citation 是观测值，AI ranking 未公开，永不 blocker —— 与 §19 / harness §4.2 `*_score` 红线同理）
- ❌ 用 parametric provider（OpenAI/Anthropic）的"品牌知晓"冒充"被引用证据"
- ❌ 无 key 时让 AI 编一个 citation rate（必须 `status: skipped`）
- ❌ 把 citation tracking 产物写进 `ai-search.json` 污染 pre-launch channel evidence

---

> 维护节奏：vendor commit 升级走 ADR；评分公式调整需要 release notes；新 AI bot 出现（如新厂商）需要在 §5.1 表格补行并更新业务决策建议；新 platform tactic（§7.7）随主流 AI 引擎产品变化季度复盘；citation provider 能力（§20.4）随 AI 引擎是否暴露 source URL 变化复盘（目前仅 Perplexity Sonar 回真实 URL）。
