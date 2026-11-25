---
name: multilingual-site-build
description: Build or normalize multilingual sites, from locale and market selection through routing, translated content, indexing, existing URL migration and rollback. Use for 多语种站点构建 or i18n site restructuring.
---

# 多语言站点构建与规范化

新站从语言矩阵开始；已有站先盘点实际路由、语言识别、收录与外链、缺译和旧 slug。确认目标语言、默认语言以及历史 URL 能否变更，再实施。沿用同一份项目契约驱动路由、内容和索引。

## 定义上线范围

| Language | Locale | Market | URL segment | Default | Indexable | Coverage |
|----------|--------|--------|-------------|---------|-----------|----------|
| English | `en-US` | Global/US | `en` 或根路径 | 是/否 | 是 | 全量/核心页 |
| Chinese | `zh-CN` | 中国大陆 | `zh-cn` | 是/否 | 是/否 | 全量/核心页 |
| Portuguese | `pt-BR` | 巴西 | `pt-br` | 是/否 | 是 | 全量/核心页 |

规则：

- Language、Locale 与 Market 不能互相代替。
- 同一语言只有内容、价格或法规确实不同，才拆成多个 locale。
- URL segment 一旦发布应稳定，不直接由浏览器 locale 字符串自动生成。
- 没有内容覆盖的 locale 不创建可索引空壳页面。

## 选择公开 URL 并建立路由契约

| 方案 | 示例 | 适用情况 | 主要代价 |
|------|------|----------|----------|
| 子目录 | `example.com/de/pricing` | 同品牌、同平台的大多数内容站和营销站 | 路由与内容统一管理 |
| 子域 | `de.example.com/pricing` | 市场团队、部署或技术栈相对独立 | 权重、监控与部署分散 |
| ccTLD | `example.de/pricing` | 强本地业务、法规或品牌独立 | 成本最高，站点分散 |
| 查询参数 | `example.com/pricing?lang=de` | 临时偏好或兼容入口 | 不适合作为唯一可索引架构 |
| Cookie/JS 切换 | 同一 URL 返回不同语言 | 登录后产品界面 | 公开内容没有稳定语言 URL |

默认从子目录开始评估。只有市场、法规、团队或部署确实独立时，才提高到子域或 ccTLD。

### 3.2 默认语言前缀

两种有效模式：

```text
as-needed： /pricing       /de/pricing
always：    /en/pricing    /de/pricing
```

选择时明确：

- 根路径由哪种语言承载；
- 默认语言未来是否可能变化；
- 是否需要保留现有已收录 URL；
- 新增市场是否要求所有语言对称；
- 框架和 CMS 能否稳定生成 canonical、Sitemap 与内链。

不得同时让 `/pricing` 和 `/en/pricing` 作为同一内容的可索引版本。选定一种 canonical 形态，另一种必须重定向或不生成。

### 3.3 URL 契约

| Route key | Default URL | Locale URL pattern | Missing translation | Indexable |
|-----------|-------------|--------------------|---------------------|-----------|
| homepage | `/` | `/{locale}` | 不发布空壳 | 是 |
| pricing | `/pricing` | `/{locale}/pricing` | 回退或隐藏，显式决定 | 是 |
| legal | `/terms` | `/{locale}/terms` | 按法律市场要求 | 是 |
| app | `/app` | 产品内 locale 状态另行决定 | 不适用 | 按项目 |

URL 段不必逐字翻译，但必须稳定、唯一并能在语言间互相映射。

## 实现路由与内容层

### 4.1 渲染要求

| 页面类型 | 最低要求 |
|----------|----------|
| 公开营销页、Blog、帮助中心 | 每个 locale 有稳定 URL，首响 HTML 含对应语言正文和 head |
| 登录后产品 | 可以客户端切换，但刷新、深链和账户偏好必须可恢复 |
| 混合站点 | 公开页使用路由级 locale，产品界面可叠加账户偏好 |

不要用纯客户端语言状态替代公开页面的 locale URL。

### 4.2 框架与 i18n 层

优先保留现有框架，除非它无法满足稳定 URL、SSR/SSG 或内容管理要求。不要为了引入 i18n 顺手更换 UI 生态。

| 技术栈 | 规划重点 |
|--------|----------|
| Next.js | App Router 的 `[locale]` 边界、middleware/路由配置、静态参数、Metadata 和内容加载 |
| Nuxt | i18n 模块或项目路由规则、默认语言策略、Nitro/SSG 输出和 SEO head |
| Astro | i18n routing、locale 内容集合、静态路径生成和岛屿边界 |
| Vite SPA | 适合登录后产品；公开多语言内容通常需要预渲染或迁到 SSR/SSG 框架 |
| Headless CMS | locale 字段、fallback、发布状态、预览和 webhook 重建策略 |

选择具体 i18n 库前确认：

1. 支持选定的默认语言前缀模式；
2. 支持服务端和构建期取词；
3. 能生成稳定 locale 路由；
4. middleware 适配部署平台；
5. locale 标识与 CMS/TMS 一致；
6. 缺翻译时能显式失败或按契约 fallback；
7. 语言切换器输出真实链接，而不只是改客户端状态。

### 4.3 内容存储

| 内容类型 | 规划方式 |
|----------|----------|
| UI 短文本 | 按 locale 分离的结构化消息文件，校验键集合 |
| 营销页面 | 按 route key + locale 组织，以 schema 约束字段 |
| Blog/长内容 | 每个 locale 独立文件或 CMS entry，允许发布状态不同 |
| 法律与市场内容 | 与 Market 绑定，不自动从默认语言 fallback |

构建或 CI 至少校验：locale 合法性、消息键缺失、重复 slug、路由冲突、未发布内容进入 Sitemap，以及 canonical URL 是否可生成。

## 切换既有 URL（仅架构变化时）

| Old URL | Locale | New URL | Action | Canonical target | Verified |
|---------|--------|---------|--------|------------------|----------|
| `/?lang=de` | `de` | `/de` | 永久重定向 | `/de` | 否 |
| `/pricing?lang=de` | `de` | `/de/pricing` | 永久重定向 | `/de/pricing` | 否 |

URL 架构变化属于显式迁移决策，不作为框架迁移的附带清理。必须同时更新重定向、canonical、hreflang、Sitemap、内链和语言切换器，并保留可回滚配置。

## 验证并交接

以 URL 契约生成测试样本，分别覆盖默认语言、非默认语言、缺译以及历史入口。抓取首响正文和 head，检查语言、canonical、hreflang 的互返关系、Sitemap 和索引状态。实际点击切换器、刷新和深链，核对落点和内容。对旧入口检查最终地址、状态码、跳转次数与循环。

交付已填写的项目契约、部署与内容加载选择、验证结果和遗留问题。发生 URL 迁移时，附实测映射、触发回滚的条件、恢复配置及负责人。
