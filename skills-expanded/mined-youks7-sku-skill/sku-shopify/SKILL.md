---
name: sku-shopify
description: "Create responsive Shopify product-detail-page content systems with semantic sections, media galleries, variant mapping, metafields, alt text, SEO metadata, accessibility, real Add to Cart components, mobile performance, and conversion measurement. Use when users mention Shopify、独立站、PDP、产品模板、theme sections、metafields、产品变体、alt text 或独立站转化。"
---

# Shopify SKU 页面

规划响应式、可索引、可访问的 PDP，而不是把独立站压成固定六屏或八屏图片。

## 读取规则

开始时完整读取 [`references/common-safety.md`](references/common-safety.md) 和 [`references/platform-rules.md`](references/platform-rules.md)。只有用户确认方向并进入正式生产时，才完整读取 [`references/per-unit-production.md`](references/per-unit-production.md)。主题能力、应用和销售地区会改变实现方式，必须记录假设。

## 工作流

1. 继承 `SKU_CONTEXT`；没有上下文时先使用 `$sku-product-core`，未安装时执行最小事实与保真检查，再确认目标地区、语言、主题、模板、变体、购买选项和品牌资产。
2. 建立产品内容模型：标题、描述、媒体、variants、metafields、披露、配送与售后。
3. 按 Hero、Gallery、Benefits、Proof、Details、FAQ、Trust 和 CTA 等真实 section 设计结构。
4. 关键文字保留为 HTML；图片提供 alt text；CTA 使用真实交互组件。
5. 用户确认方向后，严格按逐屏 / 逐模块生产协议，为每个含媒体的 PDP Section 完整输出 Prompt、Negative Prompt、处理模式、HTML 文案位置、响应式后期排版、镜头矩阵、产品一致性质检和通用 Prompt 拦截；纯组件也必须保留模板并标记 Prompt 为 N/A。
6. 检查变体媒体、库存展示、结构化信息、SEO 和可访问性一致。

## 输出

输出 `PDP Section Map`、`Content Model`、`整页生产总控`、`逐单元完整生产记录`、`Media Plan`、`Variant/Metafield Map`、`SEO/Alt Text`、`CTA`、`性能约束` 和 `实验事件`。
