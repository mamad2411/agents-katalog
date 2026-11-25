---
name: sealeap-yazi-amazon-event-eligibility-price-stack-check
description: "Run a pre-event readiness check before major sale windows: audit listing and account health signals, confirm each promotion tool's current eligibility threshold directly in the seller backend, and reconcile the net customer-facing price across every stacked promotion against the currently visible reference price. Every eligibility threshold and stacking rule is treated as changeable and must be reverified in-platform before submission. Use for 大促开售前要检查什么、店铺与商品评分够不够报会员专享折扣、优惠券和秒杀能不能叠加、折后净价怎么算才不会报错、大促报名前的账号自查清单. Do not use to submit a promotion with a percentage or price copied from a prior period without re-checking the current backend eligibility page and price calculator."
---

# Amazon 大促资格与价格联动预检

## 目标

Run a pre-event readiness check before major sale windows: audit listing and account health signals, confirm each promotion tool's current eligibility threshold directly in the seller backend, and reconcile the net customer-facing price across every stacked promotion against the currently visible reference price. Every eligibility threshold and stacking rule is treated as changeable and must be reverified in-platform before submission.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源中的具体折扣百分比、评分门槛与时间间隔天数均为特定时期的规则快照，随时可能调整，一律不采用来源数字，只在当前后台复核后使用。
- 取多个比较基准中最严格的一个作为最终价格是来源总结的通用做法，具体涉及的基准种类与计算顺序需以当前后台公式为准，不假设与来源完全一致。
- 报错处理所需的补充材料因站点和错误类型而异，来源列出的清单仅供参考，实际以系统当次提示为准。

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

1. 开售前统一核对目标站点的账号与商品健康信号：Listing 是否冻结、必填属性是否完整、账号绩效通知是否有未处理项，逐条清零而非等报名被拒才发现。
2. 确认每个促销工具（会员专享折扣、秒杀、优惠券等）当前在后台公示的资格门槛（店铺评分、商品评分、参考价可见性等），以当期后台页面数值为准，不套用往期或他人经验值。
3. 拉出真实成交价历史，标记其中的促销价、企业订单与异常订单，确认当前是否存在可见参考价；参考价不可见时先判定为不可报名，而非假设能通过审核。
4. 对将要叠加使用的每种促销工具，按后台当期公式逐一计算折后净价与各自比较基准，确认哪个基准最严格并以其作为最终报名价格依据。
5. 核对同类促销之间的时间间隔限制在当前站点后台的设置，避免因间隔不足被系统拒绝。
6. 提交前预览一次实际展示效果，确认折扣显示、到手价与库存分配符合预期；出现报错时先按后台提示核对参考价或历史价材料是否需要补充，而非重复盲试。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 账号与商品健康自查清单
- 促销工具资格门槛核对记录（按站点/工具）
- 真实成交价与参考价时间线
- 促销叠加折后净价计算表
- 报名前预览与报错处理记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
