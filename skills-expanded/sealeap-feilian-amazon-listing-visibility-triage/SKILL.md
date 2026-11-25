---
name: sealeap-feilian-amazon-listing-visibility-triage
description: "Triage a new listing's lack of visibility by checking search-index status, ad eligibility, Vine enrollment criteria, and page conversion appeal as four separate possible causes before assuming the listing was never indexed or resubmitting it. Treats the exact mechanism behind search suppression or ad eligibility gating as unverified and defers to current Seller Central status and support guidance. Use for Listing搜不到排查、广告无曝光原因排查、Vine无人认领原因排查、新品收录状态核实、删除重传前的最终确认. Do not use to delete and relist a new ASIN as a first response before completing the index, ad, Vine, and page checks below."
---

# Amazon Listing曝光异常排查

## 目标

Triage a new listing's lack of visibility by checking search-index status, ad eligibility, Vine enrollment criteria, and page conversion appeal as four separate possible causes before assuming the listing was never indexed or resubmitting it. Treats the exact mechanism behind search suppression or ad eligibility gating as unverified and defers to current Seller Central status and support guidance.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源描述的搜索抑制、索引权重、广告相关性排序等具体判定机制是其观察或转述，平台内部算法与判定口径未公开，不能反向推导出确定的规避或加速方法。
- Vine与广告资格的具体准入门槛可能随平台政策调整，需以当前卖家后台展示的条件为准，不作为固定规则长期套用。
- 删除重传通常无效是来源基于其观察给出的经验判断，遇到官方明确给出不同处理指引时，以官方指示为准。

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

1. 先在卖家后台核对Listing状态：是否active、是否有可售库存、是否处于搜索抑制或其他限制状态，作为判断完全未收录还是收录但展示受限的第一道分界线。
2. 分别用ASIN精确搜索、品牌词搜索、核心词/长尾词搜索三种方式核对前台可见情况，区分ASIN本身搜不到（可能是真正索引异常）与ASIN能搜到但核心词搜不到（多为相关性或权重问题），不能只做一种搜索就下结论。
3. 核对类目属性与关键字段（浏览节点、年龄段、尺寸、材质、功能等）是否填写准确，错误的属性归类会影响系统对相关性的判断，进而影响搜索结果里的展示位置。
4. 若怀疑广告没有曝光，按官方给出的资格排查顺序逐项核对（活动是否在运行、当日预算是否耗尽、ASIN是否具备广告资格、是否拿到可展示的报价资格、定向与否定词设置），不要直接归因为出价过低。
5. 若开启Vine后长期无人认领，除核对准入条件（评论数量、FBA在售状态、可售库存、类目属性完整）外，评估主图与价格是否具备吸引测评者认领的基本吸引力。
6. 综合四类检查结果判断根因：只有在ASIN本身搜索都无法找到、且后台已确认无库存/下架等原因时，才考虑联系客服核实索引问题；反馈时附上ASIN、具体搜索词、当前状态截图与明确诉求，避免笼统描述被导入模板回复。
7. 完成一轮诊断后，把四条线的结论分别记录为正常、异常或待观察，只对判定异常的环节采取针对性动作，不对整体链路做无差别的删除重传。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：核验ASIN、品牌词、核心词在站内前台搜索结果中的公开收录与排位情况，作为索引状态判断的独立佐证。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- Listing状态与搜索抑制核对记录
- ASIN/品牌词/核心词三级搜索结果对照表
- 广告资格排查清单
- Vine准入与页面吸引力评估
- 四线诊断结论与客服沟通记录（如需要）
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
