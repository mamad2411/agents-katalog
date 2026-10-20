# Synapse Project — Cursor Rules

This project is **Synapse**, a polyglot (TypeScript + Python) AI skill SDK with 25 skills.

## Key Conventions

1. Each skill lives in `skills/<name>/` with dual handlers (JS + Python).
2. All skills export `async handler(params, context)`.
3. Params follow the JSON Schema in `<name>.skill.json`.
4. Python integration tests require `PYTHONPATH=src`.
5. Use `pnpm` for JS dependency management.

## Available Skills

- `calculator`: Evaluates mathematical expressions and performs arithmetic operations
- `json_transformer`: Transforms, queries, flattens, diffs and validates JSON data using JSONPath, JSON Schema and deep operations
- `hash_generator`: Generates cryptographic hashes (MD5, SHA-1, SHA-256, SHA-512) and UUIDs
- `datetime_utils`: Parses, formats, converts timezones and calculates differences between dates
- `regex_engine`: Tests, matches, replaces and extracts text using regular expressions
- `web_scraper`: Fetches web pages and extracts data using CSS selectors
- `csv_excel_parser`: Parses and generates CSV/Excel data from structured input
- `pdf_parser`: Extracts text content from PDF files provided as base64 data
- `markdown_converter`: Converts between Markdown and HTML bidirectionally
- `data_visualizer`: Generates chart images (bar, line, pie, scatter) from structured data
- `http_client`: Makes HTTP requests (GET, POST, PUT, DELETE, PATCH) with custom headers and payloads
- `email_sender`: Sends emails via SMTP with HTML body support
- `file_manager`: Performs local file system operations: read, write, delete, list, and move files
- `qr_code_generator`: Generates QR code images from text and decodes QR codes from images
- `image_processor`: Performs image manipulation: resize, crop, rotate, and format conversion on base64 images
- `sql_query`: Executes parameterized SQL queries against PostgreSQL and MySQL databases
- `code_executor`: Executes Python or JavaScript code snippets in a temporary sandbox with timeout protection
- `git_operations`: Performs Git operations: clone, status, commit, push, and pull
- `jwt_auth`: Signs and verifies JSON Web Tokens using HMAC SHA256
- `webhook_handler`: Parses webhook payloads and validates HMAC signatures for services like Stripe and GitHub
- `seo_analyzer`: Analyzes HTML for SEO best practices: title tags, meta descriptions, heading structure, alt text
- `accessibility_checker`: Scans HTML for accessibility (a11y) issues: missing alt text, ARIA labels, form labels, lang attribute
- `performance_auditor`: Audits HTML for frontend performance issues: blocking scripts, lazy loading, DOM size, inline styles
- `color_palette_generator`: Generates harmonious color palettes (analogous, monochromatic, triadic, complementary) from a base hex color
- `screenshot_capture`: Captures a screenshot of a web page URL via the Microlink API

## Skill-Specific Rules

See `.cursor/rules/` for detailed per-skill rules.
