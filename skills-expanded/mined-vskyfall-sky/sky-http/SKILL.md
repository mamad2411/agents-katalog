---
name: sky-http
description: >-
  HTTP ve web ağ temelleri (geliştirici gözüyle): istek/yanıt anatomisi, yöntemler ve
  idempotency, durum kodlarının doğru kullanımı, başlıklar (Cache-Control, ETag, Vary,
  Content-Type, CORS başlıkları), çerezler ve öznitelikleri, HTTP/2 ve HTTP/3, DNS kayıtları ve
  yayılım, TLS ve sertifikalar, yönlendirmeler, sıkıştırma, range istekleri, curl ile teşhis ve
  tarayıcı ağ sekmesini okuma. "CORS anlamadım", "cache neden çalışmıyor", "DNS", "SSL hatası",
  "hangi durum kodu" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · HTTP & Ağ

## Yöntemler

| Yöntem | Güvenli | Idempotent | Kullanım |
|---|---|---|---|
| GET | ✓ | ✓ | okuma (gövde yok, önbelleklenebilir) |
| HEAD | ✓ | ✓ | yalnızca başlıklar |
| POST | | | oluşturma, eylem |
| PUT | | ✓ | tam değiştirme |
| PATCH | | (değil) | kısmi güncelleme |
| DELETE | | ✓ | silme |
| OPTIONS | ✓ | ✓ | CORS preflight |
GET ile veri değiştirme yok (önbellekler, ön yükleyiciler, botlar tetikler).

## Durum kodları (doğru seç)

- **200** OK · **201** Created (+ `Location`) · **202** Accepted (işlem kuyruğa alındı) · **204** No Content
- **301** kalıcı (SEO taşınır) · **302/307** geçici (307 yöntemi korur) · **308** kalıcı + yöntem korur · **304** Not Modified
- **400** bozuk istek · **401** kimlik yok/geçersiz · **403** kimlik var, yetki yok · **404** yok (veya varlığını gizle) · **405** yöntem yok
- **409** çakışma (çift kayıt, sürüm) · **410** kalıcı olarak gitti · **412** ön koşul (If-Match) · **413** gövde büyük · **415** tür desteklenmiyor
- **422** doğrulama hatası · **429** çok istek (+ `Retry-After`)
- **500** beklenmeyen · **502** proxy arkası çöktü · **503** geçici olarak kullanılamaz (bakım) · **504** proxy zaman aşımı

## Önbellek başlıkları

```
Cache-Control: public, max-age=31536000, immutable        # hash'li statik
Cache-Control: public, s-maxage=300, stale-while-revalidate=86400   # CDN'de 5 dk, arka planda tazele
Cache-Control: private, no-cache                          # tarayıcı saklar ama her seferinde doğrular
Cache-Control: no-store                                   # hiç saklama (hassas)
ETag: "abc123"  →  If-None-Match: "abc123"  →  304
Vary: Accept-Encoding, Accept-Language                    # önbellek anahtarına dahil edilecek başlıklar
```
`no-cache` "saklama" demek değil, "doğrulamadan kullanma" demektir. Detay `sky-caching`.

## CORS (zihinsel model)

Tarayıcı, **farklı origin**'e (şema + host + port) yapılan isteğin yanıtını, sunucu izin vermedikçe JavaScript'e vermez.
- Basit olmayan istek (JSON gövde, `Authorization` başlığı, PUT/DELETE) önce `OPTIONS` **preflight** gönderir.
- Sunucu yanıtı: `Access-Control-Allow-Origin: https://app.site.com` (credentials varken `*` olmaz), `Allow-Methods`, `Allow-Headers`, `Allow-Credentials: true`, `Max-Age`.
- CORS bir **tarayıcı** korumasıdır; sunucu güvenliği değildir (curl CORS'u umursamaz). En kolay çözüm çoğu zaman aynı origin (proxy/rewrite).

## Çerezler

`Set-Cookie: sid=…; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=2592000`
- `HttpOnly` JS okuyamaz (XSS'te çalınmaz), `Secure` yalnızca HTTPS, `SameSite=Lax` çapraz site POST'larda gönderilmez (CSRF koruması), `None` + `Secure` çapraz site gerekiyorsa.
- `Domain` verilmezse yalnızca o host; `__Host-` öneki: Secure + Path=/ + Domain yok zorunlu (en güvenli).
- Üçüncü taraf çerezler tarayıcılarda kısıtlı — farklı alan adındaki API ile çerez oturumu kurmak yerine aynı üst alan adı (`api.site.com` + `app.site.com`) veya proxy.

## HTTP/2, HTTP/3

H2: tek bağlantıda çoklu akış (domain sharding ve sprite birleştirme gereksiz). H3: QUIC/UDP, kayıplı mobil ağlarda daha iyi.
CDN'ler otomatik sağlar; uygulama sunucusunun arkasında H1.1 olması normal.

## DNS

| Kayıt | Ne için |
|---|---|
| A / AAAA | ad → IPv4 / IPv6 |
| CNAME | ad → başka ad (apex'te kullanılamaz; ALIAS/ANAME/CNAME flattening) |
| MX | e-posta sunucusu |
| TXT | doğrulama, SPF, DKIM, DMARC |
| CAA | hangi CA sertifika verebilir |
| NS | yetkili ad sunucuları |
TTL: geçiş öncesi düşür (300), sonra yükselt. Yayılım "48 saat" değil, eski TTL kadardır. Kontrol: `dig +short app.site.com`, `dig @1.1.1.1 …`, `dig TXT _dmarc.site.com`.

## TLS

Let's Encrypt (90 gün, otomatik yenileme), tam zincir (ara sertifika) sunulmalı, TLS 1.2+; HSTS (bkz. `sky-security`).
Hata teşhisi: `openssl s_client -connect site.com:443 -servername site.com`, SSL Labs testi.
"Sertifika uyuşmazlığı" → yanlış alan adı veya SNI; "süresi dolmuş" → yenileme işi çalışmıyor; "güvenilmeyen" → eksik ara sertifika.

## curl ile teşhis

```bash
curl -I https://site.com                                   # yalnızca başlıklar
curl -sv https://site.com 2>&1 | grep -E "^[<>*]"          # TLS + istek/yanıt ayrıntısı
curl -X OPTIONS https://api.site.com/x -H "Origin: https://app.site.com" -H "Access-Control-Request-Method: POST" -i   # CORS preflight
curl -w "dns:%{time_namelookup} tls:%{time_appconnect} ttfb:%{time_starttransfer} total:%{time_total}\n" -o /dev/null -s https://site.com
curl -L --max-redirs 5 -I http://site.com                  # yönlendirme zinciri
```

## Tarayıcı ağ sekmesi

Durum, boyut (transfer vs kaynak), zamanlama (Queueing, DNS, TLS, TTFB, Content Download), başlatıcı (kim istedi), "(disk cache)" / "(memory cache)",
preflight satırları, engellenen istekler (CORS/CSP — Console'da açıklama). "Copy as cURL" ile sorunu terminalde tekrarla.
