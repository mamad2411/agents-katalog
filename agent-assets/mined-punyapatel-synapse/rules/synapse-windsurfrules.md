# Synapse Skills — Windsurf / Codeium Rules
# Auto-generated. This file registers all 25 Synapse skills.

This project contains a polyglot (TypeScript + Python) skill SDK called **Synapse**.
Each skill is located in `skills/<name>/` and exposes both a JS (`index.js`) and Python (`main.py`) handler.

When the user asks for any of the following capabilities, invoke the matching skill handler.

## Calculator
Evaluates mathematical expressions and performs arithmetic operations.
- Handlers: `skills/calculator/index.js` (TS), `skills/calculator/main.py` (Python)
- Operations: `evaluate`
- Tags: math, arithmetic, calculate

## Json Transformer
Transforms, queries, flattens, diffs and validates JSON data using JSONPath, JSON Schema and deep operations.
- Handlers: `skills/json_transformer/index.js` (TS), `skills/json_transformer/main.py` (Python)
- Operations: `query`, `flatten`, `unflatten`, `diff`, `validate`
- Tags: json, transform, query, jsonpath

## Hash Generator
Generates cryptographic hashes (MD5, SHA-1, SHA-256, SHA-512) and UUIDs.
- Handlers: `skills/hash_generator/index.js` (TS), `skills/hash_generator/main.py` (Python)
- Operations: `hash`, `uuid`
- Tags: hash, crypto, uuid, checksum

## Datetime Utils
Parses, formats, converts timezones and calculates differences between dates.
- Handlers: `skills/datetime_utils/index.js` (TS), `skills/datetime_utils/main.py` (Python)
- Operations: `now`, `format`, `diff`, `convert_tz`
- Tags: date, time, timezone, format

## Regex Engine
Tests, matches, replaces and extracts text using regular expressions.
- Handlers: `skills/regex_engine/index.js` (TS), `skills/regex_engine/main.py` (Python)
- Operations: `test`, `match`, `replace`, `extract`
- Tags: regex, pattern, match, replace

## Web Scraper
Fetches web pages and extracts data using CSS selectors.
- Handlers: `skills/web_scraper/index.js` (TS), `skills/web_scraper/main.py` (Python)
- Operations: `scrape`
- Tags: web, scrape, html, extract

## Csv Excel Parser
Parses and generates CSV/Excel data from structured input.
- Handlers: `skills/csv_excel_parser/index.js` (TS), `skills/csv_excel_parser/main.py` (Python)
- Operations: `parse`, `generate`
- Tags: csv, excel, parse, spreadsheet

## Pdf Parser
Extracts text content from PDF files provided as base64 data.
- Handlers: `skills/pdf_parser/index.js` (TS), `skills/pdf_parser/main.py` (Python)
- Operations: `extract_text`
- Tags: pdf, extract, parse, text

## Markdown Converter
Converts between Markdown and HTML bidirectionally.
- Handlers: `skills/markdown_converter/index.js` (TS), `skills/markdown_converter/main.py` (Python)
- Operations: `md_to_html`, `html_to_md`
- Tags: markdown, html, convert

## Data Visualizer
Generates chart images (bar, line, pie, scatter) from structured data.
- Handlers: `skills/data_visualizer/index.js` (TS), `skills/data_visualizer/main.py` (Python)
- Operations: `generate_chart`
- Tags: chart, graph, visualize, data

## Http Client
Makes HTTP requests (GET, POST, PUT, DELETE, PATCH) with custom headers and payloads.
- Handlers: `skills/http_client/index.js` (TS), `skills/http_client/main.py` (Python)
- Operations: `request`
- Tags: http, request, api, rest

## Email Sender
Sends emails via SMTP with HTML body support.
- Handlers: `skills/email_sender/index.js` (TS), `skills/email_sender/main.py` (Python)
- Operations: `send`, `send_template`
- Tags: email, smtp, send, mail

