---
name: aggregate-search
description: 跨平台聚合搜索工具。支持 Bilibili、Reddit、GitHub、Tavily AI、小红书、Telegram 等多通道聚合检索，免登录优先、广度优先。开放网页源（Bing）已停用。
---

# Aggregate Search — 跨平台聚合搜索

## 功能特点
- **免登录优先**：B站（WBI 签名）、Reddit（arctic-shift 历史存档）、GitHub 官方 API 直接开箱可用。
- **广度优先并发**：多平台多线程并发检索，快速返回格式化 Markdown 或 JSON 结果。
- **Reddit 深度挖掘**：`scripts/reddit_miner.py` 提供意图分类、态度极性、时间趋势与评论高频短语挖掘。
- **高阶平台支持**：支持配置 Tavily AI 搜索、Telegram 全域搜索（Telethon）、小红书（xhs-cli）与 X/Twitter（twikit）。

## 快速使用

```bash
# 安装依赖（可选，用于 Telegram/X 支持）
pip install -r requirements.txt

# 默认搜索所有平台
python3 scripts/search.py "搜索关键词"

# 自选平台（逗号分隔）
python3 scripts/search.py "Python 教程" --platform bilibili,reddit,github,tavily

# 排除指定平台
python3 scripts/search.py "AI 工具" --platform all,-xhs

# 输出机器可读 JSON
python3 scripts/search.py "开源项目" --platform github --json

# 查看支持的平台列表
python3 scripts/search.py --list
```

## 支持平台与配置说明

| 平台别名 | 平台名称 | 默认通道/协议 | 鉴权/依赖说明 |
|---|---|---|---|
| `bilibili` | B站 | 官方 API + WBI 签名 | 免登录，开箱即用 |
| `reddit` | Reddit | arctic-shift 历史存档 | 免登录免 Key，开箱即用 |
| `github` | GitHub | 官方 Search API | 免登录（公共限流 10 req/min） |
| `tavily` | Tavily AI 搜索 | REST API | 需配置环境变量 `TAVILY_API_KEY` |
| `telegram`| Telegram 全域 | Telethon SearchGlobal | 需配置 `TELEGRAM_API_ID` / `TELEGRAM_API_HASH` 并登录 |
| `xhs` | 小红书 | xhs-cli / Web Cookie | 需本地 Cookie 或 xhs-cli 登录态 |

> **⚠️ web/开放网页源已停用（2026-08-26）**：Bing RSS 索引被垃圾 SEO 站点（黑料网等）污染，对推荐/选购类查询返回无效结果。需要开放网页搜索时请改用 `tavily` 平台（需 `TAVILY_API_KEY`）。

## 平台语言纪律（强制）

- **Reddit / GitHub 是英文平台**：禁止用中文关键词搜索，脚本已硬性拦截（检测到中文直接报错并提示翻译）。英文关键词如「猫粮推荐」→ `cat food recommendation`、`best budget cat food`。
- **B站 / 小红书 / Telegram（中文内容）**：用中文关键词。
- **tavily**：可自动处理，中英文皆可。
- 多平台搜索时按目标平台语言分别给出关键词（如 `bilibili: 猫粮推荐` + `reddit: cat food recommendation`），不要用一个关键词通打所有平台。

## Reddit 深度挖掘（独立模式）

```bash
# 高分真实问题挖掘
python3 scripts/reddit_miner.py --subreddits StableDiffusion --days 90

# 痛点挖掘（态度极性交叉表）
python3 scripts/reddit_miner.py --subreddits OpenAI --filter problem --top 50

# 评论高频短语提取（用户原话素材）
python3 scripts/reddit_miner.py --subreddits ChatGPT --with-comments --extract-patterns 30 --format md
```

### 环境与鉴权配置引导
运行以下命令可查看各平台登录与配置指引：
```bash
python3 scripts/auth.py
```
