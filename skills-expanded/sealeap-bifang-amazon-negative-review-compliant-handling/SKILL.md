---
name: sealeap-bifang-amazon-negative-review-compliant-handling
description: "Triage a new negative product review on Amazon by checking whether it violates community guidelines or targets the wrong product, whether seller feedback is really about the product, and whether the reviewer shows a pattern of abuse, then route each case to the compliant removal channel, a public response or a product and listing fix while explicitly refusing manipulation tactics. Use for 差评怎么处理、差评能不能删、开 case 删差评、恶意差评申诉、店铺反馈和产品评论的区别、差评影响转化. Do not use to contact reviewers for compensation, mass-report reviews, or otherwise manipulate reviews or their ranking."
---

# Amazon 差评合规处置与根因分流

## 目标

Triage a new negative product review on Amazon by checking whether it violates community guidelines or targets the wrong product, whether seller feedback is really about the product, and whether the reviewer shows a pattern of abuse, then route each case to the compliant removal channel, a public response or a product and listing fix while explicitly refusing manipulation tactics.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源认为“首页无差评”已成伪命题、评论排序与展示存在个性化；这是观测假设，不能据此设计任何标记“有用”或操纵排序的动作。
- “大量无效访问拉低转化率进而影响 Listing 权重”是来源的因果推断，只作为拒绝多账户举报类做法的理由之一，不外推为平台算法。
- 来源提及用“种子链接”合并变体稀释差评，属于变体滥用与评论操纵，不采用。
- 移除渠道、申诉入口与 Feedback 规则随平台政策变化，以当前后台可见入口与政策原文为准。

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

1. 先量化影响再行动：记录差评出现前后同口径的会话、转化率、评分与评论基数；评论基数越小单条差评的权重越大，据此排处理优先级，而不是凭感受。
2. 判定一（内容与政策）：评论是否与本品事实不符（评的是别的商品、物流或卖家服务而非产品）或含辱骂、歧视等违反社区准则的表述；命中任一条则整理证据（截图、订单/产品对照）通过后台 case 申请移除，并记录 case 编号与结果。
3. 判定二（渠道错位）：留言出现在店铺 Feedback 但内容针对产品而非店铺服务时，按当前后台的 Feedback 移除规则申请移除；核对当前政策条款，不按记忆操作。
4. 判定三（评论人模式）：查看评论人的公开评论历史，是否存在高频差评、内容雷同、集中针对同类卖家等模式；命中则通过平台的评论滥用举报/申诉渠道提交并附模式证据；未命中则按真实反馈处理。
5. 真实反馈的处置：把差评内容归入产品缺陷、期望落差（文案/图片误导）、使用方法、物流四类；文案与图片类先改 Listing 并记录旧值，产品类进入改良清单或增加随附说明；可用官方允许的公开回复渠道回应事实。
6. 停止条件：移除申请被拒且无新证据时停止重复提交；不联系评论人、不做付费删评、不用多账户举报、不用批量标记好评“有用”把差评挤到后页，这些做法一律标记“不采用”。
7. 复盘：按周复核差评率、退货率与转化率，判断处置是否改善指标；差评持续来自同一根因时，把资源转向产品与选品改进而非评论本身。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 差评影响量化记录（前后转化与评论基数对比）
- 差评分类与处置路径判定表
- 移除/申诉提交记录（证据、编号、结果）
- Listing 或产品改进清单（含旧值与回退）
- 周度复盘结论
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
