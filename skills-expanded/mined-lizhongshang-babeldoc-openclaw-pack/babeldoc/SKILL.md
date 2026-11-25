---
name: babeldoc
description: Use when translating PDF papers, manuals, or technical documents with BabelDOC while preserving layout, formulas, page ranges, bilingual output, glossaries, or offline assets.
---

# BabelDOC PDF 翻译

## 适用范围

当用户要做下列事情时使用本技能：

- 翻译科研论文、白皮书、技术手册等 PDF
- 生成双语对照 PDF 或仅保留译文页
- 对指定页做局部翻译
- 为术语统一提供 glossary CSV
- 为离线环境预热或导出 BabelDOC 离线资源

本技能优先调用 BabelDOC CLI，而不是直接依赖其内部 Python API。BabelDOC 官方将 API 视为内部接口，CLI 更稳定。

## 前置条件

1. BabelDOC 当前要求 Python `>=3.10,<3.14`。
2. 当前机器如果只有 Python 3.14，先安装 Python 3.12 或 3.13。
3. 推荐先安装 `uv`，但本技能也支持用 venv + pip 安装。

## 本地源码镜像

当前仓库随附一份 BabelDOC 源码镜像：

- 仓库相对路径：`../babeldoc-source`
- 镜像来源：`https://gitee.com/mirrors/babeldoc.git`
- 当前锁定版本：`v0.5.24`
- 当前 commit：`b1843ce5b0c719201532daa7c6f0c868f70d1373`

优先把仓库内的 `babeldoc-source` 视为可复刻基线，不必每次重新联网查找。

## 安装

优先运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_babeldoc.ps1
```

如果机器上有多个 Python，可显式指定：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_babeldoc.ps1 -PythonExe "C:\Python312\python.exe"
```

安装完成后，优先使用以下位置的可执行文件：

- `scripts\.venv\Scripts\babeldoc.exe`
- 环境变量 `BABELDOC_BIN`
- 系统 `PATH` 中的 `babeldoc`

## 从源码安装

如果你希望固定使用本地镜像源码，而不是 PyPI 版本，运行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_babeldoc_from_source.ps1
```

如需指定源码目录和 Python：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_babeldoc_from_source.ps1 `
  -SourceDir "..\babeldoc-source" `
  -PythonExe "C:\Python312\python.exe"
```

安装成功后，`translate_pdf.py` 会优先使用技能目录里的源码模式虚拟环境。

## 同步镜像

如需从 Gitee 镜像更新本地源码：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\sync_babeldoc_source.ps1
```

默认同步目录就是当前本地镜像目录。

## 常用工作流

### 固定预设

本技能已提供 3 个可直接调用的固定预设：

- `openai`：默认走 MiniMax，适合普通论文
- `deepseek`：走 DeepSeek OpenAI-compatible 接口
- `compat`：MiniMax 兼容性优先，适合复杂排版或问题 PDF

对应模板文件：

- `presets/openai-gpt4o-mini.toml`
- `presets/deepseek-chat.toml`
- `presets/openai-gpt4o-mini-compat.toml`

### 1. 基础翻译

```powershell
python .\scripts\translate_pdf.py `
  --input "C:\docs\paper.pdf" `
  --output-dir "C:\docs\out" `
  --openai `
  --openai-model "gpt-4o-mini" `
  --openai-base-url "https://api.openai.com/v1" `
  --openai-api-key "YOUR_KEY"
```

### 1.2 用固定预设直接跑

OpenAI 预设：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_babeldoc_preset.ps1 `
  -Preset openai `
  -InputPdf "C:\docs\paper.pdf" `
  -OutputDir "C:\docs\out" `
  -ApiKey "YOUR_KEY"
```

当前 `openai` 预设实际使用：

- model: `MiniMax-M2.7-highspeed`
- base url: `https://api.minimax.chat/v1`
- 已内置 no-think 清洗友好 prompt
- 已关闭自动术语提取，避免额外 JSON 噪声

DeepSeek 预设：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_babeldoc_preset.ps1 `
  -Preset deepseek `
  -InputPdf "C:\docs\paper.pdf" `
  -OutputDir "C:\docs\out" `
  -ApiKey "YOUR_KEY"
