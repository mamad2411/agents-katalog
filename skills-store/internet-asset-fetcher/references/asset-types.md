# Asset Types — URL/extension/Content-Type → handler

| Tipe | Ciri | Handler | Output |
|---|---|---|---|
| image | .jpg/.png/.webp/.svg/.gif/.avif + `image/*` | `fetch.py` (curl) | file asli |
| page | `text/html`, tanpa extension file | `page.py` (Playwright→curl) | .txt + .md + .html + .png |
| document | .pdf/.docx/.xlsx/.pptx/.csv | `fetch.py` (curl) | file asli → olah via skill `pdf`/`docx`/`xlsx` |
| text/data | .txt/.md/.json/.csv + `text/*` | `fetch.py` (curl) | file asli |
| audio/video file | .mp3/.mp4/.webm + `audio/* video/*` | `media.py` (curl+ffmpeg) | file + thumbnail |
| stream (yt/tiktok/ig/x) | domain sosmed | `media.py` → yt-dlp | file (butuh `brew install yt-dlp`) |

Deteksi berlapis: extension dulu → kalau kosong, HEAD `Content-Type` → kalau HTML, lempar ke `page.py`.
