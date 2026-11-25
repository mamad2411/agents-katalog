---
name: sky-scheduling
description: >-
  Randevu ve rezervasyon motoru: hizmet/personel/kaynak modeli, uygun slot üretimi (çalışma
  saatleri, molalar, tamponlar, mevcut randevular, tatiller), çift rezervasyonu engelleme
  (exclusion constraint, kilit), saat dilimi, online rezervasyon akışı (Calendly tarzı),
  onay/iptal/erteleme politikaları, hatırlatmalar (SMS/e-posta/WhatsApp), gelmeyen (no-show)
  takibi, bekleme listesi, Google Calendar senkronu ve personel takvimi UI. "Randevu sistemi",
  "rezervasyon", "müsait saatler", "klinik/kuaför randevu" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Randevu Motoru

## Veri modeli

```
services        id, org_id, name, duration_min, buffer_before_min, buffer_after_min, price_minor, color, online_bookable
staff           id, org_id, name, avatar_url, timezone
staff_services  staff_id, service_id
working_hours   staff_id, weekday (1-7), start_time, end_time        -- birden çok satır = mola
time_off        staff_id, starts_at, ends_at, reason                  -- izin, tatil
bookings        id, org_id, staff_id, service_id, client_id, starts_at, ends_at, status (pending|confirmed|cancelled|completed|no_show),
                source (online|staff|phone), cancel_token_hash, notes, created_at
```

## Çift rezervasyonu veritabanında engelle

```sql
create extension if not exists btree_gist;
alter table bookings add constraint no_overlap exclude using gist (
  staff_id with =, tstzrange(starts_at, ends_at, '[)') with &&
) where (status in ('pending', 'confirmed'));
```
Uygulamada kontrol yarışa açıktır; bu kısıt iki kişi aynı anda aynı slota tıklasa bile birini reddeder.
İhlali (`23P01`) yakala → "Bu saat az önce doldu, işte en yakın uygun saatler" + alternatifler.

## Slot üretimi

```
girdi: hizmet (süre + tamponlar), personel (veya "fark etmez"), tarih aralığı, kullanıcının saat dilimi
1. Personelin o günkü çalışma aralıkları (working_hours, personelin diliminde)
2. − time_off, − resmi tatiller/kapalı günler
3. − mevcut randevular (tamponlarla genişletilmiş)
4. Kalan boşlukları adım (15 dk) aralıklarla böl; hizmet süresi + tampon sığanlar = slot
5. Kural filtreleri: en erken (ör. 2 saat sonrası), en geç (60 gün ileri), günlük maks
6. "Fark etmez" seçiliyse personellerin birleşimi; slotu seçince en az dolu personele ata
```
- Hesaplamayı sunucuda yap; sonuçları kısa süre (30 sn) cache'le.
- Saat dilimi: işletmenin dilimiyle hesapla, kullanıcınınkiyle göster (farklıysa "(İstanbul saati)" yaz).

## Online rezervasyon akışı (Calendly hissi)

1. Hizmet seç (kart: süre, fiyat) → 2. Personel seç (avatar, "Fark etmez") → 3. Tarih (takvimde dolu günler soluk)
→ 4. Saat (sabah/öğle/akşam grupları, düğme ızgarası) → 5. Bilgiler (ad, telefon, not) + KVKK onayı →
6. Onay ekranı: özet, **"Takvime ekle"**, iptal/erteleme bağlantısı, konum ve yol tarifi.
- Slot seçince 5–10 dk **geçici tutma** (pending + expires_at) → form doldururken başkası kapmasın.
- Telefonla OTP doğrulama (sahte randevuyu engeller) isteğe bağlı.
- Gömülebilir widget (`<iframe>` veya script) + doğrudan bağlantı (`site.com/r/acme`) + QR kod.

## Politikalar

- İptal/erteleme son saati (ör. randevudan 12 saat önceye kadar); bağlantı e-posta/SMS'te, giriş gerektirmez (imzalı token).
- Kapora/ön ödeme (bkz. `sky-payments`) yüksek no-show'lu hizmetlerde.
- Onay modu: otomatik onay veya işletme onayı (pending → confirmed bildirimi).

## Hatırlatmalar

- 24 saat önce + 2 saat önce (ayarlanabilir); SMS (bkz. `sky-notifications`), e-posta, WhatsApp Business API.
- Hatırlatmada "Onayla / Ertele / İptal" bağlantıları → no-show belirgin şekilde düşer.
- Randevu oluşunca gecikmeli iş planla; iptal/ertelemede işi iptal et (bkz. `sky-jobs`).
- Sessiz saatlere dikkat (22:00–08:00 gönderme).

## Gelmeyenler ve bekleme listesi

- Personel randevu sonrası "Geldi / Gelmedi"; no-show sayısı müşteri kartında; 3 no-show → ön ödeme zorunlu kuralı.
- Bekleme listesi: dolu güne "Yer açılırsa haber ver"; iptal olunca listedekilere sırayla SMS ("10 dk içinde onayla").

## Personel takvimi UI

- Gün/hafta görünümü, personel sütunları (kaynak görünümü), randevular hizmet rengiyle.
- Sürükle-bırak taşıma, kenardan uzatma (bkz. `sky-drag-drop`); çakışma anında kırmızı.
- Boş slota tıkla → hızlı randevu formu; müşteri arama (bkz. `sky-search`).
- "Şimdi" çizgisi, bugünkü özet (12 randevu, 2 boşluk, ₺4.800).

## Takvim senkronu

- Google Calendar: OAuth, personelin takvimindeki meşgul zamanları **free/busy** ile oku (slotlardan düş), randevuları
  yaz; webhook (push notifications) ile değişiklikleri al. Microsoft Graph benzer.
- iCal abonelik bağlantısı (salt okuma `.ics` feed) — en basit, herkesin sevdiği seçenek.
