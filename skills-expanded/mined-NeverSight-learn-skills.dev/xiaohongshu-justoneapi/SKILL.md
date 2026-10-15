---
name: xiaohongshu-justoneapi
description: 当用户需要爬取或采集小红书（RedNote）数据时触发，包括：搜索笔记/内容、话题发现、搜索用户/博主、发现 KOL/达人、研究账号信息、抓取用户笔记等场景。通过 JustOneAPI 调用小红书接口获取数据。
---

# 小红书数据采集 —— JustOneAPI

使用 JustOneAPI 调用小红书接口抓取数据。

## 前置：获取 Token

所有接口均通过 query 参数 `token` 鉴权。按以下优先级获取 token：

1. 从当前目录向上逐级查找 `.env` 文件，匹配 `JUSTONEAPI_TOKEN` 或 `JUST_ONE_API_TOKEN`
2. 读取系统环境变量 `JUSTONEAPI_TOKEN` 或 `JUST_ONE_API_TOKEN`
3. 均未找到则报错退出，提示用户在 `.env` 中添加 token

生成代码时，token 应从环境变量读取，不要硬编码到代码中：

```
JUSTONEAPI_TOKEN=your_token_here
```

## 错误码（所有接口通用）

> ⚠️ `code` 在**响应体**中，不是 HTTP 状态码。HTTP 200 也须检查 `code`。

| `code` | 含义 | 处理策略 |
|:------:|------|----------|
| `0` | 成功 | 正常处理 |
| `100` | Token 无效或已失效 | 提示用户检查 token |
| `301` | 采集失败 | **自动重试**，间隔 2-3 秒，最多 3 次 |
| `302` | 超出速率限制 | 降低请求频率，等待后重试 |
| `303` | 超出每日配额 | 告知用户当日配额已用尽 |
| `400` | 参数错误 | 检查必填参数是否缺失或格式有误 |
| `500` | 服务器内部错误 | 稍后重试，持续则反馈 JustOneAPI |
| `600` | 权限不足 | 告知用户当前 token 无此接口权限 |
| `601` | 余额不足 | 告知用户需在 JustOneAPI 充值 |

## 接口目录

根据用户意图，按需读取对应文件，**不要自行重写脚本**。

| 用户意图 | 接口定义 | 脚本 |
|----------|----------|------|
| 搜索用户 / 发现博主 / 查账号 | `apis/search_users.md` | `scripts/search_users.py` |
| 抓取用户发布的笔记 / 内容分析 / 竞品监控 | `apis/get_user_posts.md` | `scripts/get_user_posts.py` |
| 搜索笔记 / 话题发现 / 关键词采集 / 舆情追踪 | `apis/search_notes.md` | `scripts/search_notes.py` |

## 运行方式

所有脚本统一使用 `uv run` 执行，无需手动安装依赖：

```bash
# 安装 uv（若尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 直接运行，uv 自动处理依赖
uv run scripts/search_users.py <keyword> [max_pages] [--output-dir DIR]
uv run scripts/get_user_posts.py <user_id> [user_id2 ...] [--output-dir DIR] [--since YYYY-MM-DD] [--workers N]
uv run scripts/search_notes.py <keyword> <max_pages> [--sort SORT] [--note-type TYPE] [--output-dir DIR]

# 示例
uv run scripts/search_users.py 美妆博主 5 --output-dir ./output
uv run scripts/get_user_posts.py 5b33a8556b58b74911b89949 5f279d91000000000100836c --output-dir ./output --since 2025-01-01
uv run scripts/search_notes.py 美妆 10 --sort popularity_descending --note-type _1 --output-dir ./output
uv run scripts/search_notes.py 机车骑行 20 --sort time_descending --output-dir ./output
```
