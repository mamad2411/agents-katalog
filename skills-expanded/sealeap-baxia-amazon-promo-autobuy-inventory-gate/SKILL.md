---
name: sealeap-baxia-amazon-promo-autobuy-inventory-gate
description: "Coordinate multi-marketplace promotion timing and list-price changes against a price-triggered automatic-ordering feature so inventory buffers, not just discount depth, gate any price move during a promotion window. Use for 分站点大促排期确认、上线价格触发式自动下单或提醒功能后的调价预案、促销期库存断货风险排查. Do not use to lower list price without first confirming current stock coverage and the feature's live trigger rules on the target site."
---

# Amazon 促销自动下单库存预案

## 目标

Coordinate multi-marketplace promotion timing and list-price changes against a price-triggered automatic-ordering feature so inventory buffers, not just discount depth, gate any price move during a promotion window.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 各站点具体促销日期、预热与正式期划分每轮都会调整，不作为固定日历使用，执行前以官方最新公告为准。
- 自动下单或提醒功能是否识别优惠券、秒杀价等叠加折扣，属于平台机制细节，需在目标站点当次核实，不能沿用此前版本的判断。
- 降价可能批量触发远超备货预期的订单，目前是行业观察到的待验证现象，实际触发规模因类目与关注量而异，需以自身账户监控数据校准。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、ASIN/SKU、库存阶段、补货与到仓时间
- 断货或备货前后的销量、流量、广告、自然位置和转化基线
- COGS、头程、仓储、平台费、退货和清仓成本
- 可比产品的成熟度、销量区间和需求趋势

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 促销开始前到目标站点后台核实本轮各站点的实际促销日程与规则版本，不沿用往期经验日期。
2. 确认目标市场是否已上线价格触发式自动下单或提醒功能，以及该功能当前识别的是标价还是叠加优惠后的实付价。
3. 核对每个可能触发自动下单的价格点位对应的现有库存与在途库存，估算若价位触发会消耗多少库存、是否会击穿安全库存线。
4. 调整标价前设定单次降价幅度上限与观察窗口，分批小幅试探而非一次性大幅降价，并预留暂停或恢复原价的操作路径。
5. 促销期内持续监控订单速率与库存消耗曲线，出现异常放量时立即核实是否为自动下单触发并评估是否暂停或调价。
6. 促销结束后复盘触发订单占比与库存影响，更新下一轮促销的价格与备货缓冲设置。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 分站点促销日程核对表
- 价格点位库存消耗测算
- 分批调价与回退预案
- 促销期订单异常监控记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
