---
name: sky-crypto
description: >-
  Uygulamalı kriptografi (geliştirici için, savunma amaçlı): parola saklama (argon2id/bcrypt),
  rastgelelik (kriptografik güvenli rastgele), hash ve HMAC (bütünlük, webhook imzası), simetrik
  şifreleme (AES-GCM, alan şifreleme), açık anahtar temelleri, JWT/PASETO doğru kullanımı, sabit
  zamanlı karşılaştırma, anahtar türetme ve yönetimi, TLS'e güven, yaygın hatalar ve "kendi
  kripton yok" kuralı. Parola, token, şifreleme, imza veya hash gerektiğinde kullan.
disable-model-invocation: true
---

# Sky · Uygulamalı Kriptografi

## Birinci kural: kendi kripton yok

Hazır, denetlenmiş kütüphaneleri doğru kullan; algoritma veya protokol tasarlama. Platformun yerleşik API'si (Web Crypto, Node `crypto`) + olgun kütüphaneler yeter.

## Parola saklama

```ts
import argon2 from "argon2";
const hash = await argon2.hash(password, { type: argon2.argon2id });   // tuz ve parametreler hash içinde
const ok = await argon2.verify(hash, password);
```
**argon2id** (tercih) veya **bcrypt** (cost ≥ 12) veya scrypt. Asla düz SHA-256/MD5 (hızlı = kırılabilir). Tuz otomatik. Uzunluk üst sınırı (bcrypt 72 byte) ve sızmış parola kontrolü (bkz. `sky-auth`).

## Rastgelelik

Token, oturum ID'si, davet kodu → **kriptografik** rastgele: `crypto.randomUUID()`, `crypto.getRandomValues(new Uint8Array(32))`, Node `crypto.randomBytes(32)`. `Math.random()` **asla** güvenlik için (tahmin edilebilir).

## Hash ve HMAC

- İçerik bütünlüğü/parmak izi: SHA-256.
- **Mesaj doğrulama / webhook imzası**: HMAC-SHA256 (paylaşılan gizli anahtarla) — "bu isteği gerçekten biz mi ürettik" (bkz. `sky-payments`, `sky-webhooks-out`).
- Doğrulamada **sabit zamanlı karşılaştırma**: `crypto.timingSafeEqual` / `crypto.subtle` — normal `===` zamanlama sızdırır.

## Simetrik şifreleme (duruşta)

```ts
// AES-256-GCM: her şifrelemede yeni iv, auth tag bütünlüğü sağlar
const iv = crypto.getRandomValues(new Uint8Array(12));
const ct = await crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, data);  // iv'yi ct ile sakla
```
Hassas alanlar (TC kimlik, sağlık notu, API anahtarı) için alan şifreleme; anahtar KMS/sır yöneticisinde (bkz. `sky-secrets`). IV/nonce **asla** aynı anahtarla tekrar kullanılmaz. Çoğu durumda DB/disk şifrelemesi (duruşta) + TLS (aktarımda) zaten yeterli — alan şifrelemeyi gerçekten gerektiğinde ekle.

## JWT ve token'lar

- İmzalı JWT yetki taşır ama **iptal edilemez** → kısa ömür (≤ 15 dk) + refresh; oturum için DB oturumu çoğu zaman daha iyi (bkz. `sky-auth`).
- `alg: none` kabul etme; algoritmayı sunucuda sabitle (`alg` karışıklığı saldırısı); `HS256` paylaşılan sır, `RS256/ES256` açık/özel anahtar.
- `exp`, `iss`, `aud` doğrula; hassas veri JWT payload'ında değil (base64, şifre değil).
- Daha güvenli varsayılanlar için **PASETO** iyi bir alternatif.

## Anahtar yönetimi

Anahtarlar sır yöneticisinde (bkz. `sky-secrets`), koda/Git'e gömülmez; rotasyon (çoklu aktif anahtar, `kid` ile); paroladan anahtar türetme gerekiyorsa argon2id/scrypt/PBKDF2 (yüksek iterasyon), düz hash değil.

## TLS

Aktarım güvenliği TLS'in işi — HTTPS her yerde, modern sürüm, HSTS (bkz. `sky-security`, `sky-http`). Uygulama seviyesinde "ekstra şifreleme" genelde gereksiz ve hatalı; TLS'e güven.

## Yaygın hatalar

| Hata | Doğrusu |
|---|---|
| Parola için SHA-256/MD5 | argon2id/bcrypt |
| `Math.random()` token | `crypto.randomBytes`/`randomUUID` |
| İmza doğrulamada `===` | sabit zamanlı karşılaştırma |
| ECB modu / sabit IV | AES-GCM + benzersiz IV |
| Sırrı koda gömme | sır yöneticisi |
| JWT'yi oturum gibi (iptal gerekir) kullanma | kısa ömür + refresh / DB oturumu |
| Kendi şifreleme protokolü | yerleşik, denetlenmiş kütüphane |
