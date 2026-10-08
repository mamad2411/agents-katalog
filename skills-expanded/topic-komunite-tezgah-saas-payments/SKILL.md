---
name: saas-payments
description: >
  SaaS uygulaması için ödeme ve abonelik sistemi kur. Stripe veya Lemon
  Squeezy ile checkout, webhook, abonelik yönetimi, fiyatlandırma planları
  ve müşteri portalı yapılandır. Bu skill'i kullanıcı ödeme, abonelik,
  fiyatlandırma, Stripe, gelir, plan, subscription veya checkout ile
  ilgili bir şey istediğinde kullan. "Para al", "ödeme sistemi kur",
  "pricing yap", "abonelik ekle" gibi ifadeler tetikler.
---

# SaaS Payments — Ödeme ve Abonelik Yönetimi

Bu skill, bir SaaS uygulamasının ödeme katmanını kurar. Ödeme, SaaS'ın kalbidir — doğru kurulmazsa ya para alırsın ama plan aktifleşmez, ya da plan aktifleşir ama para alınmaz.

**Bağımlılık:** Bu skill **saas-launcher** orkestratör skill'inin Faz 4'üdür. Bağımsız olarak da kullanılabilir. Auth katmanının (**saas-auth**) tamamlanmış olması gerekir — ödeme sistemi kullanıcı kimliğine bağlıdır.

**Bağlı skill'ler:**
- **saas-auth** — Kullanıcı kimliğini sağlar. Checkout öncesi auth kontrolü yapılır.
- **saas-email** — Ödeme onayı, başarısız ödeme bildirimi gibi e-postaları tetikler.
- **saas-landing-seo** — Fiyatlandırma bölümü buradaki plan tanımlarıyla uyumlu olmalı.
- **saas-api-security** — Plan bazlı erişim kontrolü oturumdaki plan bilgisini kullanır.

---

## Ödeme Sağlayıcı Seçimi

### Stripe

**Varsayılan önerimiz.** Gerekçeler:

Güçlü yönleri: Sektör standardı, en iyi dokümantasyon, en düşük komisyon (%2.9 + $0.30/işlem), kapsamlı webhook sistemi, müşteri portalı hazır, test modu ve CLI ile kolay geliştirme, dev ekosistem (faturalandırma, Connect, Tax).

Zayıf yönleri: Vergi yönetimi ayrı yapılandırılmalı (Stripe Tax ek ücretli veya kendi başına hesaplamalısın). Türkiye'den doğrudan Stripe hesabı açmak kısıtlı olabilir — Stripe Atlas ile ABD LLC kurulması gerekebilir.

Türkiye bağlamı: Stripe Türkiye'de doğrudan merchant hesabı desteklemiyor (bu durum değişebilir, güncel bilgiyi kontrol et). Seçenekler: Stripe Atlas ile ABD şirketi kurmak, ya da Lemon Squeezy'nin MoR modelini kullanmak. Kullanıcıya bu durumu mutlaka belirt.

### Lemon Squeezy

**Ne zaman seç:** Vergi yönetimiyle uğraşmak istemeyenler için ideal.

Güçlü yönleri: Merchant of Record (MoR) modeli — KDV, sales tax, GST hesaplama, tahsilat ve beyanı Lemon Squeezy yapar. Türkiye'den global satış yapan founder'lar için büyük avantaj. Herhangi bir ülkeden hesap açılabilir.

Zayıf yönleri: Daha yüksek komisyon (%5 + $0.50/işlem), Stripe kadar geniş ekosistem yok, dokümantasyon daha sınırlı.

### Karar Akışı

- Türkiye'den çalışıyorsan ve ABD şirketin yoksa → **Lemon Squeezy** (MoR avantajı)
- ABD şirketin varsa veya Stripe Atlas kullanıyorsan → **Stripe** (düşük komisyon, geniş ekosistem)
- Dijital ürün satıyorsan (e-kitap, kurs, lisans) → **Lemon Squeezy** (bu kullanım için optimize)
- Karmaşık faturalandırma gerekiyorsa (metered billing, kullanım bazlı) → **Stripe** (çok daha esnek)

---

## Fiyatlandırma Stratejisi

### Plan Sayısı

