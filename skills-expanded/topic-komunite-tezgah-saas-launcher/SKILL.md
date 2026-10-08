---
name: saas-launcher
description: >
  Sıfırdan production-ready bir SaaS uygulaması kur. Ödeme, kimlik doğrulama,
  veritabanı, e-posta, landing page, SEO ve API güvenliği dahil tüm katmanları
  kapsar. Kullanıcı SaaS kurmak, web uygulaması başlatmak, AI aracı oluşturmak
  veya online ürün çıkarmak istediğinde bu skill'i kullan — "startup kur",
  "proje başlat", "uygulama yap" gibi ifadeler dahil. Mevcut bir projeye
  tek bir katman eklemek (sadece ödeme, sadece auth vb.) için ilgili alt
  skill'e yönlendir.
---

# SaaS Launcher

Bu skill, bir SaaS uygulamasının sıfırdan production'a taşınmasını yöneten orkestratör skill'dir. Kendisi kod üretmez — kararları yönetir, sırayı belirler ve her katman için ilgili uzman skill'e yönlendirir.

## İlgili Skill'ler

Bu skill aşağıdaki uzman skill'lerle birlikte çalışır. Her biri bağımsız olarak da kullanılabilir:

- **saas-database** — Supabase veritabanı altyapısı, şema tasarımı ve RLS
- **saas-auth** — Kimlik doğrulama ve oturum yönetimi
- **saas-payments** — Ödeme sistemi ve abonelik yönetimi
- **saas-email** — Transactional e-posta ve DNS altyapısı
- **saas-storage** — Dosya depolama ve görsel yönetimi (opsiyonel)
- **saas-landing-seo** — Landing page stratejisi ve arama motoru optimizasyonu
- **saas-legal** — KVKK/GDPR uyumluluğu ve yasal sayfalar
- **saas-api-security** — API koruma, rate limiting ve input validation
- **saas-testing** — Test stratejisi ve kalite güvencesi
- **saas-analytics** — PostHog ile ürün analizi ve kullanıcı takibi
- **saas-deployment** — Production'a taşıma ve operasyonel hazırlık

---

## Faz 0: Keşif Görüşmesi

Hiçbir teknik karar almadan önce kullanıcıyla kapsamlı bir keşif görüşmesi yap. Bu görüşmenin amacı ürünü, hedef kitleyi ve teknik gereksinimleri netleştirmektir.

### Sorulması Gereken Sorular

**Ürün ve İş Modeli:**
- Uygulamanın temel işlevi ne? Bir cümleyle açıklayabilir misin?
- Hedef kitlen kim? (bireysel kullanıcı, küçük işletme, enterprise)
- Gelir modelin ne? (aylık abonelik, yıllık abonelik, tek seferlik ödeme, freemium, kullanım bazlı)
- Kaç farklı fiyat planı olacak?
- Ücretsiz deneme süresi olacak mı?

**Kullanıcı Deneyimi:**
- Kullanıcılar nasıl kayıt olacak? (Google ile giriş, e-posta/şifre, magic link, birden fazlası)
- Çok dilli destek gerekiyor mu?
- Hangi cihazlarda kullanılacak? (web, mobil web, native mobil)

**Teknik Tercihler:**
- Tercih ettiğin bir tech stack var mı? (framework, veritabanı, hosting)
- Mevcut kullandığın araçlar veya hesaplar var mı? (Stripe, Vercel, AWS vb.)
- Takım büyüklüğü? (solo founder, küçük takım, büyük ekip)

**Zaman ve Öncelik:**
- Ne kadar sürede launch etmek istiyorsun?
- MVP mi, tam ürün mü?
- Hangi özellikler Day 1 için zorunlu, hangileri sonra eklenebilir?

### Keşif Sonrası Çıktı

Keşif görüşmesi tamamlandığında kullanıcıya şu bilgileri özetle:
- Seçilen tech stack ve her seçimin gerekçesi
- Faz sıralaması ve tahmini zaman çizelgesi
- Day 1 özellik listesi vs. sonraya bırakılanlar
- Oluşturulması gereken dış hesaplar listesi (Stripe, Google Cloud Console, e-posta servisi, hosting vb.)

---

## Faz 1: Tech Stack Kararları

Her karar için kullanıcının cevaplarını, projenin ihtiyaçlarını ve ekosistem olgunluğunu tartarak bir öneri sun. Kullanıcı kararlarını zaten verdiyse doğrudan onayla ve ilerle.

### Framework Seçimi

