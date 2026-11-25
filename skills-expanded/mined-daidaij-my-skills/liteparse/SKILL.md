---
name: liteparse
description: Use this skill when the user asks to parse or extract text from PDF files locally without cloud dependencies.
---

# LiteParse Skill

本地解析 PDF 文档，无需云端依赖或 LLM。

## ⚠️ 必须使用本 skill 目录下的 lit.exe

**不要使用系统 PATH 中的 lit**，必须使用本 skill 目录下的 `lit.exe`（即 `SKILL.md` 同级目录）。

调用时，将 `SKILL.md` 所在目录的绝对路径拼上 `lit.exe` 作为可执行文件路径。例如：
- 若 skill 目录为 `~/.qwen/skills/liteparse/`，则命令为 `~/.qwen/skills/liteparse/lit.exe parse ...`
- 后续用 `<LIT>` 代表此完整路径

## 基本用法

```bash
<LIT> parse path_to_you_want_pdf.pdf --no-ocr -o path_to_you_want_txt.txt
```

输出示例：
```
[liteparse] extract: 116.4ms (49 pages)
[liteparse] ocr: 0.0ms
[liteparse] project: 5.7ms
[liteparse] total: 122.4ms
[liteparse] wrote output to path_to_you_want_txt.txt
```

## 批量解析

```bash
# 解析目录下所有文件，输出到指定目录
<LIT> batch-parse ./input-directory ./output-directory --no-ocr

# 仅解析 PDF，递归子目录
<LIT> batch-parse ./input ./output --extension .pdf --recursive --no-ocr
```

## ⚠️ 大文件处理

输出会显示提取的页数。**当页数超过 2 页时，不要全量读取文件**，应使用 `grep_search` 搜索关键词定位相关段落，再用 `read_file` 的 `offset` + `limit` 读取目标部分。

## 常用选项

| 选项 | 说明 |
|------|------|
| `--no-ocr` | 禁用 OCR（纯文本 PDF 推荐，更快） |
| `-o <file>` | 输出到文件 |
| `--format json` | JSON 格式输出（含 bounding box） |
| `--dpi <n>` | 渲染 DPI（默认 150，高质量用 300） |
| `--target-pages "1-5,10"` | 指定页码范围 |

## 支持格式

PDF。
