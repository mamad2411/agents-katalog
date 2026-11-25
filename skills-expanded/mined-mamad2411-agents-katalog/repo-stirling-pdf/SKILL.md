---
name: repo-stirling-pdf
description: How to run and develop Stirling-PDF (Stirling-Tools/Stirling-PDF), the open-core self-hosted PDF platform with 50+ tools (merge, split, sign, redact, OCR, convert, compress), a REST API and no-code workflows. Use when a user needs private PDF processing, a PDF API, or wants to contribute to the repo.
---

# Stirling-PDF (`Stirling-Tools/Stirling-PDF`)

Licence: **open-core** (MIT for the core; `app/proprietary` and `app/saas` carry separate terms, see `LICENSE`). Cloned shallow at `/home/user/stirling-tools/stirling-pdf` (re-clone `git clone --depth 1 https://github.com/Stirling-Tools/Stirling-PDF`). The note saved the site as stirlingpdf.io.

## Run (self-host)
```bash
docker run -p 8080:8080 docker.stirlingpdf.com/stirlingtools/stirling-pdf
# open http://localhost:8080
```
Desktop client and Kubernetes options: https://docs.stirlingpdf.com. REST API docs are linked from the README; nearly every tool has an endpoint.

## Why use it
Documents never leave your machine, unlike free hosted converters (see `pdf-document-conversion-tools`). Use it for contracts, HR, medical and financial PDFs, and for automating batch jobs.

## Develop (from AGENTS.md / CLAUDE.md in the repo)
Uses Task as the command runner: `task install`, `task dev`, `task dev:all`, `task build`, `task test`, `task lint`, `task check` (lint + typecheck + test), `task docker:build`, `task docker:up`. Layout: `app/core`, `app/common`, `app/proprietary`, `app/saas`. Read `AGENTS.md`, `ADDING_TOOLS.md` and `CONTRIBUTING.md` before changing code; keep `task desc:` text generic.

## Related
`pdf`, `pdf-to-markdown`, `pdf-document-conversion-tools`, `docker-patterns`.
