---
name: wechat-article-to-md
description: 抓取微信公众号文章并转换为 Markdown 文档。使用脚本自动获取文章标题、作者、正文内容，保留格式并保存为 .md 文件，支持下载图片到本地。适用场景：用户要求抓取/获取/下载/保存微信公众号文章内容为 Markdown 格式，或给出 mp.weixin.qq.com 链接需要提取内容。支持 Obsidian 模式（使用 -obsidian 参数）。
---

# 微信公众号文章转 Markdown

抓取微信公众号文章并将其转换为 Markdown 文档。

## 快速使用

### 普通模式
```bash
# 基本用法（自动下载图片）
python3 scripts/wechat_article_to_md.py <文章URL>

# 指定输出目录
python3 scripts/wechat_article_to_md.py <文章URL> <输出目录>
```

**图片保存位置**: `images/`
**图片引用格式**: `![alt](images/filename.png)`

### Obsidian 模式
```bash
# 使用 Obsidian 格式
python3 scripts/wechat_article_to_md.py <文章URL> [输出目录] -obsidian
```

**图片保存位置**: `attachments/img/`（向上查找固定的目录，可能位于输出目录的上级或更上级）
**图片引用格式**: `![[filename.png]]`

## 输出内容

脚本会自动提取并保存：

- **标题**: 文章主标题
- **作者**: 公众号作者名称
- **来源**: 原文链接
- **正文**: 完整内容，转换为 Markdown 格式
  - 标题层级 (h1-h6)
  - 粗体、斜体
  - 列表（有序/无序）
  - 链接
  - 图片（保留图片链接）
  - 代码块
  - 引用块

## 文件命名

输出文件名自动使用文章标题，文件名中的非法字符会被自动替换为下划线。

## 脚本位置

可执行脚本位于 `scripts/wechat_article_to_md.py`。