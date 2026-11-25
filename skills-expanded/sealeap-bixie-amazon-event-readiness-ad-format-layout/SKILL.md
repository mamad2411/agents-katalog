---
name: sealeap-bixie-amazon-event-readiness-ad-format-layout
description: "Sequence pre-event readiness (listing assets, review count, inbound inventory) against a promotion timeline, then lay out automatic, manual, product-targeting, brand, and display ad structures suited to promotion-period traffic and conversion patterns. Keeps negative-keyword and bid-ceiling guardrails explicit for the event window. Use for 大促前多久开始准备、Listing与库存是否达标、大促期广告结构怎么搭. Do not use for post-event attribution review, or to raise budget before margin math is confirmed."
---

# Amazon 大促备战清单与广告布局

## 目标

Sequence pre-event readiness (listing assets, review count, inbound inventory) against a promotion timeline, then lay out automatic, manual, product-targeting, brand, and display ad structures suited to promotion-period traffic and conversion patterns. Keeps negative-keyword and bid-ceiling guardrails explicit for the event window.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 主图、A+、评论数量等达标线因类目和竞争强度不同差异很大，应以当前类目头部竞品水平做校准，而非套用统一数字门槛。
- 大促期销量倍数、竞价上限倍数等经验值均需用自身历史大促实际数据重新校准，不同产品、不同促销力度下倍数差异可能很大。
- 商品定位广告选择的竞品评论量、评分、价格带区间是经验筛选范围，应结合当前类目实际竞争格局调整，不是固定标准。
- 品牌广告与展示广告的受众定向、出价策略以后台当前可用功能为准，平台功能与规则可能随时调整。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、店铺、ASIN/SKU、广告类型和目标
- 同口径的 Campaign、Targeting、Search Term、Placement 与 Advertised Product 报告
- 售价、优惠、COGS、Amazon 费用、退款与目标贡献利润
- 库存、Buy Box、Listing、评论和同期市场事件

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 对照大促官方时间线倒推：秒杀折扣提报截止、入库截止、货件拆分截止等关键节点，标出本店铺各产品当前的达标或缺口状态。
2. 逐条核对 Listing 基础是否达标：主图是否白底清晰并配场景图和尺寸图、是否有演示视频、标题前段是否清楚传达核心信息、A+ 页面与评论数量是否达到可支撑转化的门槛，具体门槛以当前类目同价位竞品水平校准。
3. 按大促预期销量倍数（以自身历史大促实际倍数校准，不套用统一倍率）核算现有库存加在途库存的缺口，确保能在入库截止前补齐。
4. 按头部词竞争加剧、长尾词与精准定向性价比上升的大促流量特征重新分配预算，而非单纯提高原有出价。
5. 自动广告用于测词收集候选，手动广告（短语优先于精准）承接经验证的高转化词，同时对与自身材质规格明显不符的词提前否定。
6. 商品定位广告选择评论量、评分与价格带与自身相近但非头部的竞品作为定位对象，展示广告优先覆盖近期浏览未购买与已购买互补品的人群。
7. 品牌广告在大促期主要看点击率与转化率而非 ACOS 单一指标，用于抢占搜索结果顶部曝光而非直接追求投产比。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：获取竞品 ASIN 的评论量、评分与价格带作为商品定位广告候选池的代理证据。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 大促准备时间线核对表
- Listing与库存达标缺口清单
- 分类型广告结构布局方案
- 否定词与定位候选清单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
