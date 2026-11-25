---
name: sealeap-feilian-amazon-jp-safety-compliance-check
description: "Verify current Japan-marketplace product-safety regulatory requirements (import-responsibility scope, in-country administrator designation, technical-file and labeling retention) directly against official regulator guidance and Seller Central before listing or restocking affected categories. Treats category-risk severity and preparation effort as assumptions to confirm against the account's own product scope and the currently effective rule version. Use for 日本站产品安全法规资格核对、国内管理人配置确认、技术文件与标签留存自查、受影响品类结构评估、新建ASIN合规信息准备. Do not use to assume a category is exempt, or that a past compliance setup still satisfies the current regulation version, without rechecking official guidance."
---

# Amazon 日本站产品安全合规自查

## 目标

Verify current Japan-marketplace product-safety regulatory requirements (import-responsibility scope, in-country administrator designation, technical-file and labeling retention) directly against official regulator guidance and Seller Central before listing or restocking affected categories. Treats category-risk severity and preparation effort as assumptions to confirm against the account's own product scope and the currently effective rule version.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源列出的具体生效日期、品类范围与责任划分细节属于特定修订版本，规则可能随后续公告调整，一律以监管机构与卖家后台当前发布的版本为准，不作为长期规则假设。
- 国内管理人的具体资质要求与是否强制配置，可能因品类与业务规模存在差异，需以官方最新说明和自身实际情况核实，不直接套用单一标准。
- 品类去留与合规成本高低的判断因供应链与产品结构而异，来源对品类风险的归纳是其解读，需按自身实际合规工作量重新评估，不作为强制退出依据。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- 目标 marketplace、类目、价格带、上架时间与运营模式
- 候选品与同购买意图可比样本的销量、评论、价格和上架时间
- 关键词需求、历史趋势、广告依赖、同款密度和品牌集中度
- 采购、头程、平台费、退货、仓储、交期和合规/IP 基础信息

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 对照官方监管公告与卖家后台合规提示，核对自身在售或计划上架品类是否落入受规管的商品安全类别（如含电源、含电池、涉燃气或儿童相关品类），记录当前规则版本与生效状态，不沿用旧版本印象。
2. 确认作为进口方需承担的责任范围是否已变化（是否需自行承担原本由本土进口商分担的义务），并明确是否需要配置符合条件的国内管理人（有当地地址、可代表卖家与监管机构沟通）。
3. 盘点受影响品类当前的技术文件、检验记录与合格证明是否齐全、是否满足留存年限要求；核对标签内容是否按最新要求更新，缺失项列出清单并标注负责人与补齐时限。
4. 检查新建ASIN与补货流程中是否已加入合规信息提交节点（如国内管理人信息），确认缺失该信息是否会阻断新品发布或补货，避免临上架前才发现流程卡点。
5. 对受影响品类做结构评估：区分合规成本可控、可继续运营的品类，与合规成本过高、需考虑收缩或退出的品类，形成品类去留的初步清单。
6. 设定规则版本更新时的复核节点，定期跟踪监管公告与后台提示的变化，避免下一次规则调整时错过准备窗口。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 受规管品类与规则版本核对记录
- 国内管理人配置与责任范围确认单
- 技术文件与标签留存缺口清单
- 新建ASIN合规节点检查表
- 品类去留初步评估表
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
