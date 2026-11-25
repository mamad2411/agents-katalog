---
name: sealeap-jiaotu-amazon-ad-spend-cashflow-guard
description: "Verify the ad account's current billing and settlement mechanism (what triggers a charge and what happens on insufficient balance) directly in the advertising console before assuming a prior mechanism still applies, then size a cash buffer from actual daily spend and set a low-balance alert so campaigns are not abruptly paused mid-flight. Buffer size and alert threshold are derived from the account's own spend history, not a fixed day count. Use for 广告扣款机制核对、余额不足停投排查、广告现金流预警设置、多站点广告资金调度. Do not use to assume a specific settlement threshold or charge trigger without confirming it in the current advertising billing settings."
---

# Amazon 广告账户余额现金流风控

## 目标

Verify the ad account's current billing and settlement mechanism (what triggers a charge and what happens on insufficient balance) directly in the advertising console before assuming a prior mechanism still applies, then size a cash buffer from actual daily spend and set a low-balance alert so campaigns are not abruptly paused mid-flight. Buffer size and alert threshold are derived from the account's own spend history, not a fixed day count.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 具体扣款触发门槛与结算周期是来源观察到的某一时点机制，账户实际计费规则以广告后台当前计费说明为准，不作为长期不变的规则记忆。
- 安全垫天数是来源经验值，应按自身账户的日均花费、波动幅度与回款周期重新计算，不同规模账户所需天数差异很大。
- 余额不足是否会造成广告投放大幅下跌，取决于当前平台的实际暂停与恢复机制，以自身账户历史发生过的情况或官方说明为准，不预设最坏情况一定发生。

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

1. 在广告后台的计费/结算设置里核对当前的扣款触发方式（按累计门槛扣款、还是按花费实时扣减余额）、扣款来源及余额不足时系统的处理方式，不沿用旧机制假设。
2. 按各站点近期日均广告花费和花费波动幅度（含峰值日）测算所需安全垫天数，波动大的账户按更保守的天数留存，具体天数由自身数据决定而非套用固定天数。
3. 核对各广告活动的预算上限设置是否与账户可承受的资金能力匹配，避免单一活动或异常点击在短时间内消耗超出安全垫的预算。
4. 建立资金回补节奏：核对当前提现/回款周期，评估是否需要缩短周期或预先充值以保持广告资金持续可用。
5. 在能设置的范围内配置余额或花费预警，确保余额触及安全垫下限时能在广告被暂停前完成补充或主动降预算。
6. 若同时运营多个站点/账户，核对各自结算币种与资金池是否独立，避免以为资金充足实际上分散在不互通的账户里。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 广告扣款与结算机制核对记录
- 日均花费与安全垫测算表
- 活动预算上限校核清单
- 余额预警与回补节奏方案
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