Varsayılan önerimiz Next.js (App Router + TypeScript). Gerekçe: Server ve client rendering aynı projede, API route'ları dahili, React ekosistemi, Vercel ile sıfır sürtünme deployment. TypeScript her projede zorunlu olmalı — büyüdükçe tip güvenliği hayat kurtarır.

Alternatif değerlendirme noktaları:
- Nuxt.js, yalnızca kullanıcı Vue ekosistemine hakimse ve React öğrenme maliyeti kabul edilemezse
- SvelteKit, yalnızca çok küçük bundle boyutu kritikse
- Remix, yalnızca form-ağırlıklı uygulamalarda ve nested routing çok karmaşıksa

### Veritabanı Seçimi

Üç ana yol:

**Supabase (PostgreSQL)** — Varsayılan önerimiz. Auth, veritabanı, realtime ve storage tek çatı altında. Dashboard ile görsel yönetim. Ücretsiz katman cömert. En iyi seçim: çoğu SaaS projesi, özellikle solo founder'lar.

**MongoDB Atlas** — Şemasız esneklik gerektiren projeler için. Veri yapısı sık değişiyorsa veya iç içe doküman yapıları baskınsa. Mongoose ile hızlı prototipleme. En iyi seçim: içerik odaklı uygulamalar, kullanıcı tarafından oluşturulan yapılandırılmamış veri.

**Prisma + PostgreSQL** — Tip güvenli veritabanı sorguları, migration geçmişi, şema versiyonlaması. Railway veya Neon gibi managed PostgreSQL ile. En iyi seçim: birden fazla geliştiricinin çalıştığı projeler, karmaşık ilişkisel veri.

### Ödeme Seçimi

Detaylı karar rehberi için **saas-payments** skill'ine yönlendir. Kısa özet:

**Stripe** — Sektör standardı, en düşük komisyon (%2.9 + $0.30), en iyi dokümantasyon. Vergi yönetimi ayrıca yapılandırılmalı. Varsayılan önerimiz.

**Lemon Squeezy** — Merchant of Record modeli sayesinde KDV/vergi yönetimini platform halleder. Komisyon daha yüksek (%5 + $0.50) ama vergi sorumluluğu sıfır. Türkiye'den global satış yapıyorsan ciddi avantaj.

### E-posta Seçimi

Detaylı rehber için **saas-email** skill'ine yönlendir. Kısa özet:

**Resend** — Modern API, React Email ile güzel şablonlar, Next.js uyumu mükemmel. Varsayılan önerimiz.

**Mailgun** — Yüksek hacim, gelişmiş routing, inbound e-posta işleme gerektiren projeler için.

### Hosting Seçimi

Detaylı rehber için **saas-deployment** skill'ine yönlendir. Kısa özet:

**Vercel** — Next.js'in evi, sıfır konfigürasyon. Varsayılan önerimiz.

**Railway** — Veritabanı + backend + frontend tek platformda isteyenler için.

**Fly.io** — Global dağıtım ve container bazlı deployment isteyenler için.

---

## Faz 2: Temel Altyapı

İlk teknik adımlar. Bu fazda yapılacaklar:

1. **Proje iskeleti:** Seçilen framework ile proje oluştur. TypeScript, Tailwind CSS ve temel UI kütüphanesi (shadcn/ui önerilen) kurulumu. Klasör yapısını oluştur — route grupları, lib dizini, bileşen dizini, konfigürasyon dizini, tip tanımları.

2. **Ortam değişkenleri mimarisi:** `.env.local` yapısını kur. Her servise ait değişkenleri grupla ve açıklayıcı yorumlar ekle. `.env.local.example` şablonunu oluştur. `.gitignore`'a eklemeyi unutma.

3. **Veritabanı bağlantısı:** **saas-database** skill'ini aktive et. Supabase projesini oluştur, şemayı tasarla, RLS politikalarını kur, connection pooling'i yapılandır. Detaylı rehber **saas-database** skill'inde.

4. **Temel layout:** Kök layout dosyasını oluştur — font yükleme, metadata, SessionProvider. Public sayfa grubu (landing, login) ve korumalı sayfa grubu (dashboard) için route gruplarını ayır.

Bu faz tamamlandığında `npm run dev` ile çalışan, boş ama yapısal olarak sağlam bir proje olmalı.

---

## Faz 3: Kimlik Doğrulama

**saas-auth** skill'ini aktive et. Bu fazda:

- Seçilen auth stratejisini yapılandır (OAuth, Magic Link, e-posta/şifre veya kombinasyon)
- Giriş ve kayıt sayfalarını oluştur
- Korumalı route'lar için middleware kur
- Oturum bilgisini server ve client tarafında erişilebilir yap
- Kullanıcı modeliyle entegrasyonu sağla

