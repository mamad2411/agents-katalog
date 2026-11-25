---
name: sealeap-qiongqi-amazon-premium-aplus-module-select
description: "Select and order Premium A+ Content modules for an Amazon listing by eligibility check, preference for image- and video-rich interactive modules, cross-sell comparison tables, and a Q&A module built from return reasons and negative reviews. Use for 高级 A+ 怎么开通、Premium A+ 用哪些模块、A+ 模块哪个没用、A+ 交叉销售、A+ 问答模块、移动端 A+ 显示. Do not use for basic A+ or Brand Story layout, or to make claims not supported by the product."
---

# Amazon 高级 A+ 模块取舍与布局

## 目标

Select and order Premium A+ Content modules for an Amazon listing by eligibility check, preference for image- and video-rich interactive modules, cross-sell comparison tables, and a Q&A module built from return reasons and negative reviews.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 开通条件、模块清单与审批周期由平台随时调整，来源描述仅代表当时情况，执行前以当前控制台为准。
- 『大部分模块无用、只用图像视频型』是来源偏好，技术型或专业受众产品可能需要规格与文字模块，按客群验证。
- 对比表交叉销售效果取决于是否有相关联的自有产品，单品牌单品时收益有限。
- A+ 内容仍受平台内容政策约束，不得放入无法证实的声明或对竞品的贬损对比。

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

1. 在 A+ Content Manager 新建时查看是否出现 Premium 区块；没有则按当前页面提示的资格条件补齐（来源提到品牌故事需覆盖全部在售 Listing、并累计一定数量已批准的基础 A+ 提交），以平台当前政策为准并记录审批周期。
2. 列出所有可用模块，按『富媒体互动 / 文本为主』分类：优先全幅图片、全幅视频、热点图、方案轮播、图片轮播、视频图片轮播；文本模块、单图配文、背景图加文字、技术规格（非专业品）默认不用。
3. 必放一个对比表模块：优先带加入购物车按钮的版本，用于交叉推荐本品牌其他产品或变体；产品差异复杂时用带特性勾选的对比表。
4. 用退货原因与差评归纳最常见的误买与使用误解，写成 Premium Q&A 模块，目标是在下单前拦住会产生差评的错误预期。
5. 在有限模块位内排序：先痛点/使用场景，再证据与差异化，再交叉销售与问答；桌面版与移动版分别预览并独立排版，确认热点图等模块在移动端的交互正常。
6. 提交后跟踪转化率、退货率与差评率变化，作为模块取舍的证据；未见改善再替换模块而非叠加文本。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 资格核查与开通计划
- 模块取舍清单
- Q&A 内容草案
- 桌面与移动布局稿
- 上线后指标跟踪表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
