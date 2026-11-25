---
name: sealeap-taotie-amazon-third-party-tool-data-calibration
description: "Calibrate third-party keyword and sales-estimate tools against each other: run the same keyword and the same high-volume ASIN through several tools, compare search volume, estimated monthly sales and trend shape, cross-check trend direction with a public search-trend source, note marketplace coverage gaps, and choose a tool set by store count and job to be done rather than by brand reputation. Use for 哪个选品工具准、搜索量差很多、销量估算差异、工具支持哪些站点、要不要买某工具、多店铺用什么工具、评论分析和关键词监控哪家有. Do not use to declare any single tool's number as ground truth or to recommend a paid tool without stating the calibration evidence."
---

# Amazon 第三方选品工具数据交叉校准

## 目标

Calibrate third-party keyword and sales-estimate tools against each other: run the same keyword and the same high-volume ASIN through several tools, compare search volume, estimated monthly sales and trend shape, cross-check trend direction with a public search-trend source, note marketplace coverage gaps, and choose a tool set by store count and job to be done rather than by brand reputation.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源对具体工具「偏高/偏低/鸡肋」的评价是当时样本下的观察，工具算法持续更新，每次使用前重新跑基准对比。
- 「多数工具一致即可信」只是投票式近似，估算仍是 ESTIMATE；有平台一方数据时以一方为准。
- 来源的工具价格、团购与推荐链接不采纳；本 Skill 只描述工具类别与选择标准。
- 广告分时调价、跟卖监控等功能的效果未在来源中验证，列为功能清单项而非推荐做法。

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

1. 选一个需求明确的关键词与一个评论数很多的头部 ASIN 作为基准（样本越大估算越稳），在可用的每个工具里分别记录月搜索量、购买率、月销量估算与趋势图，并注明数据月份。
2. 比较搜索量：若某类工具系统性偏高或偏低（来源观察到不同来源的工具相差约一半量级），把偏差方向写进口径表；不同工具数字并列保留，用一方数据（品牌分析或商机探测器）或公开搜索趋势核对方向。
3. 比较销量估算：多数工具聚集在同一区间时采信该区间，离群的工具标为偏高/偏低；用类目 BSR 与该区间的关系做粗校，避免只信数字大的那家。
4. 核对趋势形状：把工具的历史曲线与公开搜索趋势对比，方向一致才作为季节性证据；幅度不一致属正常。
5. 列出每个工具的站点覆盖（尤其日本、中东等站）与关键功能（关键词收录检查、反查、排名监控、市场集中度分析、评论分析、库存与广告分时、多店汇总），按当前需求打勾。
6. 按店铺数量与岗位分工选组合：单店或少店以选品与关键词功能齐全、可开子账号的工具为主；多店铺时优先能汇总店铺经营与广告数据的工具；费用高但功能重叠的工具先试用再决定。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：对同一关键词与 ASIN 获取多来源搜索量、销量估算与趋势的第三方代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 基准关键词与 ASIN 对比表
- 工具口径偏差记录
- 趋势方向核对结果
- 站点覆盖与功能清单
- 工具组合选择建议
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
