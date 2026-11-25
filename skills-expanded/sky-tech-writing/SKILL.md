---
name: sky-tech-writing
description: >-
  Teknik yazım ve geliştirici içeriği: net ve tarayılabilir yazı ilkeleri, tutorial / how-to /
  referans / açıklama ayrımı (Diátaxis), adım adım rehber yazma, kod örneği kuralları (çalışır,
  tam, güvenli), API ve README yazımı, blog yazısı ve teknik makale yapısı, sürüm notları ve
  hata mesajı metni, görsel/diyagram kullanımı, Türkçe teknik yazım ve terim tutarlılığı,
  AI ile taslak ve düzenleme. Dokümantasyon, blog, rehber veya teknik metin yazarken kullan.
disable-model-invocation: true
---

# Sky · Teknik Yazım

Doküman **sitesi** altyapısı `sky-docs-site`, arayüz metni `sky-ux-writing`, mimari belge `sky-architecture-docs`. Burada **yazının kendisi**.

## İlkeler

- Önce okuyucu ve amaç: kim, ne yapmaya çalışıyor, ne biliyor? Buna göre seviye ve kapsam.
- **Tarayılabilir**: anlamlı başlıklar, kısa paragraflar (3–4 satır), listeler, tablolar, kod; önemli bilgi başta (ters piramit).
- Net ve kısa: gereksiz kelime yok ("şunu belirtmek gerekir ki" → sil), edilgen yerine etken, somut. Bir cümle bir fikir.
- Tutarlı terim: aynı şey için tek kelime (bkz. `sky-ux-writing` sözlük); kısaltmayı ilk kullanımda aç.

## İçerik türü (Diátaxis)

| Tür | Amaç | Ton |
|---|---|---|
| **Tutorial** | öğrenme, ilk başarı | elinden tut, tek yol, "biz" |
| **How-to** | belirli görevi çözme | adım adım, varsayılan bilgi |
| **Referans** | bilgi arama | kuru, eksiksiz, tutarlı |
| **Açıklama** | anlama, "neden" | kavramsal, bağlam |
Karıştırma: tutorial'a 40 seçenekli referans tablosu koyma, referansa hikâye anlatma.

## Adım adım rehber

Hedef cümlesi ("Bu rehberin sonunda … yapabileceksin"), ön koşullar, numaralı adımlar (her adım tek eylem + beklenen sonuç + "şunu görmelisin"), sık hatalar, doğrulama, sonraki adımlar. Kullanıcının göreceği tam çıktıyı/ekranı göster.

## Kod örnekleri

- **Çalışır ve tam**: kopyala-çalıştır; eksik `...` yerine gerçek kod veya açık yer tutucu. Mümkünse örnekleri test et (bkz. `sky-docs-site`).
- Güvenli: örnekte bile sır yok, kötü kalıp yok (yeni başlayan kopyalar); dosya adı ve dil etiketi; vurgulanacak satır.
- Minimum: konuyu gösteren en küçük örnek, ilgisiz koddan arındırılmış.

## README ve API

README: tek cümle ne + demo/ekran görüntüsü + hızlı başlangıç + ana kullanım + bağlantılar (bkz. `sky-architecture-docs`). API dokümanı: her uç nokta/fonksiyon için ne yapar, parametreler (tip, zorunluluk, varsayılan), dönüş, hatalar, örnek istek+yanıt.

## Blog / makale

Çekici ama dürüst başlık, ilk paragrafta değer ("bu yazıda … öğreneceksin / şu sorunu çözeceğiz"), problem → çözüm → sonuç, gerçek kod ve örnek, görseller, özet + sonraki adım. Clickbait ve doldurma yok. SEO için `sky-seo`.

## Diğer metinler

Sürüm notları fayda odaklı (bkz. `sky-changelog`), hata mesajları ne+nasıl (bkz. `sky-ux-writing`), commit/PR açıklamaları (bkz. `sky-git`).

## Görseller ve diyagram

Mimari/akış için Mermaid (metinle sürümlenir, bkz. `sky-architecture-docs`); ekran görüntüsü yerine mümkünse metin+kod (güncel tutması kolay), gerekirse açık/koyu versiyon ve `alt` metni; diyagram bir şeyi netleştirmeli, süslemek için değil.

## Türkçe teknik yazım

Tutarlı terim ve hitap (sen/siz — bkz. `sky-ux-writing`), doğru yazım (bkz. `sky-turkish-proofreader` agent'ı), İngilizce terimin ilk geçişte karşılığı, kod/komut/değişken adları İngilizce kalır. Çeviri değil, Türkçe düşünerek yaz.

## AI ile

Taslak ve yapı için AI iyi; ama teknik doğruluğu **sen** doğrula (halüsinasyon), örnekleri çalıştır, kendi sesini koru, jenerik AI dilini (aşırı "ayrıca", "sonuç olarak") temizle. Önce madde planı → sonra yazdır → sonra düzelt.
