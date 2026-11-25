---
name: sealeap-hundun-amazon-fba-shipment-label-compliance
description: "Walk through creating an FBA shipment (packing template, ship-from address, carrier selection, carton and product label printing) while checking package-dimension thresholds that trigger oversize reclassification, defaulting to the Amazon-issued barcode, and applying a pre-ship carton-label checklist to reduce avoidable receiving losses. Use for FBA 发货流程怎么走、包装尺寸超一点点有什么影响、条码用哪个码入库更顺利、外箱标签怎么贴不容易脱落、原产地标识怎么加到标签上. Do not use to decide carrier contracts or customs classification — verify current carrier and customs rules separately."
---

# Amazon FBA 发货装箱与标签合规

## 目标

Walk through creating an FBA shipment (packing template, ship-from address, carrier selection, carton and product label printing) while checking package-dimension thresholds that trigger oversize reclassification, defaulting to the Amazon-issued barcode, and applying a pre-ship carton-label checklist to reduce avoidable receiving losses.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源给出的包装尺寸阈值、派送费区间、箱体重量分界与标签尺寸均为特定时点的费用与规则摘录，需以当前物流政策与后台费用表为准，不作为固定数字长期使用。
- 标签打印设备与耗材的具体选型因人而异，本 Skill 不采纳来源推荐的具体型号，只保留热敏打印、标签内容与尺寸需与当前要求一致的判断标准。
- 多店铺共用同一联系电话或地址信息可能带来账户关联风险，仅在确认电话与地址与目标店铺注册信息一致的前提下使用，不同店铺之间不应混用联系方式。
- 使用在线工具编辑标签文件前需自行确认该工具的数据处理与隐私条款，避免上传含店铺敏感信息的文件到不可信来源；本 Skill 不指定具体工具，只描述通用做法。

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

1. 创建货件前准备发货信息：发货地址使用与本店铺绑定一致的联系电话，多店铺时切勿混用其他店铺注册的号码，避免造成不必要的信息关联；包装模板按实际外箱规格填写并注意单位换算，首次使用某箱型需新建模板并保存。
2. 核对包装尺寸阈值：标准件与大件（可能触发更高派送费）的边长与重量分界以当前费用表为准；哪怕只超出规定阈值很小的余量也可能被判定为大件从而大幅提高单件派送费，设计包装尺寸时应预留安全余量而不是卡着上限设计。
3. 条码选择与默认设置：优先选择平台颁发的条码而非制造商条码打印商品标签，可在物流设置里把默认条码来源改为平台条码，避免每次发货都要手动切换，减少因条码类型错误导致的入库问题。
4. 外箱标签张贴规范：外箱最长边与单箱重量需控制在当前规定阈值内并预留安全余量以应对运输途中箱体变形；超过重量提醒阈值的箱子需加贴多人搬运提示；标签避免用胶带整体覆盖、避免用有色胶带；建议在外箱至少两个面各贴一张标签，并避开搬运工人手部常接触的位置。
5. 产品与外箱均需体现原产地标识：若产品本身、说明书或包装上没有原产地标识，需要额外贴标或在标签制作环节加入原产地文字；若标签打印软件自带的编辑功能无法添加文字，可用通用的 PDF 编辑工具在标签文件中加入所需文字后再批量打印，并核对打印范围只覆盖需要的标签区域。
6. 发货前三重核对：让代工厂或备货仓在发货前拍照确认产品与标签一致（尤其代工厂同时为多个卖家供货时），核对产品标与外箱标没有贴错，向货代索取物流单号与预计到仓时间；中转涉及较长距离运输时，可请货代到仓后拆箱复检产品与标签状态，降低运输损耗导致的入库问题。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 货件创建信息核对表（地址/包装模板/单位换算）
- 包装尺寸阈值与派送费分级核查记录
- 条码选择与默认设置调整记录
- 外箱标签张贴与原产地标识检查清单
- 发货前三重核对记录（工厂/标签/货代）
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
