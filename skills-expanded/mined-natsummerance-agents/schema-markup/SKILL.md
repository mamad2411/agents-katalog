---
name: schema-markup
description: |
  结构化数据专项：判定页面内容类型 → 生成 JSON-LD Schema.org 标记（Organization/Article/Product/LocalBusiness/Event/JobPosting/QAPage 等）→ 用 Rich Results Test 与 Schema Markup Validator 双验证 → 交付部署代码与修复清单。当用户要"加结构化数据""写 JSON-LD""做 rich results 富摘要"或验证现有 schema 报错时触发。不适用于：整站技术 SEO 体检（转 seo-audit）、AI 引擎内容可引用性优化（转 geo-search-optimize）、博客文章写作生产（转 blog-writing-contract）。
source_project: AgriciDaniel/claude-seo
tags: [schema, json-ld, structured-data, rich-results, schemaorg]
---

# schema-markup

## R · 上游引用

> "JSON-LD is the preferred format (Google's stated preference)."
> "/seo schema <url> — Detect, validate, and generate Schema.org markup."
> "FAQPage: Google stopped showing FAQ rich results for all sites on May 7, 2026; it has no Google rich-result benefit. ... Deprecated and never recommended: HowTo (rich results removed September 2023), SpecialAnnouncement (July 2025), ClaimReview ... (all retired June 2025)."
> "**Critical Issue:** The `founder` property only includes Daniel Agrici. Benjamin Samar (Co-Founder & Technical Director) is displayed on the page but absent from the schema. This creates a content-schema mismatch that can confuse search engines."

来源：AgriciDaniel/claude-seo 仓库 `README.md`（https://raw.githubusercontent.com/AgriciDaniel/claude-seo/main/README.md ，fetch 于 2026-08-26；主 URL 直取成功，无需启用 HEAD 备选；本地 upstream 目录为空壳）

## I · 方法论骨架

1. **内容类型判定**：先弄清页面目的（商品页？文章？本地商家主页？活动页？），类型决定 Schema.org 类型；不明确就问清再动手。
2. **格式选型**：一律首选 JSON-LD（Google 官方偏好），独立 `<script type="application/ld+json">` 块，不动可见内容。
3. **属性完备性**：`@context` + `@type` + `@id`（支持跨块交叉引用）+ sameAs 社交档案；必填属性缺失即失败，推荐属性（如 LocalBusiness 的 geo 坐标、营业时间）逐条补齐。
4. **时效红线**：弃用类型不出货——HowTo、SpecialAnnouncement、ClaimReview 等 2023–2026 年间已退役；FAQPage 自 2026-05-07 起在 Google 无富结果收益，仅在有非 Google 或内部语义需求时保留。
5. **双验证器**：Rich Results Test（富结果资格）+ Schema Markup Validator（语法与语义），双过才算完成。
6. **内容-标记一致性**：标记必须与页面可见内容对齐——页面写了两位联合创始人而 schema 只列一位，即判 critical。

## A1 · 案例

- **输入**："帮我的 SaaS 关于页加结构化标记，Rich Results Test 老报警告。"
- **做法**：判定页面适用 Organization + WebSite + SoftwareApplication 三块→检查现有 JSON-LD 发现 founder 属性只填一位创始人而页面展示两位、foundingDate 只有年份→按 ISO 8601 补齐并新增第二位 founder。
- **结果**：产出三段可直接粘贴的 JSON-LD，双验证器零错误；报告以 B+ 定级并注明"solid foundation, actionable gaps"，遗留建议 areaServed 改用 GeoShape 提升语义精度。

## A2 · 触发判断 ★

适用情境：
1. 用户要求为某页面生成、补全或修复 JSON-LD / Schema.org 标记。
2. 用户提到富媒体摘要（rich results / rich snippets）没显示或测试工具报错。
3. 用户不确定自己的内容该用什么 Schema 类型，需要类型判定与选型。

