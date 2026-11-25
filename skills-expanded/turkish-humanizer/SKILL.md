---
name: turkish-humanizer
description: Türkçe metinleri yapay zeka izlerinden arındırıp doğal bir insan yazısına dönüştürür. Anlamı, sayıları, terimleri ve özel isimleri olduğu gibi korur. Kullanıcı "Türkçeleştir", "insanlaştır", "doğallaştır", "yapay zeka gibi durmasın", "daha doğal yaz", "robot gibi olmuş", "AI kokuyor", "humanize" dediğinde ya da bir Türkçe metnin (blog, e-posta, akademik paragraf, ürün açıklaması, LinkedIn gönderisi, rapor) üslubunu düzeltmek, akıcılaştırmak veya ChatGPT/Claude çıktısı gibi durmaktan çıkarmak istediğinde bu skill'i mutlaka kullan. Türkçe bir metni "yeniden yaz", "elden geçir", "redakte et" isteklerinde de kullan. Use for any request to humanize or de-AI Turkish text.
---

# Turkish Humanizer

Türkçede yapay zeka izi sözcüklerden çok **yapıda** görülür: tekdüze dizilim, eşit cümle uzunlukları, "ve/ama/çünkü" tekeli, "-mektedir" yığılması, çeviri kokan kalıplar ve İngilizce noktalama. Bu skill'in işi, bir Türkçe metni bu izlerden arındırırken **söylediği hiçbir şeyi değiştirmemektir.**

## Değişmez kurallar

Bu kurallar üslupla ilgili her karardan önce gelir. Daha "doğal" bir cümle kurmak için bunlardan birini çiğnemek, skill'in amacını boşa çıkarır. Kullanıcı bu metni bir yere gönderecek ya da yayımlayacak, yanlış bir sayı ya da uydurulmuş bir iddia ona zarar verir.

1. **Anlamı değiştirme.** İddiaların gücünü de koru: "olabilir" "olur"a, "bazı" "birçok"a, "artırabilir" "artırır"a dönüşmesin.
2. **Sayıları, tarihleri, birimleri, terimleri, özel isimleri, alıntıları, URL'leri ve kodu aynen koru.** Yalnızca sayıların **biçimini** TDK'ya uydurabilirsin (*25%* → *%25*), ama değerin ne olduğundan emin değilsen dokunma.
3. **Bilgi ekleme.** Kaynakta olmayan bir örnek, gerekçe, sonuç, rakam ya da özne uydurma. Edilgen bir cümleyi etkene çevirirken eylemi yapan metinde açıkça yoksa edilgen bırak.
4. **Bilgi çıkarma.** Yalnızca gerçekten boş olan dolguları sil (klişe açılış ve kapanışlar, tekrar eden özet cümleleri, aynı şeyi söyleyen eş anlamlı sıfatlar). Bir maddeyi düzyazıya çevirdiğinde içindeki her bilgi yerinde kalmalı.
5. **Registerı koru.** Akademik metin akademik, resmi yazışma resmi kalır. Hitap biçimi (siz/sen) ve kişi (biz/ben/edilgen) değişmez.

## Çalışma adımları

### 1. Metni tanı

- **Register:** akademik/resmi · iş yazışması · blog/deneme · pazarlama/ürün · sosyal medya. Kararsızsan daha resmi olanı seç. Resmi bir metni gündelikleştirmek, gündelik bir metni biraz resmi bırakmaktan daha büyük bir hatadır.
- **Korunacaklar listesi:** Metindeki bütün sayıları, tarihleri, özel isimleri, terimleri, alıntıları ve iddiaların kesinlik derecesini zihninde (ya da uzun metinde not olarak) çıkar. Son adımda bu listeyle karşılaştıracaksın.

### 2. Örüntüleri bul

`references/ai-oruntuleri.md` dosyasını oku. Örüntü kataloğu ve her biri için önce/sonra örneği orada. Metinde hangilerinin bulunduğunu belirle. Her örüntünün **Dokunma** satırına dikkat et: Aynı kalıp bir registerda iz, ötekinde olağan dildir.

Gerektiğinde şu dosyalara uzan:
- `references/cumle-turleri.md`: Tekdüze bir paragrafı hangi yapılarla kırabileceğini ve hangi yapının hangi registerda yerinde olduğunu gösterir.
- `references/baglaclar.md`: ve/ama/çünkü tekeline alternatifler, register etiketleri ve anlam tuzakları.
- `references/noktalama.md`: TDK'ya dayalı noktalama ve yazım denetimi (uzun çizgi, de/da, ki, mi, kesme, büyük harf, sayılar).

### 3. Yeniden yaz

