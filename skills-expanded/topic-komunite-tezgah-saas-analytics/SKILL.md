---
name: saas-analytics
description: >
  SaaS uygulaması için PostHog analytics ve ürün analizi kur. Event tracking,
  kullanıcı tanımlama, feature flag, session replay, funnel analizi ve
  gizlilik uyumlu yapılandırma. Bu skill'i kullanıcı analytics, PostHog,
  event tracking, kullanıcı davranışı, feature flag, A/B test, dönüşüm
  analizi veya metrik takibi ile ilgili bir şey istediğinde kullan.
  "Analytics kur", "kullanıcıları takip et", "PostHog ekle", "feature flag
  yap" gibi ifadeler tetikler.
---

# SaaS Analytics — PostHog ile Ürün Analizi

Bu skill, bir SaaS uygulamasının analitik katmanını kurar. Göremediğin şeyi iyileştiremezsin — kullanıcıların ürünü nasıl kullandığını, nerede takıldığını ve neden ayrıldığını anlamak büyümenin temelidir.

**Bağımlılık:** Bu skill **saas-launcher** orkestratör skill'inin deployment fazıyla birlikte veya sonrasında uygulanır. Bağımsız olarak da kullanılabilir.

**Bağlı skill'ler:**
- **saas-auth** — Kullanıcı kimliği analytics ile ilişkilendirilir.
- **saas-payments** — Gelir metrikleri ve dönüşüm hunileri.
- **saas-legal** — KVKK/GDPR uyumlu tracking yapılandırması.

---

## Neden PostHog

### Alternatiflerle Karşılaştırma

**PostHog vs. Google Analytics:**
- PostHog ürün analizi için tasarlanmış (event bazlı), GA pazarlama analizi için (sayfa görüntüleme bazlı)
- PostHog self-host edilebilir (veri sende kalır — KVKK avantajı)
- PostHog'da session replay, feature flag, A/B test dahili
- GA cookie consent gerektirir (GDPR), PostHog cookieless mode'da çalışabilir

**PostHog vs. Mixpanel:**
- PostHog açık kaynak, self-host seçeneği
- PostHog ücretsiz katmanı çok cömert (1M event/ay)
- Mixpanel'in analiz arayüzü daha olgun ama PostHog hızla yaklaşıyor

**PostHog vs. Plausible:**
- Plausible sadece sayfa analizi — event tracking, funnel, session replay yok
- Plausible gizlilik odaklı basit analitik için iyi ama SaaS ürün analizi için yetersiz

**Sonuç:** SaaS için PostHog en dengeli seçim — ürün analizi, feature flag ve session replay tek platformda.

---

## PostHog Kurulumu

### Cloud vs. Self-Host

**PostHog Cloud (önerilen başlangıç):** Kayıt ol, proje oluştur, API key al. Ücretsiz katman: aylık 1M event, 5K session recording, 1M feature flag değerlendirmesi.

**Self-host:** Docker Compose ile kendi sunucunda çalıştır. Avantaj: veri tamamen sende, KVKK endişesi sıfır. Dezavantaj: sunucu yönetimi, güncelleme sorumluluğu. Büyüdükçe veya yasal gereklilik varsa değerlendir.

### Next.js Entegrasyonu

PostHog'un resmi `posthog-js` kütüphanesini kur:

```
npm install posthog-js
```

**PostHog Provider oluştur:** Client component olarak bir provider yaz. App Router'da root layout'a ekle. Ortam değişkenleri:
- `NEXT_PUBLIC_POSTHOG_KEY` — proje API anahtarı (public)
- `NEXT_PUBLIC_POSTHOG_HOST` — PostHog instance URL'si (cloud için `https://us.i.posthog.com` veya `https://eu.i.posthog.com`)

**EU instance kullan.** Türkiye'den çalışıyorsan ve KVKK uyumluluğu önemliyse EU instance seç — veri Avrupa'da kalır.

### Server-Side Tracking

API route'ları ve server component'lerde event göndermek için `posthog-node` kütüphanesini kullan. Server-side tracking özellikle ödeme event'leri, webhook işlemleri ve arka plan görevleri için gerekli.

---

## Event Tracking Tasarımı

### İsimlendirme Kuralları

Tutarlı event isimlendirmesi kritiktir. Kaotik isimler analizi imkânsız kılar.

Format: `nesne_eylem` — küçük harf, alt çizgi ile ayır.
- `user_signed_up` (kayıt oldu)
- `plan_upgraded` (plan yükseltti)
- `project_created` (proje oluşturdu)
- `checkout_started` (ödeme başlattı)
- `checkout_completed` (ödeme tamamladı)

**Yapma:** `SignUp`, `user-sign-up`, `Signed Up`, `signup` — tutarsız isimlendirme analiz yapılmasını engeller.

### Temel Event'ler

Her SaaS'ta izlenmesi gereken event'ler:

**Dönüşüm hunisi:**
1. `page_viewed` (properties: path, referrer)
2. `signup_started` (kayıt formunu açtı)
3. `user_signed_up` (kayıt tamamlandı, properties: method — google/magic_link)
4. `checkout_started` (plan seçti, properties: plan, period)
5. `checkout_completed` (ödeme başarılı, properties: plan, amount)

**Ürün kullanımı:**
- `feature_used` (properties: feature_name)
- `project_created` / `project_deleted`
- `settings_updated`

**Ayrılma sinyalleri:**
- `plan_cancelled` (iptal etti)
- `plan_downgraded` (düşürdü)
- `account_deleted` (hesabı sildi)

