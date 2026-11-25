---
name: sku-pinduoduo
description: "Create Pinduoduo-native product image and detail plans while verifying SKU, displayed product, price, quantity, bundle, gift, specification, and claim consistency. Use when users mention 拼多多、PDD、多多商品、拼多多主图、轮播图、SKU 图、详情图、低价 SKU 或拼多多描述不符风险。"
---

# 拼多多 SKU 详情页

优先保证用户看到的商品、价格、规格和实际交付一致，再设计高信息效率的素材。

## 读取规则

开始时完整读取 [`references/common-safety.md`](references/common-safety.md) 和 [`references/platform-rules.md`](references/platform-rules.md)。只有用户确认方向并进入正式生产时，才完整读取 [`references/per-unit-production.md`](references/per-unit-production.md)。平台尺寸和类目要求以商家后台当前提示为准。

## 工作流

1. 继承 `SKU_CONTEXT`；没有上下文时先使用 `$sku-product-core`，未安装时执行最小事实与保真检查，再补充所有变体、价格、数量、套装、赠品和交付内容。
2. 建立 SKU—价格—图片一致性矩阵，识别最低价 SKU 与曝光商品的差异。
3. 区分曝光图、轮播图、SKU 图和详情图。
4. 生成以价值确定性、使用证明或规格清晰为核心的动态方向，不默认做廉价促销风。
5. 确认方向后，严格按逐屏 / 逐模块生产协议，为每个槽位完整输出 Prompt、Negative Prompt、处理模式、文案位置、后期排版、镜头矩阵、产品一致性质检和通用 Prompt 拦截。
6. 检查品牌、材质、型号、功效、数量和活动标识是否相互一致且有证据。

## 输出

输出 `SKU—价格—图片矩阵`、`素材槽位计划`、`确认方向方案`、`整页生产总控`、`逐单元完整生产记录`、`描述不符风险`、`低价引流风险` 和 `最终检查`。
