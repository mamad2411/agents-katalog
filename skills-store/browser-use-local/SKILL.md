---
name: browser-use-local
description: WAJIB OTOMATIS dipakai tanpa slash saat user minta buka web, cek situs, ambil isi halaman JS-heavy, screenshot, atau otomasi browser. Playwright headless lokal, gratis tanpa API key. Trigger: buka web, cek situs, baca halaman, screenshot, browser, otomasi web.
version: 1.0.0
tags: [browser, playwright, gratis, headless]
---

# Browser Lokal (Playwright headless)

Buka halaman yang butuh JavaScript (SPA, dashboard, docs dinamis) tanpa API key.

## Pakai

```bash
python3 ~/.agents/skills-store/browser-use-local/scripts/browse.py "https://example.com"
```

Keluaran: `TITLE`, `URL` final (setelah redirect), dan isi halaman dalam teks.

## Kapan dipakai

- Halaman yang `curl`/webfetch hasilnya kosong karena render via JS
- Butuh teks setelah login-less interaksi (tab, "load more")
- Screenshot untuk referensi visual

## Alur kerja AI

1. Coba `webfetch` dulu (lebih murah). Gagal/kosong → skrip ini.
2. Jangan menebak isi halaman: tempel hasil atau bilang gagal.
3. Butuh screenshot/klik kompleks → pakai MCP playwright on-demand
   (`mamat-mcp on playwright` → pakai → `mamat-mcp off playwright`).

## Batasan

- Headless sering diblok Cloudflare → laporkan, jangan akali.
- Halaman butuh login: cookie tidak dibawa skrip ini.
- Butuh Chromium Playwright terpasang (`playwright install chromium`).
