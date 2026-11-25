---
name: sealeap-tianlu-amazon-saudi-vat-withholding-response
description: "Determine whether a seller's actual Saudi-marketplace sales activity currently triggers Saudi VAT registration or platform withholding, verify requirements directly against official ZATCA and Amazon seller-console sources, and track registration and filing-calendar execution. Does not calculate a specific tax or penalty amount. Use for 沙特站VAT代扣代缴自查、注册材料与流程核对、申报日历搭建、代扣异常排查. Do not use to determine final tax liability or to replace a local Saudi VAT advisor's opinion."
---

# Amazon 沙特VAT代扣代缴应对

## 目标

Determine whether a seller's actual Saudi-marketplace sales activity currently triggers Saudi VAT registration or platform withholding, verify requirements directly against official ZATCA and Amazon seller-console sources, and track registration and filing-calendar execution. Does not calculate a specific tax or penalty amount.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 文中列出的具体税率、注册门槛金额、罚款比例与豁免条件为该时间点信息，规则可能调整，操作前必须以官方最新公告为准。
- 平台代扣机制的触发条件与执行细节由平台与当地税务机关共同决定，具体扣缴逻辑以官方说明与账户实际扣款情况为准，不应假设与其他站点规则一致。
- 是否需要注册、能否享受过渡期减免属于属地税务判断，需由熟悉当地VAT规则的顾问或代理确认，本流程仅用于自查触发条件与准备材料。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- 目标 marketplace 与案例 ASIN 的明确时间范围
- 销量、评论、价格、促销、变体和上架时间线
- 关键词自然/广告可见度、品牌与站外流量代理证据
- 可复核来源、数据口径、缺失项和替代解释

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 核对本账户在沙特站的实际经营方式（自发货、海外仓或FBA）与销售规模，对照沙特税务机关当前公开的VAT注册门槛判断是否已触发注册义务，不以境内销售规则类推。
2. 直接从沙特税务主管机关官网或亚马逊官方卖家后台公告确认当前的注册流程、所需材料清单与截止时间，不依赖二手转述的材料清单。
3. 核实店铺后台登记的店铺名称、主体信息与拟提交的VAT注册材料完全一致，避免因信息不匹配导致注册被拒或后续被平台判定为未注册。
4. 注册完成后核实当前的申报周期（按季度或按月，门槛以官方最新标准为准）并建立对应的申报日历，避免逾期触发滞纳金或罚款。
5. 若注册涉及政策生效日与实际完成注册之间的缺口期，核实是否存在过渡期或减免政策及申请条件，由具备资质的当地税务顾问确认是否适用。
6. 持续监控平台是否已开始代扣及扣款比例是否与预期一致，发现扣款异常及时联系平台与税务顾问核实原因。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- VAT注册触发条件核查记录
- 官方注册材料清单与进度跟踪表
- 申报日历
- 扣款异常核对记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
