# Tool terpasang (bisa dipanggil semua AI lewat PATH)
total: 3
- **github-mcp-server** ← `github/github-mcp-server` (go) · perintah: `github-mcp-server`
- **sk** ← `jerbouma/financetoolkit` (uv) · perintah: `sk`
- **playwright-mcp** ← `microsoft/playwright-mcp` (npm) · perintah: `playwright-mcp`

## Tool komunitas tambahan (install 2026-11-24)

| Tool | Sumber | Fungsi |
|---|---|---|
| `officecli` | officecli/officecli (npm) | Generate PPTX/DOCX/XLSX/gambar dari prompt NL (100 kredit hosted gratis; External Mode = LLM sendiri) |
| `kinetograph` | 0xs4n4tg/kinetograph (npm) | Video engine programatik browserless (Remotion-shaped TS → render GPU Skia/Metal); `doctor`, `init`, ada skill+built-in MCP opsional |
| `mmdr` | 1jehuang/mermaid-rs-renderer (cargo) | Render diagram Mermaid → PNG/SVG, Rust native, tanpa browser |
| `dataproofer` | dataproofer/dataproofer (npm) | Proofreader data CSV/Excel (test inti/info/statistik/geo, JSON output — cocok CI) |
| `financetoolkit-mcp` | jerbouma/financetoolkit (uv, [mcp]) | MCP server analisis keuangan (harga, portofolio, fundamental) — terdaftar di opencode `enabled:false`, nyalakan `pow mcp on financetoolkit` |
| `abogen` (+cli/pyqt/web) | denizsafak/abogen (uv py3.12) | EPUB/PDF/teks → audiobook dengan TTS lokal (Kokoro/supertonic), sinkron caption |

Skill terkait ikut ter-ingest: `obsidian-skills-*` (resmi Obsidian: CLI, headless, Bases, JSON Canvas), `kinetograph` skills, finance skills (`finance-ai-tools`, `day-trader-skill`, dll dari repo-refs).
