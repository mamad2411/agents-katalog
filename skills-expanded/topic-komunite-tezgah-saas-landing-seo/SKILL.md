---
name: saas-landing-seo
description: >
  SaaS uygulaması için dönüşüm odaklı landing page tasarla ve arama motoru
  optimizasyonu (SEO) kur. Hero, pricing, FAQ, testimonials gibi bileşenler,
  metadata, sitemap, robots.txt, Open Graph, yapısal veri ve blog sistemi.
  Bu skill'i kullanıcı landing page, ana sayfa, fiyatlandırma sayfası, SEO,
  sitemap, Open Graph, blog veya "daha fazla müşteri çekmek" istediğinde
  kullan. "Güzel bir ana sayfa yap", "SEO ayarla", "pricing section ekle",
  "blog kur" gibi ifadeler tetikler.
---

# SaaS Landing & SEO — Dönüşüm ve Keşfedilebilirlik

Bu skill, bir SaaS uygulamasının vitrin yüzünü (landing page) ve arama motorlarında keşfedilebilirliğini (SEO) kurar. Landing page'in tek amacı ziyaretçiyi ödeme yapan müşteriye dönüştürmektir. SEO'nun amacı bu ziyaretçilerin organik olarak gelmesini sağlamaktır.

**Bağımlılık:** Bu skill **saas-launcher** orkestratör skill'inin Faz 6'sıdır. Bağımsız olarak da kullanılabilir.

**Bağlı skill'ler:**
- **saas-payments** — Fiyatlandırma bölümü ödeme skill'indeki plan tanımlarıyla aynı kaynaktan beslenmeli.
- **saas-auth** — CTA butonları giriş yapmamış kullanıcıları auth akışına yönlendirir.

---

## BÖLÜM 1: LANDING PAGE

### Sayfa Akış Mimarisi

Kanıtlanmış SaaS landing page yapısı, yukarıdan aşağıya doğru şu sırayı takip eder. Her bileşenin sayfadaki konumu rastgele değildir — psikolojik bir amaca hizmet eder.

**1. Navbar**
Amacı: Navigasyon ve sürekli erişilebilir CTA.
İçerik: Logo (sol), navigasyon linkleri (orta), CTA butonu (sağ, "Ücretsiz Dene" veya "Giriş Yap"). Scroll'da sticky olmalı — kullanıcı sayfanın neresinde olursa olsun CTA'ya erişebilmeli. Mobilde hamburger menü.

**2. Hero**
Amacı: İlk 5 saniyede ne olduğunu, kimin için olduğunu ve neden önemli olduğunu anlatmak.
İçerik: Ana başlık (değer önerisi, fayda odaklı — ne yaptığını değil ne sağladığını söyle), alt açıklama (1-2 cümle), birincil CTA butonu, opsiyonel ürün ekran görüntüsü veya demo. Küçük güven göstergesi: "Kredi kartı gerektirmez" veya "14 gün ücretsiz dene".

Başlık formülleri:
- "[Sonuç] + [kolaylık/hız]" — "İlk müşterini 24 saatte bul"
- "[Problem]'e son ver" — "E-posta kaosuna son ver"
- "[Hedef kitle] için [çözüm]" — "Freelancer'lar için proje yönetimi"
- "[Eski yol] değil, [yeni yol]" — "Spreadsheet'ler değil, akıllı dashboard'lar"

**3. Sosyal Kanıt Bandı**
Amacı: "Başkaları da kullanıyor" güveni oluşturmak.
İçerik: Müşteri sayısı ("500+ şirket tarafından kullanılıyor"), müşteri logoları (grayscale, aynı yükseklikte), veya rakamlar (aktif kullanıcı, uptime, müşteri puanı). Henüz müşterin yoksa: beta kullanıcı sayısı, waitlist sayısı veya bu bölümü atla.

**4. Problem/Çözüm**
Amacı: Kullanıcının hissettiği acıyı tanımlamak ve çözümü sunmak.
İçerik: "Bunu yaşıyorsun değil mi?" duygusu. Mevcut yöntemlerin zorluğunu anlat, ardından senin çözümünün bunu nasıl ortadan kaldırdığını göster. Empati kurarak yaz — kullanıcı kendini tanımalı.

**5. Özellikler**
Amacı: Ne sunduğunu somut şekilde göstermek.
İçerik: 3-6 ana özellik, her biri ikon + başlık + kısa açıklama. Teknik jargon değil, fayda dili kullan: "Yapay zeka motorumuz" yerine "Müşteri kaybını 3 gün önceden tahmin et". İstenirse her özellik için detay sayfasına link.

**6. Nasıl Çalışır (Opsiyonel)**
Amacı: Karmaşık ürünlerde süreçi basitleştirmek.
İçerik: 3 adım, numaralandırılmış. "1. Kaydol → 2. Veri bağla → 3. Sonuçları gör". Adım sayısı 3'ü geçmemeli — 3'ten fazlaysa basitleştir veya bu bölümü atla.

