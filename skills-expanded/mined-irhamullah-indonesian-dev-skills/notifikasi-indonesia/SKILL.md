---
name: notifikasi-indonesia
description: Use when sending notifications via WhatsApp (Fonnte, Wablas, Watzap, official Meta Cloud API), Telegram Bot, or Email (SMTP/Gmail) for Indonesian users. Triggers on "kirim WhatsApp", "notifikasi WhatsApp", "WA gateway", "Fonnte", "Wablas", "Telegram bot notif", "OTP WhatsApp", "kirim email dari aplikasi", "notification service", "alert ke WhatsApp/Telegram"
---

# Notifikasi Indonesia (WhatsApp, Telegram, Email)

## Overview

Kirim notifikasi ke user Indonesia via channel yang benar-benar mereka pakai:
**WhatsApp** (dominan), **Telegram** (internal/alert), dan **Email**
(formal/transaksional). Satu interface `NotificationProvider` + adapter per
provider, sehingga business logic tetap provider-agnostic dan gateway bisa
diganti tanpa mengubah alur bisnis.

## When to Use

- Kirim OTP / verifikasi via WhatsApp
- Notifikasi transaksi (order, pembayaran) ke customer
- Alert internal (worker down, error spike) ke Telegram/WhatsApp
- Email transaksional (invoice, reset password)
- Multi-channel fallback (WA → SMS → Email)
- Migrasi antar WhatsApp gateway (Fonnte ↔ Wablas ↔ official)
- Trigger: "kirim WhatsApp", "WA gateway", "Fonnte", "Wablas", "OTP WhatsApp",
  "Telegram bot notif", "kirim email dari aplikasi", "alert ke WhatsApp/Telegram"

**Jangan pakai kalau:** payment webhook (lihat `payment-gateway-indonesia`) atau
push notification mobile (FCM/APNs) — keduanya berbeda.

## Router

| Topik / tugas | Berkas |
| --- | --- |
| WhatsApp gateway: Fonnte, Wablas, Watzap, Meta Cloud API, normalisasi nomor, anti-ban | `references/whatsapp-gateway.md` |
| Telegram bot: setup, chat_id, HTML, inline buttons, webhook, alert server | `references/telegram-bot.md` |
| Email: Gmail SMTP, Nodemailer, template HTML, SPF/DKIM/DMARC, Resend | `references/email-notification.md` |
| OTP flow, security rules, template pesan, opt-in/consent | `references/otp-and-templates.md` |
| Perbandingan channel/provider, biaya, decision tree, migration path | `references/provider-comparison.md` |
| Anti-pattern: kode salah vs benar (hardcode provider, OTP lemah, log sensitif) | `references/anti-patterns.md` |
| Adapter lengkap semua provider, service orchestrator, factory, `.env` | `examples.md` |

## Core Principles

1. **Channel abstraction.** Satu interface `NotificationProvider` untuk semua
   channel; business logic tidak boleh tahu detail provider.
2. **Pilih channel sesuai konteks.** OTP/transaksional → WhatsApp, alert internal
   → Telegram, dokumen formal → Email, marketing → WhatsApp dengan opt-in wajib.
3. **Official vs unofficial.** Unofficial (Fonnte/Wablas/Watzap) murah dan cepat
   tapi nomor bisa di-ban; official (Meta Cloud API) aman untuk produksi/high
   volume. Selalu siapkan fallback.
4. **Idempotency & rate limit.** Jangan kirim OTP berulang untuk request yang
   sama; batasi maksimal 3 OTP per 5 menit per nomor.

```typescript
// Business logic cukup begini — provider dipilih lewat config
await notifier.send({
  channel: 'whatsapp',
  to: '+6281234567890',
  template: 'otp',
  data: { code: '123456' },
});
```

## Workflow

1. Petakan kebutuhan ke channel (OTP, transaksional, internal, formal, marketing).
   → detail: `references/provider-comparison.md`
2. Pilih provider dan pahami aturannya (24h window, template approval, risiko ban).
   → detail: `references/whatsapp-gateway.md`
3. Definisikan `NotificationRequest`/`NotificationProvider` dan
   `NotificationService` sebagai orchestrator.
   → detail: `examples.md`
4. Implement adapter per provider (Fonnte, Wablas, Watzap, Meta, Telegram, Email).
   → detail: `examples.md`
5. Susun template terpusat dan flow OTP yang aman (hash, TTL, max attempts).
   → detail: `references/otp-and-templates.md`
6. Isi konfigurasi via environment variable dan wiring factory per channel.
   → detail: `examples.md`
7. Tambahkan fallback multi-channel dan logging tanpa data sensitif.
   → detail: `references/anti-patterns.md`

## Anti-Patterns

- Hardcode provider di business logic (`fonnte.sendWA(...)`) — pakai `notifier.send()`.
- Kirim WA marketing tanpa opt-in → ban + ilegal.
- OTP pakai `Math.random()` — wajib `crypto.randomInt()`.
- Simpan OTP plaintext — hash dulu (bcrypt) dengan TTL.
- Tidak ada fallback saat WA gagal.
- Log nomor/OTP penuh — selalu mask.
- Pakai Gmail SMTP untuk produksi volume tinggi.
- Email tanpa SPF/DKIM/DMARC, layout flexbox, atau tanpa plain-text fallback.
- Blast pesan identik ke banyak nomor tanpa personalisasi (risiko ban unofficial).

Detail kode salah/benar: `references/anti-patterns.md`.

## Verification

- [ ] Unified `NotificationProvider` interface
- [ ] Minimal 1 channel per jenis (WA, Telegram, Email)
- [ ] Provider dipilih via config (bukan hardcode)
- [ ] Template engine untuk pesan
- [ ] Rate limiting untuk OTP/notif sensitif
- [ ] OTP: crypto-secure + hashed + TTL
- [ ] Multi-channel fallback untuk notif kritikal
- [ ] Opt-in tracking untuk marketing
- [ ] Logging tanpa data sensitif
- [ ] Handle provider outage (retry + fallback)
- [ ] Biaya/quota monitoring (WA gateway)
- [ ] Kepatuhan: official API untuk volume tinggi

## References

- `references/whatsapp-gateway.md` — Fonnte, Wablas, Watzap, Meta Cloud API, normalisasi nomor, rate limit & anti-ban.
- `references/telegram-bot.md` — setup @BotFather, chat_id, HTML vs Markdown, inline buttons, webhook, alert server.
- `references/email-notification.md` — Gmail SMTP, Nodemailer, template HTML, deliverability (SPF/DKIM/DMARC), Resend.
- `references/otp-and-templates.md` — OTP flow lengkap, security rules, idempotency, template & renderer, opt-in.
- `references/provider-comparison.md` — perbandingan channel/provider, biaya, decision tree, hybrid strategy, migration.
- `references/anti-patterns.md` — contoh kode salah vs benar untuk semua jebakan umum.
- `examples.md` — adapter lengkap semua provider, service orchestrator, fallback, factory, `.env`.

## Related Skills

- `payment-gateway-indonesia` — Notifikasi status pembayaran
- `hosting-deployment-indonesia` — Alert server ke Telegram/WhatsApp
- `security-and-hardening` — Rate limiting, secret management
- `observability-and-instrumentation` — Logging & delivery monitoring
