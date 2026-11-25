---
name: sky-privacy-engineering
description: >-
  KVKK'nın mühendislik tarafı: kişisel veri envanteri, açık rıza kaydı, saklama ve silme, çerez onayı,
  "verilerimi sil". "KVKK", "kişisel veri" dendiğinde kullan. Hukuki metin için hukukçuya yönlendir.
---

# Sky · Gizlilik Mühendisliği

Bu skill **teknik uygulamayı** kapsar; aydınlatma metni, VERBİS kaydı ve hukuki değerlendirme bir
hukukçunun işidir — bunu kullanıcıya açıkça hatırlat.

## 1. Veri envanteri (her şeyin başı)

`docs/privacy/data-inventory.md`:
| Veri | Tablo.sütun | Kategori | Amaç | Hukuki dayanak | Saklama | Kimler erişir | Aktarım |
|---|---|---|---|---|---|---|---|
| Ad soyad | clients.name | Kimlik | Randevu | Sözleşme | Son işlemden 2 yıl | Org üyeleri | — |
| Telefon | clients.phone | İletişim | Hatırlatma SMS | Sözleşme/rıza | aynı | Org, SMS sağlayıcı | Netgsm (TR) |
| Sağlık notu | visits.note | **Özel nitelikli** | Hizmet | Açık rıza | 10 yıl | Yalnızca hekim rolü | — |
Özel nitelikli veri (sağlık, biyometrik, din, ceza…) → ek şifreleme, dar erişim, açık rıza.

## 2. Minimizasyon

Her form alanı için "buna gerçekten ihtiyacımız var mı?" TC kimlik numarası, doğum tarihi, cinsiyet gibi
alanları gereksiz toplama. Toplanmayan veri sızmaz.

## 3. Saklama süreleri ve otomatik silme

```
retention_policies  table_name, condition_sql, keep_days, action (delete|anonymize)
```
Gece işi (bkz. `sky-jobs`): süresi dolan kayıtları sil veya anonimleştir; kaç kayıt işlendiğini logla.
Örnekler: doğrulanmamış hesaplar 30 gün, iletişim formu mesajları 1 yıl, ham loglar 30 gün, analitik olaylar 13 ay.

## 4. "Verilerimi indir"

- Ayarlar → Gizlilik → "Verilerimi indir" → arka plan işi → JSON + CSV ZIP (profil, kayıtlar, dosyalar listesi,
  rıza geçmişi) → e-posta ile 7 gün geçerli imzalı bağlantı.
- Her tablo için dışa aktarım fonksiyonu; yeni tablo eklenince envanter + export güncellenir (PR kontrol listesi).

## 5. "Hesabımı sil"

1. Yeniden kimlik doğrulama + onay ("hesabımı sil" yazdır).
2. 14–30 gün bekleme (geri alınabilir), bu sürede giriş yapılırsa iptal seçeneği.
3. Sonra: kişisel alanlar silinir/anonimleşir, oturumlar kapanır, dosyalar silinir, üçüncü taraflara silme
   isteği (e-posta sağlayıcı listesi, analitik `deleteUser`).
4. Yasal saklama zorunluluğu olanlar (fatura — VUK 5/10 yıl) ayrı ve erişimi kısıtlı tutulur.
5. Kullanıcıya tamamlandı e-postası.

## 6. Anonimleştirme

- Silme yerine istatistik korunacaksa: ad → "Silinmiş kullanıcı", e-posta → `deleted+<id>@invalid`, telefon → null,
  serbest metin alanları → temizle, IP → kısalt.
- Takma ad (pseudonymization): analitikte kullanıcı ID'si yerine hash'li ID; anahtar ayrı.
- Test/staging'e prod verisi **kopyalama**; gerekiyorsa maskelenmiş döküm.

## 7. Rıza kayıtları

```
consents  user_id, purpose (marketing_email|marketing_sms|analytics|health_data), granted bool, text_version, source, ip_trunc, created_at
```
Append-only (geçmiş korunur); geri çekme aynı kolaylıkta (ayarlarda tek tık). Ticari ileti → İYS ile senkron (bkz. `sky-notifications`).

## 8. Çerezler

- Envanter: ad, sağlayıcı, amaç, süre, kategori (zorunlu/işlevsel/analitik/pazarlama).
- Onay bandı: "Kabul et" ve "Reddet" **eşit ağırlıkta**, "Tercihler" ile kategori seçimi; reddedince analitik scriptler hiç yüklenmez.
- Tercih değiştirme bağlantısı footer'da her zaman.
- Çerezsiz analitik (Plausible/Umami) ile onay bandını gereksiz kılmak en zarif çözüm (bkz. `sky-observability`).

## 9. Log ve analitikte PII

pino `redact` (bkz. `sky-observability`), Sentry `beforeSend`, analitik olaylarında e-posta/telefon/ad yok,
AI izlerinde maskeleme. URL'lerde kişisel veri yok (`?email=` asla).

## 10. Alt işleyiciler ve aktarım

`docs/privacy/subprocessors.md`: Vercel (ABD/AB), Supabase (bölge), Resend, Netgsm, Sentry, PostHog (AB)…
Yurt dışı aktarım KVKK'da ayrı şartlara bağlıdır — listeyi hukukçuya ver. Mümkünse AB/TR bölgesi seç.

## 11. İhlal planı

Kim karar verir, nasıl tespit edilir (anormal export, toplu erişim alarmı), 72 saat içinde Kurul'a bildirim
(hukukçu ile), etkilenen kişilere bildirim şablonu, olay kaydı. Bkz. `sky-observability` alarmlar.
