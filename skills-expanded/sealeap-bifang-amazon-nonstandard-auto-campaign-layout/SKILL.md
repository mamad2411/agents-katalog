---
name: sealeap-bifang-amazon-nonstandard-auto-campaign-layout
description: "Design and review a layered automatic campaign structure for non-standard Amazon products whose buyers browse rather than search with intent: several automatic campaigns split by targeting group and bid level, category-word negatives, product-page placements, a budget cap relative to the whole account, a fixed adjustment cadence tied to the attribution window, and early setup ahead of peak season so campaigns carry history when traffic arrives. Use for 非标品广告怎么投、自动广告要不要一直开、旺季前广告布局、关联流量投放、自动广告分组、广告调整频率. Do not use for standard products with clear head keywords, or to create live campaigns without an approved change table."
---

# Amazon 非标品自动广告分层布局

## 目标

Design and review a layered automatic campaign structure for non-standard Amazon products whose buyers browse rather than search with intent: several automatic campaigns split by targeting group and bid level, category-word negatives, product-page placements, a budget cap relative to the whole account, a fixed adjustment cadence tied to the attribution window, and early setup ahead of peak season so campaigns carry history when traffic arrives.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- “标品占平台大部分流量”“非标品在靠后页面也有成交”是来源对流量特性的概括，需用自身广告位报告验证。
- “两档竞价形成内部竞争可降低整体消耗”是来源对拍卖机制的推断，作为假设观测；六组结构和竞价差额均为个人习惯，按类目与预算调整。
- 调整周期与最低点击数是经验值，以当前归因窗和转化率的统计稳定性校准。
- “临时新建活动没有权重、旺季投产比低”是平台算法解释，不作为规律；只以自身历史数据比较新旧活动表现。

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

1. 判定产品类型：看流量结构——搜索意图明确、主要在搜索结果前几页成交的属标品；无明确主词、搜索结果靠后页面与详情页关联流量也有成交的属非标品。用搜索词报告和广告位报告（搜索结果页 vs 商品页）验证，不凭类目常识判断。
2. 非标品预算取向：把预算更多分给流量入口拓展（自动广告与商品页投放）而不是推高单一关键词排名；以自动广告作为拓词、收录和关联流量的工具，竞价整体放低。
3. 分层结构：按投放组分成三层，每层两个不同竞价档的广告活动以形成内部竞争——①全部匹配方式、否定已知的品类大词，用于拓词与详情页曝光；②只保留紧密匹配、低于建议竞价的两档，用于为手动投放积累词；③只投同类/互补商品、否定头部品牌 ASIN，用于关联流量。竞价档差距按当前建议竞价校准。
4. 手动承接：当某词或某 ASIN 在自动组内的转化率稳定并高于组内均值时，移入手动投放并给予更高竞价；只有手动组的转化率超过自动组后才在自动组内否定该对象，避免过早否词。
5. 自守与预算上限：在自己的商品页投放自身广告位以防竞品占满；自动广告合计预算不超过总预算的一定比例（按当前账户校准），成熟后以手动为主。
6. 调整节奏与停止：每次改竞价或否词都写入记录；投放初期可较频繁调整，之后至少等一个归因窗口再动；每个大组累计足够点击后才评估转化率，点击不足不下结论；某一竞价档连续多个周期点击充足却无转化时关停该档。
7. 旺季准备：提前建立并让活动积累表现历史，旺季到来只通过加预算与提竞价放量，避免临时新建活动。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 标品/非标品判定依据（搜索词与广告位报告摘要）
- 自动广告分层结构表（组、匹配、竞价档、否定、预算）
- 自动到手动的承接与否词规则
- 调整节奏与变更记录模板
- 旺季前布局检查表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
