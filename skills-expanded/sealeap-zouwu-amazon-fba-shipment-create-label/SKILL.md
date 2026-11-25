---
name: sealeap-zouwu-amazon-fba-shipment-create-label
description: "Convert a merchant-fulfilled offer to FBA and build the first inbound shipment in Seller Central: verify packing template units, prep and labeling owner, carrier path, shipment splits, SKU and carton labels, then fill tracking IDs and read back shipment status. Field names follow the current console. Use for FBA 发货流程、FBM 转 FBA、创建货件、装箱模板怎么填、SKU 标签和箱标打印、货件追踪码怎么填、贴标方怎么选. Do not use to negotiate a forwarder's commercial terms or to prepare customs declarations beyond the label content."
---

# Amazon FBA 首票货件创建与贴标核对

## 目标

Convert a merchant-fulfilled offer to FBA and build the first inbound shipment in Seller Central: verify packing template units, prep and labeling owner, carrier path, shipment splits, SKU and carton labels, then fill tracking IDs and read back shipment status. Field names follow the current console.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 平台贴标每件收费、货件拆分数量与配置费规则、送达时段等数值随站点与政策变化，来源经验值仅作参考，以当前控制台报价为准。
- 标签贴法（每件一张、外箱多面）与原产地标注要求应按当前 FBA 入库要求和目的国海关规定复核，不作固定规律。
- 卡派无追踪码时回填货代参考号是来源做法，当前系统是否接受需在保存后回读确认。

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

1. 在库存管理中确认该 SKU 当前的配送方式（可编辑数量栏通常代表卖家自配送），通过编辑入口执行转换为亚马逊配送，先按实际回答危险品信息问卷再发布为 FBA 商品；入口名称以当前控制台为准。
2. 进入发货流程后核对发货地址与目标商城；首次创建装箱模板时记录每箱件数、箱规与重量，单位按站点核对（美国站英寸/磅，欧洲站厘米/千克），保存后模板可复用。
3. 预处理与贴标方按实际选择：产品无需预处理时明确标注；贴标方默认由卖家自贴，选平台贴标前先核对当前每件收费并与自贴成本比较。若提示缺少单品尺寸重量，回到商品信息补齐后重试。
4. 填写箱数与总件数后进入承运人选择：平台合作承运与自找货代两条路径按签约状态选；货件被拆到多个目的仓时先核对拆分数量与配置费提示，再确认送达时段并接受费用。
5. 打印 SKU 标签与箱标：格式按所购标签纸或热敏打印机的实际规格选择，份数与件数/箱数一致；SKU 标每件一张贴在产品外包装可扫描处，箱标按当前入库要求贴在外箱多个面，标签上补充原产地信息以满足清关要求。
6. 货代提供唛头与内部编号后贴于外箱，发出后把快递单号或货代参考号回填到货件追踪码栏；多货件时用表格批量上传。
7. 回读货件状态：确认货件编号、件数、箱数、承运信息与追踪码已保存并处于预期状态，异常记入待办。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- FBA 转换与货件创建核对表
- 装箱模板与贴标方案
- 标签打印与贴标清单
- 追踪码回填与货件回读记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
