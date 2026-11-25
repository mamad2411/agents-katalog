---
name: sealeap-dijiang-amazon-review-mined-image-iteration
description: "Mine competitor reviews with AI assistance to surface recurring pain points and desired improvements, benchmark the main image against top competitors, validate candidate images with quick naive-viewer reaction tests, and let controlled split-test results, not internal intuition, decide which version ships. Use for 主图怎么迭代、怎么从评论里找卖点、图片该不该做分屏测试、主图要不要参考竞品. Do not use to add on-image or on-render claims and text that are not actually true of the shipped product."
---

# Amazon 评论痛点驱动主图迭代

## 目标

Mine competitor reviews with AI assistance to surface recurring pain points and desired improvements, benchmark the main image against top competitors, validate candidate images with quick naive-viewer reaction tests, and let controlled split-test results, not internal intuition, decide which version ships.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- AI批量评论摘要存在误判与遗漏，重大素材改版前应人工抽查原始评论确认摘要没有扭曲原意。
- 直觉测试样本量小、参与者背景单一，只能作为方向性参考，不能替代真实流量下的分屏测试结论。
- 主图与效果图必须与实物一致，把产品本身不具备的文字、认证或功能标识加到渲染图上属于不采用的做法，即使短期未被追责也存在合规与售后风险。
- 同等转化率下价格更高的商品更容易被平台优先展示这类因果表述属于未经证实的假设，不作为定价决策的确定依据。

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

1. 用AI辅助工具批量扫描竞品的评论内容，归纳出高频出现的抱怨点与好评点，区分材质结构类可改进项与包装说明类体验项，作为素材迭代的原始输入，而不是凭主观猜测消费者在意什么。
2. 把归纳出的真实痛点与自身产品的实际能力对照：产品本身就能解决的痛点在主图与文案里明确呈现；产品目前不具备的能力，不通过渲染图伪造出与实物不符的文字或标识来暗示具备。
3. 制作主图前用同类竞品的主图做并排对比，观察头部竞品在留白、卖点呈现方式上的共性，作为设计方向参考，而非直接照搬某一竞品的具体版式。
4. 素材定稿前找一批不了解产品背景的人做快速直觉测试：只给几秒钟看图，之后询问能否说出这是什么产品、解决什么问题，如果多数人说不出来，说明图片信息传达不清晰，需要重新设计。
5. 上线新素材后用分屏测试收集实际点击与转化数据，测试结果与内部主观判断不一致时以数据结果为准，回到上一步重新分析原因，而不是坚持看起来更好看的版本。
6. 把每一轮痛点挖掘、竞品对标、直觉测试与分屏测试结果都留痕，作为下一轮迭代的起点，避免重复测试已经验证过的方向。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：批量抓取竞品评论用于AI痛点归纳，为主图与文案迭代提供证据来源。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 竞品评论痛点/好评归纳清单
- 主图竞品对标分析
- 直觉测试反馈记录
- 分屏测试结果与迭代结论
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
