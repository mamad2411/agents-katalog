---
name: mulan-paper-skill
version: "1.0.0"
description: 查询木兰论文解读（paper.mulanai.com）的 AI 论文中文解读、每日精选、周报与主题分类。当用户询问最新 AI 论文、每日论文精选、某主题论文、论文中文摘要或推荐理由时使用。全部接口匿名只读、无需 API Key。
---

# 木兰论文解读 Skill

木兰论文解读（https://paper.mulanai.com）提供每日 AI 论文精选、中文摘要、推荐理由、主题分类与周报。本 Skill 通过其公开只读 API 与 RSS 查询内容。

## 基本信息

- Base URL：`https://paper.mulanai.com`
- 认证：无需 token，仅匿名 GET
- 格式：JSON（REST）/ RSS 2.0 XML（feed）
- 建议设置自定义 User-Agent 自报客户端名称，便于排障

## 端点

### 每日精选

| 端点 | 用途 |
|---|---|
| `GET /api/v1/digests/dates` | 有解读的日期列表（倒序） |
| `GET /api/v1/digests/daily?date=YYYY-MM-DD` | 某日精选论文卡片列表 |

### 周报

| 端点 | 用途 |
|---|---|
| `GET /api/v1/digests/weeks` | 可用 ISO 周列表 |
| `GET /api/v1/digests/weekly?year=&week=` | 某周周报，按日分组 |

### 主题

| 端点 | 用途 |
|---|---|
| `GET /api/v1/digests/topic-names` | 主题名 + 论文计数（轻量） |
| `GET /api/v1/digests/by-topic?topic=主题名` | 某主题下论文卡片（topic 需 URL 编码） |

### 检索与全文

| 端点 | 用途 |
|---|---|
| `GET /api/v1/digests/articles/search?q=关键词` | 站内检索，按相关性排序 |
| `GET /api/v1/digests/articles/{id}` | 单篇完整解读（含 content_md 全文 markdown） |

### RSS

| 地址 | 内容 |
|---|---|
| `/feed.xml` | 精选摘要，最新 50 条（推荐默认订阅） |
| `/feed/full.xml` | 精选全文，content:encoded 内联正文 |
| `/feed/daily.xml` | 日报，每天一期，保留最近 30 期 |
| `/feed/topic/{topic}.xml` | 主题订阅（topic 需 URL 编码） |

RSS 支持 ETag 条件请求，未变化返回 304；建议每 30 分钟或更慢轮询。

## 卡片字段

`daily` / `by-topic` / `search` 返回的论文卡片字段：

- `id`：站内文章 ID，用于 `/articles/{id}` 取全文与拼接站内链接
- `arxiv_id`、`title`、`authors`、`pub_date`
- `topic`：主题分类；`tags`：话题标签数组
- `summary_zh`：中文摘要；`reason_zh`：推荐理由
- `pdf_url`、`arxiv_url`：原始论文入口

## 典型工作流

1. **"最近有什么值得看的 AI 论文？"**
   先 `GET /api/v1/digests/dates` 取最新日期，再 `GET /api/v1/digests/daily?date=<最新日期>`，按 `reason_zh` 挑 5 条以内呈现。
2. **"讲讲某篇论文"**
   用 `search?q=` 找到 `id`，再 `GET /api/v1/digests/articles/{id}` 读 `content_md` 全文后总结。
3. **"某主题（如 Agent）近期有哪些论文？"**
   `GET /api/v1/digests/by-topic?topic=<URL 编码主题>`，按 `pub_date` 倒序呈现。

## 输出要求

- 回答注明时间窗（如"2026-07-24 精选"）。
- 标题链接到站内阅读页：`https://paper.mulanai.com/article/{id}`。
- 保留"木兰论文解读"署名；第三方原文版权归原作者，引用数字或原话前用 `arxiv_url` 回原文核对。
- 中文呈现，每条给出一句中文摘要或推荐理由。
