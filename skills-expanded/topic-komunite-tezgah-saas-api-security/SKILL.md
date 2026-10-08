---
name: saas-api-security
description: >
  SaaS uygulaması için API güvenlik katmanı kur. Rate limiting, plan bazlı
  erişim kontrolü, input validation, hata yönetimi, CORS ve health check.
  Bu skill'i kullanıcı API güvenliği, rate limiting, yetkilendirme, input
  doğrulama, hata yönetimi veya API koruması ile ilgili bir şey istediğinde
  kullan. "API'yi koru", "rate limit ekle", "plan kontrolü yap", "input
  validation" gibi ifadeler tetikler.
---

# SaaS API Security — Güvenlik ve Kalite Katmanı

Bu skill, bir SaaS uygulamasının API katmanını güvenlik, dayanıklılık ve kalite açısından sağlamlaştırır. Diğer katmanların (auth, payments) üzerine son bir koruma ve kalite katmanı olarak eklenir.

**Bağımlılık:** Bu skill **saas-launcher** orkestratör skill'inin Faz 7'sidir. Bağımsız olarak da kullanılabilir.

**Bağlı skill'ler:**
- **saas-auth** — Oturum bilgisi API korumasının temelini oluşturur.
- **saas-payments** — Plan bilgisi erişim kontrolü kararlarını belirler.

---

## Güvenlik Katmanları Mimarisi

Bir API isteği geldğinde sırasıyla şu katmanlardan geçmelidir:

```
İstek geldi
  → 1. Rate Limiting (çok fazla istek mi?)
    → 2. Authentication (kim bu?)
      → 3. Authorization (bu işlemi yapma yetkisi var mı? Planı uygun mu?)
        → 4. Input Validation (gönderdiği veri geçerli mi?)
          → 5. İş Mantığı (asıl işlem)
            → 6. Hata Yönetimi (bir şeyler ters giderse)
              → Cevap döndür
```

Her katman bağımsızdır ve ihlal durumunda sonraki katmanlara geçmeden isteği reddeder.

---

## 1. Rate Limiting

### Neden Gerekli

Rate limiting olmadan:
- Bir kullanıcı (veya bot) saniyede binlerce istek göndererek sunucunu çökertebilir (DDoS)
- Brute force saldırıları giriş sayfasını hedef alabilir
- API'ni bedava kullanan biri kaynaklarını tüketebilir
- Ödeme webhook endpoint'in dışarıdan spam'lanabilir

### Strateji

Rate limit'i iki seviyede uygula:

**Global seviye (IP bazlı):** Tüm endpoint'lere uygula. Saniyede veya dakikada belirli sayıda istek. Amaç: DDoS ve brute force koruması.

**Endpoint seviyesi (kullanıcı bazlı):** Hassas endpoint'lere ayrıca uygula — login denemesi, checkout oluşturma, e-posta gönderimi. Amaç: kaynakların adil kullanımı.

### Serverless Ortamda Rate Limiting

Serverless ortamlarda (Vercel, Netlify) her istek ayrı bir process'te çalışır. Bu yüzden in-memory rate limiting (bellekte sayaç tutma) çalışmaz — her process kendi belleğine sahiptir, sayaçlar paylaşılmaz.

Çözüm: Dış bir veri deposu kullan. Upstash Redis serverless ortamlar için optimize edilmiş managed Redis servisidir. HTTP üzerinden çalışır (TCP bağlantısı gerektirmez), her istekte sayacı Redis'te tutar. Ücretsiz katmanı çoğu erken SaaS için yeterlidir.

Basit proje veya MVP'de Upstash bile fazlaysa: rate limiting'i atla ve production'da ihtiyaç ortaya çıkınca ekle. Ama login endpoint'i ve webhook endpoint'i için en azından basit bir koruma koy.

### Rate Limit Yanıtı

Limit aşıldığında HTTP 429 (Too Many Requests) döndür. Yanıtta şu bilgileri header olarak ekle:
- Toplam limit (X-RateLimit-Limit)
- Kalan hak (X-RateLimit-Remaining)
- Sıfırlanma zamanı (X-RateLimit-Reset)

Kullanıcı dostu hata mesajı: "Çok fazla istek gönderildi. Lütfen birkaç saniye bekleyip tekrar deneyin."

---

## 2. Authentication Kontrolü

Bu katman **saas-auth** skill'inin kurduğu oturum sistemini tüketir.

Her korumalı API endpoint'inde oturum kontrolü yap:
- Oturum yoksa → 401 Unauthorized döndür
- Oturum geçersiz veya süresi dolmuşsa → 401 döndür
- Oturum geçerliyse → kullanıcı bilgisini sonraki katmana aktar

