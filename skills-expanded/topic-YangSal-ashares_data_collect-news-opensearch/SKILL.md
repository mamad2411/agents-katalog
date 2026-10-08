---
name: news-opensearch
description: |
  A股新闻 OpenSearch 库的查询与分析技能。库内含四通道新闻数据（快讯 flash/新闻联播
  cctv/公司公告 announcement/个股新闻 stock，2 万+ 文档持续增长），支持 BM25 关键词、
  kNN 语义、hybrid 混合三种检索与聚合分析。当需要检索/统计/分析 A 股新闻舆情、公告、
  个股消息面时使用。适用于任何智能体（Claude/Hermes 等）——本文档自包含。
---

# A 股新闻库（OpenSearch）使用手册

## 1. 连接信息

| 项 | 值 |
|---|---|
| 端点 | `https://192.168.9.12:9200`（自签证书，客户端需关闭证书校验） |
| 只读账号 | `news_reader` / 密码见部署方（建置见 `docs/deploy/news-reader-account.md`） |
| 读入口 | 统一用别名 **`news`**（物理索引按年 `news-2026`、`news-2027`…，别名聚合全部） |
| 查询向量服务 | Ollama `http://192.168.9.12:11434`（内网免鉴权），模型 `bge-m3`，1024 维 |

Python 连接示例：

```python
from opensearchpy import OpenSearch
client = OpenSearch(
    hosts=[{"host": "192.168.9.12", "port": 9200}],
    http_auth=("news_reader", ",
    use_ssl=True, verify_certs=False, ssl_show_warn=False,
)
```

若在 data_collect 仓库环境内，直接用现成封装（读 config.yaml 凭据）：
```python
from data_collect.utils.news_search import search_news
search_news("锂电池 产能扩张", top_k=10, channel="stock", mode="hybrid")
# → {"total": N, "hits": [{title, source, channel, pub_time, url, score, highlight}, ...]}
```

## 2. 数据模型（一篇新闻 = 一个文档）

| 字段 | 类型 | 含义与注意 |
|---|---|---|
| `channel` | keyword | 通道：`flash` 快讯 / `cctv` 联播 / `announcement` 公告 / `stock` 个股新闻 / `marker` 系统标记（**分析时务必排除**） |
| `source` | keyword | 数据源：cls/em（快讯）、cctv、cninfo（公告）、em_stock（个股） |
| `title` | text(中文分词) | 标题（清洗后） |
| `content` | text(中文分词) | 摘要/正文：快讯=全文、联播=全文、公告=标题、个股=~130字摘要 |
| `body` | text | **全文**（个股=网页正文、公告=PDF 正文，截断 5 万字），部分文档尚无（抽取进行中/失败） |
| `pub_time` | date | 发布时间，格式 `"YYYY-MM-DD HH:MM:SS"`（北京时间），range 查询用它 |
| `stocks` | keyword[] | 关联股票代码，如 `["600519.SH","000001.SZ"]`——个股/公告最全，快讯为标题打标 |
| `url` | keyword | 原文链接（公告为 PDF 链接） |
| `content_vec` | knn_vector(1024) | bge-m3 语义向量（编码 title+全文前 3000 字，L2 归一） |
| `vec_status` | keyword | `done`=有向量可 kNN；`pending`=刚入库还没编码（小时级补齐） |
| `ann_type`/`pdf_status`/`body_status`/`body_truncated` | keyword/bool | 公告类型(暂空)/公告PDF抽取状态/个股全文抽取状态/全文被截断标记 |

**三个坑**：
1. 聚合/排序 `body_status` 时用 **`body_status.keyword`**（该字段在 news-2026 是 text）；`channel`/`vec_status`/`pdf_status`/`stocks` 直接用即可。
2. 一定加 `must_not: {term: {channel: "marker"}}` 或显式指定 channel——marker 是系统标记文档，不是新闻。
3. 跨票重复：同一篇文章只存一份、`stocks[]` 挂全部相关标的——按 `stocks` 过滤即得某票全部相关新闻（含板块联动文章）。

