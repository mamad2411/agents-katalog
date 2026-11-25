---
name: sealeap-dijiang-amazon-ppc-spend-gate-budget-rebalance
description: "Gate any keyword or search-term verdict behind a minimum spend or sample threshold calibrated to the product's own price point, distinguish genuinely unconverting terms from ones merely starved of budget inside a shared campaign, periodically re-audit historical negatives for revival, and rebalance placement bids and campaign budgets using each account's own efficiency line rather than someone else's benchmark. Use for 关键词该不该否掉、否定词是不是永久生效、广告位出价怎么调、预算没花完要不要加、SB和SP是不是在抢同一单. Do not use to pause or negate a keyword before it has accumulated enough spend or time to judge, and do not treat any fixed spend or ACOS percentage from external sources as this account's threshold."
---

# Amazon PPC关键词判定与预算再平衡

## 目标

Gate any keyword or search-term verdict behind a minimum spend or sample threshold calibrated to the product's own price point, distinguish genuinely unconverting terms from ones merely starved of budget inside a shared campaign, periodically re-audit historical negatives for revival, and rebalance placement bids and campaign budgets using each account's own efficiency line rather than someone else's benchmark.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源给出的花费比例、ACOS百分比等具体数字均为个人经验值，不同账户的客单价与类目转化率差异很大，一律用自身账户数据重新校准阈值，不直接套用。
- 预算没花完就加预算的逻辑建立在该广告本身投产效率已验证良好的前提上，效率尚未验证清楚的广告活动不适用这条，加错预算只会放大无效花费。
- 广告位维度的出价调整机制随广告类型与平台迭代变化，具体能否单独针对某一广告位降价以当前广告后台实际功能为准。

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

1. 在给任何关键词或搜索词下该不该否、该不该降价的判断之前，先设定一个按自身客单价校准的最低花费或订单样本门槛，花费或时间不够的词一律先归入数据不足、暂不判断，不提前处理。
2. 对达到判断门槛但确实零转化或转化极差的词，才作为否定词候选处理；对花费明显不足、但所在广泛匹配或自动广告活动里存在更大搜索量词抢占预算的词，先怀疑是被压制而非真的不转化，把它单独放进一个新广告活动获得独立预算再重新观察。
3. 定期回顾历史否定词清单，与当前搜索词报告的表现交叉核对：早期否定的词可能随着评论增多、Listing优化而具备了转化能力，符合条件的词可以移出否定清单重新测试，而不是否定后永久搁置。
4. 按广告位拆开看每个广告活动的实际转化效率，对明显优于自身目标效率线的位置加位置加价，对明显落后的位置由于通常无法单独降价，改为在下一轮统一下调关键词基础出价后再观察该位置的综合表现变化，避免频繁大幅跳变。
5. 对投产效率良好但当日预算并未跑满的广告活动，不要因为没花完就默认判定为已经到顶，先假设可能是高峰时段因预算受限被动错过了本可承接的优质流量，小幅上调预算后观察增量花费是否仍维持原有效率。
6. 如果同时存在多种广告类型在同一批词或同一批商品上重叠投放，用一次控制变量的暂停测试观察总转化是否明显下降，以此判断两者是互相蚕食还是真正增量，而不是默认都算作独立贡献。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 关键词判定花费/样本门槛设置记录
- 真死词与预算压制词分类清单
- 历史否定词复审与恢复测试记录
- 广告位效率对照与预算调整记录
- 广告类型间蚕食测试结论
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
