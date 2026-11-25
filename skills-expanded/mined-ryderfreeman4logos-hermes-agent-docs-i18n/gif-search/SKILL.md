---
name: gif-search
description: "Search/download GIFs from Tenor via curl + jq."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
prerequisites:
  env_vars: [TENOR_API_KEY]
  commands: [curl, jq]
metadata:
  hermes:
    tags: [GIF, Media, Search, Tenor, API]
---

# GIF搜索（Tenor API）

可通过curl直接利用Tenor API搜索并下载GIF文件，无需额外工具。

## 适用场景

适用于查找表情GIF、创建视觉内容，以及在聊天中发送GIF。

## 配置步骤

在您的环境变量中设置Tenor API密钥（请将其添加到`${HERMES_HOME:-~/.hermes}/.env`文件中）：

```bash
TENOR_API_KEY=your_key_here
```

您可以在 https://developers.google.com/tenor/guides/quickstart 获取免费的 API 密钥——Google Cloud Console 提供的 Tenor API 密钥完全免费，且拥有较为宽松的调用频率限制。

## 先决条件

- `curl` 和 `jq`（在 macOS/Linux 系统中均为标准工具）
- `TENOR_API_KEY` 环境变量

## 搜索 GIF 图片

```bash
# Search and get GIF URLs
curl -s "https://tenor.googleapis.com/v2/search?q=thumbs+up&limit=5&key=${TENOR_API_KEY}" | jq -r '.results[].media_formats.gif.url'

# Get smaller/preview versions
curl -s "https://tenor.googleapis.com/v2/search?q=nice+work&limit=3&key=${TENOR_API_KEY}" | jq -r '.results[].media_formats.tinygif.url'
```

## 下载 GIF 图片

```bash
# Search and download the top result
URL=$(curl -s "https://tenor.googleapis.com/v2/search?q=celebration&limit=1&key=${TENOR_API_KEY}" | jq -r '.results[0].media_formats.gif.url')
curl -sL "$URL" -o celebration.gif
```

## 获取完整元数据

```bash
curl -s "https://tenor.googleapis.com/v2/search?q=cat&limit=3&key=${TENOR_API_KEY}" | jq '.results[] | {title: .title, url: .media_formats.gif.url, preview: .media_formats.tinygif.url, dimensions: .media_formats.gif.dims}'
```

## API 参数

| 参数 | 描述 |
|------|------|
| `q` | 搜索查询（空格需用 `+` 进行 URL 编码） |
| `limit` | 最大返回结果数（1-50，默认为 20） |
| `key` | API 密钥（来自 `$TENOR_API_KEY` 环境变量） |
| `media_filter` | 格式过滤选项：`gif`、`tinygif`、`mp4`、`tinymp4`、`webm` |
| `contentfilter` | 安全级别：`off`、`low`、`medium`、`high` |
| `locale` | 语言代码：`en_US`、`es`、`fr` 等 |

## 支持的媒体格式

每个搜索结果都会在 `.media_formats` 字段中提供多种格式：

| 格式 | 适用场景 |
|------|----------|
| `gif` | 全质量 GIF 图片 |
| `tinygif` | 小尺寸预览 GIF 图片 |
| `mp4` | 视频版本（文件体积更小） |
| `tinymp4` | 小尺寸预览视频 |
| `webm` | WebM 视频格式 |
| `nanogif` | 极小尺寸缩略图 |

## 注意事项

- 需对搜索查询进行 URL 编码：空格替换为 `+`，特殊字符替换为 `%XX` 格式。
- 若在聊天中发送，`tinygif` 格式的链接文件体积更小。
- GIF 链接可直接用于 Markdown 中：`![标题](url)`