- **2 plan** — Çoğu erken aşama SaaS için ideal. Basit karar: ucuz ve pahalı. Kullanıcı hızla seçer.
- **3 plan** — Klasik "Good-Better-Best" modeli. Orta plan en çok satanı olur (decoy effect). Ama erken aşamada gereksiz karmaşıklık yaratabilir.
- **1 plan + ücretsiz katman** — En basit model. Freemium veya deneme süresi ile.

**Önerimiz:** 2 plan ile başla. İhtiyaç ortaya çıktıkça 3. planı ekle.

### Fiyat Belirleme

Bu işte kesin formül yok ama rehber ilkeler:

- **Değer bazlı fiyatla.** Maliyetinin üstüne kâr koyma — sunduğun değerin bir kısmını iste. Kullanıcına ayda 10.000 TL tasarruf sağlıyorsan, ayda 500 TL istemek makul.
- **Yuvarlak sayılar kullan.** $19, $49, $99 — psikolojik fiyatlandırma çalışır.
- **Yıllık indirim sun.** Genellikle %15-20 indirim (2 ay ücretsiz eşdeğeri). Yıllık planlar nakit akışını iyileştirir ve churn'ü azaltır.
- **Ücretsiz deneme vs. Freemium:** Deneme süresi (7-14 gün) aciliyet yaratır. Freemium (sınırlı ücretsiz plan) geniş kullanıcı tabanı oluşturur ama dönüşüm oranı genellikle daha düşük.

### Plan Özellik Matrisi

Her planın net sınırları olmalı. Sınırlar şu kategorilerden seçilmeli:

- **Kaynak limitleri:** Proje sayısı, depolama alanı, takım üyesi sayısı
- **Kullanım limitleri:** API çağrısı, işlem sayısı, e-posta gönderimi
- **Özellik erişimi:** Gelişmiş raporlar, API erişimi, özel entegrasyonlar, öncelikli destek
- **Destek seviyesi:** E-posta desteği vs. canlı destek vs. dedicated account manager

Her sınır ölçülebilir ve uygulanabilir olmalı. "Sınırsız" vaat etme — ya kaynakların tükenir ya da kötü niyetli kullanım başlar. "Cömert limitler" daha dürüst ve sürdürülebilir.

---

## Checkout Akışı

### Kullanıcı Yolculuğu

1. Kullanıcı fiyatlandırma sayfasında plan seçer
2. Giriş yapmamışsa → login sayfasına yönlendirilir, giriş sonrası checkout'a döner
3. Server-side API route'u ödeme sağlayıcıda checkout session oluşturur
4. Kullanıcı ödeme sağlayıcının hosted checkout sayfasına yönlendirilir
5. Ödeme başarılıysa → başarı sayfasına yönlendirilir
6. Ödeme iptal edilirse → fiyatlandırma sayfasına geri yönlendirilir

**Hosted Checkout kullan.** Kendi ödeme formu oluşturmaya çalışma. Stripe Checkout ve Lemon Squeezy Checkout PCI uyumlu, güvenli, dönüşüm için optimize edilmiş hosted sayfalardır. Kendi formunu yapmak güvenlik riski ve dönüşüm kaybıdır.

### Checkout Session Oluşturma

Server-side API route'unda yapılması gerekenler:
1. Kullanıcının giriş yapmış olduğunu doğrula
2. Seçilen planın ve periyodun (aylık/yıllık) geçerli olduğunu doğrula
3. Kullanıcının ödeme sağlayıcıda müşteri kaydı yoksa oluştur
4. Müşteri kaydını veritabanındaki kullanıcıyla ilişkilendir
5. Checkout session oluştur — başarı ve iptal URL'lerini, kullanıcı bilgisini ve metadata'yı gönder
6. Checkout URL'sini client'a döndür

**Kritik:** Checkout session'a kullanıcı ID'sini metadata olarak ekle. Webhook geldiğinde bu ID ile ödemeyi doğru kullanıcıya eşleştireceksin.

---

## Webhook Yönetimi

Webhook, ödeme sağlayıcının "hey, bir şey oldu" diye senin sunucuna haber göndermesidir. SaaS'ın en kritik altyapı parçasıdır.

### Neden Checkout Başarı Sayfası Yeterli Değil?

