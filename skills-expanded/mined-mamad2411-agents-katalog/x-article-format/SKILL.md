---
name: x-article-format
description: X Article (uzun yazı) paketinin biçim otoritesi — uzunluk, iskelet, tablo yasağı, görsel işaretleri, lansman postu ve son kontrol listesi. twitter-icerik takımı kullanır.
kaynak: A Şirketi kitinin kendi üretimi — dış kaynak yok
lisans: —
uyarlayan: A Şirketi kiti (2026-09-11)
takimlar: [twitter-icerik]
---

# X Article formatı

## 1 · Konu article mı, post mu
Article olur: konu tek gözlemden büyükse, adım adım kurulan bir sistem varsa, okurun uygulayabileceği
bir reçete çıkıyorsa. Post olur: tek keskin gözlem, tek ekran görüntüsü, tek cümlelik itiraz.
Şüphedeysen post yaz — zorlanmış article okunmaz.

## 2 · Uzunluk ve iskelet
- Gövde **1.000-2.000 kelime**, **3-7 bölüm**, her bölüm tek fikir.
- Başlık 6-12 kelime ve **gövdenin içinde tekrar edilmez** (X başlığı ayrı alanda gösterir).
- Açılış: okurun tanıdığı somut bir durum, iki-üç cümle. Soyut giriş yok.
- Her bölüm bir `##` başlıkla açılır; başlık iddia taşır ("Bekçi neden ayrı kafa olmalı"),
  etiket taşımaz ("Giriş", "Sonuç").
- Kapanış: okurun bugün yapabileceği tek şey.

## 3 · Yasaklar
- **Tablo yok** — ne markdown, ne `<table>`, ne boşlukla hizalanmış sahte tablo. X Article tabloyu
  taşımaz; yapıştırınca dağılır. Karşılaştırma **kalın etiketli maddeye** dönüşür:
  `**Yerel koşu** — 2 USD tavan, 15 dk, makinede.`
- **Kod bloğu yok.** Tek satırlık komut satır içi `kod` olur; çok satırlı her şey görsele gider.
- **Markdown link yok** — X Article çıplak URL'i kendi linkler. `[metin](url)` yapıştırınca bozulur.
- **İç içe liste yok.** Tek seviye madde.
- Kişi adı yok; kaynaktaki insanlar rolüyle anılır. İstisna: kendi hesabın.
- Kaynaksız sayı yok. Her iddia ✅/🟡/⛔ etiketiyle doğrulanmış olmalı.

## 4 · Görseller
Görsel yerleri gövdede **kendi satırında** durur:
`[GÖRSEL 2: dongu-semasi.png — kuyruktan koşuya kadar akış]`
Yayın günü bu satır silinir, yerine görsel konur. Görsel sayısı 2-5; her biri bir bölümü kanıtlar.
Kapak: 3840×736 (5,2:1), tek satır başlık, `bin/kapak_uret.py`.

## 5 · Lansman postu ve quote repost
- Lansman postu 3 varyant; her biri link payıyla birlikte **255 karakterin altında**.
  İlk satır kancadır, article'ın başlığını tekrar etmez.
- Quote repost 3 varyant; yayından 3-6 saat sonra atılır, lansman postunun cümlesini tekrar etmez,
  yazının **ikinci** en iyi fikrini öne çıkarır.
- Karakter sayıları `00-BURADAN-BASLA.md` içinde yazılı olur.

## 6 · Bitirmeden önce (kontrol listesi)
- [ ] Tablo yok (hiçbir dosyada)
- [ ] Markdown link yok, çıplak URL var
- [ ] İç içe liste yok
- [ ] Başlık gövdede geçmiyor
- [ ] Her görsel işareti tek satırda
- [ ] Lansman postu 255 karakter altında
- [ ] Quote varyantları lansmanı tekrar etmiyor
- [ ] Uydurma sayı yok; her iddia etiketli
- [ ] Kişi adı yok
- [ ] `article.html` tek başına açılıyor, kopyala butonu çalışıyor

## Öğrenilenler
Bu yetenek koşuda aldığı veriyle **kendini geliştirir**: hangi kural pakete gerçekten yaradı, hangi
madde boşuna yer tuttu — `takimlar/twitter-icerik/defter.md`'ye tek ders olarak yaz. Aynı ders üç
koşuda tekrar ediyorsa koşu kaydına "yetenek önerisi: `x-article-format` → ## Öğrenilenler'e şu satır
eklensin" yaz; kararı patron verir, yeteneği kendi başına değiştirme.

- (henüz ders yok)
