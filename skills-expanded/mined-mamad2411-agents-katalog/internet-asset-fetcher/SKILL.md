---
name: internet-asset-fetcher
description: Fetch any internet asset to local files — images, text/articles, documents (PDF/DOCX/XLSX/PPTX), audio/video, web pages. Use when user says download image, ambil gambar, save article, unduh dokumen, scrape page, archive URL. Internet-capable via curl/wget/Playwright, saves to ./assets with manifest.
license: MIT
---

# Internet Asset Fetcher

Download ANY public internet asset to local disk with provenance. One skill for image + text + document + media.

## When to Use

- User: "download gambar ini", "fetch image", "save this photo"
- User: "ambil artikel/teks dari URL", "archive page", "scrape this"
- User: "unduh PDF/dokumen", "download file dari link"
- User: "download video/audio" (via ffmpeg)
- Any task needing offline copy of online content

## Quick Start

```bash
# image
python3 scripts/fetch.py --url "https://example.com/photo.jpg" --out ./assets
# web page → markdown + screenshot (needs Playwright, fallback curl)
python3 scripts/fetch.py --url "https://example.com/article" --page --out ./assets
# document
python3 scripts/fetch.py --url "https://example.com/file.pdf" --out ./assets
# batch from list
python3 scripts/fetch.py --list urls.txt --out ./assets
```

Output: `./assets/<slug>.<ext>` + `./assets/manifest.json`
(sumber URL, waktu UTC, sha256, ukuran, tipe).

## Workflow

1. **Kenali tipe** dari URL/extension/`Content-Type` → baca `references/asset-types.md`.
2. **Pilih metode**: file langsung → curl; halaman JS-berat → Playwright; media stream → ffmpeg. Detail di `references/fetch-methods.md`.
3. **Fetch** via `scripts/fetch.py` (jangan tulis ulang curl manual).
4. **Verifikasi**: file ada, ukuran >0, tipe benar (`file` command), image bisa dibuka, PDF punya halaman.
5. **Catat** ke `manifest.json` (otomatis oleh script).
6. **Lapor**: path file + ukuran + sumber URL. JANGAN dump base64 ke chat.

## Rules

- Hormati `robots.txt` + ToS situs. Jangan bypass paywall/login/captcha.
- Rate-limit: jeda 1 detik antar request batch (`--sleep 1`, default ON).
- User-Agent jujur: `internet-asset-fetcher/1.0 (AI-agent; contact: local)`.
- Simpan ke `./assets` relatif project — JANGAN ke /tmp (hilang) atau home random.
- Gambar >5MB → tawarkan kompres (lihat `references/compress.md`).
- Gagal (403/429/timeout) → coba fallback chain: curl → wget → playwright. Tulis error ke manifest, jangan ngarang isi file.

## Scripts

| Script | Fungsi |
|---|---|
| `scripts/fetch.py` | entry utama: auto-deteksi tipe, download, manifest |
| `scripts/page.py` | halaman web → markdown + teks + screenshot (Playwright, fallback readability-curl) |
| `scripts/browse.py` | **browsing interaktif**: open/shot/text/click/fill/scroll/wait/eval (lihat `references/browsing.md`) |
| `scripts/media.py` | audio/video via ffmpeg, thumbnail otomatis |

## References

- `references/asset-types.md` — mapping extension/Content-Type → handler
- `references/fetch-methods.md` — curl vs wget vs Playwright vs ffmpeg, kapan pakai apa
- `references/browsing.md` — **AI browsing interaktif** (klik/isi/scroll kayak manusia)
- `references/mcp-internet.md` — **MCP internet** (fetch/playwright/brave on-demand, kapan pakai apa)
- `references/compress.md` — kompres image/video (ffmpeg/PIL)
- `references/troubleshooting.md` — 403/429/timeout/SSL/redirect loop

## Related

- `web-search` (cari URL) → `internet-asset-fetcher` (unduh isinya) → `pdf`/`docx`/`xlsx` (olah isinya)
- `image-generation` (bikin gambar baru) vs skill ini (ambil gambar yang sudah ada)
- `video-downloader` (khusus video) vs skill ini (semua tipe)
