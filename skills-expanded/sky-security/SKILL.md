---
name: sky-security
description: >-
  Derin uygulama güvenliği: tehdit modelleme (STRIDE kısaca), OWASP Top 10 denetim rehberi,
  Content-Security-Policy yazma (nonce, strict-dynamic, rapor modu), güvenlik başlıkları seti,
  IDOR/yetki açıkları avı, SSRF, XSS ve CSRF örnekleri, bağımlılık ve tedarik zinciri güvenliği,
  sır yönetimi ve rotasyonu, şifreleme (at rest/in transit, alan bazlı), güvenlik testleri ve
  sızma testi öncesi kontrol listesi, güvenlik açığı bildirimi (security.txt). "Güvenlik
  denetimi", "CSP", "hacklenir mi", "pentest öncesi" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Güvenlik

Temel kurallar `sky-backend-api` ve `sky-auth`'ta. Bu skill **denetim ve sertleştirme** içindir.

## 30 dakikalık tehdit modeli

Her yeni özellik için 4 soru:
1. **Varlıklar**: neyi koruyoruz? (kişisel veri, ödeme, hesap, itibar)
2. **Giriş noktaları**: form, API, webhook, dosya yükleme, URL parametresi, üçüncü parti.
3. **Kim saldırır**: anonim, kayıtlı kullanıcı, başka kiracı, kötü niyetli çalışan, ele geçirilmiş bağımlılık.
4. **Ne ters gidebilir** (STRIDE): kimlik taklidi, veri değiştirme, inkâr, bilgi sızıntısı, hizmet engelleme, yetki yükseltme.
Her riske bir kontrol ve bir test eşle.

## OWASP Top 10 hızlı denetim

| Risk | Nerede ara | Kontrol |
|---|---|---|
| Kırık erişim kontrolü (IDOR) | `/:id` alan her uç nokta, server action | sahiplik/org kontrolü, 404 |
| Kriptografik hatalar | parola, token, PII saklama | argon2id, rastgele token hash'li, TLS |
| Enjeksiyon | ham SQL, `exec`, şablon | parametreli sorgu, izinli liste |
| Güvensiz tasarım | iş akışları | tehdit modeli, rate limit, onay adımları |
| Yanlış yapılandırma | başlıklar, CORS, debug, varsayılan şifreler | başlık seti, `NODE_ENV=production` |
| Zayıf bileşenler | `package.json` | audit, Renovate, kilit dosyası |
| Kimlik doğrulama hataları | giriş, sıfırlama, oturum | `sky-auth` kontrol listesi |
| Bütünlük hataları | CI, webhook, güncellemeler | imza doğrulama, korumalı branch |
| Log/izleme eksikliği | auth olayları | audit log, alarm |
| SSRF | URL alan fetch'ler (önizleme, webhook, görsel içe aktarma) | izinli şema/host, iç IP engeli |

## CSP (Content-Security-Policy)

Next.js'te nonce'lu katı politika (proxy/middleware'de üret):
```
default-src 'self';
script-src 'self' 'nonce-{NONCE}' 'strict-dynamic';
style-src 'self' 'unsafe-inline';
img-src 'self' blob: data: https://cdn.site.com;
font-src 'self';
connect-src 'self' https://*.ingest.sentry.io https://api.site.com;
frame-ancestors 'none'; base-uri 'self'; form-action 'self'; object-src 'none';
upgrade-insecure-requests;
```
- Önce `Content-Security-Policy-Report-Only` + rapor uç noktası ile 1 hafta izle, sonra uygula.
- Üçüncü parti scriptler (analitik, chat widget) CSP'yi deler — gerçekten gerekli mi sor.

## Başlık seti

`Strict-Transport-Security: max-age=63072000; includeSubDomains; preload` · `X-Content-Type-Options: nosniff` ·
`Referrer-Policy: strict-origin-when-cross-origin` · `Permissions-Policy: camera=(), microphone=(), geolocation=(self)` ·
`Cross-Origin-Opener-Policy: same-origin`. Test: securityheaders.com, Mozilla Observatory (hedef A+).

## IDOR avı (en sık ciddi açık)

Grep: `params.id`, `searchParams.get("id")`, `findUnique({ where: { id } })`, server action'larda gelen `id`.
Her biri için: "Bu ID başka kullanıcınınsa ne olur?" Otomatik test: iki kullanıcı oluştur, A'nın kaynağına B ile istek → 404 beklenir.

## Tedarik zinciri

- Kilit dosyası commit'li, CI'da `--frozen-lockfile`.
- Yeni paket eklemeden önce: indirme sayısı, bakım, yaş, typo-squat (Sky `pre-bash` hook'u uyarır).
- `npm audit --omit=dev` yüksek/kritik = 0; Renovate/Dependabot; Socket.dev gibi davranış taraması.
- `postinstall` scriptli paketlere dikkat; CI'da gereksizse `--ignore-scripts`.
- GitHub Actions'ı commit SHA ile sabitle; `GITHUB_TOKEN` izinleri minimum.

## Sırlar

- Repoda sır yok: `gitleaks` pre-commit + CI. Sızdıysa: **önce döndür**, sonra geçmişten temizle.
- Sır rotasyon takvimi (yılda bir veya personel değişiminde); döndürme runbook'u.
- Prod sırlarına erişim kişi bazlı ve loglu.

## Şifreleme

- Aktarımda: her yerde TLS; DB bağlantısı `sslmode=require`.
- Duruşta: yönetilen DB/depolama zaten şifreler; **hassas alanlar** (TC kimlik, sağlık notu, IBAN) için ayrıca
  uygulama seviyesinde alan şifreleme (AES-256-GCM, anahtar KMS'te), aranabilirlik için ayrı hash sütunu.

## Test ve sızma testi öncesi

- [ ] Yetki matrisi testleri (her rol × her uç nokta)
- [ ] OWASP ZAP baseline taraması staging'de
- [ ] Rate limit'ler çalışıyor (giriş, OTP, API)
- [ ] Hata sayfalarında stack trace yok; `X-Powered-By` kapalı
- [ ] Dosya yükleme kötü dosya testleri (SVG script, çift uzantı, büyük dosya)
- [ ] Oturum: çıkış her yerde geçersiz kılıyor, çerez bayrakları doğru
- [ ] `/.well-known/security.txt` (iletişim, politika) — araştırmacılar nereye yazacağını bilsin
