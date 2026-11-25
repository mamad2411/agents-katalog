---
name: sealeap-jiaotu-amazon-list-price-compliance-audit
description: "Audit List Price validity and rolling promotion-day exposure against the currently published reference-price and regular-price rules rather than a specific rule version, then produce a cleanup list for unsupported reference prices and a monitoring cadence that keeps the promotion-to-regular-price day ratio inside whatever threshold is officially in effect. Reference-price display eligibility is treated as opaque and re-checked, not guaranteed by any single corrective action. Use for 划线价资格核对、List Price清理、促销天数占比监控、参考价消失排查、常规价被促销价拉低预警. Do not use to set a List Price without current supporting evidence, and do not assume any single fix restores reference-price display without re-verification."
---

# Amazon 参考价与促销天数合规审计

## 目标

Audit List Price validity and rolling promotion-day exposure against the currently published reference-price and regular-price rules rather than a specific rule version, then produce a cleanup list for unsupported reference prices and a monitoring cadence that keeps the promotion-to-regular-price day ratio inside whatever threshold is officially in effect. Reference-price display eligibility is treated as opaque and re-checked, not guaranteed by any single corrective action.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源给出的具体日期节点、天数阈值是特定规则版本的参数，实际以当前官方说明为准，规则可能已调整。
- 站外比价的具体渠道与比对方式由平台技术判定，卖家无法直接验证比对逻辑，只能确保自身定价真实一致，不能假设某个渠道价格必然被采信。
- "自然订单占比"与常规价计算的具体关系是来源解读，实际权重和计算细节未完全公开，只作为促销结构设计的参考方向，不作为精确公式。

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

1. 查阅当前官方关于参考价与常规价计算方法的最新说明，记录生效版本与判定口径（如是否要求站外可比价、站内真实成交、连续动销天数等），不沿用旧版规则。
2. 逐ASIN核对现有List Price是否有当前规则认可的依据（真实成交记录或可比对的站外价格），无依据的先移除或按真实价格重设，不以"能显示就是合规"作为判断标准。
3. 导出近期滚动窗口内的每日售价与成交记录，标记出哪些是标价、哪些是各类促销/优惠券带来的实际成交价，区分不同促销工具是否计入常规价重算口径。
4. 按当前规则统计滚动窗口内低价天数占比，对接近或超过官方阈值的ASIN提前预警，避免常规价被促销价拖低后影响后续折扣展示空间。
5. 制定促销与全价交替的节奏草案：在满足业务促销需求的同时，把低价天数控制在当前规则允许的范围内，具体天数上限以官方当前说明为准。
6. 新设List Price时，先按当前规则要求积累真实动销记录后再叠加促销；"先抬价再打折"或制造虚假参考价的做法不采用。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 参考价规则版本核对记录
- List Price合规性清理清单
- 促销天数占比监控表
- 促销与全价交替节奏草案
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
