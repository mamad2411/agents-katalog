---
name: etkinlik-tarama
description: "Kültür-etkinlik sahnesini haftalık tarar: kıyas kurum programları, biletleme platformları, kültür-sanat basını; sinyal çıkarır, kıyas tablosu kurar. Kullan: 'haftalık tarama', 'etkinlik taraması', 'kıyas kurumlar ne duyurdu', 'bilet fiyatlarını karşılaştır' dendiğinde veya haftalik-tarama-loop tetiklendiğinde. Örnek: 'Bu haftanın taramasını yap' → kaynak listesini gez, 5+ sinyal çıkar, kıyas tablosunu doldur."
allowed-tools: Read, Write, WebFetch, WebSearch
model: sonnet
user-invocable: true
---
# Etkinlik Tarama

Haftalık etkinlik/kıyas-kurum taraması yordamı. Çıktısı `/haftalik-tarama-raporu`nun girdisidir.

## Ne zaman aktifleş
"Haftalık tarama", "etkinlik taraması", "kıyas kurumlar", "bilet stratejisi karşılaştır",
"sahnede yeni ne var" bağlamlarında; `haftalik-tarama-loop` her tetiklendiğinde.

## Kaynak listesi (tarama sırasıyla)
1. **Kurum siteleri/duyuruları** — İstanbul: İKSV, Zorlu PSM, AKM, ENKA Sanat, CRR,
   Harbiye Açıkhava, KüçükÇiftlik Park · Dünya: Barbican, Southbank Centre,
   Philharmonie de Paris, Elbphilharmonie, Lincoln Center
2. **Biletleme platformları** — Biletix, Passo, Biletinial, Bugece, Mobilet
   (yeni satışa çıkanlar, fiyat kademeleri, tükenme hızı sinyalleri)
3. **Kültür-sanat basını** — Time Out İstanbul, Milliyet Sanat, Unlimited, Argonotlar
   + uluslararası sektör basını (The Stage, Pollstar)

## Adım adım yordam
1. Dönemi sabitle: son 7 gün duyuruları + gelecek 90 gün programı.
2. Her kaynaktan sinyal çıkar. Sinyal türleri: **program** (yeni sezon/festival/tur),
   **bilet** (fiyat, abonelik, indirim, tükenme), **format** (yeni tür/mekân/deneyim),
   **kitle** (hedef segment hamlesi).
3. Her sinyali tek satıra damıt: `[tür] kurum — ne yaptı — kaynak+tarih — fırsat/tehdit/nötr`.
4. Kıyas tablosunu doldur:

| Kurum | Öne çıkan program | Fiyat aralığı | Format hamlesi | Kültür AŞ'ye not |
|---|---|---|---|---|

5. En güçlü 5 sinyali seç (etki × yakınlık × kanıt gücü) → `/haftalik-tarama-raporu`na aktar.

## Kurallar
- Kaynaksız/tarihsiz sinyal yazma; erişilemeyen sayfayı "erişilemedi" diye işaretle, uydurma.
- Fiyatları para birimi + tarih ile ver; kur çevirisi yapıyorsan kuru not et.
- Kamu kurumu dili: kıyas kurumu, ölçülü ifade, doğrulanabilir iddia.

## Referanslar
Kaynak listesi büyürse `references/kaynaklar.md` altına taşı; ana dosya kısa kalsın.
