# 14 — Performa, beban, dan skalabilitas

## 1. Jenis uji beban (pilih sesuai risiko)
| Jenis | Pertanyaan | Bentuk beban |
|---|---|---|
| Smoke load | bisa menangani trafik normal? | 1–5 VU, 1 menit |
| Load | sesuai kapasitas rencana? | puncak harian ×1.5, 10–30 menit |
| Stress | di mana titik patahnya? | naik bertahap sampai error/latensi meledak |
| Soak | bocor memori/koneksi? | beban normal 2–8 jam |
| Spike | tahan lonjakan mendadak? | 10× dalam 10 detik |
| Scalability | tambah instance membantu? | 1 vs 2 vs 4 replika, bandingkan RPS |
| Breakpoint | batas keras | ramp sampai 5xx > 1% |

## 2. Anggaran (tulis di README, uji otomatis)
| Metrik | Anggaran awal |
|---|---|
| p95 API baca | ≤ 200 ms |
| p95 API tulis | ≤ 400 ms |
| p99 | ≤ 2× p95 |
| Error rate | < 0.1% (5xx) |
| LCP / INP / CLS | ≤ 2.5 s / ≤ 200 ms / ≤ 0.1 |
| Throughput | ≥ target bisnis (mis. 300 RPS) |
| Memori | stabil (tidak naik >10% per jam saat soak) |

## 3. k6 (sudah terpasang)
```js
// load.js
import http from "k6/http"
import { check, sleep } from "k6"
export const options = {
  scenarios: {
    load:    { executor: "ramping-vus", startVUs: 0, stages: [
      { duration: "1m", target: 50 }, { duration: "5m", target: 50 }, { duration: "30s", target: 0 }] },
    spike:   { executor: "constant-vus", vus: 100, duration: "20s", startTime: "7m" },
  },
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<200", "p(99)<500"],
  },
}
export default function () {
  const r = http.get(`${__ENV.BASE_URL}/api/items?limit=20`)
  check(r, { "status 200": (x) => x.status === 200, "ada item": (x) => x.json("items").length > 0 })
  sleep(1)
}
```
```bash
k6 run load.js -e BASE_URL=http://localhost:3000
k6 run --out json=hasil.json load.js && jq '.metrics.http_req_duration' hasil.json
ab -n 1000 -c 50 http://localhost:3000/health        # baseline cepat
```

## 4. Frontend (Core Web Vitals)
```bash
npx --yes lighthouse http://localhost:3000 --preset=desktop --output=json --output-path=lh.json \
  --chrome-flags="--headless"
jq '.categories.performance.score, .audits["largest-contentful-paint"].numericValue' lh.json
dref <url>      # LCP/CLS nyata + screenshot
```
Periksa: ukuran bundle (< 200 KB gzip awal), jumlah request, gambar (format modern + ukuran),
font (preload, `font-display`), render-blocking, hidrasi, hydration mismatch, long task > 50 ms.

## 5. Database & backend
- `EXPLAIN (ANALYZE, BUFFERS)` untuk setiap query baru; tolak `Seq Scan` pada tabel besar.
- Indeks: ada untuk kolom filter/join/sort; cek indeks tak terpakai (`pg_stat_user_indexes`).
- N+1: hitung query per request (target < 5 untuk endpoint list).
- Connection pool: uji 2× pool size, tidak boleh habis/timeout.
- Cache: hit ratio, TTL benar, invalidasi setelah update, stampede saat cache dingin.
- Antrean: throughput consumer, retry, dead-letter, idempoten.
- Batas: request 1000 paralel → 429 (bukan 5xx, bukan mati).

## 6. Profil sebelum optimasi (jangan menebak)
```bash
python3 -m cProfile -o out.prof app.py && python3 -m pstats out.prof   # python
node --cpu-prof --cpu-prof-dir=prof server.js                           # node
go tool pprof -http=:8080 http://localhost:6060/debug/pprof/profile     # go
```
Tulis 3 temuan teratas + dampak terukur (ms/RAM) di laporan. Optimasi tanpa angka = spekulasi.

## 7. Observability saat uji beban
Pantau bersamaan: CPU/RAM/disk/net, p95/p99 latensi, error rate, queue depth, DB
slow query, koneksi pool, GC pause. Uji beban tanpa metrik server = tidak ada kesimpulan.

## 8. Definition of Done performa
- [ ] Script beban ada di repo dan bisa dijalankan siapa pun (1 perintah).
- [ ] Threshold di kode (`k6 thresholds`) → CI gagal bila lambat.
- [ ] Angka p95/p99, error rate, RPS tercatat di laporan + tanggal + spesifikasi mesin.
- [ ] Ada rekomendasi konkret (indeks, cache, pagination, async) dengan perkiraan dampak.
