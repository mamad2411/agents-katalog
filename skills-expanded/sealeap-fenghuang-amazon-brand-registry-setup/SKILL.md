---
name: sealeap-fenghuang-amazon-brand-registry-setup
description: "Prepare and submit an Amazon Brand Registry application (US marketplace by default) with the trademark, listing, and distribution evidence it requires, then activate the unlocked brand tools—A+ Content, video, Vine, Transparency, Sponsored Brands, Stores, Brand Analytics, Attribution, and referral bonus—in a prioritized order with observation metrics. Use for 品牌备案怎么申请、备案需要什么材料、备案后能用什么功能、A+ 怎么解锁、品牌保护怎么做. Do not use to file trademarks on the user's behalf or to promise approval timelines."
---

# Amazon 品牌备案申请与功能启用

## 目标

Prepare and submit an Amazon Brand Registry application (US marketplace by default) with the trademark, listing, and distribution evidence it requires, then activate the unlocked brand tools—A+ Content, video, Vine, Transparency, Sponsored Brands, Stores, Brand Analytics, Attribution, and referral bonus—in a prioritized order with observation metrics.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 「A+ 提高转化、转化提高排名」是来源的因果链，可作假设；A+ 上线前后要控制价格、广告与库存再比较转化率。
- 新卖家激励、品牌推荐奖励、Vine 费用与名额、Transparency 免费额度等数值随政策变化，一律以当前官方页面为准。
- 品牌备案降低但不消除跟卖与侵权风险；举报需要能证明所有权与侵权事实的材料。
- 商标申请建议走正规渠道或专业代理；本 Skill 不评估商标可注册性或近似风险。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、ASIN/SKU、产品事实和当前 Listing
- 同购买意图可比竞品、价格、评论、图片和销量
- Search Term、Placement、CTR、CVR、订单、退货和利润
- VOC、Q&A、退货原因与任何页面或广告变更日志

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 先核对前置条件：商标状态（已注册或处于当前 Brand Registry 可接受的申请中状态）、商标文字或图形与包装和 Listing 一致、申请账号有对应权限。
2. 申请前先创建至少一条 Listing（可不完美），因为申请需提供品牌所在类目的代表 ASIN；同时准备品牌官网链接（可选）与产品或包装上带品牌标识的实物图片。
3. 如实填写分销信息：是否卖给分销商、销售国家或地区、是否对外授权商标；这些答案决定后续品牌保护的可用范围。
4. 提交后跟踪状态；若被驳回，按驳回原因补材料再申请，不要重复提交相同内容。
5. 通过后按优先级启用：A+ 内容与视频（转化）→ Vine（早期评论）→ Transparency 与侵权举报（保护）→ Brand Analytics 与 Attribution（数据）→ Sponsored Brands 与 Store（流量）→ 品牌推荐奖励与新卖家激励（费用回收）。
6. 把每个功能的开通状态、启用日期与首个观察指标记录成表，复盘时才能区分是功能带来的变化还是季节波动。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 备案前置条件核对表
- 申请材料清单
- 分销信息答复记录
- 功能启用优先级表
- 开通状态追踪表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
