---
name: web-search-cce
description: 网络搜索策略。当需要搜索网络信息、查询最新资料、查找技术文档、或选择搜索工具时，必须使用此技能。定义了多层搜索工具优先级链，同层并发、失败即降级。
---

> 来自 [cc-enhance](https://github.com/luochang212/cc-enhance)。`-cce` 后缀表示此技能由 cc-enhance 项目安装，避免与本地同名技能冲突。

# 网络搜索

## 核心原则

1. **先读注册表**。`~/.claude/tool-registry.json` 记录了每个工具的实测状态。
2. **同层并发**。独立通道同时发起，谁先返回用谁。
3. **失败即降级，不重试**。一个工具失败一次就跳到下一层。

## 优先级链

### Tier 0 — 直接 URL

用户给了 URL 或你知道目标地址 → 不搜索，直接提取页面内容。优先用内置 `WebFetch`（<1s，覆盖 90% 页面）；JS 渲染/反爬页面用 Crawl4AI（需 Python 环境）；Crawl4AI 超时或被检测时降级到原生 Playwright 拿 `inner_text`。

### Tier 1 — WebSearch（内置，零配置）

`WebSearch` 是 Claude Code 内置工具，零依赖、零成本、结构化返回。始终最先尝试。失败（如当前模型不支持）则立即降级到 Tier 2。

### Tier 2 — Tavily / SearXNG（并列）

**Tavily** — ~0.6s 响应，JSON 结构化返回，不限频，英中文均可。1000 次/月。

→ [references/tavily.md](references/tavily.md)

**SearXNG** — 自部署 Docker，零额度限制，~3s 响应，中文 18 条/Tavily 5 条。

→ [references/searxng.md](references/searxng.md)

### Tier 3 — web_search_prime MCP

域名过滤、时效性、内容长度控制优于 Tavily。有月额度，备选。

→ [references/web-search-prime.md](references/web-search-prime.md)

### Tier 4 — DuckDuckGo（兜底）

纯免费但 ~2s、HTML 需解析、限频。仅在前三层全部不可用时使用，降级前告知用户。

→ [references/duckduckgo.md](references/duckduckgo.md)

## 降级流程

```
需要搜索
  ├─ WebSearch (内置)           ──失败──┐
  │                                   ▼
  ├─ Tavily curl (Bash)      ──失败──┐
  ├─ SearXNG (本地 Docker)    ──失败──┤
  │                                   ▼
  ├─ web_search_prime MCP     ──失败──┐
  │                                   ▼
  └─ DuckDuckGo curl           ── 兜底
```

搜索拿到 URL 后，提取页面内容：优先 `WebFetch`（内置，<1s）→ JS 重/反爬页用 Crawl4AI（`magic=True` 解微信）→ 超时或被检测时降级到原生 Playwright（`wait_until=commit`）。

## 结果展示

**每条搜索结果必须附带链接**，让用户能直接点开看原文。格式：

```
1. **标题** — 来源
   🔗 https://...
```

## 维护

工具状态变更时更新 `~/.claude/tool-registry.json`。

## 环境依赖

| 依赖 | 用途 | 安装方式 | 磁盘 | 必需 |
|------|------|----------|------|------|
| Tavily API Key | 首选搜索，~0.6s，1000次/月 | 注册 [tavily.com](https://tavily.com) → `export TAVILY_API_KEY=xxx` | 0 | 否 |
| ddgs | 兜底搜索，防 CAPTCHA | `pip install ddgs` | ~1MB | 否 |
