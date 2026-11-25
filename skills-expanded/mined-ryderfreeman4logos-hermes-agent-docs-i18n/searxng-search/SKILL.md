---
name: searxng-search
description: Free keyless meta-search aggregating 70+ engines.
version: 1.0.1
author: hermes-agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [search, searxng, meta-search, self-hosted, free, fallback]
    related_skills: [duckduckgo-search, domain-intel]
    fallback_for_toolsets: [web]
---

# SearXNG 搜索功能

基于 [SearXNG](https://searxng.org/) 提供的免费元搜索服务——这是一款注重隐私的自托管搜索聚合工具，可同时查询70多种搜索引擎。

使用公共实例时**无需 API 密钥**。如需完全掌控搜索功能，也可选择自托管方式。当未配置主要网络搜索工具集（`FIRECRAWL_API_KEY`）时，该功能会自动作为备用选项出现。

## 配置说明

SearXNG 需要一个名为 `SEARXNG_URL` 的环境变量，用于指定您的 SearXNG 实例地址：

```bash
# Public instances (no setup required)
SEARXNG_URL=https://searxng.example.com

# Self-hosted SearXNG
SEARXNG_URL=http://localhost:8888
```

如果未配置任何实例，则该技能将不可用，代理会转而使用其他搜索选项。

## 检测流程

在选择具体方法之前，请先确认实际可用的资源。

```bash
# Check if SEARXNG_URL is set and the instance is reachable
curl -s --max-time 5 "${SEARXNG_URL}/search?q=test&format=json" | head -c 200
```

决策流程：
1. 若已设置 `SEARXNG_URL` 且实例能够响应，则使用 SearXNG。
2. 若未设置 `SEARXNG_URL` 或无法连接该地址，则转而使用其他可用的搜索工具。
3. 若用户明确要求使用 SearXNG，则协助其搭建实例或查找公共实例。

## 方法 1：通过 curl 调用 CLI（推荐方式）

通过“终端”使用 `curl` 命令来调用 SearXNG 的 JSON API。这种方式无需假设系统中已安装特定的 Python 包。

```bash
# Text search (JSON output)
curl -s --max-time 10 \
  "${SEARXNG_URL}/search?q=python+async+programming&format=json&engines=google,bing&limit=10"

# With Safesearch off
curl -s --max-time 10 \
  "${SEARXNG_URL}/search?q=example&format=json&safesearch=0"

# Specific categories (general, news, science, etc.)
curl -s --max-time 10 \
  "${SEARXNG_URL}/search?q=AI+news&format=json&categories=news"
```

### 常用 CLI 参数

| 参数 | 描述 | 示例 |
|------|-------------|---------|
| `q` | 查询字符串（需进行 URL 编码） | `q=python+async` |
| `format` | 输出格式：`json`、`csv`、`rss` | `format=json` |
| `engines` | 以逗号分隔的引擎名称 | `engines=google,bing,ddg` |
| `limit` | 每个引擎返回的最大结果数（默认为 10） | `limit=5` |
| `categories` | 按类别筛选 | `categories=news,science` |
| `safesearch` | 0=无限制，1=适度限制，2=严格限制 | `safesearch=0` |
| `time_range` | 筛选时间范围：`day`、`week`、`month`、`year` | `time_range=week` |

### 解析 JSON 结果

```bash
# Extract titles and URLs from JSON
curl -s --max-time 10 "${SEARXNG_URL}/search?q=fastapi&format=json&limit=5" \
  | python3 -c "
import json, sys
data = json.load(sys.stdin)
for r in data.get('results', []):
    print(r.get('title',''))
    print(r.get('url',''))
    print(r.get('content','')[:200])
    print()
"
```

每个搜索结果返回的字段包括：`title`、`url`、`content`（摘要）、`engine`、`parsed_url`、`img_src`、`thumbnail`、`author`以及`published_date`。

## 方法 2：通过 `requests` 调用 Python API

利用 `requests` 库直接从 Python 程序调用 SearXNG 的 REST API：

```python
import os, requests, urllib.parse

base_url = os.environ.get("SEARXNG_URL", "")
if not base_url:
    raise RuntimeError("SEARXNG_URL is not set")

query = "fastapi deployment guide"
params = {
    "q": query,
    "format": "json",
    "limit": 5,
    "engines": "google,bing",
}

resp = requests.get(f"{base_url}/search", params=params, timeout=10)
resp.raise_for_status()
data = resp.json()

for r in data.get("results", []):
    print(r["title"])
    print(r["url"])
    print(r.get("content", "")[:200])
    print()
```

## 自主托管 SearXNG

如需运行属于自己的 SearXNG 实例：

```bash
# Using Docker
docker run -d -p 8888:8080 \
  -v $(pwd)/searxng:/etc/searxng \
  searxng/searxng:latest

# Then set
SEARXNG_URL=http://localhost:8888
```

或者通过 pip 安装：
```bash
pip install searxng
# Edit /etc/searxng/settings.yml
searxng-run
```

公开的 SearXNG 实例地址如下：
- `https://searxng.example.com`（可替换为任意其他公开实例）

## 工作流程：先搜索再提取

SearXNG 返回的是标题、URL 以及内容片段，而非整页内容。若需获取完整页面内容，需先进行搜索，然后使用 `web_extract`、浏览器工具或 `curl` 来提取最相关的 URL。

```bash
# Search for relevant pages
curl -s "${SEARXNG_URL}/search?q=fastapi+deployment&format=json&limit=3"
# Output: list of results with titles and URLs

# Then extract the best URL with web_extract
```

## 局限性

- **实例可用性**：如果 SearXNG 实例处于关闭状态或无法访问，搜索将失败。请务必确认已设置 `SEARXNG_URL` 且该实例可正常访问。
- **无内容提取功能**：SearXNG 只能返回摘要信息，而非完整页面内容。如需获取全文，请使用 `web_extract`、浏览器工具或 `curl`。
- **速率限制**：部分公共实例会对请求量进行限制，而自托管则可避免此问题。
- **引擎支持情况**：可用的搜索引擎取决于 SearXNG 实例的配置，某些引擎可能被禁用。
- **结果更新频率**：元搜索工具会聚合多个外部引擎，因此结果的新鲜度取决于这些引擎的表现。

## 故障排除

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 未设置 `SEARXNG_URL` | 未配置实例 | 使用公共 SearXNG 实例或自行搭建实例 |
| 连接被拒绝 | 实例未运行或 URL 错误 | 检查 URL 是否正确以及实例是否正在运行 |
| 返回空结果 | 实例阻止了查询请求 | 尝试使用其他实例或选择自托管方案 |
| 响应速度慢 | 公共实例负载过高 | 选择自托管方式或使用负载较低的公共实例 |
| 不支持 `json` 格式 | SearXNG 版本过旧 | 尝试使用 `format=rss` 格式或升级 SearXNG |

## 常见陷阱

- **务必设置 `SEARXNG_URL`**：若未设置该参数，该技能将无法正常运行。  
- **对查询参数进行 URL 编码**：在使用 curl 时需对空格及特殊字符进行编码，或在 Python 中使用 `urllib.parse.quote()` 函数处理。  
- **指定 `format=json` 参数**：默认的输出格式可能无法被机器读取，因此务必明确请求 JSON 格式的数据。  
- **设置超时时间**：请始终使用 `--max-time` 或 `timeout=` 参数，以避免在无法连接的实例上卡住。  
- **自行托管最为可靠**：公共实例可能会出现故障、被限制访问频率或被屏蔽，而自行托管的实例则更加稳定可靠。  

## 实例查找  

如果未设置 `SEARXNG_URL`，且用户询问有关 SearXNG 的信息，请协助他们：  
1. 找到一个公共的 SearXNG 实例（可搜索“public searxng instance”）；  
2. 使用 Docker 或 pip 自行搭建实例。  

各类公共实例的列表可访问：https://searxng.org/
