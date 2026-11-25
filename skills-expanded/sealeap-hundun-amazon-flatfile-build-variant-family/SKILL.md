---
name: sealeap-hundun-amazon-flatfile-build-variant-family
description: "Use a category-specific inventory flat-file template to create a brand-new multi-variant listing from a single existing listing, append an additional variant to an already-multi-variant family, or bulk-edit fields on already-live listings, by correctly setting parent/child SKU references, the variation theme, and update-versus-partial-update flags. Requires accurate existing SKU/ASIN references; never fabricates product identifiers. Use for 用表格新增变体、单属性产品怎么加变体、多属性产品怎么加变体、表格批量改标题图片、UPC报品牌不一致怎么办. Do not use this to merge two already-independent live listings into one family (use the dedicated merge workflow for that), and do not submit a template without first checking brand/category consistency across all rows."
---

# Amazon 表格新建变体家族与增补

## 目标

Use a category-specific inventory flat-file template to create a brand-new multi-variant listing from a single existing listing, append an additional variant to an already-multi-variant family, or bulk-edit fields on already-live listings, by correctly setting parent/child SKU references, the variation theme, and update-versus-partial-update flags. Requires accurate existing SKU/ASIN references; never fabricates product identifiers.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 品牌名、制造商名、商品编码三者之间的一致性要求以当前账户实际报错情况为准，来源中“某类占位文案能避免报错”的做法是经验性变通，操作前建议先在单个 SKU 上小范围验证。
- “更新”模式会整体覆盖对应行涉及的字段，遗漏未填的字段可能被清空，因此对已上线 listing 的调整应默认使用“部分更新”，仅在确需整体重建时才用“更新”。
- 部分账户版本的库存文件预检查功能不一定可用，建议先小批量上传验证模板正确性，再扩大到批量操作。

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

1. 按产品类目下载对应的批量表模板，先看清哪些列被标为必填，很多非必填列可以先留空，图片列可以留到后台再单独补传。
2. 单属性产品（原本只有一条 listing）增补变体：新建一个附体 SKU 和一个新的子体 SKU（均自定义），把原有 listing 的 SKU 填入另一子体行、商品编码列用其 ASIN；新变体行的商品编码则用 UPC/EAN 等填写并补全该类目要求的全部产品属性。
3. 多属性产品（已有附体家族）增补变体：只需新增一行子体，附体行沿用现有附体 SKU、品牌、标题、ASIN，不必重复列出家族里已存在的其他子体。
4. 变体关系与更新方式：新建的附体行选“更新”，原本已存在、只是被引用或部分调整的行选“部分更新”；变体主题按产品属性实际情况选择，且所有行的品牌名必须完全一致，否则无法建立变体关系。
5. 如果没有完成品牌备案、商品编码来自非官方渠道，按平台提示在建议的编码/品牌占位字段中如实填写，避免触发品牌不一致报错；色卡类字段与颜色名称类字段要分开填写，不要混用。
6. 如果目的只是修改已上线 listing 的某个字段（标题、图片地址、五点等），同样用该类目模板，只改要调整的列、ASIN 列填对应 ASIN，更新方式选“部分更新”，未改动的字段会保持原样。
7. 保存表格后到后台上传库存文件；上传结果分两种，提示有草稿待处理通常代表有报错需要下载报告定位修正，没有该提示则代表上传成功，随后再到前台补充图片、五点等尚未通过表格填写的内容。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 类目专属批量表模板（已填写）
- parent/child SKU、ASIN、变体属性对照表
- 上传结果报告（成功/报错定位）
- 后台补充项清单（图片/五点/描述）
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
