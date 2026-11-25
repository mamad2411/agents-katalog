---
name: sealeap-taotie-amazon-fba-first-leg-freight-selection
description: "Choose an FBA first-leg freight option by mapping time, cost and risk across sea-express, sea-truck, direct fast vessel, slow consolidated vessel and air-plus-local-delivery, then verify destination region, sailing code, chargeable-weight formula, insurance, customs documents, pallet specs and the bill of lading before booking. Forwarder terms are compared, not endorsed. Use for 头程怎么选、海派海卡区别、快船普船正班加班、空派和商业快递区别、甩柜是什么、双清包税、HS 编码、体积重怎么算、要不要打托盘、货丢了怎么理赔、账期怎么谈. Do not use to recommend a specific forwarder or to file customs declarations on the seller's behalf."
---

# Amazon FBA 头程物流渠道选择与风险核对

## 目标

Choose an FBA first-leg freight option by mapping time, cost and risk across sea-express, sea-truck, direct fast vessel, slow consolidated vessel and air-plus-local-delivery, then verify destination region, sailing code, chargeable-weight formula, insurance, customs documents, pallet specs and the bill of lading before booking. Forwarder terms are compared, not endorsed.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 各渠道的天数、每公斤单价、赔付标准均为来源当时的经验值，随季节、航线与货代变化，只作比较框架，不作预期承诺。
- 「便宜渠道必然甩柜」「大公司时效最稳」是来源的经验概括，属待验证假设；用同一批次不同渠道的实际到仓记录校准。
- 来源点名的船公司与货代推荐不采纳；本 Skill 只保留可验证的判断标准（航线代码、停靠码头、赔付条款）。
- 双清包税是否含全部税费、清关资料要求随目的国政策变化，需每票与货代书面确认。

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

1. 先定约束：到仓截止日期（旺季补货或首发）、货值、体积重与实重、是否含电池等敏感属性；创建货件后读取目的仓编码判断美西/美中/美东，区域越远时效与费用越高。
2. 读懂报价表术语：海派 = 海运 + 末端快递（通常含双清包税，到港后清关放行快）；海卡 = 海运 + 卡车派送（通常不含税，末端需预约，成本最低）；快船 = 固定航线直航少停靠，普船 = 拼船多停靠且旺季易延误；正班与加班船的差别常在停靠码头与卸货速度；空派 = 空运 + 目的国本地派送，通常比商业快递省关税与附加费。
3. 按风险清单核对每个报价：低价渠道的甩柜/甩货风险、拼柜同柜敏感货导致的查验连带风险、旺季港口拥堵、清关资料（商业发票、电池等认证）是否齐全；把每项风险写成「谁承担、怎么赔」。
4. 要求货代提供船公司航线代码与跟踪方式，用代码验证其宣称的快船/正班是否属实；把承诺时效写入合同并核对延误赔付条款（来源见过按公斤按日计赔的条款）。
5. 核算计费重量：目的国平台按英寸立方除以系数得磅，国内货代按厘米立方除以 5000 或 6000 得公斤，两者系数不同，先问清货代用哪种；超过当前托盘/整车阈值时选择对应承运方式。
6. 决定是否打托盘：托盘降低破损率但计入托盘体积；尺寸、堆叠高度与四周留边按当前入库要求，托盘外贴货件标签；准备 HS 编码（前六位国际通用，后几位按目的国）与提货单 BOL，用于清关和少件理赔。
7. 货值高或首发批次投保（按申报价值比例理赔）；形成「渠道、时效、费用、风险承担、保险、资料」六列的比较表后再下单，收货后回读上架数量与签收记录，差异按 BOL 与保险条款处理。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 头程约束与目的仓区域记录
- 渠道术语与风险对照表
- 报价比较表（时效/费用/风险承担）
- 计费重量与托盘方案
- 清关资料、保险与 BOL 清单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
