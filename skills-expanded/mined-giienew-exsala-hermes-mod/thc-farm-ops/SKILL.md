---
name: thc-farm-ops
description: Use when farming Token Harbor keys (thkh/9router).
version: 1.0.0
author: Me
license: MIT
metadata:
  tags: [farming, tokenharbor, proxy, 9router, tempmail]
  related_skills: [dahl-key-farming]
---
# TokenHarbor Farm Ops (thc)

## When to Use
Gunakan saat: farming key tokenharbor (`thk_live_`) bulk, cek state tmux `thc`, scan proxy, atau pump ke 9router.

Farming `thk_live_` API keys dari Token Harbor (tokenharbor.ai) bulk, pake repo `tokenharbor-farm`. Jalan ala dahl.js (rotate proxy + autopump 9router). tmux session `thc`.

**Lokasi repo berubah WEB-LOCATION: ~/app/cache/scratch/ itu VOLATILE — idle 24h di-prune.** Repo farm durable ada di `~/app/farms/thc/` (thc.js, git-tracked di repo farming). SEBELUM klaim bisa run: cek keberadaan `index.mjs`/`run5.mjs` di lokasi yang disebut — kalau scratch/thc hilang, jangan langsung rebuild dari nol; cek dulu `~/app/farms/thc/` + backup git (`cd ~/app && git log --oneline --all | grep -i thc`), baru clone ulang repo `tokenharbor-farm` ke scratch kalau perlu.

## Cek state
```bash
tmux capture-pane -pt thc | grep -v '^$' | tail -14
python3 ~/app/cache/scratch/chk_9r.py   # cek row tokenharbor di DB 9router
```

## Jalankan farm
```bash
cd ~/app/cache/scratch/thc && TH_N=20 node thc_farm.mjs
```
Re-run per-akun (satu CLI call):
```bash
node src/index.mjs -n 1 --retries 4 -o output/x.json --inbox-provider exsala --mail-api-key gionova14 --proxy "http://<proxy>"
```

### Batch runner tanpa pump — `run5.mjs`
Satu file `~/app/cache/scratch/thc/run5.mjs`: sequential (bukan multi-process), tiap akun random proxy dari `good_jio_pw.txt` (pool TANPA skema — wrapper nambah `http://` sendiri), `--retries 3`, `--inbox-provider me` (worker `tempmail.YOUR_ACCOUNT.workers.dev`), output per-akun `output/run5_<ts>.json`. NO auto-pump → aman kirim ke user. Panjang (5 akun × ~2min) → jalankan via terminal `background=true`, cek hasil dengan `grep OK key= /tmp/run5.log`. Kalau N gagal sebagian jalan lagi (random proxy baru) — user minta total N fresh key, bukan laporan gagal. Cek jalan: `pgrep -f "node run5.mjs"`.

### Farm TUI interaktif — headless drive
`src/tui.mjs` (tokenharbor-farm) nunggu keypress menu (mis. `9` = start) — jalan bare `node src/tui.mjs` di background tanpa input = TUI nunggu stdin forever, gak mulai. Pipe keypress dengan delay:
```bash
cd ~/app/cache/scratch/tokenharbor-farm && (sleep 3; printf '9\n') | node src/tui.mjs > logs/headless.log 2>&1
```
jalankan via terminal `background=true` + notify. Verifikasi jalan: `ps -eo pid,cmd | grep "src/tui"` (**nunjukin DUA: wrapper bash + node asli**) — bunuh keduanya, atau just process_manage. Jangan cek `pgrep -f` sendirian → match bash wrapper doang.

## Tempmail
- exsala (default): `https://api.your-provider.com/api/tools/tempmail-v3/create?apikey=gionova14` → `{data:{email,token}}`; inbox `.../inbox?token=<email>&apikey=`; shape `{data:{total,emails:[{subject,content}]}}`. Gak butuh auth key (default `gionova14` dari cfbypass.js).
- me: worker `https://tempmail.YOUR_ACCOUNT.workers.dev` (`/generate`, `/inbox?email=`). Domain `@me-agent.web.id`.
- Provider tempmail di `src/inbox/index.mjs`: `temp-email-dev` (browser, gak jalan dari DC IP), `custom`/`rest` (mail.tm), `me`, `exsala`.