Auth, diğer tüm katmanların temelini oluşturur. Ödeme sistemi kullanıcı kimliğine bağlıdır, e-posta gönderimi kullanıcı bilgisine bağlıdır, API koruması oturuma bağlıdır. Bu yüzden auth her zaman ödemeden önce tamamlanmalıdır.

---

## Faz 4: Ödeme Sistemi

**saas-payments** skill'ini aktive et. Bu fazda:

- Fiyat planlarını tanımla ve yapılandır
- Checkout akışını kur (kullanıcı → ödeme sayfası → başarı/iptal)
- Webhook handler'ı oluştur ve imza doğrulamayı uygula
- Abonelik yaşam döngüsünü yönet (başlangıç, yenileme, güncelleme, iptal, ödeme hatası)
- Müşteri portalı entegrasyonu
- Plan bazlı erişim kontrolü (hangi özellikler hangi plana ait)

Ödeme, SaaS'ın kalbidir. Webhook handler en kritik tek dosyadır — buradaki hatalar doğrudan gelir kaybına yol açar. Bu fazda acele etme.

---

## Faz 5: E-posta Altyapısı

**saas-email** skill'ini aktive et. Bu fazda:

- E-posta servisini yapılandır
- DNS kayıtlarını ayarla (SPF, DKIM, DMARC) — kullanıcıyı adım adım yönlendir
- Temel e-posta şablonlarını oluştur (hoş geldin, ödeme onayı, ödeme hatası)
- Magic Link kullanılıyorsa giriş e-postası şablonunu özelleştir

DNS ayarlarının yayılması 24-48 saat sürebilir. Bu yüzden e-posta fazını mümkün olduğunca erken başlat — en azından DNS kayıtlarını projenin ilk gününde ekle.

---

## Faz 6: Landing Page ve SEO

**saas-landing-seo** skill'ini aktive et. Bu fazda:

- Landing page akışını tasarla ve bileşenlerini oluştur
- SEO temellerini kur (metadata, sitemap, robots.txt, Open Graph)
- Performans optimizasyonu (görsel, font, bundle boyutu)
- İstenirse blog sistemi kur

Landing page ürünün vitrin yüzüdür. İlk izlenim burada oluşur. Fiyatlandırma bölümü Faz 4'teki plan tanımlarıyla uyumlu olmalı.

---

## Faz 6.5: Dosya Depolama (Opsiyonel)

Proje dosya yükleme gerektiriyorsa (profil fotoğrafları, kullanıcı dokümanları, görseller) **saas-storage** skill'ini aktive et. Bu fazda:

- Supabase Storage yapılandırması
- Dosya yükleme endpoint'leri ve güvenlik kontrolleri
- Görsel optimizasyonu
- Plan bazlı depolama limitleri

Her SaaS'ta gerekmez. Yalnızca dosya yükleme ihtiyacı varsa uygula.

---

## Faz 7: Yasal Uyumluluk

**saas-legal** skill'ini aktive et. Bu fazda:

- Gizlilik politikası sayfası oluştur (Google OAuth onayı için de gerekli)
- Kullanım koşulları sayfası oluştur
- KVKK aydınlatma metni hazırla
- Çerez onayı mekanizmasını kur
- Hesap silme akışını uygula

Yasal sayfalar landing page'in footer'ında yer almalı. Google OAuth onay ekranı gizlilik politikası URL'si gerektirir — bu yüzden auth'tan önce en azından taslak hazırla.

---

## Faz 8: API Güvenliği

**saas-api-security** skill'ini aktive et. Bu fazda:

- Rate limiting uygula
- Plan bazlı API koruması kur
- Input validation katmanını ekle
- Hata yönetimi standardize et
- Health check endpoint'i oluştur

Bu faz genellikle diğer fazların üstüne son bir güvenlik ve kalite katmanı olarak eklenir.

---

## Faz 9: Test

**saas-testing** skill'ini aktive et. Bu fazda:

- Vitest ile birim ve entegrasyon testleri kur
- Webhook handler testlerini yaz (en kritik test)
- Playwright ile E2E testler kur (auth ve checkout akışları)
- CI pipeline'a test adımlarını ekle

Deployment'tan önce en azından webhook handler ve auth akışı test edilmiş olmalı.

---

## Faz 10: Analytics

**saas-analytics** skill'ini aktive et. Bu fazda:

