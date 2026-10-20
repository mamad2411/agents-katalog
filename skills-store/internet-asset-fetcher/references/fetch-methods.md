# Fetch Methods — curl vs wget vs Playwright vs ffmpeg

- **curl** (default): file statis, redirect, retry 2x, timeout 120s. Cepat, cukup untuk 90% kasus.
- **wget**: fallback kalau curl diblokir header-nya (`wget -U` UA beda kadang lolos WAF sederhana).
- **Playwright** (`page.py`): halaman JS-rendered (SPA, infinite scroll, konten muncul setelah load).
  Butuh `pip install playwright && playwright install chromium`. Tanpa itu → fallback curl + strip-tags.
  Tunggu `networkidle` + 1.5s; screenshot full-page otomatis.
- **ffmpeg** (`media.py`): probe + thumbnail + kompres media. `ffmpeg -i in -vframes 1 thumb.jpg`.
- **yt-dlp**: stream sosmed. Bukan bawaan — `brew install yt-dlp`.

Urutan fallback otomatis di skill: curl → wget → playwright (page) → lapor gagal ke manifest.
Jangan retry >2x per metode; hormati 429 (tunggu, jangan spam).
