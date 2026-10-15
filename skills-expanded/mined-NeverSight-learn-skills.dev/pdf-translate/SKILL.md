---
name: pdf-translate
version: 1.1.0
description: "pdf-cli 翻译模块：PDF 文档翻译全流程。支持查看语言列表、翻译引擎、上传文件、发起翻译（会员/免费）、arXiv 论文翻译、文本翻译、查询进度、下载结果、查看历史记录。"
metadata:
  requires:
    bins: ["pdf-cli"]
  cliHelp: "pdf-cli translate --help"
---

# translate

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../pdf-shared/SKILL.md`](../pdf-shared/SKILL.md)，其中包含认证、配置、错误处理**

## Core Concepts

- **file-key**: 上传文件后获得的唯一标识（`tmpFileName`），用于发起翻译
- **task-id**: 翻译任务标识（`blobFileName` 去掉扩展名），用于查询状态和下载结果
- **record-id**: 操作记录 ID（数字），用于下载翻译结果和查看记录详情

## 翻译工作流

```
1. languages  →  查看支持的语言列表
2. engines    →  查看可用翻译引擎
3. upload     →  上传 PDF 文件，获取 file-key
4. start      →  发起翻译（会员用户），获取 task-id
   free       →  免费翻译（无需登录），获取 task-id
   arxiv      →  arXiv 论文翻译，获取 task-id
5. status     →  查询翻译进度（支持 --wait 轮询）
6. download   →  下载翻译结果
```

## 命令概览

| 命令 | 说明 | 需要登录 |
|------|------|----------|
| [`languages`](references/pdf-translate-languages.md) | 获取支持的语言列表 | 否 |
| [`engines`](references/pdf-translate-engines.md) | 获取可用翻译引擎列表 | 否 |
| [`upload`](references/pdf-translate-upload.md) | 上传待翻译文件 | 是 |
| [`start`](references/pdf-translate-start.md) | 发起翻译任务（会员） | 是 |
| [`free`](references/pdf-translate-free.md) | 免费翻译（无需登录） | 否 |
| [`arxiv`](references/pdf-translate-arxiv.md) | arXiv 论文下载并翻译 | 否 |
| [`arxiv-info`](references/pdf-translate-arxiv-info.md) | 查询 arXiv 论文摘要 | 否 |
| [`text`](references/pdf-translate-text.md) | 文本内容翻译 | 是 |
| [`status`](references/pdf-translate-status.md) | 查询翻译进度 | 是 |
| [`continue`](references/pdf-translate-continue.md) | 继续暂停的翻译 | 是 |
| [`cancel`](references/pdf-translate-cancel.md) | 取消翻译任务 | 是 |
| [`download`](references/pdf-translate-download.md) | 下载翻译结果 | 是 |
| [`history`](references/pdf-translate-history.md) | 查看翻译记录 | 是 |

## 快速开始

```bash
# 查看支持的语言
pdf-cli translate languages

# 查看翻译引擎
pdf-cli translate engines

# 会员翻译流程（完整参数）
pdf-cli translate upload --file ./paper.pdf
pdf-cli translate start --file-key <file-key> --to zh --engine google --ocr --term-ids "1,2" --prompt-type 1
pdf-cli translate status --task-id <task-id> --wait
pdf-cli translate download --task-id <record-id>

# 免费翻译（无需登录）
pdf-cli translate upload --file ./paper.pdf
pdf-cli translate free --file-key <file-key> --to zh

# arXiv 论文翻译
pdf-cli translate arxiv --arxiv-id 2301.00001 --to zh --engine 1

# 文本内容翻译
pdf-cli translate text --record-id 123 --text "Hello World" --engine 1
```

## Important Notes

- 上传返回的 `file-key` 是 `tmpFileName` 字段，不是 `sourceFileId`
- 发起翻译返回的 `task-id` 是 `blobFileName` 去掉扩展名，用于 status 查询
- 发起翻译返回的 `record-id` 是数字 ID，用于 download 和 records 查询
- 翻译 API 要求 `ocrFlag` 参数，CLI 通过 `--ocr` flag 控制（默认关闭）
- status 查询的响应格式为 `{taskId: {status, translateRate, ...}}`，是嵌套结构
- `free` 命令无需登录，适合游客使用，但有排队限制
- `start` 命令支持 `--term-ids`（术语表）、`--prompt-type`（翻译风格）等高级参数
- `arxiv` 命令直接通过 arXiv ID 下载并翻译，无需先上传文件
