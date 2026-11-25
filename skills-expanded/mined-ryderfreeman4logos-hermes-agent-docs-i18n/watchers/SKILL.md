---
name: watchers
description: Poll RSS, JSON APIs, and GitHub with watermark dedup.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [cron, polling, rss, github, http, automation, monitoring]
    category: devops
    requires_toolsets: [terminal]
    related_skills: []
---

# 监视器

定期轮询外部数据源，仅对新增内容作出响应。提供三个现成脚本以及一个通用的水印辅助工具；可将它们集成到定时任务中（或直接通过终端运行）。

## 适用场景

- 用户希望监控 RSS/Atom 订阅源，并在有新内容时收到通知
- 用户希望监控 GitHub 仓库中的问题、拉取请求、版本发布及代码提交记录
- 用户希望轮询任意 JSON 接口，并在新数据出现时获得通知
- 用户要求“为 X 创建一个监视器”或“当 X 发生变化时通知我”

## 工作原理

监视器本质上只是一个脚本，其功能包括：

1. 从外部数据源获取数据
2. 将获取的数据与之前记录的水印文件中的 ID 进行比对
3. 将新的 ID 写入水印文件
4. 将新内容输出到标准输出（若无变化则不输出任何内容）

以下脚本可完成上述全部功能。Agent 可通过终端工具、定时任务、Webhook 或交互式聊天等方式运行这些脚本，并反馈新增内容。

## 现成脚本

安装该技能后，这三个脚本均位于 `$HERMES_HOME/skills/devops/watchers/scripts/` 目录下。每个脚本都会根据 `--name` 参数指定的名称，从 `WATCHER_STATE_DIR`（默认为 `$HERMES_HOME/watcher-state/`）中读取状态文件。

| 脚本名 | 监控内容 | 去重键值 |
|---|---|---|
| `watch_rss.py` | RSS 2.0 或 Atom 订阅源地址 | `<guid>` / `<id>` |
| `watch_http_json.py` | 任何返回对象列表的 JSON 接口 | 可配置的 ID 字段 |
| `watch_github.py` | 指定 GitHub 仓库的问题、拉取请求、版本发布及代码提交记录 | `id` / `sha` |

这三个脚本的共同特点如下：

- 首次运行时会记录初始数据作为基准，不会重复处理已有内容
- 水印文件采用有限 ID 集合（最多 500 个 ID），以控制内存占用
- 输出格式：每条记录为 `## <标题>\n<网址>\n\n<可选内容>` 
- 若无新内容则标准输出为空，调用方可将其视为无变化
- 获取数据时出现错误则返回非零退出码

## 使用方法

可直接通过终端工具运行监视器：

```bash
python $HERMES_HOME/skills/devops/watchers/scripts/watch_rss.py \
  --name hn --url https://news.ycombinator.com/rss --max 5
```

监控 GitHub 仓库（请在 `${HERMES_HOME:-~/.hermes}/.env` 中设置 `GITHUB_TOKEN`，以避免每小时 60 次的匿名请求限制）：

```bash
python $HERMES_HOME/skills/devops/watchers/scripts/watch_github.py \
  --name hermes-issues --repo NousResearch/hermes-agent --scope issues
```

轮询任意 JSON API：

```bash
python $HERMES_HOME/skills/devops/watchers/scripts/watch_http_json.py \
  --name api --url https://api.example.com/events \
  --id-field event_id --items-path data.events
```

## 与 cron 的集成

可通过如下提示语让智能体安排 cron 任务：

> 每 15 分钟运行一次 `watch_rss.py --name hn --url https://news.ycombinator.com/rss`。如果该脚本输出了内容，则汇总相关标题并发送出去；若无输出，则保持沉默。

智能体会在 cron 任务的智能体循环中通过终端工具来调用该脚本，无需对 cron 内置的 `--script` 参数进行任何修改。

## 状态文件

每个监控器都会生成 `$HERMES_HOME/watcher-state/<名称>.json` 文件。可对此文件进行检查：

```bash
cat $HERMES_HOME/watcher-state/hn.json
```

强制重新执行（将下一次运行视为首次查询）：

```bash
rm $HERMES_HOME/watcher-state/hn.json
```

## 自定义脚本编写

这三种脚本均采用相同的结构模板：加载水印、获取数据、进行差异对比、保存结果以及输出信息。`scripts/_watermark.py` 是一个通用的辅助工具，导入该文件即可免费获得原子化写入功能、受限的 ID 集以及首次运行时的基准数据。只需查看任意一个参考脚本，就能了解其所需的样板代码量其实非常少。

## 常见问题

1. **在每次循环时都打印“无新项目”的提示信息**。调用方通常认为空的标准输出即代表没有变化。如果在为空的差异数据上仍打印内容，就会造成通道信息过载。现有脚本已解决了此问题，自定义脚本同样需要做到这一点。
2. **误以为首次运行时会输出项目数据**。实际上并不会——首次运行仅用于记录基准数据。如果需要初始摘要，可在首次运行后删除状态文件，或在自己的脚本中添加 `--prime-with-latest N` 参数。
3. **水印数量无限制增长**。通用辅助工具将 ID 数量上限设定为 500 个。对于数据更新频繁的源数据，可提高此上限；在磁盘空间有限的系统中，则应适当降低该数值。
4. **将状态目录设置在代理程序的沙箱环境无法写入的位置**。`$

