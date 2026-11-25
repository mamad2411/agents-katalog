---
name: paddleocr-text-recognition
description: >-
  Use this skill whenever the user wants text extracted from images, photos, scans, screenshots,
  or scanned PDFs. Returns exact machine-readable strings with line-level text and optional bbox
  coordinates. Strong accuracy for CJK, small print, and handwritten text.
  Trigger terms: OCR, 文字识别, 图片转文字, 截图识字, 提取图中文字, 扫描识字, 识字, 纯文字,
  plain text extraction, 坐标, 检测框, bbox, bounding box, image to text, screenshot, photo scan,
  recognize text.
license: Apache-2.0
metadata:
  openclaw:
    requires:
      env:
        - PADDLEOCR_ACCESS_TOKEN
    primaryEnv: PADDLEOCR_ACCESS_TOKEN
    emoji: "🔤"
---

# PaddleOCR Text Recognition

## When to Use This Skill

**Use this skill for**:

- Extract text from images (screenshots, photos, scans)
- Extract text from PDFs or document images when the goal is **line/box-level text**
- Extract text from URLs or local files that point to images/PDFs

**Do not use for**:

- Documents with tables, formulas, charts, or complex layouts — use Document Parsing instead

## Usage

### Method 1: Python API (Recommended)

Run a Python script to call the PaddleOCR API directly:

```python
import json, os, requests, sys, time

JOB_URL = "https://paddleocr.aistudio-app.com/api/v2/ocr/jobs"
TOKEN = os.environ.get("PADDLEOCR_ACCESS_TOKEN")
MODEL = "PaddleOCR-VL-1.6"

headers = {"Authorization": f"bearer {TOKEN}"}

optional_payload = {
    "useDocOrientationClassify": False,
    "useDocUnwarping": False,
    "useChartRecognition": False,
}

# For URL input:
headers["Content-Type"] = "application/json"
payload = {"fileUrl": file_url, "model": MODEL, "optionalPayload": optional_payload}
job_response = requests.post(JOB_URL, json=payload, headers=headers)

# For local file input:
data = {"model": MODEL, "optionalPayload": json.dumps(optional_payload)}
with open(file_path, "rb") as f:
    job_response = requests.post(JOB_URL, headers=headers, data=data, files={"file": f})

jobId = job_response.json()["data"]["jobId"]

# Poll for results:
while True:
    result = requests.get(f"{JOB_URL}/{jobId}", headers=headers).json()["data"]
    if result["state"] == "done":
        break
    elif result["state"] == "failed":
        print(f"Job failed: {result['errorMsg']}")
        sys.exit()
    time.sleep(5)

# Get OCR text:
jsonl_url = result["resultUrl"]["jsonUrl"]
lines = requests.get(jsonl_url).text.strip().split('\n')
for line in lines:
    page_result = json.loads(line)["result"]
    for res in page_result["layoutParsingResults"]:
        # res["markdown"]["text"] contains the recognized text
        print(res["markdown"]["text"])
```

### Method 2: CLI

```bash
paddleocr api \
  --model_type ocr \
  --file_path "./document.pdf"
```

## Important Notes

- Always use `PADDLEOCR_ACCESS_TOKEN` env var for auth, never hardcode tokens
- For flat images (screenshots, properly scanned docs), disable preprocessing for speed:
  `useDocOrientationClassify: False, useDocUnwarping: False`
- Display full extracted content, don't truncate with "..." unless exceeding 10,000 chars
- Handle errors gracefully: auth issues, rate limits, blank images