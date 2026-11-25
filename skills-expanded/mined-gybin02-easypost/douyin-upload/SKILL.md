---
name: douyin-upload
description: 使用 EasyPost 自动填充或发布抖音创作者服务平台的短视频与图文。Use when 用户需要向抖音发布短视频或图集。
license: MIT-0
slug: easypost-douyin-upload
displayName: 抖音自动发布 (EasyPost)
version: 1.0.0
summary: 基于真实 Chrome 浏览器会话的抖音短视频与图文零风控自动发布。
---

# 抖音自动填充与发布 Skill

通过 EasyPost 驱动真实已登录的 Chrome 浏览器无感填充或发布抖音内容。

## 平台规格限制与最佳实践

- **内容形态**：
  - `shortVideo`：短视频（推荐 9:16 竖版高清 MP4/MOV）；
  - `imageText`：抖音图文（1~35 张图片）。
- **字段限制**：
  - **标题/文案**：标题最多 30 字；作品描述建议在 300 字以内，话题采用 `#话题` 格式；
  - **下载权限设置**：可在 `data.allowDownload` 中设置 `true`（允许下载）或 `false`（禁止下载）；
  - **个人声明**：支持自主声明（如原创、AI创作标注等）。

---

## 示例

### 发布抖音短视频
```bash
printf '%s\n' '{
  "type": "shortVideo",
  "platforms": ["douyin"],
  "data": {
    "title": "晨间高效生活习惯记录",
    "content": "保持专注与充沛精力的三个微习惯 #自我提升 #日常自律 #成长",
    "allowDownload": true
  },
  "assets": [
    {
      "path": "/absolute/path/to/vlog.mp4",
      "role": "media"
    },
    {
      "path": "/absolute/path/to/cover.jpg",
      "role": "cover"
    }
  ]
}' | easypost fill
```
