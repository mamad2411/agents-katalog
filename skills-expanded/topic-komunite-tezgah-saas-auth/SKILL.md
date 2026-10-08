---
name: saas-auth
description: >
  SaaS uygulaması için kimlik doğrulama ve oturum yönetimi kur. Google OAuth,
  Magic Link, e-posta/şifre veya bunların kombinasyonlarını yapılandır. Bu
  skill'i kullanıcı login sistemi, kayıt akışı, oturum yönetimi, korumalı
  route'lar veya kullanıcı profili ile ilgili bir şey istediğinde kullan.
  "Giriş sayfası yap", "auth ekle", "kullanıcı sistemi kur", "login/register"
  gibi ifadeler tetikler.
---

# SaaS Auth — Kimlik Doğrulama ve Oturum Yönetimi

Bu skill, bir SaaS uygulamasının kimlik doğrulama katmanını kurar. Auth, uygulamanın diğer tüm katmanlarının temelidir — ödeme sistemi kullanıcı kimliğine, API koruması oturuma, e-posta gönderimi kullanıcı bilgisine bağlıdır.

**Bağımlılık:** Bu skill **saas-launcher** orkestratör skill'inin Faz 3'üdür. Bağımsız olarak da kullanılabilir.

**Bağlı skill'ler:**
- **saas-email** — Magic Link stratejisi seçildiyse e-posta altyapısının kurulu olması gerekir.
- **saas-payments** — Auth tamamlandıktan sonra ödeme sistemi kullanıcı kimliğini kullanır.
- **saas-api-security** — Oturum bilgisi API koruma katmanı tarafından tüketilir.

---

## Auth Stratejisi Seçimi

Kullanıcıyla beraber doğru stratejiyi belirle. Her yöntemin avantaj ve dezavantajlarını açıkla.

### Google OAuth

**Ne zaman seç:** Çoğu SaaS için varsayılan önerimiz. Kullanıcılar yeni bir şifre oluşturmak zorunda kalmaz, güven algısı yüksektir.

**Avantajları:** Tek tıkla giriş, şifre yönetimi yükü yok, profil bilgisi (isim, fotoğraf) otomatik gelir, güvenilir e-posta adresi garanti.

**Dezavantajları:** Google Cloud Console'da OAuth uygulama oluşturma ve onay süreci gerekir. Production'da Google'ın app review'u birkaç gün sürebilir. Bazı kurumsal kullanıcılar kişisel Google hesaplarını iş araçlarında kullanmak istemeyebilir.

**Kritik adımlar:**
- Google Cloud Console'da proje oluştur, OAuth Client ID al
- Callback URL'leri hem development hem production için tanımla
- OAuth Consent Screen'i yapılandır ve yayınla
- Scopes: `email` ve `profile` neredeyse her zaman yeterli

**Dikkat:** Google OAuth başvurusunda uygulama adı, logo ve gizlilik politikası URL'si gerekir. Gizlilik politikası sayfası launch'tan önce hazır olmalı.

### Magic Link (E-posta ile Giriş)

**Ne zaman seç:** Şifresiz deneyim isteyenler için. Google'a bağımlı olmak istemeyenler veya Google OAuth'u destekle birlikte ikinci yöntem olarak.

**Avantajları:** Şifre yok, hesap çalınma riski düşük, e-posta adresi otomatik doğrulanmış olur.

**Dezavantajları:** Her girişte e-posta kutusuna gitmek gerekir — sürtünme yaratır. E-posta teslim edilemezse kullanıcı giremez. E-posta altyapısı hazır olmalı (DNS kayıtları dahil).

**Bağımlılık:** Magic Link kullanmak için **saas-email** skill'inin tarif ettiği e-posta altyapısı önceden kurulmuş olmalı. DNS kayıtları (SPF, DKIM, DMARC) yapılmadan magic link e-postaları spam'a düşer.

**Dikkat:** Magic link bağlantılarının süresi olmalı (24 saat makul). Bağlantı tek kullanımlık olmalı — tekrar kullanılması güvenlik açığıdır.

### E-posta + Şifre

