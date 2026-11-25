---
name: stringer
description: 「什么值得做」(stringers.io):面向独立开发者和小团队的 App 商业情报库——涵盖热门赛道、早鸟新苗子、52 万个 App 全量档案与投放素材、每日市场动态和增长打法。用户问「现在做什么有机会」「这个想法有没有搞头」「谁在做 X、赚到钱没」「这个 App 怎么做起来的、在不在买量」「最近什么在涨」「我的产品怎么拿到用户」、要一份情报日报时使用。
version: 0.11.0
homepage: https://stringers.io
metadata: {"openclaw": {"homepage": "https://stringers.io", "emoji": "🧭"}}
---

# 什么值得做

站在 https://stringers.io 。这是一套聚焦移动应用的商业情报库，由五个互补的数据层组成，按「找方向 → 验产品 → 追变化 → 找打法」串起来：

1. **热门赛道（`list_waves` / `get_wave`）**：近一两年 App Store / Google Play 上先有人做出量、后面持续有人跟进且新进者也能赚到钱（月入 ≥ $1K）的具体方向。这是目前市场上相对有确定性的方向；看一条赛道重点看近 3 个月新进赚钱数、窗口期和后进者凭什么反超。
2. **早鸟新苗子（`list_early_apps`）**：近期上架已经开始赚钱、全库还没见到同款的 0 跟进独苗。这类方向确定性低于赛道，没法一眼下结论，适合挑出几个感兴趣的再用 `get_app` 逐个拆解产品形态、流量来源和可复制性。
3. **App 库（`search_apps` / `list_apps` / `get_app` / `query_sql`）**：约 52 万个 App 的月收入、下载、增长、评分、同开发者矩阵和四平台（Meta / Google / TikTok / Apple）买量素材；高关注度产品附有深度调查稿。用来按一句话模糊找某类 App、按条件拉清单、深扒单个竞品或做 SQL 统计。
4. **市场动态（`feed`）**：每天数据上突然异动的小产品及原因调查，适合捕捉最新变化、解释某个产品为什么这几天火了，或按用户关心的方向整理成情报日报。
5. **打法库（`plays`）**：从大量真实起量案例里归纳出的获客、冷启动与变现招数（含步骤、正反案例），也支持用 `case_q` 直接按获客做法搜实证案例。

## 手里有什么（12 个工具）

接了 `stringer` MCP（`https://stringers.io/mcp/<token>`）：

- `publish_board`：**推荐/盘点/日报必用**。把筛选出的赛道（`wave`）、早鸟（`early`）和具体 App（`app`）打包成一张可交互网页清单（`https://stringers.io/appdb/#b/<id>`），展示图标、月入走势、赛道图标墙、月度进场柱图和 AI 点评；回复开头贴清单页链接，正文重点点名的每个 App 名字上也挂好 `https://stringers.io/appdb/#app/<key>` 详情页链接。
- `research_app`：**一个 App 的全套调研材料**：输入 App Store / Google Play 链接、key 或名字，一次返回库里关于它的全部真值（收入、差评原文、多国榜单、更新日志、四平台广告素材、已有调查稿），并附一张「还需要你自己联网查什么」的清单。只给数据，联网调查和成文由你自己的模型做。
- `compare_apps`：**2–3 款竞品并排对比**。一次传入 2–3 个 App，并发拉取月入、下载、多国主力市场、四平台投放与真实 1–2 星差评原文，直接找出共同痛点、各自优势与市场空白。

- `list_waves`：热门赛道列表（只含已有人跟进的赛道）。默认返回 15 条紧凑高密度行，`detail=true` 附完整分析，`offset` 翻页；`store='ios'|'play'` 筛平台，`category` 筛方向/品类，`q` 支持语义+关键词混合搜并按相关度排。
- `get_wave`：一条赛道的完整档案——定位、分析、逐月进场节奏、全部赚钱成员（标出小团队 / 在投广告数 / 有调查稿）和未过线名单。`key` 支持赛道 key、赛道中文名，或任意成员 App 的 key/链接/名字反查。
- `list_early_apps`：早鸟新苗子列表（0 跟进独苗）。支持 `q` 语义+关键词混合搜、`category` 品类筛、`store` 平台筛、`min_rev` 月入下限、`sort='rv'|'dl'|'rn'|'newest'`、`cloneable_only` 默认排除官方/银行/硬件壳。看中后直接用 `get_app(key)` 逐个深挖。
- `search_apps`：在 52 万个 App 里按一句话或名字模糊搜，按相关度排，自动带出相关赛道；可叠收入、上架时间、小团队、品类等过滤。
- `list_apps`：按条件筛选一批 App 并按收入/增长/新旧排序，开头给总数，支持 `pattern` 全文正则与翻页。
- `get_app`：单个 App 的全维档案。默认精简（月入、下载、增长、评分、支持语言/内购区间/官网、所在赛道、四平台投放状态、调查稿摘要）；`sections` 按需加段：`reviews`（真实用户评论与 1-2 星差评痛点，支持 `review_days` / `review_max_rating`）、`charts`（多国畅销/免费榜单与主力起量国）、`release_notes`（版本更新日志）、`ads`（四平台逐条广告素材与原页链接）、`research`（调查稿全文）、`description`（商店介绍全文）、`developer`（同开发者其他 App）、`daily`（近两周走势）、`wave`（赛道分析）、`all`。传 `check_ads=true` 可当场实时查 Apple + Meta 广告库（约 30 秒）。
- `query_sql`：对 App 库跑只读 DuckDB SQL，算分布、分位数和跨品类统计。
- `feed`：市场动态。不带参数给最新一天，`day` 查某一天，`q` 搜全部历史，`slug` 读完整调查。
- `plays`：打法库。不带参数给全部打法清单，`id='p04'` 读全文，`q` 搜打法；`case_q='正则'` 按获客做法搜数千个真实实证案例，`case_key='<key>'` 读单个案例的完整获客过程。

*(ChatGPT 深度研究 / 只认 `search` + `fetch` 的连接器可使用 `https://stringers.io/mcp/oai/<token>`。)*

## 常用配合

1. **宽泛找方向**：先并发 `list_waves()`（确定性赛道）+ `list_early_apps()`（早鸟新苗子）+ `feed()`（最新异动），挑出值得深挖的用 `get_wave` 和 `get_app` 展开——先基于库里跑出来的真实赛道和产品讨论，再结合用户自身条件做判断。
2. **验具体想法**：`search_apps(query="一句话描述")` + `list_waves(q="...")` 摸清市场上已有谁在做、有没有形成赛道、赚不赚钱，再挑领头和后进者用 `get_app` 看做法与投放。
3. **扒竞品与广告**：`get_app(key="商店链接或名字")` 看精简档案，要逐条广告素材和原页链接加 `sections="ads"`，要调查稿全文加 `sections="research"`。
4. **找获客与变现打法**：先 `plays()` 看归纳好的打法，再用 `plays(case_q="渠道或做法关键词")` 搜真实案例。
5. **整理每日情报日报**：`feed()` 拉最新一天，结合用户关心品类补 `list_waves` / `list_early_apps` 的最新动态。
