---
name: geo-search-optimize
description: |
  GEO 生成引擎优化：让网站内容更容易被 ChatGPT / Claude / Perplexity / Gemini / Google AI Overviews 等 AI 搜索引擎理解、引用和推荐。覆盖 AI 可引用性评分（134–167 词自包含段落）、AI 爬虫 robots.txt 可达性、跨平台品牌提及信号、平台差异化策略与综合 GEO 评分。当用户问"怎么让 AI 引用我们""ChatGPT/Perplexity 里搜不到我们"时触发。不适用于：传统 Google 整站技术体检（转 seo-audit）、单页 JSON-LD 标记生成（转 schema-markup）、博客文章写作生产（转 blog-writing-contract）。
source_project: zubair-trabzada/geo-seo-claude
tags: [geo, ai-search, citability, brand-mentions, llm-visibility]
---

# geo-search-optimize

## R · 上游引用

> "GEO-first, SEO-supported. Optimize websites for AI-powered search engines (ChatGPT, Claude, Perplexity, Gemini, Google AI Overviews) while maintaining traditional SEO foundations."
> "Citability Scoring: Analyzes content blocks for AI citation readiness. Optimal AI-cited passages are 134-167 words, self-contained, fact-rich, and directly answer questions."
> "Brand mentions correlate 3x more strongly with AI visibility than backlinks."
> 评分权重："AI Citability & Visibility 25% · Brand Authority Signals 20% · Content Quality & E-E-A-T 20% · Technical Foundations 15% · Structured Data 10% · Platform Optimization 10%"

来源：zubair-trabzada/geo-seo-claude 仓库 `README.md`（main 分支，2026-08-25 初蒸馏、2026-08-26 复核逐条引文；raw 直连失败后经 github.com 仓库页核对全文；本地 clone 为浅克隆失败残留空壳，不可用）

## I · 方法论骨架

1. **可引用性优先**：把内容改造成"可直接被摘引"的段落——134–167 词、自包含、事实密集、直接回答一个问题；问题式标题层级。
2. **AI 爬虫可达性**：检查 robots.txt 对 GPTBot / ClaudeBot / PerplexityBot 等 14+ 家 AI 爬虫的放行状态，给出逐家 allow/block 建议。
3. **品牌提及信号**：品牌在 Wikipedia / Reddit / YouTube / LinkedIn 等 AI 高频引用平台的在场度，比外链对 AI 可见性的相关性更强。
4. **平台差异策略**：同一查询仅约 11% 域名被 ChatGPT 与 Google AIO 同时引用——按目标引擎分别校准，不做一刀切。
5. **综合评分收敛**：六类加权合成 0–100 GEO Score，输出带 quick wins 的优先级行动清单。
6. **传统地基兜底**：GEO 不替代 SEO——索引资格仍是入场券，技术面问题指回 seo-audit。

## A1 · 案例

- **输入**："我们在 Perplexity 上完全搜不到，但 Google 排名还行，帮我看看为什么。"
- **做法**：跑可引用性评分→发现博客段落平均超 400 词且结论埋在段尾；查 robots.txt 发现 PerplexityBot 被封；扫品牌提及发现 Reddit/知乎零在场。
- **结果**：三步改造——核心回答前置成 150 词自包含块、robots.txt 放行 PerplexityBot、制定两处高权重社区的品牌答题计划；复评 GEO Score 由 41 升至 68，附各引擎复查方法。

## A2 · 触发判断 ★

适用情境：
1. 用户想让自己或客户的内容出现在 ChatGPT / Perplexity / Gemini / AI Overviews 的回答里。
2. 用户问"GEO / AEO / AI 搜索优化怎么做"、要给内容打可引用性分。
3. 用户怀疑 AI 爬虫被 robots.txt 挡住，或想知道品牌在 AI 引用平台上的在场度。

语言信号（≥3 条）：
- "怎么让 ChatGPT / Perplexity 引用我们的内容"
- "在 AI 搜索里搜不到我们公司"
- "帮我做一下 GEO / AI 搜索优化"
- "检查一下 GPTBot 能不能爬我的站"

