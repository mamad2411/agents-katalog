---
name: industry-chain-research
description: 产业链研究：从宏观趋势拆解产业链、定位瓶颈环节、找到具体标的、交叉验证风险。核心理念——不问AI"买什么"，在结构化框架里让AI做产业链研究员。Use when user says 产业链分析, 拆产业链, 产业链研究, 瓶颈分析, 景气度投资, supply chain analysis, industry chain, "帮我拆一下XX产业链", "XX赛道有哪些机会", or wants to systematically research an industry theme for A-share investing.
---

# 产业链研究（Industry Chain Research）

从一个宏观趋势出发，沿产业链逐层下钻，定位瓶颈环节和具体标的，最终输出可执行的投资研究报告。

## 方法论来源

前 RISC-V Foundation 成员、AI 研究科学家的公开方法 + 王鹏景气度投资四阶段模型。

## 工作流

四个阶段，每阶段结束后与用户确认方向再继续。

### Phase 1 — 产业链地图（Chain Mapping）

用户给出宏观趋势/主题。AI 执行：

1. 用 `web-access` skill 搜索最新产业动态
2. 拆解完整产业链（上游原材料 → 中游制造 → 下游应用）
3. 标注每个环节供需状态：`充裕` / `紧平衡` / `瓶颈`
4. 输出 Mermaid 产业链地图

**交互点**：展示地图，问用户对哪个瓶颈环节最感兴趣。

### Phase 2 — 瓶颈下钻（Bottleneck Drill-down）

对用户选定的环节深入拆解：

1. 子产业链结构（核心零部件、工艺、材料）
2. 哪一段最难扩产？为什么？
3. 全球和 A 股供应商清单：公司名、代码、市值、市占率、核心客户
4. 是否已进入头部客户供应链？

**输出**：候选公司清单（聚焦 A 股上市公司）。

### Phase 3 — 交叉验证（Cross Validation）

对每个候选标的做五维验证（详见 [REFERENCE.md](REFERENCE.md)）：

1. **瓶颈持续性** — 技术替代风险？替代方案进展？
2. **竞争壁垒** — 壁垒来源？追赶者距离？
3. **收入兑现** — 订单→收入周期？新业务占比？
4. **风险因素** — 减持/增发？地缘？管理层？
5. **估值合理性** — 当前 price in 几年？下行空间？

**输出**：风险验证摘要，标注每个标的为 `强烈关注` / `值得跟踪` / `暂时回避`。

### Phase 4 — 市场阶段判断（Phase Assessment）

判断市场对该产业的认知阶段，给出对应的选股建议：

| 阶段 | 市场特征 | 策略 |
|------|---------|------|
| 1 分歧期 | 趋势初现，多空争论 | 买龙头，确定性优先 |
| 2 共识期 | 逻辑被验证，资金涌入 | 找供需错配最大的细分环节 |
| 3 压制期 | 预期透支，估值高位 | 只看二线弹性或新催化 |
| 4 泡沫期 | 全民讨论，故事代替逻辑 | 回避或只做交易 |

### 输出 — 研究报告

汇总 Phase 1-4 内容，生成结构化报告，用 `lark-doc` skill 发布到飞书云文档。

报告结构见 [REFERENCE.md](REFERENCE.md#报告模板)。

## 数据源

### wechat-article-feeds（微信公众号文章）

本地存储路径：`apps/天演资本/wechat-article-feeds/{公众号名称}/{YYYY-MM-DD}-{标题}.md`

订阅了 ~22 个财经类公众号（猫哥读研报、调研纪要更新、聪明投资者、搬砖小组 等），每篇文章含 YAML frontmatter（title, author, date, URL, summary）+ Markdown 正文。

**在产业链研究中的用法**：
- Phase 1（产业链地图）：搜索公众号文章中关于目标产业的分析，获取国内视角的产业链拆解和景气度判断
- Phase 2（瓶颈下钻）：搜索特定环节的深度研报、调研纪要，获取一手的供需数据和公司调研信息
- Phase 3（交叉验证）：用不同公众号的分析交叉印证，避免单一信源偏见

**搜索方式**：直接用 Grep 工具在 `apps/天演资本/wechat-article-feeds/` 目录下搜索关键词。

### 东方财富研报中心（券商研报）

通过 `web-access` skill 访问东方财富研报中心，获取券商研报原文和摘要。

**搜索入口**：`https://reportapi.eastmoney.com/report/list?industryCode=&pageSize=50&industry=关键词&beginTime=起始日期&endTime=结束日期`

**在产业链研究中的用法**：
- Phase 1（产业链地图）：搜索行业研报，获取券商对产业链的专业拆解和景气度评级
- Phase 2（瓶颈下钻）：搜索细分环节的深度研报，获取供需数据、产能统计、公司覆盖
- Phase 3（交叉验证）：查看目标公司的最新研报，获取盈利预测、目标价、风险提示

**搜索策略**：先用行业关键词搜索（如"光模块"、"HBM"），再按发布时间排序取最新的 3-5 篇。

### 其他数据源

- `web-access` skill — 联网搜索产业动态、英文资料、其他信息源
- `sepa.db` 本地数据库 — A 股历史行情、估值、财务指标（用于 Phase 3 估值验证）
- `tushare-data` skill — 补充实时财务和市场数据

## 与 company-analyzer 的关系

本 skill 聚焦产业链全景，定位"哪些公司值得研究"。找到标的后，可用 `company-analyzer` skill 对单个公司做深度分析。两者互补。
