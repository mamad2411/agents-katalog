---
name: sealeap-jiaotu-amazon-cross-marketplace-policy-audit
description: "Run a recurring cross-marketplace review that pulls each active marketplace's current fee schedule, new-seller incentive terms, and compliance requirement changes directly from official sources, then routes findings into operations, logistics, finance, and brand action lists. Findings are marketplace- and date-stamped at review time rather than assumed to persist, since fee and incentive terms are revised on independent schedules per marketplace. Use for 多站点费率变动核查、新卖家权益核对、跨站合规差异梳理、季度政策复盘、供应链与定价随政策调整. Do not use to apply one marketplace's fee change or incentive terms to another marketplace without checking that marketplace's own current announcement."
---

# Amazon 跨站点政策费用变动审计

## 目标

Run a recurring cross-marketplace review that pulls each active marketplace's current fee schedule, new-seller incentive terms, and compliance requirement changes directly from official sources, then routes findings into operations, logistics, finance, and brand action lists. Findings are marketplace- and date-stamped at review time rather than assumed to persist, since fee and incentive terms are revised on independent schedules per marketplace.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源列出的具体费率数字、优惠金额与门槛是特定时点的对比结果，各站点费率会独立调整，必须以当前官方公告为准，不得跨周期或跨站点直接套用。
- "平台战略意图"属于来源的解读与推测，不构成官方承诺，仅作为理解政策走向的背景参考，不应作为具体执行依据。
- 新兴站点的阶段性优惠通常有到期或退坡机制，需按官方说明核实到期后的正常费率，不按优惠期费率做长期规划。

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

1. 列出账户实际运营的所有站点，逐个进入官方费用与政策公告页面，记录本次复核周期内的费率变化、新增合规要求与生效日期，按站点分别归档而非混用。
2. 对每个站点核对是否存在未领取的新卖家或阶段性权益，逐项确认申领条件、有效期与是否需要主动申请，避免权益过期作废。
3. 从运营维度评估是否需要调整AI辅助工具、选品或Listing优化的使用方式，以匹配当前站点披露的新功能或新要求。
4. 从物流维度核对超龄库存费率、入库合作承运商政策与跨境履约选项的变化，评估是否需要调整库龄管理阈值或入仓路径。
5. 从财务维度按站点分别重算FBA与佣金成本对利润的影响，更新各站点独立的盈亏测算口径，不用单一站点的成本结构套用全部站点。
6. 从品牌与市场维度判断是否需要调整站点聚焦策略，依据是自身资源能否覆盖已识别的合规与运营要求，而非单纯因为有新优惠就扩张。
7. 把本轮审计结论与下一轮复核日期存档，形成可追溯的政策变化时间线，便于跨周期对比。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 分站点费率与政策变化记录
- 新卖家权益申领核对清单
- 运营/物流/财务/品牌四维度行动项
- 政策变化时间线归档
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
