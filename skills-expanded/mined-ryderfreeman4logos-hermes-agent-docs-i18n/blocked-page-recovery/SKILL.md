---
name: blocked-page-recovery
description: "Use when a fetch fails: 403/429, paywall, WAF, bot wall."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Research, Archives, Wayback, Paywall, WAF, Fallback]
    related_skills: [grounded-citations]
---

# 被屏蔽页面的恢复方法

当某个页面无法加载时——出现 403/429 错误、Cloudflare 的“稍候…”提示、付费墙，或是机器人检测弹窗——请不要放弃，也不要反复尝试同一个网址。通常第三方服务会保存该页面的**副本**。可以按以下顺序尝试，从成本最低的方法开始。

## 恢复步骤

```
1. Wayback Machine  — archive.org "available" API  (snapshot + timestamp)
2. archive.today    — domain rotation: archive.ph → .md → .li → .is
3. Jina Reader      — only if JINA_API_KEY is set  (live server-side render)
4. API-first pivot  — look for /api/, /graphql, .json, or RSS on the same host
5. Real browser     — browser tool as the last, most expensive resort
```

使用附带的脚本一次性运行它：

```bash
python3 scripts/recover_page.py "https://example.com/blocked-article" --json
```

该脚本会按顺序尝试每条检索路径，对每个返回的结果进行验证（详见下文的“虚假成功案例”），并输出首个真实有效的结果及其来源信息。

## 来源标识规范（必须严格遵守）

所有获取到的内容均带有来源标识，在引用时**必须保留**这些信息：

| 检索路径 | 来源标识 | 引用方式 |
|---------|---------|---------|
| Wayback / archive.today | `snapshot` | 需注明快照日期，例如：“存档于2026-08-06”。切勿将快照内容当作实时页面使用——因为它可能已过时。 |
| Jina Reader | `live` | 通过服务器端重新渲染实时页面，按常规方式引用即可。 |
| 直接获取实时内容 / 浏览器 | `live` | 按常规方式引用即可。 |

如果用户需要*最新*数据（如价格、库存状态、突发新闻），快照仅能作为背景参考，而非最终答案——应明确说明这一点，并注明快照的时效性。

## 手动检索路径

### 1. Wayback Machine（来源最可靠，优先尝试）

```bash
# Discovery: returns closest snapshot URL + timestamp as JSON
curl -sL "https://archive.org/wayback/available?url={URL}"
# Then fetch archived_snapshots.closest.url
```

在需要枚举大量快照（或恢复已删除的页面）时，CDX 索引：

```bash
curl -sL "https://web.archive.org/cdx/search/cdx?url={URL}&output=json&limit=10"
```

在负载较高时，CDX 会偶尔返回 503 错误——遇到这种情况，请转而使用 `available` API，切勿频繁重试。

适用场景：所有可公开爬取的网址。不适用场景：被机器人屏蔽的网站、从未被爬取过的网址，以及仅基于 JavaScript 的单页应用（因其快照无法正常渲染）。

### 2. archive.today（付费墙与已删除内容）

该平台提供用户上传的存档内容——其中往往包含 Wayback Machine 所没有的带付费墙的新闻文章。但其会严格实施速率限制（返回 429 错误），并且还会不断更换域名，因此需要不断尝试不同的访问方式。

```bash
for d in archive.ph archive.md archive.li archive.is; do
  curl -sL --max-time 20 "https://$d/newest/{URL}" -o /tmp/page.html \
    -w "%{http_code}" && break
done
```

**应验证内容体，而非状态码**——即便返回 429 状态码，服务器仍会传输数 KB 的速率限制相关 HTML 内容，仅从大小检查来看，这些内容似乎属于成功响应。

### 3. Jina Reader（需提供 JINA_API_KEY）

`r.jina.ai` 会在服务器端使用真实浏览器重新渲染目标网页，并以 Markdown 格式返回结果。匿名访问已不可用（会返回 401 错误并跳转至 Turnstile 系统）；使用时必须提供 API 密钥：

```bash
curl -s -H "Authorization: Bearer $JINA_API_KEY" "https://r.jina.ai/{URL}"
```

能够处理那些归档工具无法处理的 JS 单页应用。如果相关环境变量未被设置，则应完全跳过该路由。

### 4. 以 API 优先的策略

Web 应用防火墙对 HTML 页面的保护力度远远大于其背后的数据接口。当某个网站遭到 2-3 次拦截尝试后，应停止尝试直接处理 HTML 页面，转而寻找以下内容：

- 页面 URL 的 `/api/...`、`/graphql` 或 `.json` 变体
- RSS/Atom 订阅源（如 `/feed`、`/rss`，或是从任何可获取的页面副本中找到的 `<link rel="alternate">` 标签）
- 显示标准 URL 的站点地图（`/sitemap.xml`），这些 URL 可能并未被设置访问限制

## 虚假的成功响应——那些会欺骗你的路由

这类路由会返回 HTTP 200 状态码，并附带看似正常的页面内容，但实际上并非目标页面。脚本会自动拒绝此类请求，建议也手动将其过滤掉：

- **Google 缓存已失效**（自 2024 年年中起）。`webcache.googleusercontent.com` 会返回 200 状态码及数十 KB 的内容，但这其实是 Google 搜索界面中的临时页面，通过 JS 实现重定向，并非真正的缓存内容。切勿将其视为有效数据。
- **AMP 缓存**（`*.cdn.ampproject.org`）通常会返回一个约 300 字节的 `<title>Redirecting</title>` 元刷新标记，指向被拦截的原始 URL。若将其视为成功响应，会导致无限循环请求。
- **限流提示页面**：archive.today 的 429 错误页面为数 KB 级别的 HTML 内容。应检查目标页面的实际内容（如标题文字、预期字符串），而不仅仅是文件大小。

脚本所采用的检测规则包括：每条路由的响应内容字节数低于设定阈值；元刷新/JS 重定向标记的目标地址为原始主机；页面标题包含“稍候”、“正在重定向”、“Google 搜索”或“需要注意”等字样。

## 代理中转：请避免使用

常规的“网络代理”中继在架构上本质上属于中间人类型。切勿通过此类代理传输 Cookie 或 Authorization 请求头，也不应将其用于任何用户需要依赖其真实性的场景——因为其数据来源根本无法被验证。相比之下，归档服务更为可靠，至少它们会对存储的内容添加时间戳。