**Ne zaman seç:** Genellikle önerilmez, ama bazı enterprise senaryolarda veya kullanıcı tabanı OAuth'a aşina değilse gerekebilir.

**Avantajları:** Kullanıcılara tanıdık kalıp, hiçbir dış servise bağımlılık yok.

**Dezavantajları:** Şifre saklama yükümlülüğü (hashing, salt, güvenli depolama), şifre sıfırlama akışı, brute force koruması, şifre politikası yönetimi. Güvenlik yüzey alanı çok daha geniş.

**Eğer bu yol seçilirse:** Şifreler bcrypt veya argon2 ile hash'lenmeli, minimum şifre uzunluğu zorunlu olmalı, rate limiting giriş denemelerine uygulanmalı, şifre sıfırlama token'ları tek kullanımlık ve süreli olmalı.

### Önerilen Kombinasyon

Çoğu SaaS için en iyi strateji: **Google OAuth + Magic Link**. Kullanıcıya iki yol sunar — Google hesabı olanlar tek tıkla girer, olmayanlar e-posta ile girer. İkisi de şifresiz.

Aynı e-posta ile hem Google hem Magic Link kullanılabilmesi için hesap bağlama (account linking) aktif edilmeli. Bu yapılmazsa "bu e-posta zaten kayıtlı" hatası oluşur.

---

## Oturum Stratejisi

### JWT vs. Database Session

**JWT (JSON Web Token) — Varsayılan önerimiz:**
- Oturum bilgisi token içinde taşınır, her istekte veritabanı sorgusu yapmaz
- Serverless ortamlarda (Vercel) çok daha performanslı
- Token içine plan bilgisi gibi özel alanlar eklenebilir
- Dezavantaj: token iptal etmek anında mümkün değil (token süresi dolana kadar geçerli)

**Database Session:**
- Oturum veritabanında saklanır, her istekte sorgulanır
- Anlık iptal mümkün (oturumu sil → kullanıcı çıkış yapmış olur)
- Dezavantaj: her API isteğinde veritabanı sorgusu, serverless'ta latency

**Karar:** JWT seç. Plan bilgisinin anlık güncellenmesi gerekiyorsa (ödeme sonrası plan yükseltme), session update mekanizmasını kullan — token'ı yenile.

### Token'a Eklenecek Bilgiler

JWT token'a şu bilgileri ekle:
- Kullanıcı ID'si (veritabanı referansı)
- Plan bilgisi (free/starter/pro — API koruma katmanı bunu kullanır)
- Gerekirse: takım ID'si, rol bilgisi

Token'a büyük veri ekleme — her istekte taşınır. Detaylı kullanıcı bilgisi gerektiğinde veritabanından çek.

---

## Korumalı Route Mimarisi

### Route Grupları

Next.js App Router'da route gruplarını kullanarak public ve korumalı alanları ayır:

- `(public)` grubu: Landing page, blog, fiyatlandırma — herkese açık
- `(auth)` grubu: Giriş, kayıt — sadece giriş yapmamış kullanıcılar görmeli
- `(dashboard)` grubu: Uygulama arayüzü — sadece giriş yapmış kullanıcılar

### Middleware Stratejisi

