---
name: api-wrapper
description: Contoh skill wrapper untuk REST API (JSONPlaceholder). Demonstrasi pattern standar untuk membungkus API eksternal menjadi skill yang reusable. Use when learning how to create API wrapper skills.
---

# API Wrapper (Contoh)

Skill ini mendemonstrasikan cara membungkus REST API menjadi skill OpenClaw.

## Usage
```bash
# List posts
python3 scripts/api.py list --limit 5

# Get single post
python3 scripts/api.py get 1

# Search posts
python3 scripts/api.py search "dolor"
```

## Environment Variables
| Variable | Required | Description |
| :--- | :---: | :--- |
| `API_BASE_URL` | No | Override base URL (default: jsonplaceholder.typicode.com) |

## API Reference
See [references/endpoints.md](references/endpoints.md) for full endpoint documentation.
