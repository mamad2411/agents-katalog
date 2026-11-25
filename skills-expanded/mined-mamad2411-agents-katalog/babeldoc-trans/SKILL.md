---
name: babeldoc-trans
description: "PDF论文自动翻译工具。使用 BabelDOC 引擎将英文 PDF 论文翻译为中文，保留原始版面（图表、公式、图片位置不变），输出文件自动以论文的中文标题命名。支持 arxiv URL / arxiv ID / 本地 PDF 路径作为输入。当用户发送 arxiv 链接、上传 PDF 文件、或说翻译论文、翻译这篇 PDF、translate paper、把论文译成中文时触发。"
---

# BabelDOC 论文翻译

基于 [BabelDOC](https://github.com/funstory-ai/BabelDOC) 的论文 PDF 翻译封装。智能版式分析 + 公式保护 + 术语自动提取，输出自动以中文标题命名。

## 触发条件

- 用户发送 arxiv 链接（`https://arxiv.org/abs/xxxx.xxxxx` 或 `https://arxiv.org/pdf/xxxx.xxxxx`）
- 用户发送 arxiv ID（如 `2412.13211`）
- 用户上传或指定 PDF 文件路径
- 用户说"翻译这篇论文"、"translate this paper"等

## 工作流程

### 步骤 1：获取 SKILL 路径

确定本 skill 的安装路径（即包含此 SKILL.md 的目录），用于定位 `scripts/translate.py`。

### 步骤 2：执行翻译

```bash
python {SKILL_DIR}/scripts/translate.py "<输入>" --output-dir /tmp/babeldoc_output
```

**输入可以是：**
- arxiv URL：`https://arxiv.org/abs/2412.13211`
- arxiv PDF URL：`https://arxiv.org/pdf/2412.13211`
- arxiv ID：`2412.13211`
- 本地 PDF 路径：`/path/to/paper.pdf`

### 步骤 3：返回结果

脚本最后会打印 `[DONE] {JSON}`，包含：
- `title_en` / `title_zh` — 英文/中文标题
- `output_pdf` — 最终 PDF 绝对路径（已以中文标题命名）
- `size_kb` — 文件大小

将翻译后的 PDF 文件发送给用户。

## 常用参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--output-dir` | PDF 输出目录 | `/tmp/babeldoc_output` |
| `--pages` | 只翻译指定页，如 `1-5` | 全部 |
| `--qps` | 翻译并发 QPS | `8` |
| `--dual` | 额外输出双语对照 PDF | off |
| `--model` | OpenAI 模型 | `gpt-4o-mini` |
| `--api-base` | API base URL | `https://api.bltcy.ai/v1` |
| `--api-key` | API key | 读取 `$BABELDOC_API_KEY` |

## 环境变量

| 变量 | 说明 | 必须 |
|------|------|------|
| `BABELDOC_API_KEY` | OpenAI 兼容 API key | 是 |
| `BABELDOC_API_BASE` | API base URL | 否（默认 `https://api.bltcy.ai/v1`） |
| `BABELDOC_MODEL` | 模型名 | 否（默认 `gpt-4o-mini`） |

## 安装依赖

首次使用前运行：
```bash
bash {SKILL_DIR}/scripts/setup.sh
```

## 详细文档

更多参数说明、性能参考和常见问题排查，请查阅 `references/usage_guide.md`。
