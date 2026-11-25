---
name: sky-pricing-page
description: >-
  Fiyatlandırma sayfası: plan yapısı, aylık/yıllık, karşılaştırma tablosu, TL ve KDV dahil fiyat
  gösterimi. "Fiyatlandırma sayfası", "pricing" dendiğinde kullan.
---

# Sky · Fiyatlandırma Sayfası

## Yapı

```
Başlık: "Her ölçekte işletme için basit fiyatlar"   [Aylık | Yıllık  %20 tasarruf]
┌ Başlangıç ┐ ┌ Pro (Önerilen) ┐ ┌ Ekip ┐
│ ₺0        │ │ ₺299/ay        │ │ ₺799/ay │      + "Kurumsal? Bize ulaşın" şeridi
│ kime?     │ │ kime?          │ │ kime?   │
│ [Başla]   │ │ [14 gün dene]  │ │ [Dene]  │
│ ✓ özellik │ │ Başlangıç +    │ │ Pro +   │
└───────────┘ └────────────────┘ └─────────┘
Özellik karşılaştırma tablosu (katlanabilir) · Güven (yorumlar/logolar) · SSS · Son CTA
```

## Psikoloji (dürüst olanlar)

- **3 plan**: seçim kolay; ortadaki "Önerilen" (rozet + hafif büyük + vurgu kenarlığı) çoğunluğu oraya yönlendirir.
- **Çapa**: en pahalı plan solda veya sağda referans noktası oluşturur; Kurumsal "Bize ulaşın" tavanı belirler.
- **"Kime" satırı** her planda: "Tek başına çalışanlar için", "Büyüyen ekipler için" — insanlar kendini bulur.
- **Yıllık geçişi**: tasarrufu TL olarak da göster ("Yılda ₺718 tasarruf"); yıllıkta aylık eşdeğer fiyat + "yıllık faturalandırılır".
- **Ücretsiz deneme** kart istemeden → daha çok başlangıç; kartla → daha nitelikli. Hedefe göre seç.
- Fiyatlar yuvarlak ve net; gizli ücret yok. Sahte geri sayım, sahte "son 2 yer" yok (bkz. `sky-ethical-ux`).

## Özellik listesi

- Her planda **farkı** listele ("Pro: Başlangıç'taki her şey +"), uzun tekrar listesi değil.
- En değerli 5–7 özellik kartta; tam liste karşılaştırma tablosunda.
- Limitler açık ("Ayda 50 randevu", "5 personel") — bkz. `sky-metering-quotas`.
- Teknik terimlere tooltip (ⓘ): "SMS hatırlatma — randevudan 24 saat önce otomatik".

## Karşılaştırma tablosu

Yapışkan plan başlıkları (kaydırırken), gruplanmış satırlar (Randevu, Bildirimler, Raporlar, Destek), ✓ / — / metin
değerleri, mobilde plan seçmeli tek sütun görünüm (3 sütunlu tablo 375px'te okunmaz). Butonlar subgrid ile aynı hizada (bkz. `sky-css-modern`).

## Türkiye detayları

- Fiyat TL, KDV dahil mi hariç mi **açıkça** ("Fiyatlara KDV dahildir" veya "+KDV"); tüketiciye KDV dahil göster.
- `₺299` veya `299 TL` — tek biçim; ondalık gerekmiyorsa gösterme.
- Döviz bazlı fiyatlıyorsan TL karşılığını ve kur güncelleme politikasını yaz.
- Taksit seçeneği (yıllık planda "12 taksit") Türk kullanıcıları için güçlü.
- Fatura: e-Arşiv/e-Fatura kesildiğini belirt (kurumsal müşteriler sorar).

## Fiyat hesaplayıcı

Koltuk/kullanım bazlı fiyatlarda kaydırıcı ("Kaç personel?" 1–25) → anlık toplam, plan önerisi. Kullanıcılar
etkileşimli hesaplayıcıyı sever ve sonuca daha çok güvenir.

## SSS (itirazlar)

"İstediğim zaman iptal edebilir miyim?", "Deneme bitince ne olur?", "Plan değiştirirsem?", "Verilerim güvende mi / nerede?",
"Fatura kesiyor musunuz?", "İade politikası?", "Öğrenci/dernek indirimi?". `FAQPage` JSON-LD (bkz. `sky-seo`).

## Ölçüm ve test

Olaylar: plan kartı tıklama, aylık/yıllık geçişi, SSS açma, checkout başlatma. A/B fikirleri (bkz. `sky-feature-flags`):
önerilen plan, varsayılan yıllık/aylık, deneme süresi, plan adları. Fiyat testleri hassastır — mevcut müşterilere tutarlı davran.
