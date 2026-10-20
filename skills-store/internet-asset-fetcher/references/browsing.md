# AI Browsing — Playwright interaktif via `scripts/browse.py`

AI bisa BUKA + LIHAT + KLIK web kayak manusia, bukan cuma download.

```bash
B=scripts/browse.py
python3 $B open --url "https://example.com"              # judul + URL final
python3 $B shot --url "https://.../dashboard" --file ./assets/dash.png
python3 $B text --url "https://.../artikel"              # teks + preview 800 char
python3 $B click --url "https://.../list" --sel "button.next"
python3 $B fill --url "https://.../search" --sel "input[name=q]" --value "kopi"
python3 $B scroll --url "https://.../feed" --value 5     # infinite scroll 5x
python3 $B wait --url "https://.../app" --sel "#loaded"  # tunggu elemen muncul
python3 $B eval --url "https://..." --value "document.querySelectorAll('a').length"
```

Aturan AI browsing:
- headless default. Jangan isi kredensial tanpa izin user eksplisit.
- Tiap aksi → screenshot bukti (`shot`) sebelum klaim "berhasil".
- Hormati ToS/robots; kalau diblokir bot-guard → berhenti, laporkan.
- Output teks panjang → file, chat cuma preview 800 char.
