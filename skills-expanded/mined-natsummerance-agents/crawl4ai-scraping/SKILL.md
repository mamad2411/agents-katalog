---
name: crawl4ai-scraping
description: |
  LLM 友好的开源网页爬虫（unclecode/crawl4ai）：异步浏览器抓取公开网页，产出去噪 fit_markdown / 引用化 Markdown 喂 RAG 与 agent，或用 JsonCssExtractionStrategy（免 LLM 的 CSS/XPath schema）与 LLMExtractionStrategy（pydantic schema）抽结构化 JSON；覆盖 JS 渲染、虚拟滚动、iframe、BFS 深爬与崩溃恢复，并可 Docker 化为带 JWT 鉴权的 FastAPI 服务。
  当用户说「把网页/文档站转成 LLM 可用的 markdown」「爬商品列表输出 JSON」「页面是 JS 动态渲染的」「搭一个爬虫 API 服务」时使用。
  不适用于：PDF 文件本体解析（转 odl-pdf-extraction）；被 Cloudflare 等强反爬盾拦截的站点（转 scrapling-stealth）。
source_project: unclecode/crawl4ai
tags: [crawl4ai-scraping, web-crawler, llm-ready-markdown, structured-extraction, docker-service, 蒸馏技能]
---

# Crawl4ai Scraping · LLM 友好网页抓取引擎

## R (Reading) — 上游原文

> "Crawl4AI turns the web into clean, LLM ready Markdown for RAG, agents, and data pipelines."
>
> "Why developers pick Crawl4AI: **LLM ready output**, smart Markdown with headings, tables, code, citation hints · **Fast in practice**, async browser pool, caching, minimal hops · **Full control**, sessions, proxies, cookies, user scripts, hooks · **Adaptive intelligence**, learns site patterns, explores only what matters · **Deploy anywhere**, zero keys, CLI and Docker, cloud friendly."
>
> — unclecode/crawl4ai README（v0.9.2）
> 来源: https://raw.githubusercontent.com/unclecode/crawl4ai/HEAD/README.md

上游定位补充："Open-source LLM Friendly Web Crawler & Scraper"，CLI 形态为 `crwl <url> -o markdown`，深爬示例 `--deep-crawl bfs --max-pages 10`，问答式抽取 `-q "Extract all product prices"`。

## I (Interpretation) — 方法论骨架

1. **双层配置心智模型**：`BrowserConfig` 管浏览器层（headless/user_data_dir/proxy），`CrawlerRunConfig` 管单次运行层（cache_mode/markdown_generator/extraction_strategy/js_code），统一由 `AsyncWebCrawler(config=browser_config)` + `crawler.arun(url, config=run_config)` 驱动——先想清楚哪层的问题再调参。
2. **Markdown 双轨输出**：`raw_markdown` 保真，`fit_markdown` 走启发式去噪——`PruningContentFilter(threshold=0.48)` 按文本密度剪枝，`BM25ContentFilter(user_query=...)` 按查询聚焦；链接自动转为编号引用列表，天然适配 LLM 上下文。
3. **结构化抽取双策略**：重复 DOM 模式用 `JsonCssExtractionStrategy(schema)`（baseSelector + fields，XPath/CSS，零 token 成本）；语义复杂的异构页面用 `LLMExtractionStrategy`（pydantic schema + instruction，LLMConfig 支持 litellm 全系 provider 与 backoff 限流参数）。巨型表格另有 `LLMTableExtraction` 分块合并。
4. **动态内容工具箱**：`js_code` 注入脚本（点 tab/展开）、`wait_for` 等待、`VirtualScrollConfig` 处理无限滚动、`flatten_shadow_dom=True` 展开 Shadow DOM、iframe 内容无缝抽取、lazy-load 等待图片加载。
5. **规模化深爬**：BFS/DFS/BestFirst 策略 + `arun_many`（`MemoryAdaptiveDispatcher` 内存自适应并发）；`resume_state` + `on_state_change` 崩溃恢复长任务；`prefetch=True` 先 5–10x 提速做 URL 发现再做选择性加工。
6. **服务化交付**：Docker 镜像 + FastAPI（端口 11235），v0.9.0 起 secure-by-default（JWT 默认开启、默认绑 loopback、请求体视为不可信边界），附 dashboard/playground/MCP 集成，`POST /crawl` 提交任务轮询 `/task/{id}`。
7. **反检测与持久化**：stealth 模式、`browser_type="undetected"`、代理链升级重试（ProxyConfig.DIRECT → fallback），`use_persistent_context` 复用带 cookie 的浏览器档案。

## A1 (Past Application) — 源项目典型应用

### 案例: 新闻频道首页 → LLM 语料（Quick Start）
- **输入**: https://www.nbcnews.com/business
- **做法**: `AsyncWebCrawler().arun()` 打印 `result.markdown`，或 CLI `crwl <url> -o markdown`
- **结果**: 数秒获得干净 Markdown，直接进入 RAG/agent 上下文管道

### 案例: Kidocode 课程页免 LLM 结构化抽取（Advanced Examples）
- **输入**: 需点击 tab 才展开的重复卡片式课程页
- **做法**: `JsonCssExtractionStrategy` 定义 baseSelector+fields schema；`js_code` 循环 `scrollIntoView()+click()` 展开全部 tab；`CacheMode.BYPASS`
- **结果**: `json.loads(result.extracted_content)` 得到课程名/描述/图标 URL 的结构化数组，零 token 成本

### 案例: OpenAI 定价页 LLM schema 抽取
- **输入**: 语义异构的 openai.com/api/pricing 页面
- **做法**: `LLMExtractionStrategy(llm_config=..., schema=PydanticModel.schema(), extraction_type="schema", instruction=...)`
- **结果**: 全部模型名称与 input/output 费用的规范化 JSON 列表，字段级可控

