---
name: sealeap-dijiang-amazon-price-ctr-funnel-diagnostic
description: "Diagnose whether weak ad performance stems from the impressions-to-click stage, driven by main image, price, and reviews, or the click-to-sale stage, driven by full listing content, then run price as a single controlled variable on a fixed weekly cadence tracking click-through rate, conversion rate, and absolute profit rather than click-through rate alone. Use for ACOS高到底是广告问题还是listing问题、定价要不要测试、点击率转化率怎么拆分排查. Do not use fixed click-through-rate or conversion-rate percentages as pass/fail thresholds — calibrate against this account's own category baseline."
---

# Amazon 定价点击转化漏斗诊断

## 目标

Diagnose whether weak ad performance stems from the impressions-to-click stage, driven by main image, price, and reviews, or the click-to-sale stage, driven by full listing content, then run price as a single controlled variable on a fixed weekly cadence tracking click-through rate, conversion rate, and absolute profit rather than click-through rate alone.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源给出的点击率、转化率与目标净利率数值均为示例，实际达标线因类目、客单价、竞争格局差异极大，一律以自身历史数据与同类目竞品的量级作为参照，而非固定百分比。
- 单变量测试的前提是排除同期促销、库存断货等外部干扰，测试窗口内出现这些情况应作废重测，不纳入结论。
- 主图与文案的对标竞品应基于真实存在于产品上的信息，不能通过效果图渲染出产品本身不具备的文字或标识来误导消费者，这类做法不采用。

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

1. 出现ACOS偏高或整体表现不佳时，先用漏斗拆分定位问题环节：曝光量由自然排名与广告共同带来；曝光转点击主要由主图、价格与评论决定；点击转成交主要由五点、详情图、视频、品牌故事、加强型内容与追评内容决定。
2. 点击率明显偏低时优先检查主图与价格而不是急着调广告出价；转化率明显偏低但点击率正常时优先检查详情页内容与评论质量而不是加大广告预算。
3. 需要测试定价时把价格设为单一变量，固定一个可判断趋势的周期，期间不同时改动主图或核心文案，避免多个变量同时变化导致无法归因。
4. 每个测试周期结束后同时记录点击率、转化率与实际到手利润三项指标，而不是只看点击率或只看转化率：点击率与转化率同时下降但利润因客单价提高而上升时，视为该轮测试的正向结果。
5. 按利润结果决定下一步：利润提升就保留当前价位或按相同方向再微调一档；利润下降就回退到上一价位，再尝试相反方向的调整，不要连续大幅跳价。
6. 全程使用自己的账户与类目数据判断什么样的点击率、转化率算好，不套用外部经验值作为达标线。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 曝光-点击-转化漏斗诊断记录
- 单变量定价测试日志（价格/点击率/转化率/利润）
- 定价调整结论与下一轮测试计划
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
