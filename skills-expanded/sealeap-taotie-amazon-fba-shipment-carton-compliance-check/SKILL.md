---
name: sealeap-taotie-amazon-fba-shipment-carton-compliance-check
description: "Walk a new FBA inbound shipment through hazmat and battery declaration, prep ownership, packing type, quantity consistency, carton size and weight limits, carton sturdiness and shipment-label placement, reading back each field against the current Seller Central workflow before the cartons leave the factory. Use for FBA 货件怎么建、带电池要不要申报、预处理方选谁、混装还是原厂包装、外箱尺寸限制、箱子被压变形多收费、箱标和快递单区别、轻小商品计划条件. Do not use for first-leg forwarder selection or customs paperwork, and never to game split-shipment allocation by misreporting quantities."
---

# Amazon FBA 货件创建与外箱合规自检

## 目标

Walk a new FBA inbound shipment through hazmat and battery declaration, prep ownership, packing type, quantity consistency, carton size and weight limits, carton sturdiness and shipment-label placement, reading back each field against the current Seller Central workflow before the cartons leave the factory.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源提到「多发少发不会被处罚」并以此规避分仓，属于利用规则漏洞的做法，本 Skill 不采用；数量不一致会触发预处理费与入库延迟，且规则随时可能收紧。
- 预处理费、数量不符处理费、外箱尺寸重量阈值、轻小商品计划的费用与上限都是随季节与政策变化的数值，来源数字仅作参考，以当前控制台与帮助页为准。
- 「箱子压变形导致按更大尺寸计费」是来源对费用差异的解释，属可验证假设；出现费用差异时先申请平台重新测量再下结论。
- 来源中关于多账号共用海外仓是否关联的说法不转译；账号关联问题不在本 Skill 范围。

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

1. 创建货件前如实完成危险品信息：含任何电池（含纽扣电池、干电池）、气溶胶、腐蚀性清洁剂等商品按当前问卷申报，并让 Listing 描述与实际配置保持一致；申报口径以当前控制台为准。
2. 选择预处理方与贴标方时默认由卖家在国内完成（气泡膜、塑料袋、贴标、套装标识等），先读取当前平台预处理的每件收费再决定是否外包；套装商品用外盒加「作为一件销售」类标识，让入库按一个 SKU 计数。
3. 按货件内容选装箱类型：多个 SKU 或不同状况的商品选混装，单一 SKU 全新商品选原厂包装；逐 SKU 填写发货数量，并让创建数量与实际装箱数量一致，不用多发少发来规避分仓。
4. 核对外箱限制：单箱最长边、单箱重量、单件超尺寸的当前阈值在帮助页读取；箱内留缓冲与角部支撑并选用结实纸箱，避免运输中压扁使测得尺寸超限而被按更高档位计费。
5. 填写箱数、每箱件数、箱重与尺寸并打印箱标：箱标是平台生成的货件标签，与承运人快递单是两种标签，每个外箱都要贴；大箱套小箱时只在最外箱贴唯一箱标；外箱标签纸选质量更好的规格并可加透明胶带保护。
6. 计算物流与配送费时把平台出库时可能再套外箱的重量增量计入，用发货前的预估费用与自算值对照；差异大时记录并在入库后核对实际收费。
7. 低单价小件商品评估轻小商品类计划资格：先把包装尺寸重量在 Listing 中填全，再按当前项目条件（尺寸、重量、价格上限、全新）判断；货件发出后回读状态，异常（数量不符、拒收、破损）按类型记入待办。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 危险品与电池申报记录
- 预处理与装箱方案
- 外箱尺寸重量自检表
- 箱标打印与贴标清单
- 货件回读与异常待办
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
