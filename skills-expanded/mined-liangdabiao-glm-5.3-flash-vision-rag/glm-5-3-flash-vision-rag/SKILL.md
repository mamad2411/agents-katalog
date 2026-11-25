---
name: glm-5.3-flash-vision-rag
description: 基于智谱GLM-5.3-Flash视觉大模型的PDF深度问答与检索（vision RAG）。当用户提到 PDF、文档、资料、报告、论文、电子书、手册、说明书，并想提问、查找、搜索、总结或理解其内容，或问"在哪一页"、"引用原文"、要页面截图时，使用本skill。支持扫描版、图表、表格、代码的视觉理解；回答带物理页码引用，并把命中页原图展示给用户。（GLM 版本；DeepSeek 版为 deepseek-v4-flash-vision-rag）
---

# GLM-5.3-Flash Vision RAG

用智谱 GLM-5.3-Flash 视觉大模型"看懂"整份 PDF：先为每页建立视觉索引
（一次性、缓存复用），再对用户问题做 本地粗筛 → 视觉精排 → 深读回答，
回答带 `[第N页]` 引用，并把命中页图片展示给用户。

与 DeepSeek 姊妹版同构：页码来自渲染天然精确；三层漏斗（免费粗筛→看图确认→深读作答）。
差异详见 `references/api-notes.md`（无 Files API 内联传图、reasoning_effort=low
等效关思考、图片按分辨率计费故 dpi 默认 110）。

## 环境

- Python：`openai`、`pymupdf(fitz)`；**ffmpeg 不需要**
- API key：环境变量 `GLM_API_KEY` 或 `~/.glm_api_key` 文件首行（代码不内置密钥）

## 工作流

### 第 1 步：建索引（每份 PDF 一次）

```bash
python scripts/ingest.py "<pdf路径>"
```

120 页约 3 分钟、6 次模型调用；重复运行命中缓存。参数：`--force` 重建｜
`--limit N` 只索引前 N 页试水｜`--clean` 清缓存。

### 第 2 步：提问

```bash
python scripts/ask.py "<pdf路径>" "问题"
```

输出四段：`=== 答案 ===`（带 [第N页] 引用）、`=== 引用页 ===`、
`=== 页面图片 ===`（PNG 在 ./pdf-vision-out/）、`=== 预览 ===`（自包含 HTML）。

### 第 3 步：展示

优先把 HTML 预览或 PNG 路径给用户双击打开；支持 inline 的环境可再 Read 图片作补充，
但不得只依赖 inline。

用户要看指定页：

```bash
python scripts/show.py "<pdf路径>" --pages 6,7 [--dpi 220]
```

## 回答规范

- 以脚本答案为事实基础组织回答，保留 `[第N页]` 标记；索引只覆盖部分页时如实说明
- 展示必须提供本地路径，不能只靠 inline 图片

## 注意事项

- 首次 ingest 分钟级正常；之后每次提问 2 次调用
- 调参/排错先读 `references/api-notes.md`（实测行为记录）
