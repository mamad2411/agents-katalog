# Synapse Project Instructions for Claude Code

This project is **Synapse**, a polyglot (TypeScript + Python) AI skill SDK.

## Project Structure

- `skills/<name>/` — Individual skills with dual JS/Python handlers
- `packages/sdk-ts/` — TypeScript SDK
- `packages/sdk-python/` — Python SDK

## Available Skills (25 total)

- **Calculator** (`/calculator`): Evaluates mathematical expressions and performs arithmetic operations
- **Json Transformer** (`/json_transformer`): Transforms, queries, flattens, diffs and validates JSON data using JSONPath, JSON Schema and deep operations
- **Hash Generator** (`/hash_generator`): Generates cryptographic hashes (MD5, SHA-1, SHA-256, SHA-512) and UUIDs
- **Datetime Utils** (`/datetime_utils`): Parses, formats, converts timezones and calculates differences between dates
- **Regex Engine** (`/regex_engine`): Tests, matches, replaces and extracts text using regular expressions
- **Web Scraper** (`/web_scraper`): Fetches web pages and extracts data using CSS selectors
- **Csv Excel Parser** (`/csv_excel_parser`): Parses and generates CSV/Excel data from structured input
- **Pdf Parser** (`/pdf_parser`): Extracts text content from PDF files provided as base64 data
- **Markdown Converter** (`/markdown_converter`): Converts between Markdown and HTML bidirectionally
- **Data Visualizer** (`/data_visualizer`): Generates chart images (bar, line, pie, scatter) from structured data
- **Http Client** (`/http_client`): Makes HTTP requests (GET, POST, PUT, DELETE, PATCH) with custom headers and payloads
- **Email Sender** (`/email_sender`): Sends emails via SMTP with HTML body support
- **File Manager** (`/file_manager`): Performs local file system operations: read, write, delete, list, and move files
- **Qr Code Generator** (`/qr_code_generator`): Generates QR code images from text and decodes QR codes from images
- **Image Processor** (`/image_processor`): Performs image manipulation: resize, crop, rotate, and format conversion on base64 images
- **Sql Query** (`/sql_query`): Executes parameterized SQL queries against PostgreSQL and MySQL databases
- **Code Executor** (`/code_executor`): Executes Python or JavaScript code snippets in a temporary sandbox with timeout protection
- **Git Operations** (`/git_operations`): Performs Git operations: clone, status, commit, push, and pull
- **Jwt Auth** (`/jwt_auth`): Signs and verifies JSON Web Tokens using HMAC SHA256
- **Webhook Handler** (`/webhook_handler`): Parses webhook payloads and validates HMAC signatures for services like Stripe and GitHub
- **Seo Analyzer** (`/seo_analyzer`): Analyzes HTML for SEO best practices: title tags, meta descriptions, heading structure, alt text
- **Accessibility Checker** (`/accessibility_checker`): Scans HTML for accessibility (a11y) issues: missing alt text, ARIA labels, form labels, lang attribute
- **Performance Auditor** (`/performance_auditor`): Audits HTML for frontend performance issues: blocking scripts, lazy loading, DOM size, inline styles
- **Color Palette Generator** (`/color_palette_generator`): Generates harmonious color palettes (analogous, monochromatic, triadic, complementary) from a base hex color
- **Screenshot Capture** (`/screenshot_capture`): Captures a screenshot of a web page URL via the Microlink API

## Invoking Skills

Each skill directory contains:
- `<name>.skill.json` — JSON Schema definition
- `index.js` — TypeScript handler
- `main.py` — Python handler
- `package.json` — JS dependencies
- `requirements.txt` — Python dependencies

Use the custom commands in `.claude/commands/` to invoke any skill by name.

## Testing

- TypeScript: `cd packages/sdk-ts && npx vitest run`
- Python: `cd packages/sdk-python && PYTHONPATH=src pytest`
