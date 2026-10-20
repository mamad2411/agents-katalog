# Troubleshooting

| Gejala | Sebab | Aksi |
|---|---|---|
| `http=403` | WAF/bot-guard | coba wget UA beda → Playwright (browser asli). Gagal → catat, JANGAN bypass agresif |
| `http=429` | rate limit | `--sleep 5`, lanjutkan batch lain, retry maks 1x |
| timeout | file besar / server lambat | naikkan `--max-time`, atau `wget -c` (resume) manual |
| SSL error | cert kadaluarsa/server aneh | JANGAN `-k` diam-diam — tanya user dulu (risiko MITM) |
| redirect loop | cookie/session | Playwright (handle cookie otomatis) |
| `Content-Type: text/html` padahal mau file | link kedaluwarsa / butuh login | laporkan sebagai page, minta URL langsung |
| playwright ImportError | belum install | `pip install playwright && playwright install chromium` (sekali saja) |
| paywall/login/captcha | konten privat | BERHENTI. Hormati akses. Tawarkan alternatif publik |
