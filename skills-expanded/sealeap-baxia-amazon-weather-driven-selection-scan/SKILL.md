---
name: sealeap-baxia-amazon-weather-driven-selection-scan
description: "Screen a weather- or event-triggered demand spike for Amazon product opportunities by checking local supply-capacity gaps, installation or usage-friction barriers, and one's own supply-chain response speed before committing inventory. Use for 极端天气或突发事件带来的短期需求判断、季节性选品的供需缺口验证、追热点选品前的产能与合规评估. Do not use to commit large inventory purchases based solely on a short observation window without a clearance or markdown fallback plan."
---

# Amazon 极端天气选品排查

## 目标

Screen a weather- or event-triggered demand spike for Amazon product opportunities by checking local supply-capacity gaps, installation or usage-friction barriers, and one's own supply-chain response speed before committing inventory.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 供给缺口规模、产能数字与出口增速等是来源引用的公开统计口径，具体量级会随时间变化，判断时应查证当下最新数据而非沿用旧口径。
- 短期需求缺口能持续多久、是否会被本土产能追平，属于待验证假设，不能按单一季度的热销直接外推为长期机会。
- 涉及电器类等有安全认证要求的品类，供需缺口大不代表可以跳过认证流程，合规仍是前置条件。

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

1. 观察到极端天气或突发事件带来某类目搜索或销量异动时，先确认异动是否集中在少数相关品类而非全站噪音。
2. 核实当地本土产能与市场需求的量级关系，判断是结构性供给缺口还是短期物流延迟，两者的应对方式不同。
3. 对比自身候选产品与当地主流产品在安装门槛、使用便利性上的差异，判断是否存在真实的替代优势而不仅是价格更低。
4. 评估自身供应链从接单到出货的响应速度，能否在需求窗口关闭前完成备货与上架，响应不上的品类不追。
5. 小批量试单验证转化与复购，同时准备好需求回落后的降价清仓或转品预案，不因短期爆单一次性大量压货。
6. 跟进过程中持续检查目的地站点的合规与认证要求，例如涉及电器类目的安全认证，确认满足后再放量。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：补充目标市场的销量与出口等公开统计数据，用于验证供需缺口是否成立。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 需求异动品类清单
- 供需缺口与竞争优势评估
- 供应链响应速度核验记录
- 试单与回退预案
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