## Proxy — KRITIS
- **Proxt.txt `~/app/proxt.txt` (19k): semua basi/datacenter checkpoint → 0 live. Jangan dipake.**
- **Jio pool `~/app/jio_proxies_pool.txt`: scan via PLAYWRIGHT (bukan urllib) → 51 proxy buka form.** Simpan di `~/app/cache/scratch/thc/good_jio_pw.txt`.
- **Format proxy pool beda**: proxt.txt = `user:pass@host:port` TANPA skema; jio pool = udah `http://`. thc_farm.mjs nambah `http://` sendiri → file pool yang dibaca WAJIB tanpa skema. Jangan salin mentah dari proxt.txt ke good_jio_pw.txt tanpa strip skema.
- **User insist pool bekas (ex: proxt.txt "premium 20k"): JANGAN debat dari ingatan — re-scan sample dulu.** Jalankan `node ~/app/cache/scratch/thc/_scan_proxt.mjs` (Playwright, sample 120 random, output `good_proxt.txt`). Bukti scan 120 → 0 live. Versi portable: `scripts/scan_proxt.mjs` di skill ini.
- **Scan proxy WAJIB Playwright** — urllib gagal: tokenharbor SPA/Next.js render JS, HTML mentah gak ada input type=email. Vercel Security Checkpoint di IP datacenter flagged.
- **Probe pool fisik SEBELUM farm run** — jangan bakar retries/timeout di pool yang health-nya taktahu. Sample kecil raw HTTP (mis. POST api.guerrillamail.com / api.ipify.org via tiap proxy) dulu, baca FAILURE-MODE bukan cuma hitung mati: `Tunnel connection failed: 400 Bad Request` = proxy HIDUP tapi TOLAK tunnel HTTPS (Squid acl SSL_ports, CONNECT dinonaktifkan, atau auth gagal) — beda dari `Connection refused`/timeout (proxy beneran mati) dan `403 Forbidden` (auth/deny target). Port 3128 = Squid default: sering nolak CONNECT atau butuh proxy-auth yang tidak disediakan pool. Pool yang SEMUA 400/403 = config-side reject — jangan retry per proxy, cari pool baru / jalan direct (`proxy: off` = semua akun IP bawaan VPS).
### Pool exclusion tiers (`pools/proxies.txt`)
- File sibling turunan dari nama pool (strip `.txt`): `<base>-banned.txt` (permanen), `<base>-cooldown.txt` (time-bound; format `proxy  # <label> <until_ms>`, baris kadaluarsa diabaikan), `<base>-skip.txt` (permanen, manual). Format tiap file: satu proxy per baris, `#` komentar diabaikan.
- **Tiap consumer pool load exclusion files SENDIRI-sendiri** (pickProxy worker, pool picker recheck). Nambah tier exclusion baru (mis. skip) WAJIB patch ke SEMUA consumer — kalau tidak diverge dan consumer lain (recheck) tetap pakai proxy yang udah di-skip. Grep `loadExcluded|banned|cooldown|skip` dulu buat enumerasi semua consumer sebelum nambah tier.
- **Picker WAJIB baca ulang exclusion files berkala** (tiap ~5 panggilan) — snapshot statis gak pernah liat ban/skip/cooldown yang ditulis runtime.
- **Pool file itu HIDUP — bisa di-rewrite proses lain / merge session lain kapan aja** (bukan cuma exclusion files). Jangan bangun edit di atas snapshot yang kebaca beberapa menit lalu: re-read file tepat sebelum nulis. Abis nulis, verify ulang (concurrent writer bisa clobber hasil edit begitu selesai). Cek merge pakai `scripts/verify_pool.py <source> <pool>` — verifikasi set-based (semua baris source ada di pool) + host coverage (`rsplit('@')`) + bad-token scan. JANGAN cek nyari line number — baris bergeser abis merge, dan isi yang sama bisa keliatan beda karena format berubah (prefix ke-strip).
- Proxy confirmed: `103.18.78.135:8080` (flaky), `103.152.148.19:8282`, `103.156.17.71:8818`.
- IP VPS langsung: 1 akun OK, abis itu ke-flag (`email-taken` padahal email baru — false positive, page gak redirect dashboard).

## Lokasi repo — volatile
`~/app/cache/scratch/` itu VOLATILE — isi idle 24h di-prune. Jangan anggap repo farm di sana ada selamanya. Kalau `thc.js` nunjuk ke BASE `~/app/cache/scratch/thc` dan folder hilang: jangan rebuild from scratch dulu — cek `~/app/farms/thc/` (durable, git-tracked) + `git ls-files | grep thc` + clone ulang `tokenharbor-farm` ke scratch kalau perlu. Daerah durable: `~/app/`. Daerah transient: `scratch/` (auto-prune).

