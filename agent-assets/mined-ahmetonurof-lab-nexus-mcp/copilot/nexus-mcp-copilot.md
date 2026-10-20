# Copilot Instructions — nexus-mcp

## Codebase Exploration (ZORUNLU)

**Bu projede `codebase-memory-mcp` tool'ları birincil codebase exploration aracıdır.**

### Kural

Her codebase exploration işleminde ÖNCE `search_graph` veya `get_architecture` kullan. Bu tercih değil, zorunluluktur.

### Sıralama

1. `search_graph` → sembol/fonksiyon/dosya bul
2. `get_code_snippet` → kodu oku
3. `trace_path` → çağrışım zincirini izle
4. `get_architecture` → yüksek seviye yapı

### Yasak (MCP varken)

- `grep`, `find`, `glob` ile kod keşfi
- `read` ile dosya dosya gezme

### Fallback

MCP 0 sonuç dönerse veya error verirse → grep/glob/read kullanılabilir.

### Indexed Projects

- `nexus-mcp-sniper` — sniper trading bot
- `nexus-mcp-backtest-sniper` — backtest engine
