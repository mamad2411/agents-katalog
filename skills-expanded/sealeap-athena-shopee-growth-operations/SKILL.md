---
name: sealeap-athena-shopee-growth-operations
description: "处理 Shopee 折扣、优惠券、组合促销、广告、联盟营销、直播和视频等增长任务。按实际活动类型读取细则，保留叠加限制、预算与发布权限。"
---

# Shopee 促销、广告与内容运营

处理 Shopee 折扣、优惠券、组合促销、广告、联盟营销、直播和视频等增长任务。按实际活动类型读取细则，保留叠加限制、预算与发布权限。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [Shopee 加购优惠 促销管理](references/capabilities/shopee-account-add-on-deal/workflow.md) | 限定本次活动类型为加购优惠；核对当前活动与资格，计算折扣叠加、库存和毛利影响，提交授权配置后回读 |
| [Shopee 广告管理](references/capabilities/shopee-account-ads/workflow.md) | 先读广告实体与同窗报表，形成出价、预算或状态差异，执行已授权对象并回读 |
| [Shopee 联盟营销](references/capabilities/shopee-account-ams/workflow.md) | 核对活动与商品资格，分开自然销售和联盟归因，准备授权佣金或活动变更 |
| [Shopee 捆绑优惠 促销管理](references/capabilities/shopee-account-bundle-deal/workflow.md) | 限定本次活动类型为捆绑优惠；核对当前活动与资格，计算折扣叠加、库存和毛利影响，提交授权配置后回读 |
| [Shopee 单品折扣 促销管理](references/capabilities/shopee-account-discount/workflow.md) | 限定本次活动类型为单品折扣；核对当前活动与资格，计算折扣叠加、库存和毛利影响，提交授权配置后回读 |
| [Shopee 关注奖励活动](references/capabilities/shopee-account-follow-prize/workflow.md) | 核对当前平台允许的关注奖励类型和叠加条件，创建可评审配置后按授权执行 |
| [Shopee 直播管理](references/capabilities/shopee-account-livestream/workflow.md) | 读取正式直播能力和场次状态，准备商品或场次变更，再核对生效结果 |
| [Shopee 限时特卖 促销管理](references/capabilities/shopee-account-flash-sale/workflow.md) | 限定本次活动类型为限时特卖；核对当前活动与资格，计算折扣叠加、库存和毛利影响，提交授权配置后回读 |
| [Shopee 精选商品](references/capabilities/shopee-account-top-picks/workflow.md) | 核对可售状态和现有精选配置，准备顺序或商品调整并回读 |
| [Shopee 视频管理](references/capabilities/shopee-account-video/workflow.md) | 核对视频及商品关系，准备内容或状态变更预览，执行授权操作并查看发布状态 |
| [Shopee 优惠券 促销管理](references/capabilities/shopee-account-voucher/workflow.md) | 限定本次活动类型为优惠券；核对当前活动与资格，计算折扣叠加、库存和毛利影响，提交授权配置后回读 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。各促销类型保留适用条件和叠加限制；广告/直播/视频使用独立参考与授权。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
