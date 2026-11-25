---
name: company-analyzer
description: Analyze a company through three layers — story, logic, judgment — and deliver a narrative-driven report with a clear take. Use whenever the user asks to research, analyze, or deeply understand a specific company, whether the motivation is investing, career, competitive intel, partnership, or curiosity. Trigger even when the user says "研究 XX 公司", "深度分析 XX", "带我看懂 XX 这家公司", or names a company alongside investment/career/competition context without explicitly saying "analyze". NOT for quick fact lookup, real-time stock quotes, or broad multi-company surveys.
---

# Company Analyzer

Produces a company analysis organized as **Story × Logic × Judgment** — a deliberate departure from SWOT-style templated reports. The three layers map to how humans actually understand a business: the narrative arc makes it memorable, the economic logic makes it rigorous, and the forced judgment makes it useful.

The benchmark for style and depth is 《晚点 LatePost》-class industry writing (see `references/style-benchmark.md` for an annotated example). If the output reads like a translated McKinsey slide with English jargon sprinkled in, it failed — even if all the facts are correct.

## When to use

- "分析一下 XX 公司" / "深度研究 XX" / "我想搞懂 XX 这家公司"
- Weighing an investment, job, or partnership with a specific company
- Wants to understand the company *as a thesis*, not a data dump

## When NOT to use

- Quick factual lookup (founding year, headcount) — answer directly
- Real-time prices, intraday earnings reactions — route to a market data tool
- Comparing ≥5 companies at once — depth-first, not breadth-first
- Pure concepts/technologies (Transformer, RAG) — not a company

## Writing style (非协商)

This is the hardest part to get right and the easiest to fail. Before writing any section, hold the following rules in memory.

1. **母语化中文**，不要自造中英夹杂术语。"护城河"说护城河，不要说 "moat"；"资本配置"说资本配置，不要说 "capital allocation"；"工艺 know-how" 最多保留 "know-how" 这样已被中文业界吸收的词。行业通用英文缩写（CAGR、PE、TIER 1、ROE、FCF）可保留；自造英译概念（process power、moat type、unit economics 当小标题用）不要。
2. **小标题必须是带动词的一句完整论断**，不是名词短语。
   - 好：「过往的路径依赖，让公司错失了新能源车的增长红利」
   - 差：「历史沿革」「业务模式」「护城河分析」
3. **每段话都要自我解释因果**。不写"它有规模优势"，写"它在 X 细分市场占 Y% 份额，这让它能摊薄 Z 这条固定成本——但同一份额在 W 市场并不成立"。
4. **因果链至少 3 层深**。事件 → 为什么发生 → 业务影响 → 投资含义。停在任何中间层都是懒惰。
5. **段间用中文连接词过渡**，不要靠 markdown 视觉结构硬拼（无 emoji、无表格作为论证主体——表格只用于展示分段数字）。
6. **数字要带解释**。不要"营收 147 亿元，同比 +4.83%"，要"营收 147 亿元，同比只 +4.83%，而扣非反而 -4.39%——意味着这 4.83% 增速里一多半是卖资产，不是主业。"

## Workflow

### Phase 0 — Scope alignment (可跳过)

Default: use `AskUserQuestion` to confirm three things before any web search:

1. **Target disambiguation** — "Cursor" = 编辑器 (Anysphere) 还是概念？
2. **Purpose** — 投资 / 求职 / 竞争情报 / 好奇. 决定哪一层权重最重.
3. **Depth** — quick / standard / deep (见下方 length quota).

**跳过条件**: 用户在请求里已经明确指定了公司 + 目的 + 深度（或者深度从上下文清楚），直接进入 Phase 1，不要为了"按流程"打断用户. 但如果任一维度歧义（公司名有两个候选 / 没说目的 / 没说深度），必须问.

### Phase 1 — Scenario branching

按公司生命周期选 ONE. 下列权重是**叙事重心**，不是字数机械切分.

- **A — Early-stage (<3y)**: Story 60% / Logic 25% / Judgment 15%. 创始人 DNA 主导；护城河是假设.
- **B — Growth (3–10y)**: Story 40% / Logic 40% / Judgment 20%. 商业模式走完第一个周期.
- **C — Mature (10y+, private)**: Story 30% / Logic 45% / Judgment 25%. 数字和结构位置主导.
- **D — Public company**: 同 C，额外叠加财务层 — 见 `references/financial-analysis.md`.

