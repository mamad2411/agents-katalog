---
name: agenmail-inbox-infra
category: farm
description: Use when deploying CF inbox infra or extracting OTP.
---

# AgentMail Inbox Infra — own CF mail for farming

Repo: `~/farming/repos/agenmail` (clone dari hirotomasato/agenmail).
Inbox infra untuk agents: 1 Cloudflare Worker terima mail via Email Routing (catch-all), simpan di D1+R2, expose JSON. Dashboard private provisioning mailbox. Ini JAUH lebih gacor dari tempmail exsala/worker sendiri — karena multi-domain (semua zone di account), mailbox unlimited, OTP parsed.

## Kenapa gacor buat farming
- **Multi-domain**: 1 worker layani SEMUA zone di CF account. Domain burn → tambah domain baru tanpa deploy ulang.
- **Public create**: `POST /api/v1/mailboxes` bisa anonymous kalau `PUBLIC_CREATE_ENABLED=true` → farm bikin mailbox tanpa auth.
- **Long-poll inbox**: `GET /api/v1/mailboxes/me/messages?wait=25` — nunggu sampai mail masuk (max 25s), langsung return. Perfect buat farm: create → signup → wait → ambil OTP, tanpa polling loop.
- **OTP auto-extract**: `src/lib/extract.ts` parsed kode verifikasi otomatis (regex keyword window ±90 chars, sanitize URL/UUID).
- **TTL per mailbox**: 60s–2592000s, auto-expire. Gak perlu cleanup manual.

## Deploy
```bash
cd ~/farming/repos/agenmail
pnpm install
npx wrangler d1 create agentmail
npx wrangler r2 bucket create agentmail-mail
# isi wrangler.jsonc: database_id, routes custom_domain, PUBLIC_BASE_URL, PUBLIC_CREATE_ENABLED=true
npx wrangler secret put TOKEN_PEPPER  # openssl rand -hex 32
npx wrangler secret put ADMIN_TOKEN   # prefixed: agn_xxxxxxxx
npx wrangler d1 migrations apply DB --remote
pnpm deploy
```

## API inti (base `/api/v1`)
| Endpoint | Auth | Fungsi |
|---|---|---|
| `POST /mailboxes` | Bearer admin ATAU anonymous (kalau PUBLIC_CREATE_ENABLED=true) | bikin mailbox. Body: `{domain: "random"|specific, local?, label?, ttl?, meta?}`. Response: `address`, `apiKey` (sekali), `accessToken` |
| `GET /mailboxes/me/messages?wait=25` | `X-API-Key` | long-poll inbox, return saat mail masuk |
| `GET /messages/<id>` | `X-API-Key` | parsed message: from, subject, snippet, otp[], links[], codes[], intent, primaryLink |
| `POST /admin/domains` | Bearer admin | register domain baru |

Auth: `Authorization: Bearer <admin>` atau `X-API-Key: <mailbox>` atau `X-Access-Token: <link>`. Dashboard session pakai cookie `agentmail_admin` + `X-AgentMail-CSRF: 1` buat mutation.

## Teknik OTP extraction (dari src/lib/extract.ts)
1. **Sanitize dulu**: hapus URL (`https?:\/\/[^\s<>"'`()[\]]+`) dan UUID (`[0-9a-f]{8}-...`) — keduanya berisi digit run yang bukan OTP.
2. **Subject priority**: kode di subject hampir selalu yang dimaksud mail.
3. **Keyword window**: kode di body cuma valid kalau dalam ±90 chars dari kata kunci (otp|verification|verify|passcode|security code|kode|verifikasi|pin|token|login code|auth code).
4. **Format `123 456` / `123-456`**: gabung jadi `123456`.
5. **Digit 4–8** yang standalone (bukan embedded dalam token lebih panjang).
6. Keyword beda: `code|coupon|promo|voucher|referral|invite|activation|license|key` → `codes[]` (alphanumeric).
7. `unsubscribe`/`opt-out` link dipisah (`unsubscribe[]`) biar automation gak pernah follow.
8. `intent`: verification|password_reset|receipt|newsletter|notification|other; `primaryLink` = link yang cocok intent (verify|confirm|activate|reset|magic|token|invite|accept|signin).

## Pitfall
- `local` unik per domain; duplicate → `409 address_taken`. Generated names retry otomatis kalau collision.
- TTL min 60s — jangan set lebih kecil.
- `TOKEN_PEPPER` ganti = semua API key + session invalid.
- MIME parsing: `src/lib/mime.ts` handle multipart + base64. Kalau perlu parse HTML mail, pakai `content` dari message (bukan snippet).
- Rate limit ada di `src/ratelimit.ts` — per-IP untuk public create; kalau farm ngebut, rotate IP atau set lebih longgar.
