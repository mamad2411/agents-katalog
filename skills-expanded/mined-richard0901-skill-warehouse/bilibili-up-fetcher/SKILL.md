---
name: bilibili-up-fetcher
description: 获取 B 站 up 主所有视频的字幕并生成逐字稿。当用户想要获取某个 B 站 up 主的全部视频字幕内容时使用。
---

# Bilibili Up 主视频字幕抓取

**⚠️ 注意**：B 站大部分视频没有字幕（需要用户手动上传或开会员 AI 字幕），此工具目前功能有限。

## 当前可用方案

### 1. 获取弹幕（danmaku）
```bash
yt-dlp --write-subs --sub-lang danmaku --skip-download "https://www.bilibili.com/video/BV号"
```

### 2. 下载视频 + 语音识别（需要 whisper）
```bash
# 下载视频
yt-dlp "https://www.bilibili.com/video/BV号" -o "video.mp4"

# 用 whisper 识别（需要本地安装 whisper）
```

### 3. 使用 summarize skill（试验中）
```bash
npx -y summarize@latest "https://www.bilibili.com/video/BV号" --youtube auto
```

## 脚本（待完善）

- `fetch_up_videos.py` - 获取 up 主视频列表（API 限流严重）
- `fetch_single_video.py` - 获取单视频字幕（需要视频本身有字幕）

## 输出

- 目录：`~/Documents/life/workspace/bilibili/{up主名字}/`
- 文件格式：`{发布日期}_{BV号}_{标题}.md`

## 已知问题

- B 站 API 有严格限流，需要登录 Cookie 才能稳定调用
- 大部分视频没有字幕（除非 up 主手动上传）
- 需要 B 站大会员才能使用 AI 字幕功能
