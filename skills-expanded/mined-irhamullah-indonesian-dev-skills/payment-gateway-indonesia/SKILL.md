---
name: payment-gateway-indonesia
description: Use when integrating Indonesian payment gateways (Midtrans, Xendit, Doku) with QRIS, Virtual Account, or e-wallets (GoPay, OVO, DANA, ShopeePay). Triggers on "payment gateway", "Midtrans", "Xendit", "Doku", "QRIS", "virtual account", "e-wallet", "GoPay", "webhook verification", "payment integration Indonesia"
---

# Payment Gateway Indonesia Integration

## Overview

Integrasi payment gateway lokal Indonesia (Midtrans, Xendit, Doku) dengan satu
normalization layer: interface `PaymentGateway` yang provider-agnostic, adapter per
provider, dan webhook handler yang memverifikasi signature sebelum memproses payload.
Detail per topik ada di `references/`, contoh implementasi lengkap di `examples.md`.

## When to Use

- Setup payment gateway Indonesia (Midtrans, Xendit, atau Doku)
- Implement payment methods: QRIS, Virtual Account, e-wallet (GoPay, OVO, DANA, ShopeePay)
- Handle webhook dari payment provider
- Mapping status transaksi yang berbeda-beda antar provider
- Setup sandbox testing environment
- Switch atau tambah payment provider baru

**Jangan pakai kalau:**

- International payment gateway only (Stripe, PayPal) → gunakan `api-and-interface-design`
- Payment logic sudah ada dan stable (cuma bug fixing kecil)

## Router

| Topik / tugas | Berkas |
| --- | --- |
| Bandingkan provider: endpoint, auth, payload per metode, pros-cons | `references/provider-comparison.md` |
| Verifikasi signature webhook per provider | `references/webhook-verification.md` |
| Mapping status transaksi & transisi status | `references/status-mapping.md` |
| Sandbox: kredensial, simulasi pembayaran, env vars, testing | `references/sandbox-setup.md` |
| Interface `PaymentGateway` + tipe `PaymentStatus` | `references/status-mapping.md#normalized-payment-interface` |
| Normalize status di adapter, bukan di business logic | `references/status-mapping.md#normalize-at-the-boundary` |
| Factory / provider selection | `references/provider-comparison.md#factory-pattern-untuk-provider-selection` |
| Webhook handler provider-agnostic | `references/webhook-verification.md#provider-agnostic-webhook-handler` |
| Idempotent webhook handling | `references/webhook-verification.md#idempotent-webhook-handling` |
| Adapter Midtrans/Xendit/Doku lengkap + contoh aplikasi | `examples.md` |
| Anti-pattern: status string hardcoded | `references/status-mapping.md#anti-pattern-status-string-hardcoded` |
| Anti-pattern: provider logic bocor ke business layer | `references/provider-comparison.md#anti-pattern-provider-logic-leaking-to-business-layer` |

## Core Principles

1. **Normalize at the boundary.** Format tiap provider berbeda; normalisasi dilakukan
   sekali di adapter, sisa aplikasi memakai `PaymentStatus` yang sama.
2. **Webhook security first.** Verifikasi signature sebelum memproses payload; algoritma
   berbeda per provider (SHA512, HMAC-SHA256, SHA256).
3. **Idempotent webhook handling.** Webhook bisa datang berulang; cek status transaksi
   dulu dan proses hanya sekali.
4. **Business layer provider-agnostic.** Business logic tidak boleh tahu detail provider;
   akses provider lewat `PaymentGatewayFactory`.

## Workflow

1. Pilih provider dan payment method yang didukung → detail: `references/provider-comparison.md`
2. Definisikan interface `PaymentGateway`, `PaymentStatus`, dan tipe request/response → detail: `references/status-mapping.md#normalized-payment-interface`
3. Implement adapter untuk satu provider dulu (biasanya Midtrans atau Xendit) → detail: `examples.md`
4. Tambahkan factory agar provider bisa diganti lewat env/config → detail: `references/provider-comparison.md#factory-pattern-untuk-provider-selection`
5. Implement webhook handler: verify → parse → idempotency → update status → post-payment → detail: `references/webhook-verification.md#provider-agnostic-webhook-handler`
6. Setup sandbox, environment variables, dan test signature/status mapping → detail: `references/sandbox-setup.md`
7. Jalankan checklist testing dan production readiness → detail: `references/sandbox-setup.md#testing-checklist`

## Anti-Patterns

- Tanpa signature verification — webhook palsu bisa menandai order sebagai `paid`.
- Status string hardcoded (`settlement`, `SUCCEEDED`, `SUCCESS`) tersebar di business logic.
- Tidak ada idempotency check — webhook berulang memicu charge atau email ganda.
- Provider logic bocor ke business layer (`if provider === ...` di service).
- Memakai production credentials untuk testing, atau API key Xendit sebagai webhook token.
- Log payload/signature mentah sampai kredensial bocor ke log.

## Verification

- [ ] Interface `PaymentGateway` terdefinisi dan documented
- [ ] Minimal 1 adapter implemented (Midtrans or Xendit)
- [ ] Webhook signature verification working
- [ ] Status normalization table complete
- [ ] Sandbox testing berhasil (webhook simulation)
- [ ] Idempotency check implemented
- [ ] Environment variables documented
- [ ] Error handling untuk network failures
- [ ] Logging untuk debugging (without sensitive data)
- [ ] Unit tests untuk signature verification dan status mapping

## References

- `references/provider-comparison.md` — perbandingan Midtrans/Xendit/Doku: endpoint, auth, payload QRIS/VA/e-wallet, pros-cons, migration checklist, factory pattern.
- `references/webhook-verification.md` — algoritma signature per provider, implementasi, gotchas, unit/integration test, security practices, handler provider-agnostic.
- `references/status-mapping.md` — enum status, mapping per provider, unified mapper, business rules, interface `PaymentGateway`, anti-pattern status.
- `references/sandbox-setup.md` — kredensial dan endpoint sandbox, simulasi pembayaran, ngrok, testing checklist, tools, env vars, production readiness.
- `examples.md` — implementasi adapter Midtrans/Xendit/Doku, usage di service, checkout flow, testing helper.

Checklist lintas skill tersedia di bundle `agent-skills`: `security-checklist`
(webhook security) dan `testing-patterns` (testing strategy).

## Related Skills

- `api-and-interface-design` — untuk design interface layer yang robust
- `security-and-hardening` — untuk webhook security dan credential management
- `test-driven-development` — untuk testing adapter implementations
- `observability-and-instrumentation` — untuk monitoring payment transactions
