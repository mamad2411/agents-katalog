---
name: sealeap-tianlu-amazon-data-reporting-filing-evidence-collection
description: "Help a seller decide and execute a response after a marketplace begins sharing seller sales data with tax authorities: verify reporting-scope applicability, collect sales and deductible-cost evidence from backend report channels, document a comply-now-or-wait decision with a review trigger, and check payout-account compliance. Does not determine final tax liability or endorse entity-switching as a workaround. Use for 平台数据报送后报税应对决策、抵扣凭证归集、收款账户合规核对. Do not use to decide final tax liability, and do not use to justify switching business entities to avoid reporting."
---

# Amazon 数据报送后报税应对

## 目标

Help a seller decide and execute a response after a marketplace begins sharing seller sales data with tax authorities: verify reporting-scope applicability, collect sales and deductible-cost evidence from backend report channels, document a comply-now-or-wait decision with a review trigger, and check payout-account compliance. Does not determine final tax liability or endorse entity-switching as a workaround.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 是否已被纳入报送范围、申报口径与“按实申报 vs 观望”的利弊在不同地区、不同主管税务机关的执行尺度下可能差异很大，文中判断仅为该时点观察，不能当作全国统一规律。
- 各类费用凭证能否被认可为合规抵扣依据，最终取决于主管税务机关的认定，本流程只负责收集与整理，不代替税务师出具申报意见。
- 频繁更换经营主体是否会被认定为规避申报属于个案判断，不做“一定安全”或“一定违规”的断言，需结合具体情况由专业顾问评估。

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

1. 确认本账户是否已进入平台向税务机关报送经营数据的适用范围，以平台官方通知与当地税务机关的最新口径为准，不凭猜测判断是否被覆盖。
2. 如决定按实申报，先从店铺后台可核实的官方报表（结算类汇总报表、广告费用凭证申请渠道、物流仓储费用明细报表等）逐项导出销售与费用数据作为申报依据，不使用回款到账金额代替销售额。
3. 对每一类可抵扣费用，核实当前可获取的凭证形式（发票、平台开具的费用证明、报表明细等）是否被主管税务机关认可，不确定的项先标记待确认，交给税务顾问判断。
4. 如选择观望而非立即按实申报，明确记录观望的具体理由、预计复核时间点与触发立即行动的条件（如收到官方通知、同行出现稽查案例等），避免无限期搁置。
5. 检查各店铺收款账户是否符合平台当前要求的账户合规标准，对不符合项按官方要求的时限完成调整，避免触发下架或禁售风险。
6. 不以更换经营主体作为应对报送压力的手段；如确有合理的主体调整需求，先与税务顾问确认时点与方式是否会被解读为规避申报，再决定是否执行。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 报送范围适用性核查记录
- 销售与费用凭证归集表
- 观望/申报决策记录及复核触发条件
- 收款账户合规核对清单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