## 3. 三种检索

### 3.1 BM25 关键词（无需向量，最快）
```json
POST news/_search
{
  "query": {"bool": {
    "must": [{"multi_match": {"query": "回购 增持", "fields": ["title^2", "content", "body"]}}],
    "filter": [
      {"term": {"channel": "announcement"}},
      {"range": {"pub_time": {"gte": "2026-07-01 00:00:00", "lte": "2026-07-07 23:59:59"}}}
    ]
  }},
  "size": 10, "_source": ["title", "pub_time", "stocks", "url"]
}
```

### 3.2 kNN 语义（同义/近义/口语化查询也能命中）
先把查询文本编成向量（Ollama），再 kNN：
```python
import requests
vec = requests.post("http://192.168.9.12:11434/api/embed",
                    json={"model": "bge-m3", "input": ["白酒企业业绩与消费回暖"]},
                    timeout=120).json()["embeddings"][0]

body = {
  "size": 10,
  "query": {"knn": {"content_vec": {"vector": vec, "k": 10,
      "filter": {"bool": {"must": [{"term": {"channel": "stock"}}]}}}}},
  "_source": ["title", "pub_time", "stocks", "url"],
}
client.search(index="news", body=body)
```
实测效果：查「白酒企业业绩与消费回暖」（不含任何原词）→ 命中「端午白酒动销平淡…茅台能否率先筑底」(0.79)。

### 3.3 hybrid 混合（BM25+kNN 融合，检索质量最好）
同 kNN 构造向量，查询体换 hybrid 并带 `search_pipeline` 参数：
```python
body = {
  "size": 10,
  "query": {"hybrid": {"queries": [
      {"bool": {"must": [{"multi_match": {"query": "锂电池 产能扩张",
           "fields": ["title^2", "content", "body"]}}],
        "filter": [{"term": {"channel": "stock"}}]}},
      {"knn": {"content_vec": {"vector": vec, "k": 50,
        "filter": {"term": {"channel": "stock"}}}}}
  ]}},
}
client.search(index="news", body=body, params={"search_pipeline": "news-hybrid"})
```

## 4. 分析配方

**某票近 7 日消息面**（个股新闻+公告一把抓）：
```json
{"query": {"bool": {"filter": [
    {"terms": {"channel": ["stock", "announcement"]}},
    {"term": {"stocks": "600519.SH"}},
    {"range": {"pub_time": {"gte": "now-7d/d"}}}]}},
 "sort": [{"pub_time": "desc"}], "size": 50,
 "_source": ["pub_time", "channel", "title", "url"]}
```

**每日各通道量趋势**（数据健康度/新闻热度）：
```json
{"size": 0, "query": {"bool": {"must_not": [{"term": {"channel": "marker"}}]}},
 "aggs": {"day": {"date_histogram": {"field": "pub_time", "calendar_interval": "day"},
   "aggs": {"ch": {"terms": {"field": "channel"}}}}}}
```

**热门标的榜**（近 3 日被新闻提及最多的股票）：
```json
{"size": 0, "query": {"bool": {"filter": [
    {"term": {"channel": "stock"}}, {"range": {"pub_time": {"gte": "now-3d/d"}}}]}},
 "aggs": {"hot": {"terms": {"field": "stocks", "size": 20}}}}
```

**取全文做 NLP/摘要**：过滤 `exists: {field: "body"}` 取 `body`；无 body 的退回 `content`（摘要永远在）。

## 5. 边界与礼仪

- 本账号**只读**：任何写操作 403 属预期，不要重试。
- 大结果集用 `size` 分页或 `search_after`，别一次拉全库；聚合优先于全量拉取。
- 数据新鲜度：快讯 15 分钟级；个股新闻每晚 22:00；公告 20:40；全文/向量小时级补齐（`vec_status=pending` 的新文档暂无向量，BM25 仍可查）。
- `body` 在 2026 年索引为 standard 分词（中文按单字），关键词查 body 精度略降——优先 title/content 字段，或用语义检索。
