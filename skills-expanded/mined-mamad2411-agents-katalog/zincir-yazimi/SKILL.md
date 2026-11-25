---
name: zincir-yazimi
description: X zinciri ve lansman postu yazar: açılış hem kancalar hem ödülü vaat eder, her gönderi bir sonrakini hak eder, kapanış tek çağrıyla biter — ve "bu aslında zincir değil, tek post olmalı" itirazını söyleme izni vardır. Twitter içerik takımı article paketinin lansman postlarını yazarken okur.
kaynak: https://github.com/social-media-skills/skills/blob/main/skills/thread-writer/SKILL.md (commit 6e30eeb, 2026-07-19)
lisans: MIT
uyarlayan: A Şirketi (2026-09-11)
takimlar: [twitter-icerik]
---

# Zincir yazımı

Zincir metinde çalışan bir **tutma makinesidir**: her gönderi bir sonrakini hak etmek zorundadır,
yoksa okuyan düşer. Bloğu parçalara bölmek zincir değildir; tek posttan kötüdür.

## Üç ilke
1. **Açılış işin tamamıdır.** 1. gönderi hem **durdurur** hem **ödülü vaat eder**. Paylaşılan gönderi de
   odur; erişim orada yaşar ya da ölür.
2. **Zincirde tek fikir, gönderide tek fikir.** Zincir tek bir noktaya varır; her gönderi onu bir adım ilerletir.
3. **Her gönderi bir sonrakini hak eder.** Ölçü momentumdur. İleri çekmeyen gönderi kesilir.

## Ne zaman
- Gece article paketi hazırlandığında: **lansman postu** ve **quote repost** varyantları.
- Yayınlanan bir videonun tek bir tezini X'te anlatmak gerektiğinde.
- `x-icerik` bir kaynağı "yazıya değer" işaretlediğinde.

## Adımlar
1. **Tek fikri, ödülü ve formatı sabitle.**
   - Tek fikir: zincirin vardığı tek nokta.
   - Ödül: okuyan sonunda **ne alıyor** (ders, liste, sonuç, dosya).
   - **Zincir mi tek post mu?** Fikir gerçekten birkaç adım istemiyorsa **tek keskin post her zaman
     zorlanmış zinciri yener.** Öyleyse bunu söyle ve tek postu yaz.
2. **Açılışı yaz** (`kanca-yazimi` ile). İki işi aynı anda yapmalı: gerçek bir mekanizmayla kancalamak
   ve ödülü vaat etmek. Açılış **tek başına** güçlü bir post olmalı. Yavaş giriş yok.
3. **Omurgayı kur.** Yapı: liste · hikâye · argüman · nasıl yapılır · çözümleme.
   Açılışın vaadi ve onu ödeyen sıralı gönderiler. Omurga, zinciri "doğranmış makale"den ayıran şeydir.
4. **Gövde gönderilerini yaz.** Her gönderi: noktayı öne yükle, tek adım ilerlet, karakter sınırında kal,
   ve **ileri çek** (mini kanca, numara, "ama asıl mesele şu"). Boğaz temizleyen gönderiyi kes.
5. **Kapanış ve tek çağrı.** Son gönderi ödülü indirir, sonra **tek** istek yapar.
   Bağlantı buraya ya da ilk cevaba.
6. **Biçim.** Numaralandırma yönelim sağlıyorsa kullan; cümleyi ortadan bölme; gönderi içinde satır arası kullan.
7. **Teslim.** `takimlar/twitter-icerik/cikti/<tarih>-<slug>/00-BURADAN-BASLA.md` içine:
   lansman postu + quote repost varyantları + **karakter sayıları**.

## Çıktı şablonu

