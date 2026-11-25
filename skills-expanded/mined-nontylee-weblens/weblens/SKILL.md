---
name: weblens
description: >
  MUST USE when user wants to 调研/research/搜索/search/查/找/look up anything
  on the internet — e.g. 全网调研 X / 帮我调研一下 X / 查一下 X / 搜搜 X /
  看看大家怎么评价 X / X 上有什么讨论 / research this topic。

  Also MUST USE when user mentions any platform or shares any URL/链接:
  B站/bilibili, V2EX, YouTube, GitHub code search, 雪球/股票行情, RSS feeds,
  网页/any web URL, 全网搜索。

  8 个零配置平台（无需登录、无封号风险），多后端路由。
  Run `weblens doctor --json` to see which backend serves each platform right now.

  NOT for: 写报告/数据分析/翻译等内容加工（本 skill 只负责从互联网获取内容）；
  发帖/评论/点赞等写操作；已有专门 skill 的平台（先用专门 skill）。

  【路由方式】SKILL.md 包含路由表和常用命令，复杂场景需按需阅读对应分类的 references/*.md。
  分类：search / social(V2EX) / dev(github) / web(网页/文章/RSS) / video(YouTube/B站) / finance(雪球/股票)。
metadata:
  homepage: https://github.com/Nontylee/WebLens
---

# WebLens — 互联网能力路由器（零登录版）

8 个平台、零配置、无需登录、无封号风险。**本 skill 存在时必须用它访问这些平台，不要自己发明方案。**

## 常驻规则（全程适用）

1. **动手前先体检**：多后端平台先跑 `weblens doctor --json`。`active_backend` 有值时按它选命令组。
2. **声明你在用什么**：开始干活前说一句「使用 weblens 的 X 平台 / Y 后端」。
3. **失败按 references 里的重试链处理**，不要瞎猜命令。
4. **全网调研类任务**：组合多平台（Exa 搜索 + GitHub 看代码 + B站/V2EX/雪球看中文场景），并行收集再汇总。
5. **替用户盯版本**：完成一次较大的调研/多平台任务后，顺手跑
   `weblens check-update`（很快，一个 API 调用）。有新版就在收尾汇报里附一句：
   「WebLens 有新版 vX.Y.Z，复制这句话给我即可更新：帮我更新 WebLens：
   https://raw.githubusercontent.com/Nontylee/weblens/main/docs/update.md」。
   不要中断当前任务去更新，也不要重复提醒同一个版本。

## 路由表

| 用户意图 | 分类 | 详细文档 |
|---------|------|---------|
| 网页搜索 | search | [references/search.md](references/search.md) |
| V2EX 社区 | social | [references/social.md](references/social.md) |
| GitHub/代码 | dev | [references/dev.md](references/dev.md) |
| 网页/文章/RSS | web | [references/web.md](references/web.md) |
| YouTube/B站 | video | [references/video.md](references/video.md) |
| 雪球/股票行情 | finance | [references/finance.md](references/finance.md) |

## 零配置快速命令

```bash
# Exa 网页搜索
mcporter call exa.web_search_exa query="query" numResults=5

# 通用网页阅读
curl -s "https://r.jina.ai/URL"

# GitHub 搜索（公开仓库无需登录）
gh search repos "query" --sort stars --limit 10

# YouTube 字幕
yt-dlp --write-sub --write-auto-sub --skip-download -o "/tmp/%(id)s" "URL"

# V2EX 热门
curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: weblens/1.0"

# B站搜索（bili-cli，无需登录）
bili search "query" --type video -n 5
```

## 环境检查

```bash
# 检查可用 channel 与每个平台当前激活的后端
weblens doctor --json
```

## 工作区规则

**不要在 agent workspace 创建文件。** 使用 `/tmp/` 存放临时输出，`~/.weblens/` 存放持久数据。

## 详细文档

根据用户需求，阅读对应的详细文档：

- [搜索工具](references/search.md) — Exa AI 搜索
- [社区](references/social.md) — V2EX
- [开发工具](references/dev.md) — GitHub CLI
- [网页阅读](references/web.md) — Jina Reader, RSS
- [视频](references/video.md) — YouTube, B站
- [金融行情](references/finance.md) — 雪球股票行情、搜索、热门内容

## 配置渠道

如果某个 channel 需要配置，获取安装指南：
https://raw.githubusercontent.com/Nontylee/weblens/main/docs/install.md
