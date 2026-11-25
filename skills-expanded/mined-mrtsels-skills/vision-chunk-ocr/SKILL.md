---
name: vision-chunk-ocr
description: OCR large images by splitting into chunks.
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [OCR, Vision, Chinese, ImageProcessing]
---

# Vision Chunk OCR

When `vision_analyze` rejects an image (too large, unsupported model, primary model doesn't support image_url) or tesseract Chinese OCR produces garbled output, split the image into chunks and OCR each chunk via `vision_analyze`.

**Does not** cover general PDF text extraction, scanned-PDF OCR pipelines, or tesseract tuning — see `ocr-and-documents` and `scanned-pdf-ocr` for those.

## When to Use

- `vision_analyze` returns 400: `unknown variant image_url` (model limitation)
- Tesseract Chinese OCR garbles dense tables with small CJK characters
- Any very tall/narrow image (e.g. 550×10000 px roster, scrollable table screenshot)
- You need structured tabular output from an image and the table has >50 rows

## Prerequisites

- `PIL/Pillow` (`pip install Pillow` if missing)
- Hermes `vision_analyze` tool (the fallback vision model handles images when the primary model doesn't)

## Procedure

### 1. Split the image into chunks

```python
from PIL import Image

img = Image.open('input.png')
w, h = img.size
# Target ~1000-1200 px per chunk
n = max(1, h // 1000)
chunk_h = h // n

for i in range(n):
    y1 = i * chunk_h
    y2 = (i + 1) * chunk_h if i < n - 1 else h
    chunk = img.crop((0, y1, w, y2))
    # Scale up 2x — helps the vision model read small text
    chunk = chunk.resize((w * 2, (y2 - y1) * 2), Image.LANCZOS)
    chunk.save(f'tmp/ocr_chunk_{i:02d}.png')
    print(f'Chunk {i}: saved ({chunk.size})')
```

### 2. OCR each chunk

Call `vision_analyze` for each chunk. Make the `question` very specific about the table structure and output format:

```
vision_analyze(
    image_url='tmp/ocr_chunk_00.png',
    question='OCR this table. Extract ALL rows with columns: [col1], [col2], ... Output as pipe-separated: col1|col2|col3. Do not skip any rows.'
)
```

Key tips:
- Name the expected columns explicitly in the question
- Request pipe-separated output (easier to parse than markdown tables)
- Say "output pipe-separated rows only, no other text" to suppress description prose
- For Chinese text, the question can be in Chinese or English — English works fine
- **Batch up to 4 independent chunks in one turn** for speed; they return in order

### 3. Merge and deduplicate

```python
all_rows = []
for chunk_id in range(n):
    # Copy rows from vision_analyze response manually
    pass  # merge into a single list

# Deduplicate overlapping rows at chunk boundaries
# (chunk N's last 2 rows may duplicate chunk N+1's first 2)
```

## Why This Works

The Hermes fallback vision model handles mixed Chinese/English text in tabular layouts far better than Tesseract, which confuses similar glyphs in dense CJK tables (e.g. 已/己, 亻/彳, 日/曰). Splitting bypasses the primary model's image rejection and keeps each chunk within the fallback model's effective resolution window.

## Pitfalls

- **Boundary duplicates**: the last 1-2 rows of chunk N may re-appear as the first 1-2 rows of chunk N+1. Deduplicate when merging.
- **Chunk size**: chunks >~1500px may also be rejected. Split to ~1000-1200px.
- **Chunk order**: chunks dispatched in parallel return in submission order — safe to batch 3-4 per turn.
- **Not for full-document OCR**: for multi-page PDFs, use `scanned-pdf-ocr` skill instead. This technique is for single-image data tables.
- **Vision model latency**: each chunk is an API call. For >15 chunks, consider whether the data justifies the cost/time.

## Verification

```bash
# Count extracted rows
grep -c "^[0-9]" tmp/ocr_output.csv
```