Middleware ile genel koruma zaten yapılmış olmalı (bkz. **saas-auth**). API route seviyesinde ek kontrol, middleware'in kapsamadığı edge case'ler için güvenlik ağıdır.

---

## 3. Authorization — Plan Bazlı Erişim Kontrolü

Authentication "kim bu?" sorusunu cevaplar. Authorization "bu kişi bu işlemi yapabilir mi?" sorusunu cevaplar.

### Plan Hiyerarşisi

Plan'ları bir hiyerarşi olarak tanımla: free < starter < pro < enterprise. Her API endpoint'i minimum bir plan seviyesi gerektirir. Kullanıcının planı gereken seviyenin altındaysa 403 Forbidden döndür.

403 yanıtı kullanıcı dostu olmalı:
- Mevcut plan bilgisi
- Gereken plan bilgisi
- Yükseltme URL'si (fiyatlandırma sayfasına link)

### Plan Kontrol Noktaları

Sadece API route'larda değil, şu noktalarda da plan kontrolü yap:
- **UI seviyesinde:** Üst plan gerektiren özellikleri görsel olarak kilitle (kilit ikonu, "Pro planı gerektirir" etiketi). Bu UX'tir, güvenlik değil — gerçek kontrol her zaman server-side'da.
- **API seviyesinde:** Her korumalı endpoint'te plan kontrolü. Bu gerçek güvenlik katmanıdır.
- **Kaynak limitleri:** "5 projeye kadar" gibi limitleri yeni kaynak oluşturma endpoint'lerinde kontrol et.

### Kullanım Bazlı Limitler