Middleware, her istek öncesinde çalışan ve oturum kontrolü yapan katmandır. Next.js middleware'i Edge Runtime'da çalışır — bu yüzden veritabanı sorgusu yapamaz (JWT strategy'nin önemli olma nedeni).

Middleware'de yapılacaklar:
- Giriş yapmamış kullanıcıyı korumalı sayfalardan login'e yönlendir
- Giriş yapmış kullanıcıyı login sayfasından dashboard'a yönlendir
- API route'ları için auth header kontrolü

Middleware **yapmaması gereken şeyler:**
- Veritabanı sorgusu (Edge Runtime'da çalışmaz)
- Ağır hesaplamalar (her istekte çalışır, hızlı olmalı)
- Plan bazlı erişim kontrolü (bunu API route seviyesinde yap, middleware'de değil — bkz. **saas-api-security**)

### Sayfa Seviyesinde Koruma

Middleware genel koruma sağlar. Sayfa seviyesinde ek kontrol için:
- Server Component'lerde oturum bilgisini server-side al ve kontrol et
- Client Component'lerde oturum hook'unu kullan, loading state göster

---

## Giriş ve Kayıt Sayfası Tasarımı

### Tek Sayfa Yaklaşımı (Önerilen)

Ayrı login ve register sayfası yerine tek bir sayfa kullan. SaaS'larda giriş ve kayıt aynı akıştır — Google ile giriş yapan kullanıcı ilk seferde otomatik kayıt olur, Magic Link ile giriş yapan kullanıcı da öyle.

Sayfa yapısı:
1. Başlık: "Giriş yap" veya "Hesabını oluştur"
2. Google ile devam et butonu (birincil — en görünür)
3. "veya" ayracı
4. E-posta input'u + "E-posta ile devam et" butonu (Magic Link)
5. Küçük metin: "Devam ederek gizlilik politikasını kabul edersin"

### Giriş Sonrası Yönlendirme

- Başarılı giriş → Dashboard'a yönlendir
- İlk kez giriş yapan kullanıcı → Onboarding akışına yönlendir (varsa)
- Ödeme sayfasından gelen kullanıcı → Giriş sonrası checkout'a geri yönlendir

Callback URL'yi giriş öncesinde sakla (URL parametresi veya cookie ile) ve giriş sonrası oraya yönlendir. Bu özellikle "Satın Al" butonuna tıklayıp giriş yapması gereken kullanıcılar için kritik.

---

## Kullanıcı Profili ve Ayarları

### Minimum Profil Bilgileri

SaaS'ta kullanıcı profilinde olması gerekenler:
- İsim (düzenlenebilir)
- E-posta (gösterilir, değiştirilmez — veya değiştirme akışı ayrıca tasarlanmalı)
- Profil fotoğrafı (OAuth'tan gelir, opsiyonel değiştirme)
- Mevcut plan bilgisi
- Plan yönetimi linki (Stripe müşteri portalına yönlendir — bkz. **saas-payments**)

### Hesap Silme

GDPR ve KVKK uyumluluğu için kullanıcının kendi hesabını silebilmesi gerekir. Bu akış:
1. Kullanıcı silme isteği yapar
2. Onay adımı (geri dönüşü olmadığını belirt)
3. Aktif abonelik varsa önce iptal et (bkz. **saas-payments**)
4. Kullanıcı verisini sil veya anonimleştir
5. Oturumu sonlandır

---

## Gotchas

- **Account linking:** Aynı e-posta ile Google ve Magic Link kullanıldığında hesaplar birleşmeli. Bu ayar açıkça aktifleştirilmeli, yoksa "bu hesap zaten var" hatası alırsın.
- **Production secret:** Auth secret'ı (JWT imzalama anahtarı) production'da development'tan farklı ve güçlü olmalı. `openssl rand -base64 32` ile üret.
- **OAuth callback URL'leri:** Hem `localhost` hem production domain'i eklenmiş olmalı. Eksik callback URL = "redirect_uri_mismatch" hatası.
- **Edge uyumluluğu:** Middleware Edge Runtime'da çalışır. Veritabanı adapter'ları genellikle Edge'de çalışmaz — bu yüzden JWT strategy kritik.
- **Session senkronizasyonu:** Kullanıcının planı değiştiğinde (ödeme sonrası) oturum token'ını güncellemeyi unutma. Yoksa kullanıcı plan yükseltir ama arayüzde hâlâ eski planı görür.
- **Google OAuth onay süreci:** Production'da "Test" modundan çıkıp "Published" moduna geçmeden sadece test kullanıcıları giriş yapabilir. Launch'tan birkaç gün önce yayınla.
- **Magic Link spam riski:** Aynı e-postaya çok sayıda magic link gönderilmesini engelle (rate limit). Aksi halde kötü niyetli biri başkasının e-posta kutusunu doldurabilir.
- **Redirect sonrası sayfa yenileme:** Bazı tarayıcılarda OAuth redirect sonrası cache sorunları olabilir. Giriş sonrası router.refresh() veya hard redirect kullan.
