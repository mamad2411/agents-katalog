---
name: cnote
version: 0.1.16
description: 云端笔记——在 OneDrive 上管理轻量 HTML 笔记，支持查看、新建、追加、列表。需要 Microsoft 登录。想查电视节目去问 tv skill。【重要】必须先读 skill 原文获取正确命令格式，禁止瞎猜。
---

# 云端笔记

## 概述

在 OneDrive `Notes` 文件夹中管理 HTML 笔记。需要先登录 Microsoft 账号（登录方式见 cyeam-cli skill 的"登录方式"）。

```bash
cyeam cnote list                     # 列出所有笔记
cyeam cnote get "笔记标题"            # 查看（默认 markdown 格式）
cyeam cnote get "笔记标题" --format text
cyeam cnote new "笔记标题" < note.html
cyeam cnote append "笔记标题" < more.html
```

## 安装

```bash
# macOS Apple Silicon
curl -L https://github.com/mnhkahn/cyeam-cli/releases/latest/download/cyeam_Darwin_arm64.tar.gz | tar xz && chmod +x cyeam && sudo mv cyeam /usr/local/bin/

# macOS Intel
curl -L https://github.com/mnhkahn/cyeam-cli/releases/latest/download/cyeam_Darwin_x86_64.tar.gz | tar xz && chmod +x cyeam && sudo mv cyeam /usr/local/bin/

# Linux amd64
curl -L https://github.com/mnhkahn/cyeam-cli/releases/latest/download/cyeam_Linux_x86_64.tar.gz | tar xz && chmod +x cyeam && sudo mv cyeam /usr/local/bin/
```

检查安装：`which cyeam && cyeam version`

## 命令

```
cyeam whoami                         查看登录状态（登录方式见 cyeam-cli skill）

cyeam cnote list                     列出笔记（显示文件名、修改时间、可点击链接）
cyeam cnote get <title>              读取笔记内容（默认 markdown 渲染）
cyeam cnote get <title> --format text
cyeam cnote new <title> < note.html  从 stdin 创建笔记
cyeam cnote append <title> < note.html
```

## 数据存储

笔记存储在 OneDrive 的 `Notes/` 文件夹下，每篇笔记是一个 `.html` 文件。列表时如果有 `webUrl` 会显示可点击的"打开"链接。

## 注意事项

- 需要 Microsoft 账号登录，使用 Device Code 流程（登录方式见 cyeam-cli skill）
- 登录后 token 自动刷新（带 refresh_token）
- 内容是纯 HTML，`get` 命令会解析并转换为 markdown/text 显示
- `new` 和 `append` 从 stdin 读取，适合管道：`echo "<h1>hello</h1>" | cyeam cnote new test`