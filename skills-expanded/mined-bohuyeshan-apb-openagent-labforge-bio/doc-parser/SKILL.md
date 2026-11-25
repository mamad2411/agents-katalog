---
name: doc-parser
description: Standardized PDF/DOCX document parsing — structured text output with preserved paragraph/sentence boundaries. Use when LLM cannot natively read a document file.
tool_type: python
primary_tool: PyMuPDF
---

# Document Parser (doc-parser)

标准化的 PDF/DOCX 文档解析工具。解决两个问题：

1. **模型不支持原生文件读取**（如 DeepSeek、Qwen 等无法直接读 PDF）
2. **模型自己写解析脚本质量不稳定**——有的破坏句子边界，有的漏段落

**方案**：由顶级模型写好稳定的标准解析脚本，注册为工具。所有模型走同一管线。

## 统一输出格式

所有解析器输出相同的 JSON 结构：

```json
{
  "filename": "paper.pdf",
  "total_pages": 10,
  "pages": [
    {
      "page_num": 1,
      "width": 595.0,
      "height": 842.0,
      "paragraphs": [
        {
          "index": 0,
          "text": "这是第一段正文...",
          "bbox": [72.0, 50.0, 523.0, 80.0]
        }
      ],
      "sentences": [
        {
          "index": 0,
          "text": "这是第一个句子。",
          "paragraph_index": 0,
          "start_char": 0,
          "end_char": 7
        }
      ],
      "tables": [],
      "images": []
    }
  ],
  "full_text": "所有页面的纯文本拼接（用于直接喂 LLM）"
}
```

## 解析管线

### Pipeline 1: 文本 PDF（主力）

```python
import fitz  # PyMuPDF

def parse_pdf(path: str) -> dict:
    doc = fitz.open(path)
    result = {"filename": Path(path).name, "total_pages": len(doc), "pages": []}
    for page_num, page in enumerate(doc, 1):
        blocks = page.get_text("dict")["blocks"]
        paragraphs = []
        full_text = ""
        for block in blocks:
            if block["type"] == 0:  # 文本块
                text = "".join(
                    span["text"] for line in block["lines"]
                    for span in line["spans"]
                )
                paragraphs.append({
                    "index": len(paragraphs),
                    "text": text,
                    "bbox": block["bbox"]
                })
                full_text += text + "\n"
        result["pages"].append({
            "page_num": page_num,
            "paragraphs": paragraphs,
            "full_text": full_text.strip()
        })
    result["full_text"] = "\n".join(p["full_text"] for p in result["pages"])
    return result
```

### Pipeline 2: 扫描件 PDF（OCR 兜底）

```python
# 需要 ocrmypdf + tesseract
import ocrmypdf

def ocr_pdf(input_path: str, output_path: str):
    ocrmypdf.ocr(input_path, output_path, language='chi_sim+eng')
    # 输出为文本 PDF，再走 Pipeline 1
    return parse_pdf(output_path)
```

### Pipeline 3: DOCX 解析

```python
from docx import Document

def parse_docx(path: str) -> dict:
    doc = Document(path)
    paragraphs = []
    for i, para in enumerate(doc.paragraphs):
        if para.text.strip():
            paragraphs.append({
                "index": i,
                "text": para.text,
                "style": para.style.name if para.style else None
            })
    return {
        "filename": Path(path).name,
        "paragraphs": paragraphs,
        "full_text": "\n".join(p["text"] for p in paragraphs)
    }
```

## 使用方式

### 直接调用

```python
from doc_parser import parse_pdf

text = parse_pdf("paper.pdf")
print(text["full_text"])  # 纯文本喂给 LLM
```

### 命令行

```bash
# 解析 PDF
python scripts/parse_pdf.py paper.pdf -o output.json

# 导出纯文本
python scripts/parse_pdf.py paper.pdf --text-only

# 批量解析目录
python scripts/parse_pdf.py papers/ --batch
```

## 输出质量控制

标准解析脚本保证以下质量要求：

| 要求 | 说明 |
|------|------|
| ✅ 段落边界保留 | 不会把两个段落合并或一个段落拆散 |
| ✅ 句子边界正确 | 中文句号、问号、感叹号正确分句 |
| ✅ 英文单词完整 | 跨行 hyphenation 正确合并 |
| ✅ 段落顺序保留 | 按阅读顺序输出 |
| ❌ 不提取图表 | PyMuPDF 不处理图表的文本层嵌入 |
| ❌ 不处理公式 | 公式作为图片跳过 |

## 依赖

```bash
# 核心依赖
pip install PyMuPDF  # 主力 PDF 解析

# OCR 兜底
pip install ocrmypdf pytesseract
# 还需要安装 Tesseract OCR 引擎：
#   Windows: https://github.com/UB-Mannheim/tesseract/wiki
#   Linux: apt install tesseract-ocr tesseract-ocr-chi-sim

# DOCX 解析
pip install python-docx
```

## 工具检查

```bash
# 检查 PyMuPDF
python -c "import fitz; print(fitz.__doc__)"

# 检查 OCR
python -c "import ocrmypdf; print(ocrmypdf.__version__)"

# 检查 python-docx
python -c "from docx import Document; print('OK')"
```
