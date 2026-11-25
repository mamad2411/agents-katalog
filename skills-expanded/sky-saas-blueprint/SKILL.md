---
name: sky-saas-blueprint
description: >-
  Sıfırdan SaaS kurma yol haritası (meta-skill): doğru sırayla auth → org/takım → plan ve
  ödeme → onboarding → çekirdek özellik → dashboard → bildirimler → ayarlar → yasal sayfalar →
  gözlemlenebilirlik → yayın; her adımda hangi Sky skill'inin yükleneceği, MVP kesme kuralları,
  "1 hafta / 1 ay" kapsam şablonları ve yayın öncesi kontrol listesi. "SaaS yapacağım",
  "sıfırdan ürün", "MVP", "abonelikli uygulama" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · SaaS Yol Haritası

Bu bir **orkestrasyon** skill'i: her adımda ilgili skill'i yükle, bitince bir sonrakine geç.
Her adımın sonunda çalışan, deploy edilmiş bir uygulama olsun (dikey dilimler).

## 0. Karar sayfası (30 dk)

- Tek cümle: "**[kime]** için **[ne sorunu]** **[nasıl]** çözen ürün."
- Aha anı (bkz. `sky-onboarding`), ilk 3 çekirdek özellik, fiyat hipotezi.
- Stack: Next.js + Postgres (Supabase/Neon) + Drizzle + Better Auth / Supabase Auth + Tailwind/shadcn (bkz. `sky-web-stack`).
- `sky-architect` yöntemi ile 1 sayfalık plan.

## Sıra

| # | Adım | Skill'ler | Bitti ölçütü |
|---|---|---|---|
| 1 | İskelet + deploy | `sky-web-stack`, `sky-deploy`, `sky-ui-craft` | `/sky-new`, preview URL canlı, CI yeşil |
| 2 | Auth | `sky-auth`, `sky-auth-ux` | kayıt/giriş/çıkış/sıfırlama, korumalı sayfa |
| 3 | Org/takım | `sky-multitenancy` | org oluştur, davet et, rol, izolasyon testi |
| 4 | Çekirdek özellik (dikey dilim) | `sky-data`, `sky-backend-api`, `sky-forms`, `sky-states-library` | aha anına ulaşılabiliyor |
| 5 | Onboarding | `sky-onboarding`, `sky-ux-writing` | kayıttan aha'ya < 5 dk |
| 6 | Plan ve ödeme | `sky-payments`, `sky-metering-quotas`, `sky-pricing-page` | deneme → ücretli geçiş, limitler |
| 7 | Dashboard | `sky-dashboard`, `sky-dataviz` | ana metrikler, tablo, filtre |
| 8 | Bildirimler | `sky-notifications`, `sky-email-design` | işlemsel e-postalar, tercihler |
| 9 | Ayarlar | profil, org, fatura, bildirim, tehlikeli bölge | hesap/org silme çalışıyor |
| 10 | Landing + SEO | `sky-landing`, `sky-seo`, `sky-brand` | Lighthouse ≥ 90, OG kartları |
| 11 | Yasal + gizlilik | `sky-privacy-engineering`, `sky-ethical-ux` | gizlilik, KVKK aydınlatma, çerez, veri indir/sil |
| 12 | Gözlem | `sky-observability`, `sky-security` | Sentry, uptime, audit log, güvenlik başlıkları |
| 13 | Yayın | `sky-launch`, `/sky-check` | GEÇTİ, durum sayfası, destek kanalı |

## MVP kesme kuralları

- Tek kullanıcı tipi, tek ana akış, tek fiyat planı (+ deneme) ile başla.
- Admin paneli yerine önce DB arayüzü (Supabase Studio/Drizzle Studio) — gerçek ihtiyaç doğunca yaz.
- "Kendi kendine yaptığın" işleri (fatura kesme, destek) ilk 20 müşteride elle yap.
- Ertelenebilir: çok dil, mobil uygulama, API, webhook, SSO, gelişmiş raporlar, temalar.
- Ertelenemez: güvenlik (auth, yetki, kiracı izolasyonu), yedekler, hata izleme, hesap silme, ödeme doğruluğu.

## Kapsam şablonları

- **1 hafta**: adım 1–4 + basit landing (tek plan, ödeme yok — bekleme listesi).
- **1 ay**: adım 1–13 (her biri sade).
- **3 ay**: + çok dil, API, gelişmiş raporlar, entegrasyonlar.

## Her adımda

`/sky-check` → yeşil → deploy → kısa not (`docs/progress.md`: ne yapıldı, ne ertelendi).
