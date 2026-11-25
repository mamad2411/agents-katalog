---
name: sku-tiktok-shop
description: "Create region-aware TikTok Shop product-detail-page image plans, SKU variation media, Product Shopping Ads source-asset checks, and shoppable-photo handoffs while protecting real product identity. Use when users mention TikTok Shop、TikTok 商品页、PDP images、variation images、Product Shopping Ads、Shop Ads、Shoppable Photo 或 TikTok Shop listing policy. Do not use for Douyin Mall."
---

# TikTok Shop SKU 页面

严格区分 PDP 合规图片、广告复用源素材、Shoppable Photo 和视频内容，不把 UGC 风格套到白底主图。

## 读取规则

开始时完整读取 [`references/common-safety.md`](references/common-safety.md) 和 [`references/platform-rules.md`](references/platform-rules.md)。只有用户确认方向并进入正式生产时，才完整读取 [`references/per-unit-production.md`](references/per-unit-production.md)。规则因国家和时间变化，发布前核对当地 Seller Center 当前政策。

## 工作流

1. 继承 `SKU_CONTEXT`；没有上下文时先使用 `$sku-product-core`，未安装时执行最小事实与保真检查，再确认国家、语言、类目、品牌、variations 和目标素材槽位。
2. 区分 PDP main image、additional images、variation images、Shop Ads source、Shoppable Photo 和视频交接。
3. 主图和变体图采用真实商品与严格保真；平台禁止数字渲染或覆盖元素时不得使用模式 B。
4. 追加图片可按平台允许范围展示角度、细节、使用、尺寸和场景，不重复相同视角。
5. 用户确认后，严格按逐屏 / 逐模块生产协议，为每张 PDP / variation 图片完整输出 Prompt、Negative Prompt、处理模式、文案位置与平台覆盖限制、后期排版、镜头矩阵、产品一致性质检和通用 Prompt 拦截。
6. 视频、达人或直播任务只生成结构化交接 Brief，并转入专用内容工作流；检查 PDP 信息与广告复用素材、SKU、品牌、披露和实际交付一致。

## 输出

输出 `地区规则状态`、`PDP Image Map`、`Variation Map`、`整页生产总控`、`逐单元完整生产记录`、`Shop Ads Source Check`、`Shoppable Photo Brief`、`视频交接 Brief` 和 `发布质检`。
