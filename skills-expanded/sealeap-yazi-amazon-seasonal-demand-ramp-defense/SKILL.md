---
name: sealeap-yazi-amazon-seasonal-demand-ramp-defense
description: "Sequence a seasonal listing's push from off-season pickup through peak-season promotion into the next off-season by checking inventory pacing, ad-architecture completeness, keyword-testing timing, and deal/coupon/reference-price consistency before defending rank with disciplined pricing. Every pacing or pricing threshold is calibrated to the account's own margin and inventory data, not copied from any single case. Use for 季节性产品淡季接手怎么起量、旺季秒杀价格被系统锁死怎么防、会员日前广告怎么布局、淡季怎么守住排名、变体什么时候该补齐. Do not use to promise a specific rank, order volume or price outcome, and do not use to set live deal or coupon prices without checking current back-end reference-price status first."
---

# Amazon 季节性单品推进节奏管理

## 目标

Sequence a seasonal listing's push from off-season pickup through peak-season promotion into the next off-season by checking inventory pacing, ad-architecture completeness, keyword-testing timing, and deal/coupon/reference-price consistency before defending rank with disciplined pricing. Every pacing or pricing threshold is calibrated to the account's own margin and inventory data, not copied from any single case.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源中的具体价格、单量、排名名次与费用数字均为单一案例的经验观察，不同账户的品类、客单价与竞争格局差异很大，不作为可复制目标，需用自身账户历史数据重新校准。
- 先测试核心词转化率再决定是否加大投入之类的先后顺序是该案例的经验判断，未验证在所有品类都适用，按待验证假设处理。
- 促销工具与参考价的联动细节（例如系统按历史最低价自动认定折扣基准）会随平台规则调整，执行前必须在当前后台复核，不能沿用旧经验。
- 案例中出现的具体折扣力度、活动报名费用与档期时长来自特定时期与站点，需在报名页面核对当期实际规则后再决策，不代入历史数字。

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

1. 接手时先核对起点基线：链接是否断货、广告架构覆盖是否完整（关键词、否定词、ASIN 定投）、自然单与广告单占比、当前类目排名区间，把这些记为对照基准而非目标值。
2. 判断产品是否具备可持续起量的差异化依据（评论、复购或同类相对表现），证据不足时先做小范围测试验证需求，不直接放量推广告。
3. 起量顺序为先补齐广告架构覆盖面、再测试高流量核心词：核心词转化率达到账户自身盈亏平衡水平前，不追加大额预算硬推核心词。
4. 使用秒杀、优惠券、专享价等促销工具前，先在后台核对当前参考价/历史价与各工具的联动规则（哪个价格字段会被系统记为参照的最低价），小范围验证不会被锁定在非预期低点后再放量执行。
5. 冲高排名前，用可用库存（不含预留与在途）能否覆盖预期单量增幅作为判断依据，不足时主动控制预算，不冒断货风险冲排名。
6. 大促与会员日的广告及价格布局提前完成，活动结束后待指标企稳再进行下一轮调整，避免同时改动多个变量导致无法归因。
7. 进入需求下滑期后从冲排名切换为守排名：以现有广告效率与价格稳定性为主，并对表现落后的变体加快出清，避免拖累整体库存与利润。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 起点基线记录（断货状态/广告架构/占比/排名区间）
- 差异化与需求证据核查结果
- 促销工具与参考价联动核对记录
- 库存与冲排名的联合评估表
- 淡季防守动作与变体调整记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
