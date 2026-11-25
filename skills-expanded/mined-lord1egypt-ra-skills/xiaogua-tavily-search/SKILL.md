---
name: xiaogua-tavily-search
description: Tavily-powered live web search skill for current information, news, online research, source gathering, and fallback web search when built-in web_search is rate-limited or insufficient. Primary credential: `TAVILY_API_KEY`. Also supports `--api-key` and local `.secrets/tavily.key` for private setups. Use when Tavily search is explicitly desired and you want cleaner result ranking, official-source preference, path-level scoring, deduplication, noisy-domain suppression, and readable terminal output. 适用于需要实时网页搜索、新闻检索、在线研究、资料收集，或内置 web_search 限流/效果不足时作为高质量备用搜索通道的场景。主推荐凭据方式：`TAVILY_API_KEY`；也支持 `--api-key` 与本地 `.secrets/tavily.key`（仅适合私有本地环境）。适合希望优先官方来源、按路径质量排序、自动去重、压制低质量噪音站点并输出更易读结果的任务。
---

# Xiaogua Tavily Search / 小瓜 Tavily 搜索

A practical Tavily search skill for OpenClaw, optimized for better ranking, cleaner output, and safer day-to-day use.

这是一个面向 OpenClaw 的实用 Tavily 搜索技能，重点优化了排序质量、输出可读性，以及日常长期使用时的稳定性与安全性。

## Credential requirements / 凭据要求

**Primary credential / 主要凭据**
- `TAVILY_API_KEY`

**Also supported / 其他支持方式**
- `--api-key`
- local `.secrets/tavily.key`

**Notes / 说明**
- This skill requires a Tavily API key to run.
- The published package does **not** include any API key.
- For public/shared installs, prefer `TAVILY_API_KEY`.
- `skills/xiaogua-tavily-search/.secrets/tavily.key` is intended for local private setups only, and this published script does not search parent directories for secrets.

- 本技能运行时需要 Tavily API key。
- 公开发布的 skill 包**不包含**任何 API key。
- 对公共/共享安装场景，优先使用 `TAVILY_API_KEY`。
- `.secrets/tavily.key` 仅建议用于本地私有环境。

## Key advantages / 当前版本优势

Compared with simpler public Tavily skills, this version adds:

相比更基础的公共 Tavily skill，这个版本额外做了这些增强：

- **Consistent credential behavior**: `TAVILY_API_KEY` is the primary documented credential, while `--api-key` and `.secrets/tavily.key` remain supported as secondary paths.
  - **更一致的凭据策略**：公开说明中已将 `TAVILY_API_KEY` 作为主推荐凭据，`--api-key` 和 `.secrets/tavily.key` 作为补充方式，避免用户混淆。
- **Official-source preference** for recognized products/topics such as OpenClaw, WSL, Ubuntu, and Tavily.
  - **官方来源优先**：针对 OpenClaw、WSL、Ubuntu、Tavily 等主题，会优先官方文档/官方仓库/更可信来源。
- **Path-level ranking** instead of domain-only ranking.
  - **路径级排序**：不只看域名，还会区分 `/releases`、`/docs`、`/issues`、`/discussions` 等 URL 路径质量。
- **Intent-aware ranking** for release notes, docs/setup, troubleshooting, and news.
  - **按查询意图排序**：能根据“发布说明 / 文档安装 / 故障排查 / 新闻”这几类问题调整结果排序逻辑。
- **Deduplication** for near-identical URLs.
  - **结果去重**：避免同类页面重复占据前排。
- **Noisy-domain suppression** for common low-signal social/content-farm results.
  - **噪音站点压制**：默认压低或排除 Facebook、Reddit、Pinterest、Instagram、X/Twitter、Quora 等低信噪比来源。
- **Readable terminal output** with source labels, host display, scores, and trimmed snippets.
  - **更适合终端阅读的输出**：显示来源标签、域名、分数，并对摘要做裁剪，方便快速判断结果质量。
- **Windows-friendly UTF-8 output handling**.
  - **适配 Windows 终端编码问题**：避免部分字符导致输出报错。
