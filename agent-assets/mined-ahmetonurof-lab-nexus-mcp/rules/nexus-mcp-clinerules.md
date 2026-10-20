# Codebase Exploration Rules — ZORUNLU

## codebase-memory-mcp Kullanımı (Birincil)

**Bu projede `codebase-memory-mcp` tool'ları birincil codebase exploration aracıdır.**

### Sıralama (kesin)

1. `search_graph` → sembol/fonksiyon/dosya bul
2. `get_code_snippet` → kodu oku
3. `trace_path` → çağrışım zincirini izle
4. `get_architecture` → yüksek seviye yapı
5. `find_references` → referansları bul

**Eğer MCP 0 sonuç dönerse veya error verirse** → fallback olarak grep/glob/read kullan.

### Yasak

- Dosya bulmak için `grep` kullanma (MCP varken)
- Kod okumak için `read` ile dosya açma (MCP varken)
- Çağrı zincirini bulmak için `grep -r` kullanma

### İzin

- String literal, error message, config değeri → grep OK
- Non-code dosyalar (Dockerfile, shell script, .env) → grep OK
- Runtime log, build output → grep OK
- Dosya içeriği okuma (MCP sonrası doğrulama) → read OK

### Indexed Projects

- `nexus-mcp-sniper` (2307 node, 9714 edge)
- `nexus-mcp-backtest-sniper` (2653 node, 8312 edge)
