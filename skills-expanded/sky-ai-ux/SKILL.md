---
name: sky-ai-ux
description: >-
  AI özellikleri için arayüz kalıpları: streaming yanıt gösterimi, düşünme/adım göstergeleri,
  düzenlenebilir ve kabul/ret edilebilir çıktı, satır içi AI (seçili metne "iyileştir"), öneri
  çipleri ve boş durum promptları, kaynak gösterme ve güven göstergeleri, iptal/yeniden üret,
  geri bildirim (👍/👎), sohbet geçmişi, hata ve sınır durumları, AI etiketleme ve beklenti
  yönetimi. "AI arayüzü", "chat UI", "AI çıktısını nasıl gösterelim" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · AI Arayüzü

Teknik taraf `sky-ai` / `sky-ai-agents`'ta. Burada kullanıcının **güvenini ve kontrolünü** sağlayan kalıplar.

## Temel ilke: AI önerir, kullanıcı karar verir

Çıktı her zaman **düzenlenebilir**, **geri alınabilir** ve kalıcı işlemden önce **onaylanır**. "AI kendi kafasına göre
gönderdi" deneyimi güveni bir kerede bitirir.

## Streaming

- Token token akış (yazıyor hissi); ilk token < 1 sn hedef. Beklerken üç nokta animasyonu veya "Düşünüyor…".
- Uzun işlerde adım göstergesi: "🔎 Randevular aranıyor → ✓ 7 bulundu → ✍️ Özet yazılıyor" (bkz. `sky-ai-agents`).
- Akış sırasında otomatik en alta kaydır; kullanıcı yukarı kaydırırsa durdur ("↓ Yeni içerik" butonu).
- **Durdur** butonu her zaman görünür; durdurunca kısmi çıktı kalır.
- Markdown'ı akarken güvenli render et (yarım kod blokları bozulmasın — `streamdown` gibi kütüphaneler).

## Çıktı kontrolleri

Her yanıtın altında: **Kopyala · Yeniden üret · Düzenle · 👍 👎**. Taslaklarda: **Kullan / Düzenle / Vazgeç**.
Birden çok seçenek: "3 farklı versiyon" sekmeleri veya kartları — kullanıcı seçmeyi yazmaktan çok sever.

## Satır içi AI

- Metin seçince bubble menüde ✨ "AI ile": Kısalt, Uzat, Resmîleştir, Samimileştir, Yazım hatalarını düzelt, Çevir.
- Sonuç **diff olarak** önerilir (silinen üstü çizili, eklenen yeşil) → Kabul (Tab) / Reddet (Esc).
- Boş alanda "✨ Taslak oluştur" ("Hizmet açıklaması yaz").
- Form akıllı doldurma: AI'ın doldurduğu alanlar hafif vurgulu + "AI tarafından dolduruldu, kontrol et" notu.

## Boş durum ve keşif

Sohbet açılışında boş kutu yerine **öneri çipleri**: "Bu haftaki iptalleri özetle", "En sadık 10 müşterim kim?",
"Yarın için boş saatler". Kullanıcı neler yapabileceğini anında öğrenir. Bağlama göre değişsin (hangi sayfadaysa).

## Güven ve şeffaflık

- **Kaynak gösterme**: iddiaların yanında küçük atıf numaraları [1] → tıklayınca kaynak parça/belge (RAG, bkz. `sky-ai`).
- Araç kullanımları katlanabilir ayrıntı ("3 sorgu çalıştırıldı ▾").
- Belirsizlikte açık söyleme: "Bu bilgiyi kayıtlarda bulamadım." — uydurmaktan çok daha güven verici.
- AI içerik etiketi (✨ simgesi / "AI ile oluşturuldu") — özellikle müşteriye giden metinlerde.
- Sınırlar: "AI hata yapabilir. Önemli bilgileri kontrol et." — bir kez, sade.

## Onay kartları (yıkıcı/dışa dönük işlemler)

```
📤 12 müşteriye SMS gönderilecek
"Merhaba {ad}, yarınki randevunuzu hatırlatırız…"   [Önizle ▾]
Tahmini maliyet: ₺4,80
[Gönder]  [Düzenle]  [Vazgeç]
```
Ne olacağı, kime, kaça mal olacağı net. Toplu işlemlerde alıcı listesi açılabilir.

## Geri bildirim

👍/👎 tek tık; 👎'de isteğe bağlı neden çipleri ("Yanlış bilgi", "Çok uzun", "Ton uygun değil") + serbest metin.
Geri bildirim eval setine akar (bkz. `sky-ai-eval`). Teşekkür mikro mesajı.

## Geçmiş ve bağlam

- Sohbet geçmişi listesi (otomatik başlıklı), arama, silme; yeni sohbet butonu belirgin.
- Bağlam göstergesi: "Bu sohbet Ayşe Yılmaz'ın kaydı hakkında" çipi (kaldırılabilir).
- Ek dosya/görsel yükleme sürükle-bırak.

## Hata ve sınır durumları

- Kota doldu: "Bu ayki AI kullanımın doldu · Yenilenme 15 Kasım · [Planı yükselt]" (bkz. `sky-metering-quotas`).
- Model hatası/zaman aşımı: kısmi çıktıyı koru + "Yeniden dene".
- Reddedilen istek: yargılamayan dil, alternatif öner.
- Yavaşlık: 10 sn'den uzun işlerde arka plana al, bitince bildir.

## Erişilebilirlik

Akan yanıt `aria-live="polite"` (ama token token değil, tamamlanan cümleler/paragraflar duyurulsun), durdur butonu klavyeyle,
öneri çipleri buton, odak yönetimi (yeni yanıtta odak kaybolmasın).
