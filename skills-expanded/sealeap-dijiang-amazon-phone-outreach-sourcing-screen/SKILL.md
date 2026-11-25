---
name: sealeap-dijiang-amazon-phone-outreach-sourcing-screen
description: "Prioritize phone contact over email-only outreach when developing new suppliers to get faster responses and build negotiating relationships, and screen candidate products against fulfillment-risk categories plus crowding signals before committing sourcing time or capital. Use for 供应商不回复邮件怎么办、要不要打电话谈供应商、哪些品类不要选、爆款选品会不会撞车. Do not use to fabricate a false identity when contacting suppliers beyond practicing your own pitch, and do not use to justify skipping supplier verification just because a call went well."
---

# Amazon 选品排雷与供应商电话开发

## 目标

Prioritize phone contact over email-only outreach when developing new suppliers to get faster responses and build negotiating relationships, and screen candidate products against fulfillment-risk categories plus crowding signals before committing sourcing time or capital.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源给出的打几通电话就能适应等次数是个人经验，实际所需练习量因人而异，以自己是否能顺畅完成一次真实报价沟通为准，不设固定次数。
- 评论少但搜索量大本身不是安全信号，需结合独立的第三方销量或搜索量数据与拥挤度信号交叉验证，不能仅凭单一维度下结论。
- 易碎、超重、季节性品类的风险等级会随包装工艺与目标市场配送条件变化，来源结论作为初筛方向，最终仍以自身报价与实测破损或退款率为准。

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

1. 把产品研究与供应商对接安排在不同的时间块甚至不同天，研究阶段进入无干扰环境完成候选清单，对接阶段再逐一跟进，避免两件事混着做导致都做得很浅。
2. 对已进入候选池的供应商，优先用电话而非纯邮件联系：电话响应更快，也更容易在后续建立长期合作关系，从而获得对方不对所有买家公开的优选货源或价格。
3. 如果对打电话有顾虑，先用不影响真实商务关系的方式做几次演练，把重点放在熟悉对方通常会问什么、怎么报价上，而不是无限期回避电话沟通。
4. 建立品类排雷清单，在选品早期就过滤掉三类高风险候选：易碎易损商品（运输破损引发的退款与差评会侵蚀账户表现）、超大或超重商品（履约与仓储成本会显著推高单位成本）、强季节性商品（旺季一过极易变成长期滞销库存）。
5. 对搜索量大、评论看起来不算多的爆款型候选，先假设已有其他卖家在跟进，用同类目的选品或预售追踪类信号交叉验证是否已被大量卖家同时寻源，而不是只看当前评论数就直接下单铺货。
6. 把排雷结果与电话沟通记录都留痕，作为后续复盘这类品类或这类供应商响应模式是否值得再投入的依据。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：补充候选品在选品或预售追踪类公开信号中的曝光情况，辅助判断是否已被大量卖家同时寻源。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 供应商电话开发脚本与跟进记录模板
- 品类排雷清单（易碎/超重/季节性）
- 候选品拥挤度交叉验证记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