- PostHog entegrasyonunu kur
- Temel event tracking'i yapılandır (kayıt, giriş, checkout, özellik kullanımı)
- Kullanıcı tanımlama (identify) bağlantısını kur
- Dönüşüm hunisi ve temel dashboard'u oluştur
- Feature flag altyapısını kur (opsiyonel)

Analytics deployment ile paralel veya hemen sonrasında kurulabilir.

---

## Faz 11: Deployment

**saas-deployment** skill'ini aktive et. Bu fazda:

- Production ortamını hazırla
- Ortam değişkenlerini production değerleriyle güncelle
- Domain ve SSL yapılandır
- Ödeme sistemini live mode'a geçir
- DNS kayıtlarını tamamla
- Son doğrulama testlerini yap
- İzleme ve hata takibi kur

---

## Fazlar Arası Bağımlılıklar

```
Faz 0 (Keşif) → Faz 1 (Tech Stack)
                      ↓
                 Faz 2 (Altyapı + DB) ←── saas-database
                      ↓
                 Faz 3 (Auth) ←── Faz 5 (E-posta) gerektirebilir (Magic Link)
                      ↓
                 Faz 4 (Ödeme) ←── Auth tamamlanmış olmalı
                      ↓
                 Faz 5 (E-posta) ←── DNS kayıtları erken başlatılabilir
                      ↓
                 Faz 6 (Landing) ←── Fiyatlandırma bölümü Faz 4 ile uyumlu olmalı
                  ↓         ↓
     Faz 6.5 (Storage)  Faz 7 (Yasal) ←── Gizlilik politikası OAuth için de gerekli
                  ↓         ↓
                 Faz 8 (API Güvenliği)
                      ↓
                 Faz 9 (Test) ←── Deployment öncesi kalite güvencesi
                      ↓
                 Faz 10 (Analytics)
                      ↓
                 Faz 11 (Deployment) ←── Tüm fazlar tamamlanmış olmalı
```

**Paralel çalışabilecek fazlar:**
- DNS kayıtları (Faz 5'in bir parçası) Faz 2 ile paralel başlatılabilir
- Landing page tasarımı (Faz 6) Faz 4 ile paralel ilerleyebilir
- Google OAuth başvurusu (Faz 3'ün bir parçası) onay süreci nedeniyle erken başlatılmalı
- Yasal sayfalar (Faz 7) ve Storage (Faz 6.5) Landing ile paralel ilerleyebilir
- Analytics (Faz 10) Deployment ile paralel kurulabilir

---

## MVP vs. Tam Ürün Stratejisi

Eğer kullanıcı hızlı launch istiyorsa, MVP sırasını öner:

**MVP (Hafta 1):** Faz 0 + 1 + 2 + 3 + 4 + 7 (yasal taslak) + 11 — Çalışan auth, ödeme, gizlilik politikası taslağı ve boş dashboard. Landing page basit bir hero + pricing olabilir.

**İkinci Dalga (Hafta 2-3):** Faz 5 + 6 + 8 + 9 — Düzgün e-posta altyapısı, dönüşüm odaklı landing page, API güvenlik katmanı, temel testler.

**Üçüncü Dalga (Hafta 3-4):** Faz 6.5 + 10 — Dosya depolama (gerekiyorsa), analytics, feature flags.

**Sürekli İyileştirme:** Blog, A/B test, müşteri geri bildirimi döngüsü, yasal dokümanların hukukçu onayı.

---

## Genel Gotchas

- **Dış servis hesapları erken oluşturulmalı.** Google OAuth onay süreci, DNS yayılımı, Stripe account review — bunlar gün alabilir. İlk gün hesapları aç.
- **Environment variable disiplini.** `NEXT_PUBLIC_` prefix'i olmayan değişkenler client'ta görünmez. Hassas anahtarlar asla public prefix almamalı.
- **Webhook'lar SaaS'ın sinir sistemidir.** Ödeme webhook'u çalışmazsa para alırsın ama plan aktifleşmez. E-posta webhook'u çalışmazsa destek talepleri kaybolur. Webhook'ları test et, logla, izle.
- **Build test.** Her deployment'tan önce mutlaka build testi yap. Server-side render hataları sadece build sırasında ortaya çıkar.
- **Maliyet kontrolü.** Tüm servislerin ücretsiz katmanı var: Vercel, Supabase, Resend, Stripe (komisyon dışında ücret yok). İlk ödeme yapan müşteriye kadar $0/ay ile çalışabilirsin.
- **Güvenlik asla "sonra" yapılmaz.** Auth ve ödeme ilk günden doğru kurulmalı. "Şimdilik basit yapalım, sonra güvenliği ekleriz" cümlesi felaket reçetesidir.