## File Manager
Performs local file system operations: read, write, delete, list, and move files.
- Handlers: `skills/file_manager/index.js` (TS), `skills/file_manager/main.py` (Python)
- Operations: `read`, `write`, `delete`, `list`, `move`
- Tags: file, fs, read, write, manage

## Qr Code Generator
Generates QR code images from text and decodes QR codes from images.
- Handlers: `skills/qr_code_generator/index.js` (TS), `skills/qr_code_generator/main.py` (Python)
- Operations: `generate`, `decode`
- Tags: qr, barcode, generate, decode

## Image Processor
Performs image manipulation: resize, crop, rotate, and format conversion on base64 images.
- Handlers: `skills/image_processor/index.js` (TS), `skills/image_processor/main.py` (Python)
- Operations: `resize`, `crop`, `rotate`, `convert`
- Tags: image, resize, crop, rotate, process

## Sql Query
Executes parameterized SQL queries against PostgreSQL and MySQL databases.
- Handlers: `skills/sql_query/index.js` (TS), `skills/sql_query/main.py` (Python)
- Operations: `execute`
- Tags: sql, database, postgres, mysql, query

## Code Executor
Executes Python or JavaScript code snippets in a temporary sandbox with timeout protection.
- Handlers: `skills/code_executor/index.js` (TS), `skills/code_executor/main.py` (Python)
- Operations: `run_python`, `run_js`
- Tags: code, execute, sandbox, python, javascript

## Git Operations
Performs Git operations: clone, status, commit, push, and pull.
- Handlers: `skills/git_operations/index.js` (TS), `skills/git_operations/main.py` (Python)
- Operations: `clone`, `status`, `commit`, `push`, `pull`
- Tags: git, vcs, clone, commit, push

## Jwt Auth
Signs and verifies JSON Web Tokens using HMAC SHA256.
- Handlers: `skills/jwt_auth/index.js` (TS), `skills/jwt_auth/main.py` (Python)
- Operations: `sign`, `verify`
- Tags: jwt, auth, token, sign, verify

## Webhook Handler
Parses webhook payloads and validates HMAC signatures for services like Stripe and GitHub.
- Handlers: `skills/webhook_handler/index.js` (TS), `skills/webhook_handler/main.py` (Python)
- Operations: `parse`, `validate_signature`
- Tags: webhook, parse, validate, signature

## Seo Analyzer
Analyzes HTML for SEO best practices: title tags, meta descriptions, heading structure, alt text.
- Handlers: `skills/seo_analyzer/index.js` (TS), `skills/seo_analyzer/main.py` (Python)
- Operations: `analyze`
- Tags: seo, html, analyze, meta

## Accessibility Checker
Scans HTML for accessibility (a11y) issues: missing alt text, ARIA labels, form labels, lang attribute.
- Handlers: `skills/accessibility_checker/index.js` (TS), `skills/accessibility_checker/main.py` (Python)
- Operations: `analyze`
- Tags: accessibility, a11y, html, aria

## Performance Auditor
Audits HTML for frontend performance issues: blocking scripts, lazy loading, DOM size, inline styles.
- Handlers: `skills/performance_auditor/index.js` (TS), `skills/performance_auditor/main.py` (Python)
- Operations: `analyze`
- Tags: performance, audit, speed, optimization

## Color Palette Generator
Generates harmonious color palettes (analogous, monochromatic, triadic, complementary) from a base hex color.
- Handlers: `skills/color_palette_generator/index.js` (TS), `skills/color_palette_generator/main.py` (Python)
- Operations: `generate`
- Tags: color, palette, design, hex

## Screenshot Capture
Captures a screenshot of a web page URL via the Microlink API.
- Handlers: `skills/screenshot_capture/index.js` (TS), `skills/screenshot_capture/main.py` (Python)
- Operations: `capture`
- Tags: screenshot, capture, web, image
