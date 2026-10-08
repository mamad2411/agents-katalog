---
name: saas-legal
description: >
  SaaS uygulaması için yasal uyumluluk altyapısı kur. KVKK ve GDPR
  uyumluluğu, gizlilik politikası, kullanım koşulları, çerez onayı,
  aydınlatma metni ve veri işleme süreçleri. Bu skill'i kullanıcı yasal
  gereklilikler, KVKK, GDPR, gizlilik politikası, kullanım koşulları,
  çerez onayı, kişisel veri veya uyumluluk ile ilgili bir şey istediğinde
  kullan. "Gizlilik politikası yaz", "KVKK uyumlu yap", "çerez onayı ekle",
  "yasal sayfaları hazırla" gibi ifadeler tetikler.
---

# SaaS Legal — Yasal Uyumluluk

Bu skill, bir SaaS uygulamasının yasal uyumluluk katmanını kurar. Yasal gereklilikler "launch sonrası hallederiz" diye ertelenebilecek şeyler değildir — gizlilik politikası olmadan Google OAuth onayı alamazsın, çerez onayı olmadan KVKK cezası riskin var, kullanım koşulları olmadan hukuki korunman yok.

**Bağımlılık:** Bu skill **saas-launcher** orkestratör skill'inin Landing Page fazından sonra uygulanır. Bağımsız olarak da kullanılabilir.

**Bağlı skill'ler:**
- **saas-auth** — Google OAuth onay ekranı gizlilik politikası URL'si gerektirir.
- **saas-analytics** — Tracking ve veri toplama gizlilik politikasında açıklanmalı.
- **saas-landing-seo** — Yasal sayfalar footer'da link olarak yer almalı.

---

## Türkiye'deki SaaS İçin Yasal Çerçeve

### KVKK (Kişisel Verilerin Korunması Kanunu)

KVKK, Türkiye'nin kişisel veri koruma kanunudur (6698 sayılı kanun). AB'nin GDPR'ına benzer ama bazı farklılıkları var.

**Kim uymalı:** Türkiye'deki kullanıcılardan kişisel veri toplayan her gerçek ve tüzel kişi. Solo founder dahil.

**Kişisel veri nedir:** Kimliği belirli veya belirlenebilir kişiye ilişkin her türlü bilgi — ad, e-posta, IP adresi, çerez verileri, ödeme bilgileri, kullanım verileri.

**Temel yükümlülükler:**
1. **Aydınlatma:** Veri toplamadan önce kullanıcıyı bilgilendir (hangi veri, neden, ne kadar süre)
2. **Açık rıza:** Zorunlu olmayan veri işleme için kullanıcının onayını al
3. **Veri güvenliği:** Toplanan veriyi teknik ve idari tedbirlerle koru
4. **Veri silme:** Kullanıcının talebine 30 gün içinde yanıt ver
5. **VERBİS kaydı:** Yıllık çalışan sayısı veya ciro eşiğini aşıyorsan VERBİS'e kayıt ol

### GDPR (AB Kullanıcıları Varsa)

AB'deki kullanıcılara hizmet veriyorsan GDPR de geçerli. KVKK'ya ek olarak:
- Daha katı açık rıza gereksinimleri
- Veri İşleme Sözleşmesi (DPA) yükümlülüğü
- Veri ihlali bildirimi (72 saat)
- Daha yüksek cezalar

**Pratik yaklaşım:** GDPR uyumlu ol, KVKK otomatik olarak karşılanmış olur (GDPR daha katı).

---

## Gizlilik Politikası

### Neden Zorunlu

