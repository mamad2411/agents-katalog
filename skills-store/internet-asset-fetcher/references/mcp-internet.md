# MCP Internet — AI akses web lewat MCP (bukan cuma script)

Script `fetch/page/browse` = sekali jalan. MCP = AI pakai tools web kapan saja
dalam sesi. Keduanya saling melengkapi.

## MCP yang tersedia

| MCP | Fungsi | Status |
|---|---|---|
| `fetch` (parked) | ambil URL → markdown (model-controlled) | on-demand: `python3 ~/.agents/mcp-lifecycle.py --on fetch` |
| `playwright` (parked) | browser penuh: navigate/screenshot/click/fill | on-demand, sama |
| `brave-search` (parked) | search web via API (butuh key) | butuh `BRAVE_API_KEY` |
| skill `web-search` | strategi query (bukan eksekusi) | core ✅ |
| skill `internet-asset-fetcher` | download + browsing via script | core ✅ |

## Kapan pakai apa

- Butuh 1 file/halaman → `scripts/fetch.py` / `page.py` (cepat, tanpa MCP overhead).
- Butuh eksplorasi multi-langkah (klik, form, scroll, bandingkan halaman) → MCP `playwright` ATAU `scripts/browse.py` bertahap.
- Butuh search berkala / banyak query → MCP `fetch` + skill `web-search` buat strategi.
- Semua butuh bukti visual → screenshot (`browse.py shot` / MCP screenshot), JANGAN klaim tanpa bukti.

## Menyalakan (hemat: matikan lagi setelah selesai)

```bash
python3 ~/.agents/mcp-lifecycle.py --on fetch        # 1 sesi scrape
python3 ~/.agents/mcp-lifecycle.py --off fetch       # selesai → mati (hemat RAM)
```

JANGAN nyalakan semua MCP internet sekaligus — satu per tugas.
