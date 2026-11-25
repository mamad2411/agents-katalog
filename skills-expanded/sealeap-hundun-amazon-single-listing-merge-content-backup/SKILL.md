---
name: sealeap-hundun-amazon-single-listing-merge-content-backup
description: "Merge one standalone, already-live listing into an existing parent/child variation family through the interactive manage-variations flow by matching SKU, ASIN, price, quantity and the variation attribute, while pre-emptively preserving the child's bullet points, description and backend search terms that this workflow can overwrite or blank out. Single-listing scope; does not assume identical platform behavior on every account. Use for 怎么把一条listing合并进变体、合并变体后五点没了怎么办、合并变体内容丢失、后台添加变体选项怎么用. Do not use for bulk merging many listings at once (use the flat-file batch workflow for that), and do not merge listings across different brands."
---

# Amazon 单Listing并入变体防丢失

## 目标

Merge one standalone, already-live listing into an existing parent/child variation family through the interactive manage-variations flow by matching SKU, ASIN, price, quantity and the variation attribute, while pre-emptively preserving the child's bullet points, description and backend search terms that this workflow can overwrite or blank out. Single-listing scope; does not assume identical platform behavior on every account.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 合并会用附体的标题等内容覆盖子体，这是基于操作观察的经验，不同账户/类目模板下具体覆盖哪些字段可能不同，操作前后都要人工核对，不能假设不会覆盖。
- 色卡（如 color map）与颜色名称（如 color name）通常是两个独立字段，前者一般为平台限定可选值、后者可自定义展示文案，混填会导致提交失败或展示异常。
- 库存与价格必须与被合并 listing 当前状态一致再提交，避免因价格/库存不匹配触发额外错误或短暂的错误展示。

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

1. 合并前先完整保存要被合并的这条 listing 当前的标题、五点、长描述、后台搜索词等内容（复制到本地文档），因为合并后这些字段有较高概率被覆盖或清空。
2. 打开目标变体家族的附体（parent）listing，进入其变体编辑区域，按产品属性（如颜色）添加一个新的变体维度值。
3. 在新增变体行填入要合并进来的这条 listing 的 ASIN（作为商品编码）、SKU（必须与被合并 listing 的当前 SKU 完全一致）、当前价格、当前库存和对应的属性值（如色卡与颜色名称），状态选“全新”。
4. 确认无误后保存，等待当前账户观察到的生效时间，到前台核实变体数量是否增加、被合并的 listing 是否已经挂在家族下。
5. 核对合并后该子体的标题、五点、描述、后台关键词是否被附体内容覆盖或清空；如有丢失，把第一步保存的内容逐项粘贴补齐，必要时多保存几次以确认生效。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 合并前内容备份文档（标题/五点/描述/后台关键词）
- 变体合并操作记录（SKU/ASIN/属性值对照）
- 合并后内容核对与补齐清单
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