## Flow signup
`/login?mode=signup` (bukan `/signup`) → form `input[type=email]` + `input[type=password]` → tombol "Create account" → dashboard → verify email (klik link) → API key `thk_live_`. Per akun ~75-150s. Email-taken = false positive kalau text landing gak berubah.

Detail arsitektur repo `tokenharbor-farm` (hybrid verify+mint dari IP bawaan, fast-path endpoints `/api/me/send-verification-email` + `/api/keys`, klasifikasi provider inbox HTTP-vs-browser, retry semantics, throttle handling): `references/tokenharbor-farm-architecture.md`.

## Baca hasil run (MULTI-PROCESS → file pertama, bukan terakhir)
Hasil farm = gabungan beberapa `output/run_*.json` (satu per CLI call), masing-masing satu array. `thc_farm.mjs` merge semua file jadi `~/app` — baca file GABUNGAN itu, atau `node -e "process.stdout.write(JSON.stringify(require('fs').readdirSync('output')))` — JANGAN `cat <file>` + `head -n 2 jam terakhir`. Konvensi nama file: `run_<created_at>.json`, isi `ok`/_api_key_/_email-taken_. File terakhir bisa kosong/truncated kalau farm mati seketika — mergeResults toleransi JSON malformed (`catch {}`).

Beda format output: `thc_farm.mjs`/`src/index.mjs` nulis `run_<created_at>.json` (satu array per file); `run5.mjs` nulis `run5_<ts>.json` (SATU objek hasil per file, bukan array). Glob `output/run*.json` nyangkut dua-duanya. **JANGAN percaya file gabungan `~/app` saat resume — bisa stale dari merge lama; selalu recompute dari glob `output/run*.json` + dedupe.** File `thc_results.json` tua nunjukin key yang udah dipump, padahal output/ masih bawa key fresh yang belum.

Kalau user minta yang "fresh" — link yang kadarluasa/pakai dianggap user gak berguna; lapor jumlah key valid, jangan tampilkan expired. "Fresh" = key yang BELUM di 9router (sudah dipump = dianggap kepake/rusak). Form deliver VERBATIM tiap key:
```
link fresh jio - me / <n> / <key>
```
Gagal proxy = `elapsed_ms` <10s + `ERR_PROXY_CONNECTION_FAILED`/`ERR_TIMED_OUT` (`error_kind` network/other) — retry dengan proxy lain, bukan ubah flow.

## Dedupe vs 9router SEBELUM kirim (fresh = belum dipump)
Orch new keys JANGAN langsung kirim — bandingkan dulu sama pool 9router. Key `thk_live_*` yang udah masuk `providerConnections.data.apiKey` di DB = udah dipump → user nilai gak fresh, buang dari laporan.

`sqlite3` CLI TIDAK install di VPS — pake Python stdlib (sudah terbukti).
```python
import sqlite3, json, glob, os
con=sqlite3.connect("~/app/db/data.sqlite"); cur=con.cursor()
# set key thk yang SUDAH di pool (data kolom JSON, ambil apiKey)
db_thk=set()
for d, in cur.execute("SELECT data FROM providerConnections"):
    try:
        k=json.loads(d).get("apiKey","")
        if k.startswith("thk_live_"): db_thk.add(k)
    except: pass
# key dari hasil farm (gabungan semua output/run*.json)
mine={r["api_key"] for f in glob.glob("~/app/cache/scratch/thc/output/run*.json")
      for r in json.load(open(f)) if r.get("ok") and r.get("api_key","").startswith("thk_live_")}
fresh=sorted(mine-db_thk); print(len(fresh),"fresh /", len(mine),"total")
```
DB punya ribuan row (dahl 8k+) — jangan cat semua; loop `data` doang. Jangan stop pas 15 row pertama; `SELECT data FROM providerConnections` TANPA LIMIT, filter di Python. Terus bacakan gabungan output (bukan satu file terakhir) supaya gak ada key ke-lewat.

## Pump ke 9router — DEFAULT OFF
User rule: JANGAN auto-push hasil farm ke 9router — pool itu publik. Auto-pump di `thc_farm.mjs` (tiap 5 key + final) KONFLIK sama rule ini — nonaktifkan sebelum run, atau edit thc_farm.mjs jadi hasil cuma ke file. Kirim ke user, hapus file setelahnya.

