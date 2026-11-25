---
name: sealeap-feilian-amazon-promo-tier-remarketing-plan
description: "Review current on-platform ad and promotion performance before a major sales event to tier discount depth by SKU contribution margin instead of running one blanket promotion, then time a post-event remarketing push toward shoppers who compared but did not convert. Treats any channel-mix or timing pattern drawn from public commentary as a hypothesis to verify against the account's own traffic and margin data. Use for 大促促销深度分层、毛利保护、站外内容渠道承接测试、节后回流承接、促销预算与广告投放占比复核. Do not use to copy a blanket discount rate or channel-mix ratio from public commentary without checking current account margin and traffic data first."
---

# Amazon 大促分层促销与站外承接规划

## 目标

Review current on-platform ad and promotion performance before a major sales event to tier discount depth by SKU contribution margin instead of running one blanket promotion, then time a post-event remarketing push toward shoppers who compared but did not convert. Treats any channel-mix or timing pattern drawn from public commentary as a hypothesis to verify against the account's own traffic and margin data.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源提到的消费支出变化、卖家规模占比等统计数字来自第三方市场报告，样本与口径不明，只能作方向性参考，不能作为本账户流量或利润变化的直接归因证据。
- 自然流量见顶、平台流量成本上升是来源的解读，需用自身账户近期展示/点击/转化趋势独立验证，不能仅因行业报道就断定自身流量结构已改变。
- 站外内容渠道的引流效果因品类与受众而异，来源列举的具体平台组合是启发而非结论，需按自身产品适配性测试后再决定资源分配比例。
- 促销分层与节后承接动作不得涉及刷单、补单冲量、诱导好评或虚构订单等操纵性做法；所有优惠与顾客沟通须在平台规则允许范围内公开进行。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- 目标 marketplace 与案例 ASIN 的明确时间范围
- 销量、评论、价格、促销、变体和上架时间线
- 关键词自然/广告可见度、品牌与站外流量代理证据
- 可复核来源、数据口径、缺失项和替代解释

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 核对本次大促可用的促销工具与近期广告位表现（展示量、点击率、转化率趋势），判断当前流量是否已出现展示上升但转化未同步增长的边际收益下降信号，而不是默认归因于外部大环境。
2. 按SKU贡献毛利与库存深度分层：区分可承受深折扣的走量款、需要控制折扣深度的稳态款、只做曝光不做深促的边缘款，为每层设定各自的折扣上限与预算占比，并写入同一张表避免层级混用。
3. 小规模测试将部分预算从站内广告转向站外内容渠道（如第三方测评、短视频、社群分享）的引流成本与到站转化，验证后再决定是否扩大投入，不直接套用某一组固定渠道组合。
4. 为新客与老客设计不同的促销触点（如新客首购价、老客专属券），在后台核实两者是否可叠加以及顾客实际到手价，避免促销工具冲突导致折扣超出预期或触发资格问题。
5. 提前规划大促结束后固定天数内的站外承接动作（如补充对比测评、更新内容），用于承接消费者活动结束后对比复盘再下单的回流需求。
6. 活动结束后按同一套口径复盘：分渠道流量成本、实际折扣深度、单件净贡献与库存去化速度，判断本轮分层策略是否达到保护毛利的目标，用于校准下一轮的分层阈值。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 促销位与广告位边际收益诊断记录
- SKU毛利分层与折扣上限对照表
- 新老客促销叠加与到手价核验记录
- 节后站外承接排期草案
- 分渠道复盘与分层阈值调整建议
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
