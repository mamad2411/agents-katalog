---
name: web-search-plus
description: 智能多引擎搜索技能，聚合 Serper/Tavily/Exa/Perplexity/You.com/SearXNG 等多个搜索引擎结果
metadata:
  tags: search, multi-engine, aggregation
---

# web-search-plus

智能多引擎搜索技能，聚合多个搜索引擎结果。

## 支持的搜索引擎

- Serper (Google)
- Tavily
- Exa
- Perplexity
- You.com
- SearXNG

## 使用方法

```bash
# 智能搜索
web-search-plus "搜索关键词"
```

## 配置

需要在 `TOOLS.md` 或环境变量中配置相关 API Key：

- `SERPER_API_KEY`
- `TAVILY_API_KEY`
- `EXA_API_KEY`
- `PERPLEXITY_API_KEY`

## 说明

此 skill 会自动选择可用的搜索引擎，聚合返回最佳结果。