Kalau DISURUH pump: `~/app/thc_pump.py` (provider DB `openai-compatible-chat-89d5eb90-2f90-47ce-b5a9-69734bbcc35a` — MUST pakai id yang ADA di tabel providerNodes, bukan `openai-compatible-chat-tokenharbor`; kalau id orphan, row masuk DB tapi gak kelihatan dashboard). baseUrl `https://api.tokenharbor.ai/v1`.

Pump re-run idempotent: `0 key baru` = udah pernah dipump, bukan bug.

### Autopump KONFLIK di thc_farm.mjs
`thc_farm.mjs` nulis gabungan ke `~/app` — SALAH SATU sumber stale. Tambah rule: kalau defisit 1-2 key, TIDAK usah jalankan farm ulang (mahal, OOM risk, lama) — langsung kirim yang fresh ada. Kebutuhan user = fresh, bukan angka genap.

## Pitfall
- `elapsed_ms` di record output nentuin kelas error: **close cepat (<10s) = proxy mati/network**, close lambat (~30s konsisten semua akun) = OOM-kill chromium. Jangan buru-buru baca semua `browser has been closed` sebagai OOM — cek `elapsed_ms` dulu, beda obatnya (ganti proxy vs bersihin orphan chromium).
- Klasifikasi error per run pakai `scripts/analyze_output.py` (aggregate `output/run_*.json` → total, ok+key, hitung per `error_kind`). Baca gabungan, bukan satu file.
- tokenharbor dihost Vercel → proxy datacenter kena Vercel Security Checkpoint.
- Tiap akun butuh `timeout 260` (child node src/index.mjs).
- 9router dashboard di **:20128** (bukan 20127). Restart service: `pm2 restart 9router`, verifikasi uptime reset + `curl -sL -o /dev/null -w "%{http_code}" http://127.0.0.1:20128/` → 200 (redirect 307 `/dashboard` dulu). **`curl :20127` = 000 (refused) itu NORMAL — BUKAN tanda server mati**; `node custom-server.js --port 20127` di argv pm2 menyesatkan, socket beneran dengerin di 20128. Jangan declare "server down" dari 20127=000; cek 20128 dulu.
- `pgrep -f` bisa nge-match shell pemanggilnya sendiri (pattern text ada di command line bash wrapper) → nunjukin PID palsu yang lagi mati. Jangan percaya mentah; verifikasi dengan `ps -p <pid> -o pid,cmd` dulu, baru bunuh.

## OOM / resource 2GB (KRITIS — terbukti bawa semua mati)
Error `browser has been closed` di `page.goto` ~30s konsisten semua akun = OOM-kill chromium, BUKAN flow bug. VPS 2GB/2-core jalan Hermes (318MB) + next-server 9router (159MB) + farm (69MB) + browser — di `ps aux --sort=-rss` keliatan 9 browser 40-150MB tiap satu. OOM fatal bisa matiin SELURUH tmux server (thc + farm + hunter session semua) → farm runner ikut mati. Bukan cuma thc yang gagal.

Rule:
1. **JANGAN jalanin browser farm (thc) bareng jio farm + hunter + Hermes** di 2GB — OOM, trus semua mati (rugi: farm runner ikut mati). Prioritas: link farm (uang) > key thc. Kalau thc mau jalan: stop farm dulu, jalankan thc, start balik farm setelahnya.
2. **Bersihin SEMUA orphan browser SEBELUM retry farm** — gagal/OOM ninggalin proses chromium 40-150MB masing. cf-clearance-scraper (`~/app`, node `index.js` spawner) juga bisa ngeblob Chrome nyampe 174 proses × 40-150MB → OOM, bisa matiin 9router. Brush lengkap: `tmux kill-session -t thc; pkill -9 -f chromium; pkill -9 -f chrome; pkill -9 -f 'cf-clearance|index.js'`. VERIFIKASI sebelum lanjut: `pgrep -c chrome` = 0, `pgrep -f 'cf-clearance'` kosong, `free -m` available ≥700MB. Tanpa ini, run berikutnya OOM lagi di titik yang sama.
3. `MAX_CONCURRENCY` 2 (dari 3) pas jalan di 2GB.
4. Belum ke-test (jangan tulis verified): `node src/index.mjs -c 2` satu process satu browser dua context jauh lebih ringan dari `thc.js` spawn 2 proses terpisah — worth coba saat manual run.
