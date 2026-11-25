---
name: sealeap-tianlu-amazon-fba-delivery-window-appeal
description: "When an FBA shipment is flagged for missing its estimated delivery window, first confirm the current window definition and any platform-side delivery-interruption notice in Seller Central, then assemble a dispute package (interruption notice, original window evidence, and a concise root-cause statement) through the shipment issue dispute flow. Assumes the appeal template and turnaround expectation are recalibrated against the account's own dispute history rather than a fixed prior benchmark. Use for FBA货件绩效异常申诉、送达窗口变更申诉材料准备、入仓时效问题追踪. Do not use to file a dispute without first confirming the shipment was actually affected by a platform-side interruption rather than the seller's own inbound delay."
---

# Amazon FBA送达异常申诉

## 目标

When an FBA shipment is flagged for missing its estimated delivery window, first confirm the current window definition and any platform-side delivery-interruption notice in Seller Central, then assemble a dispute package (interruption notice, original window evidence, and a concise root-cause statement) through the shipment issue dispute flow. Assumes the appeal template and turnaround expectation are recalibrated against the account's own dispute history rather than a fixed prior benchmark.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 送达窗口的具体天数、判定规则会随平台政策调整，来源提到的具体窗口天数仅供参考，执行前以账户当前后台展示为准。
- 申诉成功率与处理时效因证据完整度和本次绩效历史而异，来源关于多数卖家能成功撤销的说法是个案总结，不能作为申诉结果的保证。
- 仅当延误确系平台侧通知的中断或调整所致时才适用本流程；自身发货或资料问题导致的绩效记录应按对应问题分类处理，不应混用本申诉话术。

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

1. 核对当前账户后台对预计送达窗口的定义与本次货件被判定异常的具体口径，不沿用旧窗口天数的印象。
2. 用货件编号在通知邮箱与后台消息中检索配送中断或时间窗口调整类通知，完整保存原始通知内容，作为证据的时间戳来源。
3. 核对本次货件的绩效标记原因是否确系平台侧调整或中断所致，而非自身发货延迟、资料缺失等自身原因造成，避免对非平台责任的延误发起申诉。
4. 在货件问题详情页发起争议，用简洁英文说明原始窗口设置、附上平台通知证据，并明确指出延误的根本原因，避免主观归因或无证据陈述。
5. 提交后按后台展示的处理时效跟进结果；若被驳回，核对驳回理由是否指向证据不足或本次确非平台责任，再决定是否补充材料重新申诉。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 送达窗口口径与异常判定核对记录
- 配送中断/调整通知证据留存
- 申诉说明文本与提交记录
- 申诉结果跟踪与复核记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
