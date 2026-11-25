---
name: sku-tmall
description: "Create Tmall-specific branded product asset and detail-page plans with strict SKU fidelity, brand authorization awareness, SPU/SKU consistency, category qualifications, and reusable brand systems. Use when users mention 天猫、天猫旗舰店、天猫品牌详情页、品牌旗舰店素材、天猫商品发布或天猫品牌资产。"
---

# 天猫 SKU 详情页

在淘宝类素材槽位基础上强化品牌身份、类目资质、SPU/SKU 关系和跨商品视觉一致性。

## 读取规则

开始时完整读取 [`references/common-safety.md`](references/common-safety.md) 和 [`references/platform-rules.md`](references/platform-rules.md)。只有用户确认方向并进入正式生产时，才完整读取 [`references/per-unit-production.md`](references/per-unit-production.md)。资质、品牌和类目字段以商家后台当前 Schema 为准。

## 工作流

1. 继承 `SKU_CONTEXT`；没有上下文时先使用 `$sku-product-core`，未安装时执行最小事实与保真检查，再确认品牌权利、店铺类型、SPU、SKU 和目标类目。
2. 分开记录真实品牌资产、允许使用的认证和缺失资质。
3. 区分主图、轮播、SKU 图、详情模块、品牌故事和资质说明。
4. 从品牌系统与产品差异共同生成方向，不用空泛黑金或伪奢华替代品牌证据。
5. 用户确认后，严格按逐屏 / 逐模块生产协议，为每个槽位完整输出 Prompt、Negative Prompt、处理模式、品牌资产来源、文案位置、后期排版、镜头矩阵、产品一致性质检和通用 Prompt 拦截。
6. 检查品牌、产品、包装、参数、资质和售后在所有位置一致。

## 输出

输出 `品牌与资质输入清单`、`SPU/SKU 素材映射`、`品牌视觉固定项与变化项`、`整页生产总控`、`逐单元完整生产记录`、`证据缺口` 和 `发布质检`。
