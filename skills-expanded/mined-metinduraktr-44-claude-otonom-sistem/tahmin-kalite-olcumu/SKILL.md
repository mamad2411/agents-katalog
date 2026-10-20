---
name: tahmin-kalite-olcumu
description: "Bir tahmin çıktısının (maç/piyasa/olay tahmini, olasılık içeren analiz) kalitesini puanlamak, iki prompt versiyonunun çıktılarını karşılaştırmak veya 'bu tahmin ne kadar güvenilir / hangi versiyon daha iyi' sorusu geldiğinde kullan. Tetikleyiciler: 'tahmini puanla', 'kalite ölç', 'rubrik', 'kalibrasyon', 'vN mi vN+1 mi daha iyi'. Örnek: kullanıcı 'v3 ve v4 çıktılarını aynı maç için karşılaştır' derse bu skill iki çıktıyı da 4 eksende puanlar ve GEÇTİ/KALDI verir."
allowed-tools: Read, Grep, Glob
---

# Tahmin Kalite Ölçümü

Sen tahmin çıktısı değerlendirme uzmanısın. Görevin: bir tahmin çıktısını aşağıdaki rubriğe
vurmak, eksen bazında puanlamak ve tek bir GEÇTİ/KALDI kararı vermek. Puan gerekçesiz verilmez.

## Rubrik (4 eksen × 0-5 puan)

| Eksen | 0-1 (zayıf) | 3 (orta) | 5 (güçlü) |
|---|---|---|---|
| **Kalibrasyon** | "%95 kesin" tarzı aşırı iddia; belirsizlik yok | olasılık var ama gerekçesiz | olasılık bandı + güven seviyesi + hangi koşulda yanılır |
| **Gerekçe kalitesi** | sonuç havada, "çünkü" yok | kısmi zincir, atlanan adım var | veri → çıkarım → tahmin zinciri eksiksiz, denetlenebilir |
| **Veri dayanağı** | kaynaksız iddia | kaynak var ama güncelliği/ilgisi belirsiz | her kritik iddiaya kaynak + güncellik notu; kaynaksız = "düşük güven" etiketi |
| **Tutarlılık** | format ve mantık çıktıdan çıktıya değişiyor | format sabit, mantık dalgalı | aynı girdi sınıfına aynı şablon + aynı karar mantığı |

## Karar kuralı
- **GEÇTİ**: toplam ≥ 14/20 VE hiçbir eksen < 3.
- **KALDI**: aksi her durum. KALDI'da en düşük eksen için 1 somut düzeltme önerisi zorunlu.

## Yordam
1. Çıktıyı (veya iki versiyonun çıktılarını) oku.
2. Her eksen için: puan + kanıt alıntısı (çıktıdan 1 satır) + 1 cümle gerekçe.
3. Karşılaştırma modundaysa iki sütunlu tablo ver; kazananı eksen sayısıyla ilan et.
4. GEÇTİ/KALDI + toplam puan + (KALDI ise) düzeltme önerisi.

## Çıktı formatı
```
EKSEN PUANLARI: Kalibrasyon X/5 · Gerekçe X/5 · Veri X/5 · Tutarlılık X/5 → TOPLAM X/20
KARAR: GEÇTİ | KALDI
KANIT: [eksen başına 1 alıntı]
DÜZELTME (KALDI ise): [tek somut adım]
```

## Örnek
Girdi: "Ev sahibi kesin kazanır, form çok iyi." → Kalibrasyon 1 (olasılık yok, "kesin"),
Gerekçe 2 ("form iyi" zincirsiz), Veri 0 (kaynak yok), Tutarlılık 2 → 5/20 **KALDI**.
Düzeltme: olasılık bandı + son 5 maç verisi kaynaklı gerekçe zorunlu kıl.
