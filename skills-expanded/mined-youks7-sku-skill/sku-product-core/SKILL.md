---
name: sku-product-core
description: "Analyze real product images and supplied documents to establish verified SKU identity, evidence boundaries, fidelity mode, product-specific visual memory points, and a reusable SKU_CONTEXT. Use before platform production when facts are not yet normalized, when multiple marketplaces share one product, or when users ask for 产品事实分析、商品图保真、禁止编造、模式 A/B/C、竞品安全参考或跨平台 SKU 上下文。"
---

# SKU 产品事实核心

把真实产品资料整理为所有平台可复用的事实与保真上下文。只完成公共产品分析，不生成平台尺寸、页面结构或正式生图 Prompt。

## 读取规则

完整读取：

- [`references/core-rules.md`](references/core-rules.md)
- [`references/sku-context-schema.md`](references/sku-context-schema.md)
- [`references/core-qa.md`](references/core-qa.md)

只有用户要求竞品扫描、类目同质化判断或参考竞品时，再读取 [`references/competitor-research.md`](references/competitor-research.md)。没有实际检索或用户提供的竞品素材时，只能称为经验性启发。

## 工作流

1. 盘点产品图、包装图、规格表、认证、品牌资产和用户陈述。
2. 分开记录已确认事实、谨慎推断、禁止主张和缺失证据。
3. 判断模式 A、B 或 C，并说明允许修改与禁止修改的内容。
4. 提炼三个有图片或资料证据的产品专属视觉记忆点。
5. 标记高风险类目和需要人工或法律复核的主张。
6. 按标准结构输出 `SKU_CONTEXT`。
7. 每轮只提出真正会改变真实性或平台路线的问题，其他未知项保持为空。

## 边界

不要选择平台方向，不要输出固定屏数，不要生成价格、参数、认证或正式广告承诺。用户指定平台时，把完成的 `SKU_CONTEXT` 交给对应平台 Skill。
