---
name: marker-pdf-ocr
description: Convert PDF to Markdown using Marker OCR (local-first, cloud fallback)
user-invocable: true
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["MARKER_API_KEY"],
        "bins": ["python3"],
        "minRamMb": 512
      },
      "primaryEnv": "MARKER_API_KEY",
      "install": [
        {
          "id": "pip-marker",
          "kind": "exec",
          "label": "Install marker-pdf package",
          "command": "pip install marker-pdf torch --extra-index-url https://download.pytorch.org/whl/cpu"
        }
      ],
      "suggestedEnv": {
        "MARKER_DEPLOYMENT_MODE": "auto",
        "MARKER_MAX_MEMORY_MB": "4096"
      }
    }
  }
---

# Marker PDF OCR

Convert PDF documents to Markdown with high accuracy using Marker OCR engine.

## Usage

### Convert a PDF file
```bash
# Auto mode (tries local first, falls back to cloud)
marker-ocr convert /path/to/document.pdf

# Force local mode
marker-ocr convert /path/to/document.pdf --mode local

# Force cloud mode
marker-ocr convert /path/to/document.pdf --mode cloud

# With specific output format
marker-ocr convert /path/to/document.pdf --format json
```

### Check system health
```bash
marker-ocr health-check
```

### Batch processing
```bash
for f in *.pdf; do marker-ocr convert "$f"; done
```

## Deployment Modes

| Mode | Description | RAM | Network | Privacy |
|------|-------------|-----|---------|---------|
| **local** (default) | Process on-premise with CPU | 4GB | No | ✅ High |
| **cloud** | Use Datalab.to API | 512MB | Yes | ⚠️ Data leaves |
| **auto** | Try local first, fallback to cloud | 4GB | Optional | ✅ Best effort |

### Mode Selection Logic (Auto)
1. Check if marker-pdf is installed locally
2. Check available memory (need 4GB free)
3. If local available → use local
4. If local fails or OOM → fallback to cloud
5. If cloud API key not set → error

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MARKER_API_KEY` | For cloud mode | - | API key from datalab.to |
| `MARKER_DEPLOYMENT_MODE` | No | `auto` | Force mode: local/cloud/auto |
| `MARKER_MAX_MEMORY_MB` | No | `4096` | Memory limit for local mode |
| `MARKER_TIMEOUT_SECONDS` | No | `300` | Processing timeout |

## Installation

### Option 1: Local Mode (Recommended)
```bash
# Install marker-pdf (CPU-only version)
pip install marker-pdf torch --extra-index-url https://download.pytorch.org/whl/cpu

# Verify installation
marker-ocr health-check
```

### Option 2: Cloud Mode (Minimal Setup)
```bash
# Just set API key, no local dependencies
export MARKER_API_KEY="your-api-key"
```

### Option 3: Via OpenClaw Install
```bash
openclaw skill install marker-pdf-ocr
```

## Requirements

- **OS**: Linux, macOS, Windows (WSL2)
- **Python**: >= 3.8
- **RAM**: 
  - Local mode: 4GB (with 23GB swap configured)
  - Cloud mode: 512MB
- **Disk**: 5GB for local mode (models + cache)

## Output Formats

- `markdown` (default): Clean Markdown text
- `json`: Structured JSON with metadata
- `html`: HTML representation

## Examples

### Process scientific paper
```bash
marker-ocr convert paper.pdf --mode local --format markdown
```

### Batch convert with progress
```bash
for pdf in *.pdf; do
  echo "Processing: $pdf"
  marker-ocr convert "$pdf" --mode auto || echo "Failed: $pdf"
done
```

### Check what mode will be used
```bash
marker-ocr health-check --verbose
```

## Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `OOMError` | Local mode ran out of memory | Use `--mode cloud` or increase swap |
| `APIQuotaExceeded` | Cloud API limit reached | Wait and retry, or use local mode |
| `FileTooLarge` | PDF exceeds size limit | Split PDF or use cloud mode |
| `MarkerNotInstalled` | Local dependencies missing | Run `pip install marker-pdf` |

## Architecture

```
┌─────────────────┐
│   OpenClaw      │
│   Agent         │
└────────┬────────┘
         │ exec
         ▼
┌─────────────────┐
│   marker-ocr    │
│   CLI           │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐  ┌──────────┐
│ Local │  │ Cloud    │
│ (CPU) │  │ (API)    │
└───────┘  └──────────┘
```

## Troubleshooting

### Local mode is slow
- Expected: CPU processing is ~3-5x slower than GPU
- For faster processing: Use cloud mode or provision GPU

### Cloud mode costs
- Estimated: $0.001-0.01 per page
- For cost control: Use local mode for bulk processing

### Memory issues
- Ensure swap is configured: `free -h` should show >20GB swap
- Set `MARKER_MAX_MEMORY_MB` to limit memory usage
- Use `--mode cloud` for large documents

## References

- Marker GitHub: https://github.com/VikParuchuri/marker
- Datalab API: https://www.datalab.to/
- OpenClaw Skills: https://docs.openclaw.ai/tools/skills