- **Minimal dependency footprint**: Python stdlib only.
  - **依赖最小化**：只使用 Python 标准库，便于审查和维护。

## Quick start / 快速开始

1. Set `TAVILY_API_KEY` in your environment (recommended).
2. As alternatives, use `--api-key` or a local `.secrets/tavily.key` file for private setups.
3. Run:

```bash
python skills/xiaogua-tavily-search/scripts/tavily_search.py "your query"
```

4. Use `--json` if you want raw structured output.

1. 推荐先在环境变量中设置 `TAVILY_API_KEY`。
2. 本地私有使用场景下，也可使用 `--api-key` 或本地 `.secrets/tavily.key`。
3. 运行：

```bash
python skills/xiaogua-tavily-search/scripts/tavily_search.py "your query"
```

4. 如需原始结构化结果，使用 `--json`。

## Recommended usage / 推荐使用场景

Use this skill when:

在这些场景下推荐使用本技能：

- built-in `web_search` is rate-limited or temporarily unavailable
- you explicitly want Tavily results
- you need a cleaner ranked result list
- you care about official docs/releases/issues being surfaced earlier
- you want a deterministic script you can inspect and modify locally

- 内置 `web_search` 被限流或暂时不可用
- 你明确想用 Tavily 搜索
- 你希望搜索结果排序更干净
- 你希望官方文档 / 官方发布 / 官方 issue 更早浮出来
- 你希望这是一个可本地审查、可继续修改的确定性脚本

## Ranking behavior / 排序逻辑

By default, the script behaves like a careful human researcher:

默认情况下，脚本会尽量模拟“认真做检索的人”的行为：

- product-specific official domains are preferred
- release/changelog queries boost release-note paths
- install/configuration queries boost documentation paths
- troubleshooting queries boost issues, FAQ, and troubleshooting pages
- GitHub community discussions rank below official docs/repo pages for factual product questions

- 产品相关问题优先官方域名
- 发布说明/更新日志类问题提升 release 路径权重
- 安装/配置类问题提升 docs/guide/configure 路径权重
- 故障排查类问题提升 issue/faq/troubleshooting 路径权重
- 对事实型产品问题，GitHub 社区讨论会排在官方文档/官方仓库之后

Disable defaults when needed:

如有需要，也可以关闭默认优化：

```bash
python skills/xiaogua-tavily-search/scripts/tavily_search.py "query" --no-official-first --no-exclude-noisy-default
```

## Common commands / 常用命令

Basic search / 基础搜索:

```bash
python skills/xiaogua-tavily-search/scripts/tavily_search.py "OpenClaw latest release notes"
```

Search with Tavily answer / 带 Tavily 综合回答:

```bash
python skills/xiaogua-tavily-search/scripts/tavily_search.py "OpenClaw latest release notes" --include-answer
```

Raw JSON / 原始 JSON 输出:

```bash
python skills/xiaogua-tavily-search/scripts/tavily_search.py "OpenClaw latest release notes" --json
```

Troubleshooting query / 排障查询:

```bash
python skills/xiaogua-tavily-search/scripts/tavily_search.py "WSL localhost proxy NAT not supported fix" --include-answer
```

News-style query / 新闻查询:

```bash
python skills/xiaogua-tavily-search/scripts/tavily_search.py "AI infrastructure funding" --topic news --days 7 --include-answer
```

## Security notes / 安全说明

- This published skill should not include any API key.
- Put your key in local environment variables or local `.secrets` files after installation.
- Do not commit or publish your real key.

- 公开发布的 skill 包本身不应包含任何 API key。
- 请在安装后于本地环境变量或本地 `.secrets` 文件中放置密钥。
- 不要把真实密钥提交或发布出去。

## Resources / 资源

### scripts/
- `tavily_search.py`: Tavily search wrapper with source cleanup, intent detection, path scoring, deduplication, and result labeling.
- `tavily_search.py`：带来源清洗、意图识别、路径级排序、去重与结果标签能力的 Tavily 搜索脚本。
去重与结果标签能力的 Tavily 搜索脚本。