**7. Fiyatlandırma**
Amacı: Fiyat bilgisini şeffaf sunmak ve satın alma kararını kolaylaştırmak.
İçerik: Plan kartları yan yana, özellik karşılaştırması, aylık/yıllık toggle, "En Popüler" etiketi, CTA butonu her kartta. Fiyatlandırma verileri **saas-payments** skill'indeki plan konfigürasyonuyla aynı kaynaktan gelmeli.

Tasarım kuralları:
- Yıllık planı vurgula (tasarruf yüzdesini göster)
- En popüler planı görsel olarak öne çıkar (kenarlık, etiket, gölge)
- Her planın altında özellik listesi — check işaretiyle
- Ücretsiz deneme veya money-back guarantee varsa belirt

**8. SSS (FAQ)**
Amacı: Satın alma öncesi itirazları gidermek.
İçerik: 4-8 soru-cevap, accordion formatında. Mutlaka cevaplanması gereken sorular:
- Ücretsiz deneme nasıl çalışır?
- İstediğim zaman iptal edebilir miyim?
- Verilerim güvende mi?
- Hangi ödeme yöntemlerini kabul ediyorsunuz?

**9. Testimonials / Müşteri Yorumları**
Amacı: Sosyal kanıt derinleştirmek, güven inşa etmek.
İçerik: 3-6 gerçek müşteri yorumu. Her biri: alıntı, isim, unvan/şirket, fotoğraf. Spesifik yorumlar etkili: "Harika araç" değil, "İlk ayda %40 dönüşüm artışı sağladık". Henüz müşterin yoksa: beta kullanıcı geri bildirimleri veya bu bölümü atla.

**10. Son CTA**
Amacı: Sayfayı güçlü bir aksiyonla bitirmek.
İçerik: Büyük başlık ("Bugün başla"), kısa tekrar değer önerisi, CTA butonu. Sayfanın sonuna kadar okuyan ziyaretçi yüksek niyetlidir — onu kaçırma.

**11. Footer**
İçerik: Logo, kısa açıklama, navigasyon linkleri, yasal linkler (gizlilik politikası, kullanım koşulları), sosyal medya ikonları, copyright.

---

## BÖLÜM 2: SEO

### Teknik SEO Temelleri

#### Metadata

Her sayfanın benzersiz title ve description'ı olmalı.

Title kuralları: Ana anahtar kelimeyi başa yaz, marka adını sona koy. 50-60 karakter. Format: "Sayfa Başlığı | Marka Adı". Alt sayfalar template kullanmalı.

Description kuralları: Sayfanın ne sunduğunu ve neden tıklanması gerektiğini anlat. 150-160 karakter. CTA içermeli: "Ücretsiz deneyin", "Hemen başlayın".

#### Sitemap

Dinamik sitemap dosyası oluştur — framework'ün sitemap üretme özelliğini kullan. İçermesi gerekenler:
- Tüm public sayfalar (landing, pricing, blog yazıları)
- Her sayfanın son güncelleme tarihi
- Değişim sıklığı (monthly, weekly)
- Öncelik (homepage: 1.0, blog: 0.6)

İçermemesi gerekenler: Dashboard sayfaları, API endpoint'leri, auth sayfaları.

#### Robots.txt

Arama motorlarına neyi taraması, neyi atlamaması gerektiğini söyler. İzin ver: tüm public sayfalar. Engelle: /api/, /dashboard/, /settings/. Sitemap URL'sini belirt.

#### Open Graph ve Twitter Card

Sosyal medyada paylaşıldığında güzel görünen önizleme kartları.

OG görseli: 1200x630px, marka renkleri, büyük başlık, kısa açıklama. Her sayfa için ayrı OG görseli ideal ama başlangıçta tek genel görsel yeterli. Framework'ün dinamik OG görsel üretme özelliğini kullan — her sayfa için otomatik üret.

Test: https://www.opengraph.xyz adresinde URL'ni test et.

#### Yapısal Veri (JSON-LD)

Arama sonuçlarında zengin snippet (yıldız puanı, fiyat bilgisi, SSS) göstermek için. SaaS için en yararlı schema türleri:
- SoftwareApplication — ürün sayfası
- FAQPage — SSS bölümü
- Organization — şirket bilgisi
- Article — blog yazıları

### İçerik SEO'su: Blog

Blog, organik trafik çekmenin en etkili yoludur. MVP'de zorunlu değildir ama ilk aydan itibaren başlamak uzun vadede büyük fark yaratır.

#### Blog Stratejisi

- **Anahtar kelime araştırması:** Hedef kitlenin Google'da aradığı soruları bul. Düşük rekabetli, orta hacimli (uzun kuyruk) kelimelerle başla.
- **İçerik türleri:** "Nasıl yapılır" rehberleri, karşılaştırma yazıları ("X vs Y"), liste yazıları ("En iyi 10 araç"), problem çözme yazıları.
- **Yayın sıklığı:** Haftada 1 yazı ideal başlangıç. Tutarlılık, sıklıktan daha önemli.
- **İç linkler:** Her blog yazısı ilgili diğer yazılara ve ürün sayfalarına (pricing, features) link vermeli.