## A2 (Future Trigger) ★ 触发场景

### 用户会在什么情境下需要
1. **建 RAG/agent 知识库**：把文档站、博客、新闻页批量清洗成 LLM 可直接消费的 fit_markdown（去广告/导航噪音，保标题层级与代码块）
2. **批量结构化采集**：列表页/详情页存在重复 DOM 模式 → CSS schema 秒级抽取成 JSON；页面结构语义混乱时再升级 LLM 策略
3. **工程化交付**：JS 渲染页/无限滚动/iframe 内容抓取；深爬整站且要求断点续爬；或把抓取能力封装为团队共享的 Docker API 服务

### 语言信号
- "把这个网页/整个文档站转成 markdown，我要喂给大模型"
- "爬取列表页里的商品标题和价格，输出结构化 JSON"
- "这页面要执行 JS 才出内容 / 是下拉无限加载的"
- "给我搭一个爬虫 REST API / Docker 服务，别的程序来调"
- "深爬这个 docs 站最多 10 页，中途崩了能接着爬"

### 与同 agent 兄弟 skill 的区分
- 与 `odl-pdf-extraction` 的区别：看输入形态——本 skill 处理**网页**；目标是 PDF 文件本体（表格版面/坐标/扫描件）→ 转 odl-pdf-extraction。网页中发现的 PDF 下载后同样交给它。
- 与 `scrapling-stealth` 的区别：看对抗强度——常规公开页面本 skill 直取；一旦撞上 Cloudflare Turnstile 挑战页/高级指纹检测导致内容拿不到 → scrapling-stealth 的隐身栈接管。

## E (Execution) — 可执行步骤

1. **环境安装与体检** — `pip install -U crawl4ai && crawl4ai-setup && crawl4ai-doctor`；完成标准: doctor 检查全绿，浏览器问题用 `python -m playwright install chromium` 补装成功
2. **最小抓取冒烟** — `AsyncWebCrawler().arun(url)` 打印 `result.markdown`；完成标准: 输出非空且包含目标页面关键词
3. **确定输出形态** — 语料路线配 `DefaultMarkdownGenerator(content_filter=PruningContentFilter(...))` 或 BM25；结构化路线写 JsonCssExtractionStrategy schema 或 LLMExtractionStrategy(pydantic+instruction)；完成标准: fit_markdown 明显小于 raw 且正文完整保留 / `extracted_content` 可 json.loads 且 schema 字段齐全
4. **动态内容攻坚** — 按 need 组合 js_code、wait_for、virtual_scroll_config、flatten_shadow_dom；完成标准: 此前缺失的关键数据出现在结果中（对照浏览器实机抽查）
5. **批量化与服务化** — 批量走 `arun_many` + url_matcher 多配置 + cache_mode + resume_state；服务化走 `docker run -d -p 11235 --shm-size=1g unclecode/crawl4ai:latest` 后 `POST /crawl`；完成标准: 批量任务全部成功或产出明确失败清单；API 冒烟返回 200 与 results
6. **合规自检收尾** — 核对 robots.txt/ToS、设定频率与并发上限、确认个人信息处理依据；完成标准: 三项检查结论写入交付说明

## B (Boundary) — 边界

### 不适用场景
- 输入是 PDF/DOCX 等**文件本体**而非网页 → `odl-pdf-extraction`（其 bounding box/阅读序/扫描 OCR 是为此设计）
- 已被强反爬（Cloudflare 挑战页、高级 bot 检测）拦截的站点 → `scrapling-stealth`
- 一次性静态请求（requests/httpx 即可）或内部 API/数据库导出类需求——不必动用浏览器爬虫全家桶

### 已知局限 / 失败模式
- `LLMExtractionStrategy` 有 token 成本与供应商速率限制（LLMConfig 的 backoff_base_delay/max_attempts/exponential_factor 可调），schema 与 instruction 质量直接决定抽取质量
- Docker 服务虽 v0.9.0 起 secure-by-default，仍不应裸暴露公网；同步（Selenium）版本已弃装
- undetected/stealth 属对抗性措施，对最新反爬升级可能滞后——持续失败本身就是该转 `scrapling-stealth` 或放弃的信号

### 合规红线
- 抓取前核对 **robots.txt 与目标站 ToS**；用 CacheMode、deep crawl 的 max_pages、并发上限控制请求频率与体量
- **不绕过登录墙、付费墙或验证码**获取未经授权内容；「帮我爬需要登录的付费内容」→ 应拒绝，建议官方 API/导出或取得授权
- 涉及**个人信息**的采集必须有合法依据并最小化存储；商用部署遵守 Apache-2.0 的 attribution 要求（badge 或文字声明）

## 相关 skills

- contrasts-with: scrapling-stealth（强反爬隐身抓取）、odl-pdf-extraction（PDF 文件版面解析）
- composes-with: odl-pdf-extraction（网页中发现 PDF 链接 → 下载后交其结构化解析）

---

## 审计信息

- **验证**: V1 ✓（README 特性清单 / Quick Start / Advanced Examples / Docker 章节相互印证配置与函数契约）/ V2 ✓（可回答「该用 CSS schema 还是 LLM 策略」「如何服务化并保证安全默认」等书外新问题）/ V3 ✓（双层配置 + 双抽取策略 + 安全默认服务化的完整决策管线是非常识性工作流）
- **测试通过率**: 100%（详见 test-prompts.json / test-results.md）
- **蒸馏时间**: 2026-08-25
- **来源 URL 清单**:
  - https://raw.githubusercontent.com/unclecode/crawl4ai/HEAD/README.md （fetch 成功）
