---
name: ai-seo
description: |
  AI 搜索优化（GEO）工具。帮网站在 ChatGPT、Perplexity、Claude、Google AI Overviews 等 AI 搜索引擎里被引用和推荐。
  覆盖：AI 可引用性评分、AI 爬虫检测、llms.txt 生成、品牌提及扫描、结构化数据、内容质量、技术SEO、完整审计报告。
  触发词：/ai-seo、AI搜索优化、GEO、网站审计、AI可见性、llms.txt、被AI引用、AI搜索流量
  Trigger: /ai-seo, GEO audit, AI search optimization, citability, llms.txt, AI visibility
---

# AI-SEO：让你的网站被 AI 搜索引用

> 传统 SEO 优化 Google 排名。AI-SEO 优化 ChatGPT/Perplexity/Claude 的引用。

---

## 命令速查

| 命令 | 功能 |
|------|------|
| `/ai-seo audit <url>` | 完整 AI-SEO 审计（评分 + 行动清单） |
| `/ai-seo quick <url>` | 60秒快速快照 |
| `/ai-seo citability <url>` | AI 可引用性评分 |
| `/ai-seo crawlers <url>` | 检查 AI 爬虫是否能访问 |
| `/ai-seo llmstxt <url>` | 分析或生成 llms.txt |
| `/ai-seo brands <url>` | 品牌提及扫描 |
| `/ai-seo schema <url>` | 结构化数据检测与生成 |
| `/ai-seo content <url>` | 内容质量 + E-E-A-T 评估 |
| `/ai-seo technical <url>` | 技术 SEO 审计 |
| `/ai-seo report <url>` | 生成完整报告（Markdown） |

---

## 核心概念

**GEO（生成引擎优化）**：让 AI 搜索引擎在回答用户问题时，主动引用你的内容。

**为什么现在必须做：**
- AI 引用流量转化率是普通搜索流量的 **4.4倍**
- 品牌在 AI 引用中的权重是反链的 **3倍**
- 2028年 Google 搜索流量预计下降 **50%**（Gartner）
- 只有 **23%** 的营销人员在做 GEO

---

## 完整审计流程（/ai-seo audit）

### Phase 1：站点发现
1. 抓取首页 HTML
2. 识别网站类型（SaaS / 本地服务 / 电商 / 内容站 / 机构 / 其他）
3. 从 sitemap.xml 提取关键页面（最多50页）

### Phase 2：五维并行分析

读取 `references/` 下对应模块，对以下5个维度评分：

| 维度 | 权重 | 评分要点 |
|------|------|---------|
| AI 可引用性 & 可见性 | 25% | 内容段落质量、AI爬虫访问、llms.txt |
| 品牌权威信号 | 20% | Reddit/YouTube/Wikipedia/LinkedIn 提及 |
| 内容质量 & E-E-A-T | 20% | 专业度、原创数据、作者权威 |
| 技术基础 | 15% | SSR渲染、Core Web Vitals、移动端 |
| 结构化数据 | 10% | JSON-LD 完整性、Schema 类型匹配 |
| 平台优化 | 10% | ChatGPT / Perplexity / Google AIO 各自适配 |

### Phase 3：综合评分 + 行动清单
- 计算综合 AI-SEO 分数（0-100）
- 按优先级输出行动清单（快速见效 / 中期 / 战略）
- 保存到 `AI-SEO-REPORT.md`

---

## 可引用性标准（AI Citability）

AI 倾向引用的内容具备以下特征（读取 `references/citability.md` 详细标准）：

- **段落长度**：134-167字最优，自成一体
- **事实密度**：含数据、来源、具体例子
- **问答结构**：直接回答"什么是X""如何做X"
- **权威信号**：有作者署名、发布日期、引用来源

---

## 输出文件

| 命令 | 输出 |
|------|------|
| `/ai-seo audit` | `AI-SEO-AUDIT-REPORT.md` |
| `/ai-seo citability` | `AI-SEO-CITABILITY.md` |
| `/ai-seo crawlers` | `AI-SEO-CRAWLERS.md` |
| `/ai-seo llmstxt` | `llms.txt`（可直接部署） |
| `/ai-seo brands` | `AI-SEO-BRANDS.md` |
| `/ai-seo schema` | `AI-SEO-SCHEMA.md` + JSON-LD 代码 |
| `/ai-seo report` | `AI-SEO-CLIENT-REPORT.md` |
| `/ai-seo quick` | 直接输出，不存文件 |

---

## 参考文档

- `references/citability.md` — AI 可引用性详细评分标准
- `references/crawlers.md` — 14+ AI 爬虫列表及 robots.txt 配置
- `references/schema-templates.md` — JSON-LD 模板（6种网站类型）
- `references/platform-rules.md` — ChatGPT / Perplexity / Google AIO 各平台优化规则
