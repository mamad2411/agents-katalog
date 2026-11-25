---
name: sku-detail-page-director
description: "Orchestrate a one-entry real-SKU product-page workflow across product fact analysis, marketplace routing, direction approval, and specialist handoff. Use when users explicitly invoke $sku-detail-page-director, want one guided entry point, have not chosen a marketplace, compare multiple marketplaces, or adapt one SKU across platforms. For implicit single-marketplace requests, prefer the matching sku-* specialist."
---

# SKU 详情页总导演

作为用户唯一入口，识别产品事实、目标平台和素材槽位，再在同一任务中把工作交给对应平台 Skill。不要要求用户重复输入上下文，也不要把不同平台压缩成一套通用长图。

## 读取规则

先读取 [`references/common-safety.md`](references/common-safety.md) 和 [`references/routing-map.md`](references/routing-map.md)。只读取命中的平台 Skill，不读取全部平台规则。

## 路由流程

1. 识别用户已有的 `SKU_CONTEXT`、产品图片、已确认事实和处理模式。
2. 识别平台、国家或站点、类目、语言、卖家类型和素材槽位。
3. 平台未知时，根据销售场景推荐平台，或只询问一个会改变路线的问题。
4. 缺少 `SKU_CONTEXT` 时，在同一任务中使用 `$sku-product-core` 完成公共产品分析；不要让用户另开任务或重新粘贴资料。
5. 单平台请求只进入一个平台 Skill，并直接继续到方向提案；不要只返回 Skill 名称让用户自己再次调用。
6. 多平台请求从同一基础 `SKU_CONTEXT` 派生多个 target 副本，分别进入专用 Skill。
7. 专用 Skill 未安装时，明确指出缺失名称和所需安装包；不要悄悄模拟整套平台规则。
8. 用户确认方向后，在后续轮次继续使用已选平台 Skill 的生产协议，不重新执行产品分析。

## 保持单向依赖

路由可以调用公共核心和平台 Skill。平台 Skill 不要重新调用本路由，避免循环。平台 Skill 必须继承事实和处理模式，只补充平台字段。

## 输出

默认向用户输出简洁的产品事实边界、识别的平台、素材槽位、二至三个方向、推荐理由和下一步唯一决策。内部路由信息只在有助于排错时展示。用户确认方向前不要生成正式平台 Prompt。
