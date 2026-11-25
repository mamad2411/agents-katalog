---
name: proxy-pool-manager-ops
description: "Use when rotating or health-checking the proxy pool."
---

# Proxy Pool Manager — azza (/opt/proxy-pool-manager)

Service: `systemctl status proxy-pool-manager` — API 127.0.0.1:PORT_PROXY, panel via Caddy :8891 (basicauth ari / CHANGE_ME_PASSWORD). Token: `/opt/proxy-pool-manager/token`, kirim header `X-Api-Token`.

## Endpoints
- `GET /next` → proxy verified hidup acak (JSON `url` siap pakai: `http://user:pass@host:port`). Prioritas: yang pernah lolos probe (ada `exit_ip`).
- `GET /next?cc=jp` → sama tapi exit dipindah ke negara tsb — username di-swap jadi `__cr.<cc>` (host/port/pass sama). 72 kode geo (SUPPORTED_CC di manager.py): ae am ar at au az be bg bh br ca ch cl co cz de dk ee eg es fi fr gb ge gr hk hr hu id ie il in iq ir it jo jp ke kr kw kz lb lt lv ma md mx my ng nl no nz om ph pl pt qa ro rs ru sa se sg sk th tr tw ua us vn za uz. cc invalid → 400. VERIFIED: jp→JP Amagasaki, us→US Leesburg, id→ID Denpasar. 816 port × 72 cc ≈ 58k exit.
- `GET /current` — yang terakhir /next
- `GET /stats` — total/alive/dead/geo_codes/combos/events; `GET /list?alive=1&tag=vn`
- `POST /check` — full scan (48 worker paralel, 816 proxy ~40s, non-blocking)
- `POST /import {"proxies":["host:port:user:pass",...], "tags":["vn"]}` — tambah pool baru
- `POST /mark?host=&port=&ok=0/1` — tool lain lapor hasil pakai proxy
- `POST /prune` — buang semua yang dead
- `GET /panel` — dashboard live (auto-refresh 5s)

## perilaku
- Health loop tiap 5 menit otomatis. Probe = HTTPS api.ipify.org via proxy, simpan latency + exit IP.
- `fails >= 3` beruntun → `dead=true` → keluar dari /next dan live.txt. Satu sukses → reset fails.
- live.txt di /opt/proxy-pool-manager = snapshot hidup (host:port:user:pass) — sumber pool buat tool lain.
- Telegram-rotator (18125) TIDAK pakai ini (dia punya health-check sendiri, jangan disentuh — lifeline gateway). Tool lain (firecrawl-farm, farming, scraper) wajib ambil proxy dari /next + lapor /mark kalau gagal.

## integrasi tool (pola)
```python
import urllib.request, json
TOK = open('/opt/proxy-pool-manager/token').read().strip()
req = urllib.request.Request('http://127.0.0.1:PORT_PROXY/next', headers={'X-Api-Token': TOK})
proxy = json.load(urllib.request.urlopen(req))['url']
# pakai proxy... kalau gagal: POST /mark?host=..&port=..&ok=0 → manager yang matur mati/ganti
```

## Pitfall Caddy 2.6 di azza
- Directive = `basicauth` (bukan `basic_auth` 2.7+); hash = `caddy hash-password --plaintext 'pw'`
- `admin off` di Caddyfile → `systemctl reload` GAGAL (minta :2019). WAJIB `systemctl restart caddy`.
