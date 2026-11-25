---
name: pdf-batch
description: 批量把含正文、表格、数学公式和图片的 PDF、DOCX、PPTX、XLSX 与图片转换为 Dify 文本库 Markdown 和多模态图片检索包。用户要求一键转换论文、OCR 扫描件、保留 LaTeX 公式/原图或生成批量转换清单时使用。
---

# 文档批量转 Markdown

调用 scripts/batch_convert.py 和 MinerU。保持输入文档只读，将结果写入 PROJECT_ROOT。旧式 `.doc` 先转换为 `.docx`。

输入目录、Markdown 输出目录和多模态包输出目录必须彼此分离，既不能相同也不能互相嵌套；否则递归发现可能把上次产物再次当作输入，工具会拒绝运行。

## 环境与运行

MinerU 在 Windows 上要求 Python 3.10 至 3.12。本机默认 Python 可以用于启动批处理，但 MinerU 应使用 uv 建立的独立 Python 3.12 工具环境：

    uv tool install --python 3.12 "mineru[all]"

安装体积较大，未经用户同意不要自动安装或下载模型。在 PROJECT_ROOT 中运行：

    python <SKILL_ROOT>\tools\pdf-batch\scripts\batch_convert.py --input knowledge_inbox\pdf --output knowledge_ready

默认使用支持纯 CPU 的 pipeline 后端。可用 --backend auto 切换默认后端，--dry-run 只检查计划，--force 强制重新转换。

推荐单次高精度转换同时生成文本库与图片库成品：

    python <SKILL_ROOT>\tools\pdf-batch\scripts\batch_convert.py --input <文档目录> --output <多模态包目录> --markdown-output <Markdown目录> --backend auto --effort high --image-analysis --dify-multimodal

此模式对每份文档只调用一次 MinerU，同时发布：

- 纯 Markdown：保留公式和图表分析文字、移除无法上传的本地图片链接，用于现有文本知识库。
- `.dify-mm.zip`：包含 `manifest.json`、`document.md` 和唯一命名的原图，用于配套 Dify 插件和统一多模态图片库。该包只索引含图片的块，正文仍由文本库负责。

只有两份成品都存在且不早于源文档时才跳过。中间 JSON、布局结果和临时目录在单篇完成后自动清理。

只需要一个 Markdown 时仍可使用 `--md-only`。

## 输出与检查

- 图片名包含源文档哈希、图序号和图片哈希；插件再按清单路径与 SHA-256 校验，避免跨论文串图。
- 同名且同扩展名的源文档会在输出名中加入内容哈希，避免覆盖。
- batch_report.json 记录源文件 SHA-256、命令、状态、耗时和输出。
- dify_upload_list.txt 列出成功生成的 Markdown，供用户手动上传。
- conversion.log 保存每篇文档的 MinerU 输出。

重复运行时跳过未变化且两份成品均已存在的文件。文本 Markdown 上传普通知识库；`.dify-mm.zip` 只上传统一多模态图片库。