Kullanıcı ödeme yaptıktan sonra başarı sayfasına yönlendirilir. Ama bu sayfaya ulaşmak ödemenin gerçekten tamamlandığını garanti etmez — tarayıcı kapanabilir, internet kesilir, kullanıcı geri tuşuna basar. **Tek güvenilir kaynak webhook'tur.**

### İşlenmesi Gereken Webhook Event'leri

| Event | Anlam | Yapılması Gereken |
|-------|-------|-------------------|
| Checkout tamamlandı | Kullanıcı ilk ödemeyi yaptı | Planı aktifleştir, veritabanını güncelle |
| Abonelik güncellendi | Plan değişti veya yenilendi | Plan bilgisini ve bitiş tarihini güncelle |
| Abonelik iptal edildi | Kullanıcı iptal etti veya süre doldu | Planı free'ye düşür, ödeme referanslarını temizle |
| Ödeme başarısız | Kart reddedildi veya bakiye yetersiz | Kullanıcıyı bilgilendir (e-posta), grace period başlat |

### Webhook Güvenliği

**İmza doğrulama zorunludur.** Her webhook isteği ödeme sağlayıcı tarafından imzalanır. Bu imzayı doğrulamadan webhook'u işleme — aksi halde herhangi biri sahte webhook göndererek planları bedava aktifleştirebilir.

İmza doğrulama süreci:
1. İsteğin ham gövdesini (raw body) al — JSON parse etme, ham metin olarak oku
2. İstek header'ından imzayı al
3. Ödeme sağlayıcının SDK'sı ile imzayı doğrula
4. Doğrulama başarısızsa 400 döndür ve işleme

**Raw body kritik.** Çoğu framework (Next.js dahil) gelen istekleri otomatik JSON parse eder. Webhook endpoint'inde bu davranışı devre dışı bırakmalısın — Stripe imza doğrulaması ham byte'lar üzerinde çalışır.

### Idempotency

Ödeme sağlayıcılar aynı webhook'u birden fazla kez gönderebilir (ağ kesintisi, timeout, retry mekanizması). Webhook handler'ın idempotent olmalı — aynı event'i iki kez işlese bile sonuç aynı olmalı.

Yaklaşımlar:
- Event ID'sini sakla, daha önce işlenmiş event'leri atla
- Veritabanı işlemlerini "oluştur veya güncelle" (upsert) olarak tasarla
- En basit yol: güncel durumu set et, artımlı değişiklik yapma. "Plan = pro yap" her seferinde aynı sonucu verir.

### Hata Yönetimi

Webhook handler'da hata olursa ne döndürmelisin?

- **İşleme hatası (kendi kodundaki bug):** 200 döndür. 500 dönersen ödeme sağlayıcı tekrar dener ve aynı hata tekrarlanır. 200 döndür, hatayı logla, düzelt.
- **İmza doğrulama hatası:** 400 döndür. Bu gerçekten geçersiz bir istek.
- **Bilinmeyen event türü:** 200 döndür ve yoksay. İleride yeni event türleri eklenebilir.

---

## Abonelik Yaşam Döngüsü

### Durumlar ve Geçişler

```
[Ücretsiz] → Checkout → [Aktif Abonelik]
[Aktif] → Yenileme başarılı → [Aktif] (bitiş tarihi uzar)
[Aktif] → Ödeme başarısız → [Grace Period] → Düzelirse [Aktif], düzelmezse [İptal]
[Aktif] → Kullanıcı iptal etti → [İptal Bekliyor] → Dönem sonunda [Ücretsiz]
[Aktif] → Plan değişikliği → [Yeni Plan Aktif]
```

### Grace Period (Ödeme Tolerans Süresi)

Kart reddedildiğinde kullanıcının erişimini hemen kesme. Grace period tanımla (genellikle 3-7 gün). Bu sürede:
- Kullanıcıya e-posta gönder: "Ödemeniz başarısız oldu, kart bilgilerinizi güncelleyin"
- Ödeme sağlayıcı otomatik retry yapar (genellikle 3 deneme)
- Grace period sonunda hâlâ başarısızsa planı düşür

### İptal Politikası

İki yaklaşım:
- **Dönem sonunda iptal (önerilen):** Kullanıcı iptal eder, mevcut ödeme döneminin sonuna kadar erişimi devam eder. Adil ve standart.
- **Anında iptal:** Kullanıcı iptal eder, erişim hemen kesilir. Kısmi iade yapılır mı? Karmaşıklık yaratır.

