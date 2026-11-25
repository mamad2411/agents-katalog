---
name: sealeap-hundun-amazon-brand-store-page-setup
description: "Stand up a minimal viable Amazon brand store page — a shallow page hierarchy, a title module, a product grid and product modules — fast enough to clear the current page-count threshold some Sponsored Brands store-page placements require, then iterate on the remaining layout modules after the store is live and approved. Use for 品牌旗舰店怎么搭建、开品牌广告需要几个页面、商品网格三种添加方式怎么选、旗舰店审核多久、编辑中的旗舰店会不会影响已上线页面. Do not use to assume every placement has the same page-count requirement — verify the current requirement for the specific placement before planning page count."
---

# Amazon 品牌旗舰店搭建

## 目标

Stand up a minimal viable Amazon brand store page — a shallow page hierarchy, a title module, a product grid and product modules — fast enough to clear the current page-count threshold some Sponsored Brands store-page placements require, then iterate on the remaining layout modules after the store is live and approved.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 来源给出的图片像素尺寸、页面数门槛与审核时长为特定时点的规则摘录，需以当前后台实时提示为准，不作为长期不变的规范。
- 旗舰店页面越多越有利于开通广告是来源基于特定广告位规则的经验总结，具体门槛因广告位类型而异，应先核实目标广告位当前要求再规划页面数量，不盲目堆砌页面数。
- 参考同类目旗舰店版式仅借鉴模块结构与信息组织方式，不得直接复制其图片、文案或品牌视觉元素。
- 商品网格自动抓取商品信息会随 Listing 本身更新而变化，若使用自定义编辑方式呈现商品信息，需要自行维护内容与实际 Listing 保持一致，避免出现价格或状态不符导致的买家投诉。

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

1. 进入后台的品牌旗舰店管理入口，首次创建选创建 Store，已有旗舰店则用编辑品牌旗舰店；先规划页面结构：主页为必须页面，其余页面按需添加，子页面层级最多到二级，超过二级需要合并或重新规划信息架构。
2. 确认目标广告位的页面数门槛：若计划开启需要旗舰店配合的品牌推广类广告位，需要先核实该广告位当前要求的最低页面数，按门槛规划页面数量，不同广告位要求可能不同，需逐一核实而非套用单一数字。
3. 每个页面先完成标题模块：标题图片需满足当前要求的最小像素尺寸，可从资产库复用已上传过的图片避免重复上传；模板优先选商品网格类简单版式，新手不必一开始追求复杂版式。
4. 按需添加拆分模块与商品模块：商品模块两种呈现方式，一种自动带出商品详情，一种为自定义编辑；按页面用途选择合适的类型。
5. 商品网格根据商品数量选添加方式：单个或少量商品用关键词或 ASIN 逐条搜索添加；商品数量多时用手动输入 ASIN 列表批量提交，比逐条搜索添加更省时间；同时设置是否隐藏缺货商品。
6. 提交后进入审核，审核通过前不影响已上线页面的展示；建议先提交能满足开通广告门槛的基础版本上线，后续编辑内容需要重新审核但同样不影响已上线版本，通过后才会替换。
7. 后续再逐步完善其余版式模块与页面细节，参考同类目旗舰店的公开页面结构作为版式对照，但不直接复制其图片与文案。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 第三方 MCP 数据

仅在自有数据不足且当前任务确实需要外部证据时，读取 [references/mcp-data-plan.md](references/mcp-data-plan.md)，再使用 `scripts/mcp_research.py`。本 Skill 的外部取数目的：抓取同类目品牌旗舰店的公开页面结构与模块组织方式，作为版式规划的对照参考。

- 先 `doctor`，再 `search-tools` 和 `describe`；工具名及参数以实时 `tools/list` 与 `inputSchema` 为准。
- Token 只从环境变量读取。不得写入命令参数、URL、Skill、报告、日志或 Git。
- `tools/call` 或 Actor 可能计费；先展示 Provider、工具、无密钥业务参数、预计成本与输出位置，核对已有授权覆盖后才加 `--allow-cost`；该标志不是费用上限。


## 必须交付的结果

- 旗舰店页面结构规划（含二级页面层级）
- 目标广告位页面数门槛核查记录
- 各页面模块配置清单（标题/拆分/商品/商品网格）
- 提交审核记录与上线前后对比
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
