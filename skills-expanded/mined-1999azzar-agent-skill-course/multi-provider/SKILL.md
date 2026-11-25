---
name: multi-provider
description: Contoh skill multi-provider search aggregator. Demonstrasi pattern untuk menggabungkan beberapa sumber data dengan fallback. Use when learning how to build aggregator skills with multiple providers.
---

# Multi-Provider Search (Contoh)

Skill ini mendemonstrasikan cara membangun aggregator yang query ke banyak provider sekaligus.

## Usage
```bash
# Search all providers
python3 scripts/search.py all "artificial intelligence"

# Search specific provider
python3 scripts/search.py wiki "machine learning"
python3 scripts/search.py news "cybersecurity"
```

## Providers
- `wiki`: Wikipedia OpenSearch API
- `news`: Google News RSS
- `all`: Semua provider sekaligus (concurrent)

## Architecture
See [references/architecture.md](references/architecture.md) for provider design patterns.
