---
name: sku-jd
description: "Create JD-native product image and detail-page plans with verified parameters, model compatibility, package contents, installation conditions, warranty responsibility, and service boundaries. Use when users mention 京东、JD、京东主图、京东参数详情、兼容性、包装清单、质保、安装说明或专业商品页。"
---

# 京东 SKU 详情页

把商品视觉、结构化参数、兼容性、包装和服务承诺连接到同一证据链。

## 读取规则

开始时完整读取 [`references/common-safety.md`](references/common-safety.md) 和 [`references/platform-rules.md`](references/platform-rules.md)。只有用户确认方向并进入正式生产时，才完整读取 [`references/per-unit-production.md`](references/per-unit-production.md)。类目参数和资质以京东商家后台与规则中心当前要求为准。

## 工作流

1. 继承 `SKU_CONTEXT`；没有上下文时先使用 `$sku-product-core`，未安装时执行最小事实与保真检查，再补充型号、规格、兼容性、包装、安装、质保和售后证据。
2. 建立参数—证据矩阵，未知数字保持为空。
3. 区分主图、附图、参数模块、兼容性、安装使用和服务模块。
4. 根据购买疑虑生成专业证明型方向，不用科技光效替代真实性能证据。
5. 用户确认后，严格按逐屏 / 逐模块生产协议，为每个模块完整输出 Prompt、Negative Prompt、处理模式、文案位置、后期排版、镜头矩阵、参数证据、产品一致性质检和通用 Prompt 拦截。
6. 检查图片、参数、包装清单和服务承诺的一致性。

## 输出

输出 `参数—证据矩阵`、`兼容性表`、`包装清单`、`素材模块计划`、`整页生产总控`、`逐单元完整生产记录`、`服务边界` 和 `发布质检`。
