---
name: wechat-weread-official
license: MIT
description: 检索微信公众号文章、获取原文链接和可见正文，支持按日期/公众号/关键词筛选、断点续采、离线重筛及 JSON/CSV/Markdown 导出。用于公众号资料收集、主题研究和用户提供的 mp.weixin.qq.com 链接提取；检索通过本机 Edge 的微信读书登录态完成。
---

# 微信公众号检索与正文采集

使用 `scripts/wechat_official.py`，通过 `uv run` 运行。脚本固定依赖，直接操作 Edge CDP；不要重复编写爬虫，也不要臆造公众号链接或调用未验证的私有接口。

## 选择任务

- **找文章/列链接**：`search`。先看关键词覆盖、过滤原因和候选质量。
- **找文章并读正文**：`collect`。按用户范围设置正文数量；`--fulltext-limit` 控制本次选择中的前 N 篇，省略则全部获取。
- **已有原文链接或结果**：`fetch`。无需先登录微信读书；支持任务目录、v1/v2 JSON、旧版数组、JSONL、UTF-8 URL 文本和重复 `--url`。
- **调整已有结果的条件/数量/排序**：`rank`。优先读取完整候选池，不联网、不启动浏览器。
- **运行环境失败**：`doctor`。检查 Python、依赖、浏览器和指定 CDP 端口，不访问网站；它不证明已登录。

主题研究、多关键词扩展、覆盖不足或用户要求解释检索质量时，读取 [references/research-search.md](references/research-search.md)。给定精确关键词或公众号时先忠实执行，不自动改变研究范围。

## 运行

```powershell
$wxSkill = "$env:USERPROFILE\.codex\skills\wechat-weread-official"
```

含中文关键词和多个筛选条件时，优先写 UTF-8 JSON 配置，避免 shell 编码损坏。可参考 `examples/search-config.json`；数组字段必须使用字符串数组，未知字段会报错。

```powershell
uv run "$wxSkill\scripts\wechat_official.py" search `
  --query-file "$wxSkill\examples\search-config.json" `
  --run-dir ".\outputs\wechat-search"

uv run "$wxSkill\scripts\wechat_official.py" collect `
  --query-file "$wxSkill\examples\search-config.json" `
  --fulltext-limit 5 --run-dir ".\outputs\wechat-collect"

uv run "$wxSkill\scripts\wechat_official.py" fetch `
  --input ".\outputs\wechat-search" --limit 5 `
  --run-dir ".\outputs\wechat-fulltext"

uv run "$wxSkill\scripts\wechat_official.py" rank `
  --input ".\outputs\wechat-search" --sort newest `
  --min-date 2026-01-01 --exclude-any "培训" `
  --target 10 --run-dir ".\outputs\wechat-reranked"

uv run "$wxSkill\scripts\wechat_official.py" doctor
```

关注 stderr 的登录、关键词进度和风控消息。运行目录用任务的 `outputs/` 保存正式交付，试运行用 `work/`。用户指定路径时遵循用户选择。

## 筛选、排序与覆盖

- 每个关键词最多观察 `per_query_limit` 条卡片，受 `max_scroll_rounds` 约束。执行全部关键词后再去重、筛选并应用全局 `target`，不会由第一个关键词提前占满配额。
- `contains_any`、`contains_all`、`exclude_any` 匹配**标题、摘要和公众号名称**；`source_include_any`、`source_exclude_any` 只匹配公众号名称。它们不检索尚未读取的正文。需要按全文分析时先采集，再分析 `fulltext`。
- 日期范围包含边界。默认 `unknown_date=drop`；不限定日期的探索性检索可用 `keep`，避免日期解析失败造成漏检。相对日期按原任务采集日解析，保留原始日期；“个月前/年前”为近似换算。
- 默认 `sort=relevance`，综合有效链接、关键词覆盖、标题/摘要命中和站内排名；`sort=newest` 优先有效链接和日期。这是本地排序，不是微信索引的相关性分数。
- `candidates.json` 保留已观察的全部去重候选，包含筛选未通过和超出 `target` 的条目，方便离线重筛。提高 `target` 不能增加已经观察过的索引范围。
- 用 `summary.md` 的逐关键词状态、过滤原因、停止原因和错误定位不足。结果数不代表公众号全量覆盖；无法达到目标时报告实际数量及原因。

## 登录、失败与恢复

搜索使用持久化专用 Edge profile。需要登录时脚本保存 `login-qr.png` 并等待；展示二维码或已返回的截图，让用户扫码，随后同一命令继续。不要主动让用户上传截图，也不要复制登录 profile。

```powershell
uv run "$wxSkill\scripts\wechat_official.py" collect `
  --run-dir ".\outputs\wechat-collect" --resume
```

恢复必须使用原命令和原目录，搜索条件保持一致；原正文上限自动保留，可显式提高。成功/明确无结果的关键词会跳过，失败的关键词重试；正文成功、图片文章、已删除等终止状态会复用。若改变筛选条件，用 `rank`；若扩大检索范围，新建搜索目录。

发现风控立即停止后续请求并保存已有结果。保留 `risk_control`、`deleted`、`client_only`、`blocked` 等实际状态，不把它们当成空结果或尝试绕过。返回码 0 表示请求范围处理完成，2 表示部分完成、风控、登录未完成或诊断失败。

只提取会话正常显示的内容。图片正文标记 `image_only` 并保留图片链接；不声称已做 OCR。正文中谈论“访问频繁”等词不会被当成拦截页。

## 交付与验证

交付实际运行状态、筛选后数量、正文状态分布、关键词覆盖缺口、原文链接及 `results.json`/`results.csv`/`summary.md`。只有读取了正文才能称为“正文已核实”；摘要层面的判断注明依据。需要研究结论时摘要引用原文链接，避免不必要地重复传播长篇正文。

维护脚本后运行：

```powershell
uv run "$wxSkill\tests\test_unit.py"
uv run "$wxSkill\tests\test_browser_fixtures.py"
```

按需参考：

- [references/runtime-and-troubleshooting.md](references/runtime-and-troubleshooting.md)：浏览器所有权、登录、恢复、运行问题。
- [references/selectors-and-statuses.md](references/selectors-and-statuses.md)：DOM 入口、状态和重试范围。
- [references/output-schema.md](references/output-schema.md)：v2 字段与旧结果兼容。
