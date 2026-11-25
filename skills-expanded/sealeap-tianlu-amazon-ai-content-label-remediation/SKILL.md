---
name: sealeap-tianlu-amazon-ai-content-label-remediation
description: "Verify the current official disclosure requirement for AI-generated or AI-modified marketing imagery and copy (scope, effective date, and which listing surfaces it covers) before acting, then tier existing assets by disclosure risk and route new uploads through a standard labeling checklist. Assumes the specific label format, penalty schedule, and exemptions are re-checked each cycle from Seller Central and official regulatory text rather than carried over from a prior review. Use for 新增素材上传前标注核查、存量图片视频 AI 标注整改、跨站点 AI 披露规则确认. Do not use to assume a jurisdiction's disclosure rule, exemption, or penalty amount still applies without checking the current official text for the account's actual marketplaces."
---

# Amazon AI生成素材标注核验

## 目标

Verify the current official disclosure requirement for AI-generated or AI-modified marketing imagery and copy (scope, effective date, and which listing surfaces it covers) before acting, then tier existing assets by disclosure risk and route new uploads through a standard labeling checklist. Assumes the specific label format, penalty schedule, and exemptions are re-checked each cycle from Seller Central and official regulatory text rather than carried over from a prior review.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 具体处罚金额、抽检方式与豁免情形来自单一来源总结，未逐一核实官方原文，执行前必须以当前官方法规文本与卖家后台说明为准。
- 不同站点、不同法规版本对 AI 生成内容的定义与标注要求可能不同，不能把某一地区的规则直接套用到其他站点。
- 素材是否构成 AI 生成有时边界模糊（如仅用 AI 做背景替换），判定从严处理，存疑素材归入高风险优先整改而非默认豁免。

## 先判断任务模式

1. **诊断**：读取现状、证据和缺口，不生成线上写入动作。
2. **方案草案**：输出可审核的结构、参数范围、实验和回退值。
3. **执行准备**：只生成待批准变更表或 API/控制台操作草案。
4. **已批准执行**：仅对用户在当前会话明确批准的对象和字段执行，并立即回读核验。

用户未指定时采用“诊断”。

## 开始前要拿到

- 目标 marketplace、产品事实、品牌语气和当前政策约束
- 已授权的 Listing、关键词、评论/VOC、图片和竞品证据
- 每项数据的来源、时间、站点、样本和限制
- 人工审核人、发布边界和不可生成的声明或视觉特征

缺失项必须标为 `NEEDS_EVIDENCE`；不得猜数字、补属性或把不同站点、ASIN、变体、币种和时间窗混在一起。

## 工作流

先读取 [references/playbook.md](references/playbook.md)，确认该方法适用于当前对象。按以下顺序执行：

1. 核对账户实际经营站点当前适用的 AI 生成内容披露规则原文（官方法规文本与亚马逊后台政策说明双向核对），记录管辖范围、生效日期与是否已在本账户站点落地执行。
2. 逐条核对当前上传流程中是否已包含 AI 生成内容的标注勾选或字段，确认哪些内容类型（主图、A+、视频、帖子、广告素材等）被纳入范围，哪些明确豁免（如纯实拍、传统调色裁剪）。
3. 对存量素材按当前规则定义的触发条件分类（如是否用了 AI 生成人物、场景或模特换脸），标出高风险素材优先整改。
4. 按当前规则要求的标注位置与格式逐一补标或重新上传，已有官方勾选入口的渠道（如 A+ 内容）优先处理，因为操作成本最低。
5. 对暂停投放或零曝光的历史素材评估是否值得整改或直接下线，避免把整改资源花在已无展示价值的内容上。
6. 建立新增素材的标准化标注检查点，纳入上新/上传流程，并设定下一次官方规则复核的时间点，不假设本次核对结果长期有效。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 适用规则核对记录（管辖范围/生效日期/覆盖内容类型）
- 存量素材风险分级清单
- 标注补齐执行记录
- 新增素材标注检查点与下次复核时间
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