### Phase 2 — Three-layer parallel execution

派 3 个子 agent 并行. 每个 agent 负责一层，收到 prompt 后要做的第一件事是**独立核实父 agent 传过来的初始事实**——创始人履历、年份、关键数字这些，如果和公开资料冲突，以独立核实为准，不要照搬父 agent 的叙述。父 agent 也会出错。

- **Sub-agent 1 — Story layer.** Read `references/story-patterns.md`.
  - 产出：创始人的来路 + 关键决策（不是流水账）. 为 Mature / Public 公司，Story 可以压缩为"三到四个决定公司命运的分叉"；不需要给每家公司做电影式开场. 
  - 对早期公司 (A/B) 可以有场景化细节；对 Mature / Public 公司以**战略事件**为主（并购、合资股权比例、高管变动、重大监管事件、关键客户签入或丢失）.
- **Sub-agent 2 — Logic layer.** Read `references/business-logic.md`、`references/moat-types.md`、和 `references/industry-structure.md`.
  - **必须先做"行业结构分析"再讲公司**. 行业层次是什么（细分应用市场各占多少、集中度如何、技术壁垒高低）. 公司在这张地图上的坐标是什么. 如果上来就写"公司业务模式如何……"，是失败.
  - 产出：行业结构 → 公司定位 → 收入/成本机制 → 护城河 → **配对比较（强制）**.
  - **配对比较是必做项，不是可选**. 选 1 个最能说明问题的对手做深度对比（该对手做对了什么、该公司做错了什么，或反之）. 如果找不到合适对手，要**命名理由**（为什么这是一个孤立市场），不能跳过.
- **Sub-agent 3 — Judgment layer.** Read `references/anti-patterns.md` first. 在 Story + Logic 落地后运行.
  - 产出：公司现在在生命曲线的哪里、未来 3–5 年的赌注（2–3 个可证伪的杠杆）、**命名立场**（"我会"或"我不会"或"我会等+触发条件"——骑墙算失败）、5 个监控指标.

### Phase 3 — Synthesis

主 agent 把三层编织成一篇文章，不是三段拼接. 语言风格参照 `references/style-benchmark.md` 的《晚点》示例：平白中文、整句论断作标题、段间用"但问题在于"/"对比而言"/"所以"做过渡. 不保留英文术语标签作为 section header（不要出现 "### Moat Analysis" 这种东西）.

## Length quota

量化配额（中文字符数），低于下限视为研究深度不够，高于上限视为灌水.

- **Quick**: 2000–3500 字
- **Standard**: 7000–10000 字
- **Deep**: 15000–22000 字

（注：这是 synthesis 后**最终产出**字数，不是三层草稿相加；单层草稿会在合成时被压缩和穿插.）

## Anti-patterns (必避)

详见 `references/anti-patterns.md`. 短清单：

1. **流水账年表** — "2015 年 A，2016 年 B……"
2. **咨询八股** — 赋能 / 抓手 / 闭环 / 打造 / 生态位；英文 synergize / leverage / holistic / empower.
3. **自造中英夹杂术语** — "moat"、"process power"、"capital allocation"、"unit economics"、"go-to-market"、"stickiness" 作为中文段落里的概念词出现.
4. **模板骨架** — SWOT、波特五力、PEST 作为 section header.
5. **财报文字版** — 把 10-K 数字粘贴成段落而不解读.
6. **骑墙立场** — "既有机遇也有挑战".
7. **综上所述 / In conclusion** 总结.
8. **名词性标题** — 章节标题是"业务模式"而不是"业务模式决定它只能做中等生意"这种带论断的句子.

## Progressive disclosure (参考文件)

- `references/style-benchmark.md` — 《晚点 LatePost》风格标注示例（v2 新增）
- `references/industry-structure.md` — 如何做行业结构分析（v2 新增）
- `references/story-patterns.md` — 五种叙事形态（成熟公司可简化使用）
- `references/business-logic.md` — 收入机制 + 商业性质 + 管理层分析
- `references/moat-types.md` — 7 类护城河 + 监管/IP/资本（用作思考工具，输出时用中文自然语言）
- `references/financial-analysis.md` — 上市公司财务 4 步读法
- `references/anti-patterns.md` — 详细负面清单 + 重写对照
- `templates/report-template.md` — 建议骨架（标题按一句话论断写）