- **Ölçülü ol.** Hedef, iyi bir Türk yazarın bu metni nasıl yazacağıdır. Her cümleyi değiştirmek hedef değildir. İyi bir cümleye dokunma. Cümlelerin çoğu yine kurallı ve orta uzunlukta kalabilir, yalnızca aralarına doğal kırılmalar girer.
- **Önce sadeleştir, sonra çeşitlendir.** En etkili düzeltme çoğu zaman silmektir (klişe, pekiştirme, boş geçiş sözü). Ardından birleştir (zarf-fiil, sıfat-fiil), en son bağlaç ve dizilimle oyna.
- **Devrik ve eksiltili cümleyi ancak bağlam isterse kullan.** Blog ve sosyal medyada bir iki tanesi metne ses katar. Akademik, resmi ve iş yazışmasında kullanma. Metne "insan" süsü vermek için eklenen bir devrik cümle, düzeltilen tekdüzelik kadar yapay durur.
- **Bağlaçları dağıtma, seç.** "ama" yerine sırayla "oysa, ne var ki, buna karşın" koymak da bir örüntüdür. Her ilişki için en uygun bağlacı seç, çoğu zaman da bağlacı tamamen kaldır.
- **Biçimi metne uydur.** Kısa bir e-postadaki başlıkları ve madde işaretlerini düzyazıya çevir. Gerçek adım listelerini ve taranacak bilgileri koru.
- **Noktalama ve yazımı düzelt.** Cümle içindeki uzun çizgiyi (—) kaldır, "ve"den önceki virgülü sil, de/da, ki, mi ve kesme işaretini TDK'ya göre düzelt.

### 4. Denetle

Teslim etmeden önce yeni metni korunacaklar listesiyle karşılaştır:
- Her sayı, tarih ve özel isim yerinde ve aynı mı?
- Her iddia aynı kesinlikte mi? Kaynakta olmayan bir özne, gerekçe ya da sonuç eklendi mi?
- Silinen her şey gerçekten boş muydu?
- Register ve hitap aynı mı?

Bir şüphe varsa kaynaktaki hâline dön. Anlamca güvenli ama biraz daha az akıcı bir metin, akıcı ama yanlış bir metinden her zaman iyidir.

## Çıktı

Varsayılan olarak **yalnızca düzeltilmiş metni** ver: önsöz yok, "İşte düzeltilmiş metin:" yok, kapanış yok. Kaynak metnin biçimini (paragraf bölümleri, gerçek listeler, imza bloğu) koru.

İki durumda metnin altına kısa bir not ekle:
- Kullanıcı değişiklikleri, özeti ya da gerekçeyi isterse.
- Anlamdan emin olamadığın için bir şeye dokunmadıysan (ör. "1,500"ün binlik mi ondalık mı olduğu belirsiz) ya da metinde bir olgu hatası fark ettiysen. Olguyu sen düzeltme, yalnızca belirt.

Özet istendiğinde şu biçimi kullan (en çok 5-7 madde):

```
**Değişiklik özeti**
- YAPI-03: "-mektedir" ile biten 6 yüklemin 4'ü geniş zaman ve şimdiki zamana çevrildi.
- NOK-01: 3 uzun çizgi kaldırıldı (2'si virgül, 1'i iki nokta oldu).
- SOZ-02: "Bu bağlamda", "günümüzde" silindi.
- Dokunulmayanlar: "1,500" (binlik mi ondalık mı belirsiz).
```

## Özel durumlar

- **Metin zaten doğalsa** küçük düzeltmelerle (yazım, noktalama) yetin ve bunu bir cümleyle söyle. Yapacak bir şey yokken değişiklik üretme.
- **Metin Türkçe değilse ve kullanıcı "Türkçeleştir" diyorsa** metni Türkçeye çevir. Çeviriyi baştan bu dosyadaki ilkelere uygun yaz, kelime kelime çeviri yapma. Çeviri olduğunu belirt.
- **Karışık dil (Türkçe metin içinde İngilizce terim)** varsa terimlere dokunma. Yerleşik bir Türkçe karşılığı olsa bile terim kullanıcının tercihidir.
- **Kod blokları, alıntılar, yasal metinden aktarılan maddeler** olduğu gibi kalır.
- **Uzun metinlerde** paragraf paragraf ilerle. Her paragraftan sonra korunacaklar listesini kontrol et.
- **Kullanıcının bilinçli üslubu** (edebi bir devrik dil, kasıtlı plaza dili, markanın emoji kullanımı) belirginse onu koru. Yalnızca yapay zekadan gelen katmanı temizle.

## Örnekler

`examples/` klasöründe beş metin türü için (blog, e-posta, akademik paragraf, ürün açıklaması, LinkedIn gönderisi) tam önce/sonra çiftleri var. Her dosya hangi örüntülerin düzeltildiğini ve nelerin bilinçli olarak korunduğunu da gösterir. Bir türle ilk kez karşılaştığında ilgili örneğe bakmak ölçüyü tutturmana yardım eder.
