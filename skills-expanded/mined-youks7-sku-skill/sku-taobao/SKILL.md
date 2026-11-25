---
name: sku-taobao
description: "Create Taobao-native product asset plans from verified real-SKU materials, separating search images, 1:1 or 3:4 main media, carousel images, SKU property images, and mobile detail modules. Use when users mention 淘宝、淘宝商品主图、淘宝轮播图、淘宝 SKU 属性图、淘宝详情页、淘系普通店铺或淘宝商品发布。Do not use for Tmall brand workflows."
---

# 淘宝 SKU 详情页

把已确认的产品事实转换为淘宝原生素材方案，不把所有素材做成同一种 9:16 长图。

## 读取规则

开始时完整读取 [`references/common-safety.md`](references/common-safety.md) 和 [`references/platform-rules.md`](references/platform-rules.md)。只有用户确认方向并进入正式生产时，才完整读取 [`references/per-unit-production.md`](references/per-unit-production.md)。涉及类目尺寸、资质或发布字段时，以用户后台当前规则为准。

## 工作流

1. 继承 `SKU_CONTEXT`；没有上下文时先使用 `$sku-product-core`，未安装时执行最小事实与保真检查。
2. 确认淘宝市场、叶子类目、商品类型、语言、变体和目标素材槽位。
3. 区分搜索/主图、轮播、SKU 属性图和详情模块，分别定义商业任务。
4. 根据商品与价格带生成二至三个真实不同的策略方向，不固定套用功能、场景、高端三类。
5. 用户确认后，严格按逐屏 / 逐模块生产协议，为每个槽位完整输出 Prompt、Negative Prompt、处理模式、文案位置、后期排版、镜头矩阵、产品一致性质检和通用 Prompt 拦截。
6. 检查标题、属性、图片、SKU、赠品、规格和详情描述一致性。

## 输出

输出 `淘宝素材槽位清单`、`方向提案`、`整页生产总控`、`确认后的逐单元完整生产记录`、`SKU 图映射`、`事实与描述不符风险` 和 `最终发布检查`。最终文字使用独立排版；平台禁止覆盖文字的槽位遵守更严格规则。
