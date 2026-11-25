---
name: sealeap-suanni-amazon-fba-shipment-labeling
description: "Walk through creating an FBA inbound shipment plan from a verified carton specification, choose the shipment split and transport mode on total landed cost rather than defaults, and verify unit, carton and compliance labels before cartons are handed to the forwarder. Use for FBA 发货流程、创建货件、FNSKU 标签、外箱标签、货件拆分怎么选、入库配置费、送达时间窗、发货地址填什么、超重标签. Do not use to bypass Amazon inbound requirements or to misstate the ship-from location in order to influence warehouse allocation."
---

# Amazon FBA 货件创建与贴标核对

## 目标

Walk through creating an FBA inbound shipment plan from a verified carton specification, choose the shipment split and transport mode on total landed cost rather than defaults, and verify unit, carton and compliance labels before cartons are handed to the forwarder.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源提到的送达容错天数、拆分方案的最低箱数、每页标签张数、超重阈值都是某一时期的后台规则，以当前货件创建页面的实时提示与站点政策为准。
- “分仓免入库配置费更划算”是经验倾向而非规律；每批按实际箱数、目的仓分布与货代报价算总成本后再选。
- 来源提到过去有卖家填目的国地址以争取分到特定仓库，属于虚报起运地，不采用；发货地址按真实起运地填写。
- 标签版式、危险品问卷、承运人选项与页面入口会随后台改版变化；本 Skill 只提供顺序与核对项，不替代官方入库指南。

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

1. 创建前先备齐事实：SKU 已转为亚马逊配送、危险品/电池/管制问卷已如实填写、外箱实测尺寸与重量（按后台要求的单位与取整）、每箱装数、总箱数、货代提货或到仓日期；缺任何一项先补齐再进后台。
2. 发货地址填真实起运地（如国内实际发货地址），不填目的国地址；后台按起运地给出的预计送达容错窗口不同，以当前页面提示为准，并据此倒排货代提货时间。
3. 包装方式按实际选择：单一 SKU 整箱选单一商品箱并保存箱规模板复用；多 SKU 混装选混装并逐箱申报内容；箱规模板保存后，后续同款补货只需改箱数。
4. 货件拆分方案（分到多仓 vs 集中一两仓）不按默认选：分仓通常免或降低入库配置费但头程可能拆成多段变贵，集中入仓则相反；用本次箱数与货代报价算总成本后再选，并核对该方案的最低箱数要求。
5. 运输方式与承运人按实际：散箱走小包裹、托盘走 LTL；不用平台合作承运人时，空运填实际承运商、海运选“其他”并说明船运；送达窗口按货代时效如实填，窗口内未到会留下绩效记录，因此宁可保守。
6. 提交后下载两类标签并核对：商品级 FNSKU 标签（新品条件用站点语言表述、含原产地标识、每个单品一张）与货件级外箱标签（按分配的目的仓分别打印，同一目的仓内同规格箱可复用，每箱至少贴两个相邻侧面）；核对箱数与标签数一致、目的仓代码与货代面单一致。
7. 补齐合规标签后再交货代：外箱与商品都要有原产地标识，超过站点重量阈值的箱子加多人搬运/超重标签，玩具等特定品类加对应警示标签；交货后在货件里回填追踪号，到仓后核对接收数量与差异。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 货件创建前置检查表（SKU 状态、问卷、箱规、日期）
- 货件拆分与运输方式成本对比
- 标签清单与贴标核对记录（FNSKU、外箱、目的仓）
- 合规标签需求清单（原产地、超重、品类警示）
- 追踪号回填与到仓核对记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
