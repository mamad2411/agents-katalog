# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Node.js (ESM) PDF processing pipeline that automates scanning, OCR barcode verification, compression, and upload of answer sheet PDFs.

## Commands

```bash
# Install dependencies
npm install

# Install Ghostscript (required external dependency)
node install-ghost-script.js

# Run the application (interactive CLI)
node index.js
```

There are no tests (`npm test` exits with error).

## External Dependency: Ghostscript

Ghostscript (`gs` on Mac/Linux, `gswin64c` on Windows) must be installed system-wide. It is invoked via `child_process.exec` for PDF compression. Without it, the compression step silently fails and falls back to the original file.

## Pipeline Architecture

The entire application lives in `index.js` as a single-file pipeline with three sequential stages, each powered by a `chokidar` file watcher and a `p-queue` for concurrency control:

```
SCANNED_FOLDER
    │
    ▼ scanWatcher() — watches for new folders or loose PDFs
    │  • Folders: waits for stability (file count stable for 4s), moves PDFs to LINEARIZED_FOLDER
    │  • Loose PDFs: waits 2s, generates PDF report, moves to LINEARIZED_FOLDER
    │
LINEARIZED_FOLDER
    │
    ▼ setupLinearizedWatcher() — OCR barcode verification
    │  • Sends each PDF to one of 4 round-robin OCR API workers
    │  • Barcode in API response must match filename (without extension)
    │  • Match → UPLOAD_FOLDER
    │  • Mismatch / error → ERROR_FOLDER
    │
UPLOAD_FOLDER
    │
    ▼ setupUploadWatcher() — compresses and uploads to system API
       • Compresses PDF in-memory via Ghostscript (temp file, then deleted)
       • POSTs to UPLOAD_API_URL (env var, defaults to pahsu.paperevaluation.com)
       • HTTP 400 → UPLOAD_ERROR/Already Uploaded/
       • HTTP 422 → UPLOAD_ERROR/Assessment Not Created/
       • API failedFiles list → UPLOAD_ERROR/<error-type>/
       • Success → SYSTEM_UPLOADED/
```

## Key Design Decisions

- **Concurrency**: Each watcher stage uses an independent `PQueue`. Concurrency for each queue (scan/linearized/upload, 1–5) is configured at startup via the interactive CLI.
- **OCR round-robin**: Four Cloudflare Worker endpoints (`osm-barcode-reader-worker[0-3].data-0e9.workers.dev`) are cycled via a module-level `currentIndex` counter.
- **Upload API URL**: Configurable via `UPLOAD_API_URL` environment variable (`.env` file). Defaults to `https://pahsu.paperevaluation.com/api/v1/assessment/answer-code-bulk`.
- **Logging**: Two parallel logs — `scan-log.txt` (plain text, append-only stream) and `scan-log.csv` (structured with Scanner/PC/Folder/File/Status/Action/Message columns). PDF metadata is separately logged to `pdf-report.csv`.
- **Startup prompt**: `promptForFolders()` collects scanner name, PC name, and all folder paths interactively before starting watchers. All folders are created if missing.

## Folder Reference

All folders default to `process.cwd()` subdirectories and are created automatically on startup:

| Folder | Purpose |
|---|---|
| `SCANNED_FOLDER` | Input: raw scans drop here |
| `LINEARIZED_FOLDER` | Intermediate: awaiting OCR check |
| `UPLOAD_FOLDER` | Intermediate: OCR passed, awaiting upload |
| `ERROR_FOLDER` | OCR mismatch/errors |
| `SYSTEM_UPLOADED` | Successfully uploaded |
| `UPLOAD_ERROR` | Upload failures (sub-folders by error type) |
| `COMPRESSED_FOLDER` | Legacy (not used in current pipeline) |
| `READY_TO_UPLOAD_FOLDER` | Legacy (not used in current pipeline) |
