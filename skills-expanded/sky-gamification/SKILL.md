---
name: sky-gamification
description: >-
  Oyunlaştırma ve motivasyon tasarımı: ilerleme çubukları, seriler (streak), rozetler ve
  başarımlar, seviyeler ve puanlar, lider tabloları, hedefler ve kilometre taşları, kutlama
  anları, sürpriz ödüller ve haftalık özetler; ne zaman işe yarar ne zaman zarar verir
  (içsel vs dışsal motivasyon), veri modeli ve suistimal önleme. "Kullanıcıları motive
  edelim", "rozet sistemi", "seri", "puan", "oyunlaştırma" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Oyunlaştırma

## Önce: işe yarar mı?

✓ Tekrarlanan, kendisi biraz sıkıcı ama faydalı davranışlar: dil öğrenme, egzersiz, alışkanlık, onboarding tamamlama,
öğrenme platformu, topluluk katkısı.
✗ Kullanıcının zaten içsel motivasyonla yaptığı işi puana bağlamak (anlam kaybı), profesyonel B2B araçlarda çocuksu rozetler,
rekabetin zarar verdiği bağlamlar (sağlık, yas, finansal stres).
Kural: oyunlaştırma **ilerlemeyi görünür kılar**, kullanıcıyı manipüle etmez (bkz. `sky-ethical-ux`).

## Mekanikler

| Mekanik | Ne zaman | Dikkat |
|---|---|---|
| **İlerleme çubuğu** | kurulum, profil, kurs | evrensel olarak iyi; ilk adım önceden dolu |
| **Seri (streak)** | günlük alışkanlık | **seri dondurma** hakkı (kötü bir gün her şeyi silmesin), kaybetme kaygısı yaratmasın |
| **Kilometre taşı** | 10. müşteri, 100. randevu | kutlama + paylaşılabilir kart — B2B'de bile sevilir |
| **Rozet/başarım** | keşif (özellik kullanımı), topluluk | az ve anlamlı; gizli rozetler sürpriz yaratır |
| **Seviye / puan** | öğrenme, topluluk | puan neyin karşılığı açık olsun |
| **Lider tablosu** | rekabetçi, eşit koşullu gruplar | yalnızca opt-in, arkadaş/küçük grup bazlı, haftalık sıfırlanan; mutlak lider tablosu çoğunluğu demotive eder |
| **Hedef** | kullanıcının kendi koyduğu | kullanıcı belirlesin ("Haftada 3 ders") |
| **Haftalık özet** | her ürün | "Bu hafta 23 randevu, geçen haftadan %15 fazla 📈" — sessiz ama güçlü |

## Kutlama anları

- Küçük: ✓ animasyonu, "Harika!" mikro metni, hafif titreşim.
- Orta: konfeti (bkz. `sky-canvas`), seri sayısı büyüyerek belirir.
- Büyük (kilometre taşı): tam ekran kart, paylaş butonu (OG görseli: "100. randevumu Sky ile aldım 🎉").
Sıklık azaldıkça büyüklük artar; her tıklamada konfeti anlamını yitirir. Reduced-motion'da animasyonsuz kutlama.

## Veri modeli

```
achievements       id, key, title, description, icon, secret bool, tier
user_achievements  user_id, achievement_key, unlocked_at, progress int
streaks            user_id, kind, current, longest, last_activity_date, freezes_left
events             user_id, type, created_at      -- tetikleyici kaynak (bkz. sky-observability olayları)
```
- Başarımlar olaylardan **sunucuda** hesaplanır (istemci "rozet kazandım" diyemez); arka plan işi ile (bkz. `sky-jobs`).
- Seri hesabı kullanıcının **saat diliminde** gün sınırıyla (bkz. `sky-date-time`).
- Geriye dönük: yeni rozet eklenince mevcut kullanıcılar için hesapla (sürpriz "zaten kazandın!" anı).

## Suistimal

Puan/ödül gerçek değer taşıyorsa (indirim, para) hile yapılır: hız sınırı, anlamsız tekrar tespiti, kendi kendine etkileşim
engelleme, ödülü gecikmeli verme.

## UI

- Profilde başarım vitrini (kazanılan renkli, kilitli soluk + ilerleme "7/10").
- Seri göstergesi üstte küçük 🔥 12; kaybetme riski varsa nazik hatırlatma ("Serini korumak için bugün 1 ders yeterli").
- Bildirimler kişisel ve seyrek; "bugün giriş yapmadın!" baskısı yok.
