---
name: bilibili-upload
description: 使用 EasyPost 自动填充或发布哔哩哔哩（B站）视频或动态。Use when 用户需要向 B站 投稿视频或发布图文动态。
license: MIT-0
slug: easypost-bilibili-upload
displayName: 哔哩哔哩自动发布 (EasyPost)
version: 1.0.0
summary: 基于真实 Chrome 浏览器会话的 B站 视频投稿与图文动态自动发布。
---

# 哔哩哔哩（Bilibili）自动填充与发布 Skill

通过 EasyPost 驱动真实已登录的 B站 创作中心（`member.bilibili.com`）或动态主页（`t.bilibili.com`）。

## 平台规格限制与最佳实践

- **内容形态**：
  - `shortVideo`：视频投稿（横版 16:9 或竖版视频）；
  - `dynamic`：B站图文动态。
- **字段与封面规范**：
  - **视频标题**：最多 80 个字；
  - **横版封面（强烈推荐）**：B站视频推荐 16:9 横版封面，素材配置使用 `role: "horizontalCover"`；
  - **简介/标签**：支持详细视频简介与标签数组。

---

## 示例：视频投稿
```bash
printf '%s\n' '{
  "type": "shortVideo",
  "platforms": ["bilibili"],
  "data": {
    "title": "从零搭建个人多平台自动化分发流水线实战",
    "content": "本期视频手把手拆解如何通过真实浏览器扩展实现零风控分发，附源码与完整配置。",
    "tags": ["自动化", "生产力", "程序员", "创作工具"]
  },
  "assets": [
    {
      "path": "/absolute/path/to/video.mp4",
      "role": "media"
    },
    {
      "path": "/absolute/path/to/cover_16_9.jpg",
      "role": "horizontalCover"
    }
  ]
}' | easypost fill
```
