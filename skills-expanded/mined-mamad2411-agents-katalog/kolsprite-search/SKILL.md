---
name: kolsprite_search
description: Automatically use the KOLSprite MCP tools for straightforward TikTok creator, video, product, and shop lookups. Do not use for multi-step business research, opportunity evaluation, cold-start planning, competitor research, or growth strategy.
---

# Purpose

You have access to the KOLSprite MCP service.

Whenever the user asks about TikTok creators, videos, products, or shops, automatically invoke the appropriate MCP tool.

Never ask the user whether the MCP should be used.

Use natural language understanding to determine the correct tool.

---

# Available MCP Tools

- creator_search
- video_search
- product_search
- shop_search

Always select the single best matching tool.

If the user's request spans multiple domains (for example, "Find creators promoting this product"), you may invoke multiple MCP tools when appropriate.

Never fabricate data.

---

# Tool Selection Rules

## Use creator_search when the user wants to:

- 查询达人
- 查达人
- 搜达人
- 找达人
- TikTok达人
- TikTok博主
- TikTok创作者
- KOL
- Influencer
- Creator
- 网红
- 达人数据
- 达人分析
- 达人主页
- 达人粉丝
- 达人销量
- 达人GMV
- 达人带货
- 达人联系方式
- 达人分类
- 达人榜单
- 达人推荐
- 查某个达人
- Search creators
- Find creators
- Creator analytics
- Creator profile

Examples

- 查询美国美妆达人
- 查粉丝100万以上达人
- 搜索宠物达人
- Find UK fitness creators

→ Call creator_search

---

## Use video_search when the user wants to:

- 查询视频
- 查视频
- 搜视频
- 热门视频
- 爆款视频
- 视频分析
- 视频数据
- 视频播放
- 视频互动
- 视频销量
- 视频GMV
- 视频趋势
- Search videos
- Trending videos
- Viral videos
- Shoppable videos
- Video analytics

Examples

- 查询美国爆款视频
- 搜索美妆视频
- 最近热门视频
- Find viral skincare videos

→ Call video_search

---

## Use product_search when the user wants to:

- 查询商品
- 查商品
- 搜商品
- 商品数据
- 商品销量
- 商品分析
- 商品价格
- 商品排行榜
- 热卖商品
- 爆款商品
- TikTok商品
- Search products
- Find products
- Product analytics

Examples

- 查询美国销量最高的精华液
- 查售价20美元以下商品
- Find skincare products

→ Call product_search

---

## Use shop_search when the user wants to:

- 查询店铺
- 查店铺
- 搜店铺
- 店铺数据
- 店铺销量
- 店铺评分
- 店铺分析
- 店铺排行榜
- TikTok Shop
- 商家
- Seller
- Shop
- Search shops
- Find shops

Examples

- 查询美国美妆店铺
- 查销量最高店铺
- Find electronics shops

→ Call shop_search

---

# Multi-tool Queries

If the user's request naturally requires multiple datasets, call multiple MCP tools.

Examples

"哪些达人在推广这款商品？"

→ product_search
→ creator_search

"这个店铺有哪些爆款视频？"

→ shop_search
→ video_search

"销量最高商品对应哪些达人？"

→ product_search
→ creator_search

"美国销量最高店铺卖什么商品？"

→ shop_search
→ product_search

---

# Missing Information

If required information is missing, ask only for the minimum clarification.
ki
Good:

"请问要查询哪个国家？"

Bad:

"是否需要调用MCP？"

Never ask whether the user wants to use MCP.

---

# Response Rules

1. Always invoke MCP first.
2. Base answers only on MCP results.
3. Do not fabricate statistics.
4. Summarize results clearly.
5. Preserve important numeric metrics.
6. When multiple results exist, rank them appropriately.
7. Explain filters that were applied.
8. Use the user's language.
9. If no data is found, clearly state that no matching records were returned.
