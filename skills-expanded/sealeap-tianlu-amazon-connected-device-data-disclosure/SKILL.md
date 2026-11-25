---
name: sealeap-tianlu-amazon-connected-device-data-disclosure
description: "Determine whether any of the account's currently listed connected or smart devices fall inside a data-transparency regulation's current scope by checking the official text directly (covered product categories, data-holder obligations, and effective date), then map each in-scope product's user-facing disclosure gaps against what the rule currently requires. Produces a compliance gap list rather than a legal conclusion on the account's actual liability. Use for 联网/智能设备数据披露合规核对、新规适用范围判断、产品说明与隐私披露文案缺口排查. Do not use to draft or finalize legally binding disclosure text without qualified legal review of the account's specific product and marketplace."
---

# Amazon 联网设备数据披露核对

## 目标

Determine whether any of the account's currently listed connected or smart devices fall inside a data-transparency regulation's current scope by checking the official text directly (covered product categories, data-holder obligations, and effective date), then map each in-scope product's user-facing disclosure gaps against what the rule currently requires. Produces a compliance gap list rather than a legal conclusion on the account's actual liability.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 法规覆盖的具体产品类别、义务细节与生效安排可能存在多个版本或过渡期，必须以官方最新文本为准，来源总结仅作排查起点。
- 本流程只产出合规缺口清单，不构成法律意见；产品是否真正适用、披露文案是否合规需由具备资质的法律顾问最终确认。
- 不同产品线（消费类设备/工业设备/配套数字服务）适用条款可能不同，不能用同一份披露模板不加区分地套用全部产品。

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

1. 直接核对相关数据透明度法规的官方原文（而非二手解读），确认其管辖地域范围、生效日期版本与数据持有者义务的定义。
2. 逐一核对账户在该管辖范围内销售的产品是否属于覆盖范围内的联网/智能设备或配套数字服务类别，标出适用与不适用的产品清单。
3. 对已确认适用的产品，核对当前产品页、说明书或配套服务中是否已披露数据类型、存储方式、访问方式、处理目的与第三方共享情况，逐项列出缺口。
4. 针对披露缺口，起草需要补充的披露要点（不替代法律文本），标注每一项披露内容对应的信息来源（研发/产品/隐私团队）以便核实准确性。
5. 将本次核对结果与草拟披露要点提交给具备资质的法务或合规顾问复核后再对外发布，不把自行起草的文案直接视为合规达标。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 法规适用范围与生效日期核对记录
- 在售产品适用性清单
- 用户数据披露缺口清单
- 待法务复核的披露要点草稿
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