与兄弟 skill 的区分：geo-search-optimize 管 **AI 引擎的内容可见性层**——可引用性、爬虫准入、品牌信号；传统 Google 整站技术体检归 `seo-audit`（若用户只说"全面查站"，即使提到 AI 也先走 seo-audit，由其转介）；页面 JSON-LD 结构化标记的具体写法归 `schema-markup`（本 skill 只把它当 10% 权重的子项调用）；从零写文章并过质量门归 `blog-writing-contract`。

## E · 执行流程

1. **锁定目标引擎与查询集** — 完成标准: 列出用户关心的 AI 引擎清单和 3~5 条目标业务查询，缺一退回补问。
2. **可引用性评分** — 完成标准: 输出每篇目标页的分值，并标出至少一处不符合"134–167 词自包含回答块"的具体段落位置。
3. **爬虫准入核查** — 完成标准: 给出 14+ 家 AI 爬虫的 allow/block 现状表，每条封锁项附修改建议原文。
4. **品牌提及扫描** — 完成标准: 报告 Wikipedia / Reddit / YouTube / LinkedIn 等平台的在场/缺席清单，缺席项附可执行的在场建设动作。
5. **平台差异校准** — 完成标准: 对每个目标引擎至少给出一条差异化建议，并说明为何该建议不适用于其他引擎。
6. **合成分与行动清单** — 完成标准: 按 25/20/20/15/10/10 六类权重算出 0–100 分，quick wins 每条含预期影响面与验证方式。
7. **边界移交** — 完成标准: 若发现纯技术 SEO 缺陷或 schema 缺失，已分别写入转介 seo-audit / schema-markup 的具体条目而非混在本报告里。

## B · 边界与红线

不适用（≥2）：
- 传统搜索引擎的整站技术体检、反链画像 → 转 `seo-audit`。
- 单页 Schema.org / JSON-LD 标记的检测与生成 → 转 `schema-markup`。
- 博客文章从选题到过门交付的生产流程 → 转 `blog-writing-contract`。

局限：
- llms.txt 的实际引用效果存争议：上游 geo-seo-claude 提供 llms.txt 生成，但据 AgriciDaniel/claude-seo 的原始证据核查，Google 立场是搜索忽略 llms.txt 且它并非当前的引用杠杆——涉及 llms.txt 的建议必须标注为实验性。
- AI 引擎抓取与引用机制不透明且变化快，任何评分都是启发式快照，不是引擎内部真相。

红线：
- **无法保证被 AI 引用或推荐**：不得承诺"让 ChatGPT 必然推荐你家"，只能改善可测量的信号。
- **拒绝黑帽式操纵**：关键词堆砌、隐藏文字、链接农场、批量伪造品牌提及/评论等一律拒绝并解释平台惩罚风险。
- 收到"能不能给我刷到第一/让 AI 必须推荐我"类要求：拒绝并解释——AI 引擎按自身检索与排序逻辑动态选择引用源，无人能保证结果；声称能保证的服务要么违规要么欺骗；随后转向可验证的可引用性与信号建设。

## 相关 skills

- `seo-audit` — 传统整站体检入口；GEO 假设索引资格成立，地基问题先走这里。
- `schema-markup` — 结构化数据是 GEO 六类权重之一，专项生成与验证在此执行。
- `blog-writing-contract` — 需按可引用性标准生产新文章时的交付门禁。

---

## 审计信息

- V1✓ 来源可溯：R 段引用上游 README ≤100 词，标注实际获取路径与本地 clone 失效事实
- V2✓ 四角分工：GEO/AI 搜索角，A2 与 seo-audit / schema-markup / blog-writing-contract 互设诱饵并写明区分
- V3✓ 红线齐备：不承诺 AI 推荐 + 黑帽排除 + "保第一"拒绝话术入 B 段与 edge_case
- 蒸馏时间：2026-08-25（2026-08-26 复核：R 段引文与上游仓库页全文逐条比对通过）
- 来源：fetch — github.com/zubair-trabzada/geo-seo-claude main 分支 `README.md`（raw main/HEAD 直连传输失败，改走仓库页渲染全文核对；本地 upstream 目录为浅克隆失败残留，无工作区文件）
