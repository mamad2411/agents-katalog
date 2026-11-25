---
name: sky-secrets
description: >-
  Sır (secret) yönetimi uçtan uca: hangi bilgi sırdır, .env ve .env.example düzeni, geliştirici
  makinesinde sırlar (1Password CLI, Doppler, Infisical), CI/CD sırları ve OIDC ile anahtarsız
  erişim, bulut sır yöneticileri (AWS Secrets Manager, GCP Secret Manager, Key Vault, Vault),
  runtime'da yükleme, rotasyon ve iptal, sızıntı tespiti (gitleaks, secret scanning) ve sızıntı
  müdahale planı, ekip içi paylaşım ve ayrılan çalışan süreci. "API anahtarı nerede tutulmalı",
  ".env", "sır sızdı" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Sır Yönetimi

## Neler sırdır?

API anahtarları, veritabanı parolaları/URL'leri, JWT/oturum imza anahtarları, OAuth client secret'ları, webhook imza anahtarları, özel anahtarlar (TLS, SSH, imzalama), servis hesabı dosyaları, SMTP parolaları.
Sır **değil** (ama yine de dikkat): yayınlanabilir anahtarlar (Stripe publishable, Supabase anon, Firebase web config) — bunlar kurallarla korunur.

## Düzen

```
.env.example      # Git'te: tüm değişken adları, açıklama, sahte değer
.env.local        # Git'te DEĞİL: geliştiricinin kendi değerleri
```
`.gitignore`: `.env*` + `!.env.example`. Uygulama başlangıcında env doğrulama (bkz. `sky-web-stack` `lib/env.ts`) — eksik sır sessizce `undefined` olmasın.
İstemciye giden önekler (`NEXT_PUBLIC_`, `VITE_`, `EXPO_PUBLIC_`) asla sır taşımaz.

## Geliştirici makinesi

Sırları Slack/WhatsApp/e-postayla paylaşma. Seçenekler: **1Password** (`op run --env-file=.env.tpl -- pnpm dev` — referanslar `op://vault/item/field`), **Doppler** (`doppler run -- pnpm dev`), **Infisical** (açık kaynak), Bitwarden Secrets Manager. Herkes kendi erişimiyle, merkezi güncelleme, ayrılan kişinin erişimi tek tıkla kapanır.

## CI/CD

- Platform sırları (GitHub Actions secrets/environments) — ortama özel ve korumalı.
- Buluta erişim **OIDC** ile (uzun ömürlü erişim anahtarı yok — bkz. `sky-github-actions`).
- Loglarda maskeleme; sırları `echo` ile yazdırma; çatal PR'lara sır yok.

## Üretim

- Bulut sır yöneticisi (AWS Secrets Manager / SSM, GCP Secret Manager, Azure Key Vault) veya HashiCorp Vault / OpenBao; uygulama kimliğiyle (rol/managed identity) okunur.
- Platform env değişkenleri (Vercel, Fly, Railway) küçük projeler için yeterli; erişimi kişi bazlı.
- Konteyner imajına, Git'e, istemci paketine, log'a, hata raporuna sır girmez (bkz. `sky-observability` redact).

## Rotasyon

- Takvim (yılda bir / yüksek riskte 90 gün) ve olay bazlı (çalışan ayrılışı, sızıntı şüphesi).
- Kesintisiz döndürme: yeni anahtar oluştur → her iki anahtarı kabul et → uygulamaları yeni anahtara geçir → eskisini iptal et (webhook imza anahtarlarında, JWT'de `kid` ile çoklu anahtar).
- Veritabanı: dinamik kısa ömürlü kimlik bilgileri (Vault) veya IAM ile DB kimlik doğrulama.

## Sızıntı tespiti ve müdahale

Önleme: **gitleaks** pre-commit + CI, GitHub secret scanning + push protection, Sky `sky-quality` hook'u (gömülü anahtar kalıpları).
Sızdıysa (sırası önemli):
1. **Hemen döndür / iptal et** (geçmişten silmek yetmez — kopyalanmış olabilir).
2. Erişim loglarını incele (anahtar kötüye kullanıldı mı?).
3. Git geçmişinden temizle (`git filter-repo`), zorunlu push koordinasyonu.
4. Kök nedeni düzelt (neden commit'lendi?) ve olay kaydı (bkz. `sky-observability` runbook).
