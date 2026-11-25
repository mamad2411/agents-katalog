---
name: mahalle-avcisi
description: Semtte sitesi olmayan esnafı bulur, satış şansına göre puanlar, her birine kendi adıyla site kurar ve satılan siteyi gerçek fotoğraf/fiyatla yayına hazırlar. "mahalle avcısı", "esnaf tara", "sitesi olmayan dükkân", "/mahalle-avcisi" denince kullan.
---

# Mahalle Avcısı

Bu klasördeki `mahalle_avcisi.py` her şeyi yapar. Python 3.9+ yeter, kurulum ve API anahtarı yok. Veri OpenStreetMap'ten gelir.

## 1. Tara
Kullanıcı semt verdiğinde:
```
python3 mahalle_avcisi.py tara "<Semt>, <İl>"
```
- Mahalle küçükse ya da sınır bulunamadıysa: `--yaricap 900` ekle.
- Çıktı: `ciktilar/<semt>/dukkanlar.csv` ve `.json`. İlk 10'u kullanıcıya tablo olarak göster.
- Puan bir öncelik sırasıdır, kesin tahmin değil. Bunu kullanıcıya böyle anlat.

## 2. Kur
```
python3 mahalle_avcisi.py kur --en-iyi 50
```
- Her dükkâna `ciktilar/<semt>/siteler/<dükkân>/index.html` kurulur, hepsi `galeri.html`'de toplanır.
- Kullanıcıya galeriyi tarayıcıda aç: `open ciktilar/<semt>/galeri.html` (macOS).
- Sektöre göre metin ve hizmet listesi `sablonlar/sektorler.json`'dan gelir; tasarım `sablonlar/site.html`. Kullanıcı tasarım değişikliği isterse şablonu değiştir, `kur` komutunu tekrar çalıştır.

## 3. Satılan siteyi hazırla
Kullanıcı "şu dükkân evet dedi" dediğinde:
1. Siteyi `ciktilar/<semt>/siteler/<dükkân>/` içinde düzenle (yeni klasöre kopyalama).
2. `<!-- TASLAK -->` yorumu ve altındaki `.taslak` bandını sil.
3. Kullanıcının verdiği fotoğrafları `img/` klasörüne koy; uzun kenarı 1600 px, JPEG kalite 80'e küçült (`sips -Z 1600` macOS'ta hazır). Kahraman bölümüne bir fotoğraf, altına 4–8 fotoğraflık galeri ekle; her `<img>`'e anlamlı Türkçe `alt` ve `loading="lazy"` yaz.
4. "Fiyat için arayın" satırlarını gerçek fiyatlarla değiştir. Fiyat verilmediyse olduğu gibi bırak; asla fiyat uydurma.
5. Slogan ve hizmet açıklamalarını dükkânın kendi diline göre yeniden yaz. Yorum, ödül, "en iyi", müşteri sayısı gibi doğrulanmamış iddia ekleme.
6. `<title>`, `meta description` ve JSON-LD'yi güncelle (alan adı belli ise `url` ekle).
7. Telefon genişliğinde (390 px) ekran görüntüsü alıp kontrol et: taşan yazı, kırık görsel, çalışmayan buton olmasın.
8. Yayın seçeneklerini `satis-kiti/03-satistan-sonra.md`'den anlat. Kullanıcının hesabına kendin bir şey yükleme; adımları ver.

## Kurallar
- Taslak siteleri kullanıcı açıkça istemedikçe internete koyma. Dükkân onay vermeden yayına alınmaz.
- Toplu SMS/WhatsApp gönderme işi yapma; satış yüz yüze yapılır.
- OpenStreetMap atfı ("© OpenStreetMap katkıcıları") sitelerin altında kalsın.
