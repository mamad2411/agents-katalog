---
name: sealeap-tianlu-amazon-variation-compliance-audit
description: "Audit existing and planned parent-child variation structures against the current official variation policy (allowed merge scenarios, maximum variation dimensions, and parent/child title and attribute consistency rules) read directly from Seller Central rather than a remembered rule set, flag merges that resemble known risk patterns (version or model differences, mismatched core attributes, disguised multi-packs, dormant or previously-flagged listings), and route confirmed violations through the platform's remediation and appeal path. Produces a compliance gap list, not a guarantee against system-triggered splits. Use for 变体合并前合规预检、已合并变体排查、变体拆分后申诉材料准备. Do not use to merge listings based on a remembered rule of thumb without checking the current official variation policy for the account's actual category."
---

# Amazon 变体合并合规排查

## 目标

Audit existing and planned parent-child variation structures against the current official variation policy (allowed merge scenarios, maximum variation dimensions, and parent/child title and attribute consistency rules) read directly from Seller Central rather than a remembered rule set, flag merges that resemble known risk patterns (version or model differences, mismatched core attributes, disguised multi-packs, dormant or previously-flagged listings), and route confirmed violations through the platform's remediation and appeal path. Produces a compliance gap list, not a guarantee against system-triggered splits.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 允许的最大变体维度数、具体合并适用场景等属于平台可调整的政策细节，来源总结的具体数字与条款仅作排查方向，执行前以当前官方变体政策文本为准。
- 违规后果的具体分级来自来源观察总结，未经官方文本逐条证实，实际处理结果以账户收到的实际系统提示或通知为准。
- 通过合并继承评价等操纵性操作不应采用，一经识别应主动拆分整改，而不是寻找规避检测的方法。

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

1. 核对当前官方变体政策原文中的合并适用场景与不适用场景说明，以及每个父体允许的最大变体维度数，不依赖既往经验或旧规则印象。
2. 逐一核对计划合并或已合并的父子体：子体的核心属性（型号、材质、款式等）是否与父体描述一致，是否存在版本迭代、不同款式类型被强行归入同一父体的情况。
3. 核对父体标题是否包含具体变体值、子体标题主体是否与父体完全一致（差异仅体现在变体属性值上），标出命名模糊或不一致的子体。
4. 核对选用的变体主题是否与实际区分维度精确对应，并核对是否存在把评价通过合并继承到新链接等已知高风险操作。
5. 排查历史链接：是否有失效、零流量或曾因变体问题被处理过的链接混入当前变体结构，若有先评估是否应在合规排查中一并拆分清理。
6. 对确认违规的变体，先按官方提示完成自行拆分或整改；如已收到绩效警告，再准备产品真实信息证明与整改说明发起申诉，同时排查店铺内其他产品是否存在同类风险。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 变体政策核对记录（合并场景/维度上限/生效版本）
- 父子体一致性排查清单
- 高风险操作与历史链接排查记录
- 违规整改与申诉材料准备清单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
