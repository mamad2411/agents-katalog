---
name: saas-email
description: >
  SaaS uygulaması için transactional e-posta altyapısı kur. Resend veya
  Mailgun yapılandırması, DNS kayıtları (SPF, DKIM, DMARC), e-posta
  şablonları ve spam'dan kaçınma stratejisi. Bu skill'i kullanıcı e-posta
  gönderimi, DNS ayarları, spam sorunu, magic link, e-posta şablonu veya
  e-posta servisi ile ilgili bir şey istediğinde kullan. "E-postalar spam'a
  düşüyor", "DNS ayarla", "hoş geldin e-postası yap" gibi ifadeler tetikler.
---

# SaaS Email — E-posta Altyapısı

Bu skill, bir SaaS uygulamasının e-posta katmanını kurar. E-posta, kullanıcıyla iletişimin en kritik kanalıdır — magic link giriş, ödeme onayları, bildirimler ve destek hep e-postaya bağlıdır.

**Bağımlılık:** Bu skill **saas-launcher** orkestratör skill'inin Faz 5'idir. Bağımsız olarak da kullanılabilir.

**Bağlı skill'ler:**
- **saas-auth** — Magic Link stratejisi bu skill'in altyapısına bağlıdır.
- **saas-payments** — Ödeme bildirimleri (onay, hata, iptal) e-posta ile gönderilir.

**Zamanlama notu:** DNS kayıtlarının yayılması 24-48 saat sürebilir. E-posta altyapısını mümkün olduğunca erken — ideal olarak projenin ilk gününde — başlat. En azından DNS kayıtlarını ekle, servis tarafında doğrulamayı beklerken diğer fazlara devam et.

---

## E-posta Servisi Seçimi

### Resend — Varsayılan Önerimiz

**Ne zaman seç:** Çoğu SaaS projesi için. Modern API, React Email ile güzel şablonlar, Next.js ekosistemiyle doğal uyum.

Güçlü yönleri: API tasarımı basit ve modern, React Email ile tip güvenli şablonlar, webhook desteği, domain doğrulama dashboard'u anlaşılır, Next.js ve Vercel ile sorunsuz entegrasyon.

Zayıf yönleri: Ücretsiz katman günde 100 e-posta ile sınırlı (launch günü aşılabilir), inbound e-posta desteği sınırlı, görece yeni servis (Mailgun kadar olgun değil).

Fiyatlandırma: Ücretsiz katman (100/gün), ardından $20/ay (50K e-posta). Çoğu erken SaaS için yeterli.

### Mailgun

**Ne zaman seç:** Yüksek hacimli gönderim, gelişmiş inbound e-posta routing, mevcut Mailgun altyapısı varsa.

