---
name: unienv
description: Use for any document, spreadsheet, presentation, PDF, OCR, image or data task outside a project (docx, xlsx, pptx, pdf, csv, parquet, png). Lists the tools already installed on this machine and exactly how to call them, so nothing needs to be installed or put in a temporary virtualenv.
---

# UniEnv AI: preinstalled tools on this machine

Everything below is already installed and shared by every AI tool on this machine. Do not create a virtualenv or `pip install` anything for these tasks.

- Python: `{{BIN}}/ue-py` (Python 3.12 with all packages below)
- Node.js: `{{BIN}}/ue-node` (preinstalled packages resolvable with `require`)
- Installed batteries: {{BATTERIES}}

## How to do common tasks

{{NOTES}}

## When something is missing

- Python package: `{{BIN}}/unienv need <package>`
- Node package: `{{BIN}}/unienv need --node <package>`
- System tool: `{{BIN}}/unienv need --bin <homebrew-formula>` (or `--cask` for apps)

These install permanently, update `{{HOME_DIR}}/manifest.json`, and make the tool available to every AI tool on this machine. If a tool fails, run `{{BIN}}/unienv doctor --json` and follow its `fix` hints.

## Python packages installed

{{PY_PACKAGES}}