语言信号（≥3 条）：
- "帮我加/写一段 JSON-LD 结构化数据"
- "Product / Article / FAQ 的 schema 怎么配"
- "Rich Results Test 报错了帮我看看"
- "为什么我们的富媒体摘要（星级/价格）不显示"

与兄弟 skill 的区分：schema-markup 只管**结构化数据这一层**——类型判定、JSON-LD 生成、双验证、弃用类型规避；整站横向体检（含"顺带看看 schema 有没有"的模糊请求）归 `seo-audit`，由其审计发现缺口后转介本 skill；AI 搜索可引用性与品牌信号归 `geo-search-optimize`（结构化数据仅是其 10% 权重子项）；文章写作流程归 `blog-writing-contract`。反向诱饵：只要请求落在"某个具体标记怎么写/为什么报错"，即使出现在审计对话里也归本 skill。

## E · 执行流程

1. **判定内容类型** — 完成标准: 输出该页的 Schema 类型选择及理由；页面目的不明时已向用户提问确认而非猜测。
2. **检测现状** — 完成标准: 列出页面现有 JSON-LD/Microdata/RDFa 块数与类型清单（无则记 0），并标注检测到的弃用类型。
3. **生成或修复 JSON-LD** — 完成标准: 产出含 @context/@type/@id/sameAs 的完整片段，必填属性齐全，且每个属性值能在页面可见内容中找到对应。
4. **核对时效红线** — 完成标准: 产物中不含 HowTo/SpecialAnnouncement/ClaimReview 等退役类型；FAQPage 仅在用户明确接受"Google 无富结果收益"后保留。
5. **双验证器校验** — 完成标准: Rich Results Test 与 Schema Markup Validator 双双通过，或每条报错附定位到行的修复方案。
6. **交付部署说明** — 完成标准: 给出粘贴位置（head/body）、部署后复验步骤和预期富结果形态；不承诺任何名次或流量变化。

## B · 边界与红线

不适用（≥2）：
- 整站技术 SEO 审计、反链与体量画像 → 转 `seo-audit`。
- AI 搜索引擎的可引用性改造与品牌提及建设 → 转 `geo-search-optimize`。
- 博客文章从选题到质量门交付的生产 → 转 `blog-writing-contract`。

局限：
- 结构化数据只影响**资格与呈现**（能否出富结果），不直接决定排名；向用户表述时不得把加标记说成提权手段。

红线：
- **SEO 无法保证排名结果**：加 schema 不承诺任何名次提升、收录时限或富结果必然展示——展示与否由搜索引擎决定。
- **拒绝黑帽手法**：拒绝用 schema 造假——标记与页面可见内容不符（虚假评分、虚构评论、隐藏实体）、关键词堆砌、隐藏文字、链接农场一律拒绝并解释风险（手动处罚/富结果资格取消）。
- 收到"能不能给我刷到第一"类要求：拒绝并解释排名由算法与竞争决定，schema 只是让搜索引擎更准确地理解页面，不是操纵排名的开关；随后回到类型判定与合规生成的正轨。

## 相关 skills

- `seo-audit` — 整站体检发现 schema 缺口后的转介入口；本 skill 的上游漏斗。
- `geo-search-optimize` — 把结构化数据当作 AI 可见性六类权重之一做全局权衡的地方。
- `blog-writing-contract` — 文章生产管线中的 schema 注入步骤调用本 skill 的生成规范。

---

## 审计信息

- V1✓ 来源可溯：R 段引用 fetch 所得上游 README ≤100 词，标注 raw URL
- V2✓ 四角分工：结构化数据角，A2 与 seo-audit / geo-search-optimize / blog-writing-contract 互设诱饵并写明区分
- V3✓ 红线齐备：不承诺排名 + 拒绝 schema 造假与黑帽 + "保第一"拒绝话术入 B 段与 edge_case
- 蒸馏时间：2026-08-25（2026-08-26 复核：R 段四条引文与上游 main 分支逐字比对通过）
- 来源：fetch — https://raw.githubusercontent.com/AgriciDaniel/claude-seo/main/README.md （主 URL 成功，未启用 HEAD 备选；本地 upstream 目录为空壳）
