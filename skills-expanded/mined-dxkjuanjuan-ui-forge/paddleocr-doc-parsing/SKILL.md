---
name: paddleocr-doc-parsing
description: >-
  Use this skill to extract structured Markdown/JSON from PDFs and document images—tables with
  cell-level precision, formulas as LaTeX, figures, seals, charts, headers/footers, multi-column
  layout and correct reading order.
  Trigger terms: 文档解析, 版面分析, 版面还原, 表格提取, 公式识别, 多栏排版, 扫描件结构化,
  发票, 财报, 复杂 PDF, PDF转Markdown, 图表, 阅读顺序; reading order, formula, LaTeX,
  layout parsing, structure extraction, PP-StructureV3, PaddleOCR-VL.
license: Apache-2.0
metadata:
  openclaw:
    requires:
      env:
        - PADDLEOCR_ACCESS_TOKEN
    primaryEnv: PADDLEOCR_ACCESS_TOKEN
    emoji: "📄"
---

# PaddleOCR Document Parsing

## When to Use This Skill

**Use this skill for**:

- Documents with tables (invoices, financial reports, spreadsheets)
- Documents with mathematical formulas (academic papers, scientific documents)
- Documents with charts and diagrams
- Multi-column layouts (newspapers, magazines, brochures)
- Complex document structures requiring layout analysis
- Converting PDFs to structured Markdown with images

## Usage

### Method 1: Python API (Recommended)

```python
import json, os, requests, sys, time

JOB_URL = "https://paddleocr.aistudio-app.com/api/v2/ocr/jobs"
TOKEN = os.environ.get("PADDLEOCR_ACCESS_TOKEN")
MODEL = "PaddleOCR-VL-1.6"

file_path = "<local file path or file url>"

headers = {"Authorization": f"bearer {TOKEN}"}

optional_payload = {
    "useDocOrientationClassify": True,
    "useDocUnwarping": True,
    "useChartRecognition": True,
}

# For URL input:
headers["Content-Type"] = "application/json"
payload = {"fileUrl": file_url, "model": MODEL, "optionalPayload": optional_payload}
job_response = requests.post(JOB_URL, json=payload, headers=headers)

# For local file input:
data = {"model": MODEL, "optionalPayload": json.dumps(optional_payload)}
with open(file_path, "rb") as f:
    job_response = requests.post(JOB_URL, headers=headers, data=data, files={"file": f})

assert job_response.status_code == 200
jobId = job_response.json()["data"]["jobId"]

# Poll for results:
while True:
    result = requests.get(f"{JOB_URL}/{jobId}", headers=headers).json()["data"]
    state = result["state"]
    if state == "done":
        jsonl_url = result["resultUrl"]["jsonUrl"]
        break
    elif state == "failed":
        print(f"Job failed: {result['errorMsg']}")
        sys.exit()
    time.sleep(5)

# Parse results and save:
lines = requests.get(jsonl_url).text.strip().split('\n')
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
page_num = 0
for line in lines:
    result = json.loads(line)["result"]
    for res in result["layoutParsingResults"]:
        # Save markdown
        md_filename = os.path.join(output_dir, f"doc_{page_num}.md")
        with open(md_filename, "w", encoding="utf-8") as md_file:
            md_file.write(res["markdown"]["text"])
        # Download images
        for img_path, img in res["markdown"]["images"].items():
            full_img_path = os.path.join(output_dir, img_path)
            os.makedirs(os.path.dirname(full_img_path), exist_ok=True)
            with open(full_img_path, "wb") as img_file:
                img_file.write(requests.get(img).content)
        # Download output images (layout visualization, etc.)
        for img_name, img in res["outputImages"].items():
            img_response = requests.get(img)
            if img_response.status_code == 200:
                filename = os.path.join(output_dir, f"{img_name}_{page_num}.jpg")
                with open(filename, "wb") as f:
                    f.write(img_response.content)
        page_num += 1
```

### Method 2: CLI

```bash
paddleocr api \
  --model_type doc_parsing \
  --file_path "./document.pdf"
```

## Important Notes

- For doc parsing, keep preprocessing enabled (useDocOrientationClassify, useDocUnwarping) by default
- Only disable preprocessing for flat, well-oriented scans where speed matters
- `useChartRecognition: True` enables chart/diagram extraction
- Output includes: Markdown text, inline images, layout visualization images
- Always display full extracted content, don't truncate unless exceeding 10,000 chars
- Handle errors gracefully: auth issues, rate limits, blank documents