### Property'ler

Her event'e bağlam ekleyen metadata:
- **Kullanıcı property'leri:** plan, kayıt tarihi, ülke
- **Event property'leri:** sayfa yolu, buton konumu, seçilen plan
- **Süper property'ler:** her event'e otomatik eklenen ortak veriler

---

## Kullanıcı Tanımlama

### Anonim → Tanımlı Geçiş

PostHog her ziyaretçiye anonim bir ID atar. Kullanıcı giriş yapınca `posthog.identify()` ile gerçek kimliğini bağla. Bu sayede giriş öncesi ve sonrası davranışlar tek profilde birleşir.

Identify çağrısında gönderilecek property'ler:
- email
- name
- plan
- created_at
- stripe_customer_id (opsiyonel)

**Identify'ı auth callback'inde yap.** Giriş başarılı olduktan sonra, dashboard'a yönlendirmeden önce.

### Group Analytics

Takım/organizasyon bazlı SaaS'larda kullanıcıları gruplara bağla. Bu sayede "şirket bazında kaç aktif kullanıcı var?" gibi soruları cevaplayabilirsin. Tek kullanıcılı SaaS'larda gerekmez.

---

## Feature Flags

### Neden PostHog Feature Flags

Ayrı bir feature flag servisi (LaunchDarkly, Flagsmith) yerine PostHog'un dahili feature flag'lerini kullan — ek maliyet yok, analytics ile doğal entegre, aynı dashboard'da yönetim.

### Kullanım Alanları

- **Kademeli rollout:** Yeni özelliği önce %10 kullanıcıya aç, sorun yoksa %100'e çıkar
- **Beta testi:** Belirli kullanıcılara veya planlara özel özellik erişimi
- **A/B testi:** İki farklı UI varyantını karşılaştır, dönüşüm oranlarını ölç
- **Kill switch:** Sorunlu özelliği anında kapat — deploy gerekmez

### Server-Side Flag Kontrolü

Feature flag'leri sadece UI'da değil, API route'larında da kontrol et. Client-side flag kontrolü UX içindir (UI'yı gizle/göster), güvenlik için server-side kontrol zorunludur — client-side kontrol bypass edilebilir.

---

## Session Replay

PostHog'un session replay özelliği kullanıcının ne yaptığını video olarak kaydeder. Hata raporlarını anlamak, UX sorunlarını tespit etmek ve kullanıcı davranışını gözlemlemek için güçlü araç.

### Gizlilik Ayarları

- Hassas input'ları otomatik maskele (şifre, kart bilgisi, kişisel veri)
- Belirli element'leri maskelemek için `data-posthog-mask` attribute'ü ekle
- KVKK uyumluluğu için session replay'i cookie consent'e bağla veya tamamen devre dışı bırak

**Dikkat:** Session replay çok veri tüketir. Ücretsiz planda 5K kayıt/ay — tüm trafiğe açarsan hızla tükenir. Sampling oranını düşür veya sadece belirli sayfalarda aktifleştir.

---

## Dashboard ve Metrikler

### Her SaaS'ın İzlemesi Gereken Metrikler

**Büyüme:**
- Haftalık/aylık kayıt sayısı (trend)
- Kayıt → aktifleşme oranı (ilk anlamlı aksiyonu yapan oran)
- Organik vs. referral vs. direkt trafik dağılımı

**Gelir:**
- MRR (Aylık Tekrarlayan Gelir)
- Yeni MRR vs. Churn MRR
- Plan dağılımı (free/starter/pro)
- Ortalama gelir per kullanıcı (ARPU)

**Etkileşim:**
- Günlük/haftalık/aylık aktif kullanıcı (DAU/WAU/MAU)
- Core feature kullanım sıklığı
- Oturum süresi ve derinliği

**Kayıp:**
- Churn oranı (aylık iptal / toplam abone)
- İptal öncesi davranış kalıpları
- İptal nedenleri (anket entegrasyonu)

### PostHog Dashboard Oluşturma

Dashboard'da insight'lar oluştur: trend grafikleri, huniler (funnel), tutma analizi (retention), kullanıcı yolculukları (paths). Takım ile paylaş ve haftalık gözden geçirme ritüeli oluştur.

---

## Gotchas

- **Event spam'i:** Her tıklamayı ve fare hareketini izleme. Sadece anlamlı aksiyonları event olarak gönder — aksi halde event kotanı gereksiz tüketirsin.
- **Gizlilik yasaları:** KVKK ve GDPR, kullanıcı verisi toplamadan önce bilgilendirme gerektirir. En azından gizlilik politikasında analytics kullanımını belirt. Cookie consent gerekiyorsa PostHog'un cookieless mode'unu değerlendir.
- **Adblocker'lar PostHog'u engeller.** Kullanıcıların %20-30'u adblocker kullanır. Server-side tracking ile tamamla veya PostHog'un reverse proxy yöntemini kullan.
- **Development event'lerini ayır.** Development ortamındaki event'ler production verisini kirletir. Ayrı PostHog projesi veya environment filtresi kullan.
- **Çok fazla dashboard, az aksiyon.** Dashboard oluşturmak kolay, insight'ı aksiyona dönüştürmek zor. Her metrik için "bu düşerse/yükselirse ne yapacağız?" sorusunu cevapla.
- **Identify'dan önce event gönderme.** Kullanıcı giriş yaptıktan sonra önce `identify()`, sonra event gönder. Sıra yanlışsa event'ler anonim kalır ve profille birleşmez.