- KVKK aydınlatma yükümlülüğü (yasal zorunluluk)
- Google OAuth onay ekranı (gizlilik politikası URL'si gerekli)
- App Store / Play Store gereksinimleri (mobil uygulama varsa)
- Kullanıcı güveni

### İçermesi Gerekenler

**1. Veri sorumlusu bilgileri:**
- Şirket/kişi adı, adres, iletişim bilgileri
- Solo founder için kişisel bilgiler yeterli

**2. Toplanan veriler:**
- Kimlik verileri (ad, e-posta)
- İletişim verileri (e-posta adresi)
- Ödeme verileri (Stripe/Lemon Squeezy aracılığıyla — kart bilgisi sende saklanmaz)
- Kullanım verileri (sayfa görüntüleme, tıklama, oturum süresi)
- Teknik veriler (IP adresi, tarayıcı, cihaz bilgisi)
- Çerez verileri

**3. Verilerin işlenme amaçları:**
- Hizmet sunumu ve hesap yönetimi
- Ödeme işleme
- İletişim (transactional e-postalar)
- Ürün geliştirme ve analitik
- Yasal yükümlülükler

**4. Verilerin paylaşıldığı üçüncü taraflar:**
- Supabase (veritabanı barındırma)
- Stripe / Lemon Squeezy (ödeme işleme)
- Resend (e-posta gönderimi)
- PostHog (analytics)
- Vercel (hosting)
- Google (OAuth — kullanılıyorsa)

**5. Veri saklama süresi:**
- Hesap aktif olduğu sürece
- Hesap silindikten sonra yasal saklama süresi (fatura verileri için 10 yıl)
- Anonim analitik verileri süresiz

**6. Kullanıcı hakları:**
- Verilere erişim hakkı
- Düzeltme hakkı
- Silme hakkı (hesap silme)
- İtiraz hakkı
- Veri taşınabilirliği hakkı
- Başvuru yöntemi (e-posta adresi)

**7. Çerez politikası** (ayrı sayfa veya aynı sayfada bölüm)

**8. Güncelleme bilgisi:** Politika değişikliklerinde kullanıcıya bildirim

### Uygulama

Gizlilik politikası sayfasını `/privacy` route'unda oluştur. Footer'da her sayfadan erişilebilir olmalı. Son güncelleme tarihini göster.

**Başlangıçta:** AI aracından taslak üret, projenin gerçek veri işleme süreçlerine göre düzenle. Launch'ı hukukçu bekleme yüzünden erteleme — taslakla çık, ardından bir hukukçuya onaylat.

---

## Kullanım Koşulları (Terms of Service)

### İçermesi Gerekenler

1. **Hizmet tanımı:** Ne sunuyorsun
2. **Kabul koşulları:** Hizmeti kullanarak koşulları kabul etme
3. **Hesap sorumlulukları:** Kullanıcının hesap güvenliği sorumluluğu
4. **Kabul edilebilir kullanım:** Yasadışı, zararlı kullanım yasağı
5. **Ödeme koşulları:** Fiyatlandırma, faturalandırma, iade politikası
6. **İptal ve fesih:** Nasıl iptal edilir, veriye ne olur
7. **Fikri mülkiyet:** Senin yazılımın senin, kullanıcının verisi kullanıcının
8. **Sorumluluk sınırlaması:** Hizmet kesintisi, veri kaybı durumunda sorumluluk sınırı
9. **Uygulanacak hukuk:** Türk hukuku, yetkili mahkeme
10. **Değişiklik bildirimi:** Koşullar değişirse kullanıcıya bildirim

Sayfayı `/terms` route'unda oluştur.

---

## Çerez Onayı (Cookie Consent)

### Ne Zaman Gerekli

- **Zorunlu çerezler** (oturum, güvenlik): Onay gerekmez — çalışması için teknik olarak gerekli
- **Analitik çerezler** (PostHog, GA): KVKK ve GDPR kapsamında onay gerekir
- **Pazarlama çerezleri** (reklam, retargeting): Kesinlikle onay gerekir

### Uygulama Yaklaşımı

**Basit banner:** Sayfanın altında veya üstünde çerez bildirimi. İki buton: "Kabul Et" (tüm çerezler), "Sadece Zorunlu" (analytics kapalı). Kullanıcı seçimini localStorage'da veya cookie'de sakla.

**Detaylı yönetim (opsiyonel):** Çerez kategorilerini ayrı ayrı açma/kapama. İlk aşamada gerekmez.

### PostHog ile Entegrasyon

Kullanıcı analitik çerezlerini reddederse PostHog'u başlatma veya cookieless modda çalıştır. PostHog'un `opt_out_capturing()` ve `opt_in_capturing()` fonksiyonlarını çerez onayı kararına bağla.

---

## KVKK Aydınlatma Metni

KVKK'nın özel gereksinimi. Gizlilik politikasından farklı olarak yasal formatta yazılmalı:

1. Veri sorumlusunun kimliği
2. Kişisel verilerin hangi amaçla işleneceği
3. İşlenen kişisel verilerin kimlere ve hangi amaçla aktarılabileceği
4. Kişisel veri toplamanın yöntemi ve hukuki sebebi
5. İlgili kişinin hakları (KVKK madde 11)

Bu metin kayıt/giriş akışında kullanıcıya gösterilmeli veya erişilebilir olmalı.

---

## Hesap Silme Akışı (KVKK Madde 7)

Kullanıcının hesabını ve verilerini silme hakkı yasal zorunluluktur.

### Uygulama

1. Ayarlar sayfasında "Hesabımı Sil" butonu
2. Onay adımı: geri dönüşü olmadığını, aktif aboneliğin iptal edileceğini belirt
3. Aktif abonelik varsa: önce iptal et (bkz. **saas-payments**)
4. Kullanıcı verisini sil veya anonimleştir
5. Yasal saklama yükümlülüğü olan verileri (fatura) anonimleştir, silme
6. Supabase Auth'tan kullanıcıyı sil
7. Oturumu sonlandır
8. Üçüncü taraf servislerde veriyi temizle (Stripe müşteri kaydı, PostHog profili)
9. Kullanıcıya silme onay e-postası gönder

**Süre:** KVKK'ya göre silme talebi 30 gün içinde sonuçlandırılmalı. Otomatik silme mekanizması kur — manuel süreç ölçeklenmez.

---

## İade Politikası

Ödeme kabul ediyorsan iade politikası olmalı:

- İade koşulları (hangi durumlarda iade yapılır)
- İade süresi (14 gün, 30 gün)
- İade yöntemi (aynı ödeme yöntemine)
- Kısmi iade (dönem ortasında iptal)

Tüketici koruma mevzuatı gereği dijital hizmetlerde 14 gün cayma hakkı olabilir — hukuki danışmanlık al.

---

## Launch Kontrol Listesi

- [ ] Gizlilik politikası sayfası (`/privacy`) yayında
- [ ] Kullanım koşulları sayfası (`/terms`) yayında
- [ ] KVKK aydınlatma metni erişilebilir
- [ ] Çerez onayı banner'ı çalışıyor
- [ ] Footer'da gizlilik ve kullanım koşulları linkleri var
- [ ] Google OAuth onay ekranında gizlilik politikası URL'si
- [ ] Hesap silme mekanizması çalışıyor
- [ ] İade politikası belirlenmiş
- [ ] Veri işleme envanteri çıkarılmış (hangi veri, nerede, neden)

---

## Gotchas

- **Google OAuth gizlilik politikası olmadan onaylanmaz.** OAuth Consent Screen'de gizlilik politikası URL'si zorunlu alan. Launch'tan önce hazırla.
- **"Herkes kullanıyor, sorun olmaz" yanılgısı.** KVKK cezaları bireysel veri sorumlularına da uygulanır. Solo founder muaf değildir.
- **Çerez onayı almadan analytics başlatma.** PostHog veya GA'yı kullanıcı onayı olmadan başlatmak KVKK/GDPR ihlali.
- **Gizlilik politikasını güncel tutma.** Yeni bir üçüncü taraf servis ekledikçe (analytics, e-posta, CDN) gizlilik politikasını güncelle.
- **Veri lokasyonu önemli.** KVKK yurt dışına veri aktarımında açık rıza veya yeterli koruma gerektirir. Supabase, Vercel, Stripe gibi servislerin veri merkezlerini gizlilik politikasında belirt.
- **Fatura verileri silinemez.** Vergi mevzuatı gereği fatura ve ödeme kayıtları 10 yıl saklanmalı. Hesap silinse bile bu veriler anonimleştirilerek tutulmalı.
- **Hukukçuya danış ama bekleme.** AI ile taslak oluştur, yayınla, ardından hukukçuya onaylat. Hukukçu beklentisi launch'ı aylarca erteleyebilir.
