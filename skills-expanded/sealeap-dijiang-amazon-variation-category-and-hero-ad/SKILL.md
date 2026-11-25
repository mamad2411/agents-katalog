---
name: sealeap-dijiang-amazon-variation-category-and-hero-ad
description: "Judge whether multiple product variants genuinely qualify to share one Amazon listing under the category's allowed variation themes before merging them, then concentrate PPC spend on the best-converting variant as the default storefront face while the parent listing collects combined reviews. Use for 要不要把这几个商品做成变体、变体主题类目怎么选、主推哪个规格打广告、变体家族评论怎么共享. Do not use the technique of attaching a discontinued or unrelated listing as a variation purely to transfer its reviews onto a new listing."
---

# Amazon 变体类目适配与主推广告

## 目标

Judge whether multiple product variants genuinely qualify to share one Amazon listing under the category's allowed variation themes before merging them, then concentrate PPC spend on the best-converting variant as the default storefront face while the parent listing collects combined reviews.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- “是否允许合并成变体”的最终判断标准以平台当前的变体政策与类目规则为准，本条目给出的是判断思路，不能替代逐条核对官方政策。
- 把某个规格设为默认门面并集中广告资源，是一种流量分配策略，不改变其他规格本身的转化能力，若门面规格与顾客实际偏好脱节，可能压低整体家族转化，需要持续用数据复核。
- 来源中提到的“把已下架或不再销售的旧listing作为变体挂到新listing上以转移评论”的做法，本条目不采纳、不转译为可执行步骤——该做法可能违反平台关于评论真实性与商品一致性的政策，存在listing被处理的风险。
- 选择更宽泛类目以获得更大变体自由度时，需确认新类目仍准确描述商品本身，若为了变体便利而选择明显不符的类目，可能构成品类误导，带来合规风险。

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

1. 先判断候选商品是否满足“做成同一变体家族”的前提：是否本质是同一件商品、仅在颜色/尺寸等有限属性上不同，且顾客会自然期望在同一详情页里看到这些选项；如果商品之间的核心功能、目标顾客或使用场景有明显差异，应保持独立listing而不是强行合并。
2. 核实目标类目当前支持的变体主题选项（如颜色、尺寸、气味、材质、组合装等，且部分类目支持双重变体），只能在类目实际支持的属性范围内合并，不能自行定义类目未提供的变体维度。
3. 若产品线较广、想让更多规格出现在同一入口，评估是否可以通过选择更贴合、允许更宽变体范围的类目来实现（前提是新类目对该商品仍然准确、不构成品类误导），而不是为了合并而随意改类目。
4. 变体家族上线后，各子体会各自积累自己的评论并汇总展示在父体页面，这意味着新增规格可以借力已有规格积累的评论基础，规划新规格上市顺序时可以把这一点作为参考因素之一。
5. 广告资源分配上，先识别变体家族里转化率最好的那个子体，将其设为默认展示的门面规格，并把主要广告预算与出价集中在该规格上，用它承接大部分关键词流量，而不是把预算平均分给所有规格。
6. 定期用各子体的独立转化数据复核门面规格的选择是否仍然成立，若其他规格的转化数据后来居上，应重新评估是否更换主推规格与默认门面。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 变体家族适配性判断记录
- 目标类目可用变体主题核对结果
- 门面规格与广告预算分配方案
- 定期转化复核与门面规格调整记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
