---
name: sky-import-export
description: >-
  Toplu veri içe/dışa aktarım: CSV ve Excel (xlsx) içe aktarma sihirbazı (yükle → sütun eşle →
  önizle → doğrula → içe aktar), Türkçe CSV tuzakları (ayraç ;, BOM, Windows-1254 kodlama,
  virgüllü ondalık, gg.aa.yyyy tarih), satır bazlı hata raporu, kısmi başarı, tekrar eden kayıt
  tespiti, büyük dosyalarda stream ve arka plan işi, dışa aktarma (filtreli CSV/Excel), şablon
  dosya indirme. "Excel'den müşteri yükle", "CSV içe aktar", "dışa aktar" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · İçe / Dışa Aktarım

## İçe aktarma sihirbazı (insanların bayıldığı akış)

```
1. Yükle      → sürükle-bırak CSV/XLSX + "Örnek şablonu indir"
2. Eşle       → dosya sütunları ↔ alanlar (otomatik tahmin: "Ad Soyad"→name, "Telefon"/"GSM"→phone)
3. Önizle     → ilk 20 satır, hücre bazında hata işaretleri (kırmızı), satırı düzelt/atla
4. Seçenekler → tekrar edenler: atla / güncelle / yeni oluştur
5. İçe aktar  → ilerleme çubuğu; bitince özet: "1.180 eklendi · 34 güncellendi · 12 hata (raporu indir)"
```
Hazır bileşen: **Flatfile / OneSchema / CSVBox** (ücretli) veya `react-spreadsheet-import` (açık kaynak).

## Türkçe CSV tuzakları

| Sorun | Çözüm |
|---|---|
| Excel TR'de ayraç `;` | Ayraç otomatik algıla (Papa Parse `delimiter: ""`) |
| Türkçe karakterler bozuk (Ä±, ÅŸ) | Kodlamayı algıla: UTF-8 (BOM'lu/BOM'suz) değilse **Windows-1254** dene (`TextDecoder("windows-1254")`) |
| `1.234,56` | Locale'e göre sayı parse: binlik `.` sil, `,` → `.` |
| `05.11.2026`, `5/11/2026` | Birden çok tarih biçimini dene, belirsizse (05/11) kullanıcıya biçim sor |
| Telefon `0532 123 45 67`, `+90 (532)…` | Normalize → E.164 `+905321234567` |
| Excel'de telefon sayıya dönüşüp baştaki 0 kaybolmuş | 10 haneli ve 5 ile başlıyorsa `0` ekle |
| Boş satırlar, birleştirilmiş başlıklar | Tamamen boş satırları at; ilk boş olmayan satır başlık |

Excel için `exceljs` / SheetJS; formül hücrelerinde değeri (`result`) oku.

## Doğrulama ve hata raporu

- Her satır Zod şeması ile; hata: `{ row: 47, column: "telefon", value: "123", message: "Geçerli bir cep telefonu değil" }`.
- **Kısmi başarı**: geçerli satırları içe aktar, hatalıları rapor et (tümünü reddetme) — kullanıcı tercihine bağlı seçenek.
- Hata raporu: orijinal dosya + "Hata" sütunu eklenmiş CSV — düzeltip tekrar yükleyebilsin.

## Tekrar eden kayıtlar

- Eşleşme anahtarı: telefon (normalize), e-posta (lower), ya da harici ID sütunu.
- Dosya içi tekrarlar da tespit edilir.
- Seçenek: atla / güncelle (boş hücreler mevcut değeri silmesin) / her zaman yeni.

## Büyük dosyalar

- 5MB+ veya 10k+ satır → dosyayı depolamaya yükle (bkz. `sky-storage`), arka plan işi (bkz. `sky-jobs`) stream ile parse eder.
- 500'lük partilerle `insert … on conflict` (bkz. `sky-sql` upsert), her parti ayrı transaction.
- İlerleme yüzdesi canlı; bitince bildirim/e-posta.
- Geri alma: içe aktarım ID'si her kayıtta → "Bu içe aktarımı geri al" (24 saat).

## Dışa aktarma

- Mevcut filtreler/sıralama ile (bkz. `sky-dashboard`); "Görünen sütunlar" veya "Tüm alanlar" seçimi.
- CSV: UTF-8 **BOM** + `;` ayraç (TR Excel'de çift tıkla düzgün açılsın) veya kullanıcıya "Excel uyumlu / Standart" seçimi.
- XLSX: başlık satırı kalın + dondurulmuş, sütun genişlikleri, tarih hücreleri gerçek tarih tipi, para biçimi.
- Büyük dışa aktarım arka planda + indirme bağlantısı; dosya adı `musteriler-2026-11-04.xlsx`.
- Kişisel veri dışa aktarımı audit log'a yazılır (kim, ne zaman, kaç kayıt).

## Şablon dosya

"Örnek şablonu indir": doğru başlıklar, 2 örnek satır, açıklama sayfası (xlsx'te ikinci sekme: alanlar, zorunluluk, biçimler).
Bu basit şey destek taleplerini yarıya indirir.

## Diğer kaynaklardan göç

Rakip uygulamalardan geçişte ("X'ten taşı") hazır eşleme profilleri — kullanıcılar sihirbazda kaynağı seçer,
sütunlar otomatik eşlenir. Satış için güçlü bir koz.
