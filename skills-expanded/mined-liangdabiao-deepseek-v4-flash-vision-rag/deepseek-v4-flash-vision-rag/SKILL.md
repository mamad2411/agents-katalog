---
name: deepseek-v4-flash-vision-rag
description: 基于DeepSeek视觉大模型（deepseek-v4-flash-vision-exp）的PDF深度问答与检索（vision RAG）。当用户提到 PDF、文档、资料、报告、论文、电子书、手册、说明书，并想提问、查找、搜索、总结或理解其内容，或问"在哪一页"、"引用原文"、要页面截图时，使用本skill。支持扫描版、图表、表格、代码的视觉理解；回答带物理页码引用，并把命中页原图展示给用户。
---

# DeepSeek V4-Flash Vision RAG

用 DeepSeek 视觉大模型"看懂"整份 PDF：先为每页建立视觉索引（一次性、缓存复用），
再对用户问题做 本地粗筛 → 视觉精排 → 深读回答，回答带 `[第N页]` 引用，
并把命中页图片展示给用户。

相比逐段文本 RAG，它直接看页面图像，因此能理解排版、图表、表格、代码块，
扫描版也能用；页码来自渲染本身，天然精确。

## 环境

- Python 依赖：`openai`、`pymupdf(fitz)`（本机已装；缺了先 `pip install`）
- API key：默认已内置；可用环境变量 `DEEPSEEK_API_KEY` 覆盖
- 所有脚本在 `scripts/` 下，Windows 下可直接 `python scripts/xxx.py`

## 工作流

### 第 1 步：建立索引（每份 PDF 一次，之后走缓存）

```bash
python scripts/ingest.py "<pdf路径>"
```

- 渲染每页 → Files API 上传 → 分批视觉分析 → 落盘 `scripts/.cache/<sha>/index.json`
- 120 页约 3–5 分钟、5 次模型调用；重复运行直接命中缓存
- 常用参数：`--force` 重建索引；`--limit N` 只索引前 N 页（大文档先试水）；
  `--clean` 删本地缓存
- 输出会打印页型分布（正文/目录/附录…）和大纲条数，可据此向用户简报文档结构

### 第 2 步：回答用户问题

```bash
python scripts/ask.py "<pdf路径>" "用户的问题"
```

- 流程：本地 TF-IDF 粗筛 top12 → 视觉精排选 top4（1 次调用）→ 命中页±1 深读
  （1 次调用，开推理）→ 输出带 `[第N页]` 引用的答案
- 可调：`--top K` 深读页数；`--cands N` 粗筛候选数；`--no-images` 不复制图片

脚本 stdout 分四段：`=== 答案 ===`、`=== 引用页 ===`、`=== 页面图片 ===`（图片
已复制到 `./pdf-vision-out/<书名>_p<N>.png`）。

### 第 3 步：向用户展示页面原图（必须做）

终端里用户**未必能看到 inline 图片**，所以必须给出用户自己能打开的路径，按优先级：

1. **HTML 预览（首选）**：ask.py 自动在 `./pdf-vision-out/` 生成 `<书名>_<问题>.html`
   ——自包含单文件（答案 + 全部引用页原图 base64 内嵌），把路径告诉用户，
   双击即可在浏览器查看，无需联网。Windows 下也可代用户执行 `start "<路径>"` 打开。
2. **单页 PNG 路径**：`./pdf-vision-out/<书名>_p<N>.png`，用户只要某几页时逐张给出。
3. 支持 inline 图片的环境（如 ZCode）可再用 Read 工具读取 PNG，把图渲染进对话作为
   **补充**；但不得只依赖这种方式——Read 的图用户端可能不显示。

用户想直接看某几页时：

```bash
python scripts/show.py "<pdf路径>" --pages 6,7 [--dpi 220]
```

然后把输出的 PNG 路径给用户（同样可 `start` 打开）。

## 回答规范

- 以脚本产出的答案为事实基础，组织成简洁中文回答；保留 `[第N页]` 引用标记
- 答案与引用页不符、或脚本说明"内容不足"时，如实告诉用户，不要编造
- 展示原图时必须提供用户可自行打开的本地路径（HTML 预览或 PNG），不能只靠
  inline 展示
- 可以顺带告诉用户引用页码，方便他翻原 PDF 对照

## 注意事项

- 首次 ingest 慢（分钟级）是正常的；告知用户后续提问秒级响应
- `--limit` 建过的索引是部分的，之后不带 `--limit` 重跑会自动补全
- API 细节（推理开关、384 token/图、Files API 限制等坑）见
  `references/api-notes.md`，改 `scripts/ds_client.py` 前必读
- 索引/缓存结构见 `references/index-schema.md`