```

兼容模式预设：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_babeldoc_preset.ps1 `
  -Preset compat `
  -InputPdf "C:\docs\paper.pdf" `
  -OutputDir "C:\docs\out" `
  -ApiKey "YOUR_KEY"
```

仅翻译部分页：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_babeldoc_preset.ps1 `
  -Preset openai `
  -InputPdf "C:\docs\paper.pdf" `
  -OutputDir "C:\docs\out" `
  -Pages "1-3,8,10-12" `
  -ApiKey "YOUR_KEY"
```

携带术语表：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_babeldoc_preset.ps1 `
  -Preset openai `
  -InputPdf "C:\docs\paper.pdf" `
  -OutputDir "C:\docs\out" `
  -GlossaryFile "C:\docs\glossary.csv" `
  -ApiKey "YOUR_KEY"
```

### 1.1 从本地源码直接运行

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_babeldoc_source.ps1 --help
```

或直接转 PDF：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_babeldoc_source.ps1 `
  --files "C:\docs\paper.pdf" `
  --openai `
  --openai-model "gpt-4o-mini" `
  --openai-base-url "https://api.openai.com/v1" `
  --openai-api-key "YOUR_KEY"
```

### 2. 指定页翻译

```powershell
python .\scripts\translate_pdf.py `
  --input "C:\docs\paper.pdf" `
  --pages "1-3,8,10-12" `
  --output-dir "C:\docs\out" `
  --openai `
  --openai-model "deepseek-chat" `
  --openai-base-url "https://api.deepseek.com/v1" `
  --openai-api-key "YOUR_KEY"
```

### 3. 兼容性优先

出现排版或阅读器兼容问题时，优先加：

- `--enhance-compatibility`
- `--max-pages-per-part 50`
- `--skip-scanned-detection` 或 `--ocr-workaround`

### 4. 只输出译文页

```powershell
python .\scripts\translate_pdf.py `
  --input "C:\docs\paper.pdf" `
  --pages "1-5" `
  --only-include-translated-page `
  --output-dir "C:\docs\out" `
  --openai `
  --openai-model "gpt-4o-mini" `
  --openai-base-url "https://api.openai.com/v1" `
  --openai-api-key "YOUR_KEY"
```

## 术语表

如果用户要求术语统一，传入 CSV：

```powershell
python .\scripts\translate_pdf.py `
  --input "C:\docs\paper.pdf" `
  --output-dir "C:\docs\out" `
  --glossary-file "C:\docs\glossary.csv" `
  --openai `
  --openai-model "gpt-4o-mini" `
  --openai-base-url "https://api.openai.com/v1" `
  --openai-api-key "YOUR_KEY"
```

CSV 建议列名：

- `src`
- `dst`
- `note`
- `tgt_lng`

## 离线资源

首次在线环境可以先预热或导出离线资源：

```powershell
python .\scripts\translate_pdf.py --warmup
python .\scripts\translate_pdf.py --generate-offline-assets "C:\babeldoc-assets"
```

离线机器恢复：

```powershell
python .\scripts\translate_pdf.py --restore-offline-assets "C:\babeldoc-assets\offline_assets_xxx.zip"
```

## 执行策略

- 优先使用绝对路径
- 默认输出目录显式指定 `--output-dir`
- 大文件优先启用 `--max-pages-per-part`
- 遇到扫描版 PDF，先尝试 `--auto-enable-ocr-workaround`
- 遇到复杂表格或版式异常，可尝试 `--translate-table-text`、`--disable-rich-text-translate`
- 日常使用优先走 `run_babeldoc_preset.ps1`
- 需要细调参数时再用 `translate_pdf.py` 或 `run_babeldoc_source.ps1`
- 当前默认推荐模型链路就是 `MiniMax-M2.7-highspeed`

## 关键事实

- BabelDOC 官方更推荐 CLI，用于直接翻译 PDF。
- 当前主要验证充分的方向是英文到中文，其他语言方向可用但稳定性要额外验证。
- 目前只支持 OpenAI-compatible LLM 接口。
- 仓库内 `babeldoc-source` 是 `Gitee` 镜像源码，可作为稳定复刻基线。