#### Teknik Blog Altyapısı

MDX (Markdown + JSX) önerilen format. Avantajları: Markdown ile hızlı yazım, içine React bileşenleri gömme (interaktif demolar, kod örnekleri), frontmatter ile metadata yönetimi (title, description, date, author, tags).

Blog yazısı dosya yapısı: Frontmatter (YAML) + içerik (Markdown). Liste sayfasında tarih sırasına göre göster, okuma süresi hesapla, kategori/etiket filtresi ekle.

### Performans SEO'su

Google Core Web Vitals artık sıralama faktörü. Hedefler:

- **LCP (Largest Contentful Paint):** 2.5 saniye altı. Hero görseli optimize et, font yüklemesini prioritize et.
- **FID/INP (Interaction to Next Paint):** 200ms altı. Ağır JavaScript'i lazy load et, gereksiz client-side rendering'den kaçın.
- **CLS (Cumulative Layout Shift):** 0.1 altı. Görsellere width/height ver, font yüklenirken layout kaymasını engelle.

Performans araçları:
- Lighthouse (Chrome DevTools'ta dahili)
- PageSpeed Insights (https://pagespeed.web.dev)
- Vercel Analytics (Web Vitals otomatik ölçüm)

### Launch Öncesi SEO Kontrol Listesi

- Her sayfada benzersiz title ve description var mı?
- Sitemap.xml erişilebilir mi?
- Robots.txt erişilebilir mi?
- OG görselleri test edildi mi?
- Google Search Console'a site eklendi mi?
- Sitemap Google'a gönderildi mi?
- Favicon ve apple-touch-icon ayarlandı mı?
- H1 etiketi her sayfada bir kez kullanıldı mı?
- Tüm görsellerde alt etiketi var mı?
- 404 sayfası özelleştirildi mi?
- Canonical URL'ler doğru mu?
- Lighthouse skoru 90+ mı?

---

## BÖLÜM 3: DÖNÜŞÜM OPTİMİZASYONU

### Temel İlkeler

- **Tek bir ana CTA.** Sayfadaki tüm butonlar aynı aksiyona yönlendirmeli. "Ücretsiz Dene" veya "Hemen Başla" — tutarlı ol.
- **Sürtünmeyi azalt.** Kayıt formunda en az bilgiyi iste. Sadece e-posta yeterli — isim, şirket adı, telefon numarası launch sonrasına bırakılabilir.
- **Aciliyet yarat.** "Sınırlı süre teklifi", "İlk 100 kullanıcıya özel fiyat", "14 gün ücretsiz deneme" gibi zaman baskısı unsurları.
- **İtirazları gider.** FAQ'da fiyat, güvenlik, iptal, destek sorularını cevapla. Her cevapsız soru potansiyel müşteri kaybıdır.
- **Güven göstergeleri.** SSL rozeti, ödeme sağlayıcı logosu ("Powered by Stripe"), gizlilik politikası linki, müşteri sayısı.

### Gizlilik Politikası ve Kullanım Koşulları

Yasal zorunluluktur. İçerikleri:
- Hangi veriler toplanıyor
- Veriler nasıl kullanılıyor
- Üçüncü taraflarla paylaşım
- Kullanıcı hakları (GDPR/KVKK)
- İletişim bilgileri

Başlangıçta bir AI aracından taslak ürettirip bir hukukçuya onaylat. Launch'ı hukukçu bekleme yüzünden erteleme — taslakla çık, sonra onaylat.

---

## Gotchas

- **Hero başlığında jargon kullanma.** "AI-powered omnichannel analytics platform" yerine "Müşterilerini anla, gelirini büyüt". Ziyaretçi teknik bir doküman değil, bir çözüm arıyor.
- **Fiyatlandırmayı gizleme.** Fiyat bilgisi olmayan SaaS sayfaları güven kaybeder. "Demo talep et" yerine fiyatı şeffaf göster — en azından "X'den başlayan fiyatlar".
- **Çok fazla CTA.** "Ücretsiz dene", "Demo izle", "Whitepaper indir", "Bize ulaş" — dört farklı yöne çeken bir sayfa hiçbir yere çekmez. Tek bir birincil CTA seç.
- **OG görseli unutma.** Sitenin sosyal medyada paylaşıldığında çirkin veya boş görünmesi ilk izlenimi öldürür. Launch'tan önce test et.
- **Mobile test eksikliği.** Trafiğin %60+'ı mobil. Desktop'ta güzel görünen sayfa mobilde kırılıyorsa müşterilerin çoğunu kaybedersin.
- **Blog içeriğinin ürünle ilgisiz olması.** "Yapay zekanın geleceği" gibi genel yazılar trafik çeker ama dönüşüm sağlamaz. Hedef kitlenin spesifik sorunlarını çözen yazılar yaz.
- **Sitemap'i güncellemeyi unutma.** Yeni sayfa veya blog yazısı ekledikçe sitemap otomatik güncellenmiyor olabilir. Dinamik sitemap üretimi kur.
