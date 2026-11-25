---
name: deckcraft
description: "Bir oyuna deckbuilder tarafini kurar: kart cizimi, paket acma toreni, kart sanati eslemesi. ~/Projects/deckcraft paketini kullanir, oyunun veri modeline adapter ile baglar ve ise yarayan her bulguyu pakete geri yazar. Triggers: deckbuilder, kart tasarimi, kart cizimi, paket acma, pack opening, kart sistemi, deste sistemi, card frame, kart cercevesi, deckcraft."
user-invocable: true
argument-hint: "[hedef: kart | toren | ikisi]  (bos birakilirsa projeden cikarilir)"
---

# /deckcraft — deckbuilder tarafını kur

Kart çizimi ve paket açma töreni her oyunda sıfırdan yazılıyordu. `~/Projects/deckcraft`
o işin bir kez yapılmış hâli; bu skill onu **bu** oyuna bağlar ve bağlarken
öğrendiğini pakete geri yazar.

> Tek çizim · Ölçü tek nesnede · Paket oyunu bilmez

---

## Önce bilmen gereken: bu Three.js sahnesi değil

Paket **DOM + CSS**. Three.js kullanan oyunlarda `<canvas>`'ın ÜSTÜNDE ayrı bir
katman olarak çalışır, sahneyle aynı bağlamı paylaşmaz.

Bu bir eksiklik değil seçim, ve gerekçesi ölçülebilir: kartın gövdesi **metin**
— başlık, kural, etiket. DOM'da satır kırma, elipsis ve yazı tipi hinting'i
bedava; texture'a çizince her dil için yeniden ölçüp atlas üretmek gerekiyor.
Cozy'de kural metni 10px'te üç satır; bir piksel kayma kartı bozuyor.

Kâğıt bükülme efekti tek istisna: o zaten ham WebGL (`peel.js`), kendi
canvas'ında.

**Kullanıcı "Three.js mesh'i olsun" derse** bunu söyle, sonra istiyorsa yap —
ama metin ölçüsünün bedelini önceden yaz.

---

## Faz 1 — bağlan, yeniden yazma

Paketi kopyalama; **referansla** kullan. Oyunun build'ine `~/Projects/deckcraft/src/`
dosyalarını dahil et, sonra tek bağlantı noktasını doldur:

```js
deckcraft.init({
  card: id => {
    const c = OYUNUN_KART_TABLOSU[id];
    return { name: c.n, rules: c.tx, cost: c.act, tag: c.tags[0],
             tagColor: RENK[c.tags[0]], art: artKeyFor(c),
             seal: rarityOf(c) && "Seal_" + MUHUR[rarityOf(c).id],
             ingredient: c.ing };
  },
  art: key => ART[key],
  fonts: { CozyDisplay: FONT.display, CozyLabel: FONT.label, CozyBody: FONT.body },
});
```

`card.art` bir ART anahtarı **ya da** doğrudan bir URL olabilir. Gömülü base64
kullanan oyun anahtar verir, dosyadan yükleyen yol verir; paket ikisini de kabul
eder ve hangisi olduğunu bilmez.

**Adapter dışında pakete dokunma.** Oyuna özel bir kural pakete sızarsa paket o
oyuna çivilenir ve üçüncü oyunda çatallanır.

## Faz 2 — ölçüleri oyuna göre ayarla

Bütün ölçüler `CARD_LOOK` içinde tek nesnede ve `applyCardLook()` onları CSS
özel değişkenlerine yazıyor. **CSS ve JS aynı sayıyı okuyor** — kartı bir tık
büyütmek tek satır.

Ayarlarken:
- Oran her yerde aynı kalır. Farklı yoğunluk gerekiyorsa **ölçek** değiştir
  (`--k`), ikinci bir kart tasarlama.
- Kural metni 5–6 pikselin altına inerse kart işini yapmıyor demektir; oradan
  aşağısı ölçek değil düzen sorunudur.

## Faz 3 — sanat eşlemesi

`artmap.js` kartın hangi resmi çizeceğini seçer: **önce kartın kendi adı**
(`"Night Baker"` → `Illustration_NightBaker`), sonra anahtar kelime kuralı.

Yeni illüstrasyon eklendiğinde tabloya satır yazmak gerekmiyor — ad eşleşmesi
onu kendiliğinden bulur. Bu yüzden **kart adında kesme işareti kullanma**:
`"Baker's Kid"` → `"BakerSKid"` üretir, dosya `BakersKid`'dir, eşleşme kaçar ve
kart sessizce başkasının resmini çizer.

Bunu bir kapıyla koru:

> Adından türeyen anahtar bir illüstrasyona denk gelen kart, o illüstrasyonu
> KULLANMAK zorundadır.

## Faz 4 — pakete geri yaz

Bu skill'in asıl işi burada. Oyunda bir şey **düzelttiğinde**, düzeltme oyuna
özelse oyunda kalır; **pakete aitse pakete taşınır**. Ayrımı şu soru verir:

> Bu hata ikinci bir oyunda da olur muydu?

Olurdu diyorsan `~/Projects/deckcraft`'e taşı ve **neden** olduğunu yanına yaz.
Sayıyı yazma, sebebi yaz — sonraki okuyan sayıyı zaten görüyor.

Pakete taşınmış, ölçülmüş tuzaklar (hepsi yaşandı):

- `border-image` dilimi **yüzde** olmalı. Piksel dilim kaynağın kanonik
  ölçüsüne bağlanır; gömülü kopya yeniden ölçeklenince sol+sağ dilim kaynağın
  genişliğini aşar ve ortadaki `fill` yaması **sıfıra düşer** — elemanın ortası
  hiç çizilmez.
- **Dikey dilim sıfır olamaz**: `0 x fill` ile orta yamanın kaynak yüksekliği
  sıfırdır. Aynı sonuç, farklı sebep.
- 9-slice dikişi genelde süslemenin yerinden değil, sprite'ın eni boyunca giden
  **ışık geçişinden** gelir. Her sütunu merkez sütunla karşılaştır, farkın en
  küçük olduğu yerden kes.
- **Şablon dizesi içindeki yorumda ters tırnak** dizeyi kapatır; hata satırlar
  sonra patlar.
- WebGL'de `preserveDrawingBuffer` yokken `readPixels` **ölçüm için
  kullanılamaz** — sunumdan sonra tampon temizlenir, "0 piksel çizildi" yalan
  çıkar.
- Kart oranını iki yerde tanımlama. İkinci "yoğun" varyant, aynı kartı oyuncuya
  iki nesne olarak gösterir.

## Yapma

- **Paketi kopyalayıp oyuna gömme.** İki kopya bir gün ayrışır; ayrıştığı gün
  hangisinin doğru olduğunu kimse bilmez.
- **Adapter'ı atlayıp pakete oyunun tablolarını okutma.**
- **Sprite sheet üret diye kart animasyonu isteme** — bkz. `/animate`.
- **"Taşınabilir" deme.** Paket şu an tek oyundan çıkarıldı ve ikinci bir oyunda
  denenmedi; bağımlılıkları kesilmiş durumda, kanıtlanmış değil. İkinci oyunda
  çalıştığında bu satırı sil.
