---
name: sealeap-dijiang-amazon-inbound-ip-claim-response
description: "When receiving a trademark or copyright infringement claim against a listing, verify the claimant's actual registered rights rather than assuming a mark is too generic to be owned, weigh contesting versus complying based on exposure and resources, and if complying, negotiate explicit sell-through and reinstatement terms while confirming the supplier actually implements the redesign going forward. Use for 收到商标投诉怎么办、版权投诉要不要认、被下架了商标问题怎么恢复销售、供应商改标签会不会没改到. Do not use to assume any word, symbol, or shape is unownable without professional verification, and do not fabricate facts when negotiating or replying to the platform."
---

# Amazon 被诉侵权应对与还原

## 目标

When receiving a trademark or copyright infringement claim against a listing, verify the claimant's actual registered rights rather than assuming a mark is too generic to be owned, weigh contesting versus complying based on exposure and resources, and if complying, negotiate explicit sell-through and reinstatement terms while confirming the supplier actually implements the redesign going forward.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 判断某个词汇或图形符号太常见不可能被注册是常见误区，实际是否已被注册与保护范围需专业核实，不能凭直觉下结论。
- 是否应诉、和解金额与条款高度依赖具体案情与法律管辖，本流程不构成法律意见，涉及重大金额或诉讼风险的情形应聘请专业知识产权律师主导。
- 与对方或平台的沟通中不得提供不实陈述，协商条款、金额与时限均为个案结果，来源中的具体数字仅为示例。

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

1. 收到投诉后先分清角色与类型：对方是主张商标近似还是版权或外观近似，投诉是通过平台直接下架Listing还是以邮件等站外方式发出法律警告，两种情形的紧急程度与处理入口不同。
2. 不要仅凭这个词或图案看起来很常见就假设对方主张不成立，通过专业渠道核实对方主张的注册范围与是否真实有效，必要时咨询有资质的知识产权律师，尤其是涉及现有库存价值较大的情形。
3. 结合对方规模、潜在诉讼成本与自己继续销售现有库存的价值，权衡是应诉还是接受更换设计：涉及现有库存价值较高、且对方明显资源占优时，优先评估和解成本是否显著低于诉讼成本。
4. 如果选择接受更换设计，在协商中明确写入几项条款：允许售完现有库存、由对方出具正式的权利撤销或放行文件提交给平台以恢复销售、以及是否能获得已发生的注册相关费用的补偿。
5. 提前准备好一到两版备选设计方案，一旦达成和解可以立即提供给对方确认，缩短恢复销售的等待时间。
6. 换标后向供应商明确新设计要求，并在下一批生产前用样品或首件确认的方式核实供应商确实采用了新设计，而不是默认对方会自动执行，防止下一批货又用回旧版本重蹈覆辙。
7. 整个过程中的沟通记录、对方发来的权利证明、提交给平台的撤销文件都要留档，作为账号健康记录与未来同类问题的参考。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：核实投诉方商标或版权的实际注册状态与保护范围，辅助判断投诉是否成立及应对策略。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 投诉类型与角色识别记录
- 权利核实与应诉/和解决策依据
- 和解条款清单（售罄库存/撤销文件/费用补偿）
- 供应商换标执行核实记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
