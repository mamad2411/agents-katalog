# CLAUDE.md — nexus-mcp

## Codebase Exploration (ZORUNLU — KURAL)

**Bu projede `codebase-memory-mcp` tool'ları birincil codebase exploration aracıdır.**

### Kural

Her codebase exploration işleminde ÖNCE `search_graph` veya `get_architecture` kullan. Bu tercih değil, zorunluluktur.

### Sıralama

1. `search_graph` → sembol/fonksiyon/dosya bul
2. `get_code_snippet` → kodu oku
3. `trace_path` → çağrışım zincirini izle
4. `get_architecture` → yüksek seviye yapı
5. `find_references` → referansları bul

### Yasak (MCP varken)

- `grep`, `find`, `glob` ile kod keşfi
- `read` ile dosya dosya gezme
- `bash` ile kod arama

### Fallback

MCP 0 sonuç dönerse veya error verirse → grep/glob/read kullanılabilir.

### Indexed Projects

- `nexus-mcp-sniper` — sniper trading bot
- `nexus-mcp-backtest-sniper` — backtest engine

## Proje Yapısı

- `sniper/` — Ana trading bot (Python)
- `backtest-sniper/` — Backtest engine (Python)
- `sniper/memory-bank/` — Bug registry, chat history, active context
- `sniper/output/` — Paper trade logs, events, trades history

## Test Komutları

- Backtest: `cd backtest-sniper && python run.py`
- Tests: `cd sniper && python -m pytest tests/`
