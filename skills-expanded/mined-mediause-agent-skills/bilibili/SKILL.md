---
name: bilibili
description: MediaUse bilibili skill usage guide. Includes full bilibili manifest command map, parameter guidance, and executable examples for search/get/read/user/collection/engage flows.
---

# MediaUse Bilibili Skill

该 Skill 面向 bilibili 平台的内容发现、账号上下文、视频/动态/评论读取，以及可选的发布互动工作流，适合在 MediaUse CLI 中完成从命令发现到结果回溯的完整操作。

Summary：

- 适用于 Bilibili 的内容搜索、热门信息获取、视频与动态阅读，以及账号相关的上下文绑定
- 支持查看用户资料、收藏夹和评论等常见操作，适合日常内容分析与信息收集
- 提供可直接复用的命令模板和示例工作流，帮助用户按需快速执行 Bilibili 任务

## Scope

适用场景：

- 视频搜索与用户搜索
- 热门/排行榜/历史/关注动态拉取
- 视频详情、字幕、AI 摘要、评论读取
- 当前用户与指定用户数据读取
- 收藏夹内容读取
- 评论发布/回复（可选 execute 控制）

## 1. Install MediaUse CLI

Install the MediaUse CLI in the user's own secure environment using the official npm package:

```powershell
npm install -g @mediause/cli
mediause --version
```

If the CLI is already installed, run the version check again to confirm it is available in PATH.

## 2. Key & Account Context

```powershell
mediause manage key --json
mediause auth list --json
mediause use account bilibili:<account_id> --json
mediause auth health --json
```

如需人工观察浏览器：

```powershell
mediause use account bilibili:<account_id> --show --json
```

风险说明：

- 对站点实时读取/互动动作，`--show` 通常可降低反爬挑战导致的拦截风险。

可选 guest：

```powershell
mediause use account bilibili:guest --json
```

## 3. 快速发现命令

```powershell
mediause plugin list --json
mediause plugin add bilibili --json
mediause bilibili -h
mediause bilibili account -h
mediause bilibili search -h
mediause bilibili get -h
mediause bilibili read -h
mediause bilibili user -h
mediause bilibili collection -h
mediause bilibili engage -h
```

## 4. Bilibili Site Command Map（Full）

来源：`crates/platforms/plugins/bilibili/manifest.yaml`

### 4.1 capability 概览

- `account`: `health`
- `search`: `video`, `user`
- `get`: `dynamic`, `hot`, `ranking`, `history`, `feed`
- `read`: `feed-detail`, `video`, `subtitle`, `summary`, `comments`, `dynamic`
- `user`: `me`, `profile`, `following`, `videos`, `feed`
- `collection`: `favorite`
- `engage`: `comment`

### 4.2 分组使用方式（按 capability）

```powershell
# account
mediause bilibili account health --json

# search
mediause bilibili search video --query <text> [--page <n>] [--limit <n>] --json
mediause bilibili search user --query <text> [--page <n>] [--limit <n>] --json

# get
mediause bilibili get dynamic [--limit <n>] --json
mediause bilibili get hot [--limit <n>] --json
mediause bilibili get ranking [--limit <n>] --json
mediause bilibili get history [--limit <n>] --json
mediause bilibili get feed [--type <text>] [--pages <n>] [--limit <n>] --json

# read
mediause bilibili read feed-detail --id <dynamic_id> --json
mediause bilibili read video --bvid <bvid> --json
mediause bilibili read subtitle --bvid <bvid> [--lang <code>] --json
mediause bilibili read summary --bvid <bvid> --json
mediause bilibili read comments --bvid <bvid> [--parent <id>] [--limit <n>] --json
mediause bilibili read dynamic --id <dynamic_id> --json

# user
mediause bilibili user me --json
mediause bilibili user profile [--uid <uid>] [--me <true|false>] --json
mediause bilibili user following [--uid <uid>] [--page <n>] [--limit <n>] --json
mediause bilibili user videos --uid <uid> [--order <text>] [--page <n>] [--limit <n>] --json
mediause bilibili user feed --uid <uid> [--type <text>] [--pages <n>] [--limit <n>] --json

# collection
mediause bilibili collection favorite [--fid <id>] [--page <n>] [--limit <n>] --json

# engage
mediause bilibili engage comment --bvid <bvid> --text <text> [--parent <id>] [--execute <true|false>] --json
```

### 4.3 关键参数速查

- 通用分页参数：`page`、`pages`、`limit`
- 视频唯一键：`bvid`
- 动态唯一键：`id`
- 用户唯一键：`uid`
- 评论回复参数：`parent`
- 评论执行开关：`execute`，`false` 用于只读参数检查，`true` 用于真实发布

## 5. Workflow Examples

### 5.1 搜索视频并读取详情

```powershell
mediause use account bilibili:<account_id> --json
mediause bilibili search video --query "AI" --limit 5 --json
mediause bilibili read video --bvid <bvid> --json
mediause bilibili read summary --bvid <bvid> --json
mediause trace last --json
```

### 5.2 获取关注动态并查看动态详情

```powershell
mediause use account bilibili:<account_id> --json
mediause bilibili get feed --type all --pages 1 --limit 20 --json
mediause bilibili read dynamic --id <dynamic_id> --json
mediause bilibili read feed-detail --id <dynamic_id> --json
mediause trace last --json
```

### 5.3 用户画像与视频列表

```powershell
mediause use account bilibili:<account_id> --json
mediause bilibili user profile --uid <uid> --json
mediause bilibili user videos --uid <uid> --order pubdate --limit 10 --json
mediause bilibili user following --uid <uid> --limit 20 --json
mediause trace last --json
```

### 5.4 评论读取与回复

```powershell
mediause use account bilibili:<account_id> --json
mediause bilibili read comments --bvid <bvid> --limit 20 --json
mediause bilibili engage comment --bvid <bvid> --text "学习了" --execute false --json
mediause bilibili engage comment --bvid <bvid> --text "学习了" --execute true --json
mediause trace last --json
```

## 6. Guardrails

- 遵守平台规则与当地法规
- 不绕过验证码、风控或封禁机制
- 不进行垃圾信息、诈骗、骚扰、仇恨、侵权等内容生成或投放
- 建议优先使用 `--json` 便于自动化处理
- 若遇到 `unusual traffic`、验证码或人工确认页面，建议使用 `--show` 人工处理后再继续

## 7. Quick Reference

```powershell
# install/update
npm install -g @mediause/cli
mediause --version

# discover
mediause plugin list --json
mediause plugin add bilibili --json
mediause bilibili -h
mediause bilibili read -h

# context
mediause auth list --json
mediause use account bilibili:<account_id> --json
mediause auth health --json

# common reads
mediause bilibili get hot --json
mediause bilibili read video --bvid <bvid> --json
mediause bilibili read subtitle --bvid <bvid> --lang zh-CN --json
mediause bilibili read summary --bvid <bvid> --json
mediause bilibili read comments --bvid <bvid> --json

# write (optional)
mediause bilibili engage comment --bvid <bvid> --text "学习了" --execute true --json

# trace
mediause trace last --json
```

Skill Metadata
Maintainer: @mediause-demo
Last-Updated: 2026-08-22
Version: v2


