---
name: cf-bulk-deploy
description: "Bulk deploy Cloudflare Worker proxy relays across accounts."
version: 1.0.0
author: Me
license: MIT
---

# Hermes · powered me

## When to Use
Gunakan saat: mau deploy banyak akun Cloudflare jadi Worker proxy relay, bangun proxy pool dari akun CF, atau diagnosa credential token CF. Endpoint di bawah hasil verifikasi langsung ke API Cloudflare.

# CF Bulk Deploy — Worker Proxy Relay

Deploy N akun Cloudflare menjadi Worker proxy relay sekaligus (concurrency 10, max 100/run). Semua request diteruskan ke satu upstream. URL relay hasil masuk proxy pool (`Type: cloudflare`).

## Input
Satu akun per baris: `name/email|accountID|apiToken[|domain]`
Naming worker: `<prefix>-<batch>-<urutan>` — BUKAN dari email. Publikasi ke **Custom Domain** (zone milik akun), bukan workers.dev.

## Endpoint CF (TERVERIFIKASI — jangan pakai yang lain)
| Method | Endpoint | Status |
|---|---|---|
| GET | `/user` | ✅ identitas token |
| GET | `/accounts/{id}` | ✅ cek akses akun |
| GET | `/zones?account.id={id}&status=active&per_page=50` | ✅ daftar zone |
| PUT | `/accounts/{id}/workers/scripts/{name}` | ✅ upload script (multipart) |
| PUT | `/accounts/{id}/workers/domains` | ✅ publish Custom Domain |
| POST | `/accounts/{id}/workers/domains` | ❌ 10405 method not allowed — pakai PUT |
| GET | `/accounts/{id}/zones` | ❌ 7003 route tidak ada |

## Dua Bug Kritis (jangan ulangi)
1. **Endpoint zone:** `/accounts/{id}/zones` TIDAK ADA. Benar: `/zones?account.id={id}`. Error `7003 Could not route` = route salah. Probe endpoint: kirim credential sengaja rusak — `6003/9106` = route ADA (cuma auth ditolak), `7003/7000` = route TIDAK ADA.
2. **JSON `result`:** field `Result` tipe `[]byte` di Go HANYA menerima string base64 → error `non-JSON response (N bytes)` saat CF balas `result: []`. Pakai `Result any` lalu round-trip marshal sebelum unmarshal ke slice.

```go
type cfEnvelope struct {
    Success bool           `json:"success"`
    Errors  []cfAPIErrItem `json:"errors"`
    Result  any            `json:"result"`
}
raw, _ := json.Marshal(env.Result)
var zones []cfZone
json.Unmarshal(raw, &zones)
```

## Worker Script (proxy relay)
Upstream di-bake ke source — worker tidak butuh secret/KV:
```js
const UPSTREAM = "https://upstream.example.com";
export default {
  async fetch(request) {
    const incoming = new URL(request.url);
    const upstream = new URL(UPSTREAM);
    upstream.pathname = incoming.pathname;
    upstream.search  = incoming.search;
    const headers = new Headers(request.headers);
    headers.set("X-Forwarded-Host", incoming.host);
    headers.set("X-Forwarded-Proto", "https");
    const init = { method: request.method, headers, redirect: "manual" };
    if (request.method !== "GET" && request.method !== "HEAD") init.body = request.body;
    const resp = await fetch(new Request(upstream.toString(), init));
    const out = new Headers(resp.headers);
    out.set("X-Exsala-Relay", "<name>");
    return new Response(resp.body, { status: resp.status, headers: out });
  },
};
```

## Auth CF — dua skema + auto-fallback
1. `Authorization: Bearer <token>` (scoped API token)
2. `X-Auth-Email` + `X-Auth-Key` (Global API Key) — fallback otomatis

Fallback dipicu jika respons = `6003, 6103, 6111, 9106, 9109, 10000, 10001` atau body tak ter-parse. Syarat: kolom pertama berisi email (`@`).

## Permission Token (per akun)
`Account → Account Settings: Read` · `Zone → Zone: Read` · `Zone → DNS: Edit` · `Account → Workers Scripts: Edit` → buat di dash.cloudflare.com/profile/api-tokens, template "Edit Cloudflare Workers" + tambah `Zone:Read`.

## Credential Diagnostics (sebelum deploy)
Probe per akun (paralel 10), verdict:
- `SIAP DEPLOY` — token ✓ account ✓ ada zone
- `TOKEN MATI / FORMAT SALAH` — token ditolak
- `ACCOUNT ID TIDAK COCOK` — token valid tapi bukan akun itu (`9109`)
- `AKUN TANPA ZONE AKTIF` — 0 domain aktif

## Pitfalls (dari deploy nyata)
- **Jangan simpan API token** — pakai sekali saat deploy, tak pernah ke DB.
- Build order: frontend (npm build) DULU, baru Go — `go:embed` snapshot `web/dist` saat compile. Cek hash aset yang dilayani `curl ... | grep -oE '/assets/index-[A-Za-z0-9_-]+\.js'`.
- Deploy binary: `systemctl stop` dulu sebelum `cp` — binary dipakai = `Text file busy`.
- `pip3` mungkin tidak ada di VPS → `apt install python3-fonttools`.
- `json.RawMessage` tidak ada di `encoding/json/v2` → pakai `any`.

## Batasan jujur
Relay CF = domain/endpoint murah (banyak subdomain dari N akun). BUKAN IP unik — semua worker muncul dari IP edge CF yang sama per region. Gagal untuk target yang fingerprint by-IP.