---

## Müşteri Portalı

Stripe ve Lemon Squeezy hazır hosted müşteri portalı sunar. Bu portalda kullanıcılar:
- Kart bilgilerini güncelleyebilir
- Aboneliğini yükseltebilir/düşürebilir
- Aboneliğini iptal edebilir
- Fatura geçmişini görebilir

**Kendi portal sayfanı yapmaya çalışma.** Hosted portal PCI uyumlu, bakım gerektirmez ve ödeme sağlayıcı tarafından güncel tutulur. Senden tek gereken: bir API endpoint'i oluştur, portal URL'sini al, kullanıcıyı oraya yönlendir.

---

## Fiyatlandırma Sayfası ile Entegrasyon

Fiyatlandırma sayfası (**saas-landing-seo** skill'inin kapsamında) buradaki plan tanımlarını tek kaynaktan okumalı. Plan bilgilerini bir konfigürasyon dosyasında tanımla — isim, açıklama, fiyat, özellik listesi, ödeme sağlayıcı referansları (price ID veya variant ID). Bu konfigürasyonu hem fiyatlandırma sayfası hem checkout akışı kullanır.

Aylık/yıllık toggle: Fiyatlandırma sayfasında aylık ve yıllık arasında geçiş yapabilen bir toggle koy. Yıllık planı vurgula — tasarruf yüzdesini göster.

---

## Test Stratejisi

### Development'ta Test

Her ödeme sağlayıcının test modu var. Development'ta her zaman test modu kullan.

**Stripe:** Test kartları — 4242 4242 4242 4242 (başarılı), 4000 0000 0000 0002 (reddedilir). Stripe CLI ile webhook'ları localhost'a yönlendir. Her event türünü ayrı ayrı test et.

**Lemon Squeezy:** Dashboard'da test modu aktifleştir. Test ürünleri ve variant'ları ayrıca oluşturulmalı.

### Test Senaryoları

Minimum test edilmesi gerekenler:
1. Başarılı checkout → plan aktifleşiyor mu?
2. Başarısız ödeme → kullanıcı bilgilendiriliyor mu?
3. Abonelik iptal → dönem sonunda plan düşüyor mu?
4. Plan değişikliği (upgrade/downgrade) → doğru plan yansıyor mu?
5. Webhook tekrar gönderimi → idempotent çalışıyor mu?

---

## Gotchas

- **Webhook imzası atlanırsa:** Herhangi biri sunucuna POST göndererek bedava plan alabilir. İmza doğrulama hayati derecede kritik.
- **Raw body parsing:** Webhook endpoint'inde framework'ün otomatik JSON parsing'ini devre dışı bırak. Bu yapılmazsa imza doğrulama her zaman başarısız olur.
- **Test vs. live anahtarları:** Stripe test anahtarları `sk_test_` ile, live `sk_live_` ile başlar. Karıştırma — test ödemesi live'da görünmez, live ödeme test'te görünmez.
- **Price ID farklılığı:** Test modundaki fiyat ID'leri live moddakilerden farklıdır. Production'a geçerken güncelle.
- **Para birimi karışıklığı:** Stripe miktarları kuruş/cent cinsindedir. $19 = 1900. Gösterimde 100'e bölmeyi unutma, checkout'ta 100 ile çarpmayı unutma.
- **Webhook endpoint runtime:** Next.js Edge Runtime'da Stripe webhook imza doğrulaması çalışmaz. Webhook route'u Node.js runtime'da çalışmalı.
- **Checkout sonrası yönlendirme:** Başarı sayfasına plan bilgisini URL parametresi ile geçirme — bu parametre manipüle edilebilir. Başarı sayfasında veritabanından güncel plan bilgisini çek.
- **Çift ödeme:** Kullanıcı checkout butonuna hızlıca iki kez tıklarsa iki checkout session açılabilir. Butonu tıklama sonrası devre dışı bırak ve loading state göster.
- **Kur dönüşümü:** Stripe hesap para birimi ile fiyat para birimi farklıysa kur farkı komisyonuna dikkat. Mümkünse tek para biriminde kal.
