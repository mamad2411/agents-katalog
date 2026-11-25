---
name: sealeap-zouwu-amazon-fba-mixed-carton-shipment
description: "Build an FBA inbound shipment where several SKUs share cartons: switch from single-SKU packing templates to mixed cartons, allocate units per carton so totals reconcile, enter per-carton dimensions and weights, handle console warnings, and estimate chargeable weight from the greater of actual and volumetric weight. Uses the current Send to Amazon workflow. Use for FBA 混装发货、一箱装多个 SKU、Web 表单填箱内数量、箱数超限用表格上传、抛重怎么算、体积重和实重取大. Do not use for single-SKU original-carton shipments or to decide freight rates without the forwarder's actual quote."
---

# Amazon FBA 混装货件分箱与抛重核算

## 目标

Build an FBA inbound shipment where several SKUs share cartons: switch from single-SKU packing templates to mixed cartons, allocate units per carton so totals reconcile, enter per-carton dimensions and weights, handle console warnings, and estimate chargeable weight from the greater of actual and volumetric weight. Uses the current Send to Amazon workflow.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 体积重换算系数（来源海运与空运各有常用值）以当前货代报价单为准，不作固定常数。
- 单次可在 Web 表单录入的箱数上限随控制台版本变化，以当前界面提示为准。
- 「箱体贴合可省运费」需用实际报价对比验证，箱规也要满足入仓与产品保护要求。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- marketplace、ASIN/SKU、库存阶段、补货与到仓时间
- 断货或备货前后的销量、流量、广告、自然位置和转化基线
- COGS、头程、仓储、平台费、退货和清仓成本
- 可比产品的成熟度、销量区间和需求趋势

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 选中要一起入仓的多个 SKU 发起补货，在包装设置中把默认的单 SKU 原装箱模板改为混装商品，并为每个 SKU 设置预处理与贴标方；入口名称以当前控制台为准。
2. 先填每个 SKU 的总件数，再声明需要多个包装箱；箱数在当前 Web 表单允许范围内直接填，超过则按提示下载表格批量填写。
3. 逐箱分配：每箱中各 SKU 数量之和必须与该 SKU 总件数一致，任何一箱不能为空；各箱尺寸与重量按实际分别填写，不同箱规分开录入。
4. 系统弹出警告时先读内容：属于抛重或箱规提示则核对尺寸后确认，属于数量不一致则回到分配表修正，不盲目忽略。
5. 头程计费预估：分别算实重与体积重（长×宽×高 ÷ 货代给定的体积系数，海运与空运系数不同），取大者作为计费重量；箱体尽量与产品贴合以减少抛重。
6. 确认并继续后回读货件：箱数、每箱内容、总重与承运信息与分配表一致，差异记入待办。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 混装分箱分配表
- 逐箱尺寸重量清单
- 计费重量预估表
- 货件回读核对记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
