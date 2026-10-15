---
name: ocr-recognition
description: |
  OCR (Optical Character Recognition) for extracting text from images.
  Use when user needs to: (1) Extract text from screenshots, (2) Recognize captcha codes, 
  (3) Read text from photos, (4) Convert scanned PDFs to text, (5) Identify numbers/letters from images.
  Supports Tesseract OCR with Docker, Python OpenCV preprocessing, and decision flow for captcha recognition.
---

# OCR Recognition

## Quick Start

### 1. Check System Tesseract

```bash
which tesseract
tesseract --version
```

### 2. Docker Alternative (No Install Required)

```bash
# Pull image (one-time)
docker pull minidocks/tesseract:latest

# Download language pack (注意：-L 跟随重定向，-O 指定输出文件)
wget -L -O /tmp/eng.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata

# 推荐：映射整个 tessdata 目录（更可靠）
mkdir -p /tmp/tessdata
mv /tmp/eng.traineddata /tmp/tessdata/

docker run --rm \
  -v /path/to/image.png:/image.png:ro \
  -v /tmp/tessdata:/usr/share/tessdata:ro \
  minidocks/tesseract:latest \
  tesseract /image.png stdout
```

### 3. Digits Only (for captcha)

```bash
docker run --rm \
  -v /path/to/captcha.png:/captcha.png:ro \
  -v /tmp/tessdata:/usr/share/tessdata:ro \
  minidocks/tesseract:latest \
  tesseract /captcha.png stdout --psm 6 -c tessedit_char_whitelist=0123456789
```

## Decision Flow

See [references/decision-flow.md](references/decision-flow.md) for complete decision tree.

### TL;DR

1. System has tesseract? → Use it
2. No sudo? → Use Docker
3. Poor results? → Try preprocessing (see scripts/)
4. Still poor (especially captcha)? → Use commercial solution (see references/commercial-solutions.md)

## Common Tasks

### Debug Steps (Always Run First)

```bash
# 1. Verify image is valid
file your_image.png

# 2. Verify Docker is available
docker --version

# 3. Verify traineddata exists and is valid
ls -la /tmp/tessdata/
file /tmp/tessdata/eng.traineddata  # Should show "data" type
```

### Extract text from screenshot

```bash
docker run --rm \
  -v screenshot.png:/image.png:ro \
  -v /tmp/tessdata:/usr/share/tessdata:ro \
  minidocks/tesseract:latest tesseract /image.png stdout
```

### Recognize captcha (digits only)

See [references/captcha-guide.md](references/captcha-guide.md) for detailed captcha strategies.

### Chinese text recognition

```bash
mkdir -p /tmp/tessdata
wget -L -O /tmp/tessdata/chi_sim.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata

docker run --rm \
  -v image.png:/image.png:ro \
  -v /tmp/tessdata:/usr/share/tessdata:ro \
  minidocks/tesseract:latest tesseract /image.png stdout -l chi_sim
```

## Scripts

### Setup Tessdata Directory (One-time)

```bash
mkdir -p /tmp/tessdata
wget -L -O /tmp/tessdata/eng.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata
# Add more languages as needed:
# wget -L -O /tmp/tessdata/chi_sim.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata
```

### Preprocessing Pipeline

When OCR results are poor, use preprocessing:

```bash
# See scripts/preprocess.py for full preprocessing options
python3 scripts/preprocess.py --input captcha.png --output processed.png --method otsu
```

Available methods: `threshold`, `otsu`, `adaptive`, `morphology`

### Quick OCR Command

```bash
# Make sure tessdata is set up first (see above)
# Then use the wrapper script:
./scripts/ocr.sh image.png
```

## Parameters Reference

### PSM Modes

| PSM | Description | Best For |
|-----|-------------|----------|
| 3 | Fully automatic | Default |
| 6 | Assume single block | Captcha |
| 7 | Treat as single line | Single row |
| 8 | Treat as single word | Spaced chars |
| 10 | Character mode | Single char |

### White list

```bash
# Digits only
-c tessedit_char_whitelist=0123456789

# Letters only
-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz

# Alphanumeric
-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
```

## When to Use This Skill

- Extract text from screenshots
- Read captcha/verification codes
- Convert images to text
- Batch OCR processing
- Any image-to-text task