Bazı planlar aylık API çağrısı veya işlem limiti içerir. Bu limitleri takip et:
- Her API çağrısında sayacı artır
- Limite yaklaşıldığında uyarı header'ı ekle
- Limit aşıldığında 429 döndür (rate limit'ten farklı — bu plan limiti)
- Sayacı her ayın başında sıfırla

---

## 4. Input Validation

### Neden Kritik

Kullanıcıdan gelen her veri potansiyel olarak kötü niyetlidir. Doğrulanmamış input:
- SQL Injection (veritabanı manipülasyonu)
- XSS (zararlı script enjeksiyonu)
- Tip hataları (string beklerken nesne gelirse çökme)
- İş mantığı hataları (negatif miktar, çok uzun metin)

### Validation Stratejisi

Zod gibi bir şema doğrulama kütüphanesi kullan. Her API endpoint'inin kabul ettiği veriyi bir şema olarak tanımla. Gelen veriyi bu şemadan geçir — geçersizse 400 Bad Request döndür, geçerliyse tip güvenli veri ile devam et.

Doğrulama şemasında tanımlanması gerekenler:
- Her alanın tipi (string, number, boolean, enum)
- Zorunlu/opsiyonel alanları
- Uzunluk/boyut sınırları (max 100 karakter, max 5MB)
- Format kuralları (e-posta formatı, URL formatı)
- Değer aralıkları (min: 0, max: 100)
- İzin verilen değerler (enum: ["free", "starter", "pro"])

### Hata Yanıt Formatı

Validation hatası yanıtı hangi alanın neden geçersiz olduğunu açıkça belirtmeli:

```
{
  "error": "Geçersiz veri",
  "details": [
    { "field": "email", "message": "Geçerli bir e-posta adresi gerekli" },
    { "field": "name", "message": "En fazla 100 karakter olmalı" }
  ]
}
```

Bu format hem insan tarafından okunabilir hem de client tarafından programatik olarak işlenebilir.

---

## 5. Hata Yönetimi

### İlke: Kullanıcıya Yardımcı Ol, Saldırgana Bilgi Verme

Hata mesajları iki kitleye hitap eder:
- **Meşru kullanıcılar:** Ne yanlış gittiğini ve ne yapması gerektiğini anlamalı
- **Kötü niyetli aktörler:** Sistem hakkında bilgi edinmemeli

Bu denge:
- Validation hataları → detaylı (kullanıcıya yardımcı)
- İş mantığı hataları → açıklayıcı ama teknik detaysız
- Sunucu hataları → genel mesaj ("Bir şeyler yanlış gitti"), detay sadece log'da

### Hata Kategorileri ve HTTP Kodları

| Kod | Anlam | Ne Zaman | Mesaj Detayı |
|-----|-------|----------|--------------|
| 400 | Bad Request | Input validation hatası | Detaylı (hangi alan, neden) |
| 401 | Unauthorized | Oturum yok veya geçersiz | "Giriş yapmanız gerekiyor" |
| 403 | Forbidden | Plan yetersiz veya yetki yok | Plan bilgisi + yükseltme linki |
| 404 | Not Found | Kaynak bulunamadı | "Kaynak bulunamadı" |
| 409 | Conflict | Çakışma (duplicate) | "Bu kaynak zaten mevcut" |
| 429 | Too Many Requests | Rate limit aşıldı | Bekleme süresi bilgisi |
| 500 | Internal Server Error | Beklenmeyen hata | Genel mesaj, detay log'da |

### Loglama

Production'da console.log yeterli değildir. Bir loglama servisi kullan (Sentry, LogSnag, Axiom, Vercel Log Drain). Her 500 hatasında:
- Hata mesajı ve stack trace
- İstek URL'si, metodu, body'si
- Kullanıcı ID'si (varsa)
- Zaman damgası

Sentry özellikle önerilir — hataları gruplar, trend gösterir, alert gönderir.

---

## 6. CORS (Cross-Origin Resource Sharing)

### Ne Zaman Gerekli

Eğer API'ni sadece kendi frontend'in kullanıyorsa (Next.js full-stack) CORS yapılandırması gerekmez — aynı origin'den gelir.

CORS gerekli durumlar:
- API'ni başka domain'lerden erişilebilir yapıyorsan (public API)
- Mobil uygulama API'ni kullanıyorsa
- Üçüncü taraf entegrasyonlar API'ne istek gönderiyorsa

### CORS Yapılandırma İlkeleri

- Wildcard (`*`) kullanma — sadece güvenilen origin'leri listele
- İzin verilen HTTP methodlarını sınırla (GET, POST — gereksiz PUT, DELETE açma)
- Preflight isteklerine (OPTIONS) doğru yanıt ver
- Credentials (cookie) gerektiren isteklerde `Access-Control-Allow-Credentials: true` ekle

---

## 7. Health Check Endpoint

Her SaaS'ın `/api/health` endpoint'i olmalı. Bu endpoint:
- Uygulamanın çalıştığını doğrular
- Opsiyonel: veritabanı bağlantısını kontrol eder
- Uptime monitoring servisleri (BetterStack, UptimeRobot) tarafından düzenli aralıklarla çağrılır
- CI/CD pipeline'larında deployment sonrası doğrulama için kullanılır

Yanıt: status (ok/degraded), timestamp, uptime. Veritabanı bağlantısı yoksa "degraded" dön ama 200 döndür (uygulama çalışıyor, DB bağlantısı yok).

---

## Güvenlik Kontrol Listesi

- Rate limiting tüm public endpoint'lerde aktif mi?
- Login endpoint'inde brute force koruması var mı?
- Auth kontrolü tüm private endpoint'lerde yapılıyor mu?
- Plan kontrolü ücretli özellikler için uygulanıyor mu?
- Input validation tüm POST/PUT endpoint'lerinde var mı?
- Hata mesajları hassas bilgi sızdırmıyor mu? (stack trace, DB detayları, dosya yolları)
- Ortam değişkenleri `NEXT_PUBLIC_` olmadan server-side'da kalıyor mu?
- Webhook endpoint'lerinde imza doğrulama var mı? (bkz. **saas-payments**)
- CORS sadece gerekli endpoint'lerde açık mı?
- Error tracking (Sentry vb.) kurulu mu?

---

## Gotchas

- **Rate limit serverless'ta in-memory çalışmaz.** Her function invocation ayrı process. Upstash Redis veya benzeri dış çözüm gerekir.
- **IP tespiti proxy arkasında.** Vercel veya Cloudflare arkasında gerçek client IP `x-forwarded-for` header'ındadır. Doğrudan `req.ip` güvenilir olmayabilir.
- **Plan kontrolü UI'da yeterli değil.** Client-side plan kontrolü UX içindir (butonu kilitle, mesaj göster). Asıl kontrol server-side'da olmalı — client-side kontrol kolayca bypass edilir.
- **Validation sadece API'de değil.** Client tarafında da validation yap (UX için — hızlı geri bildirim), ama güvenlik için server-side validation zorunlu. Client-side validation bypass edilebilir.
- **500 hatasında detay verme.** "Internal server error: MongoDB connection timeout at line 42" gibi mesajlar saldırgana veritabanı türünü ve yapısını ifşa eder. Kullanıcıya "Bir şeyler yanlış gitti" de, detayı logla.
- **Hata tracking kurulmadan launch yapma.** Kullanıcılar hata raporlamaz — sessizce giderler. Sentry veya benzeri bir araç yoksa hataları asla öğrenemezsin.
- **Health check endpoint'i auth'a bağlama.** Monitoring servisleri auth token göndermez. Health check public ve lightweight olmalı.
