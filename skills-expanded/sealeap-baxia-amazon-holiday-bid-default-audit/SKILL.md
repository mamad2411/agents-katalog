---
name: sealeap-baxia-amazon-holiday-bid-default-audit
description: "Audit Amazon Sponsored Products bidding-strategy settings for a silently pre-enabled schedule-based bid increase during a seasonal demand drop, and pair the correction with clearance and next-cycle product planning. Use for 旺季销量骤降但ACOS走高的排查、广告后台默认竞价规则核查、季节性滞销品清仓与选品转向决策. Do not use to raise or lower live bids without first checking current organic rank and conversion for the same keywords."
---

# Amazon 旺季广告默认竞价排查

## 目标

Audit Amazon Sponsored Products bidding-strategy settings for a silently pre-enabled schedule-based bid increase during a seasonal demand drop, and pair the correction with clearance and next-cycle product planning.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 默认全天加价这类具体规则名称与幅度可能随广告后台改版调整，执行前必须在自己账户实际界面核实当前选项文字与默认状态，不能假设与来源描述完全一致。
- 平台是否为最大化广告收入而设置默认加价，属于对平台动机的推测，只作为待验证假设，不作为申诉或谈判依据。
- 何时判定某SKU为滞销及清仓折扣幅度，需按自身库存周转与毛利数据设定阈值，不套用统一比例。

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

1. 对比近期自然流量与广告花费曲线，确认是否存在销量下滑但广告支出不降反升的背离，锁定异常时间段。
2. 逐个广告活动进入竞价策略设置，检查按时段规则一类选项下是否存在系统默认勾选的全天或分时段加价规则，记录发现时的具体勾选状态。
3. 对已确认季节性高自然流量的关键词，评估维持默认加价是否只推高花费而未提升增量转化，作为取消或下调该规则的依据。
4. 手动调整竞价前用当前账户的盈亏平衡ACOS作为校准基准，而不是套用固定百分比，分批调整并观察数据后再决定下一步。
5. 对判断为季节性滞销的库存，评估降价清仓与继续投放广告的资金效率，优先回笼现金而非维持曝光。
6. 旺季结束前启动下一节点的选品与广告预算迁移计划，避免资源在需求切换后仍集中于旧品。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 旺季自然流量与广告花费背离记录
- 默认竞价规则排查清单
- 分批调价与观察记录
- 滞销清仓与选品转向计划
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
