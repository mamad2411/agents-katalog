---
name: sealeap-taotie-amazon-search-term-report-tiered-review
description: "Review the Sponsored Products search term report by tier—impressions, clicks, CTR, orders and conversion per customer search term—separating searched terms from targeted keywords and ASIN entries, then produce a keyword-promotion list, a negative-keyword list and a listing-fix list gated by evidence. Use for 搜索词报告怎么看、客户搜索词和关键词区别、B0 开头是什么、哪些词加否定、否定短语和否定精确怎么选、自动广告的词怎么迁到手动、有点击没转化怎么办. Do not use to push negatives or bid changes to live campaigns without an approved change table."
---

# Amazon 搜索词报告分层复盘与否定词

## 目标

Review the Sponsored Products search term report by tier—impressions, clicks, CTR, orders and conversion per customer search term—separating searched terms from targeted keywords and ASIN entries, then produce a keyword-promotion list, a negative-keyword list and a listing-fix list gated by evidence.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 「ASIN 条目无法否定」是来源当时的控制台限制，商品页投放与否定商品功能已多次更新，必须以现有功能为准。
- 来源举例的 CTR、转化率、出价数值与时间窗均为经验值，以本账户各广告组均值与样本量校准，不作阈值。
- 「点击多不转化 = 价格或评价问题」是来源的排除法假设；每次只改一个变量并设观察窗，才能把结论归入账户内证据。
- 搜索词报告的曝光与业务报告口径不同，不得把两者相减推算自然流量。

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

1. 在广告报告入口下载搜索词报告（时间范围按当前允许上限自定义），确认报告只含产生过广告点击的搜索词、且曝光口径与业务报告不可直接比较；报告字段名以当前控制台为准。
2. 区分三列：关键词/投放列是你设置的投放对象（自动投放显示为通配标记），客户搜索词是买家实际输入，以 ASIN 编号形式出现的条目来自商品页关联流量；后者能否被否定或作为投放对象，按当前控制台功能核对，不沿用旧结论。
3. 先按广告组筛选再按曝光降序看：曝光高但 CTR 明显低于本账户均值的词，检查搜索意图与产品是否错配（同词根不同品类），错配词进入否定候选，匹配的词检查主图与价格。
4. 按点击降序看：点击多但零单或转化远低于本 ASIN 平均转化的词，先排除评价数量与星级、价格相对同页竞品、副图不足这三个 Listing 侧原因；三者无问题再判定词无效，写入否定或降价清单。
5. 按订单降序看：转化高但流量少的词迁入手动广告并按当前控制台做精准或词组投放，小幅上调出价观察点击是否随之增长；同一词在不同活动重复出现时合并统计后再决策。
6. 否定词选类型：否定词组拦截包含该词组及近似变体的搜索，否定精确只拦截完全一致；否定项添加后匹配类型不可改，只能新增；每行词数上限以当前控制台为准。
7. 输出待批准的变更表（迁词、否定、调价、Listing 修复各一列），批准后执行并在下一周期回读同一报告验证；同时把重复出现的搜索词按款式/颜色/型号归类，作为产品开发线索。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 搜索词分层复盘表
- 高效词迁移清单
- 否定词清单（含匹配类型）
- Listing 修复待办
- 待批准变更表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
