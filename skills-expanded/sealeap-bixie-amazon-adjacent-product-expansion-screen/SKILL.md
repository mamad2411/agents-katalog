---
name: sealeap-bixie-amazon-adjacent-product-expansion-screen
description: "Expand a product line along a deepening (niche variant) or widening (complementary accessory) path using AI-assisted candidate generation validated against market size, competitive intensity, and review-mined pain points. Requires a profitability check before any candidate is accepted. Use for 老品增长见顶找新方向、细分赛道还是互补赛道选择、拓品候选筛选. Do not use to source a candidate before its profit model and IP screen pass, or as a substitute for formal patent clearance."
---

# Amazon 细分与互补赛道拓品筛选

## 目标

Expand a product line along a deepening (niche variant) or widening (complementary accessory) path using AI-assisted candidate generation validated against market size, competitive intensity, and review-mined pain points. Requires a profitability check before any candidate is accepted.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- AI 拓品工具生成的候选是启发式建议，搜索量、竞价强度等指标的准确性依赖所用数据源，落地前必须用当前市场数据复核而非直接采信。
- 差评痛点词频高不等于该痛点可被现有供应链低成本解决，痛点识别与产品设计可行性是两个独立的验证步骤。
- 利润模型必须覆盖头程、平台费、预估广告成本等全部环节，任何一项按经验值估算而未经验证的，都应在结论中标注为待验证假设。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- 目标 marketplace、类目、价格带、上架时间与运营模式
- 候选品与同购买意图可比样本的销量、评论、价格和上架时间
- 关键词需求、历史趋势、广告依赖、同款密度和品牌集中度
- 采购、头程、平台费、退货、仓储、交期和合规/IP 基础信息

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 从当前主力产品出发，用拓品工具批量生成细分方向（同一产品更细分的差异化版本）与互补方向（用户同期需要的关联品）候选列表。
2. 对每个候选先看市场基本面：搜索量量级、参与竞争的活跃 listing 数、新品占比、平均评论数，排除明显过热或过冷的方向。
3. 对通过基本面筛选的候选，拉出其现有竞品的差评做痛点词频统计，判断该方向是否存在可被产品设计解决的共性痛点。
4. 核算候选品类的推广竞争强度指标（如广告竞价水平、上首页所需的相对出单量），挑出竞争强度明显低于当前主力品的候选。
5. 对入围候选逐个跑单位经济模型（采购成本、头程、平台费、预估广告成本后的净利润），利润不达标的候选直接淘汰，不因方向看起来合理而保留。
6. 对最终候选评估与现有产品线的运营协同（能否共用供应链、广告流量、关联销售位），优先选择协同度高的方向落地。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：抓取候选品类的搜索量、广告竞价水平与竞品差评作为拓品机会筛选的代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 细分互补拓品候选清单
- 市场基本面筛选表
- 痛点词频统计
- 候选单位经济测算表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
