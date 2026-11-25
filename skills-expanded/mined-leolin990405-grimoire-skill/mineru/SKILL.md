---
name: mineru
description: MinerU document parsing API - convert PDF/DOC/PPT/images to Markdown/JSON. Supports OCR, formula recognition, table extraction, and batch processing.
triggers:
  - mineru
  - pdf解析
  - 文档解析
  - document parsing
  - pdf to markdown
  - extract pdf
---

# MinerU API Skill

## Overview
MinerU converts PDF, DOC, DOCX, PPT, PPTX, PNG, JPG, JPEG, HTML into machine-readable Markdown/JSON. Supports OCR (109 languages), formula/table recognition, cross-page table merging, and batch processing.

**Two modes:**
- **Cloud API** — `https://mineru.net/api/v4` (no GPU required, token-based)
- **Local API** — `mineru-api --port 8000` (self-hosted, requires GPU or CPU backend)

## Authentication (Cloud API)

- **Token file**: `~/.config/mineru/token`
- **Header**: `Authorization: Bearer <token>`
- **Get token**: https://mineru.net/apiManage/token

```bash
mkdir -p ~/.config/mineru
echo "YOUR_TOKEN" > ~/.config/mineru/token
chmod 600 ~/.config/mineru/token
```

## Limits (Cloud API)

| Item | Limit |
|------|-------|
| Single file size | 200MB max |
| Single file pages | 600 pages max |
| Daily priority pages | 2000 pages/account |
| Batch upload | 200 files/request |
| Token validity | 90 days |

## Model Versions

| Model | Use Case | Speed | Notes |
|-------|----------|-------|-------|
| `hybrid` | **Default since v2.7.0** — best of pipeline + vlm | Medium | Recommended for most use |
| `pipeline` | General documents, CPU-friendly | Fast | Pure CPU support |
| `vlm` | Complex layouts, higher accuracy | Slower | Needs GPU (10GB+ VRAM) |
| `MinerU-HTML` | HTML output, preserves formatting | Medium | For web content |

## API Endpoints (Cloud)

Base URL: `https://mineru.net/api/v4`

### 1. Create Extraction Task (Single File)
```
POST /extract/task
```

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| url | string | yes | - | File URL (no direct upload) |
| model_version | string | no | hybrid | `hybrid` / `pipeline` / `vlm` / `MinerU-HTML` |
| is_ocr | bool | no | false | Enable OCR |
| enable_formula | bool | no | true | Formula recognition |
| enable_table | bool | no | true | Table recognition |
| language | string | no | ch | Document language |
| data_id | string | no | - | Custom identifier |
| page_ranges | string | no | - | e.g. "2,4-6" |
| callback | string | no | - | Callback URL for async results |
| extra_formats | array | no | - | `["docx"]`, `["html"]`, `["latex"]` |

**Response:**
```json
{"code": 0, "data": {"task_id": "xxx"}, "msg": "ok"}
```

### 2. Get Task Results
```
GET /extract/task/{task_id}
```

**States:** `pending` → `running` → `done` / `failed` / `converting`

**Done response:** includes `full_zip_url` (download link)

### 3. Batch Upload Local Files
```
POST /file-urls/batch
```
Returns presigned upload URLs (valid 24h). System auto-submits extraction after upload.

### 4. Batch URL Extraction
```
POST /extract/task/batch
```
Submit multiple URLs at once, returns `batch_id`.

### 5. Batch Results
```
GET /extract-results/batch/{batch_id}
```

## Local API (Self-Hosted)

### Start Server
```bash
# FastAPI server
mineru-api --host 0.0.0.0 --port 8000

# Gradio WebUI
mineru-gradio --server-name 0.0.0.0 --server-port 7860

# OpenAI-compatible server (for remote VLM inference)
mineru-openai-server --port 30000
```

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `MINERU_MODEL_SOURCE` | Model source: `modelscope` / `huggingface` | huggingface |
| `MINERU_API_MAX_CONCURRENT_REQUESTS` | Max concurrent API requests | Unlimited |
| `MINERU_API_ENABLE_FASTAPI_DOCS` | Enable /docs page | true |

### Local API Docs
Access at `http://127.0.0.1:8000/docs` after starting.

### Use CLI with Remote Server
```bash
mineru -p input.pdf -o output/ -b hybrid-http-client -u http://server:30000
```

## Error Codes

| Code | Issue | Fix |
|------|-------|-----|
| A0202 | Token invalid | Check Bearer prefix and token |
| A0211 | Token expired | Recreate at mineru.net |
| -60002 | Unrecognized format | Check file extension |
| -60005 | File too large | Max 200MB |
| -60006 | Too many pages | Max 600, split document |
| -60008 | URL timeout | Check URL accessibility |
| -60012 | Task not found | Verify task_id |

## Helper Script

`~/.claude/skills/mineru/scripts/mineru-parse.sh` — full-featured CLI wrapper.

```bash
# URL mode
mineru-parse.sh https://example.com/doc.pdf

# Local file with options
mineru-parse.sh /path/to/file.pdf --model vlm --ocr --output /tmp/result

# Extra formats
mineru-parse.sh doc.pdf --format docx --format latex

# Page ranges
mineru-parse.sh doc.pdf --pages "1-5,8" --output ./results

# Auto-extract markdown from zip
mineru-parse.sh doc.pdf --output ./results --extract
```

## Quick Parse (Python)

```python
import requests, time

TOKEN = open("~/.config/mineru/token").read().strip()
BASE = "https://mineru.net/api/v4"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def parse_document(url, model="hybrid", ocr=False, extra_formats=None):
    """Parse a document from URL, return download link."""
    body = {
        "url": url, "model_version": model,
        "is_ocr": ocr, "enable_formula": True, "enable_table": True,
    }
    if extra_formats:
        body["extra_formats"] = extra_formats

    resp = requests.post(f"{BASE}/extract/task", headers=HEADERS, json=body)
    task_id = resp.json()["data"]["task_id"]

    while True:
        result = requests.get(f"{BASE}/extract/task/{task_id}", headers=HEADERS).json()
        state = result["data"]["state"]
        if state == "done":
            return result["data"]["full_zip_url"]
        elif state == "failed":
            raise Exception(f"Task failed: {result}")
        time.sleep(5)
```

## Quick Parse (curl)

```bash
TOKEN=$(cat ~/.config/mineru/token)

# Submit
curl -s -X POST "https://mineru.net/api/v4/extract/task" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/doc.pdf","model_version":"hybrid"}'

# Check result
curl -s "https://mineru.net/api/v4/extract/task/{task_id}" \
  -H "Authorization: Bearer $TOKEN"
```

## Installation (Local Mode)

```bash
pip install uv
uv pip install -U "mineru[all]"
```

Requirements: Python 3.10-3.13, 16GB+ RAM, 20GB+ SSD. GPU optional (Volta+ or Apple Silicon).
