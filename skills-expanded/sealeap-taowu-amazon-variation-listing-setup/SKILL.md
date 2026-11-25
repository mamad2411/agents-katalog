---
name: sealeap-taowu-amazon-variation-listing-setup
description: "Set up or extend a parent-child variation family in Seller Central: choose the variation theme and attribute display order, name child attributes with matching color and size maps, assign a unique product ID and a readable seller SKU per child, then verify price, condition and inventory settings for FBA versus FBM before saving. Produces a child-level fill sheet and a post-save verification list. Use for 怎么加变体、父子体怎么建、颜色尺码变体设置、每个变体要不要单独 UPC、变体主题选哪个、变体 SKU 命名. Do not use to merge or split existing ASINs into variations that violate category variation policy, and do not use for variation ad structure."
---

# Amazon 变体 Listing 搭建

## 目标

Set up or extend a parent-child variation family in Seller Central: choose the variation theme and attribute display order, name child attributes with matching color and size maps, assign a unique product ID and a readable seller SKU per child, then verify price, condition and inventory settings for FBA versus FBM before saving. Produces a child-level fill sheet and a post-save verification list.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- “变体越多转化越高”是来源的经验判断；变体增加也带来条码、库存与滞销成本，扩展范围按自家转化与库存证据决定。
- 每个子体是否必须有独立 UPC/EAN 取决于当前品牌备案与条码豁免政策，按站点当期规则核对，不以来源说法为准。
- 变体主题的可选项与字段随类目和站点变化，界面式步骤会过时，以当前上架页面字段为准。
- 把不相关产品硬拼成变体属于违规做法，不采用。

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

1. 先确认变体是否成立：子体必须是同一产品在颜色、尺码、数量、材质等属性上的差异，且目标类目允许该变体主题；不同产品、不同用途或类目禁止的组合不做变体。
2. 选变体主题与展示顺序：单一属性选对应主题；双属性时按顾客决策顺序决定先选什么（如先尺码后颜色），以可比 Listing 的做法和自家转化证据校准。
3. 整理子体属性表：每个子体给顾客可读的属性名，同时填写平台标准的颜色/尺码映射值，保证筛选与搜索能识别；创意命名不能替代标准映射。
4. 为每个子体准备唯一产品 ID（UPC/EAN 或已获豁免的方式）和可读的 Seller SKU 命名规则（如 产品-尺码-颜色），并留存子体与条码的对应表，避免后续贴标与库存混乱。
5. 逐子体填写状况、价格与库存：价格可按子体差异化但要复核利润；FBM 填真实可售数量，FBA 的数量以到仓接收为准；保存前逐行核对无空缺。
6. 保存后回读：父页面是否正确聚合、各子体是否可购买、图片与属性是否对应；出现子体脱离父体或属性错位时按平台的变体修正流程处理并记录。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 变体可行性判断（属性差异、类目主题、政策依据）
- 子体填写表（属性名、颜色/尺码映射、产品 ID、Seller SKU、价格、库存）
- 变体主题与展示顺序建议
- 保存后核对清单与异常处理记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
