---
name: sealeap-bifang-amazon-offsite-channel-and-attribution
description: "Choose and evaluate off-Amazon traffic channels for a product, including deal and discount-code postings, platform or creator collaborations, a compliant email list, SEO content, paid social ads and influencer reviews, by matching each channel to the goal and margin, routing traffic through Amazon's official attribution links for measurement, keeping insert cards within policy, and treating any keyword-rank lift from canonical-style URLs as a hypothesis to test rather than a tactic to rely on. Use for 站外推广怎么做、折扣码发哪里、邮件列表怎么建、小卡片能写什么、权威链接是什么、站外引流能提升排名吗. Do not use to solicit or incentivise reviews, to build URLs intended to manipulate search ranking, or to spend on channels without an approved budget and measurement plan."
---

# Amazon 站外引流渠道选择与验证

## 目标

Choose and evaluate off-Amazon traffic channels for a product, including deal and discount-code postings, platform or creator collaborations, a compliant email list, SEO content, paid social ads and influencer reviews, by matching each channel to the goal and margin, routing traffic through Amazon's official attribution links for measurement, keeping insert cards within policy, and treating any keyword-rank lift from canonical-style URLs as a hypothesis to test rather than a tactic to rely on.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- “站外订单提升关键词权重与排名”“权威链接内含核心关键词”均为来源对平台机制的解释；只可作假设在账户内观测，不可据此构造引导搜索的链接。
- 来源提到通过抽奖、折扣变相刺激评论增加，属于激励评论，不采用。
- 站外流量转化率通常低于站内，可能稀释整体转化率；用官方归因与业务报告分开口径看，不混算。
- 大促期间的平台整体销售数据与个体表现无因果，不用于预测本品效果。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、ASIN/SKU、广告归因窗与业务报告时间窗
- 广告订单、总订单、会话、自然位置、TACOS 与贡献利润
- 价格、优惠、库存、Buy Box、Listing 和评论变更日志
- 查询、广告位和投放对象的相关性证据

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 先定目标与约束：本次站外是为了触达新客、拉高转化率还是清库存；写下可让利的折扣上限（按利润率倒推）与预算；目标不同选渠道不同。
2. 渠道匹配：低单价高折扣适合折扣码/促销信息渠道；有内容属性的产品适合红人体验与社媒内容；复购品适合邮件列表；有品牌与自建站的可用付费社媒定向广告；每个渠道写明预期成本、预计订单和停止线。
3. 合规的触点：随货卡片只放售后邮箱、说明书、官网等中性信息，不引导评价；邮件列表通过问卷或售后服务合法收集，内容为使用指南、更新与优惠。
4. 链接与度量：所有站外链接优先使用平台官方的归因链接（可分渠道计量，且可能享有品牌推荐奖励），记录点击、加购、订单与归因窗；来源所说的“含核心关键词的权威链接可提升关键词权重”只作为待验证假设，如要测试必须单渠道单变量并设对照期。
5. 验证与停止：按渠道比较站外订单成本与站内 PPC 成本、转化率是否被无效流量稀释、目标关键词自然位是否变化；成本超过停止线或转化率明显下滑的渠道暂停并复盘。
6. 沉淀：把有效渠道、折扣幅度、时间点与结果写入渠道档案，作为下次新品或促销的起点。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 站外目标、折扣上限与预算表
- 渠道匹配与停止线表
- 合规触点文案清单（卡片、邮件）
- 归因链接计量记录与渠道效果对比
- 渠道档案
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
