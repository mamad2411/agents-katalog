---
name: sealeap-yazi-amazon-policy-change-response-checklist
description: "Run a structured response check whenever Amazon announces a policy change (variant/review rules, FBA labeling, listing-content standards, category compliance deadlines, payout timing): confirm the official rule and effective date, determine applicability to the current account, list the evidence or listing changes required, and set an internal deadline with an owner. Treats every rule as subject to change and requiring in-platform reverification. Use for 亚马逊新规怎么应对、变体评论规则变了要不要拆分、能不能用厂商条码替代平台标签、页面会不会被判定低质量降权、类目认证快到期了怎么办、结算周期变化要不要调整现金流. Do not use to state what a rule currently says without verifying it on the official policy page and seller backend first."
---

# Amazon 平台新规响应核对流程

## 目标

Run a structured response check whenever Amazon announces a policy change (variant/review rules, FBA labeling, listing-content standards, category compliance deadlines, payout timing): confirm the official rule and effective date, determine applicability to the current account, list the evidence or listing changes required, and set an internal deadline with an owner. Treats every rule as subject to change and requiring in-platform reverification.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 具体的生效日期、评分门槛、认证截止日等数值会随官方公告调整或延期，本 Skill 不代入任何具体日期或数值，一律以官方页面当前状态为准。
- 平台内容质量评估等算法机制的判定标准未公开，只能作为待验证假设纳入自查清单，不能当作确定规则执行。
- 同一政策在不同站点的生效时间与适用范围可能不同，需按站点分别核实，不能用一个站点的结论套用到其他站点。
- 结算周期或费率变化对现金流的影响需用自身账户实际回款数据测算，来源说法仅提示存在变化，具体影响幅度不采用来源数字。

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

1. 拿到新规信息后，先到官方政策页面或卖家后台通知核实规则原文、适用站点与生效日期，转载或摘要内容只作为线索，以官方页面为准。
2. 判断新规是否适用于自身账户与产品：逐条核对涉及的类目、变体结构、品牌注册状态或结算方式是否命中范围，未命中的记录暂不适用并保留复核时间点。
3. 命中的条目逐项列出所需证据或操作（变体分类整理、条码更换资质、认证文件、内容改版），标注负责人与所需时间，按生效日期倒推内部截止日。
4. 涉及可能影响展示或资金的规则（内容质量评估、结算周期变化）时，用自身账户数据评估影响幅度，作为待验证影响预留缓冲，不假设与来源描述的程度一致。
5. 生效日期前完成自查，并在后台做一次预览或模拟检查（如可行），确认相关对象状态已符合新规要求。
6. 建立新规追踪台账：记录规则来源、生效日期、命中状态、处理进度与复核时间点，供下一次规则更新复用同一流程。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 新规适用性核对表（站点/类目/命中状态）
- 证据与操作清单（含负责人与截止日）
- 现金流或展示影响的待验证评估记录
- 生效前自查结果
- 新规追踪台账
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
