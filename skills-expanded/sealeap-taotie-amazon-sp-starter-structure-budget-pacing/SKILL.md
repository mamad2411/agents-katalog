---
name: sealeap-taotie-amazon-sp-starter-structure-budget-pacing
description: "Set up the first Sponsored Products structure for a listing—one auto and one manual campaign, hero variation only, daily budget sized to run all day, default bid tuned so spend tracks budget—then read impressions, clicks, CTR, spend and ACOS together with organic uplift to decide the next adjustment. Console labels follow the current Ads interface. Use for 新品广告怎么开、自动手动各开一组、变体要不要都推、日预算多少合适、预算一早花完、默认竞价怎么调、曝光高点击低、不符合条件状态、ACOS 要不要算自然单. Do not use for bulk bid rules, SB or SD campaigns, or executing changes without an approved change table."
---

# Amazon SP 广告起步结构与预算节奏校准

## 目标

Set up the first Sponsored Products structure for a listing—one auto and one manual campaign, hero variation only, daily budget sized to run all day, default bid tuned so spend tracks budget—then read impressions, clicks, CTR, spend and ACOS together with organic uplift to decide the next adjustment. Console labels follow the current Ads interface.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 「出价高不等于排名高，广告有质量分」「广告不能挽救产品力」是来源对平台机制的解释，属待验证假设，只能用账户内的 CTR 与转化数据观察。
- 来源举例的预算、出价与 ACOS 数字为经验值，以当前建议竞价区间、毛利与盈亏平衡 ACOS 校准。
- 把自然单纳入 ACOS 判断需要固定归因窗口与基线对照，否则会高估广告效果；建议与总 ACOS（TACOS）并列记录。
- 控制台菜单、匹配类型说明与报表列名以当前广告界面为准，来源截图时代的名称可能已变更。

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

1. 确认可投放前提：SKU 有购物车且 FBA 有货，状态显示「不符合条件」时先查库存与购物车，不调广告参数；报表视图把所有列（曝光、点击、CTR、花费、CPC、订单、销售额、ACOS）全部勾选显示。
2. 自动与手动各建一组：自动组可放多个同型号不同款式的 SKU 轮流曝光以找出热销款；手动组只推最可能成交的一个变体（尺码/颜色），避免多个变体各自出价互相抢位。
3. 日预算按「能跑满全天」定：预算过小会在数小时内耗尽后停止曝光；默认竞价从当前建议区间中位附近起步，隔日看消耗，出价偏低则预算花不完、偏高则提前耗尽，反复微调到日消耗接近预算。
4. 先读三列：曝光足够但 CTR 低于同类目经验值时检查主图、价格与关键词意图错配；曝光不足时看出价或相关性；点击多但订单少时看评价数量与详情页转化；每次只改一个变量。
5. 看 ACOS 时把广告带来的自然单增长纳入判断（广告花费 ÷（广告销售额 + 归因期内的自然销售增量）），不以单一 ACOS 越低越好为目标；变体互购会计入广告销售额，读数时注意。
6. 自动组找到订单集中的款式后，把该款作为引流 SKU 加库存或小幅让利，并在手动组用词组或精准投放承接；手动组每周按词调整出价，无效词降价或暂停，有效词加价并记录。
7. 输出待批准变更表并设置回读：下次复盘先比较日消耗、CTR 与订单是否按预期变化，再决定第二轮调整。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 起步广告结构表（自动/手动/推广变体）
- 日预算与默认竞价校准记录
- 三列诊断结论（曝光/CTR/转化）
- 含自然单的 ACOS 读数表
- 待批准变更表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
