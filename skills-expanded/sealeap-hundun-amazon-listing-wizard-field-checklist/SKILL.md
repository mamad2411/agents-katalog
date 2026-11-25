---
name: sealeap-hundun-amazon-listing-wizard-field-checklist
description: "Walk a seller through Amazon's guided single-listing creation flow field by field — category match, brand/UPC exemption, package versus carton dimensions, and price fields — to reduce rework from mismatched categories or missing required attributes. Uses only existing catalog and product-fact data; never fabricates identifiers. Use for 新品如何上架、如何用后台向导创建listing、类目匹配不上怎么办、划线价怎么设置、UPC没有怎么办. Do not use to bulk-create or bulk-edit many SKU at once (use a flat-file based workflow for that), and do not mutate a live listing's price without confirming the current promotion calendar."
---

# Amazon 新品上架向导字段核对

## 目标

Walk a seller through Amazon's guided single-listing creation flow field by field — category match, brand/UPC exemption, package versus carton dimensions, and price fields — to reduce rework from mismatched categories or missing required attributes. Uses only existing catalog and product-fact data; never fabricates identifiers.

## 不可妥协的边界

- 当前 Amazon 官方政策、账户资格、站点字段和一方数据优先于本 Skill 的经验框架。
- 第三方数据一律标为估算或前台观测，不得写成 Amazon 一方事实。
- 默认只读诊断和草案；任何广告、Listing、库存、促销或外部系统写操作都需逐项展示并取得明确批准。
- 一次实验只改变一个主要变量，并记录基线、样本、成功、停止和回退条件。
- 不得复制来源材料或竞品表达；输出必须按当前任务重新组织并可由现有证据支撑。
- 类目自动匹配结果为经验观察，不同账户/类目库版本可能不同，应以英文搜索结果人工核对为准，不能默认系统匹配一定准确。
- List Price/划线价的展示逻辑以当前账户实际显示效果为准，“必须先有参考价历史才能划线”是待验证经验，操作前建议先小范围验证。
- 是否需要保修信息、是否含电池等安全合规字段应按产品实际情况与当前平台要求填写，不得为图方便统一勾“否”。

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

1. 先确认产品的目标类目：用英文关键词在类目选择器中检索，逐一核对候选小类目是否与对标竞品所在类目一致，而不是直接采用系统默认匹配的第一个类目。
2. 品牌与商品编码：有品牌就填品牌名，无品牌勾选“无品牌”；有 UPC/EAN 等编码就填，没有则勾选无编码并按提示走确认流程，不得编造编码。
3. 区分“单品包装尺寸”和“外箱/整箱尺寸”两类尺寸字段，只按字段说明填写对应口径，避免把整箱尺寸误填进单品字段。
4. 五点描述与长描述按产品事实填写关键词与卖点，图片可留待后续补传，不因为图片未就绪而卡住其余字段。
5. 价格字段区分 Your Price（当前售价）与 List Price（参考价/划线价基准）：如需后续做限时优惠价并显示划线效果，需要先建立 List Price 记录。
6. 提交前检查是否勾选“显示全部属性”，核对材质、颜色、是否含电池等带必填标记的字段是否遗漏，没有必填标记的字段可按实际情况留空。
7. 提交后到后台核实新 listing 是否正常显示、类目是否匹配、图片和价格是否与预期一致，发现错配及时在同一位置修正而不是重新创建新 listing。

最后做数据充分性检查，并把结论分成 `FACT / ESTIMATE / HYPOTHESIS / UNKNOWN`。若关键证据不足，状态写 `HOLD`。

## 必须交付的结果

- 类目匹配核对表
- 字段填写检查清单
- 价格字段设置记录（Your Price / List Price）
- 上架后核验记录
- 数据范围、来源、采集时间、样本与限制。
- 关键假设、待补证据、风险和不可确定项。
- 若有动作：对象、旧值、新值、预期、停止条件、回退值与审批状态。

方案状态使用 `READY FOR REVIEW / DRAFT / HOLD / STOP`；如已执行，另行记录实际结果及回读证据。未得到明确批准时，不得声称已修改线上对象。