Güçlü yönleri: Yüksek hacim desteği, güçlü inbound routing (gelen e-postaları webhook'la işle), olgun ekosistem, detaylı analitik.

Zayıf yönleri: API tasarımı eski, React Email desteği yok (HTML şablonları elle yazılmalı), kurulum daha karmaşık, EU ve US bölgeleri ayrı.

---

## DNS Altyapısı — E-postanın Temeli

DNS kayıtları, e-postalarının spam yerine inbox'a düşmesini sağlayan teknik altyapıdır. Bu kayıtlar olmadan gönderilen e-postaların büyük çoğunluğu spam klasörüne gider veya hiç teslim edilmez.

### Subdomain Stratejisi

**Ana domain'den e-posta gönderme.** `noreply@uygulamam.com` yerine `noreply@mail.uygulamam.com` kullan.

Neden: Transactional e-posta gönderimi ana domain'in itibarını riske atar. E-posta itibarı zedelenirse uygulamanın SEO'su ve diğer e-posta iletişimi de etkilenebilir. Subdomain izolasyon sağlar.

### Üç Zorunlu DNS Kaydı

#### SPF (Sender Policy Framework)

SPF, "bu domain adına kimler e-posta gönderebilir?" sorusunun cevabıdır. Alıcı sunucu bu kaydı kontrol eder — listede olmayan sunucudan gelen e-postayı reddeder veya spam'a atar.

Kayıt türü: TXT
İsim: mail (veya mail.uygulamam.com)
Değer: Resend için `v=spf1 include:_spf.resend.com ~all`, Mailgun için `v=spf1 include:mailgun.org ~all`

`~all` (softfail) başlangıç için uygun. Sistem oturduğunda `-all` (hardfail) yapılabilir.

#### DKIM (DomainKeys Identified Mail)

DKIM, gönderilen her e-postaya dijital imza ekler. Alıcı sunucu bu imzayı DNS kaydıyla doğrular — imza eşleşmezse e-posta kurcalanmış demektir.

Kayıt detayları e-posta servisinin dashboard'undan alınır. Genellikle bir veya birden fazla CNAME veya TXT kaydıdır. Her servis farklı format kullanır — dashboard'daki talimatları aynen takip et.

#### DMARC (Domain-based Message Authentication, Reporting and Conformance)

DMARC, SPF ve DKIM sonuçlarına göre ne yapılacağını belirler ve raporlama sağlar.

Kayıt türü: TXT
İsim: _dmarc.mail (veya _dmarc.mail.uygulamam.com)
Başlangıç değeri: `v=DMARC1; p=none; rua=mailto:dmarc@uygulamam.com`

**Aşamalı yaklaşım:**
1. `p=none` ile başla — sadece raporla, hiçbir şey engelleme. Raporları incele, meşru e-postaların doğru geçtiğinden emin ol.
2. Birkaç hafta sorunsuz çalıştıktan sonra `p=quarantine` yap — şüpheli e-postaları spam'a at.
3. Her şey stabil olduğunda `p=reject` yap — şüpheli e-postaları tamamen reddet.

### DNS Kayıt Ekleme Süreci

1. Domain sağlayıcının (Cloudflare, Namecheap, GoDaddy, Vercel Domains vb.) DNS yönetim paneline git
2. E-posta servisinin dashboard'undan gerekli kayıtları al (SPF, DKIM, DMARC)
3. Kayıtları DNS paneline ekle — kayıt türü, isim ve değer alanlarını aynen kopyala
4. Kaydet ve yayılmayı bekle (15 dakika - 48 saat)
5. E-posta servisinin dashboard'unda "Verify" butonuna tıklayarak doğrulamayı kontrol et

**Cloudflare kullanıyorsan:** DKIM için eklenen CNAME kayıtlarında "Proxy" (turuncu bulut) devre dışı olmalı — sadece "DNS only" (gri bulut). Proxy aktifken doğrulama başarısız olur.

---

## E-posta Şablonları Stratejisi

### Her SaaS'ta Olması Gereken E-postalar

**Zorunlu (Day 1):**
1. **Magic Link giriş e-postası** — "Giriş bağlantınız" (eğer Magic Link kullanılıyorsa)
2. **Hoş geldin e-postası** — Kayıt sonrası, ürünü nasıl kullanacağını kısaca anlat
3. **Ödeme onay e-postası** — Başarılı ödeme sonrası

**Önemli (İlk hafta):**
4. **Ödeme başarısız bildirimi** — Kart reddedilince gönderilir, kart güncelleme linki içerir
5. **Abonelik iptal onayı** — İptal edildiğinde, erişimin ne zaman sona ereceğini belirt

**Sonra eklenecek:**
6. **Deneme süresi bitiyor hatırlatması** — 3 gün kala, 1 gün kala
7. **Haftalık/aylık özet** — Kullanıcı aktivitesi raporu
8. **Yeniden etkileşim** — 30 gün inaktif kullanıcılara

### Şablon Tasarım İlkeleri

- **Basit tut.** Sade, tek sütunlu layout. Fazla görsel, karmaşık tablo, süslü grafik değil. Gmail, Outlook ve Apple Mail hepsi farklı render eder — basitlik uyumluluk sağlar.
- **Tek bir CTA.** Her e-postanın tek bir amacı ve tek bir aksiyon butonu olsun. "Giriş yap" veya "Kartını güncelle" veya "Dashboard'a git" — birden fazla buton kafa karıştırır.
- **Mobil uyumlu.** E-postaların %60+'ı mobilde okunur. Butonlar yeterince büyük (en az 44px yükseklik), metin okunabilir (en az 14px), genişlik 600px'i geçmemeli.
- **Plain text alternatifi.** Her HTML e-postanın düz metin (plain text) versiyonunu da gönder. Bazı e-posta istemcileri HTML render etmez, bazı kullanıcılar plain text tercih eder.
- **Gönderen adı kişisel.** "noreply@mail.uygulamam.com" yerine "Fatih from Uygulamam <fatih@mail.uygulamam.com>" çok daha iyi açılma oranı verir.

### React Email (Resend ile)

Resend kullanıyorsan React Email kütüphanesi tip güvenli, bileşen bazlı e-posta şablonları yazmanı sağlar. Avantajı: şablonlar React bileşeni olarak yazılır, development'ta tarayıcıda önizlenebilir, e-posta istemci uyumluluğu kütüphane tarafından yönetilir.

Development'ta `email dev` komutu ile http://localhost:3001'de tüm şablonları önizleyebilirsin.

---

## Gelen E-posta İşleme (İleri Seviye)

Bazı SaaS'larda kullanıcılardan e-posta almak gerekebilir — destek talepleri, reply-to ile etkileşim, e-posta tabanlı iş akışları.

### Yaklaşım

E-posta servisinin webhook'unu kullan — gelen e-posta geldiğinde senin API endpoint'ine POST gönderir. Endpoint'te gönderen, konu, gövde bilgilerini işle.

Kullanım alanları: Destek ticket sistemi, e-posta ile görev oluşturma, reply-based onay akışları.

**Bu Day 1 özelliği değildir.** İlk launch'ta gerek yoktur, sonradan eklenebilir.

---

## E-posta Gönderim İzleme

### Takip Edilmesi Gereken Metrikler

- **Delivery rate** — Teslim edilen / gönderilen. %99 üstü hedef. Düşükse DNS sorunları olabilir.
- **Bounce rate** — Geri dönen e-posta oranı. %2 üstüyse geçersiz e-posta adresleri temizlenmeli.
- **Spam complaint rate** — Spam olarak işaretlenme oranı. %0.1 üstüyse acil müdahale gerekir.
- **Open rate** — Transactional e-postalarda %60-80 normal. Düşükse konu satırları veya gönderen adı gözden geçirilmeli.

### E-posta servisi dashboard'unda bu metrikleri düzenli kontrol et. Özellikle launch'ın ilk haftası kritiktir.

---

## Gotchas

- **DNS yayılımı zamana bağlı.** 24-48 saat sürebilir. İlk günden DNS kayıtlarını ekle, doğrulamayı beklerken diğer işlere devam et.
- **Cloudflare proxy DKIM'i bozar.** DKIM CNAME kayıtlarında turuncu bulutu kapatıp gri bulut (DNS only) yap.
- **Spam testi yap.** Launch'tan önce https://mail-tester.com adresine test e-postası gönder. 10 üzerinden 9+ skor hedef. Düşükse DNS kayıtlarını kontrol et.
- **Rate limit farkındalığı.** Resend ücretsiz planda günde 100 e-posta. ProductHunt launch'ı veya viral büyüme günü bu limiti dakikalar içinde aşabilirsin. Önceden ücretli plana geç.
- **E-posta adresi doğrulama.** Kayıt sırasında e-posta formatını kontrol et, ama gerçek doğrulama magic link veya onay e-postası ile yapılır. Geçersiz e-postalara sürekli gönderm bounce rate'i yükseltir.
- **Unsubscribe linki zorunlu.** Pazarlama e-postalarında (haftalık özet, yeniden etkileşim) unsubscribe linki yasal zorunluluk (CAN-SPAM, GDPR). Transactional e-postalarda (ödeme onayı, magic link) gerekli değil.
- **Zaman dilimine duyarlı gönderim.** Hatırlatma ve bildirim e-postalarını kullanıcının yerel saatine göre gönder. Gece 3'te ödeme hatırlatması rahatsız edici.
- **E-posta boyutu.** Gmail 102 KB üstünü kırpar ("Bu mesaj kırpıldı" uyarısı gösterir). Şablonları küçük tut, gereksiz HTML'den kaçın.
