---
name: scrapling-stealth
description: |
  自适应反检测抓取框架（D4Vinci/Scrapling）：三级 fetcher 光谱（TLS 指纹伪装 HTTP → Playwright 动态 → StealthyFetcher 隐身处理公开页面的 Cloudflare Turnstile/Interstitial 中间盾）；解析器可 auto_save 学习元素特征、网站改版后 adaptive=True 相似度重定位选择器；Spider 框架提供 AutoThrottle 自适应限速、代理轮换、robots_txt_obey、Ctrl+C 断点续爬，并能 capture_xhr 直取页面后台 API 数据。
  当用户说「站点有 Cloudflare 人机验证爬不动」「requests 被 403 封禁」「网站改版选择器全失效」「要代理轮换+自动限速的大规模采集」时使用。
  不适用于：无反爬压力的常规公开页面（转 crawl4ai-scraping）；PDF 文件本体解析（转 odl-pdf-extraction）；绕过登录墙/付费墙/验证码的需求（应拒绝）。
source_project: D4Vinci/Scrapling
tags: [scrapling-stealth, anti-bot, adaptive-parsing, stealth-fetching, spider-framework, 蒸馏技能]
---

# Scrapling Stealth · 自适应隐身抓取框架

## R (Reading) — 上游原文

> "Scrapling is an adaptive Web Scraping framework that handles everything from a single request to a full-scale crawl. Its parser learns from website changes and automatically relocates your elements when pages update. Its fetchers bypass anti-bot systems like Cloudflare Turnstile out of the box. And its spider framework lets you scale up to concurrent, multi-session crawls with pause/resume, automatic proxy rotation, and a crawl speed that adapts to how fast each website responds and backs off when it starts blocking you."
>
> — D4Vinci/Scrapling README
> 来源: https://raw.githubusercontent.com/D4Vinci/Scrapling/HEAD/README.md

上游 Disclaimer 同段锚定边界："Always respect the terms of service of websites and robots.txt files."——隐身能力服务于公开页面的可达性，不等于授权豁免。

## I (Interpretation) — 方法论骨架

1. **三级 fetcher 光谱，按对抗强度升档**：`Fetcher`（HTTP 请求 + chrome/firefox TLS 指纹伪装 + HTTP/3）→ `DynamicFetcher`（Playwright 全浏览器自动化，network_idle 等待）→ `StealthyFetcher`（指纹伪造隐身栈，`solve_cloudflare=True` 处理公开页面的 Cloudflare Turnstile/Interstitial）。各有 Session 变体（FetcherSession/StealthySession/DynamicSession）跨请求维持 cookie 与状态。
2. **自适应解析是核心差异点**：`css('.product', auto_save=True)` 首次运行保存元素特征指纹；网站改版后同一查询加 `adaptive=True`，相似度算法在新 DOM 里重定位老元素——选择器从「一改就断的字符串」变成「可恢复的元素身份」。配套 `find_similar()` 相似元素扩展与自动选择器生成。
3. **Spider 框架规模化**：Scrapy 式 `start_urls` + async `parse(response)`；`concurrent_requests` 并发 + per-domain 限流；**AutoThrottle** 依据各域响应速度自动调 delay，被封时加倍退避或遵循 `Retry-After`，解封后自行提速；`robots_txt_obey=True` 尊重 Disallow/Crawl-delay/Request-rate；`crawldir` checkpoint 让 Ctrl+C 优雅暂停、重跑即续爬；`stream()` 流式产出 item 并附实时统计。
4. **反封锁工程箱**：`ProxyRotator` 循环/自定义轮换；域名屏蔽与内置 ~3500 个广告追踪域拦截；DNS-over-HTTPS 防 DNS 泄漏；`capture_xhr="URL pattern"` 把页面加载时的 XHR/fetch 直接收成 Response——不逆向接口也能拿后台 API 数据；`cdp_url` 连远程浏览器。
5. **AI 就绪出口**：`page.markdown()` 一行产出净化过的 LLM-ready Markdown；MCP server 让 Claude/Cursor 直接调用；内容先剥 prompt-injection 再给模型看。
6. **性能与开发体验**：解析基准大幅领先 BS4（约 785x）与 Parsel 同档；`scrapling extract` CLI 免写代码落 txt/md/html；`scrapling shell` 交互式调试 + curl 转换；官方 Docker 镜像内置全部浏览器。

## A1 (Past Application) — 源项目典型应用

### 案例: TLS 指纹伪装的会话抓取（README Basic Usage）
- **输入**: quotes.toscrape.com
- **做法**: `FetcherSession(impersonate='chrome')` + `stealthy_headers=True`，`css('.quote .text::text').getall()`
- **结果**: 轻量 HTTP 层即可稳定取得引言数据，无需启动浏览器

### 案例: Cloudflare 挑战页穿透（README Advanced stealth mode）
- **输入**: nopecha.com/demo/cloudflare 等挂盾演示站
- **做法**: `StealthySession(headless=True, solve_cloudflare=True)` 保持浏览器会话连续 fetch
- **结果**: 中间盾放行后照常用 `css('#padded_content a')` 提取目标元素

### 案例: 整店商品目录与断点续爬（Spiders）
- **输入**: Shopify 商店 / 长跑型列表爬取
- **做法**: `ShopifySpider(target_website=...)` 走店铺 JSON API 一次拉全量商品；通用 Spider 用 `crawldir="./crawl_data"` 启动，Ctrl+C 暂停后续跑
- **结果**: 每变体一条 item 的完整目录 / 中断零损失的长时间采集

## A2 (Future Trigger) ★ 触发场景

