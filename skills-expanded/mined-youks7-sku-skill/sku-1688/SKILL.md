---
name: sku-1688
description: "Create 1688-native B2B product pages focused on purchasing certainty, verified MOQ and tier pricing, samples, OEM/ODM scope, customization, production lead time, capacity, packaging, logistics, quality control, and inquiry conversion. Use when users mention 1688、批发、工厂货源、起订量、阶梯价、拿样、贴牌、OEM、ODM、定制或采购详情页。"
---

# 1688 批发商品页

围绕采购决策、定制能力和交付确定性设计商品页，不把消费者种草页简单改成批发版。

## 读取规则

开始时完整读取 [`references/common-safety.md`](references/common-safety.md) 和 [`references/platform-rules.md`](references/platform-rules.md)。只有用户确认方向并进入正式生产时，才完整读取 [`references/per-unit-production.md`](references/per-unit-production.md)。价格、MOQ、产能和交付信息必须来自商家资料。

## 工作流

1. 继承 `SKU_CONTEXT`；没有上下文时先使用 `$sku-product-core`，未安装时执行最小事实与保真检查，再确认供应方身份、买家类型、采购场景和销售单位。
2. 收集 MOQ、阶梯价、样品、定制范围、打样、生产、包装、物流和质检证据。
3. 未确认的采购字段保持“待商家补充”，不得生成行业平均值充数。
4. 动态生成采购确定型、定制能力型、样品验证型或长期合作型方向。
5. 用户确认后按采购信息顺序组织页面，并严格按逐屏 / 逐模块生产协议，为每个模块完整输出 Prompt、Negative Prompt、处理模式、文案位置、后期排版、镜头矩阵、采购证据、产品一致性质检和通用 Prompt 拦截。
6. 检查标题、图片、规格、价格、MOQ、定制与交付承诺一致。

## 输出

输出 `采购资料缺口`、`MOQ 与阶梯价`、`定制能力矩阵`、`打样与交付`、`包装物流`、`质检证据`、`整页生产总控`、`逐单元完整生产记录` 和 `询盘 CTA`。
