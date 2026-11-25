---
name: sealeap-luduan-amazon-offsite-channel-shortlist
description: "Rank six low-cost off-Amazon traffic channels (classified listings, social and video content, journalist source platforms, email lists, forum and guest-post outreach, SEO content) by fit with the product, audience and team resources, and turn the shortlist into small pilots with measurable landing and conversion checks. Provides channel selection logic and compliance boundaries, not guaranteed traffic. Use for 站外引流有哪些免费方法、低成本站外推广、新品站外预热渠道、长尾词自制视频引流、客座文章、邮件营销值不值得做、站外 SEO 要不要做. Do not use for paid deal-site or influencer budgeting, or for any tactic that buys contact lists or manipulates search engines."
---

# Amazon 低成本站外引流渠道筛选

## 目标

Rank six low-cost off-Amazon traffic channels (classified listings, social and video content, journalist source platforms, email lists, forum and guest-post outreach, SEO content) by fit with the product, audience and team resources, and turn the shortlist into small pilots with measurable landing and conversion checks. Provides channel selection logic and compliance boundaries, not guaranteed traffic.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源提到从灰色渠道购买邮件列表和“寄生虫 SEO”（在高权重站点上铺设自建页面）作为方法，本 Skill 不采用：前者违反反垃圾邮件与隐私要求，后者属于搜索引擎可能处罚的操纵手段。
- 来源称 SEO 上下限最高、短期内即可获利并给出月收入量级；这是个案经验，本 Skill 不给收益承诺，SEO 只作为长周期渠道并以实测流量校准。
- 来源给出的分类信息站流量规模、发布有效期、邮件到达量等均为特定时点的经验值，以当前平台规则与自有监测数据为准。
- 站外点击到 Listing 的转化通常低于站内搜索流量，评估渠道价值时按站外归因口径单独统计，不与站内转化率混比。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、ASIN/SKU、产品事实与目标购买任务
- 关键词、商品投放、展示和视频的聚合表现
- 受众包定义、资格、站点限制和隐私边界
- 价格、评论、页面、库存与转化基线

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 先写清引流目标与可衡量口径：目标站点、目标 ASIN、希望承接的动作（点击到 Listing、加入邮件列表、观看评测视频）、可用人力与每周时间、是否已有品牌故事与内容素材；缺目标口径不选渠道。
2. 按渠道属性做匹配打分：分类信息站适合本地化、按地区分发且需定期续期的信息；社媒群组适合先发有信息量的软文再带入产品，直接投促销链接易被反感；视频平台适合自制视频针对长尾需求词设置标题与标签；记者信源平台适合有独特故事或新颖产品的品牌；邮件适合已有自有订阅与老客户；论坛与博客客座文章适合已能长期互动的垂直社区；SEO 内容适合能持续写作的团队。
3. 为每个入围渠道定义试点：一条内容或一次发布、承接页（Listing 或带追踪参数的落地页）、观察窗、成功指标（到达点击、停留、转化）与停止条件；一次只启一个新渠道，避免归因混淆。
4. 内容规则：软文先给读者可用的信息再引出产品；视频标题与标签围绕真实需求词而非泛词；客座文章只在与博主建立一段时间真实互动后提出，内容要对其读者有价值；所有发布注明真实身份与利益关系。
5. 邮件渠道只用自有来源的列表（官网订阅、已同意的老客户），发送前核对退订机制与到达率监测；到达率异常先停发排查，不加量。
6. 每周复盘：按渠道记录投入工时、到达点击、承接转化与合规反馈（删帖、限流、投诉），淘汰投入产出比最差的渠道，把资源集中到能稳定产出的一到两个渠道。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 渠道匹配打分表（六类渠道 × 产品/受众/资源）
- 试点计划（渠道、内容、承接页、观察窗、成功与停止条件）
- 内容规则清单（软文/视频/客座文章/邮件）
- 周度渠道复盘表（工时、点击、转化、合规反馈）
- 淘汰与聚焦决策记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
