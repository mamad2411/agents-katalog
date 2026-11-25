---
name: exa-search
description: '[功能] 需要高质量外部搜索/调研时使用。触发条件：web_search 不可用或需要英文语义搜索、技术/商业调研、多源交叉验证。含 EXA REST/MCP 双路径调用法与渠道质量速查表。'
---

# EXA 高质量搜索

> 背景：当运行环境的内置 web_search 不可用或质量不足时，可用本 skill 的直调路径补位，效果等同插件接入。

## 1. 调用路径（按优先级）

### 路径 A：内置 web_search 工具
搜索插件接入后 `web_search` 自动走 Exa（provider 配置见 harness 设置）。先试它，能用就用。

### 路径 B：REST 直调（带 Key，额度高）
```powershell
$key = [Environment]::GetEnvironmentVariable('EXA_API_KEY','User')  # 或从 {AOS_ROOT}/04_MEMORY/credentials.json（utf-8-sig）读
$body = ConvertTo-Json @{query='...'; numResults=8}   # 可加 type/category/crawl 的 contents
Invoke-RestMethod -Uri 'https://api.exa.ai/search' -Method Post -ContentType 'application/json' -Headers @{'x-api-key'=$key} -Body $body
```

### 路径 C：匿名 MCP（零 Key 兜底，限流）
POST `https://mcp.exa.ai/mcp`（JSON-RPC 2.0，`tools/call web_search_exa`，Header `x-exa-source: <client>`，Accept 含 text/event-stream）。无凭证，429 时换路径 B。

## 2. 渠道质量速查（实测）

| 渠道 | 质量 | 备注 |
|---|---|---|
| EXA（英文查询） | 高 | 语义搜索；**CJK 查询大面积失效**（半数退化为问号/无关页）——中文题先转英文或拆关键词，再用 web_fetch 抓中文源直取 |
| web_fetch 直取 URL | 高 | 已知 URL 一律直取拿一手 |
| 本机实测（SQL/HEAD/API 探测） | 最高 | 能实测不搜索 |
| DuckDuckGo html 端点 | 中 | 引号精确查询会被反爬吞（返回空=可疑） |
| Bing 国内版 | 低 | 频繁返回无关结果，仅作最后手段 |

## 3. gotchas

- credentials.json 是 **UTF-8 带 BOM**：Python 读必须 `encoding='utf-8-sig'`，否则 JSON 解析失败被误诊为文件损坏（多环境共记坑）
- EXA CJK 失效是查询串层面问题，换英文措辞即可绕开；中文圈定性调研（处罚案例/社区口碑）仍是短板，结论需标注来源等级
- 匿名 MCP 返回 SSE 格式（`event: message\ndata: {...}`），解析取 `data:` 后 JSON
- 调研结论必须带来源 URL + 时间；二手指南需检查其引用的一手文件再采信
- EXA key 引用 `{AOS_ROOT}/04_MEMORY/credentials.json` 中登记的 id（勿复制值到文档）