```
# Lansman — <article başlığı>

**Tek fikir:** ... · **Ödül:** ... · **Zincir mi tek post mu:** zincir (5 gönderi) — gerekçe: ...

## Açılış (paylaşılan gönderi)
<metin>
— 217 karakter · mekanizma: bedel · ödül vaadi: "hangi üç şeyin işe yaramadığı"

## Gövde
2/ <metin> — 198 karakter
3/ ...

## Kapanış
5/ <metin> + tek çağrı — 176 karakter

## Quote repost varyantları
- A: <metin> — 142 karakter
- B: <metin> — 159 karakter

## Söylenen sayılar
| Sayı | Etiket | Kaynak |
|---|---|---|
```

## Kalite kontrol listesi
- [ ] Açılış hem kancalıyor hem ödül vaat ediyor, tek başına da güçlü mü?
- [ ] Tek fikir mi, her gönderide tek fikir mi?
- [ ] Her gönderi ileri çekiyor mu (dolgu gönderi var mı)?
- [ ] Her gönderinin karakter sayısı yazılı mı?
- [ ] Kapanışta ödül + **tek** çağrı var mı?
- [ ] **"Bu aslında tek post olmalı" ihtimali değerlendirildi mi?**
- [ ] Her sayı ✅ etiketli ve kaynaklı mı?
- [ ] Doğranmış makale mi olmuş, yoksa native zincir mi?

## Yasaklar (ANAYASA)
- **X'e yazmak, göndermek, zamanlamak — kesinlikle yasak** (§1). Tarayıcıyla X'e yazmak hesabı riske atar.
  Taslak yazılır, gönderme patronun.
- 🟡 / ⛔ sayı, üçüncü taraf gelir rakamı (§2). Açılış gönderisi en çok paylaşılan yerdir; en sıkı yer orasıdır.
- Başkasının zincirini birebir çevirmek. Yapı incelenir, cümle alınmaz.
- İki çağrı. Bir zincir bir şey ister.
- Kendi takımının dışındaki bir klasöre yazmak (§5) — başka takımın klasörü salt okunur.

## Öğrenilenler
Bu skill koşuda aldığı veriyle **kendini geliştirir**: hangi açılış mekanizması bu hesapta tuttu,
hangi zincir tek post olmalıymış — `defter.md`'ye tek ders yaz. Üç koşuda tekrarlanan ders için koşu
kaydına "yetenek önerisi: `zincir-yazimi` → ## Öğrenilenler" satırı düş.

- (henüz ders yok)

## Kaynak ve değişiklikler
**Alındığı yer:** `social-media-skills/skills` → `thread-writer`, MIT.

**Orijinalden alınanlar:** üç ilke (**açılış işin tamamıdır** · zincirde tek fikir, gönderide tek fikir ·
her gönderi bir sonrakini hak eder); adım sırası (tek fikir + ödül + zincir mi → açılış → omurga →
gövde → kapanış + tek CTA → biçim); **"tek post daha güçlüyse bunu söyle ve tek postu yaz"** izni;
açılışın tek başına paylaşılabilir bir post olması; **doğranmış makale zincir değildir** kuralı;
"ileri çekmeyen gönderiyi kes"; tek CTA; numaralandırma ve cümleyi ortadan bölmeme; kalite listesi mantığı.

**Değiştirilenler:**
- **En sert değişiklik:** orijinal "WoopSocial ile açılışı zamanla, zinciri elle at" diyor. Bizde
  ANAYASA §1 gereği **X'e yazmak kesinlikle yasak** — tarayıcıyla X'e yazmak hesabın askıya alınmasına
  yol açar. Bütün yayın adımları çıkarıldı; çıktı yalnızca taslaktır.
- Threads (Meta) karşılaştırması çıkarıldı — tek platform X.
- **Karakter sayısı yazma zorunluluğu** eklendi (orijinalde yok): paketin `00-BURADAN-BASLA.md`
  sözleşmesi karakter sayılarını istiyor.
- Çıktı `twitter-icerik` takımının klasör sözleşmesine bağlandı (lansman postu + quote repost varyantları).
- ANAYASA §2 eklendi: yalnızca ✅ sayılar; açılış gönderisi için özel vurgu.
- Başka takımın klasörünün salt-okunur olduğu (§5) açıkça yazıldı.