### 用户会在什么情境下需要
1. **撞墙时刻**：目标公开站点返回 Cloudflare Turnstile 挑战页/403，常规 requests 甚至常规浏览器指纹都被拦——需要隐身栈
2. **改版疲劳**：站点 UI 频繁迭代导致选择器天天坏——需要 auto_save/adaptive 的元素重定位能力
3. **规模化长跑**：数十万页采集，要代理轮换、AutoThrottle 退避、断点续爬、流式统计
4. **接口黑盒**：想要页面背后 XHR/API 的数据但不想逆向请求——capture_xhr 直接收割

### 语言信号
- "这个网站一打开就是 Cloudflare 人机验证，爬下来全是挑战页"
- "requests 被封 403 了，换 User-Agent 也没用"
- "网站一改版我的爬虫选择器就全失效，能不能让它自己适应"
- "帮我做带代理轮换和自动限速的大批量采集，中断了能接着跑"
- "抓它页面加载时后台调的那个接口返回的数据"

### 与同 agent 兄弟 skill 的区分
- 与 `crawl4ai-scraping` 的区别：对抗强度分层——无反爬压力的公开页/文档站，crawl4ai 的 markdown/schema 管线更直接高效；**只有在被反爬拦截或需要自适应解析/Spider 长跑时**才启用本 skill 的重型隐身栈。
- 与 `odl-pdf-extraction` 的区别：本 skill 负责「把页面/文件拿下来」，不做版面级解析——战利品若是 PDF，交给 odl-pdf-extraction。
- 合规分界：隐身 ≠ 万能钥匙。登录态之后、付费之后、验证码之后的**非公开内容**不在本 skill 服务范围（见 B 红线）。

## E (Execution) — 可执行步骤

1. **安装完整依赖** — `pip install "scrapling[fetchers]" && scrapling install`（parser 单装不含 fetchers）；完成标准: `StealthyFetcher.fetch('https://example.com')` 返回正常页面对象
2. **探测目标防护等级** — 先用最轻的 `Fetcher.get()` 试探，观察是否 403/挑战页/空壳；完成标准: 明确所需 fetcher 层级结论，避免过度隐身浪费资源
3. **选定 fetcher/session 抓取** — 按档位用 Fetcher/DynamicFetcher/StealthyFetcher（长跑用对应 Session）；完成标准: 目标关键内容出现在 response 中且非挑战页残渣
4. **编写自适应解析** — `css(选择器, auto_save=True)` 固化元素特征；抽样比对字段值；完成标准: 首轮抽取字段正确率达标，且模拟改版后 `adaptive=True` 能重定位成功
5. **规模化（可选）** — 升级 Spider：`concurrent_requests`、AutoThrottle、`ProxyRotator`、`robots_txt_obey=True`、crawldir 续爬；完成标准: 并发压测稳定，Ctrl+C 后重跑确实从断点继续
6. **合规自检收尾** — 记录 robots.txt/ToS 核对结论、频率策略、数据授权依据；完成标准: 三项写入交付说明，越界需求已当场拒绝

## B (Boundary) — 边界

### 不适用场景
- 无反爬压力的常规公开静态页/文档站 → `crawl4ai-scraping`（其 LLM-ready markdown 与 schema 抽取是主场，成本更低）
- PDF 文件本体的表格/坐标/扫描件解析 → `odl-pdf-extraction`
- **任何以绕过认证/付费为目的的采集**（登录墙后内容、付费墙文章、验证码后的私有数据）——超出本 skill 合规边界，直接拒绝

### 已知局限 / 失败模式
- `solve_cloudflare` 针对 Cloudflare Turnstile/Interstitial 类**公开页面中间盾**；Akamai/DataDome/Kasada 等企业级防护无内建支持——如实告知并评估官方 API 等合法替代，不承诺绕过
- 隐身浏览器资源开销大（headless 也吃内存），并发需用 Session 池（`max_pages`、`get_pool_stats()`）管理
- 反爬对抗是动态博弈：指纹方案可能随目标站升级失效，持续被封时应停下评估而非加码对抗

### 合规红线（上游 Disclaimer 明确要求遵守）
- 遵守 **robots.txt**（Spider 内建 `robots_txt_obey` 尊重 Disallow/Crawl-delay/Request-rate）与目标站 **ToS**
- 用 AutoThrottle/下载延迟**控制请求频率**，禁止对单一站点高压轰击
- **不绕过登录墙/付费墙/验证码**：「帮我爬需要登录的付费内容」→ 应拒绝，建议官方 API、RSS 或取得书面授权；隐身能力仅适用于公开可访问页面
- **个人信息**采集须有合法依据（GDPR/个人信息保护法），目的限定并最小化存储
- 上游声明仅供教育与研究用途、作者不对滥用负责——商用部署前自行完成法务评估

## 相关 skills

- contrasts-with: crawl4ai-scraping（常规公开页 LLM 抓取 vs 强反爬自适应隐身）、odl-pdf-extraction（下载动作 vs 文件解析）
- composes-with: crawl4ai-scraping（常规页分流给它，受阻页本 skill 接管）、odl-pdf-extraction（本 skill 下载的 PDF 交其结构化解析）

---

## 审计信息

- **验证**: V1 ✓（README 特性清单 / Basic-Advanced-Spiders 三组示例 / Disclaimer 段相互印证 API 契约与合规立场）/ V2 ✓（可回答「防护等级怎么分级选 fetcher」「改版后如何重定位元素」等 README 之外的新问题）/ V3 ✓（三级 fetcher 光谱 + 自适应元素指纹 + AutoThrottle 退避模型的组合决策是非常识性工作流）
- **测试通过率**: 100%（详见 test-prompts.json / test-results.md）
- **蒸馏时间**: 2026-08-25
- **来源 URL 清单**:
  - https://raw.githubusercontent.com/D4Vinci/Scrapling/HEAD/README.md （fetch 成功）
