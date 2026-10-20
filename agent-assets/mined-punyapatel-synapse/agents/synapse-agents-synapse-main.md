# Synapse Skills — Agent Instructions

> Auto-generated index of all 25 Synapse skills.
> Each skill has both a TypeScript (`index.js`) and Python (`main.py`) handler.

This project is a polyglot skill SDK. Each skill in `skills/<name>/` can be invoked
by calling its `handler(params, context)` function. Refer to the individual skill
schema (`<name>.skill.json`) for parameter shapes.

## Skill Index

| # | Skill | Category | Operations | Tags |
|---|-------|----------|-----------|------|
| 1 | [Calculator](skills/calculator/) | utility | `evaluate` | math, arithmetic, calculate |
| 2 | [Json Transformer](skills/json_transformer/) | utility | `query`, `flatten`, `unflatten`, `diff`, `validate` | json, transform, query, jsonpath |
| 3 | [Hash Generator](skills/hash_generator/) | utility | `hash`, `uuid` | hash, crypto, uuid, checksum |
| 4 | [Datetime Utils](skills/datetime_utils/) | utility | `now`, `format`, `diff`, `convert_tz` | date, time, timezone, format |
| 5 | [Regex Engine](skills/regex_engine/) | utility | `test`, `match`, `replace`, `extract` | regex, pattern, match, replace |
| 6 | [Web Scraper](skills/web_scraper/) | data | `scrape` | web, scrape, html, extract |
| 7 | [Csv Excel Parser](skills/csv_excel_parser/) | data | `parse`, `generate` | csv, excel, parse, spreadsheet |
| 8 | [Pdf Parser](skills/pdf_parser/) | data | `extract_text` | pdf, extract, parse, text |
| 9 | [Markdown Converter](skills/markdown_converter/) | data | `md_to_html`, `html_to_md` | markdown, html, convert |
| 10 | [Data Visualizer](skills/data_visualizer/) | data | `generate_chart` | chart, graph, visualize, data |
| 11 | [Http Client](skills/http_client/) | integration | `request` | http, request, api, rest |
| 12 | [Email Sender](skills/email_sender/) | integration | `send`, `send_template` | email, smtp, send, mail |
| 13 | [File Manager](skills/file_manager/) | integration | `read`, `write`, `delete`, `list`, `move` | file, fs, read, write, manage |
| 14 | [Qr Code Generator](skills/qr_code_generator/) | integration | `generate`, `decode` | qr, barcode, generate, decode |
| 15 | [Image Processor](skills/image_processor/) | integration | `resize`, `crop`, `rotate`, `convert` | image, resize, crop, rotate, process |
| 16 | [Sql Query](skills/sql_query/) | infrastructure | `execute` | sql, database, postgres, mysql, query |
| 17 | [Code Executor](skills/code_executor/) | infrastructure | `run_python`, `run_js` | code, execute, sandbox, python, javascript |
| 18 | [Git Operations](skills/git_operations/) | infrastructure | `clone`, `status`, `commit`, `push`, `pull` | git, vcs, clone, commit, push |
| 19 | [Jwt Auth](skills/jwt_auth/) | infrastructure | `sign`, `verify` | jwt, auth, token, sign, verify |
| 20 | [Webhook Handler](skills/webhook_handler/) | infrastructure | `parse`, `validate_signature` | webhook, parse, validate, signature |
| 21 | [Seo Analyzer](skills/seo_analyzer/) | frontend | `analyze` | seo, html, analyze, meta |
| 22 | [Accessibility Checker](skills/accessibility_checker/) | frontend | `analyze` | accessibility, a11y, html, aria |
| 23 | [Performance Auditor](skills/performance_auditor/) | frontend | `analyze` | performance, audit, speed, optimization |
| 24 | [Color Palette Generator](skills/color_palette_generator/) | frontend | `generate` | color, palette, design, hex |
| 25 | [Screenshot Capture](skills/screenshot_capture/) | frontend | `capture` | screenshot, capture, web, image |

## How to Invoke a Skill

### TypeScript
```js
import { handler } from './skills/<skill_name>/index.js';
const result = await handler(params, context);
```

### Python
```python
from skills.<skill_name>.main import handler
result = await handler(params, context)
```

## Detailed Skill Instructions

See individual files in `codex-instructions/` for per-skill details.
